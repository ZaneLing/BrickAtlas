import assert from 'node:assert/strict';
import { closeSync, existsSync, openSync, readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Budget, atomicJson } from '../../core/budget';
import type { Message } from '../../core/openrouter';
import { BENCHMARK } from '../storage';
import { digest } from '../data';
import { getSpec, taskForV2 } from '../v2/cases';
import { STUDY } from './protocol';
import { validationCases, validationMessages, replayModelValidation, VALIDATION_DIR } from './model-validation';
import { diagnoseResponse } from './failure-diagnostics';
import { validationAggregate } from './model-validation-report';

export const PAPER_MODELS = [
  { id: 'anthropic/claude-haiku-4.5', label: 'Claude Haiku 4.5', prompt: 1.05, completion: 5.1 },
  { id: 'google/gemini-3-flash-preview', label: 'Gemini 3 Flash (preview)', prompt: 0.55, completion: 3.1 },
  { id: 'qwen/qwen3-vl-8b-instruct', label: 'Qwen3-VL-8B', prompt: 0.2, completion: 0.6 },
  { id: 'meta-llama/llama-4-maverick', label: 'Llama 4 Maverick', prompt: 0.3, completion: 0.9 },
] as const;
export const PAPER_MODELS_DIR = resolve(STUDY, 'paper-models');
const read = (name: string) => JSON.parse(readFileSync(resolve(PAPER_MODELS_DIR, name), 'utf8'));
const ownHash = () => digest(readFileSync(fileURLToPath(import.meta.url), 'utf8'));

export function paperModelCeiling(model: { prompt: number; completion: number }, messages: Message[]) {
  let bytes = 2048, images = 0;
  for (const m of messages) {
    if (typeof m.content === 'string') bytes += Buffer.byteLength(m.content);
    else for (const c of m.content) if (c.type === 'text') bytes += Buffer.byteLength(c.text); else images++;
  }
  assert.ok(bytes <= 50000 && images <= 4);
  return ((bytes + images * 16384) * model.prompt + 2200 * model.completion) / 1e6 + images * .005;
}

export async function freezePaperModels() {
  const selected = validationCases();
  const rows = selected.rows.filter(r => r.arm === 'ordinary');
  assert.equal(rows.length, 39);
  const response = await fetch('https://openrouter.ai/api/v1/models', { signal: AbortSignal.timeout(20000) });
  assert.ok(response.ok, 'Model catalog unavailable');
  const catalog = (await response.json()).data;
  const pricing = PAPER_MODELS.map(model => {
    const m = catalog.find((r: any) => r.id === model.id);
    assert.ok(m?.architecture.input_modalities.includes('image') && m.supported_parameters.includes('response_format'));
    assert.ok(Number(m.pricing.prompt) * 1e6 <= model.prompt && Number(m.pricing.completion) * 1e6 <= model.completion);
    return { id: model.id, pricing: m.pricing, supportedParameters: m.supported_parameters };
  });
  const protocol = { version: 'paper-model-matrix-1', models: PAPER_MODELS, chosen: selected.chosen, rows,
    maxTokens: 2200, temperature: 0, attempts: 1, pricing, runnerHash: ownHash(),
    historicalRunHash: digest(readFileSync(resolve(VALIDATION_DIR, 'run.json'), 'utf8')),
    plannedRequests: rows.length * PAPER_MODELS.length, newSpendCap: 0.75,
    scope: 'Three shared already-exposed development source objects; not confirmation. Four historical models retain original calls; four new models use the identical 39 ordinary/default tasks. No pooled ranking.',
    decoding: 'JSON object; reasoning disabled for Gemini, no reasoning requested otherwise. Provider must support parameters, deny data collection, no fallback or automatic retry.',
    inputHashes: Object.fromEntries(rows.map(row => [row.id, digest(validationMessages(row))])) };
  assert.ok(!existsSync(resolve(PAPER_MODELS_DIR, 'protocol.json')), 'Do not overwrite frozen protocol');
  atomicJson(resolve(PAPER_MODELS_DIR, 'protocol.json'), protocol);
  return { models: PAPER_MODELS.map(m => m.id), requests: protocol.plannedRequests, sources: 3, cap: protocol.newSpendCap };
}

export async function runPaperModels() {
  const protocol = read('protocol.json');
  assert.equal(protocol.runnerHash, ownHash());
  const selected = validationCases().rows.filter(r => r.arm === 'ordinary');
  assert.deepEqual(protocol.rows, selected);
  assert.deepEqual(protocol.models, PAPER_MODELS);
  if (!process.env.OPENROUTER_API_KEY) process.loadEnvFile(resolve(BENCHMARK, '../.env'));
  const key = process.env.OPENROUTER_API_KEY;
  assert.ok(key, 'OpenRouter authorization required');
  const lock = resolve(BENCHMARK, '.runtime/pilot.lock'), fd = openSync(lock, 'wx', 0o600);
  writeFileSync(fd, `${process.pid}\n`); closeSync(fd);
  try {
    const budget = new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json'));
    assert.ok(!budget.blocked, 'Reconcile earlier charge first');
    const run = existsSync(resolve(PAPER_MODELS_DIR, 'run.json')) ? read('run.json') : {
      version: protocol.version, protocolHash: digest(protocol), status: 'running',
      startedAt: new Date().toISOString(), campaignBefore: budget.spent, campaignAfter: budget.spent,
      rows: [] as any[], error: null as string | null,
    };
    assert.equal(run.protocolHash, digest(protocol));
    if (run.status === 'complete') return { status: 'already-complete', rows: run.rows.length };
    assert.equal(run.status, 'running', 'Stopped runs require explicit review; no automatic retries');
    const save = () => {
      run.campaignAfter = budget.spent;
      atomicJson(resolve(PAPER_MODELS_DIR, 'run.json'), run);
      atomicJson(resolve(PAPER_MODELS_DIR, 'ledger.json'), budget.ledger);
    };
    save();
    try {
      for (const [i, row] of selected.entries()) {
        for (let j = 0; j < PAPER_MODELS.length; j++) {
          const model = PAPER_MODELS[(i + j) % PAPER_MODELS.length];
          if (run.rows.some((r: any) => r.id === row.id && r.model === model.id)) continue;
          const messages = validationMessages(row), inputHash = digest(messages);
          assert.equal(inputHash, protocol.inputHashes[row.id]);
          const ceiling = paperModelCeiling(model, messages);
          assert.ok(budget.spent - run.campaignBefore + ceiling <= protocol.newSpendCap, 'Paper allocation exhausted');
          const charge = budget.reserve(model.id, ceiling), began = performance.now();
          try {
            const response: Response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
              method: 'POST', signal: AbortSignal.timeout(120000),
              headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json', 'X-OpenRouter-Title': 'BrickAtlas paper pilot' },
              body: JSON.stringify({ model: model.id, messages, max_tokens: 2200, temperature: 0,
                response_format: { type: 'json_object' }, stream: false,
                ...(model.id.startsWith('google/') ? { reasoning: { enabled: false } } : {}),
                provider: { sort: 'price', allow_fallbacks: false, require_parameters: true, data_collection: 'deny',
                  max_price: { prompt: model.prompt, completion: model.completion, image: .005 } } }),
            });
            assert.ok(response.ok, `OpenRouter HTTP ${response.status}; no retry`);
            const data: any = await response.json();
            assert.ok(data.id && Number.isFinite(data.usage?.cost), 'Missing billing receipt');
            budget.settle(charge, data.usage.cost, data.id);
            const choice = data.choices?.[0];
            assert.equal(typeof choice?.message?.content, 'string', 'Missing model answer');
            const call = { id: data.id, model: data.model, provider: data.provider ?? 'unknown',
              content: choice.message.content, cost: data.usage.cost, promptTokens: data.usage.prompt_tokens,
              completionTokens: data.usage.completion_tokens, reasoningTokens: data.usage.completion_tokens_details?.reasoning_tokens ?? 0,
              finishReason: choice.finish_reason ?? 'unknown', latencyMs: Math.round(performance.now() - began) };
            run.rows.push({ id: row.id, caseId: row.caseId, model: model.id, inputHash, arm: row.arm, call,
              diagnosis: diagnoseResponse(taskForV2(getSpec(row.caseId)), call.content, call.finishReason) });
          } catch (error) { budget.uncertain(charge); throw error; }
          save();
          console.log(JSON.stringify({ responses: run.rows.length, planned: protocol.plannedRequests,
            model: model.id, newCost: budget.spent - run.campaignBefore }));
        }
      }
      run.status = 'complete'; run.completedAt = new Date().toISOString();
    } catch (error) { run.status = 'stopped'; run.error = (error as Error).message; }
    save();
    return { status: run.status, responses: run.rows.length, error: run.error, newCost: run.campaignAfter - run.campaignBefore };
  } finally { unlinkSync(lock); }
}

export function replayPaperModels() {
  replayModelValidation();
  const protocol = read('protocol.json'), run = read('run.json'), ledger = read('ledger.json');
  assert.equal(protocol.runnerHash, ownHash());
  assert.equal(run.protocolHash, digest(protocol));
  assert.equal(protocol.historicalRunHash, digest(readFileSync(resolve(VALIDATION_DIR, 'run.json'), 'utf8')));
  const selected = validationCases().rows.filter(r => r.arm === 'ordinary');
  assert.deepEqual(protocol.rows, selected);
  const seen = new Set<string>(), receipts = new Set<string>();
  let cost = 0;
  for (const row of run.rows) {
    const input = selected.find(r => r.id === row.id);
    assert.ok(input && PAPER_MODELS.some(m => m.id === row.model));
    assert.equal(row.caseId, input.caseId); assert.equal(row.arm, input.arm);
    assert.ok(!seen.has(`${row.model}/${row.id}`)); seen.add(`${row.model}/${row.id}`);
    assert.ok(!receipts.has(row.call.id)); receipts.add(row.call.id);
    assert.equal(row.inputHash, digest(validationMessages(input)));
    assert.equal(row.inputHash, protocol.inputHashes[row.id]);
    const charge = ledger.charges.find((c: any) => c.generationId === row.call.id);
    assert.equal(charge?.status, 'settled'); assert.equal(charge.actual, row.call.cost);
    assert.deepEqual(row.diagnosis, diagnoseResponse(taskForV2(getSpec(row.caseId)), row.call.content, row.call.finishReason));
    cost += row.call.cost;
  }
  assert.ok(Math.abs(cost - (run.campaignAfter - run.campaignBefore)) < 1e-8);
  if (run.status === 'complete') assert.equal(seen.size, protocol.plannedRequests);
  const old = JSON.parse(readFileSync(resolve(VALIDATION_DIR, 'run.json'), 'utf8'));
  const rows = [...old.rows.filter((r: any) => r.arm === 'ordinary'), ...run.rows];
  const models = [...new Set<string>(rows.map((r: any) => r.model))];
  const families = ['relations', 'reconstruct', 'generate', 'complete', 'edit', 'plan', 'repair'];
  const summary = models.map(model => ({
    model, cohort: PAPER_MODELS.some(m => m.id === model) ? 'new' : 'historical',
    ...validationAggregate(rows.filter((r: any) => r.model === model), 39),
    families: Object.fromEntries(families.map(kind => {
      const n = selected.filter(s => getSpec(s.caseId).kind === kind).length;
      return [kind, validationAggregate(rows.filter((r: any) => r.model === model && getSpec(r.caseId).kind === kind), n)];
    })),
  }));
  const report = { status: run.status, sourceGroups: 3, newResponses: run.rows.length, historicalResponses: 156,
    newCost: cost, campaignAfter: run.campaignAfter, summary, rows,
    protocolHash: digest(protocol), runHash: digest(run), apiRequests: 0,
    scope: 'All models use the same 39 tasks from three already exposed objects. Historical versus new calls differ in time/provider; no confidence or stable-ranking claim.' };
  atomicJson(resolve(PAPER_MODELS_DIR, 'analysis.json'), report);
  return { status: run.status, models: summary.length, responses: rows.length, newCost: cost, campaignAfter: run.campaignAfter };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const command = process.argv[2];
  console.log(command === 'freeze' ? await freezePaperModels() : command === 'run' ? await runPaperModels()
    : command === 'replay' ? replayPaperModels() : { commands: ['freeze', 'run', 'replay'] });
}
