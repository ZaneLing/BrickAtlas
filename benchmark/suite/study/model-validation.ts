import assert from 'node:assert/strict';
import { closeSync, existsSync, openSync, readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { Budget, atomicJson } from '../../core/budget';
import type { Message, CallResult } from '../../core/openrouter';
import { BENCHMARK, SYSTEM } from '../storage';
import { digest } from '../data';
import { getSpec, taskForV2 } from '../v2/cases';
import { STUDY } from './protocol';
import { calibrationSelection } from './calibration';
import { verifyCalibrationInputs } from './calibration-export';
import { diagnoseResponse } from './failure-diagnostics';
import { VALIDATION_MODELS, VALIDATION_TOKENS, validationCeiling, validationPricing, validationCompletion } from './validation-client';

export const VALIDATION_DIR = resolve(STUDY, 'model-validation');
export function validationCases() {
  const { objects, cases } = calibrationSelection();
  const chosen = ['small', 'medium', 'large'].map(difficulty => {
    const pool = objects.filter(o => o.difficulty === difficulty)
      .sort((a, b) => digest(`model-validation-1:${a.group}`).localeCompare(digest(`model-validation-1:${b.group}`)));
    assert.ok(pool.length, `No ${difficulty} calibration object`); return pool[0];
  });
  const publicRows = readFileSync(resolve(STUDY, 'calibration/inputs/public.jsonl'), 'utf8').trim().split('\n').map(l => JSON.parse(l));
  const base = chosen.flatMap(object => cases.filter(s => s.group === object.group).map(spec => {
    const row = publicRows.find(r => r.caseId === spec.id);
    assert.deepEqual(row.input, taskForV2(spec).public);
    return { id: `${spec.id}:ordinary`, caseId: spec.id, arm: 'ordinary', input: row.input, images: row.images as string[] };
  }));
  const controls = base.filter(r => getSpec(r.caseId).kind === 'reconstruct').flatMap(row =>
    ['no-image', 'symbolic-reference'].map(arm => {
      const input = structuredClone(row.input); input.imageTitles = [];
      if (arm === 'symbolic-reference') {
        input.input.reference = taskForV2(getSpec(row.caseId)).target;
        input.prompt += ' Privileged diagnostic: a full symbolic reference is supplied; this is not a visual result.';
      } else input.prompt += ' Diagnostic: images are withheld; all remaining public information is unchanged.';
      return { ...row, id: `${row.caseId}:${arm}`, arm, input, images: [] };
    }));
  return { chosen: chosen.map(o => ({ id: o.id, group: o.group, policy: o.policy, difficulty: o.difficulty, pieces: o.structure.parts.length })),
    rows: [...base, ...controls] };
}

export function validationMessages(row: ReturnType<typeof validationCases>['rows'][number]): Message[] {
  const content: Exclude<Message['content'], string> = [{ type: 'text', text: JSON.stringify(row.input) }];
  for (const [i, path] of row.images.entries()) {
    assert.match(path, /^images\/[a-f0-9]{64}\.png$/);
    const bytes = readFileSync(resolve(STUDY, 'calibration/inputs', path));
    assert.equal(digest(bytes.toString('base64')), path.slice(7, -4));
    content.push({ type: 'text', text: row.input.imageTitles[i] },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${bytes.toString('base64')}` } });
  }
  return [{ role: 'system', content: SYSTEM }, { role: 'user', content }];
}

export function prepareModelValidation() {
  verifyCalibrationInputs();
  const selected = validationCases();
  const protocol = { version: 'model-validation-1', ...selected, models: VALIDATION_MODELS,
    maxTokens: VALIDATION_TOKENS, temperature: 0, responseFormat: 'json_object', attempts: 1,
    plannedRequests: selected.rows.length * VALIDATION_MODELS.length, newSpendCap: 2.0,
    scope: 'Development screen: three independent objects, one per piece-count bin, not a powered leaderboard. Thirteen task variants; no isolated-part recognition. No-image and privileged-symbolic controls are separate.',
    sampleSelectionUsesOutcomes: false,
    analysisRules: ['Report all task/variant scores and denominators, format/domain/geometry gates and partial metrics.',
      'Never pool privileged controls into primary performance.',
      'A floor/ceiling on all models is a sensitivity warning, not proof a task is invalid.',
      'A rank on three objects is descriptive only; no significance or reliable total-rank claim.',
      'Provider/transport failures are missing evidence, not cognitive failures.',
      'Changes motivated by these results must be validated separately; do not rewrite frozen scores.'] };
  const path = resolve(VALIDATION_DIR, 'protocol.json');
  if (existsSync(path)) assert.deepEqual(JSON.parse(readFileSync(path, 'utf8')), protocol, 'Frozen protocol drift');
  atomicJson(path, protocol);
  return { plannedRequests: protocol.plannedRequests, chosen: selected.chosen,
    worstCaseReservationSum: VALIDATION_MODELS.reduce((n, m) => n + selected.rows.reduce((n, r) => n + validationCeiling(m.id, validationMessages(r)), 0), 0),
    newSpendCap: protocol.newSpendCap };
}

export async function runModelValidation() {
  prepareModelValidation();
  const protocol = JSON.parse(readFileSync(resolve(VALIDATION_DIR, 'protocol.json'), 'utf8'));
  if (!process.env.OPENROUTER_API_KEY) process.loadEnvFile(resolve(BENCHMARK, '../.env'));
  const key = process.env.OPENROUTER_API_KEY; if (!key) throw new Error('Missing credential');
  const lock = resolve(BENCHMARK, '.runtime/pilot.lock'), fd = openSync(lock, 'wx', 0o600);
  writeFileSync(fd, `${process.pid}\n`); closeSync(fd);
  try {
    const budget = new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json'));
    if (budget.blocked) throw new Error('Reconcile previous charge first');
    const path = resolve(VALIDATION_DIR, 'run.json');
    const run = existsSync(path) ? JSON.parse(readFileSync(path, 'utf8')) : {
      version: protocol.version, protocolHash: digest(protocol), pricing: await validationPricing(),
      startedAt: new Date().toISOString(), campaignBefore: budget.spent, campaignAfter: budget.spent,
      sourceHash: digest(readFileSync(resolve(BENCHMARK, 'suite/study/validation-client.ts'), 'utf8')),
      status: 'running', rows: [], error: null,
    };
    assert.equal(run.protocolHash, digest(protocol));
    assert.equal(run.sourceHash, digest(readFileSync(resolve(BENCHMARK, 'suite/study/validation-client.ts'), 'utf8')));
    if (run.status === 'complete') return { status: 'already-complete', calls: run.rows.length };
    if (run.status !== 'running') throw new Error('Prior run stopped; explicit review required before new requests');
    const persist = () => { run.campaignAfter = budget.spent; atomicJson(path, run); atomicJson(resolve(VALIDATION_DIR, 'ledger.json'), budget.ledger); };
    persist();
    try {
      for (const [i, row] of protocol.rows.entries()) {
        // Rotate model order to avoid always running one model first.
        const models = protocol.models.map((_: unknown, j: number) => protocol.models[(i + j) % protocol.models.length]);
        for (const model of models) {
          if (run.rows.some((r: any) => r.id === row.id && r.model === model.id)) continue;
          const messages = validationMessages(row), ceiling = validationCeiling(model.id, messages);
          if (budget.spent - run.campaignBefore + ceiling > protocol.newSpendCap) throw new Error('Validation allocation exhausted; uncalled cases retained as missing');
          const call = await validationCompletion(key, model.id, messages, budget);
          run.rows.push({ id: row.id, caseId: row.caseId, model: model.id, arm: row.arm,
            inputHash: digest(messages), call, diagnosis: diagnoseResponse(taskForV2(getSpec(row.caseId)), call.content, call.finishReason) });
          persist();
          console.log(JSON.stringify({ completed: run.rows.length, planned: protocol.plannedRequests,
            model: model.id, case: i + 1, newCost: budget.spent - run.campaignBefore }));
        }
      }
      run.status = 'complete'; run.completedAt = new Date().toISOString();
    } catch (error) { run.status = 'stopped'; run.error = (error as Error).message; }
    persist(); return { status: run.status, calls: run.rows.length, error: run.error, newCost: run.campaignAfter - run.campaignBefore };
  } finally { unlinkSync(lock); }
}

export function replayModelValidation() {
  const protocol = JSON.parse(readFileSync(resolve(VALIDATION_DIR, 'protocol.json'), 'utf8'));
  const run = JSON.parse(readFileSync(resolve(VALIDATION_DIR, 'run.json'), 'utf8'));
  assert.equal(run.protocolHash, digest(protocol));
  assert.equal(run.sourceHash, digest(readFileSync(resolve(BENCHMARK, 'suite/study/validation-client.ts'), 'utf8')));
  const expected = validationCases(); assert.deepEqual(protocol.rows, expected.rows);
  const ledger = JSON.parse(readFileSync(resolve(VALIDATION_DIR, 'ledger.json'), 'utf8'));
  const seen = new Set(), receipts = new Set(); let cost = 0;
  for (const row of run.rows) {
    const input = expected.rows.find(r => r.id === row.id); assert.ok(input);
    assert.equal(row.caseId, input.caseId); assert.equal(row.arm, input.arm);
    assert.ok(VALIDATION_MODELS.some(m => m.id === row.model));
    const k = `${row.id}|${row.model}`; assert.ok(!seen.has(k)); seen.add(k);
    assert.equal(row.inputHash, digest(validationMessages(input)));
    const call = row.call as CallResult; assert.ok(!receipts.has(call.id)); receipts.add(call.id);
    assert.ok(Number.isFinite(call.cost) && call.cost >= 0);
    assert.ok(Number.isInteger(call.promptTokens) && call.promptTokens > 0);
    assert.ok(Number.isInteger(call.completionTokens) && call.completionTokens >= 0 && call.completionTokens <= VALIDATION_TOKENS);
    const charge = ledger.charges.find((c: any) => c.generationId === call.id);
    assert.equal(charge?.status, 'settled'); assert.equal(charge.actual, call.cost); cost += call.cost;
    assert.deepEqual(row.diagnosis, diagnoseResponse(taskForV2(getSpec(row.caseId)), call.content, call.finishReason));
  }
  assert.ok(Math.abs(cost - (run.campaignAfter - run.campaignBefore)) < 1e-8);
  if (run.status === 'complete') assert.equal(seen.size, protocol.plannedRequests);
  const report = { status: run.status, responses: seen.size, expected: protocol.plannedRequests,
    newCost: cost, scoresReproduced: true, receiptsVerified: true, apiRequests: 0 };
  atomicJson(resolve(VALIDATION_DIR, 'replay.json'), report); return report;
}
