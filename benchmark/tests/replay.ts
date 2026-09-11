import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { Environment } from '../core/environment';
import { makeTask } from '../core/tasks';
import { atomicJson, type Ledger } from '../core/budget';
import { BUILDER_PROMPT } from '../core/prompts';
import type { RunResult, TraceStep } from '../core/results';
import type { Fault } from '../shared/types';
import { ROOT, hash } from '../run';

const { id } = JSON.parse(readFileSync(resolve(ROOT, 'results/latest.json'), 'utf8'));
const dir = resolve(ROOT, 'results', id);
const run = JSON.parse(readFileSync(resolve(dir, 'run.json'), 'utf8')) as RunResult;
assert.equal(run.status, 'complete');
let decisions = 0;
let cost = 0;
const ids = new Set<string>();
const checkedImages = new Set<string>();
function trace(env: Environment, items: TraceStep[]) {
  for (const step of items) {
    assert.deepEqual(env.observe(), step.observation, 'Model received a different observation');
    const path = resolve(dir, step.image);
    assert.ok(path.startsWith(`${dir}/observations/`));
    if (!checkedImages.has(path)) {
      assert.equal(hash(readFileSync(path)), step.image.split('/').at(-1)!.replace('.png', ''));
      checkedImages.add(path);
    }
    assert.ok(!ids.has(step.response.id), 'Duplicate generation receipt');
    ids.add(step.response.id);
    assert.ok(Number.isFinite(step.response.cost) && step.response.cost >= 0);
    cost += step.response.cost;
    env.step(step.action);
    assert.equal(env.feedback, step.feedback);
    decisions++;
  }
}
for (const episode of run.episodes) {
  assert.equal(episode.status, 'complete');
  const env = new Environment(makeTask(episode.seed, episode.variant as 0 | 1, episode.fault), episode.protocol);
  trace(env, episode.trace);
  assert.deepEqual(env.score(), episode.score, 'Recomputed score differs');
}
let conditioned = 0;
let ledger: Ledger = run.ledger;
if (existsSync(resolve(dir, 'diagnostics.json'))) {
  const diagnostic = JSON.parse(readFileSync(resolve(dir, 'diagnostics.json'), 'utf8')) as {
    status: string; ledger: Ledger; scriptHash: string; promptHash: string;
    cases: { fault: Fault; trace: TraceStep[]; status: string; finalExact: boolean; finalF1: number;
      faultTriggered: boolean; recoveryEligible: boolean; recoverySuccess: boolean | null }[];
  };
  assert.equal(diagnostic.status, 'complete');
  assert.equal(diagnostic.scriptHash, hash(readFileSync(resolve(ROOT, 'diagnostics.ts'))));
  assert.equal(diagnostic.promptHash, hash(BUILDER_PROMPT));
  for (const item of diagnostic.cases) {
    const env = new Environment(makeTask(41, 0, item.fault));
    env.step({ type: 'blueprint', blueprint: { version: 1, parts: env.task.target } });
    trace(env, item.trace);
    const score = env.score();
    assert.equal(item.finalExact, score.construction.exact);
    assert.equal(item.finalF1, score.construction.partF1);
    assert.equal(item.recoverySuccess, score.recoverySuccess);
    assert.equal(item.faultTriggered, score.faultTriggered);
    assert.equal(item.recoveryEligible, score.faultEligible);
    conditioned++;
  }
  ledger = diagnostic.ledger;
}
assert.ok(ledger.charges.every(c => c.status === 'settled'));
const billed = ledger.charges.reduce((s, c) => s + (c.actual ?? 0), 0);
assert.ok(Math.abs(cost - billed) < 1e-8, 'Receipts and ledger disagree');
assert.ok(billed < 5 && billed <= ledger.cap);
for (const [file, expected] of Object.entries(run.sourceFiles)) {
  assert.equal(hash(readFileSync(resolve(ROOT, file))), expected, `Run source changed: ${file}`);
}
const result = { measuredAt: new Date().toISOString(), runId: run.id, mainEpisodes: run.episodes.length,
  conditionedEpisodes: conditioned, decisions, imageHashesVerified: checkedImages.size,
  uniqueGenerationReceipts: ids.size, billedUsd: billed, allScoresReproduced: true, sourceHashesMatch: true };
atomicJson(resolve(dir, 'replay-verification.json'), result);
console.log(JSON.stringify(result, null, 2));
