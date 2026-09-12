import { test } from 'node:test';
import assert from 'node:assert/strict';
import { listRuns } from '../suite/storage';
import { clusterInterval } from '../suite/research/statistics';
import { replayLocal, type LocalRun } from '../suite/research/local-results';
import { PAIRED_VERSION, replayPaired, type PairedRun } from '../suite/research/paired';

test('cluster intervals resample source objects, retaining paired signs', () => {
  assert.deepEqual(clusterInterval([0, 0, 0, 0]), { mean: 0, low: 0, high: 0, clusters: 4, resamples: 256 });
  const result = clusterInterval([-1, 1, -1, 1]);
  assert.equal(result.mean, 0); assert.equal(result.low, -1); assert.equal(result.high, 1);
  assert.throws(() => clusterInterval([]));
});
test('portable local evidence rejects modified model output even if parsed score matches', () => {
  const run = structuredClone(listRuns().find(r => r.version === 'local-text-training-v1')) as LocalRun;
  assert.ok(run); assert.equal(replayLocal(run).scoresReproduced, true);
  run.results[0].calls[0].content += ' ';
  assert.throws(() => replayLocal(run), /drift/);
});
test('paired runs reproduce charges and reject modified refinement prompts', () => {
  const runs = listRuns().filter(r => r.version === PAIRED_VERSION) as unknown as PairedRun[];
  assert.ok(runs.length >= 2);
  for (const original of runs) {
    assert.equal(replayPaired(original).calls, 12);
    const run = structuredClone(original);
    run.results[0].refinementPrompt += ' changed';
    assert.throws(() => replayPaired(run), /prompt changed/);
  }
});
