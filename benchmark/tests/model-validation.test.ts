import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { Budget } from '../core/budget';
import { validationCeiling, validationCompletion } from '../suite/study/validation-client';
import { validationCases } from '../suite/study/model-validation';
import { validationAggregate, classifyPatterns, copyInputAnswer } from '../suite/study/model-validation-report';
import { ladderTasks, normalizeOrigin } from '../suite/study/reconstruction-ladder';
import { evaluateStrict } from '../suite/study/strict-evaluate';
import { getSpec, taskForV2 } from '../suite/v2/cases';

test('validation sample is fixed across models and does not pool controls', () => {
  const { chosen, rows } = validationCases();
  assert.deepEqual(chosen.map(o => o.difficulty), ['small', 'medium', 'large']);
  assert.equal(new Set(chosen.map(o => o.group)).size, 3);
  assert.equal(rows.length, 45);
  assert.equal(rows.filter(r => r.arm === 'ordinary').length, 39);
  for (const row of rows.filter(r => r.arm !== 'ordinary')) {
    assert.deepEqual(row.images, []);
    assert.equal('reference' in row.input.input, row.arm === 'symbolic-reference');
  }
});

test('new validation models cannot bypass the allowlist or prompt limits', () => {
  assert.throws(() => validationCeiling('unknown', []));
  assert.throws(() => validationCeiling('openai/gpt-4.1', [{ role: 'user', content: 'x'.repeat(51000) }]));
  assert.ok(validationCeiling('openai/gpt-4.1', [{ role: 'user', content: '{}' }]) > 0);
});

test('validation summaries keep missing evidence distinct from cognitive failures', () => {
  const row = { diagnosis: { stage: 'json', formatAccepted: false, tokenLimitReached: true,
    verdict: { metrics: { format: 0, valid: 0, success: 0, partF1: 0, falseAlarm: null } } },
    call: { cost: 0.01, promptTokens: 100, completionTokens: 2200, reasoningTokens: 0, latencyMs: 1000 } };
  const report = validationAggregate([row], 3);
  assert.equal(report.missing, 2);
  assert.equal(report.stages.json, 1);
  assert.equal(report.metrics.partF1.denominator, 1);
  assert.equal(report.metrics.falseAlarm.value, null);
  assert.equal(report.metrics.falseAlarm.denominator, 0);
  assert.equal(validationAggregate([], 3).latencyMs, null);
  assert.throws(() => validationAggregate([row], 0));
});

test('mixed task success is not automatically between-model discrimination', () => {
  assert.deepEqual(classifyPatterns([[1, 0, 0], [1, 0, 0]]),
    { classification: 'mixed', modelOutcomesDiffer: false, aggregateCountsDiffer: false });
  assert.deepEqual(classifyPatterns([[1, 0, 0], [0, 1, 0]]),
    { classification: 'mixed', modelOutcomesDiffer: true, aggregateCountsDiffer: false });
  assert.equal(classifyPatterns([[0, 0], [0, 0]]).classification, 'floor');
  assert.equal(classifyPatterns([[1, 1], [1, 1]]).classification, 'ceiling');
  assert.equal(classifyPatterns([[1, null], [1, 0]]).classification, 'incomplete');
});

test('reconstruction ladder is a distinct source and all six oracle tasks are valid', () => {
  const tasks = ladderTasks(), excluded = new Set(validationCases().chosen.map(o => o.group));
  assert.equal(tasks.length, 6);
  assert.equal(new Set(tasks.map(t => t.task.spec.group)).size, 1);
  for (const row of tasks) {
    assert.ok(!excluded.has(row.task.spec.group));
    assert.equal(row.task.target.parts.length, row.count);
    assert.equal(evaluateStrict(row.task, row.task.oracle).metrics.success, 1);
    assert.equal(row.task.frames.length, row.condition === 'ordinary' ? 4 : 0);
    assert.equal('reference' in row.task.public.input, row.condition === 'symbolic');
  }
});

test('copy-input baseline never repairs a shifted piece using evaluator truth', () => {
  const row = validationCases().rows.find(r => {
    const s = getSpec(r.caseId); return r.arm === 'ordinary' && s.kind === 'repair' && s.variant === 'shift';
  })!;
  const task = taskForV2(getSpec(row.caseId)), answer = copyInputAnswer(task.public) as any;
  assert.deepEqual(answer, { structure: task.public.input.current, faultIds: [] });
  assert.equal(evaluateStrict(task, answer).metrics.success, 0);
  const before = JSON.stringify(task.public);
  (answer.structure as any).parts[0].color = 'blue';
  assert.equal(JSON.stringify(task.public), before, 'Baseline must not mutate input');
});

test('cropped ladder v2 anchors each prefix without silently changing v1', () => {
  const old = ladderTasks(), revised = ladderTasks(true);
  assert.equal(Math.min(...old[0].task.target.parts.map(p => p.z)), 1);
  for (const [i, row] of revised.entries()) {
    assert.notEqual(row.task.spec.id, old[i].task.spec.id);
    for (const axis of ['x', 'y', 'z'] as const) assert.equal(Math.min(...row.task.target.parts.map(p => p[axis])), 0);
    assert.deepEqual(normalizeOrigin(old[i].task.target), row.task.target);
    assert.equal(evaluateStrict(row.task, row.task.oracle).metrics.success, 1);
  }
  assert.equal(Math.min(...old[0].task.target.parts.map(p => p.z)), 1, 'Normalization does not mutate frozen v1');
});

test('billing is settled from actual receipts and HTTP failure blocks new requests', async () => {
  const dir = mkdtempSync(resolve(tmpdir(), 'validation-budget-'));
  try {
    const budget = new Budget(resolve(dir, 'ledger.json'));
    const ok = (async () => new Response(JSON.stringify({ id: 'receipt-1', provider: 'fixture',
      choices: [{ message: { content: '{}' }, finish_reason: 'stop' }],
      usage: { cost: 0.001, prompt_tokens: 20, completion_tokens: 2 } }))) as typeof fetch;
    await validationCompletion('test-only', 'openai/gpt-4.1', [], budget, ok);
    assert.equal(budget.spent, 0.001); assert.equal(budget.blocked, false);
    const fail = (async () => new Response('unlogged error', { status: 503 })) as typeof fetch;
    await assert.rejects(validationCompletion('test-only', 'openai/gpt-4.1', [], budget, fail), /503/);
    assert.equal(budget.blocked, true);
    await assert.rejects(validationCompletion('test-only', 'openai/gpt-4.1', [], budget, ok), /Unsettled/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
