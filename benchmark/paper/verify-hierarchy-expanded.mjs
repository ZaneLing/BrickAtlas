import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
const paper = import.meta.dirname, root = resolve(paper, '../..'), data = resolve(root, 'benchmark/hierarchy-v3-expanded');
const read = p => JSON.parse(readFileSync(p, 'utf8'));
const hash = p => createHash('sha256').update(readFileSync(p)).digest('hex');
const evidence = read(resolve(paper, 'hierarchy-expanded-evidence.json'));
for (const [p, expected] of Object.entries(evidence.hashes)) assert.equal(hash(resolve(data, p)), expected, p);
assert.equal(evidence.sourceObjects, 144); assert.equal(evidence.tasks, 6912); assert.equal(evidence.parts, 42617);
assert.equal(evidence.publicActionSolver, 1152); assert.equal(evidence.uniqueGeometries, 143);
const manifest = read(resolve(data, 'manifest.json'));
for (const [p, expected] of Object.entries(manifest.files)) assert.equal(hash(resolve(root, p)), expected, p);
const old = resolve(root, 'benchmark/hierarchy-v3');
const compatible = read(resolve(data, 'retained-compatibility.json'));
assert.equal(compatible.unchanged.length, 48);
for (const r of compatible.unchanged) {
  assert.equal(hash(resolve(data, 'models', `${r.modelId}.json`)), r.sha256);
  assert.equal(hash(resolve(old, 'models', `${r.modelId}.json`)), r.sha256);
}
const pilot = read(resolve(old, 'pilot/run.json'));
assert.equal(hash(resolve(root, evidence.historicalPilot.path)), evidence.historicalPilot.sha256);
assert.equal(pilot.publicHash, hash(resolve(old, 'public.json')));
assert.equal(pilot.results.length, 16); assert.equal(pilot.results.reduce((s, r) => s + r.verdict.success, 0), 7);
const catalog = read(resolve(data, 'catalog.json'));
for (const m of catalog) {
  assert.equal(hash(resolve(data, 'models', `${m.id}.json`)), hash(resolve(root, 'public/benchmark/models', `${m.id}.json`)));
  const b = read(resolve(data, 'models', `${m.id}.json`));
  assert.equal(b.tasks.length, 48); assert.equal(b.validation.penetrations.length, 0);
  assert.ok(b.physics.nominalWithinTolerance);
  assert.ok(b.validation.limits.every(j => j.enabled));
}
const views = read(resolve(data, 'render-audit.json')).frames;
assert.equal(views.length, 576);
for (const v of views) {
  assert.equal(hash(resolve(data, v.file)), v.sha256);
  assert.equal(hash(resolve(root, 'public/benchmark', v.file)), v.sha256);
}
const ui = read(resolve(data, 'web-verification/report.json'));
assert.equal(ui.desktopModels.length, 144); assert.equal(ui.mobileModels, 4); assert.deepEqual(ui.errors, []);
for (const r of ui.desktopModels) assert.equal(hash(resolve(data, 'models', `${r.id}.json`)), r.modelHash);
for (const name of ['main.pdf', 'supplement.pdf', 'main.zh-CN.md'])
  assert.equal(hash(resolve(paper, name)), hash(resolve(root, 'public/benchmark/docs', name)));
for (const name of ['REPORT.zh-CN.md', 'QUESTION_BANK.zh-CN.md'])
  assert.equal(hash(resolve(data, name)), hash(resolve(root, 'public/benchmark/docs', name)));
for (const [name, report] of [['main', 'pdf-verification'], ['supplement', 'supplement-verification']]) {
  const check = read(resolve(paper, `${report}.json`));
  assert.equal(hash(resolve(paper, `${name}.pdf`)), check.pdfSha256);
  assert.equal(check.overfullBoxes, false); assert.equal(check.unresolvedCitationsOrReferences, false);
}
console.log(JSON.stringify({ verified: true, models: 144, tasks: 6912, retainedCompatible: 48, views: 576 }));
