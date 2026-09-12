import assert from 'node:assert/strict';
import { cpSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS, BENCHMARK } from '../storage';
import { selectCases, verifySelection } from '../v2/batch';
import { taskForV2 } from '../v2/cases';
import { jsonLines } from '../v2/verify';
import { strictBatch } from './strict-batch';
import { replayStrictRun } from './strict-replay';
import { strictTrace } from './strict-trace';
import { EVALUATOR_VERSION } from './strict-evaluate';
import { STUDY } from './protocol';

const selection = selectCases('test_ood', 'ordinary', 1), specs = verifySelection(selection);
const reconstruct = specs.find(s => s.kind === 'reconstruct')!;
const malformed = structuredClone(taskForV2(reconstruct).target) as any;
malformed.parts[0].color = [malformed.parts[0].color];
const predictions = new Map<string, unknown>([[reconstruct.id, malformed]]);
await assert.rejects(strictBatch(selection, new Map([['unknown', null]]), 'reject-test'), /Unknown/);
const existing = process.argv.find(a => a.startsWith('--run='))?.slice(6);
const result = existing ? { id: existing } : await strictBatch(selection, predictions, 'schema-regression-fixture-not-a-model');
const dir = resolve(ARTIFACTS, 'evaluations-v2', result.id);
await replayStrictRun(dir);
let checked = 0;
for await (const row of jsonLines(resolve(dir, 'cases.jsonl.gz'))) {
  assert.equal(row.verdict.metrics.success, 0);
  assert.equal(row.missing, row.spec.id !== reconstruct.id);
  if (row.spec.id === reconstruct.id) {
    assert.deepEqual(row.answer, malformed);
    const trace = strictTrace(result.id, 'fixture', row, []);
    assert.equal(trace.events.filter(e => e.kind === 'unfold').length, 0);
    assert.deepEqual(trace.output, []);
  }
  checked++;
}
assert.equal(checked, specs.length);
const temporary = mkdtempSync(resolve(tmpdir(), 'brickatlas-strict-replay-'));
try {
  cpSync(dir, temporary, { recursive: true });
  const summary = JSON.parse(readFileSync(resolve(temporary, 'summary.json'), 'utf8'));
  summary.rows[0].metrics.success.value = 1;
  atomicJson(resolve(temporary, 'summary.json'), summary);
  await assert.rejects(replayStrictRun(temporary));
} finally { rmSync(temporary, { recursive: true, force: true }); }
const { url } = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
const status = await (await fetch(url + '/api/status')).json();
const response = await fetch(url + '/api/v2/evaluate', {
  method: 'POST', headers: { 'Content-Type': 'application/json', 'x-benchmark-client': status.token },
  body: JSON.stringify({ caseId: reconstruct.id, answer: malformed }),
});
assert.equal(response.status, 200);
const verdict = await response.json();
assert.equal(verdict.evaluatorVersion, EVALUATOR_VERSION);
assert.equal(verdict.metrics.success, 0); assert.equal(verdict.metrics.format, 0);
const evidence = { evaluatorVersion: EVALUATOR_VERSION, cases: checked, runId: result.id,
  missingDenominatorPreserved: true, rawMalformedPreserved: true, malformedNotUnfolded: true,
  scoreAndAllAggregatesReplayed: true, tamperedAggregateRejected: true, httpSchemaRejected: true, apiRequests: 0 };
atomicJson(resolve(STUDY, 'strict-roundtrip.json'), evidence);
console.log(JSON.stringify(evidence, null, 2));
