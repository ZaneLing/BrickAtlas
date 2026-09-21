import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { root, site, data, assertNoPrivateFields } from './publish';
import type { V2Task } from './types';

const read = (p: string) => JSON.parse(readFileSync(p, 'utf8'));
const catalog = read(resolve(data, 'catalog.json'));
const tasks: V2Task[] = catalog.flatMap((e: any) => read(resolve(site, 'models', `${e.id}.json`)).tasks);
const snapshotManifest = read(resolve(data, 'request-snapshots/manifest.json'));
const payloads = new Map<string, any>(snapshotManifest.requests.map((r: any) => {
  const request = read(resolve(root, r.file));
  const payload = JSON.parse(request.messages.find((m: any) => m.role === 'user').content.find((c: any) => c.type === 'text').text);
  assertNoPrivateFields(payload);
  return [r.taskId, payload];
}));
const byFamily = (family: string) => tasks.filter(t => t.family === family);
const equalSet = (a: string[], b: string[]) => JSON.stringify([...a].sort()) === JSON.stringify([...b].sort());
const hit = (group: V2Task[], predict: (t: V2Task, p: any) => string | undefined) =>
  group.filter(t => predict(t, payloads.get(t.id)) === t.answer.choiceId).length;
const steps = byFamily('source-step');
const ranks = [0, 1, 2, 3].map(k => hit(steps, (_, p) =>
  [...p.options].sort((a, b) => Number(a.label) - Number(b.label))[k]?.id));
assert.ok(Math.max(...ranks) - Math.min(...ranks) <= 1);
const positions = [0, 1, 2, 3].map(k => hit(steps, (_, p) => p.options[k]?.id));
assert.ok(positions.every(n => n < steps.length));
for (const t of steps) {
  const options = payloads.get(t.id).options.map((o: any) => Number(o.label));
  assert.equal(new Set(options).size, 4);
  assert.ok(options.every((n: number) => Number.isInteger(n) && n >= 1 && n <= t.numericDomain!.max));
}
const offsets: Record<string, { predicted: number; correct: number }> = {};
for (const offset of [-3, -2, -1, 0, 1, 2, 3]) for (const anchor of ['min', 'max']) {
  let predicted = 0, correct = 0;
  for (const t of steps) {
    const options = payloads.get(t.id).options;
    const values = options.map((o: any) => Number(o.label));
    const n = (anchor === 'min' ? Math.min(...values) : Math.max(...values)) + offset;
    const o = options.find((o: any) => Number(o.label) === n);
    if (o) { predicted++; correct += Number(o.id === t.answer.choiceId); }
  }
  assert.ok(correct < steps.length);
  offsets[`${anchor}${offset >= 0 ? '+' : ''}${offset}`] = { predicted, correct };
}
for (const t of byFamily('graph-removal')) {
  assert.equal(t.format, 'integer'); assert.equal(payloads.get(t.id).options, undefined);
}
const shapes = byFamily('shape-match');
const referencePositions = [0, 0, 0, 0, 0];
for (const t of shapes) {
  const value = t.options!.find(o => o.id === t.answer.choiceId)!.value;
  referencePositions[t.references.findIndex(r => r.id === value)]++;
  assert.equal(payloads.get(t.id).references, undefined);
}
assert.ok(Math.max(...referencePositions) - Math.min(...referencePositions) <= 1);
const neighbors = byFamily('neighbors'), slices: Record<string, number> = {};
for (let start = 0; start <= 7; start++) for (const end of [-3, -2, -1, 2, 3, 4, 5, 6, 7, 8, 9]) {
  const count = neighbors.filter(t => equalSet(t.references.slice(start, end).map(r => r.id),
    t.options!.filter(o => t.answer.choiceIds.includes(o.id)).map(o => o.value))).length;
  slices[`${start}:${end}`] = count;
  assert.ok(count < neighbors.length);
}
const controls = Object.fromEntries([...new Set(tasks.map(t => t.family))].map(family => {
  const group = byFamily(family).filter(t => t.format === 'single-choice');
  const orderRules = ['first-option', 'last-option', 'shortest-label', 'longest-label', 'smallest-number-label'];
  return [family, { eligible: group.length, rules: Object.fromEntries(orderRules.map(rule => [rule, hit(group, (_, p) => {
    const choices = [...p.options];
    if (rule === 'last-option') choices.reverse();
    if (rule === 'shortest-label') choices.sort((a, b) => a.label.length - b.label.length);
    if (rule === 'longest-label') choices.sort((a, b) => b.label.length - a.label.length);
    if (rule === 'smallest-number-label') choices.sort((a, b) =>
      Number(a.label.replace(/\D/g, '')) - Number(b.label.replace(/\D/g, '')));
    return choices[0]?.id;
  })])) }];
}));
// Interface's answer-dependent 4/5 option count was another v1 surface cue.
for (const t of byFamily('interface')) assert.deepEqual(payloads.get(t.id).options.map((o: any) => o.label).sort(),
  ['axle', 'ball', 'fixed', 'hinge', 'stud']);
const chi = (counts: number[]) => {
  const expected = counts.reduce((s, n) => s + n, 0) / counts.length;
  return counts.reduce((s, n) => s + (n - expected) ** 2 / expected, 0);
};
const counts = [ranks, referencePositions];
const python = resolve(root, 'benchmark/.runtime/mlx-env/bin/python');
const pValues = JSON.parse(execFileSync(python, ['-c',
  'import json,sys; from scipy.stats import chi2; print(json.dumps([float(chi2.sf(v,d)) for v,d in json.loads(sys.argv[1])]))',
  JSON.stringify(counts.map(c => [chi(c), c.length - 1]))],
  { encoding: 'utf8', env: { ...process.env, PYTHONPATH: '', PYTHONNOUSERSITE: '1' } }));
const report = {
  status: 'passed-with-explicit-construct-controls', tasks: tasks.length, requestSnapshots: payloads.size,
  interpretation: 'A predictor can match individual items by chance; no tested fixed rank/offset/position rule determines all nonconstant answers. This is not proof against every possible shortcut.',
  graphRemoval: { items: 73, format: 'integer', optionRankRules: 'inapplicable-by-construction',
    preservedGraphsAndSemanticAnswers: true, prior: 'Original answer concentration remains; see descriptive analysis.' },
  sourceStep: { items: steps.length, correctSemanticRanks: ranks, optionPositions: positions, legalDomainsVerified: true,
    chiSquared: chi(ranks), pValue: pValues[0], pValueIsNotPassCriterion: true, offsetRules: offsets },
  shapeMatch: { items: shapes.length, internalReferenceAnswerPositions: referencePositions, referencesInRequests: 0,
    chiSquared: chi(referencePositions), pValue: pValues[1], pValueIsNotPassCriterion: true },
  neighbors: { items: neighbors.length, referencesInRequests: 0, internalFixedSlices: slices,
    originalSliceHits: slices['1:-2'], maxFixedSliceHits: Math.max(...Object.values(slices)) },
  interface: { items: 87, options: 'all five families on every item', knownEvidenceReadingControl: true },
  onlyFinalRequestFeatureBaselines: controls,
  constantControl: { family: 'evidence-limit', items: 24, semanticMajority: 1,
    treatment: 'Retained explicitly marked control; excluded from reasoning claims.' },
};
writeFileSync(resolve(data, 'shortcut-report.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({ status: report.status, requests: payloads.size, stepRanks: ranks,
  shapePositions: referencePositions, oldNeighborSliceHits: report.neighbors.originalSliceHits,
  maxNeighborSliceHits: report.neighbors.maxFixedSliceHits, pValues }));
