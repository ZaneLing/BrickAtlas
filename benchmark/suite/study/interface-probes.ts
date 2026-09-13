import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { SYSTEM } from '../storage';
import type { Structure } from '../shared';
import { type CaseTask, structureSchema } from '../v2/cases';
import { diagnoseResponse, diagnosticSummary } from './failure-diagnostics';
import { STUDY } from './protocol';

export function interfaceProbes() {
  return [1, 2, 4].flatMap(count => (['copy', 'recolor', 'plan'] as const).flatMap(operation => {
    const source: Structure = { version: 1, parts: Array.from({ length: count }, (_, i) => ({
      id: `p${i + 1}`, partId: '3005', color: 'red', x: 0, y: i * 3, z: 0, turn: 0,
    })) };
    const target = structuredClone(source);
    if (operation === 'recolor') for (const p of target.parts) p.color = 'blue';
    const kind: 'plan' | 'edit' = operation === 'plan' ? 'plan' : 'edit';
    const prompt = operation === 'copy' ? 'Return the supplied current structure unchanged, including every piece.'
      : operation === 'recolor' ? 'Change every red piece to blue. Preserve all IDs, types, positions and rotations. Return the full structure.'
        : 'Return all supplied piece IDs exactly once in a legal bottom-to-top assembly order. Output {"order":[...]} only.';
    const input = operation === 'plan' ? { target: source, direction: 'assemble' } : { current: source, operation };
    const responseSchema = operation === 'plan' ? { order: ['piece ID'] } : structureSchema;
    return (['envelope', 'minimal'] as const).map(arm => {
      const id = digest({ version: 'interface-probe-1', count, operation, arm }).slice(0, 24);
      const spec = { id, modelId: `tower-${count}`, group: `tower-${count}`, kind,
        variant: operation === 'plan' ? 'assemble' : operation, condition: 'default' as const,
        split: 'validation' as const, policy: 'interface-probe', difficulty: `pieces-${count}` };
      const publicTask = { id, kind, split: spec.split, family: spec.policy, prompt, input, responseSchema, imageTitles: [] };
      const task: CaseTask = { spec, public: publicTask, source, target, frames: [],
        changedIds: operation === 'recolor' ? source.parts.map(p => p.id) : [],
        oracle: operation === 'plan' ? { order: source.parts.map(p => p.id) } : target };
      return { id, count, operation, arm, task, system: SYSTEM,
        user: JSON.stringify(arm === 'envelope' ? publicTask : { prompt, input, responseSchema }) };
    });
  }));
}

export function prepareInterfaceProbes() {
  const cases = interfaceProbes().map(({ task: _task, ...row }) => row);
  const protocol = { version: 'interface-probe-1', maxTokens: 900, temperature: 0,
    checkpoints: ['base-seed17', 'multi-seed17'], cases,
    scope: 'Post-hoc interface calibration, not a held-out benchmark. Three tower sizes from one synthetic family; no images or perception claim. Both arms contain identical task data/schema; minimal omits metadata.',
    hash: digest(cases) };
  const file = resolve(STUDY, 'interface-probes/inputs.json');
  if (existsSync(file)) assert.deepEqual(JSON.parse(readFileSync(file, 'utf8')), protocol, 'Probe protocol changed');
  atomicJson(file, protocol);
  return { cases: cases.length, checkpoints: protocol.checkpoints, scope: protocol.scope };
}

export function replayInterfaceProbes() {
  const dir = resolve(STUDY, 'interface-probes');
  const protocol = JSON.parse(readFileSync(resolve(dir, 'inputs.json'), 'utf8'));
  const inputsHash = createHash('sha256').update(readFileSync(resolve(dir, 'inputs.json'))).digest('hex');
  const tasks = interfaceProbes();
  assert.equal(protocol.hash, digest(tasks.map(({ task: _task, ...row }) => row)));
  const rows = protocol.checkpoints.flatMap((checkpoint: string) => {
    const result = JSON.parse(readFileSync(resolve(dir, checkpoint + '.json'), 'utf8'));
    assert.equal(result.status, 'complete'); assert.equal(result.inputsSha256, inputsHash);
    assert.equal(result.checkpoint, checkpoint);
    assert.equal(result.scriptSha256, createHash('sha256').update(readFileSync(resolve(STUDY, '../../study/run-interface-probes.py'))).digest('hex'));
    const model = JSON.parse(readFileSync(resolve(STUDY, 'local', checkpoint, 'manifest.json'), 'utf8'));
    assert.equal(result.modelSha256, checkpoint.startsWith('base') ? model.model_sha256 : model.merged_model_sha256);
    assert.deepEqual(result.predictions.map((p: any) => p.id), tasks.map(t => t.id));
    return result.predictions.map((p: any, i: number) => {
      assert.equal(typeof p.raw, 'string');
      assert.ok(Number.isInteger(p.outputTokens) && p.outputTokens >= 0 && p.outputTokens <= protocol.maxTokens);
      assert.ok(Number.isInteger(p.inputTokens) && p.inputTokens > 0 && Number.isFinite(p.seconds) && p.seconds >= 0);
      const probe = tasks[i];
      return { checkpoint, id: p.id, operation: probe.operation, count: probe.count, arm: probe.arm,
        ...diagnoseResponse(probe.task, p.raw, p.outputTokens >= protocol.maxTokens ? 'length' : 'stop') };
    });
  });
  const summaries = protocol.checkpoints.flatMap((checkpoint: string) => ['envelope', 'minimal'].map(arm => ({
    checkpoint, arm, ...diagnosticSummary(rows.filter((r: any) => r.checkpoint === checkpoint && r.arm === arm)),
  })));
  const result = { scope: protocol.scope, apiRequests: 0, rows, summaries, actualModelCalls: rows.length,
    paired: protocol.checkpoints.flatMap((checkpoint: string) => tasks.filter(t => t.arm === 'envelope').map(t => {
      const pair = rows.filter((r: any) => r.checkpoint === checkpoint && r.operation === t.operation && r.count === t.count);
      return { checkpoint, count: t.count, operation: t.operation,
        before: pair.find((r: any) => r.arm === 'envelope')!.verdict.metrics.success,
        after: pair.find((r: any) => r.arm === 'minimal')!.verdict.metrics.success };
    })) };
  atomicJson(resolve(dir, 'replay.json'), result);
  return { actualModelCalls: rows.length, summaries };
}
