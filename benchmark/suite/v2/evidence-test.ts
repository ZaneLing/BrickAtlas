import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS, BENCHMARK } from '../storage';
import { selectCases, scoreBatch, readPredictions, verifySelection, clusterBootstrap } from './batch';
import { taskForV2 } from './cases';
import { publicAlgorithm } from './baseline';
import { evaluate } from './evaluate';

const selection = selectCases('test_id', 'all', 2), specs = verifySelection(selection);
const temp = mkdtempSync(resolve(BENCHMARK, '.runtime/v2-test-'));
const runs: string[] = [];
try {
  const predictions = new Map(specs.map(s => [s.id, taskForV2(s).oracle]));
  const correct = await scoreBatch(selection, predictions, 'TEST_ONLY_ORACLE'); runs.push(correct.id);
  let summary = JSON.parse(readFileSync(resolve(ARTIFACTS, 'evaluations-v2', correct.id, 'summary.json'), 'utf8'));
  assert.ok(summary.rows.every((r: any) => r.metrics.success.value === 1));
  predictions.delete(specs[0].id);
  const missing = await scoreBatch(selection, predictions, 'TEST_ONLY_MISSING'); runs.push(missing.id);
  summary = JSON.parse(readFileSync(resolve(ARTIFACTS, 'evaluations-v2', missing.id, 'summary.json'), 'utf8'));
  const stratum = summary.rows.find((r: any) => r.stratum === ['task', specs[0].kind, specs[0].variant, specs[0].condition, specs[0].split].join('|'));
  assert.equal(stratum.missing, 1); assert.equal(stratum.metrics.success.denominator, stratum.n);
  assert.ok(stratum.metrics.success.value < 1);
  await assert.rejects(scoreBatch(selection, new Map([['not-in-selection', {}]]), 'TEST_ONLY_UNKNOWN'), /out-of-selection/);
  const file = resolve(temp, 'duplicates.jsonl');
  writeFileSync(file, '{"caseId":"a","answer":{}}\n{"caseId":"a","answer":{}}\n');
  await assert.rejects(readPredictions(file), /Duplicate/);
  assert.throws(() => verifySelection({ ...selection, caseIds: selection.caseIds.slice(1) }), /Invalid/);
  const ci = clusterBootstrap([0, 0, 1, 1])!;
  assert.equal(ci.groups, 4); assert.equal(ci.mean, 0.5);
  let algorithms = 0, incompleteGreedyPlans = 0;
  for (const s of specs) {
    const t = taskForV2(s), answer = publicAlgorithm(t.public);
    if (answer !== null) {
      const verdict = evaluate(t, answer);
      if (s.kind === 'plan' && verdict.metrics.success === 0) {
        assert.deepEqual(verdict.issues, ['incomplete']); incompleteGreedyPlans++;
      } else assert.equal(verdict.metrics.success, 1, s.id);
      algorithms++;
    }
  }
  const evidence = { checkedAt: new Date().toISOString(), cases: specs.length, oracleBatchPass: true,
    missingCountedInDenominator: true, duplicateRejected: true, unknownRejected: true, selectionDriftRejected: true,
    publicAlgorithmsVerified: algorithms, incompleteGreedyPlans, objectBootstrapVerified: true, fixtureRunsPublished: false, apiRequests: 0 };
  atomicJson(resolve(ARTIFACTS, 'casebank-v2/evaluation-verification.json'), evidence);
  console.log(JSON.stringify(evidence, null, 2));
} finally {
  rmSync(temp, { recursive: true });
  for (const id of runs) rmSync(resolve(ARTIFACTS, 'evaluations-v2', id), { recursive: true });
}
