import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
const paper = import.meta.dirname, root = resolve(paper, '../..'), data = resolve(root, 'benchmark/hierarchy-v2');
const read = p => JSON.parse(readFileSync(p, 'utf8'));
const hash = p => createHash('sha256').update(readFileSync(p)).digest('hex');
const evidence = read(resolve(paper, 'hierarchy2-evidence.json'));
for (const [path, expected] of Object.entries(evidence.hashes))
  assert.equal(hash(resolve(data, path)), expected, path);
assert.equal(evidence.sourceObjects, 40); assert.equal(evidence.tasks, 1400);
assert.equal(evidence.parts, 5070); assert.equal(evidence.actionSolverSuccess, 200);
const manifest = read(resolve(data, 'manifest.json'));
for (const [path, expected] of Object.entries(manifest.files)) assert.equal(hash(resolve(root, path)), expected, path);
const run = read(resolve(data, 'pilot/run.json'));
assert.equal(run.publicHash, hash(resolve(data, 'public.json')));
assert.equal(run.status, 'complete'); assert.equal(run.results.length, 16);
assert.equal(run.results.reduce((s, r) => s + r.verdict.success, 0), 14);
assert.ok(Math.abs(run.results.reduce((s, r) => s + r.call.cost, 0) - (run.after - run.before)) < 1e-9);
assert.ok(run.after - run.before < 0.10);
const catalog = read(resolve(data, 'catalog.json'));
for (const m of catalog) assert.equal(hash(resolve(data, 'models', `${m.id}.json`)),
  hash(resolve(root, 'public/benchmark/models', `${m.id}.json`)));
const ui = read(resolve(data, 'web-verification/report.json'));
assert.equal(ui.desktopModels.length, 40); assert.equal(ui.mobileModels, 4); assert.deepEqual(ui.errors, []);
for (const name of ['main.pdf', 'supplement.pdf', 'main.zh-CN.md']) assert.equal(hash(resolve(paper, name)),
  hash(resolve(root, 'public/benchmark/docs', name)), `website ${name}`);
for (const [name, report] of [['main', 'pdf-verification'], ['supplement', 'supplement-verification']]) {
  const check = read(resolve(paper, `${report}.json`));
  assert.equal(check.pdfSha256, hash(resolve(paper, `${name}.pdf`)));
  assert.equal(check.overfullBoxes, false); assert.equal(check.unresolvedCitationsOrReferences, false);
}
console.log(JSON.stringify({ hierarchy2Verified: true, objects: 40, tasks: 1400, desktopModels: 40, mobileModels: 4 }));
