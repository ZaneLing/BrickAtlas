import assert from 'node:assert/strict';
import { test } from 'node:test';
import { evaluateChallenge } from '../suite/challenge/evaluate';
import { challengeModels } from '../suite/challenge/models';
import { CHALLENGE_KINDS, challengeTasks } from '../suite/challenge/tasks';
import { components, insertIssue, validate } from '../suite/geometry';
import { independentCheck } from '../suite/research/independent-check';
import type { Part } from '../suite/shared';
import { InspectionEpisode } from '../suite/challenge/inspection';

test('challenge models are connected 49-63 part structures with executable orders', () => {
  const models = challengeModels();
  assert.equal(models.length, 6);
  assert.equal(models.reduce((sum, model) => sum + model.structure.parts.length, 0), 329);
  for (const model of models) {
    assert.ok(model.structure.parts.length >= 49 && model.structure.parts.length <= 63, model.id);
    assert.deepEqual(validate(model.structure.parts), [], model.id);
    assert.equal(components(model.structure.parts), 1, model.id);
    const ordered = model.assemblyOrder.map(id => model.structure.parts.find(p => p.id === id)!);
    assert.deepEqual(independentCheck(ordered).issues, [], model.id);
    let prefix: Part[] = [];
    for (const part of ordered) {
      assert.equal(insertIssue(prefix, part), null, `${model.id}/${part.id}`);
      prefix = [...prefix, part];
    }
  }
});

test('all twelve advanced task oracles pass and empty answers fail', () => {
  const tasks = challengeTasks();
  assert.deepEqual(tasks.map(task => task.kind), [...CHALLENGE_KINDS]);
  for (const task of tasks) {
    assert.equal(evaluateChallenge(task, task.oracle).success, 1, task.kind);
    assert.equal(evaluateChallenge(task, null).success, 0, task.kind);
  }
});

test('challenge tasks cover nontrivial changed regions and action contracts', () => {
  const tasks = Object.fromEntries(challengeTasks().map(task => [task.kind, task]));
  const recovery = tasks['recovery-plan'];
  const actions = (recovery.oracle as { actions: Array<{ type: string }> }).actions;
  assert.ok(actions.some(action => action.type === 'remove') && actions.some(action => action.type === 'place'));
  assert.ok(actions.length > 30);
  assert.ok((tasks['support-counterfactual'].oracle as { unsupportedIds: string[] }).unsupportedIds.length >= 4);
  assert.ok(tasks['compound-edit'].changedIds.length >= 10);
  assert.equal((tasks['multi-fault-repair'].oracle as { faultIds: string[] }).faultIds.length, 3);
  assert.equal((tasks['step-selection'].oracle as { legalIds: string[] }).legalIds.length, 6);
  assert.ok(tasks['distributed-completion'].changedIds.length >= 8);
  assert.ok(tasks['module-transplant'].changedIds.length >= 10);
});

test('near-miss advanced answers are rejected', () => {
  for (const task of challengeTasks()) {
    const answer = structuredClone(task.oracle) as any;
    if (task.kind === 'recovery-plan') answer.actions = answer.actions.slice(1);
    else if (task.kind === 'support-counterfactual') answer.unsupportedIds = answer.unsupportedIds.slice(1);
    else if (task.kind === 'multi-fault-repair') answer.faultIds = answer.faultIds.slice(1);
    else if (task.kind === 'active-inspection') answer.queryId = 'unknown-query';
    else if (task.kind === 'graph-reasoning') answer.shortestPath++;
    else if (task.kind === 'step-selection') answer.legalIds = answer.legalIds.slice(1);
    else if (task.kind === 'pose-estimation') answer.x++;
    else {
      const structure = answer.structure ?? answer;
      structure.parts = structure.parts.slice(1);
    }
    assert.equal(evaluateChallenge(task, answer).success, 0, task.kind);
  }
});

test('public candidate poses alone suffice to reproduce next-action labels', () => {
  const task = challengeTasks().find(t => t.kind === 'step-selection')!;
  const { current, candidates } = task.input as { current: { parts: Part[] }; candidates: Part[] };
  const legalIds = candidates.filter(p => !insertIssue(current.parts, p)).map(p => p.id).sort();
  assert.deepEqual({ legalIds }, task.oracle);
});

test('strict challenge decoding rejects coercion without changing legacy sources', () => {
  const task = challengeTasks().find(t => t.kind === 'scene-reconstruction')!;
  for (const field of ['partId', 'color']) {
    const bad = structuredClone(task.oracle) as any;
    bad.parts[0][field] = [bad.parts[0][field]];
    assert.equal(evaluateChallenge(task, bad).metrics.format, 0);
  }
});

test('pose scoring accepts square yaw equivalence and rejects wrong position', () => {
  const task = challengeTasks().find(t => t.kind === 'pose-estimation')!;
  for (const turn of [0, 1, 2, 3]) {
    assert.equal(evaluateChallenge(task, { ...(task.oracle as object), turn }).success, 1);
  }
  assert.equal(evaluateChallenge(task, { ...(task.oracle as object), turn: 4 }).success, 0);
});

test('full-target visual tasks disclose every part at its bottom layer', () => {
  for (const task of challengeTasks().filter(t =>
    ['scene-reconstruction', 'distributed-completion', 'multi-fault-repair'].includes(t.kind))) {
    assert.deepEqual(task.frames.filter(f => f.layer !== null).flatMap(f => f.parts.map(p => p.id)).sort(),
      task.target.parts.map(p => p.id).sort());
  }
});

test('inspection enforces query before response and records cost independently', () => {
  const task = challengeTasks().find(t => t.kind === 'active-inspection')!;
  const episode = new InspectionEpisode(task);
  assert.throws(() => episode.submit('two-parallel-beams'));
  assert.throws(() => episode.query('unknown'));
  const observation = episode.query('layer-y-13');
  assert.ok(observation.frame?.parts.every(p => p.y === 13));
  assert.throws(() => episode.query('top-rgb'));
  assert.equal(episode.submit('two-parallel-beams').success, 1);
  assert.throws(() => episode.submit('two-parallel-beams'));
  const symbolic = new InspectionEpisode(task);
  assert.ok(symbolic.query('symbolic-graph').structure);
  const verdict = symbolic.submit('two-parallel-beams');
  assert.equal(verdict.success, 1);
  assert.equal(verdict.metrics.queryCost, 4);
});

test('articulation oracle agrees with independent delete-and-count enumeration', () => {
  const task = challengeTasks().find(t => t.kind === 'graph-reasoning')!;
  const parts = task.target.parts, count = components(parts);
  const ids = parts.filter(p => components(parts.filter(q => q.id !== p.id)) > count).map(p => p.id).sort();
  assert.deepEqual(ids, (task.oracle as { articulationIds: string[] }).articulationIds);
});
