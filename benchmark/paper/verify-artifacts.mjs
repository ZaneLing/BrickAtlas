/** Current release verifier. Historical attestations stay in versioned evidence files. */
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
const root = resolve(import.meta.dirname, '../..'), data = resolve(root, 'benchmark/ldraw-v1');
const read = p => JSON.parse(readFileSync(p, 'utf8'));
const hash = p => createHash('sha256').update(readFileSync(p)).digest('hex');
const release = read(resolve(data, 'release.json')), verification = read(resolve(data, 'verification.json'));
assert.equal(release.version, 'brickatlas-ldraw-1');
assert.equal(release.models, 24); assert.equal(release.tasks, 617); assert.equal(release.parts, 15334);
assert.equal(verification.sources, release.models); assert.equal(verification.instances, release.parts);
assert.equal(verification.tasks, release.tasks);
assert.equal(verification.negativeControls, 1606);
assert.equal(release.measuredModelResults, 0);
const catalog = read(resolve(data, 'catalog.json'));
assert.deepEqual(read(resolve(root, 'public/benchmark/catalog.json')), catalog);
assert.deepEqual(read(resolve(root, 'public/benchmark/ldraw/catalog.json')), catalog);
assert.equal(existsSync(resolve(root, 'public/benchmark/models')), false, 'Synthetic models remain in the active site');
const capture = read(resolve(data, 'capture.json'));
assert.equal(capture.models.length, release.models);
for (const m of capture.models) {
  const entry = catalog.find(e => e.id === m.id);
  assert.equal(m.sourceHash, entry.sourceHash); assert.equal(m.loadedInstances, entry.parts);
  assert.equal(m.numberedRenderVersion, 2);
  assert.deepEqual(m.errors, []);
  for (const img of m.images) assert.equal(hash(resolve(root, 'benchmark/paper/figures/ldraw', img.file)), img.sha256);
}
const inputs = read(resolve(data, 'input-renders.json'));
const visualIds = new Set();
for (const entry of catalog) {
  const b = read(resolve(root, 'public/benchmark/ldraw/models', entry.id + '.json'));
  const input = read(resolve(root, 'public/benchmark/ldraw/inputs', entry.id + '.json'));
  assert.equal(b.parts.length, entry.parts); assert.equal(input.tasks.length, b.tasks.length);
  assert.equal(hash(resolve(root, 'public/benchmark/ldraw/sources', entry.id + '.mpd')), entry.sourceHash);
  assert.equal(b.audit.duplicatePlacements, 0);
  assert.ok(b.audit.connectorCoverage >= .9);
  for (const t of input.tasks) {
    assert.ok(!('answer' in t) && !('evidenceDetail' in t));
    if (t.modality === 'visual') {
      visualIds.add(t.id);
      assert.deepEqual(t.input, {});
      assert.ok(!('sourceModel' in t.visualInput));
      const image = inputs.images.find(r => r.taskId === t.id);
      assert.ok(image); assert.equal(image.renderVersion, 2); assert.deepEqual(image.references, t.references);
      assert.equal(hash(resolve(root, 'public', t.visualInput.numberedView)), image.sha256);
    }
  }
}
assert.equal(visualIds.size, 140); assert.equal(inputs.images.length, 140);
const worked = read(resolve(data, 'worked-renders.json'));
assert.equal(worked.frames.length, 6);
for (const f of worked.frames) assert.equal(hash(resolve(root, 'benchmark/paper/figures/ldraw', f.file)), f.sha256);
const derivatives = read(resolve(data, 'figure-derivatives.json'));
for (const image of derivatives.images) {
  assert.equal(hash(resolve(root, 'benchmark/paper/figures/ldraw', image.source)), image.sourceSha256);
  assert.equal(hash(resolve(root, 'benchmark/paper/figures/ldraw', image.file)), image.sha256);
}
const browserTests = read(resolve(data, 'browser-tests.json'));
assert.equal(browserTests.stats.expected, 3); assert.equal(browserTests.stats.unexpected, 0);
assert.equal(browserTests.stats.flaky, 0);
for (const name of ['main', 'supplement']) {
  const report = read(resolve(root, 'benchmark/paper', name === 'main' ? 'pdf-verification.json' : 'supplement-verification.json'));
  assert.equal(hash(resolve(root, 'benchmark/paper', name + '.pdf')), report.pdfSha256);
  assert.equal(hash(resolve(root, 'public/benchmark/docs', name + '.pdf')), report.pdfSha256);
  assert.equal(report.cjkTextFound, false);
  assert.equal(report.overfullBoxes, false);
  assert.equal(report.unresolvedCitationsOrReferences, false);
}
const files = [
  'benchmark/suite/ldraw/release.ts', 'benchmark/suite/ldraw/questions.ts', 'benchmark/suite/ldraw/verify.ts',
  'benchmark/suite/ldraw/audit.py', 'src/benchmark/LDrawBenchmarkPage.tsx', 'src/benchmark/NumberedOverlay.ts',
  'src/benchmark/ldrawTypes.ts', 'src/benchmark/ldrawReviewStore.ts', 'src/workers/geometry.worker.ts',
  'src/scene/AtlasScene.ts', 'src/benchmark/engine.ts', 'benchmark/paper/main.tex', 'benchmark/paper/supplement.tex',
  'benchmark/ldraw-v1/release.json', 'benchmark/ldraw-v1/verification.json', 'benchmark/ldraw-v1/capture.json',
  'benchmark/ldraw-v1/input-renders.json', 'benchmark/ldraw-v1/figure-derivatives.json',
  'benchmark/ldraw-v1/browser-tests.json', 'benchmark/ldraw-v1/tool-evidence.json',
  'benchmark/suite/ldraw/paper.py', 'benchmark/suite/ldraw/score.ts',
];
const evidence = { version: release.version, models: release.models, parts: release.parts, tasks: release.tasks,
  visualInputs: visualIds.size, canonicalViews: capture.models.length * 4, workedFrames: worked.frames.length,
  hashes: Object.fromEntries(files.map(p => [p, hash(resolve(root, p))])) };
writeFileSync(resolve(root, 'benchmark/paper/ldraw-evidence.json'), JSON.stringify(evidence, null, 2) + '\n');
console.log(JSON.stringify({ ...evidence, hashes: undefined }));
