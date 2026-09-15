import assert from 'node:assert/strict';
import test from 'node:test';
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { models } from '../suite/hierarchy2/models';
import { score, replay, solveActions } from '../../src/benchmark/engine';
import type { Task, Action } from '../../src/benchmark/types';
import { scoreBatch } from '../suite/hierarchy2/score';

const root = resolve(import.meta.dirname, '../..'), out = resolve(root, 'benchmark/hierarchy-v2');
const read = (name: string) => JSON.parse(readFileSync(resolve(out, name), 'utf8'));
const all = models();
const bundles = all.map(m => read(`models/${m.id}.json`));
const tasks: Task[] = bundles.flatMap(b => b.tasks);
test('hierarchy-2: every level crosses every task family, with distinct colored-independent geometry', () => {
  assert.equal(all.length, 40); assert.equal(tasks.length, 1400);
  assert.equal(new Set(tasks.map(t => t.id)).size, 1400);
  for (const level of ['D1', 'D2', 'D3', 'D4']) {
    assert.equal(all.filter(m => m.difficulty === level).length, 10);
    const selected = tasks.filter(t => t.difficulty === level);
    assert.equal(selected.length, 350);
    for (const family of new Set(tasks.map(t => t.family))) assert.equal(selected.filter(t => t.family === family).length, 10);
  }
  const fingerprints = all.map(m => JSON.stringify(m.parts.map(p => {
    const mod = m.modules.find(x => x.id === p.moduleId)!;
    return { shape: p.shape, position: p.position.map((v, i) => +(v + mod.position[i]).toFixed(5)), size: p.size, rotation: p.rotation };
  }).sort((a, b) => JSON.stringify(a).localeCompare(JSON.stringify(b)))));
  assert.equal(new Set(fingerprints).size, 40, 'Renaming/recoloring cannot create a new geometry');
});
test('hierarchy-2: every oracle passes; missing and wrong-domain answers fail', () => {
  for (const t of tasks) {
    assert.equal(score(t, t.answer).success, 1, t.id);
    assert.equal(score(t, {}).success, 0, t.id);
    assert.equal(score(t, null).success, 0, t.id);
    if (t.format === 'multiple-choice') assert.equal(score(t, { choiceIds: [...t.answer.choiceIds, 'INVALID'] }).success, 0);
    if (t.options) assert.equal(new Set(t.options.map(o => o.label)).size, t.options.length);
  }
});
test('hierarchy-2: public transition solver reaches goals; violated dependencies and budgets reject', () => {
  for (const t of tasks.filter(t => t.format === 'actions')) {
    const answer = solveActions(t); assert.equal(score(t, answer).success, 1, t.id);
    assert.equal(score(t, { actionIds: answer.actionIds.slice(0, -1) }).success, 0, t.id);
    assert.equal(score(t, { actionIds: [...answer.actionIds, answer.actionIds[0]] }).success, 0, t.id);
    assert.equal(score(t, { actionIds: ['__unknown'] }).success, 0);
    const limited = structuredClone(t); limited.input.budget = 0;
    assert.equal(score(limited, answer).success, 0, t.id);
    const dependent = (t.input.actions as Action[]).find(a =>
      a.requires.some(f => !t.input.initialFacts.includes(f)));
    if (dependent) assert.equal(replay(t, [dependent.id]).frames.at(-1)!.accepted, false, t.id);
  }
});
test('hierarchy-2: replay changes actual visibility and color while preserving unedited modules', () => {
  for (const bundle of bundles) {
    const assembly = bundle.tasks.find((t: Task) => t.family === 'assembly');
    const frames = replay(assembly, assembly.answer.actionIds).frames;
    assert.equal(frames[0].activeModules.length, 0);
    assert.equal(frames.at(-1)!.activeModules.length, bundle.model.modules.length);
    const edit = bundle.tasks.find((t: Task) => t.family === 'compound-edit');
    const result = replay(edit, edit.answer.actionIds);
    assert.equal(result.success, 1);
    assert.deepEqual(Object.keys(result.frames.at(-1)!.colors), [bundle.model.taskConfig.serviceModule]);
    const repair = bundle.tasks.find((t: Task) => t.family === 'service-repair');
    assert.ok(replay(repair, repair.answer.actionIds).frames.some(f => f.activeModules.length < bundle.model.modules.length));
  }
});
test('hierarchy-2: resource conflicts and inconsistent world policies reject', () => {
  for (const t of tasks.filter(t => t.format === 'schedule')) {
    assert.equal(score(t, { starts: Object.fromEntries(t.input.jobs.map((j: any) => [j.id, 0])) }).success, 0);
    const delayed = structuredClone(t.answer);
    for (const key of Object.keys(delayed.starts)) delayed.starts[key] += t.input.deadline;
    assert.equal(score(t, delayed).success, 0);
  }
  for (const t of tasks.filter(t => t.format === 'policy')) {
    assert.equal(score(t, { queryId: 'visual', decisions: { same: 'continue', stuck: 'replace' } }).success, 0);
    assert.equal(score(t, { queryId: 'probe', decisions: { free: 'continue', slack: 'tighten' } }).success, 0);
  }
});
test('hierarchy-2: physics records are finite and task answers follow the measured trace', () => {
  for (const b of bundles) {
    assert.equal(b.physics.trace.length, 11); assert.equal(b.physics.paths.length, 3);
    assert.ok(Number.isFinite(b.physics.nominalDrift));
    const task = b.tasks.find((t: Task) => t.family === 'dynamic');
    const answer = task.options.find((o: any) => o.id === task.answer.choiceId).value;
    assert.equal(answer, +Math.max(...b.physics.trace.map((f: any) => f.displacement)).toFixed(4));
    const access = b.tasks.find((t: Task) => t.family === 'access');
    const answerPaths = access.options.filter((o: any) => access.answer.choiceIds.includes(o.id)).map((o: any) => o.value).sort();
    assert.deepEqual(answerPaths, b.physics.paths.filter((p: any) => p.clear).map((p: any) => p.id).sort());
  }
});
test('hierarchy-2: public export hides answers and original website includes identical model data', () => {
  const pub = read('public.json'); assert.equal(pub.length, 1400);
  assert.ok(pub.every((t: any) => !Object.hasOwn(t, 'answer')));
  for (const m of all) {
    assert.equal(readFileSync(resolve(root, 'public/benchmark/models', `${m.id}.json`), 'utf8'),
      readFileSync(resolve(out, 'models', `${m.id}.json`), 'utf8'));
    for (const view of ['iso', 'front', 'side', 'top'])
      assert.ok(existsSync(resolve(root, 'public/benchmark/images', `${m.id}-${view}.png`)));
  }
});
test('hierarchy-2: render hashes match canvas artifacts from original website', () => {
  const audit = read('render-audit.json'); assert.equal(audit.frames.length, 160);
  for (const f of audit.frames) {
    const hash = createHash('sha256').update(readFileSync(resolve(out, f.file))).digest('hex');
    assert.equal(hash, f.sha256); assert.ok(f.contrast > 100);
  }
});

test('hierarchy-2: batch denominators retain missing cases and reject unknown or duplicate IDs', () => {
  const report = scoreBatch([]);
  assert.equal(report.expected, 1400); assert.equal(report.missing, 1400);
  assert.ok(report.cells.every(c => c.answered === 0 && c.success === 0));
  assert.throws(() => scoreBatch([{ id: 'UNKNOWN', answer: {} }]));
  assert.throws(() => scoreBatch([{ id: tasks[0].id }, { id: tasks[0].id }]));
  const partial = scoreBatch([{ id: tasks[0].id, answer: tasks[0].answer }]);
  assert.equal(partial.missing, 1399);
  assert.equal(partial.rows.reduce((s, r) => s + r.verdict.success, 0), 1);
});

test('hierarchy-2: paid pilot replays archived answers and matches frozen public bytes', () => {
  const run = read('pilot/run.json');
  assert.equal(run.status, 'complete'); assert.equal(run.results.length, 16);
  assert.equal(createHash('sha256').update(readFileSync(resolve(out, 'public.json'))).digest('hex'), run.publicHash);
  for (const r of run.results) {
    assert.deepEqual(score(tasks.find(t => t.id === r.id)!, r.prediction), r.verdict);
    assert.equal(JSON.stringify(JSON.parse(r.call.content)), JSON.stringify(r.prediction));
  }
  assert.equal(run.results.reduce((s: number, r: any) => s + r.verdict.success, 0), 14);
});
