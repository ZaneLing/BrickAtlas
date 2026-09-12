import { test } from 'node:test';
import assert from 'node:assert/strict';
import { dataset, POLICIES } from '../suite/v2/dataset';
import { caseSpecs, taskForV2 } from '../suite/v2/cases';
import { evaluate } from '../suite/v2/evaluate';
import { independentMetrics, independentRelations } from '../suite/study/independent';
import { heightPlan, independentPlanCheck, trainRetrieval } from '../suite/study/algorithms';
import { selection } from '../suite/study/protocol';
import { evaluateStrict } from '../suite/study/strict-evaluate';
import { relative } from '../suite/geometry';
import { strictTrace } from '../suite/study/strict-trace';

test('study sample has 24 heldout objects, all task variants and no outcome selection', () => {
  const specs = selection(), objects = new Set(specs.filter(s => s.kind !== 'parts').map(s => s.modelId));
  assert.equal(objects.size, 24); assert.equal(specs.length, 337);
  for (const p of POLICIES) assert.equal(new Set(specs.filter(s => s.policy === p).map(s => s.modelId)).size, 3);
  assert.ok(specs.every(s => s.split.startsWith('test_')));
});
test('independent field/geometry scoring agrees and height planner solves the eight policy representatives', () => {
  const ids = new Set(POLICIES.map(p => dataset().find(m => m.policy === p)!.id));
  for (const s of caseSpecs().filter(s => ids.has(s.modelId))) {
    const task = taskForV2(s);
    if (s.kind === 'plan') {
      const order = (heightPlan(task.public) as { order: string[] }).order;
      assert.equal(evaluate(task, { order }).metrics.success, 1);
      assert.equal(independentPlanCheck(task.public, order), true);
      assert.equal(independentPlanCheck(task.public, [...order, order[0]]), false);
    } else if (s.kind === 'relations') {
      assert.deepEqual(independentRelations(task.target.parts, String(task.public.input.a), String(task.public.input.b)), task.oracle);
    } else if (s.kind === 'reconstruct' && s.condition === 'symbolic') {
      const actual = task.target.parts.slice(1);
      const a = independentMetrics(task.target.parts, actual), b = evaluate(task, { version: 1, parts: actual }).metrics;
      for (const [k, v] of Object.entries(a)) assert.ok(Math.abs(v - b[k]!) < 1e-9, k);
    }
  }
});
test('retrieval can only return a train source and never a supplied test target', () => {
  const s = selection().find(s => s.kind === 'reconstruct')!, task = taskForV2(s), output = trainRetrieval(task.public)!;
  const source = dataset().find(m => m.id === output.retrieved.id)!;
  assert.equal(source.split, 'train'); assert.notEqual(source.group, s.group);
});
test('strict scorer rejects coercible non-string IDs/colors without changing valid answer scores', () => {
  const task = taskForV2(selection().find(s => s.kind === 'reconstruct')!);
  const malformed = structuredClone(task.target) as any;
  malformed.parts[0].partId = [malformed.parts[0].partId];
  malformed.parts[0].color = [malformed.parts[0].color];
  assert.equal(evaluate(task, malformed).metrics.success, 1, 'Documents the frozen legacy parser gap');
  assert.equal(evaluateStrict(task, malformed).metrics.format, 0);
  assert.equal(evaluateStrict(task, malformed).metrics.success, 0);
  assert.deepEqual(evaluateStrict(task, task.oracle), evaluate(task, task.oracle));
});
test('strict schema rejects malformed primitive fields in absolute and relative structures', () => {
  const task = taskForV2(selection().find(s => s.kind === 'reconstruct')!);
  for (const representation of [task.target, relative(task.target)]) {
    assert.deepEqual(evaluateStrict(task, representation), evaluate(task, representation));
    for (const field of ['id', 'partId', 'color', 'turn']) for (const value of [null, {}, [], true, ['3005']]) {
      const answer = structuredClone(representation) as any;
      (answer.parts ?? answer.nodes)[0][field] = value;
      assert.equal(evaluateStrict(task, answer).metrics.success, 0);
      assert.equal(evaluateStrict(task, answer).metrics.format, 0);
    }
  }
  for (const field of ['x', 'y', 'z']) for (const value of ['0', null, 0.5, Infinity]) {
    const answer = structuredClone(task.target) as any; answer.parts[0][field] = value;
    assert.equal(evaluateStrict(task, answer).metrics.format, 0);
  }
  for (const value of [null, [], [0, 0], ['0', 0, 0], [0, 0, 0, 0]]) {
    const answer = relative(task.target) as any; answer.nodes[0].offset = value;
    assert.equal(evaluateStrict(task, answer).metrics.format, 0);
  }
  assert.equal(evaluateStrict(task, { ...task.target, nodes: [] }).metrics.format, 0);
  assert.equal(evaluateStrict(task, { ...task.target, version: '1' }).metrics.format, 0);
});
test('strict repair rejection retains raw answer but cannot unfold malformed geometry', () => {
  const spec = selection().find(s => s.kind === 'repair' && s.variant === 'color')!;
  const task = taskForV2(spec), answer = structuredClone(task.oracle) as any;
  answer.structure.parts[0].color = [answer.structure.parts[0].color];
  const verdict = evaluateStrict(task, answer);
  assert.equal(verdict.metrics.success, 0);
  const trace = strictTrace('test', 'fixture', { spec, answer, missing: false }, []);
  assert.deepEqual(trace.verdict, verdict);
  assert.deepEqual((trace.events.find(e => e.kind === 'response')!.payload as any).answer, answer);
  assert.equal(trace.events.filter(e => e.kind === 'unfold').length, 0);
});
