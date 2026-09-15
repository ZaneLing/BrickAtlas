import assert from 'node:assert/strict';
import test from 'node:test';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { evaluateMechanismTask } from '../suite/mechanism/evaluate';
import { mechanismModels } from '../suite/mechanism/models';
import {
  evaluateAccessPaths,
  paretoAlternatives,
  simulateImpulseLadder,
  simulatePrefix,
} from '../suite/mechanism/physics';
import { scoreMechanismResponses } from '../suite/mechanism/score';
import { mechanismTasks } from '../suite/mechanism/tasks';

const canonical = (task: Awaited<ReturnType<typeof mechanismTasks>>[number]) =>
  task.kind === 'active-inspection' ? { queryId: (task.oracle.queryIds as string[])[0] } : task.oracle;

test('mechanism-v1: six original whole mechanisms use diverse parts and articulated joints', () => {
  const models = mechanismModels();
  assert.equal(models.length, 6);
  assert.ok(models.every(model => model.originalDesign && model.parts.length >= 35));
  assert.ok(models.every(model => model.joints.some(joint => ['revolute', 'prismatic'].includes(joint.type))));
  const shapes = new Set(models.flatMap(model => model.parts.map(part => part.shape)));
  for (const required of ['brick', 'slope', 'wheel', 'axle', 'gear', 'window'])
    assert.ok(shapes.has(required as any), required);
  const encoded = JSON.stringify(models);
  assert.ok(!encoded.includes('library.ldraw.org'));
  assert.ok(!encoded.includes('sourceModelId'));
});

test('mechanism-v1: 48 tasks cover eight gaps on every source and all oracle answers pass', async () => {
  const tasks = await mechanismTasks();
  assert.equal(tasks.length, 48);
  const kinds = [...new Set(tasks.map(task => task.kind))];
  assert.equal(kinds.length, 8);
  for (const kind of kinds) {
    const selected = tasks.filter(task => task.kind === kind);
    assert.equal(selected.length, 6);
    assert.equal(new Set(selected.map(task => task.sourceGroup)).size, 6);
  }
  for (const task of tasks) assert.equal(evaluateMechanismTask(task, canonical(task)).success, 1, task.id);
});

test('mechanism-v1: physics creates positive/negative evidence instead of constant labels', async () => {
  const models = mechanismModels();
  const accessPatterns = new Set<string>(), thresholds = new Set<number>();
  let functionalTrue = 0, functionalFalse = 0;
  const tasks = await mechanismTasks();
  for (const model of models) {
    const valid = await simulatePrefix(model, model.assemblyOrder);
    const invalidFirst = [...model.modules].filter(m => !m.anchored)
      .sort((a, b) => b.position[1] - a.position[1])[0].id;
    const invalid = await simulatePrefix(model, [invalidFirst, ...model.assemblyOrder.filter(id => id !== invalidFirst)]);
    assert.equal(valid.success, 1);
    assert.equal(invalid.firstUnstableStep, 0);
    const access = await evaluateAccessPaths(model);
    assert.ok(access.some(row => row.accessible) && access.some(row => !row.accessible));
    accessPatterns.add(access.filter(row => row.accessible).map(row => row.pathId).join('|'));
    const ladder = await simulateImpulseLadder(model);
    assert.ok(ladder.some(row => row.safe) && ladder.some(row => !row.safe));
    thresholds.add(ladder.filter(row => row.safe).at(-1)!.impulse);
    assert.equal(paretoAlternatives(model).length, 1);
  }
  for (const task of tasks.filter(task => task.kind === 'functional-kinematics')) {
    if (task.oracle.reachesTarget) functionalTrue++; else functionalFalse++;
  }
  assert.ok(accessPatterns.size >= 4);
  assert.ok(thresholds.size >= 4);
  assert.ok(functionalTrue > 0 && functionalFalse > 0);
  assert.ok(new Set(tasks.filter(task => task.kind === 'active-inspection')
    .flatMap(task => task.oracle.queryIds as string[]).map(id => id.split('-').at(-1))).size >= 3);
});

test('mechanism-v1: missing, unknown and duplicate submissions fail closed', async () => {
  const tasks = await mechanismTasks();
  const empty = await scoreMechanismResponses([]);
  assert.equal(empty.expected, 48);
  assert.equal(empty.missing, 48);
  assert.ok(empty.rows.every(row => row.result.success === 0));
  await assert.rejects(() => scoreMechanismResponses([{ id: 'unknown', answer: {} }]));
  await assert.rejects(() => scoreMechanismResponses([{ id: tasks[0].id }, { id: tasks[0].id }]));
});

test('mechanism-v1: every model and task visualization is rendered and hash-audited', async () => {
  const output = resolve(import.meta.dirname, '../mechanism-v1');
  const audit = JSON.parse(readFileSync(resolve(output, 'render-audit.json'), 'utf8'));
  assert.equal(audit.frames.length, 72);
  for (const frame of audit.frames) {
    assert.ok(existsSync(resolve(output, frame.file)), frame.file);
    assert.equal(frame.pixels.width, 1200);
    assert.equal(frame.pixels.height, 900);
    assert.ok(frame.pixels.foreground > 15_000);
  }
});

test('mechanism-v1: archived local and cloud model scores replay exactly', async () => {
  const output = resolve(import.meta.dirname, '../mechanism-v1');
  const tasks = await mechanismTasks(), byId = new Map(tasks.map(task => [task.id, task]));
  const local = JSON.parse(readFileSync(resolve(output, 'results/local-qwen3-0.6b.scores.json'), 'utf8'));
  assert.equal(local.rows.reduce((sum: number, row: any) => sum + row.result.success, 0), 3);
  const latest = JSON.parse(readFileSync(resolve(output, 'results/latest.json'), 'utf8'));
  const run = JSON.parse(readFileSync(resolve(output, 'results', latest.path), 'utf8'));
  assert.equal(run.status, 'complete');
  assert.equal(run.results.length, 96);
  const totals = new Map<string, number>();
  const calls = new Set<string>();
  for (const row of run.results) {
    const task = byId.get(row.taskId)!;
    assert.deepEqual(evaluateMechanismTask(task, row.answer), row.verdict);
    assert.ok(!calls.has(row.call.id)); calls.add(row.call.id);
    totals.set(row.model, (totals.get(row.model) ?? 0) + row.verdict.success);
  }
  assert.equal(totals.get('openai/gpt-4.1-mini'), 28);
  assert.equal(totals.get('google/gemini-2.5-flash'), 31);
  assert.ok(run.campaignAfter <= 4.5);
  assert.ok(run.campaignAfter - run.campaignBefore < .07);
});
