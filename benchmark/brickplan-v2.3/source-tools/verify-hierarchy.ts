import { readFile, readdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { Matrix4 } from 'three';
import { LDrawLoader } from 'three/addons/loaders/LDrawLoader.js';
import { LDrawConditionalLineMaterial } from 'three/addons/materials/LDrawConditionalLineMaterial.js';
import { hash, splitMpd, resolveFile, normalize, header } from '../../../scripts/ldraw.ts';
import { writeNew } from './intake.ts';
import { sourceState } from './source-state.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
const HERE = sourceState(ROOT);
const OUTPUT = process.env.SOURCE_INTAKE_OUTPUT ?? '/tmp/brickplan-v23-work/source-intake';
const requested = process.argv.find(a => a.startsWith('--id='))?.slice(5);
const resultNames = (await readdir(resolve(HERE, 'results'))).filter(n => n.endsWith('.json')).sort();
for (const resultName of resultNames) {
  const intake = JSON.parse(await readFile(resolve(HERE, 'results', resultName), 'utf8'));
  if (intake.status !== 'manifest-ready' || (requested && intake.id !== requested)) continue;
  const reportPath = resolve(OUTPUT, 'hierarchy-checks', resultName);
  if (existsSync(reportPath)) {
    const old = JSON.parse(await readFile(reportPath, 'utf8'));
    if (old.status === 'pass' || !process.argv.includes('--retry-failed')) continue;
  }
  async function saveReport(text: string) {
    if (existsSync(reportPath)) {
      const previous = await readFile(reportPath);
      if (hash(previous) === hash(text)) return;
      await writeNew(resolve(OUTPUT, 'hierarchy-check-attempts', `${intake.id}-${hash(previous)}.json`), previous);
      await writeFile(reportPath, text);
    } else await writeNew(reportPath, text);
  }
  const warnings: string[] = [];
  const oldWarn = console.warn;
  try {
    const base = resolve(ROOT, 'web/public/models', intake.id);
    const manifestBytes = await readFile(resolve(base, 'manifest.json'));
    assert.equal(hash(manifestBytes), intake.manifestSha256);
    const manifest = JSON.parse(manifestBytes.toString());
    const provenanceBytes = await readFile(resolve(base, 'provenance.json'));
    assert.equal(hash(provenanceBytes), intake.provenanceSha256);
    const provenance = JSON.parse(provenanceBytes.toString());
    const original = await readFile(resolve(ROOT, manifest.sourceFile));
    assert.equal(hash(original), manifest.sourceHash);
    const packed = splitMpd(await readFile(resolve(base, 'model.packed.mpd'), 'utf8'));
    const dependencies: string[] = [];
    for (const dep of provenance.dependencyFiles) {
      const bytes = await readFile(resolve(ROOT, dep.path));
      assert.equal(hash(bytes), dep.sha256, `Dependency changed: ${dep.path}`);
      if (dep.origin === 'Historical hash-locked LDraw library') {
        dependencies.push(`0 FILE ${dep.file}\n${bytes.toString('utf8')}`);
      }
    }
    const colors = await readFile(resolve(base, 'LDConfig.ldr'), 'utf8');
    assert.equal(hash(colors), provenance.colorConfig.sha256);
    const loader = new LDrawLoader();
    loader.setConditionalLineMaterial(LDrawConditionalLineMaterial);
    const fileMap: Record<string, string> = {};
    for (const file of packed.values()) {
      for (const line of file.lines) {
        if (!/^1\s/.test(line.text)) continue;
        const name = line.text.split(/\s+/).slice(14).join(' ');
        fileMap[name] = resolveFile(packed, name).name;
      }
    }
    for (const dep of provenance.dependencyFiles) {
      const bytes = await readFile(resolve(ROOT, dep.path), 'utf8');
      const files = splitMpd(bytes, dep.file);
      for (const file of files.values()) for (const line of file.lines) {
        if (!/^1\s/.test(line.text)) continue;
        const name = line.text.split(/\s+/).slice(14).join(' ');
        fileMap[name] = resolveFile(packed, name).name;
      }
    }
    // Names in the original may differ from the namespace-resolved packed file.
    const originalFiles = splitMpd(original.toString('utf8'));
    for (const file of originalFiles.values()) {
      if (!packed.has(file.name)) continue;
      for (const line of file.lines) {
        if (!/^1\s/.test(line.text)) continue;
        const name = line.text.split(/\s+/).slice(14).join(' ');
        fileMap[name] = resolveFile(packed, name).name;
      }
    }
    loader.setFileMap(fileMap);
    console.warn = (...args) => warnings.push(args.map(String).join(' '));
    const text = original.toString('utf8').replace(/\n/, `\n${colors}\n`)
      + '\n' + dependencies.join('\n');
    // This pinned Three.js parser retains affine matrices before the rendering
    // path's matrix.decompose() loses shear present in some original OMR parts.
    const cache = (loader as any).partsCache.parseCache;
    const root = cache.parse(text);
    for (const [key, value] of Object.entries(cache._cache)) {
      const normalized = normalize(key);
      assert(!cache._cache[normalized] || cache._cache[normalized] === value, `Cache name collision: ${key}`);
      cache._cache[normalized] = value;
    }
    console.warn = oldWarn;
    assert.equal(warnings.length, 0, `Loader warnings: ${warnings.join('; ')}`);
    const remaining = new Map<string, any[]>();
    for (const part of manifest.instances) {
      const key = `${part.partNumber}:${part.colorCode}`;
      const list = remaining.get(key) ?? [];
      list.push(part);
      remaining.set(key, list);
    }
    let maximumMatrixError = 0, compared = 0;
    function visit(info: any, world: Matrix4, color: string, name: string, ancestors: Set<string>) {
      assert(!ancestors.has(name), `Independent parser cycle: ${name}`);
      const isModel = name.endsWith('.ldr') || /(?:^|_)Model\b/.test(header(packed.get(name)!, '!LDRAW_ORG'));
      if (!isModel) {
        const number = name.replace(/^parts\//, '').replace(/\.dat$/, '');
        const key = `${number}:${color}`;
        const candidates = remaining.get(key) ?? [];
        const match = candidates.findIndex(p => p.originalMatrix.every(
          (n: number, i: number) => Math.abs(n - world.elements[i]) < 1e-8));
        assert(match >= 0, `Unmatched original instance ${number} color=${color}`);
        const [candidate] = candidates.splice(match, 1);
        maximumMatrixError = Math.max(maximumMatrixError, ...candidate.originalMatrix.map(
          (n: number, i: number) => Math.abs(n - world.elements[i])));
        compared++;
        return;
      }
      assert.equal(info.faces.length + info.lineSegments.length + info.conditionalSegments.length, 0,
        `Direct geometry in model would be omitted by part-only manifest: ${name}`);
      const next = new Set([...ancestors, name]);
      for (const ref of info.subobjects) {
        const childName = normalize(ref.fileName);
        const child = cache.getData(childName, false);
        assert(child && !(child instanceof Promise), `Unresolved parser dependency ${childName}`);
        const childColor = ['16', '4294967295'].includes(ref.colorCode) ? color : ref.colorCode;
        visit(child, world.clone().multiply(ref.matrix), childColor, childName, next);
      }
    }
    visit(root, new Matrix4().makeScale(0.4, -0.4, -0.4), '7', manifest.rootFile, new Set());
    assert.equal(compared, manifest.instances.length);
    assert.equal([...remaining.values()].reduce((n, rows) => n + rows.length, 0), 0);
    await saveReport(JSON.stringify({
      id: intake.id, status: 'pass',
      method: 'Three.js 0.180.0 LDrawParsedCache parses original hierarchical MPD; independent traversal of parser matrices before lossy render-object decomposition',
      originalSha256: manifest.sourceHash, manifestSha256: intake.manifestSha256,
      instancesCompared: compared, partAndColorMatches: compared,
      maximumMatrixError, tolerance: 1e-8, warnings, geometryQualification: null,
      namespaceAdapter: 'Trim/case/slash normalization for FILE cache keys; unused embedded definitions are not root instances.',
      limitation: 'Pose and source/color coverage audit, not collision, stud support, or full LEGO inventory verification.',
    }, null, 2) + '\n');
    console.log(`HIERARCHY PASS ${intake.id} instances=${compared} error=${maximumMatrixError}`);
  } catch (error: any) {
    console.warn = oldWarn;
    await saveReport(JSON.stringify({
      id: intake.id, status: 'failed', error: error.message, warnings,
      geometryQualification: null,
    }, null, 2) + '\n');
    console.error(`HIERARCHY FAILED ${intake.id}: ${error.message}`);
  }
}
