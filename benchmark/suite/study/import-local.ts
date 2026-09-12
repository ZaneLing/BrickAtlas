import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS, BENCHMARK } from '../storage';
import { getSpec, taskForV2 } from '../v2/cases';
import { evaluateStrict, EVALUATOR_VERSION } from './strict-evaluate';
import { parseJSON } from '../score';
import { STUDY, selection } from './protocol';
import { validateLocalJob } from './local-contract';
import { publishLocal } from './publish-local';

export function importVLM() {
  const root = resolve(BENCHMARK, '.runtime/vlm-training');
  if (!existsSync(root)) return [];
  const reports = [];
  for (const name of readdirSync(root).filter(n => /^(base|single|multi|leave-edit)-seed\d+$/.test(n))) {
    const file = resolve(root, name, 'result.json'); if (!existsSync(file)) continue;
    const manifest = JSON.parse(readFileSync(file, 'utf8'));
    if (manifest.status !== 'complete') continue;
    const predictions = JSON.parse(readFileSync(resolve(root, name, 'predictions.json'), 'utf8'));
    const steps = existsSync(resolve(root, name, 'steps.json')) ? JSON.parse(readFileSync(resolve(root, name, 'steps.json'), 'utf8')) : [];
    validateLocalJob(name, manifest, predictions, steps, selection().map(s => s.id));
    for (const step of steps) for (const sample of step.samples) {
      const spec = getSpec(sample.caseId);
      assert.equal(spec.split, 'train'); assert.equal(spec.kind, sample.kind);
      if (manifest.condition === 'single') assert.equal(spec.kind, 'reconstruct');
      if (manifest.condition === 'leave-edit') assert.notEqual(spec.kind, 'edit');
    }
    const dir = resolve(STUDY, 'local', name);
    const publishedManifest = { ...manifest, evaluatorVersion: EVALUATOR_VERSION };
    const rows = predictions.map((p: any) => ({ ...p, answer: parseJSON(p.raw), verdict: evaluateStrict(taskForV2(getSpec(p.caseId)), parseJSON(p.raw)) }));
    const files: Record<string, unknown> = { 'manifest.json': publishedManifest, 'predictions.json': rows, 'steps.json': steps };
    if (manifest.adapter_sha256) {
      const weights = readFileSync(resolve(root, name, 'adapter/adapter_model.safetensors'));
      if (createHash('sha256').update(weights).digest('hex') !== manifest.adapter_sha256) throw new Error('Weights changed');
      const config = JSON.parse(readFileSync(resolve(root, name, 'adapter/adapter_config.json'), 'utf8'));
      config.base_model_name_or_path = manifest.model; config.revision = manifest.revision;
      files['adapter/adapter_config.json'] = config;
      files['adapter/adapter_model.safetensors'] = weights;
    }
    publishLocal(dir, files);
    const byTask = Object.fromEntries([...new Set(rows.map((r: any) => getSpec(r.caseId).kind))].map(kind => {
      const selected = rows.filter((r: any) => getSpec(r.caseId).kind === kind);
      return [String(kind), { n: selected.length, successes: selected.reduce((n: number, r: any) => n + r.verdict.metrics.success, 0) }];
    }));
    reports.push({ name, condition: manifest.condition, seed: manifest.seed, steps: manifest.steps,
      supervisedTokens: manifest.supervised_tokens, predictions: rows.length, byTask,
      imagesActuallyUsed: rows.reduce((n: number, r: any) => n + r.images, 0),
      validationBefore: manifest.validation_before, validationAfter: manifest.validation_after });
  }
  atomicJson(resolve(ARTIFACTS, 'study/local-summary.json'), reports); return reports;
}
