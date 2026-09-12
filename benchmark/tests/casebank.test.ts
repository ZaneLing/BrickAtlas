import { test } from 'node:test';
import assert from 'node:assert/strict';
import { dataset, POLICIES } from '../suite/v2/dataset';
import { caseSpecs, taskForV2 } from '../suite/v2/cases';
import { evaluate, metricNames } from '../suite/v2/evaluate';
import { groundTruth } from '../suite/v2/ground-truth';
import { canonicalGeometry, key } from '../suite/geometry';
import type { Part } from '../suite/shared';
import { models as oldModels } from '../suite/data';
import { researchModels } from '../suite/research/dataset';

test('v2 has 5120 unique source geometries and actual policy holdouts', () => {
  const models = dataset();
  assert.equal(models.length, 5120);
  assert.equal(new Set(models.map(m => canonicalGeometry(m.structure.parts))).size, 5120);
  const prior = new Set([...oldModels(), ...researchModels()].map(m => canonicalGeometry(m.structure.parts)));
  assert.ok(models.every(m => !prior.has(canonicalGeometry(m.structure.parts))));
  for (const p of POLICIES) {
    const rows = models.filter(m => m.policy === p);
    assert.equal(rows.length, 640);
    assert.ok(rows.every(m => (m.split === 'test_ood') === ['two-support-bridge', 'enclosed-shell'].includes(p)));
  }
});
test('case IDs are unique; all object-derived cases inherit source split; catalog is counted separately', () => {
  const specs = caseSpecs(), source = new Map(dataset().map(m => [m.id, m]));
  assert.equal(new Set(specs.map(s => s.id)).size, specs.length);
  assert.equal(specs.filter(s => s.kind === 'parts').length, 150);
  assert.equal(specs.length, 117910);
  for (const s of specs.filter(s => s.kind !== 'parts')) assert.equal(source.get(s.modelId)!.split, s.split);
});
test('every policy, variant and condition has validated targets, witnesses and complete failure metric schemas', () => {
  const ids = new Set(POLICIES.map(p => dataset().find(m => m.policy === p)!.id));
  for (const s of caseSpecs().filter(s => ids.has(s.modelId) || s.kind === 'parts')) {
    const t = taskForV2(s), gt = groundTruth(t);
    assert.equal(gt.oracleEvaluation.metrics.success, 1, JSON.stringify(s));
    const failed = evaluate(t, null);
    assert.equal(failed.metrics.success, 0);
    assert.deepEqual(Object.keys(failed.metrics).sort(), metricNames(s.kind).sort());
    const oracleKeys = Object.keys(gt.oracleEvaluation.metrics).sort();
    assert.deepEqual(oracleKeys, metricNames(s.kind).sort(), s.kind);
    if (s.kind === 'generate') assert.ok(!('partF1' in gt.oracleEvaluation.metrics));
  }
});
test('correct alternate IDs and yaw symmetries pass while color and collision mutations fail', () => {
  const s = caseSpecs().find(s => s.kind === 'reconstruct' && s.condition === 'symbolic')!;
  const t = taskForV2(s);
  const alternative = { version: 1, parts: t.target.parts.map((p, i) => ({ ...p, id: 'q' + i, turn: (p.turn + 2) % 4 })).reverse() };
  assert.equal(evaluate(t, alternative).metrics.success, 1);
  alternative.parts[0].color = alternative.parts[0].color === 'blue' ? 'red' : 'blue';
  assert.equal(evaluate(t, alternative).metrics.success, 0);
  const collision = structuredClone(t.target);
  collision.parts.push({ ...collision.parts[0], id: 'overlap' });
  assert.equal(evaluate(t, collision).metrics.collisionFree, 0);
  assert.equal(evaluate(t, collision).metrics.success, 0);
});
test('planning detects prefix errors; repair negative cases expose false alarms and localization', () => {
  const plan = taskForV2(caseSpecs().find(s => s.kind === 'plan' && s.variant === 'assemble')!);
  const order = (plan.oracle as { order: string[] }).order;
  assert.equal(evaluate(plan, { order }).metrics.success, 1);
  const bad = evaluate(plan, { order: [order[0], order[0], ...order.slice(1)] });
  assert.equal(bad.diagnostics.firstInvalidStep, 1); assert.equal(bad.metrics.duplicateFree, 0);
  const repair = taskForV2(caseSpecs().find(s => s.kind === 'repair' && s.variant === 'none')!);
  assert.equal(evaluate(repair, repair.oracle).metrics.trueNegative, 1);
  const alarm = evaluate(repair, { structure: repair.target, faultIds: [repair.target.parts[0].id] });
  assert.equal(alarm.metrics.falseAlarm, 1); assert.equal(alarm.metrics.success, 0);
  assert.equal(evaluate(repair, { structure: repair.target }).metrics.format, 0);
});
test('editing oracle applies rotation, recolor and removal independently of output ID order', () => {
  for (const variant of ['rotate', 'recolor', 'remove']) {
    const t = taskForV2(caseSpecs().find(s => s.kind === 'edit' && s.variant === variant)!);
    const before = t.source!.parts, after = t.target.parts;
    if (variant === 'rotate') {
      assert.equal(before.length, after.length);
      for (const p of before) { const q = after.find(q => q.id === p.id)!; assert.equal(q.z, p.x); assert.equal(q.y, p.y); assert.equal(q.turn, (p.turn + 1) % 4); }
    } else if (variant === 'remove') {
      assert.equal(after.length, before.length - 1);
      assert.ok(after.every(p => before.some(q => key(p) === key(q))));
    } else {
      assert.equal(before.length, after.length);
      assert.ok(after.every(p => before.some(q => p.id === q.id && p.x === q.x && p.y === q.y && p.z === q.z)));
    }
    assert.equal(evaluate(t, t.oracle).metrics.success, 1);
  }
});
test('all shifted repair targets avoid indistinguishable duplicate current poses', () => {
  for (const spec of caseSpecs().filter(s => s.kind === 'repair' && s.variant === 'shift' && s.condition === 'ordinary')) {
    const task = taskForV2(spec), faulty = task.source!.parts.find(p => task.changedIds.includes(p.id))!;
    assert.ok(!task.source!.parts.some(p => p.id !== faulty.id && key(p) === key(faulty)), spec.id);
  }
});
test('ordinary visual ambiguity is accepted but layers and symbolic require complete structure', () => {
  const p = (id: string, partId: string, color: Part['color'], x: number, y: number, z: number, turn = 0): Part => ({ id, partId, color, x, y, z, turn });
  const parts = [
    p('base', '3035', 'gray', 0, 0, 0), p('front', '3008', 'red', 0, 1, 3), p('back', '3008', 'red', 0, 1, 0),
    p('left', '3004', 'red', 0, 1, 1, 1), p('right', '3004', 'red', 7, 1, 1, 1),
    p('inside-a', '3004', 'blue', 2, 1, 1), p('inside-b', '3004', 'blue', 4, 1, 2), p('roof', '3035', 'yellow', 0, 4, 0),
  ];
  const alternative = { version: 1, parts: parts.map(p => p.id === 'inside-a' ? { ...p, turn: 1 } : p.id === 'inside-b' ? { ...p, turn: 1, z: 1 } : p) };
  for (const condition of ['ordinary', 'layers', 'symbolic']) {
    const task = taskForV2(caseSpecs().find(s => s.kind === 'reconstruct' && s.condition === condition)!);
    task.target = { version: 1, parts };
    const result = evaluate(task, alternative);
    assert.equal(result.metrics.surfaceF1, 1);
    assert.equal(result.metrics.fullStructureSuccess, 0);
    assert.equal(result.metrics.success, Number(condition === 'ordinary'));
  }
});
