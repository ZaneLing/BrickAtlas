import assert from 'node:assert/strict';
import { test } from 'node:test';
import { curatedCases } from '../suite/curated/cases';
import { curatedTasks } from '../suite/curated/tasks';
import { dims, insertIssue, validate } from '../suite/geometry';
import { independentCheck } from '../suite/research/independent-check';
import { evaluateStrict } from '../suite/study/strict-evaluate';
import type { Part } from '../suite/shared';

test('curated casebank has balanced difficulty, semantic styles, and restrained palettes', () => {
  const cases = curatedCases();
  assert.equal(cases.length, 12);
  assert.equal(new Set(cases.map(c => c.id)).size, 12);
  for (const d of ['easy', 'medium', 'hard']) assert.equal(cases.filter(c => c.difficulty === d).length, 4);
  for (const style of ['furniture', 'architecture', 'infrastructure', 'landmark']) {
    assert.ok(cases.some(c => c.style === style), style);
  }
  for (const model of cases) {
    assert.ok(model.name.length > 3 && model.description.length > 20);
    assert.ok(model.designIntent.length >= 3);
    assert.ok(Object.keys(model.palette).length >= 2 && Object.keys(model.palette).length <= 4);
    assert.deepEqual(new Set(model.structure.parts.map(p => p.color)), new Set(Object.keys(model.palette)));
    assert.equal(model.difficultyProfile.parts, model.structure.parts.length);
  }
});

test('curated geometry and stored assembly orders pass both implementations', () => {
  for (const model of curatedCases()) {
    assert.deepEqual(validate(model.structure.parts), [], model.id);
    const ordered = model.assemblyOrder.map(id => model.structure.parts.find(p => p.id === id)!);
    assert.deepEqual(independentCheck(ordered).issues, [], model.id);
    let current: Part[] = [];
    for (const part of ordered) {
      assert.equal(insertIssue(current, part), null, `${model.id}/${part.id}`);
      current = [...current, part];
    }
    assert.equal(new Set(model.assemblyOrder).size, model.structure.parts.length);
  }
});

test('curated designs preserve key semantic silhouettes and support roles', () => {
  const cases = Object.fromEntries(curatedCases().map(c => [c.id, c]));
  const gate = cases['easy-garden-gate'];
  assert.equal(gate.structure.parts.filter(p => p.id.startsWith('pillar-')).length, 6);
  assert.ok(gate.structure.parts.some(p => p.id === 'lintel-1' && p.partId === '3007'));
  const bridge = cases['hard-double-span-bridge'];
  assert.equal(bridge.structure.parts.filter(p => p.id.startsWith('pier-')).length, 12);
  assert.equal(bridge.structure.parts.filter(p => p.id.startsWith('deck-')).length, 2);
  const station = cases['hard-railway-station'];
  assert.equal(station.structure.parts.filter(p => p.id.startsWith('roof-')).length, 2);
  assert.equal(station.structure.parts.filter(p => p.id.startsWith('bench-')).length, 2);
  const pagoda = cases['hard-two-tier-pagoda'];
  assert.ok(pagoda.structure.parts.find(p => p.id === 'upper-roof-1')!.y
    > pagoda.structure.parts.find(p => p.id === 'lower-roof-1')!.y);
  const lighthouse = cases['hard-lighthouse'];
  const tower = lighthouse.structure.parts.filter(p => p.id.startsWith('tower-')).sort((a, b) => a.y - b.y);
  assert.deepEqual(tower.map(p => p.color), ['white', 'red', 'white', 'red', 'white', 'red']);
  assert.ok(tower.every((p, i) => i === 0 || p.y === tower[i - 1].y + dims(tower[i - 1]).h));
});

test('all eight curated task ground truths pass the strict evaluator', () => {
  const tasks = curatedTasks();
  assert.deepEqual(tasks.map(t => t.task.spec.kind),
    ['parts', 'relations', 'reconstruct', 'generate', 'complete', 'edit', 'plan', 'repair']);
  for (const { task } of tasks) {
    const answer = task.spec.kind === 'repair' ? { structure: task.target, faultIds: task.changedIds } : task.oracle;
    assert.equal(evaluateStrict(task, answer).metrics.success, 1, task.spec.kind);
  }
  const completion = tasks.find(t => t.task.spec.kind === 'complete')!.task;
  assert.ok(completion.changedIds.length >= 4 && completion.source!.parts.length < completion.target.parts.length);
  assert.ok(completion.changedIds.every(id => id.startsWith('rail-') || id.startsWith('rail-post-')));
  assert.ok(completion.source!.parts.some(p => p.id.startsWith('deck-')));
  const repair = tasks.find(t => t.task.spec.kind === 'repair')!.task;
  assert.deepEqual(repair.changedIds, ['roof-1']);
});
