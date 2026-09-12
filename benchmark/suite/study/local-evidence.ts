import assert from 'node:assert/strict';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { gunzipSync } from 'node:zlib';
import { atomicJson } from '../../core/budget';
import { BENCHMARK, SYSTEM } from '../storage';
import { digest } from '../data';
import { parseJSON } from '../score';
import { getSpec, taskForV2 } from '../v2/cases';
import { strictTrace } from './strict-trace';
import { evaluateStrict, EVALUATOR_VERSION } from './strict-evaluate';
import { STUDY, selection, type Prepared } from './protocol';
import { summarize, type StudyRow } from './results';
import { LOCAL_JOBS, validateLocalJob } from './local-contract';

export function localEvidenceRuns() {
  const root = resolve(STUDY, 'local');
  if (!existsSync(root)) return [];
  const prepared = JSON.parse(readFileSync(resolve(STUDY, 'inputs/prepared.json'), 'utf8')) as Prepared[];
  const inputs = new Map(prepared.map(p => [p.spec.id, p]));
  const names = readdirSync(root);
  assert.ok(names.every(name => LOCAL_JOBS.includes(name)), 'Unexpected published local job');
  return LOCAL_JOBS.filter(name => names.includes(name)).map(name => {
    const dir = resolve(root, name), manifest = JSON.parse(readFileSync(resolve(dir, 'manifest.json'), 'utf8'));
    const predictions = JSON.parse(readFileSync(resolve(dir, 'predictions.json'), 'utf8'));
    const steps = JSON.parse(readFileSync(resolve(dir, 'steps.json'), 'utf8'));
    validateLocalJob(name, manifest, predictions, steps, selection().map(s => s.id));
    const rows: StudyRow[] = predictions.map((p: any) => ({
      caseId: p.caseId, model: `local/smolvlm-${name}`, input: inputs.get(p.caseId)!.input, images: inputs.get(p.caseId)!.images,
      answer: p.answer, verdict: p.verdict, call: { id: `local-record-${name}-${p.caseId}`,
        provider: 'Local MLX inference; ID is a record key, not an API generation receipt.',
        content: p.raw, cost: 0, promptTokens: p.input_tokens, completionTokens: p.output_tokens,
        reasoningTokens: 0, latencyMs: Math.round(p.seconds * 1000),
        finishReason: p.output_tokens >= 2200 ? 'length' : 'stop' },
    }));
    return { id: `local-${name}`, status: 'complete', manifest, rows, dir,
      completed: rows.length, expected: prepared.length, cost: 0, localComputeNotFree: true };
  });
}
function inferenceTrace(runId: string, index: number, row: StudyRow) {
  const trace = strictTrace(runId, row.model, { spec: getSpec(row.caseId), answer: row.answer, missing: false },
    row.images.map(file => `/api/study/images/${file.slice(7)}`));
  trace.mode = 'local-inference';
  trace.caseIndex = index;
  const e = trace.events.find(e => e.kind === 'response')!;
  e.title = '本地模型原始输出'; e.payload = row.call;
  trace.evidence.responseCount = 1;
  trace.evidence.note += ' Recorded local MLX model response. No API bill; actual input/output tokens and inference seconds retained. Local compute is not free.';
  trace.modelInput = { system: SYSTEM, user: JSON.stringify(row.input) };
  return trace;
}
export function localInferenceTrace(runId: string, index: number) {
  const run = localEvidenceRuns().find(r => r.id === runId), row = run?.rows[index];
  if (!run || !row) throw new Error('Unknown local inference');
  return inferenceTrace(runId, index, row);
}
export function replayLocalEvidence() {
  const summaries = [];
  const runs = localEvidenceRuns();
  const base = runs.find(r => r.manifest.condition === 'base');
  const basePredictions = base ? JSON.parse(readFileSync(resolve(base.dir, 'predictions.json'), 'utf8')) : [];
  const baseInputs = new Map<string, any>(basePredictions.map((p: any) => [p.caseId, p]));
  for (const run of runs) {
    assert.equal(run.rows.length, run.expected);
    assert.deepEqual(run.rows.map(r => r.caseId), selection().map(s => s.id));
    const m = run.manifest;
    assert.equal(m.evaluatorVersion, EVALUATOR_VERSION);
    for (const [filename, key] of [['train.jsonl', 'train_file_sha256'], ['validation.jsonl', 'validation_file_sha256']]) {
      assert.equal(createHash('sha256').update(gunzipSync(readFileSync(resolve(STUDY, 'training-data', filename + '.gz')))).digest('hex'), m[key]);
    }
    assert.equal(createHash('sha256').update(readFileSync(resolve(STUDY, 'inputs/public.jsonl'))).digest('hex'), m.test_input_sha256);
    assert.equal(createHash('sha256').update(readFileSync(resolve(BENCHMARK, 'suite/study/train_vlm.py'))).digest('hex'), m.script_sha256);
    assert.equal(createHash('sha256').update(readFileSync(resolve(BENCHMARK, 'suite/study/infer_mlx.py'))).digest('hex'), m.inference_script_sha256);
    const predictions = JSON.parse(readFileSync(resolve(run.dir, 'predictions.json'), 'utf8'));
    for (const [index, p] of predictions.entries()) {
      const reference = baseInputs.get(p.caseId);
      assert.ok(reference, 'Base input evidence required');
      assert.equal(p.input_token_sha256, reference.input_token_sha256);
      assert.equal(p.input_tokens, reference.input_tokens);
      assert.equal(p.images, run.rows[index].images.length);
      assert.ok(Number.isInteger(p.input_tokens) && p.input_tokens > 0);
      assert.ok(Number.isInteger(p.output_tokens) && p.output_tokens >= 0 && p.output_tokens <= 2200);
      assert.ok(Number.isFinite(p.seconds) && p.seconds >= 0);
      assert.equal(p.backend, 'mlx-vlm-0.7.0-unquantized');
    }
    for (const [index, row] of run.rows.entries()) {
      assert.deepEqual(row.answer, parseJSON(row.call.content));
      assert.deepEqual(row.input, taskForV2(getSpec(row.caseId)).public);
      assert.deepEqual(row.verdict, evaluateStrict(taskForV2(getSpec(row.caseId)), row.answer));
      for (const path of row.images) {
        const hash = digest(readFileSync(resolve(STUDY, 'inputs', path)).toString('base64'));
        assert.equal(path, `images/${hash}.png`);
      }
      const trace = inferenceTrace(run.id, index, row);
      assert.deepEqual(trace.verdict, row.verdict);
      for (const [i, event] of trace.events.entries()) {
        assert.equal(digest(trace.states[event.before]), event.before);
        assert.equal(digest(trace.states[event.after]), event.after);
        if (i) assert.equal(event.before, trace.events[i - 1].after);
      }
    }
    if (m.adapter_sha256) assert.equal(createHash('sha256').update(readFileSync(resolve(run.dir, 'adapter/adapter_model.safetensors'))).digest('hex'), m.adapter_sha256);
    const steps = JSON.parse(readFileSync(resolve(run.dir, 'steps.json'), 'utf8'));
    assert.equal(steps.length, m.steps);
    assert.equal(steps.reduce((n: number, s: any) => n + s.supervised_tokens, 0), m.supervised_tokens);
    if (m.condition !== 'base') {
      assert.equal(steps.length, 120); assert.equal(m.supervised_tokens, 61440);
      for (const [i, step] of steps.entries()) {
        assert.equal(step.step, i + 1); assert.ok(Number.isFinite(step.loss));
        assert.equal(step.supervised_tokens, 512);
        assert.equal(step.samples.reduce((n: number, s: any) => n + s.supervised_tokens, 0), 512);
        for (const sample of step.samples) {
          const spec = getSpec(sample.caseId);
          assert.equal(spec.split, 'train'); assert.equal(spec.kind, sample.kind);
          if (m.condition === 'single') assert.equal(spec.kind, 'reconstruct');
          if (m.condition === 'leave-edit') assert.notEqual(spec.kind, 'edit');
        }
      }
    }
    const summary = { id: run.id, cases: run.rows.length, scoresReproduced: true, steps: steps.length,
      supervisedTokens: m.supervised_tokens, rows: summarize(run) };
    atomicJson(resolve(run.dir, 'summary.json'), summary); summaries.push(summary);
  }
  atomicJson(resolve(STUDY, 'local-replay.json'), summaries); return summaries.map(s => ({ id: s.id, cases: s.cases }));
}
