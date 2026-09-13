import assert from 'node:assert/strict';
import { readFileSync, existsSync, mkdirSync, writeFileSync, openSync, closeSync, unlinkSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson, Budget } from '../../core/budget';
import type { Message } from '../../core/openrouter';
import { BENCHMARK, SYSTEM } from '../storage';
import { digest } from '../data';
import { bom, validate, compare, decode } from '../geometry';
import { parseJSON } from '../score';
import { type Structure } from '../shared';
import { type CaseTask, structureSchema } from '../v2/cases';
import { independentCheck } from '../research/independent-check';
import { SuiteRenderer } from '../render';
import { imageEvidence } from './calibration-export';
import { calibrationSelection } from './calibration';
import { validationCases, VALIDATION_DIR } from './model-validation';
import { evaluateStrict } from './strict-evaluate';
import { diagnoseResponse } from './failure-diagnostics';
import { validationAggregate } from './model-validation-report';
import { VALIDATION_MODELS, validationPricing, validationCompletion, validationCeiling } from './validation-client';

const ladderDir = (normalized: boolean) => resolve(VALIDATION_DIR, normalized ? 'ladder-normalized' : 'ladder');
export function normalizeOrigin(structure: Structure): Structure {
  assert.ok(structure.parts.length > 0, 'Cannot anchor an empty structure');
  const minimum = Object.fromEntries(['x', 'y', 'z'].map(axis => [axis,
    Math.min(...structure.parts.map(p => p[axis as 'x' | 'y' | 'z']))]));
  return { version: 1, parts: structure.parts.map(p => ({ ...p,
    x: p.x - minimum.x, y: p.y - minimum.y, z: p.z - minimum.z })) };
}
export function ladderTasks(normalized = false) {
  const excluded = new Set(validationCases().chosen.map(o => o.group));
  const source = calibrationSelection().objects.filter(o => !excluded.has(o.group))
    .sort((a, b) => digest(`ladder-1:${a.group}`).localeCompare(digest(`ladder-1:${b.group}`)))[0];
  return [2, 4, 8].flatMap(count => {
    const prefix: Structure = { version: 1, parts: structuredClone(source.structure.parts.slice(0, count)) };
    const target = normalized ? normalizeOrigin(prefix) : prefix;
    assert.deepEqual(validate(target.parts), []);
    assert.deepEqual(independentCheck(target.parts).issues, []);
    return (['ordinary', 'symbolic'] as const).map(condition => {
      const id = digest({ version: normalized ? 'ladder-2-origin-normalized' : 'ladder-1', source: source.group, count, condition }).slice(0, 24);
      const spec = { id, group: source.group, modelId: source.id, policy: source.policy, difficulty: `${count}-piece-prefix`,
        kind: 'reconstruct' as const, variant: 'full', condition, split: 'validation' as const };
      const task: CaseTask = { spec, target, source: null, changedIds: [], oracle: target,
        frames: condition === 'ordinary' ? (['iso', 'top', 'front', 'side'] as const).map(view =>
          ({ parts: target.parts, view, layer: null, title: `Ordinary assembled ${view}` })) : [],
        public: { id, kind: 'reconstruct', split: 'validation', family: source.policy,
          prompt: 'Reconstruct a legal structure matching the supplied reference and BOM. Return the full JSON structure; IDs may be arbitrary.'
            + (condition === 'ordinary' ? ' Alternate hidden layouts may match colored positive-X/Y/Z first-hit surfaces, BOM and legality.'
              : ' Privileged symbolic diagnostic: full type/color/pose agreement is required; this is not a visual result.')
            + (normalized ? ' Coordinate convention: the minimum X, Y and Z of the full assembly are each zero.' : ''),
          input: { billOfMaterials: bom(target.parts), ...(condition === 'symbolic' ? { reference: target } : {}) },
          responseSchema: structureSchema, imageTitles: condition === 'ordinary' ? ['iso', 'top', 'front', 'side'].map(v => `Ordinary assembled ${v}`) : [] } };
      assert.equal(evaluateStrict(task, task.oracle).metrics.success, 1);
      return { count, condition, task };
    });
  });
}

export async function prepareLadder(renderer: SuiteRenderer, normalized = false) {
  const DIR = ladderDir(normalized);
  const tasks = ladderTasks(normalized), rows = [];
  mkdirSync(resolve(DIR, 'images'), { recursive: true });
  for (const { count, condition, task } of tasks) {
    const images = [];
    for (const frame of task.frames) {
      const r = await renderer.render(frame); imageEvidence(r.buffer);
      const path = `images/${r.hash}.png`;
      if (existsSync(resolve(DIR, path))) assert.deepEqual(readFileSync(resolve(DIR, path)), r.buffer);
      else writeFileSync(resolve(DIR, path), r.buffer);
      images.push(path);
    }
    rows.push({ id: task.spec.id, count, condition, input: task.public, images });
  }
  const protocol = { version: normalized ? 'ladder-2-origin-normalized' : 'ladder-1', sourceGroup: tasks[0].task.spec.group, models: VALIDATION_MODELS,
    rows, plannedRequests: 24,
    scope: 'Adaptive development follow-up: three nested prefixes from one unused calibration source object. Not three independent objects. Changes piece count and geometry jointly, not a causal scaling test. Frozen old model-validation results are untouched.'
      + (normalized ? ' Origin-normalized revision after inspecting v1: translate every cropped prefix to minimum XYZ=0 and explicitly declare the convention. Also resampled, so gains cannot be causally attributed to normalization alone.' : ''),
    apiRequestsAtPreparation: 0 };
  const path = resolve(DIR, 'protocol.json');
  if (existsSync(path)) assert.deepEqual(JSON.parse(readFileSync(path, 'utf8')), protocol);
  atomicJson(path, protocol); return { tasks: rows.length, plannedRequests: 24, sourceGroups: 1 };
}

function messagesFor(row: any, normalized = false): Message[] {
  const DIR = ladderDir(normalized);
  const content: Exclude<Message['content'], string> = [{ type: 'text', text: JSON.stringify(row.input) }];
  for (const [i, path] of row.images.entries()) {
    assert.match(path, /^images\/[a-f0-9]{64}\.png$/);
    const bytes = readFileSync(resolve(DIR, path)); assert.equal(imageEvidence(bytes).hash, path.slice(7, -4));
    content.push({ type: 'text', text: row.input.imageTitles[i] },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${bytes.toString('base64')}` } });
  }
  return [{ role: 'system', content: SYSTEM }, { role: 'user', content }];
}

export async function runLadder(normalized = false) {
  const DIR = ladderDir(normalized);
  const parent = JSON.parse(readFileSync(resolve(VALIDATION_DIR, 'run.json'), 'utf8'));
  assert.equal(parent.status, 'complete', 'Analyze the fixed screen before follow-up');
  const analysis = JSON.parse(readFileSync(resolve(VALIDATION_DIR, 'analysis.json'), 'utf8'));
  assert.equal(analysis.rawRunHash, digest(readFileSync(resolve(VALIDATION_DIR, 'run.json'), 'utf8')));
  const protocol = JSON.parse(readFileSync(resolve(DIR, 'protocol.json'), 'utf8')), tasks = ladderTasks(normalized);
  for (const row of protocol.rows) assert.deepEqual(row.input, tasks.find(t => t.task.spec.id === row.id)!.task.public);
  if (!process.env.OPENROUTER_API_KEY) process.loadEnvFile(resolve(BENCHMARK, '../.env'));
  const key = process.env.OPENROUTER_API_KEY; assert.ok(key);
  const lock = resolve(BENCHMARK, '.runtime/pilot.lock'), fd = openSync(lock, 'wx', 0o600); closeSync(fd);
  try {
    const budget = new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json'));
    const path = resolve(DIR, 'run.json');
    assert.ok(!existsSync(path), 'Preserve previous follow-up; no implicit rerun');
    const run = { status: 'running', protocolHash: digest(protocol), pricing: await validationPricing(),
      clientHash: digest(readFileSync(resolve(BENCHMARK, 'suite/study/validation-client.ts'), 'utf8')),
      campaignBefore: budget.spent, campaignAfter: budget.spent, error: null as string | null, rows: [] as any[] };
    const save = () => { run.campaignAfter = budget.spent; atomicJson(path, run); atomicJson(resolve(DIR, 'ledger.json'), budget.ledger); };
    save();
    try {
      for (const row of protocol.rows) for (const model of protocol.models) {
        const messages = messagesFor(row, normalized);
        if (budget.spent - parent.campaignBefore + validationCeiling(model.id, messages) > 2) throw new Error('Shared $2 validation budget exhausted');
        const call = await validationCompletion(key, model.id, messages, budget);
        const task = tasks.find(t => t.task.spec.id === row.id)!.task;
        run.rows.push({ id: row.id, count: row.count, condition: row.condition, model: model.id,
          inputHash: digest(messages), call, diagnosis: diagnoseResponse(task, call.content, call.finishReason) });
        save(); console.log(JSON.stringify({ completed: run.rows.length, planned: 24 }));
      }
      run.status = 'complete';
    } catch (error) { run.status = 'stopped'; run.error = (error as Error).message; }
    save(); return { status: run.status, calls: run.rows.length, error: run.error };
  } finally { unlinkSync(lock); }
}

export function replayLadder(normalized = false) {
  const DIR = ladderDir(normalized);
  const run = JSON.parse(readFileSync(resolve(DIR, 'run.json'), 'utf8'));
  const protocol = JSON.parse(readFileSync(resolve(DIR, 'protocol.json'), 'utf8')), tasks = ladderTasks(normalized);
  assert.equal(run.protocolHash, digest(protocol));
  assert.equal(run.clientHash, digest(readFileSync(resolve(BENCHMARK, 'suite/study/validation-client.ts'), 'utf8')));
  assert.deepEqual(protocol.rows.map((r: any) => r.id), tasks.map(t => t.task.spec.id));
  const ledger = JSON.parse(readFileSync(resolve(DIR, 'ledger.json'), 'utf8')), seen = new Set(), receipts = new Set();
  let cost = 0;
  for (const row of run.rows) {
    const input = protocol.rows.find((r: any) => r.id === row.id), task = tasks.find(t => t.task.spec.id === row.id);
    assert.ok(task && input); assert.deepEqual(input.input, task.task.public);
    assert.equal(row.count, task.count); assert.equal(row.condition, task.condition);
    assert.ok(VALIDATION_MODELS.some(m => m.id === row.model));
    assert.ok(!seen.has(`${row.id}:${row.model}`)); seen.add(`${row.id}:${row.model}`);
    assert.ok(!receipts.has(row.call.id)); receipts.add(row.call.id);
    assert.equal(row.inputHash, digest(messagesFor(input, normalized)));
    assert.deepEqual(row.diagnosis, diagnoseResponse(task.task, row.call.content, row.call.finishReason));
    const charge = ledger.charges.find((c: any) => c.generationId === row.call.id);
    assert.equal(charge.status, 'settled'); assert.equal(charge.actual, row.call.cost); cost += row.call.cost;
  }
  assert.ok(Math.abs(cost - run.campaignAfter + run.campaignBefore) < 1e-8);
  if (run.status === 'complete') assert.equal(run.rows.length, 24);
  const summary = { status: run.status, responses: run.rows.length, newCost: cost, sourceGroups: 1, apiRequests: 0,
    originAudit: {
      minimums: tasks.filter(t => t.condition === 'ordinary').map(t => ({ count: t.count,
        x: Math.min(...t.task.target.parts.map(p => p.x)), y: Math.min(...t.task.target.parts.map(p => p.y)),
        z: Math.min(...t.task.target.parts.map(p => p.z)) })),
      translationOnlyRecoveries: run.rows.flatMap((row: any) => {
        const decoded = decode(parseJSON(row.call.content));
        if (row.condition !== 'ordinary' || row.diagnosis.verdict.metrics.success || !decoded?.parts.length) return [];
        const task = tasks.find(t => t.task.spec.id === row.id)!.task;
        return compare(normalizeOrigin(task.target).parts, normalizeOrigin(decoded).parts).exact
          ? [{ id: row.id, model: row.model, count: row.count }] : [];
      }),
      scope: 'Post-hoc origin audit only; never changes stored predictions or official scores.',
    },
    rows: [2, 4, 8].flatMap(count => ['ordinary', 'symbolic'].flatMap(condition => VALIDATION_MODELS.map(model => ({
      count, condition, model: model.id, ...validationAggregate(run.rows.filter((r: any) =>
        r.count === count && r.condition === condition && r.model === model.id), 1),
    })))), scope: protocol.scope };
  atomicJson(resolve(DIR, 'replay.json'), summary); return summary;
}
