import { test } from 'node:test';
import assert from 'node:assert/strict';
import { models, summary } from '../suite/data';
import { CATALOG, TASKS, type Kind, type Part, type Structure } from '../suite/shared';
import { canonicalGeometry, compare, decode, dims, insertIssue, relative, removeIssue, validate } from '../suite/geometry';
import { taskFor } from '../suite/tasks';
import { baseline, legalityFeedback, score } from '../suite/score';
import { defaultSelection } from '../suite/storage';

const dataset = models();
for (const kind of TASKS) test(`multitask ${kind}: every oracle succeeds, empty answers fail, relative input agrees`, () => {
  for (const m of dataset) {
    const task = taskFor(m, kind), oracle = score(task, task.oracle);
    assert.equal(oracle.metrics.success, 1, `${m.id}/${kind}: ${JSON.stringify(oracle)}`);
    assert.equal(score(task, {}).metrics.success, 0);
    const alt = taskFor(m, kind, 'relative');
    assert.deepEqual(score(alt, alt.oracle), oracle);
  }
});
test('multitask generator is deterministic and reports variants separately from groups', () => {
  assert.equal(summary().models, 552);
  assert.equal(summary().groups, 138);
  assert.equal(summary().tasks, 4416);
  assert.equal(new Set(dataset.map(m => m.id)).size, dataset.length);
  assert.deepEqual(summary(), summary());
});
test('canonical geometry groups and family holdouts never cross dataset splits', () => {
  const mapping = new Map<string, string>();
  for (const m of dataset) {
    const key = canonicalGeometry(m.structure.parts);
    if (mapping.has(key)) assert.equal(mapping.get(key), m.split);
    mapping.set(key, m.split);
    assert.equal(['staircase', 'gate'].includes(m.family), m.split === 'test_ood');
    for (const kind of TASKS) assert.equal(taskFor(m, kind).public.split, m.split);
  }
});
test('relative representation round trips every sample exactly', () => {
  for (const m of dataset) assert.deepEqual(decode(relative(m.structure)), m.structure);
});
test('canonical grouping ignores color, translation and yaw', () => {
  const p = dataset[0].structure.parts;
  assert.equal(canonicalGeometry(p), canonicalGeometry(p.map(p => ({ ...p, color: 'blue', x: p.x + 2, z: p.z + 3 }))));
  assert.equal(canonicalGeometry(p), canonicalGeometry(p.map(p => ({ ...p, x: 24 - p.z - dims(p).d, z: p.x, turn: (p.turn + 1) % 4 }))));
});
test('part instance permutation and 180 degree symmetry do not lose scores', () => {
  const p = dataset[0].structure.parts;
  assert.ok(compare(p, [...p].reverse().map((p, i) => ({ ...p, id: `alt${i}`, turn: (p.turn + 2) % 4 }))).exact);
  assert.ok(!compare(p, [...p, { ...p[0], id: 'extra' }]).exact);
});
test('invalid structure values, cycles and duplicate IDs cannot be decoded', () => {
  const p = dataset[0].structure.parts[0];
  for (const part of [{ ...p, x: NaN }, { ...p, partId: 'imaginary' }, { ...p, x: -1 },
    { ...p, turn: 1.5 }, { ...p, color: 'unknown' }]) assert.equal(decode({ version: 1, parts: [part] }), null);
  assert.equal(decode({ version: 1, parts: [p, p] }), null);
  assert.equal(decode({ version: 1, nodes: [{ ...p, parent: p.id, offset: [0, 0, 0] }] }), null);
  assert.equal(decode({ version: 1, parts: [p], nodes: [] }), null);
});
test('overlap, unsupported bodies and vertical assembly obstructions are checked', () => {
  const base: Part = { id: 'base', partId: '3001', color: 'red', x: 0, y: 0, z: 0, turn: 0 };
  assert.ok(validate([base, { ...base, id: 'copy' }]).includes('overlap'));
  assert.ok(validate([{ ...base, y: 10 }]).includes('unsupported'));
  const pillar = { ...base, id: 'pillar', partId: '3005' };
  const roof = { ...base, id: 'roof', y: 3 };
  const other = { ...pillar, id: 'under', x: 3 };
  assert.equal(insertIssue([pillar, roof], other), 'blocked');
  assert.equal(removeIssue([pillar, roof], pillar.id), 'blocked');
  assert.equal(removeIssue([pillar, roof], roof.id), null);
});
test('generation accepts a different valid brick tiling, not just the reference sequence', () => {
  const m = dataset.find(m => m.family === 'platform' && m.parameters.width === 4 && m.parameters.depth === 2 && m.parameters.height === 1)!;
  const t = taskFor(m, 'generate'), p = t.target.parts[0];
  const alt = t.target.parts.flatMap(part => part.id === p.id
    ? [{ ...part, partId: '3003', id: 'a' }, { ...part, partId: '3003', id: 'b', x: part.x + 2 }]
    : [part]);
  assert.equal(score(t, { version: 1, parts: alt }).metrics.success, 1);
  assert.equal(compare(t.target.parts, alt).exact, false);
  assert.equal(score(t, { version: 1, parts: alt.slice(1) }).metrics.success, 0);
});
test('editing covers recolor, geometric addition and removal and penalizes collateral changes', () => {
  const ops = new Set<string>();
  for (const m of dataset.slice(0, 50)) {
    const t = taskFor(m, 'edit');
    ops.add((t.public.input.operation as { type: string }).type);
    const damaged = structuredClone(t.target);
    damaged.parts[0].x += 1;
    assert.equal(score(t, damaged).metrics.success, 0);
  }
  assert.equal(ops.size, 3);
});
test('repair contains true negatives; false alarms cannot earn exact success', () => {
  const normal = dataset.map(m => taskFor(m, 'repair')).find(t => !t.changedIds.length)!;
  assert.equal(score(normal, { structure: normal.target, faultIds: [] }).metrics.success, 1);
  const alarm = score(normal, { structure: normal.target, faultIds: ['invented'] });
  assert.equal(alarm.metrics.success, 0); assert.equal(alarm.metrics.falseAlarm, 1);
  const corrupt = dataset.map(m => taskFor(m, 'repair')).find(t => t.changedIds.length)!;
  assert.equal(score(corrupt, { structure: corrupt.target, faultIds: [] }).metrics.success, 0);
  assert.equal(score(corrupt, { structure: corrupt.target, faultIds: [...corrupt.changedIds, ...corrupt.changedIds] }).metrics.format, 0);
});
test('planning accepts swapped independent pieces but rejects duplicates and wrong prefixes', () => {
  const t = dataset.map(m => taskFor(m, 'plan')).find(t => t.public.input.direction === 'assemble' && t.public.family === 'bridge')!;
  const { order } = structuredClone(t.oracle) as { order: string[] };
  [order[0], order[1]] = [order[1], order[0]];
  assert.equal(score(t, { order }).metrics.success, 1);
  assert.equal(score(t, { order: [order[0], order[0], ...order.slice(2)] }).metrics.success, 0);
  assert.equal(score(t, { order: [...order].reverse() }).metrics.success, 0);
});
test('private answers are not present in model public task payloads', () => {
  for (const m of dataset.slice(0, 10)) for (const kind of ['parts', 'reconstruct', 'complete', 'repair'] as Kind[]) {
    const t = taskFor(m, kind);
    assert.ok(!('oracle' in t.public)); assert.ok(!('target' in t.public)); assert.ok(!('frames' in t.public));
    assert.ok(!('target' in t.public.input));
    assert.ok(t.frames.length > 0);
  }
});
test('target-blind validation cannot reveal missing target pieces or correct positions', () => {
  const m = dataset[0], other = dataset[4];
  assert.deepEqual(legalityFeedback(m.structure), { syntax: true, legality: [] });
  assert.deepEqual(legalityFeedback(other.structure), { syntax: true, legality: [] });
  assert.equal('score' in legalityFeedback(m.structure), false);
});
test('fixed smoke selection covers all eight tasks and both heldout conditions', () => {
  const selection = defaultSelection();
  assert.equal(selection.length, 16);
  for (const kind of TASKS) assert.deepEqual(selection.filter(s => s.kind === kind).map(s => s.split), ['test_id', 'test_ood']);
  for (const s of selection) assert.ok(!['train', 'validation'].includes(s.split));
  assert.equal(new Set(selection.map(s => s.taskId)).size, 16);
});
test('catalog has distinct body geometry up to rotations for isolated identification', () => {
  const shapes = Object.values(CATALOG).map(s => [Math.min(s.w, s.d), Math.max(s.w, s.d), s.h].join(':'));
  assert.equal(new Set(shapes).size, shapes.length);
});
