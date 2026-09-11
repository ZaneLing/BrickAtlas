import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { makeTask, pilotTasks } from '../core/tasks';
import { Environment } from '../core/environment';
import { bom, compileBlueprint, connected, parseBlueprint, removalIssue, scoreWorld, validateWorld } from '../core/world';
import { Budget } from '../core/budget';
import { requestCeiling } from '../core/openrouter';
import { parseAction } from '../run';
import { wilson } from '../core/results';

test('all pilot targets and blueprints are valid in the declared grid mechanics', () => {
  for (const task of pilotTasks()) {
    assert.equal(validateWorld(task.target), null);
    assert.equal(compileBlueprint({ version: 1, parts: task.target }, task.inventory).ok, true);
  }
});
test('twins have identical public metadata and BOM before intervention', () => {
  const a = makeTask(41, 0, 'none'), b = makeTask(41, 1, 'none');
  assert.deepEqual(bom(a.target), bom(b.target));
  assert.deepEqual(new Environment(a).observe(), new Environment(b).observe());
  assert.equal(scoreWorld(a.target, b.target).exact, false);
});
test('a valid lid intervention reveals two hidden parts, with private coordinates withheld', () => {
  const task = makeTask(41, 0, 'none'), env = new Environment(task);
  const obs = env.step({ type: 'detach', id: task.coverId, predict: { newlyVisible: 2, components: 1 } });
  assert.equal(obs.visible.length, 7);
  assert.equal(env.score().causalAccuracy, 1);
  assert.ok(!('x' in obs.visible[0]));
  assert.ok(!JSON.stringify(obs).includes('variant'));
});
test('hidden handles cannot be manipulated before being discovered', () => {
  const task = makeTask(41, 0, 'none'), env = new Environment(task);
  env.step({ type: 'detach', id: task.hiddenIds[0] });
  assert.equal(env.feedback, 'not_observed');
});
test('passive protocol forbids inspection removals', () => {
  const task = makeTask(41, 0, 'none'), env = new Environment(task, 'passive');
  env.step({ type: 'detach', id: task.coverId });
  assert.equal(env.feedback, 'inspection_disabled');
  assert.equal(env.inspection.length, 8);
});
test('removal checks insertion corridor and does not equate visual hiding with detach', () => {
  const task = makeTask(41, 0, 'none');
  assert.equal(removalIssue(task.target, task.target[0].id), 'blocked_above');
  assert.equal(removalIssue(task.target, task.coverId), null);
});
test('exact matching ignores interchangeable instance IDs and array order', () => {
  const target = makeTask(41, 0, 'none').target;
  const shuffled = [...target].reverse().map((p, i) => ({ ...p, id: `new${i}` }));
  assert.equal(scoreWorld(target, shuffled).exact, true);
  assert.equal(scoreWorld(target, shuffled).edgeF1, 1);
});
test('yaw symmetries of square and rectangular bricks are accepted', () => {
  const target = makeTask(41, 0, 'none').target;
  const rotated = target.map(p => ({ ...p, turn: (p.partId === '3958' ? 1 : (p.turn + 2) % 4) as 0 | 1 | 2 | 3 }));
  assert.equal(scoreWorld(target, rotated).exact, true);
});
test('duplicate pieces cannot inflate the score', () => {
  const target = makeTask(41, 0, 'none').target;
  const score = scoreWorld(target, [...target, { ...target[0], id: 'duplicate' }]);
  assert.equal(score.exact, false);
  assert.equal(score.extra, 1);
  assert.ok(score.partF1 < 1);
  assert.equal(score.valid, false);
});
test('wrong color and grid offset are rejected by scorer', () => {
  const target = makeTask(41, 0, 'none').target;
  assert.equal(scoreWorld(target, target.map((p, i) => i === 7 ? { ...p, color: 'blue' } : p)).exact, false);
  assert.equal(scoreWorld(target, target.map((p, i) => i === 7 ? { ...p, x: 1 } : p)).exact, false);
});
test('blueprint parser rejects nonfinite, duplicate and unknown values', () => {
  const target = makeTask(41, 0, 'none').target;
  for (const parts of [
    [{ ...target[0], x: NaN }], [{ ...target[0], partId: 'nope' }],
    [target[0], target[0]], [{ ...target[0], y: -1 }],
  ]) assert.equal(parseBlueprint({ version: 1, parts }), null);
  assert.equal(parseBlueprint({ version: 1, parts: [] }), null);
});
test('a reference with an invalid order is not an executable blueprint', () => {
  const task = makeTask(41, 0, 'none');
  assert.equal(compileBlueprint({ version: 1, parts: [...task.target].reverse() }, task.inventory).ok, false);
});
test('physically legal but target-wrong placement persists', () => {
  const task = makeTask(41, 0, 'none'), env = new Environment(task);
  env.step({ type: 'blueprint', blueprint: { version: 1, parts: task.target } });
  env.step({ type: 'place', part: { ...task.target[0], x: 6 } });
  assert.equal(env.feedback, 'accepted');
  assert.equal(env.built[0].x, 6);
});
test('batch errors keep only the valid prefix and conserve inventory', () => {
  const task = makeTask(41, 0, 'none'), env = new Environment(task);
  env.step({ type: 'blueprint', blueprint: { version: 1, parts: task.target } });
  env.step({ type: 'build', parts: [task.target[0], task.target[0], task.target[1]] });
  assert.equal(env.built.length, 1);
  assert.equal(env.feedback, 'overlap');
  assert.equal(env.inventory.find(i => i.partId === '3958' && i.color === 'gray')?.count, 0);
});
test('oracle solves all four tasks including real edit recovery and fresh handoff', () => {
  for (const task of pilotTasks()) {
    const env = new Environment(task);
    env.step({ type: 'detach', id: task.coverId, predict: { newlyVisible: 2, components: 1 } });
    env.step({ type: 'blueprint', blueprint: { version: 1, parts: task.target } });
    assert.equal(env.observe().phase, 'build');
    env.step({ type: 'build', parts: env.observe().blueprint!.parts });
    if (task.fault === 'offset') {
      const roof = env.built.find(p => p.partId === '3958' && p.y === 4)!;
      env.step({ type: 'detach', id: roof.id });
    }
    if (task.fault !== 'none') env.step({ type: 'place', part: task.target[7] });
    env.step({ type: 'finish' });
    assert.equal(env.score().lifecycleSuccess, true);
    if (task.fault !== 'none') {
      assert.equal(env.score().faultTriggered, true);
      assert.equal(env.score().recoverySuccess, true);
    }
  }
});
test('faults are hidden from feedback and trigger only once', () => {
  const task = makeTask(41, 0, 'missing'), env = new Environment(task);
  env.step({ type: 'blueprint', blueprint: { version: 1, parts: task.target } });
  env.step({ type: 'build', parts: task.target });
  assert.equal(env.feedback, 'accepted');
  assert.equal(env.built.length, 7);
  env.step({ type: 'place', part: task.target[7] });
  assert.equal(env.built.length, 8);
});
test('unreached faults and failed pre-fault assemblies do not earn recovery credit', () => {
  const env = new Environment(makeTask(41, 0, 'missing'));
  env.step({ type: 'finish' });
  assert.equal(env.score().recoverySuccess, null);
  assert.equal(env.score().lifecycleSuccess, false);
});
test('no-fault trials never become positive recovery examples', () => {
  const env = new Environment(makeTask(41, 0, 'none'));
  env.step({ type: 'blueprint', blueprint: { version: 1, parts: env.task.target } });
  env.step({ type: 'build', parts: env.task.target });
  env.step({ type: 'finish' });
  assert.equal(env.score().recoverySuccess, null);
});
test('invalid actions count against the decision budget', () => {
  const env = new Environment(makeTask(41, 0, 'none'));
  for (let i = 0; i < 20; i++) env.step(null);
  assert.equal(env.phase, 'done');
  assert.equal(env.actions, 14);
});
test('adjacent sides are not vertical stud connections', () => {
  const target = makeTask(41, 0, 'none').target;
  assert.equal(connected(target[1], target[3]), false);
  assert.equal(connected(target[0], target[3]), true);
});
test('cost ledger reserves before request and persists actual billed cost', () => {
  const dir = mkdtempSync(join(tmpdir(), 'care-budget-'));
  try {
    const path = join(dir, 'ledger.json'), budget = new Budget(path, 0.05);
    const id = budget.reserve('test', 0.03);
    assert.equal(JSON.parse(readFileSync(path, 'utf8')).charges[0].status, 'pending');
    assert.throws(() => budget.reserve('test', 0.01), /Unsettled/);
    budget.settle(id, 0.012, 'gen-1');
    assert.equal(new Budget(path).spent, 0.012);
    assert.throws(() => budget.reserve('test', 0.04), /Budget/);
  } finally { rmSync(dir, { recursive: true }); }
});
test('unknown billing and provider overruns fail closed across restarts', () => {
  const dir = mkdtempSync(join(tmpdir(), 'care-budget-'));
  try {
    const path = join(dir, 'ledger.json'), budget = new Budget(path);
    const id = budget.reserve('test', 0.02);
    budget.uncertain(id);
    assert.throws(() => new Budget(path).reserve('test', 0.01), /Unsettled/);
    assert.equal(new Budget(path).committed, 0.02);
    const other = new Budget(join(dir, 'other.json'));
    const request = other.reserve('test', 0.01);
    assert.throws(() => other.settle(request, 0.02, 'gen-2'), /exceeded/);
    assert.equal(other.blocked, true);
  } finally { rmSync(dir, { recursive: true }); }
});
test('budget values and request sizes cannot bypass the cap', () => {
  const dir = mkdtempSync(join(tmpdir(), 'care-budget-'));
  try {
    for (const cap of [NaN, -1, 0, 5, Infinity]) assert.throws(() => new Budget(join(dir, 'x'), cap));
    const budget = new Budget(join(dir, 'ok'));
    for (const cost of [NaN, -1, Infinity, 0]) assert.throws(() => budget.reserve('test', cost));
    assert.throws(() => requestCeiling('not-allowed', []));
    assert.throws(() => requestCeiling('openai/gpt-4.1-mini', [{ role: 'user', content: 'x'.repeat(50001) }]));
    assert.ok(requestCeiling('openai/gpt-4.1-mini', [{ role: 'user', content: 'hello' }]).ceiling > 0);
  } finally { rmSync(dir, { recursive: true }); }
});
test('only structured JSON model actions are parsed, without evaluating code', () => {
  assert.deepEqual(parseAction('```json\n{"type":"finish"}\n```'), { type: 'finish' });
  assert.equal(parseAction('I will finish'), null);
  assert.equal(parseAction('[]'), null);
});
test('confidence intervals handle zero samples and all-or-none outcomes', () => {
  assert.equal(wilson(0, 0), null);
  assert.ok(wilson(0, 4)![1] > 0.4);
  assert.ok(wilson(4, 4)![0] < 0.6);
});
