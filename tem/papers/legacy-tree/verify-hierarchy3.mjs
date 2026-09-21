import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
const paper = import.meta.dirname, root = resolve(paper, '../..'), data = resolve(root, 'benchmark/hierarchy-v3');
const read = p => JSON.parse(readFileSync(p, 'utf8'));
const hash = p => createHash('sha256').update(readFileSync(p)).digest('hex');
const evidence = read(resolve(paper, 'hierarchy3-evidence.json'));
for (const [path, expected] of Object.entries(evidence.hashes))
  assert.equal(hash(resolve(data, path)), expected, path);
assert.equal(evidence.sourceObjects, 48); assert.equal(evidence.tasks, 2304);
assert.equal(evidence.parts, 6339); assert.equal(evidence.actionSolverSuccess, 384);
const manifest = read(resolve(data, 'manifest.json'));
for (const [path, expected] of Object.entries(manifest.files)) assert.equal(hash(resolve(root, path)), expected, path);
const run = read(resolve(data, 'pilot/run.json'));
assert.equal(run.publicHash, hash(resolve(data, 'public.json')));
assert.equal(run.status, 'complete'); assert.equal(run.results.length, 16);
assert.equal(run.results.reduce((s, r) => s + r.verdict.success, 0), 7);
assert.ok(Math.abs(run.results.reduce((s, r) => s + r.call.cost, 0) - (run.after - run.before)) < 1e-9);
assert.ok(run.after - run.before < 0.10);
for (const r of run.results) assert.equal(hash(resolve(data, 'images', `${r.id.slice(3, -r.family.length - 1)}-iso.png`)), r.imageHash);
const catalog = read(resolve(data, 'catalog.json'));
for (const m of catalog) {
  assert.equal(hash(resolve(data, 'models', `${m.id}.json`)),
    hash(resolve(root, 'public/benchmark/models', `${m.id}.json`)));
  const b = read(resolve(data, 'models', `${m.id}.json`));
  assert.equal(b.validation.penetrations.length, 0);
  assert.ok(b.physics.nominalWithinTolerance);
}
const renders = read(resolve(data, 'render-audit.json'));
assert.equal(renders.frames.length, 192);
for (const f of renders.frames) assert.equal(hash(resolve(data, f.file)), f.sha256);
const ui = read(resolve(data, 'web-verification/report.json'));
assert.equal(ui.desktopModels.length, 48); assert.equal(ui.mobileModels, 4); assert.deepEqual(ui.errors, []);
for (const name of ['main.pdf', 'supplement.pdf', 'main.zh-CN.md']) assert.equal(hash(resolve(paper, name)),
  hash(resolve(root, 'public/benchmark/docs', name)), `website ${name}`);
for (const name of ['REPORT.zh-CN.md', 'QUESTION_BANK.zh-CN.md', 'ERRATA.zh-CN.md']) assert.equal(hash(resolve(data, name)),
  hash(resolve(root, 'public/benchmark/docs', name)), `website ${name}`);
for (const [name, report] of [['main', 'pdf-verification'], ['supplement', 'supplement-verification']]) {
  const check = read(resolve(paper, `${report}.json`));
  assert.equal(check.pdfSha256, hash(resolve(paper, `${name}.pdf`)));
  assert.equal(check.overfullBoxes, false); assert.equal(check.unresolvedCitationsOrReferences, false);
}
console.log(JSON.stringify({ hierarchy3Verified: true, objects: 48, tasks: 2304, desktopModels: 48, views: 192, mobileModels: 4 }));
