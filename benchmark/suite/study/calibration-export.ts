import assert from 'node:assert/strict';
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { PNG } from 'pngjs';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { SYSTEM } from '../storage';
import { SuiteRenderer } from '../render';
import { taskForV2 } from '../v2/cases';
import { sourceHashes } from '../v2/build';
import { STUDY } from './protocol';
import { calibrationSelection } from './calibration';

const DIRECTORY = resolve(STUDY, 'calibration');
export function calibrationProtocol() {
  const protocol = JSON.parse(readFileSync(resolve(DIRECTORY, 'protocol.json'), 'utf8'));
  const selected = calibrationSelection();
  assert.equal(protocol.version, 'calibration-v1');
  assert.equal(protocol.hash, digest(selected.cases));
  assert.deepEqual(protocol.cases, selected.cases);
  assert.deepEqual(protocol.sourceHashes, sourceHashes());
  assert.equal(protocol.excludedGroupsHash, digest(selected.excluded));
  return { protocol, ...selected };
}

export function imageEvidence(bytes: Buffer) {
  const png = PNG.sync.read(bytes), colors = new Set<string>();
  assert.equal(png.width, 640); assert.equal(png.height, 480);
  for (let i = 0; i < png.data.length; i += 16) colors.add(png.data.subarray(i, i + 3).toString('hex'));
  assert.ok(colors.size > 32, 'Blank or unexpectedly uniform calibration image');
  return { hash: digest(bytes.toString('base64')), width: png.width, height: png.height, sampledColors: colors.size };
}

export async function exportCalibration(renderer: SuiteRenderer) {
  const { protocol, cases } = calibrationProtocol();
  const out = resolve(DIRECTORY, 'inputs');
  if (existsSync(resolve(out, 'manifest.json'))) return verifyCalibrationInputs();
  mkdirSync(resolve(out, 'images'), { recursive: true });
  const framePaths = new Map<string, string>(), images: Record<string, ReturnType<typeof imageEvidence>> = {};
  const rows = [];
  for (const [index, spec] of cases.entries()) {
    const task = taskForV2(spec), paths = [];
    for (const frame of task.frames) {
      const recipe = digest(frame);
      let path = framePaths.get(recipe);
      if (!path) {
        const rendered = await renderer.render(frame), evidence = imageEvidence(rendered.buffer);
        assert.equal(evidence.hash, rendered.hash);
        path = `images/${evidence.hash}.png`;
        writeFileSync(resolve(out, path), rendered.buffer);
        framePaths.set(recipe, path); images[path] = evidence;
      }
      paths.push(path);
    }
    // Only public task fields and permitted PNGs enter the model bundle.
    rows.push({ caseId: spec.id, system: SYSTEM, input: task.public, images: paths });
    if ((index + 1) % 100 === 0) console.log(JSON.stringify({ exported: index + 1, total: cases.length }));
  }
  const raw = rows.map(row => JSON.stringify(row)).join('\n') + '\n';
  writeFileSync(resolve(out, 'public.jsonl'), raw);
  const manifest = { version: 'calibration-inputs-1', status: 'complete', protocolHash: protocol.hash,
    publicHash: digest(raw), cases: rows.length, imageUses: rows.reduce((n, row) => n + row.images.length, 0),
    uniqueImages: Object.keys(images).length, images,
    framePaths: Object.fromEntries(framePaths), modelCalls: 0, apiRequests: 0,
    scope: 'Development validation inputs only. Public JSONL and images are the participant bundle; manifest is evaluator metadata. RGB cases also include BOM. No neural evaluation or independent human audit implied.' };
  // Manifest is the completion marker; a failed export is never counted complete.
  atomicJson(resolve(out, 'manifest.json'), manifest);
  return verifyCalibrationInputs();
}

export function verifyCalibrationInputs() {
  const { protocol, cases, objects } = calibrationProtocol();
  const out = resolve(DIRECTORY, 'inputs'), manifest = JSON.parse(readFileSync(resolve(out, 'manifest.json'), 'utf8'));
  assert.equal(manifest.version, 'calibration-inputs-1'); assert.equal(manifest.status, 'complete');
  assert.equal(manifest.protocolHash, protocol.hash);
  const raw = readFileSync(resolve(out, 'public.jsonl'), 'utf8');
  assert.equal(digest(raw), manifest.publicHash);
  const rows = raw.trim().split('\n').map(line => JSON.parse(line));
  assert.deepEqual(rows.map(row => row.caseId), cases.map(s => s.id));
  const images = new Set<string>(), recipes = new Set<string>();
  for (const [i, row] of rows.entries()) {
    const task = taskForV2(cases[i]);
    assert.deepEqual(Object.keys(row).sort(), ['caseId', 'images', 'input', 'system']);
    assert.equal(row.system, SYSTEM); assert.deepEqual(row.input, task.public);
    assert.equal(row.images.length, task.frames.length);
    for (const [j, path] of row.images.entries()) {
      assert.match(path, /^images\/[a-f0-9]{64}\.png$/);
      const recipe = digest(task.frames[j]); recipes.add(recipe);
      assert.equal(manifest.framePaths[recipe], path);
      if (!images.has(path)) {
        const evidence = imageEvidence(readFileSync(resolve(out, path)));
        assert.equal(path, `images/${evidence.hash}.png`);
        assert.deepEqual(evidence, manifest.images[path]);
        images.add(path);
      }
    }
  }
  assert.equal(manifest.cases, rows.length);
  assert.equal(manifest.uniqueImages, images.size);
  assert.deepEqual(Object.keys(manifest.images).sort(), [...images].sort());
  assert.deepEqual(Object.keys(manifest.framePaths).sort(), [...recipes].sort());
  assert.deepEqual(readdirSync(resolve(out, 'images')).map(name => `images/${name}`).sort(), [...images].sort());
  const imageUses = rows.reduce((n, row) => n + row.images.length, 0);
  assert.equal(manifest.imageUses, imageUses);
  const report = { protocolHash: protocol.hash, cases: rows.length, sourceGroups: objects.length,
    coverage: [...new Set(objects.map(o => o.policy))].flatMap(policy => ['small', 'medium', 'large'].map(difficulty => ({
      policy, difficulty, selectedObjects: objects.filter(o => o.policy === policy && o.difficulty === difficulty).length,
    }))),
    imageUses, uniqueImages: images.size, allPublicInputsMatch: true, imageHashesVerified: true,
    allImagesNonblank: true, modelCalls: 0, apiRequests: 0,
    limitation: 'Hash and recipe association checks, not a second-renderer proof or fresh rasterization during offline replay.' };
  atomicJson(resolve(DIRECTORY, 'input-verification.json'), report);
  return report;
}
