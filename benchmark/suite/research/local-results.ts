import { copyFileSync, existsSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS, BENCHMARK, SYSTEM, sourceHashes, type SuiteRun, type ResultRow } from '../storage';
import { models, summary, digest } from '../data';
import { parseJSON, score } from '../score';
import { taskFor } from '../tasks';
import type { PublicTask } from '../shared';

export interface LocalRun extends SuiteRun { localTraining: true; training: Record<string, unknown> }
export function importLocalResults() {
  const root = resolve(BENCHMARK, '.runtime/local-training');
  if (!existsSync(root)) return [];
  const inputs = readFileSync(resolve(BENCHMARK, '.runtime/suite-exports/inputs.jsonl'), 'utf8')
    .trim().split('\n').map(line => JSON.parse(line) as { taskId: string; input: PublicTask });
  const report = [];
  for (const name of readdirSync(root)) {
    const path = resolve(root, name, 'result.json');
    if (!existsSync(path)) continue;
    const training = JSON.parse(readFileSync(path, 'utf8'));
    if (training.status !== 'complete') continue;
    const predictions = JSON.parse(readFileSync(resolve(root, name, 'predictions.json'), 'utf8')) as {
      taskId: string; raw: string; new_tokens: number; seconds: number;
    }[];
    const runId = `local-qwen3-${name}`;
    const modelName = `local/qwen3-0.6b-${name}`;
    const results: ResultRow[] = predictions.map((p, index) => {
      const input = inputs.find(i => i.taskId === p.taskId)!;
      let match: { m: ReturnType<typeof models>[number]; t: ReturnType<typeof taskFor> } | undefined;
      for (const m of models()) {
        const t = taskFor(m, input.input.kind);
        if (t.public.id === p.taskId) { match = { m, t }; break; }
      }
      if (!match) throw new Error('Local prediction task not in frozen input set');
      const { m, t } = match, answer = parseJSON(p.raw);
      return { taskId: p.taskId, modelId: m.id, group: m.group, family: m.family, split: m.split, kind: t.public.kind,
        model: modelName, mode: 'one-shot', representation: 'absolute', input: t.public, frames: [],
        answers: [answer], calls: [{ id: `local-${digest({ runId, index, raw: p.raw }).slice(0, 24)}`,
          provider: 'local PyTorch/MPS (not OpenRouter)', content: p.raw,
          cost: 0, promptTokens: 0, completionTokens: p.new_tokens, reasoningTokens: 0,
          latencyMs: Math.round(p.seconds * 1000), finishReason: p.new_tokens >= training.config.max_new_tokens ? 'length' : 'stop' }],
        verdict: score(t, answer), status: 'complete' };
    });
    const run: LocalRun = {
      localTraining: true, version: 'local-text-training-v1', id: runId, status: 'complete',
      startedAt: new Date(training.started_at * 1000).toISOString(), completedAt: new Date(training.completed_at * 1000).toISOString(),
      datasetHash: summary().digest, protocolHash: digest(SYSTEM), sourceFiles: sourceHashes(),
      selection: results.map(r => ({ modelId: r.modelId, kind: r.kind, split: r.split, taskId: r.taskId })),
      selectionHash: digest(predictions.map(p => p.taskId)), models: [modelName], mode: 'one-shot', representation: 'absolute',
      pricing: { apiUsd: 0, localComputeIsFree: false, promptTokensRecorded: false },
      results, campaignBefore: 0, campaignAfter: 0,
      training: { ...training, predictionsFileHash: digest(predictions),
        note: 'Real local weights/inference. Prompt token count was not recorded and normalized to 0; it must not be interpreted as measured zero. No API receipt exists. Local compute time is recorded separately.' },
    };
    const dir = resolve(ARTIFACTS, 'runs', runId);
    atomicJson(resolve(dir, 'run.json'), run);
    atomicJson(resolve(dir, 'local-predictions.json'), predictions);
    atomicJson(resolve(dir, 'training-manifest.json'), training);
    const historyFile = resolve(root, name, 'training-steps.json');
    if (existsSync(historyFile)) copyFileSync(historyFile, resolve(dir, 'training-steps.json'));
    if (training.adapter_sha256) {
      const weights = resolve(root, name, 'adapter/adapter_model.safetensors');
      if (createHash('sha256').update(readFileSync(weights)).digest('hex') !== training.adapter_sha256) throw new Error('Training weights changed');
      const config = JSON.parse(readFileSync(resolve(root, name, 'adapter/adapter_config.json'), 'utf8'));
      config.base_model_name_or_path = training.base_model;
      config.revision = training.revision;
      atomicJson(resolve(dir, 'adapter/adapter_config.json'), config);
      copyFileSync(weights, resolve(dir, 'adapter/adapter_model.safetensors'));
    }
    const row = { model: modelName, condition: training.condition, seed: training.seed,
      steps: training.optimization_steps ?? 0, processedTokens: training.processed_tokens ?? 0,
      cases: results.length, successes: results.reduce((n, r) => n + r.verdict.metrics.success, 0),
      validationBefore: training.validation_loss_before, validationAfter: training.validation_loss_after,
      adapterSha256: training.adapter_sha256 ?? null, apiUsd: 0,
      inferenceSeconds: predictions.reduce((n, p) => n + p.seconds, 0),
      byTask: Object.fromEntries([...new Set(results.map(r => r.kind))].map(kind => {
        const subset = results.filter(r => r.kind === kind);
        return [kind, { n: subset.length, success: subset.reduce((n, r) => n + r.verdict.metrics.success, 0) }];
      })) };
    report.push(row);
    atomicJson(resolve(dir, 'training-summary.json'), row);
    writeFileSync(resolve(dir, 'REPORT.md'), `# Local Qwen3 training baseline

Model: ${modelName}. Condition: ${training.condition}, seed ${training.seed}.
Base revision: ${training.revision}. Dataset and script hashes are in run.json.
This is a **text/structure-only, short LoRA pilot**, not a trained multimodal model.
Optimization steps: ${training.optimization_steps ?? 0}; processed training tokens: ${training.processed_tokens ?? 0}.
Adapter SHA256: ${training.adapter_sha256 ?? 'base model, no adapter'}.
Adapter weights and a portable base-model reference are bundled in this run's adapter/ directory.
API cost: $0. Local compute is NOT free; inference took ${row.inferenceSeconds.toFixed(2)} seconds.
Prompt-token count was not recorded; stored normalized zeros must not be interpreted as measurements.
Results: ${row.successes}/${row.cases}. Raw outputs and all eight applicable/absent task rows are visible in the app.

| Task | n | Success |
| --- | ---: | ---: |
${Object.entries(row.byTask).map(([kind, v]) => `| ${kind} | ${v.n} | ${v.success} |`).join('\n')}

Validation loss before: ${JSON.stringify(row.validationBefore)}

Validation loss after: ${JSON.stringify(row.validationAfter)}

Training only uses the frozen train split; validation groups are disjoint. Loss reduction does not imply general task success.
Single/multi conditions match optimizer steps but not tokens or data diversity, so this is not a causal transfer result.
`);
  }
  atomicJson(resolve(ARTIFACTS, 'research/local-training-summary.json'), {
    rows: report, multimodalTraining: false, experiment: 'Step-matched short LoRA pilot; data/token counts differ. Not a compute-matched causal transfer claim.',
  });
  return report;
}
export function replayLocal(run: LocalRun) {
  const dir = resolve(ARTIFACTS, 'runs', run.id);
  const predictions = JSON.parse(readFileSync(resolve(dir, 'local-predictions.json'), 'utf8'));
  if (!isDeepStrictEqual(run.sourceFiles, sourceHashes()) || run.datasetHash !== summary().digest
    || run.protocolHash !== digest(SYSTEM)) throw new Error('Local scoring source changed');
  const script = readFileSync(resolve(BENCHMARK, 'suite/research/train_local.py'));
  if (createHash('sha256').update(script).digest('hex') !== run.training.script_sha256) throw new Error('Training script changed');
  if (digest(predictions) !== run.training.predictionsFileHash) throw new Error('Local predictions changed');
  if (predictions.length !== run.results.length) throw new Error('Missing local output');
  if (run.training.adapter_sha256
    && createHash('sha256').update(readFileSync(resolve(dir, 'adapter/adapter_model.safetensors'))).digest('hex') !== run.training.adapter_sha256) throw new Error('Adapter changed');
  for (const [index, row] of run.results.entries()) {
    const t = taskFor(models().find(m => m.id === row.modelId)!, row.kind);
    if (!isDeepStrictEqual(t.public, row.input) || row.calls.length !== 1
      || predictions[index].taskId !== row.taskId || predictions[index].raw !== row.calls[0].content
      || !isDeepStrictEqual(row.answers[0], parseJSON(row.calls[0].content))) throw new Error('Local input/output drift');
    if (JSON.stringify(score(t, parseJSON(row.calls[0].content))) !== JSON.stringify(row.verdict)) throw new Error('Local score mismatch');
  }
  return { run: run.id, cases: run.results.length, calls: run.results.length, cost: 0, scoresReproduced: true, local: true };
}
