import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, readdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { LOCAL_JOBS, localMatrixComplete, validateLocalJob } from '../suite/study/local-contract';
import { publishLocal } from '../suite/study/publish-local';

function fixture(condition = 'single') {
  const manifest = { condition, seed: 17, status: 'complete',
    config: { condition, seed: 17, probe: false, steps: 120, tokens_per_step: 512 },
    started_at: 1, completed_at: 2, predictions: 1, steps: condition === 'base' ? 0 : 120,
    supervised_tokens: condition === 'base' ? 0 : 61440, trainable_parameters: 0,
    ...(condition === 'base' ? {} : { adapter_sha256: 'a'.repeat(64), merged_model_sha256: 'b'.repeat(64) }) };
  const predictions = [{ caseId: 'case', raw: '', input_tokens: 100, output_tokens: 0, images: 1,
    seconds: 1, input_token_sha256: 'c'.repeat(64), backend: 'mlx-vlm-0.7.0-unquantized' }];
  const steps = Array.from({ length: manifest.steps }, (_, index) => ({ step: index + 1, loss: 0.5,
    supervised_tokens: 512, samples: [{ supervised_tokens: 512, input_tokens: 1000, images: 4 }] }));
  return { manifest, predictions, steps };
}

test('matrix completion requires exact predeclared job identities, not directory count', () => {
  assert.equal(localMatrixComplete(LOCAL_JOBS), true);
  assert.equal(localMatrixComplete(LOCAL_JOBS.slice(0, -1)), false);
  assert.throws(() => localMatrixComplete([...LOCAL_JOBS.slice(0, -1), LOCAL_JOBS[0]]));
  assert.throws(() => localMatrixComplete([...LOCAL_JOBS.slice(0, -1), 'multi-seed999']));
});

test('completed local jobs validate identity, full predictions and loss-bearing token accounting', () => {
  for (const condition of ['base', 'single', 'multi', 'leave-edit']) {
    const { manifest, predictions, steps } = fixture(condition);
    assert.doesNotThrow(() => validateLocalJob(`${condition}-seed17`, manifest, predictions, steps, ['case']));
  }
  const mutations: ((f: ReturnType<typeof fixture>) => void)[] = [
    f => { f.manifest.status = 'running'; },
    f => { f.manifest.seed = 29; },
    f => { f.manifest.config.probe = true; },
    f => { f.manifest.steps = 119; },
    f => { f.manifest.supervised_tokens--; },
    f => { f.manifest.completed_at = 0; },
    f => { f.predictions.length = 0; },
    f => { f.predictions[0].caseId = 'other'; },
    f => { f.predictions[0].output_tokens = 2201; },
    f => { f.predictions[0].seconds = -1; },
    f => { f.steps[0].samples[0].supervised_tokens = 511; },
    f => { f.steps[0].step = 2; },
    f => { f.steps[0].loss = NaN; },
  ];
  for (const mutate of mutations) {
    const f = fixture(); mutate(f);
    assert.throws(() => validateLocalJob('single-seed17', f.manifest, f.predictions, f.steps, ['case']));
  }
});

test('publication is idempotent and refuses changes to any existing evidence', () => {
  const root = mkdtempSync(resolve(tmpdir(), 'brick-local-')), dir = resolve(root, 'local/single-seed17');
  const files = { 'manifest.json': { status: 'complete' }, 'steps.json': [1],
    'adapter/adapter_model.safetensors': Buffer.from('weights') };
  try {
    publishLocal(dir, files); publishLocal(dir, files);
    for (const change of [
      { 'steps.json': [2] }, { 'manifest.json': { status: 'running' } },
      { 'adapter/adapter_model.safetensors': Buffer.from('changed') },
    ]) assert.throws(() => publishLocal(dir, { ...files, ...change }));
    assert.deepEqual(JSON.parse(readFileSync(resolve(dir, 'steps.json'), 'utf8')), [1]);
    assert.deepEqual(readdirSync(root), ['local']);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test('failed staged publication exposes no partial job and removes its own temporary files', () => {
  const root = mkdtempSync(resolve(tmpdir(), 'brick-local-'));
  const circular: any = {}; circular.self = circular;
  try {
    assert.throws(() => publishLocal(resolve(root, 'local/multi-seed17'),
      { 'manifest.json': {}, 'predictions.json': circular }));
    assert.deepEqual(readdirSync(resolve(root, 'local')), []);
    assert.deepEqual(readdirSync(root), ['local']);
  } finally { rmSync(root, { recursive: true, force: true }); }
});
