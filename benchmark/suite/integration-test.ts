import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { ARTIFACTS, BENCHMARK, SUITE, listRuns } from './storage';
import { models } from './data';
import { atomicJson } from '../core/budget';

const run = listRuns().find(r => r.mode === 'one-shot' && r.representation === 'absolute' && r.status === 'complete');
assert.ok(run, 'Run one-shot smoke before integration test');
const selectedModel = run.models[0], rows = run.results.filter(r => r.model === selectedModel);
const file = resolve(BENCHMARK, '.runtime/suite-exports/predictions.from-real-run.jsonl');
writeFileSync(file, rows.map(r => JSON.stringify({ taskId: r.taskId, answer: r.answers.at(-1) })).join('\n') + '\n');
execFileSync(process.execPath, [resolve(BENCHMARK, '../node_modules/tsx/dist/cli.mjs'),
  resolve(SUITE, 'cli.ts'), 'score', `--predictions=${file}`], { stdio: 'pipe' });
const rescored = JSON.parse(readFileSync(resolve(ARTIFACTS, 'external-scores.json'), 'utf8')) as {
  taskId: string; missing: boolean; verdict: unknown;
}[];
assert.equal(rescored.length, 16);
for (const row of rescored) {
  assert.equal(row.missing, false);
  assert.deepEqual(row.verdict, rows.find(r => r.taskId === row.taskId)!.verdict);
}
const groups = new Map<string, string>(), counts: Record<string, number> = {};
for (const split of ['train', 'validation']) {
  const lines = readFileSync(resolve(BENCHMARK, `.runtime/suite-exports/${split}.sft.jsonl`), 'utf8')
    .trim().split('\n').map(line => JSON.parse(line));
  counts[split] = lines.length;
  for (const line of lines) {
    assert.equal(line.split, split);
    if (groups.has(line.group)) assert.equal(groups.get(line.group), split);
    groups.set(line.group, split);
    assert.ok(models().some(m => m.group === line.group && m.split === split));
    assert.equal(line.messages[2].role, 'assistant');
    assert.equal(line.needsImages, line.renderRequests.length > 0);
  }
}
const inputs = readFileSync(resolve(BENCHMARK, '.runtime/suite-exports/inputs.jsonl'), 'utf8')
  .trim().split('\n').map(line => JSON.parse(line));
for (const row of inputs) {
  assert.ok(!('renderRequests' in row));
  assert.ok(!('oracle' in row.input));
  assert.ok(['test_id', 'test_ood'].includes(row.input.split));
  assert.equal(row.images.length > 0, row.modality === 'RGB+text');
  for (const image of row.images) assert.ok(readFileSync(resolve(BENCHMARK, '.runtime/suite-exports', image)).length > 1000);
}
// Missing submissions fail rather than disappearing from the denominator.
writeFileSync(file, '');
execFileSync(process.execPath, [resolve(BENCHMARK, '../node_modules/tsx/dist/cli.mjs'),
  resolve(SUITE, 'cli.ts'), 'score', `--predictions=${file}`], { stdio: 'pipe' });
const missing = JSON.parse(readFileSync(resolve(ARTIFACTS, 'external-scores.json'), 'utf8'));
assert.equal(missing.length, 16);
assert.ok(missing.every((r: { missing: boolean; verdict: { metrics: { success: number } } }) => r.missing && r.verdict.metrics.success === 0));
writeFileSync(file, rows.map(r => JSON.stringify({ taskId: r.taskId, answer: r.answers.at(-1) })).join('\n') + '\n');
execFileSync(process.execPath, [resolve(BENCHMARK, '../node_modules/tsx/dist/cli.mjs'),
  resolve(SUITE, 'cli.ts'), 'score', `--predictions=${file}`], { stdio: 'pipe' });
const result = { checkedAt: new Date().toISOString(), paidRequests: 0, realPredictionsRescored: rows.length,
  trainingRows: counts, crossSplitGroupLeakage: false, testInputsExported: inputs.length,
  exportedModelInputsContainPrivateRenderGeometry: false, missingSubmissionsCountAsFailures: true };
atomicJson(resolve(ARTIFACTS, 'integration.json'), result);
console.log(JSON.stringify(result, null, 2));
