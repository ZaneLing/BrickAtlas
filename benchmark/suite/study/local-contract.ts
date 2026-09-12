import assert from 'node:assert/strict';

export const LOCAL_JOBS = ['base-seed17', ...['single', 'multi', 'leave-edit']
  .flatMap(condition => [17, 29, 43].map(seed => `${condition}-seed${seed}`))];

export function localMatrixComplete(names: string[]) {
  assert.equal(new Set(names).size, names.length, 'Duplicate local job');
  assert.ok(names.every(name => LOCAL_JOBS.includes(name)), 'Unexpected local job');
  return LOCAL_JOBS.every(name => names.includes(name));
}

export function validateLocalJob(name: string, manifest: any, predictions: any[], steps: any[], caseIds: string[]) {
  assert.ok(LOCAL_JOBS.includes(name), `Unexpected local job: ${name}`);
  assert.equal(`${manifest.condition}-seed${manifest.seed}`, name, 'Job identity mismatch');
  assert.equal(manifest.status, 'complete', 'Incomplete local job');
  assert.equal(manifest.config.condition, manifest.condition);
  assert.equal(manifest.config.seed, manifest.seed);
  assert.equal(manifest.config.probe, false);
  assert.equal(manifest.config.steps, 120);
  assert.equal(manifest.config.tokens_per_step, 512);
  assert.ok(Number.isFinite(manifest.started_at) && Number.isFinite(manifest.completed_at)
    && manifest.completed_at >= manifest.started_at, 'Invalid run timestamps');
  assert.deepEqual(predictions.map(p => p.caseId), caseIds, 'Incomplete or reordered test predictions');
  assert.equal(manifest.predictions, caseIds.length);
  for (const p of predictions) {
    assert.equal(typeof p.raw, 'string');
    assert.ok(Number.isInteger(p.input_tokens) && p.input_tokens > 0);
    assert.ok(Number.isInteger(p.output_tokens) && p.output_tokens >= 0 && p.output_tokens <= 2200);
    assert.ok(Number.isInteger(p.images) && p.images >= 0);
    assert.ok(Number.isFinite(p.seconds) && p.seconds >= 0);
    assert.match(p.input_token_sha256, /^[a-f0-9]{64}$/);
    assert.equal(p.backend, 'mlx-vlm-0.7.0-unquantized');
  }
  const targetSteps = manifest.condition === 'base' ? 0 : 120;
  assert.equal(steps.length, targetSteps, 'Incomplete training steps');
  assert.equal(manifest.steps, targetSteps);
  assert.equal(manifest.supervised_tokens, targetSteps * 512);
  if (targetSteps) {
    assert.match(manifest.adapter_sha256, /^[a-f0-9]{64}$/, 'Missing adapter hash');
    assert.match(manifest.merged_model_sha256, /^[a-f0-9]{64}$/, 'Missing merged checkpoint hash');
  } else {
    assert.equal(manifest.adapter_sha256, undefined);
    assert.equal(manifest.trainable_parameters, 0);
  }
  for (const [index, step] of steps.entries()) {
    assert.equal(step.step, index + 1);
    assert.ok(Number.isFinite(step.loss));
    assert.equal(step.supervised_tokens, 512);
    assert.ok(Array.isArray(step.samples) && step.samples.length > 0);
    assert.equal(step.samples.reduce((n: number, s: any) => n + s.supervised_tokens, 0), 512);
    for (const sample of step.samples) {
      assert.ok(Number.isInteger(sample.supervised_tokens) && sample.supervised_tokens > 0);
      assert.ok(Number.isInteger(sample.input_tokens) && sample.input_tokens >= sample.supervised_tokens);
      assert.ok(Number.isInteger(sample.images) && sample.images >= 0);
    }
  }
}
