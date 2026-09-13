import assert from 'node:assert/strict';
import { existsSync, readFileSync, openSync, closeSync, unlinkSync } from 'node:fs';
import { resolve } from 'node:path';
import { Budget, atomicJson } from '../../core/budget';
import type { Message } from '../../core/openrouter';
import { BENCHMARK, SYSTEM } from '../storage';
import { digest } from '../data';
import { imageEvidence } from './calibration-export';
import { VALIDATION_MODELS, validationPricing, validationCeiling, validationCompletion } from './validation-client';
import { VALIDATION_DIR } from './model-validation';
import { POSE_DIR, POSE_ARMS, poseQuestions, scorePose } from './pose-probes';
import { key } from '../geometry';

function protocolAndQuestions() {
  const protocol = JSON.parse(readFileSync(resolve(POSE_DIR, 'protocol.json'), 'utf8')), questions = poseQuestions();
  assert.equal(protocol.version, 'pose-probe-1');
  assert.deepEqual(protocol.models, VALIDATION_MODELS);
  assert.equal(protocol.plannedCalls, 96); assert.equal(protocol.newSpendCap, 0.6);
  assert.deepEqual(protocol.rows.map((r: any) => r.id), questions.map(q => q.id));
  for (const [i, row] of protocol.rows.entries()) {
    assert.equal(row.group, questions[i].group); assert.equal(row.arm, questions[i].arm);
    assert.deepEqual(row.input, questions[i].input);
    assert.equal(row.images.length, questions[i].frames.length);
  }
  return { protocol, questions };
}
function messages(row: any): Message[] {
  const content: Exclude<Message['content'], string> = [{ type: 'text', text: JSON.stringify(row.input) }];
  for (const path of row.images) {
    assert.match(path, /^images\/[a-f0-9]{64}\.png$/);
    const bytes = readFileSync(resolve(POSE_DIR, path)); assert.equal(imageEvidence(bytes).hash, path.slice(7, -4));
    content.push({ type: 'image_url', image_url: { url: `data:image/png;base64,${bytes.toString('base64')}` } });
  }
  return [{ role: 'system', content: SYSTEM }, { role: 'user', content }];
}
function sourceHashes() {
  return Object.fromEntries(['pose-probes.ts', 'pose-run.ts', 'validation-client.ts', '../web/viewer.ts'].map(file =>
    [file, digest(readFileSync(resolve(BENCHMARK, 'suite/study', file), 'utf8'))]));
}
export async function runPoseProbes() {
  const { protocol, questions } = protocolAndQuestions();
  const path = resolve(POSE_DIR, 'run.json');
  assert.ok(!existsSync(path), 'Run exists; never overwrite or silently repeat paid calls');
  if (!process.env.OPENROUTER_API_KEY) process.loadEnvFile(resolve(BENCHMARK, '../.env'));
  const apiKey = process.env.OPENROUTER_API_KEY; assert.ok(apiKey);
  const lock = resolve(BENCHMARK, '.runtime/pilot.lock'), fd = openSync(lock, 'wx', 0o600); closeSync(fd);
  try {
    const budget = new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json'));
    assert.equal(budget.blocked, false);
    const original = JSON.parse(readFileSync(resolve(VALIDATION_DIR, 'run.json'), 'utf8'));
    const run = { status: 'running', protocolHash: digest(protocol), sourceHashes: sourceHashes(),
      pricing: await validationPricing(), campaignBefore: budget.spent, campaignAfter: budget.spent,
      startedAt: new Date().toISOString(), error: null as string | null, rows: [] as any[] };
    const save = () => { run.campaignAfter = budget.spent; atomicJson(path, run); atomicJson(resolve(POSE_DIR, 'ledger.json'), budget.ledger); };
    save();
    try {
      for (const [i, row] of protocol.rows.entries()) for (let j = 0; j < VALIDATION_MODELS.length; j++) {
        const model = VALIDATION_MODELS[(i + j) % VALIDATION_MODELS.length], request = messages(row);
        const ceiling = validationCeiling(model.id, request);
        if (budget.spent - run.campaignBefore + ceiling > protocol.newSpendCap
          || budget.spent - original.campaignBefore + ceiling > 2) throw new Error('Validation allocation reached');
        const call = await validationCompletion(apiKey, model.id, request, budget);
        run.rows.push({ id: row.id, group: row.group, arm: row.arm, model: model.id, requestHash: digest(request),
          call, score: scorePose(questions[i], call.content) });
        save();
        console.log(JSON.stringify({ completed: run.rows.length, planned: 96, spent: budget.spent - run.campaignBefore }));
      }
      run.status = 'complete';
    } catch (error) { run.status = 'stopped'; run.error = (error as Error).message; }
    save(); return { status: run.status, responses: run.rows.length, error: run.error };
  } finally { unlinkSync(lock); }
}

export function replayPoseProbes() {
  const { protocol, questions } = protocolAndQuestions();
  const run = JSON.parse(readFileSync(resolve(POSE_DIR, 'run.json'), 'utf8'));
  assert.equal(run.protocolHash, digest(protocol)); assert.deepEqual(run.sourceHashes, sourceHashes());
  const ledger = JSON.parse(readFileSync(resolve(POSE_DIR, 'ledger.json'), 'utf8')), seen = new Set(), receipts = new Set();
  let cost = 0;
  for (const row of run.rows) {
    const index = questions.findIndex(q => q.id === row.id); assert.ok(index >= 0);
    const q = questions[index]; assert.equal(row.arm, q.arm); assert.equal(row.group, q.group);
    assert.ok(VALIDATION_MODELS.some(m => m.id === row.model));
    const k = `${row.id}:${row.model}`; assert.ok(!seen.has(k)); seen.add(k);
    assert.ok(!receipts.has(row.call.id)); receipts.add(row.call.id);
    assert.equal(row.requestHash, digest(messages(protocol.rows[index])));
    assert.deepEqual(row.score, scorePose(q, row.call.content));
    assert.ok(Number.isInteger(row.call.completionTokens) && row.call.completionTokens >= 0 && row.call.completionTokens <= 2200);
    assert.ok(Number.isInteger(row.call.promptTokens) && row.call.promptTokens > 0);
    const charge = ledger.charges.find((c: any) => c.generationId === row.call.id);
    assert.equal(charge?.status, 'settled'); assert.equal(charge.model, row.model); assert.equal(charge.actual, row.call.cost);
    cost += row.call.cost;
  }
  assert.ok(Math.abs(cost - run.campaignAfter + run.campaignBefore) < 1e-8);
  if (run.status === 'complete') assert.equal(seen.size, protocol.plannedCalls);
  const summary = POSE_ARMS.flatMap(arm => VALIDATION_MODELS.map(model => {
    const rows = run.rows.filter((r: any) => r.arm === arm && r.model === model.id);
    return { arm, model: model.id, n: rows.length, missing: 4 - rows.length,
      successes: rows.reduce((n: number, r: any) => n + r.score.success, 0),
      formatAccepted: rows.reduce((n: number, r: any) => n + r.score.format, 0),
      fields: Object.fromEntries(['x', 'y', 'z', 'orientation'].map(field => {
        const values = rows.map((r: any) => r.score[field]).filter((v: unknown) => typeof v === 'number');
        return [field, { correct: values.reduce((n: number, v: number) => n + v, 0), n: values.length }];
      })) };
  }));
  const pairs = VALIDATION_MODELS.flatMap(model => protocol.sourceGroups.map((group: string) => {
    const a = run.rows.find((r: any) => r.model === model.id && r.group === group && r.arm === 'choice-rgb');
    const b = run.rows.find((r: any) => r.model === model.id && r.group === group && r.arm === 'choice-permuted');
    const query = questions.find(q => q.group === group)!.query;
    return { model: model.id, group, matched: !!a && !!b, sameSelectedPose: a?.score.selectedPose && b?.score.selectedPose
      ? key({ ...query, ...a.score.selectedPose }) === key({ ...query, ...b.score.selectedPose }) : null,
    bothCorrect: a && b ? a.score.success === 1 && b.score.success === 1 : null };
  }));
  const result = { version: 'pose-probe-analysis-1', status: run.status, responses: seen.size, planned: protocol.plannedCalls,
    newCost: cost, campaignAfter: run.campaignAfter, summary, pairs, apiRequests: 0,
    protocolHash: digest(protocol), runHash: digest(readFileSync(resolve(POSE_DIR, 'run.json'), 'utf8')), caveats: protocol.caveats };
  atomicJson(resolve(POSE_DIR, 'analysis.json'), result);
  return result;
}
