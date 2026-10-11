import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { dirname, resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { Matrix4 } from 'three';
import { readZip } from '../../../scripts/readZip.ts';
import { sourceState } from './source-state.mjs';
import {
  splitMpd, reference, normalize, resolveFile, dependencyClosure,
  buildManifest, header, hash, referenceLine, type LDrawFile,
} from '../../../scripts/ldraw.ts';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
const HERE = sourceState(ROOT);
const RAW = resolve(ROOT, 'assets-source/brickplan-v23');
const LOCKED = resolve(ROOT, 'assets-source/ldraw-library/locked');
const registryPath = resolve(HERE, 'candidate-registry.frozen.json');

export async function writeNew(path: string, data: string | Buffer) {
  const bytes = Buffer.isBuffer(data) ? data : Buffer.from(data);
  await mkdir(dirname(path), { recursive: true });
  try {
    await writeFile(path, bytes, { flag: 'wx' });
  } catch (error: any) {
    if (error.code !== 'EEXIST') throw error;
    assert.equal(hash(await readFile(path)), hash(bytes), `Refusing overwrite: ${path}`);
  }
}

const json = (value: unknown) => JSON.stringify(value, null, 2) + '\n';
const identity = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
const axis = [0.4, 0, 0, 0, 0, -0.4, 0, 0, 0, 0, -0.4, 0, 0, 0, 0, 1];

// Independent row-major arithmetic checks the Three.js column-major manifest.
export function multiply(a: number[], b: number[]) {
  return a.map((_, index) => {
    const row = Math.floor(index / 4), column = index % 4;
    return [0, 1, 2, 3].reduce((sum, k) => sum + a[row * 4 + k] * b[k * 4 + column], 0);
  });
}

export function independentRows(files: Map<string, LDrawFile>, root: string) {
  const rows: { sourceFile: string; sourceLine: number; partNumber: string;
    colorCode: string; world: number[]; columnMajor: number[] }[] = [];
  function walk(name: string, parent: number[], color: string, ancestors: Set<string>) {
    const file = resolveFile(files, name);
    assert(!ancestors.has(file.name), 'Cyclic model');
    const next = new Set([...ancestors, file.name]);
    for (const { text, line } of file.lines) {
      if (!/^1\s/.test(text)) continue;
      const t = text.split(/\s+/), n = t.slice(2, 14).map(Number);
      assert(n.length === 12 && n.every(Number.isFinite));
      const [x, y, z, a, b, c, d, e, f, g, h, i] = n;
      const world = multiply(parent, [a, b, c, x, d, e, f, y, g, h, i, z, 0, 0, 0, 1]);
      const child = resolveFile(files, t.slice(14).join(' '));
      const resolvedColor = ['16', '4294967295'].includes(t[1]) ? color : t[1];
      if (child.name.endsWith('.ldr') || /(?:^|_)Model\b/.test(header(child, '!LDRAW_ORG'))) {
        walk(child.name, world, resolvedColor, next);
      } else {
        const display = multiply(axis, world);
        rows.push({
          sourceFile: file.name, sourceLine: line,
          partNumber: child.name.replace(/^parts\//, '').replace(/\.dat$/, ''),
          colorCode: resolvedColor, world,
          columnMajor: display.map((_, k) => display[(k % 4) * 4 + Math.floor(k / 4)]),
        });
      }
    }
  }
  walk(root, identity, '7', new Set());
  return rows;
}

export function validateTransforms(files: Map<string, LDrawFile>, root: string, instances: any[]) {
  const independentlyFlattened = independentRows(files, root);
  assert.equal(instances.length, independentlyFlattened.length, 'Full source coverage');
  let maxCompositionError = 0, maxRoundTripError = 0, reflected = 0, nonRigid = 0;
  instances.forEach((part, index) => {
    const expected = independentlyFlattened[index];
    for (const key of ['sourceFile', 'sourceLine', 'partNumber', 'colorCode'] as const) {
      assert.equal(part[key], expected[key], `${index}:${key}`);
    }
    const error = Math.max(...part.originalMatrix.map(
      (v: number, k: number) => Math.abs(v - expected.columnMajor[k])));
    maxCompositionError = Math.max(error, maxCompositionError);
    assert(error < 1e-8, `Composition mismatch ${index}: ${error}`);
    const round = reference(referenceLine(part), 0).matrix.elements;
    const expectedColumn = expected.world.map(
      (_, k) => expected.world[(k % 4) * 4 + Math.floor(k / 4)]);
    const roundError = Math.max(...round.map((v, k) => Math.abs(v - expectedColumn[k])));
    maxRoundTripError = Math.max(roundError, maxRoundTripError);
    assert(roundError < 1e-8, `Round-trip mismatch ${index}`);
    const matrix = new Matrix4().fromArray(expectedColumn);
    const determinant = matrix.determinant();
    if (determinant < 0) reflected++;
    let orthogonalityError = 0;
    for (let a = 0; a < 3; a++) for (let b = 0; b < 3; b++) {
      const dot = [0, 1, 2].reduce(
        (sum, k) => sum + expected.world[k * 4 + a] * expected.world[k * 4 + b], 0);
      orthogonalityError = Math.max(orthogonalityError, Math.abs(dot - Number(a === b)));
    }
    if (orthogonalityError > 1e-5 || Math.abs(Math.abs(determinant) - 1) > 1e-5) nonRigid++;
  });
  return {
    instancesChecked: instances.length, maxCompositionError, maxRoundTripError,
    sourceReflectionsPreserved: reflected, sourceNonRigidTransformsPreserved: nonRigid,
    matricesRepaired: 0, instancesDropped: 0, geometryQualificationRun: false,
  };
}

async function download(url: string, path: string) {
  if (existsSync(path)) return readFile(path);
  assert(url.startsWith('https://library.ldraw.org/library/omr/'));
  let bytes: Buffer | undefined;
  for (let attempt = 0; attempt < 4; attempt++) {
    try {
      bytes = execFileSync('curl', ['--compressed', '-fLsS', '--connect-timeout', '10',
        '--max-time', '300', url], { maxBuffer: 32 * 1024 * 1024, timeout: 305000 });
      break;
    } catch (error) {
      if (attempt === 3) throw error;
    }
  }
  assert(bytes && bytes.length && !bytes.subarray(0, 100).toString().includes('<!DOCTYPE'));
  await writeNew(path, bytes);
  return bytes;
}

async function run() {
  const registryBytes = await readFile(registryPath);
  const frozenHash = (await readFile(resolve(HERE, 'candidate-registry.frozen.sha256'), 'utf8')).split(' ')[0];
  assert.equal(hash(registryBytes), frozenHash, 'Registry changed after freeze');
  const registry = JSON.parse(registryBytes.toString('utf8'));
  assert.equal(registry.geometryOrPolicySelectionPerformed, false);
  assert.equal(new Set(registry.candidates.map((c: any) => c.kit)).size, registry.count);
  const globalProvenance = JSON.parse(await readFile(resolve(ROOT, 'assets-source/provenance.json'), 'utf8'));
  const archiveRecord = globalProvenance.resources.find((r: any) => r.file.endsWith('complete.zip'));
  const archive = await readFile(resolve(ROOT, archiveRecord.file));
  assert.equal(hash(archive), archiveRecord.sha256, 'Historical archive hash mismatch');
  const archiveEntries = new Map((await readZip(archive))
    .map(e => [normalize(e.entryName.replace(/^ldraw\//, '')), e]));
  const oldLock = JSON.parse(await readFile(resolve(ROOT, 'assets-source/library-lock.json'), 'utf8'));
  const cache = new Map<string, { bytes: Buffer; path: string; sha256: string }>();
  async function libraryFile(name: string) {
    const found = cache.get(name);
    if (found) return found;
    const entry = archiveEntries.get(name);
    const oldPath = resolve(LOCKED, name);
    let bytes: Buffer;
    if (existsSync(oldPath)) {
      bytes = await readFile(oldPath);
      const expected = oldLock[name] ?? (entry ? hash(await entry.getData()) : null);
      assert(expected, `Existing dependency has no verifiable lock: ${name}`);
      assert.equal(hash(bytes), expected, `Historical dependency mismatch: ${name}`);
    } else {
      assert(entry, `Missing dependency in locked archive: ${name}`);
      bytes = await entry.getData();
      await writeNew(oldPath, bytes);
    }
    const record = { bytes, path: relative(ROOT, oldPath), sha256: hash(bytes) };
    cache.set(name, record);
    return record;
  }
  const color = await libraryFile('ldconfig.ldr');
  const range = process.argv.find(a => a.startsWith('--range='))?.slice(8);
  const [start, end] = range ? range.split(':').map(Number) : [1, registry.count];
  for (const candidate of registry.candidates.slice(start - 1, end)) {
    const reportPath = resolve(HERE, 'results', `${candidate.id}.json`);
    if (existsSync(reportPath)) {
      console.log(`Existing result ${candidate.id}`);
      continue;
    }
    let sourceHash: string | null = null;
    try {
      const detail = JSON.parse(await readFile(resolve(HERE, 'details', `${candidate.kit}.json`), 'utf8'));
      assert.equal(detail.sourceUrl, candidate.sourceUrl);
      const model = detail.models.find((m: any) => m.pageModelLabel === 'Main Model')
        ?? [...detail.models].sort((a: any, b: any) => a.downloadUrl.localeCompare(b.downloadUrl))[0];
      assert(model?.pageAuthor && Object.values(model.completeness).every(v => ['Yes', 'No'].includes(String(v))));
      Object.assign(candidate, detail, model);
      const filename = decodeURIComponent(new URL(candidate.downloadUrl).pathname.split('/').at(-1)!);
      assert(/^[\w .-]+\.(mpd|ldr)$/i.test(filename));
      const sourcePath = resolve(RAW, 'original', filename);
      const sourceBytes = await download(candidate.downloadUrl, sourcePath);
      sourceHash = hash(sourceBytes);
      const source = sourceBytes.toString('utf8');
      assert.equal(hash(Buffer.from(source)), sourceHash, 'Source is not lossless UTF-8');
      const files = splitMpd(source, filename);
      const embedded = new Set(files.keys()), root = files.keys().next().value!;
      const dependencies = new Map<string, any>();
      const visited = new Set<string>();
      async function load(name: string): Promise<LDrawFile> {
        const keys = [name, `parts/${name}`, `p/${name}`, `models/${name}`].map(normalize);
        const present = keys.find(k => files.has(k));
        if (present) return files.get(present)!;
        const key = keys.find(k => archiveEntries.has(k) || existsSync(resolve(LOCKED, k)));
        assert(key, `Unresolved original dependency: ${name}`);
        const record = await libraryFile(key);
        const text = record.bytes.toString('utf8');
        assert.equal(hash(Buffer.from(text)), record.sha256, `Non-UTF8 dependency ${key}`);
        const file = splitMpd(text, key).get(key)!;
        files.set(key, file);
        dependencies.set(key, {
          file: key, path: record.path, sha256: record.sha256,
          author: header(file, 'Author:'), license: header(file, '!LICENSE'),
          origin: 'Historical hash-locked LDraw library',
          archiveSha256: archiveRecord.sha256,
        });
        return file;
      }
      async function collect(name: string) {
        const file = await load(name);
        if (visited.has(file.name)) return;
        visited.add(file.name);
        for (const { text, line } of file.lines) {
          if (/^1\s/.test(text)) await collect(reference(text, line).file);
        }
      }
      await collect(root);
      const closure = dependencyClosure(files, root);
      const semantics = buildManifest(files, root, color.bytes.toString('utf8'), () => 'body');
      const transforms = validateTransforms(files, root, semantics.instances);
      const author = header(files.get(root)!, 'Author:');
      const license = header(files.get(root)!, '!LICENSE');
      assert(author && license);
      const output = resolve(ROOT, 'web/public/models', candidate.id);
      const embeddedConflicts: any[] = [];
      for (const name of closure.filter(n => embedded.has(n))) {
        const file = files.get(name)!;
        const path = resolve(RAW, 'embedded', candidate.id, name);
        assert(path.startsWith(resolve(RAW, 'embedded', candidate.id) + '/'));
        await writeNew(path, file.text);
        dependencies.set(name, {
          file: name, path: relative(ROOT, path), sha256: hash(file.text),
          author: header(file, 'Author:'), license: header(file, '!LICENSE'),
          origin: 'Embedded MPD section; parser-normalized LF; original container preserved',
          containerSha256: sourceHash,
        });
      }
      for (const instance of semantics.instances) {
        const part = resolveFile(files, `${instance.partNumber}.dat`);
        if (!embedded.has(part.name)) continue;
        const path = resolve(LOCKED, 'parts', `${instance.partNumber}.dat`);
        assert(path.startsWith(LOCKED + '/parts/'));
        if (existsSync(path) && hash(await readFile(path)) !== hash(part.text)) {
          embeddedConflicts.push({ partNumber: instance.partNumber,
            existingSha256: hash(await readFile(path)), sourceSha256: hash(part.text) });
        } else await writeNew(path, part.text);
      }
      const manifest = {
        version: 1, schema: 'brickplan-original-source-manifest/1.0',
        model: { id: candidate.id, setNumber: candidate.setNumber, title: candidate.title,
          theme: candidate.theme, year: Number(candidate.year), author, license,
          sourceUrl: candidate.sourceUrl, downloadUrl: candidate.downloadUrl,
          notes: ['Original OMR source pose; no mesh rendering or geometry qualification performed.'] },
        sourceHash, candidateRegistrySha256: frozenHash, sourceFile: relative(ROOT, sourcePath),
        rootFile: root, independenceGroup: candidate.independenceGroup,
        sourceProfile: 'Entire selected original MPD root, including all model references.',
        transformConvention: 'Column-major diag(0.4,-0.4,-0.4,1) * composed LDraw transform',
        instances: semantics.instances.map(({ bounds, ...part }) => ({
          ...part, sourcePartSha256: dependencies.get(resolveFile(files, `${part.partNumber}.dat`).name).sha256,
        })),
        submodels: semantics.submodels,
        stats: { instances: semantics.instances.length,
          uniqueParts: new Set(semantics.instances.map(p => p.partNumber)).size,
          colors: new Set(semantics.instances.map(p => p.colorCode)).size },
        geometryQualification: null, renderedGeometry: null, bounds: null,
      };
      const provenance = {
        schema: 'brickplan-source-intake-provenance/1.0',
        candidateRegistrySha256: frozenHash, model: manifest.model,
        source: { path: relative(ROOT, sourcePath), sha256: sourceHash, bytes: sourceBytes.length },
        page: { url: candidate.sourceUrl, sha256: candidate.pageSha256,
          author: candidate.pageAuthor, modelLabel: candidate.pageModelLabel,
          completeness: candidate.completeness },
        authorHeaderMatchesPage: author === candidate.pageAuthor,
        library: archiveRecord, colorConfig: { path: color.path, sha256: color.sha256 },
        changes: ['Semantic flattening only; all original transforms, part references and colors retained.',
          'No pose normalization, substitution, pruning, editorial group selection or mesh generation.'],
        embeddedPartLockedPathConflicts: [...new Map(embeddedConflicts.map(x => [x.partNumber, x])).values()],
        dependencyFiles: closure.map(name => dependencies.get(name)),
        transformValidation: transforms, geometryQualification: null,
      };
      await writeNew(resolve(output, 'manifest.json'), json(manifest));
      await writeNew(resolve(output, 'provenance.json'), json(provenance));
      await writeNew(resolve(output, 'attribution.txt'),
        `${candidate.setNumber} ${candidate.title}\nModel author: ${author}\n${license}\n` +
        `Original: ${candidate.downloadUrl}\nOMR: ${candidate.sourceUrl}\n` +
        `Original SHA256: ${sourceHash}\nFull per-file authors/licenses: provenance.json\n` +
        'Source-only semantic flattening; no geometry qualification or physical completeness claim.\n');
      await writeNew(resolve(output, 'LDConfig.ldr'), color.bytes);
      await writeNew(resolve(output, 'assembly.ldr'), [
        `0 ${candidate.setNumber} ${candidate.title} - source-faithful flat assembly`,
        `0 Author: ${author}`, `0 !LICENSE ${license}`,
        `0 // Derived from original SHA256 ${sourceHash}; only hierarchy flattened.`,
        ...semantics.instances.map(referenceLine), '',
      ].join('\n'));
      const packed = [root, ...closure.filter(name => name !== root)].map(name => {
        const file = files.get(name)!;
        const text = file.text.split('\n').map(line => {
          if (!/^1\s/.test(line.trim())) return line;
          const tokens = line.trim().split(/\s+/);
          return [...tokens.slice(0, 14), resolveFile(files, tokens.slice(14).join(' ')).name].join(' ');
        }).join('\n');
        return `0 FILE ${name}\n${text}`;
      }).join('\n');
      await writeNew(resolve(output, 'model.packed.mpd'), packed);
      await writeNew(reportPath, json({
        id: candidate.id, kit: candidate.kit, status: 'manifest-ready', sourceHash,
        sourceFile: relative(ROOT, sourcePath), manifestFile: relative(ROOT, resolve(output, 'manifest.json')),
        manifestSha256: hash(json(manifest)), provenanceSha256: hash(json(provenance)),
        author, license, stats: manifest.stats, dependencies: closure.length, transforms,
        embeddedPartLockedPathConflicts: provenance.embeddedPartLockedPathConflicts,
        geometryQualification: null, candidateRegistrySha256: frozenHash,
      }));
      console.log(`READY ${candidate.id} instances=${manifest.stats.instances} parts=${manifest.stats.uniqueParts}`);
    } catch (error: any) {
      await writeNew(reportPath, json({
        id: candidate.id, kit: candidate.kit, status: 'intake-failed', sourceHash,
        error: error.message, candidateRegistrySha256: frozenHash, geometryQualification: null,
      }));
      console.error(`FAILED ${candidate.id}: ${error.message}`);
    }
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) await run();
