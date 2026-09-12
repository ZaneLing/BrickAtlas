import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS } from '../storage';
import { digest } from '../data';
import { evaluationHashes, verifySelection } from './batch';
import { jsonLines } from './verify';
import { taskForV2, getSpec } from './cases';
import { evaluate } from './evaluate';
import { publicAlgorithm } from './baseline';
import { DIRECTORY, sourceHashes } from './build';
import { submissionTrace } from './trace';
import { EVALUATOR_VERSION } from '../study/strict-evaluate';
import { replayStrictRun } from '../study/strict-replay';

export async function replayEvaluations() {
  const root = resolve(ARTIFACTS, 'evaluations-v2'), result = [];
  for (const id of readdirSync(root)) {
    const dir = resolve(root, id), summary = JSON.parse(readFileSync(resolve(dir, 'summary.json'), 'utf8'));
    if (summary.evaluatorVersion === EVALUATOR_VERSION) {
      result.push(await replayStrictRun(dir)); continue;
    }
    assert.equal(summary.evaluatorVersion, undefined, 'Unknown evaluator version');
    const selection = JSON.parse(readFileSync(resolve(dir, 'selection.json'), 'utf8'));
    const expected = new Set(verifySelection(selection).map(s => s.id)), seen = new Set<string>();
    assert.deepEqual(summary.sourceHashes, sourceHashes()); assert.equal(summary.selectionHash, selection.hash);
    assert.deepEqual(summary.evaluationHashes, evaluationHashes());
    const taskStats = new Map<string, { n: number; sum: number; missing: number; sums: Record<string, number>; counts: Record<string, number> }>();
    let traces = 0;
    for await (const row of jsonLines(resolve(dir, 'cases.jsonl.gz'))) {
      assert.ok(expected.has(row.spec.id) && !seen.has(row.spec.id)); seen.add(row.spec.id);
      const spec = getSpec(row.spec.id); assert.deepEqual(spec, row.spec);
      const task = taskForV2(spec); assert.equal(row.inputHash, digest(task.public));
      assert.deepEqual(row.verdict, evaluate(task, row.answer));
      if (summary.baseline) assert.deepEqual(row.answer, publicAlgorithm(task.public));
      const key = ['task', spec.kind, spec.variant, spec.condition, spec.split].join('|');
      const r: NonNullable<ReturnType<typeof taskStats.get>> = taskStats.get(key) ?? { n: 0, sum: 0, missing: 0, sums: {}, counts: {} };
      r.n++; r.sum += row.verdict.metrics.success; r.missing += Number(row.missing); taskStats.set(key, r);
      for (const [metric, value] of Object.entries(row.verdict.metrics)) if (typeof value === 'number') {
        r.sums[metric] = (r.sums[metric] ?? 0) + value; r.counts[metric] = (r.counts[metric] ?? 0) + 1;
      }
      // Every submitted plan and structure replay must reproduce its score and state chain.
      const trace = submissionTrace(id, summary.model, summary.baseline, row, []);
      assert.deepEqual(trace.verdict, row.verdict);
      for (const [i, event] of trace.events.entries()) {
        assert.equal(digest(trace.states[event.after]), event.after);
        if (i) assert.equal(event.before, trace.events[i - 1].after);
      }
      traces++;
    }
    assert.equal(seen.size, expected.size); assert.equal(summary.cases, seen.size);
    for (const [key, r] of taskStats) {
      const original = summary.rows.find((r: { stratum: string }) => r.stratum === key);
      assert.equal(original.n, r.n); assert.equal(original.missing, r.missing);
      assert.equal(original.metrics.success.value, r.sum / r.n); assert.equal(original.metrics.success.denominator, r.n);
      for (const [metric, sum] of Object.entries(r.sums)) {
        assert.equal(original.metrics[metric].value, sum / r.counts[metric]);
        assert.equal(original.metrics[metric].denominator, r.counts[metric]);
      }
    }
    result.push({ id, cases: seen.size, traceCases: traces, scoresReproduced: true,
      publicBaselineRecomputed: summary.baseline, compressedSha256: createHash('sha256').update(readFileSync(resolve(dir, 'cases.jsonl.gz'))).digest('hex') });
  }
  const evidence = { checkedAt: new Date().toISOString(), runs: result, apiRequests: 0 };
  atomicJson(resolve(DIRECTORY, 'replay-evaluations.json'), evidence);
  return evidence;
}
