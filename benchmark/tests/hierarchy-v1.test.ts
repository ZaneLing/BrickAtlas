import assert from 'node:assert/strict';
import test from 'node:test';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { evaluateHierarchyTask } from '../suite/hierarchy/evaluate';
import { hierarchyModels } from '../suite/hierarchy/models';
import { scoreHierarchyResponses } from '../suite/hierarchy/score';
import { hierarchyTasks, pilotSelection } from '../suite/hierarchy/tasks';
import { ATOMIC_OPERATIONS, DIFFICULTIES, META_FAMILIES, TASK_LAYERS } from '../suite/hierarchy/types';

const output = resolve(import.meta.dirname, '../hierarchy-v1');
const sha256 = (path: string) => createHash('sha256').update(readFileSync(path)).digest('hex');
const median = (values: number[]) => {
  const ordered = [...values].sort((a, b) => a - b);
  return ordered[Math.floor(ordered.length / 2)];
};

test('hierarchy-v1: 18 original objects form four increasing difficulty strata', () => {
  const models = hierarchyModels();
  assert.equal(models.length, 18);
  assert.deepEqual(Object.fromEntries(DIFFICULTIES.map(level => [
    level.id,
    models.filter(model => model.difficulty === level.id).length,
  ])), { D1: 4, D2: 4, D3: 6, D4: 4 });
  assert.ok(models.every(model => model.originalDesign));
  assert.ok(models.every(model => model.modules.some(module => module.anchored)));
  assert.ok(models.every(model => model.joints.some(joint => ['revolute', 'prismatic'].includes(joint.type))));
  const medians = DIFFICULTIES.map(level => median(models.filter(model => model.difficulty === level.id)
    .map(model => model.complexity.complexityIndex)));
  assert.ok(medians.every((value, index) => index === 0 || value > medians[index - 1]), medians.join(','));
  assert.equal(models.filter(model => model.difficulty === 'D4').reduce((sum, model) => sum + model.parts.length, 0), 896);
  assert.ok(!JSON.stringify(models).includes('library.ldraw.org'));
});

test('hierarchy-v1: every object has all four task layers and atomic coverage is complete', () => {
  const models = hierarchyModels(), tasks = hierarchyTasks();
  assert.equal(tasks.length, 90);
  for (const model of models) {
    const selected = tasks.filter(task => task.sourceGroup === model.id);
    assert.equal(selected.length, 5);
    assert.equal(selected.filter(task => task.layer === 'atomic').length, 2);
    for (const layer of TASK_LAYERS.filter(layer => layer.id !== 'atomic')) {
      assert.equal(selected.filter(task => task.layer === layer.id).length, 1);
    }
  }
  assert.deepEqual([...new Set(tasks.filter(task => task.family === 'atomic-operation-coverage')
    .map(task => task.operation))].sort(), [...ATOMIC_OPERATIONS].sort());
  const metaCounts = new Map(META_FAMILIES.map(family => [
    family,
    tasks.filter(task => task.layer === 'metacognitive' && task.family === family).length,
  ]));
  assert.ok([...metaCounts.values()].every(count => count === 2));
});

test('hierarchy-v1: all answer contracts pass their oracle and reject a malformed answer', () => {
  const tasks = hierarchyTasks();
  for (const task of tasks) {
    assert.equal(evaluateHierarchyTask(task, task.oracle).success, 1, task.id);
    assert.equal(evaluateHierarchyTask(task, {}).success, 0, task.id);
    if (task.format === 'single-choice' || task.format === 'multiple-choice') {
      assert.equal(task.options?.length, 4, task.id);
    }
  }
  const answerPositions = new Set(tasks.filter(task => task.format === 'single-choice')
    .map(task => task.oracle.choiceId));
  assert.deepEqual([...answerPositions].sort(), ['A', 'B', 'C', 'D']);
});

test('hierarchy-v1: procedural dependency scoring accepts equivalent topological orders', () => {
  const tasks = hierarchyTasks();
  for (const task of tasks.filter(candidate =>
    ['assembly-sequencing', 'safe-disassembly'].includes(candidate.family))) {
    const reference = task.oracle.actionIds as string[];
    const edges = task.input.dependencyEdges as Array<[string, string]>;
    const independentSwap = [...reference];
    let swapped = false;
    for (let index = 0; index < independentSwap.length - 1 && !swapped; index++) {
      const left = independentSwap[index].split(':').slice(1).join(':');
      const right = independentSwap[index + 1].split(':').slice(1).join(':');
      const dependent = edges.some(([parent, child]) =>
        (parent === left && child === right) || (parent === right && child === left));
      if (!dependent) {
        [independentSwap[index], independentSwap[index + 1]] =
          [independentSwap[index + 1], independentSwap[index]];
        swapped = true;
      }
    }
    if (swapped) assert.equal(evaluateHierarchyTask(task, { actionIds: independentSwap }).success, 1, task.id);
    assert.equal(evaluateHierarchyTask(task, { actionIds: reference.slice(1) }).success, 0, task.id);
  }
});

test('hierarchy-v1: missing, duplicate, and unknown submissions fail closed', () => {
  const tasks = hierarchyTasks();
  const empty = scoreHierarchyResponses([]);
  assert.equal(empty.expected, 90);
  assert.equal(empty.missing, 90);
  assert.equal(empty.success, 0);
  assert.throws(() => scoreHierarchyResponses([{ id: 'unknown', answer: {} }]));
  assert.throws(() => scoreHierarchyResponses([
    { id: tasks[0].id, answer: tasks[0].oracle },
    { id: tasks[0].id, answer: tasks[0].oracle },
  ]));
});

test('hierarchy-v1: pilot is a fixed complete difficulty-by-layer matrix', () => {
  const selected = pilotSelection();
  assert.equal(selected.length, 16);
  for (const difficulty of DIFFICULTIES) for (const layer of TASK_LAYERS) {
    assert.equal(selected.filter(task =>
      task.difficulty === difficulty.id && task.layer === layer.id).length, 1);
  }
  assert.ok(new Set(selected.map(task => task.sourceGroup)).size >= 10);
});

test('hierarchy-v1: all model and task renders are present and pixel audited', () => {
  const audit = JSON.parse(readFileSync(resolve(output, 'render-audit.json'), 'utf8'));
  assert.equal(audit.frames.length, 162);
  assert.equal(audit.frames.filter((frame: any) => frame.type === 'model').length, 72);
  assert.equal(audit.frames.filter((frame: any) => frame.type === 'task').length, 90);
  for (const frame of audit.frames) {
    const path = resolve(output, frame.file);
    assert.ok(existsSync(path), frame.file);
    assert.equal(sha256(path), frame.sha256, frame.file);
    assert.equal(frame.pixels.width, 1200);
    assert.equal(frame.pixels.height, 900);
    assert.ok(frame.pixels.foreground > 10_000);
  }
});

test('hierarchy-v1: public export excludes oracle answers', () => {
  const rows = JSON.parse(readFileSync(resolve(output, 'public.json'), 'utf8'));
  assert.equal(rows.length, 90);
  assert.ok(rows.every((row: any) => !Object.hasOwn(row, 'oracle')));
  assert.ok(rows.every((row: any) => row.responseSchema && row.visualization?.detailImage));
});

test('hierarchy-v1: archived low-cost pilot replays exactly when present', () => {
  const latestPath = resolve(output, 'results/latest.json');
  if (!existsSync(latestPath)) return;
  const latest = JSON.parse(readFileSync(latestPath, 'utf8'));
  const run = JSON.parse(readFileSync(resolve(output, 'results', latest.path), 'utf8'));
  const byId = new Map(hierarchyTasks().map(task => [task.id, task]));
  assert.equal(run.status, 'complete');
  assert.equal(run.cases.length, 16);
  assert.equal(run.results.length, run.models.length * run.cases.length);
  assert.equal(run.settings.protocolSha256, sha256(resolve(output, 'frozen-protocol.json')));
  assert.equal(run.settings.publicSha256, sha256(resolve(output, 'public.json')));
  assert.equal(run.settings.renderAuditSha256, sha256(resolve(output, 'render-audit.json')));
  for (const row of run.results) {
    assert.deepEqual(evaluateHierarchyTask(byId.get(row.taskId)!, row.answer), row.verdict);
  }
  assert.ok(run.campaignAfter - run.campaignBefore <= 0.12);
});

test('hierarchy-v1: release manifest and excluded 429 evidence are hash-complete', () => {
  const manifest = JSON.parse(readFileSync(resolve(output, 'manifest.json'), 'utf8'));
  for (const [path, expected] of Object.entries(manifest.files)) {
    assert.equal(sha256(resolve(output, path)), expected, path);
  }
  for (const [path, expected] of Object.entries(manifest.sources)) {
    assert.equal(sha256(resolve(import.meta.dirname, '../suite/hierarchy', path)), expected, path);
  }
  const reconciliation = JSON.parse(readFileSync(resolve(output,
    'results/2026-09-15T12-22-28-577Z-hierarchy/reconciliation.json'), 'utf8'));
  assert.equal(reconciliation.events.length, 2);
  assert.ok(reconciliation.events.every((event: any) =>
    event.httpStatus === 429 && event.generationId === null && event.settledActual === 0));
  const ledger = JSON.parse(readFileSync(resolve(output,
    'results/2026-09-15T12-22-28-577Z-hierarchy/ledger.json'), 'utf8'));
  assert.ok(ledger.charges.every((charge: any) => charge.status === 'settled'));
});
