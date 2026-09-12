import assert from 'node:assert/strict';
import { resolve } from 'node:path';
import { readFileSync, readdirSync } from 'node:fs';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS } from '../storage';
import { jsonLines } from '../v2/verify';
import { getSpec, taskForV2, caseSpecs } from '../v2/cases';
import { evaluateStrict, EVALUATOR_VERSION } from './strict-evaluate';
import { studyRuns } from './results';
import { STUDY } from './protocol';

export async function strictAudit() {
  let oracleCases = 0, existingCases = 0, malformedRejected = 0;
  const differences = [];
  for (const s of caseSpecs()) {
    const task = taskForV2(s);
    assert.equal(evaluateStrict(task, task.oracle).metrics.success, 1); oracleCases++;
    if (s.kind === 'reconstruct' && s.condition === 'ordinary') {
      const malformed = structuredClone(task.target) as any;
      malformed.parts[0].color = [malformed.parts[0].color];
      assert.equal(evaluateStrict(task, malformed).metrics.success, 0); malformedRejected++;
    }
  }
  for (const run of readdirSync(resolve(ARTIFACTS, 'evaluations-v2'))) {
    for await (const row of jsonLines(resolve(ARTIFACTS, 'evaluations-v2', run, 'cases.jsonl.gz'))) {
      const verdict = evaluateStrict(taskForV2(getSpec(row.spec.id)), row.answer);
      try { assert.deepEqual(verdict.metrics, row.verdict.metrics); }
      catch { differences.push({ run, caseId: row.spec.id }); }
      existingCases++;
    }
  }
  for (const run of studyRuns()) for (const row of run.rows) {
    const verdict = evaluateStrict(taskForV2(getSpec(row.caseId)), row.answer);
    try { assert.deepEqual(verdict.metrics, row.verdict.metrics); }
    catch { differences.push({ run: run.id, caseId: row.caseId }); }
    existingCases++;
  }
  const report = { evaluatorVersion: EVALUATOR_VERSION, oracleCases, existingCases, malformedRejected, differences,
    reason: 'Legacy Object.hasOwn converted array partId/color to a string key. Strict primitive-type validation now rejects it.',
    scope: 'Historical metrics rechecked without overwriting source runs. Invalid-response issue wording can differ.' };
  atomicJson(resolve(STUDY, 'strict-audit.json'), report);
  assert.equal(differences.length, 0); return report;
}
