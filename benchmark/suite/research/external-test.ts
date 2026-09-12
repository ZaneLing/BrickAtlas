import assert from 'node:assert/strict';
import { readFileSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS, BENCHMARK, listRuns } from '../storage';
import { digest } from '../data';
import { RESEARCH_VERSION } from './dataset';
import { type ResearchRun } from './run';
import { scoreResearchPredictions } from './external';

const dir = resolve(BENCHMARK, '.runtime/research-exports');
const inputs = readFileSync(resolve(dir, 'inputs.jsonl'), 'utf8').trim().split('\n').map(l => JSON.parse(l));
const run = listRuns().find(r => r.version === RESEARCH_VERSION) as ResearchRun;
assert.equal(inputs.length, 56);
const rows = run.results.filter(r => r.model === run.models[0]);
for (const input of inputs) {
  assert.deepEqual(input.input, rows.find(r => r.taskId === input.taskId)!.input);
  assert.ok(!('frames' in input) && !('oracle' in input));
  for (const image of input.images) {
    assert.match(image, /^images\/[a-f0-9]{64}\.png$/);
    assert.equal(digest(readFileSync(resolve(dir, image)).toString('base64')), image.slice(7, -4));
  }
}
const temp = mkdtempSync(resolve(BENCHMARK, '.runtime/external-check-')), file = resolve(temp, 'predictions.jsonl');
try {
  const predictions = rows.map(r => ({ taskId: r.taskId, answer: r.answers.at(-1) }));
  writeFileSync(file, '');
  const missing = scoreResearchPredictions(file);
  assert.equal(missing.rows.length, 56);
  assert.ok(missing.rows.every(r => r.missing && r.verdict.metrics.success === 0));
  writeFileSync(file, [predictions[0], predictions[0]].map(r => JSON.stringify(r)).join('\n'));
  assert.throws(() => scoreResearchPredictions(file), /Duplicate/);
  writeFileSync(file, JSON.stringify({ taskId: 'unknown', answer: {} }));
  assert.throws(() => scoreResearchPredictions(file), /Unknown/);
  writeFileSync(file, predictions.map(r => JSON.stringify(r)).join('\n'));
  const scored = scoreResearchPredictions(file);
  for (const row of scored.rows) assert.deepEqual(row.verdict, rows.find(r => r.taskId === row.taskId)!.verdict);
  const result = { checkedAt: new Date().toISOString(), exportedInputs: inputs.length, verifiedScores: scored.rows.length,
    imageHashesVerified: true, missingFails: true, duplicateRejected: true, unknownRejected: true, apiRequests: 0 };
  atomicJson(resolve(ARTIFACTS, 'research/external-verification.json'), result);
  console.log(JSON.stringify(result, null, 2));
} finally { rmSync(temp, { recursive: true }); }
