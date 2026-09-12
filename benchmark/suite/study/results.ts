import assert from 'node:assert/strict';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { atomicJson } from '../../core/budget';
import type { CallResult } from '../../core/openrouter';
import type { PublicTask } from '../shared';
import { parseJSON, legalityFeedback } from '../score';
import { relative, decode } from '../geometry';
import { BENCHMARK } from '../storage';
import { digest } from '../data';
import { sourceHashes } from '../v2/build';
import { getSpec, taskForV2 } from '../v2/cases';
import { evaluate, type Evaluation } from '../v2/evaluate';
import { clusterBootstrap } from '../v2/batch';
import { STUDY } from './protocol';

export interface StudyRow {
  caseId: string; model: string; arm?: string; input: PublicTask; images: string[];
  call: CallResult; answer: unknown; verdict: Evaluation; reusedFirstCall?: CallResult | null; feedback?: string | null;
  imageDonor?: string | null;
}
export function studyRuns() {
  const root = resolve(STUDY, 'runs');
  return existsSync(root) ? readdirSync(root).flatMap(id => {
    const path = resolve(root, id, 'run.json');
    return existsSync(path) ? [JSON.parse(readFileSync(path, 'utf8'))] : [];
  }) : [];
}
export function summarize(run: { rows: StudyRow[]; model?: string }) {
  const groups = new Map<string, StudyRow[]>();
  for (const r of run.rows) {
    const spec = getSpec(r.caseId), k = [r.model ?? run.model, spec.kind, spec.variant, spec.condition, spec.split, r.arm ?? 'one-shot'].join('|');
    groups.set(k, [...groups.get(k) ?? [], r]);
  }
  return [...groups].map(([stratum, rows]) => {
    const fields = [...new Set(rows.flatMap(r => Object.keys(r.verdict.metrics)))];
    const groupIds = [...new Set(rows.map(r => getSpec(r.caseId).group))];
    return { stratum, n: rows.length, sourceGroups: groupIds.length,
      metrics: Object.fromEntries(fields.map(k => {
        const values = rows.map(r => r.verdict.metrics[k]).filter((v): v is number => typeof v === 'number');
        return [k, { value: values.length ? values.reduce((a, b) => a + b, 0) / values.length : null, n: values.length }];
      })),
      successInterval: clusterBootstrap(groupIds.map(g => {
        const selected = rows.filter(r => getSpec(r.caseId).group === g);
        return selected.reduce((n, r) => n + r.verdict.metrics.success, 0) / selected.length;
      })),
      outputTokens: rows.reduce((n, r) => n + r.call.completionTokens, 0),
      promptTokens: rows.reduce((n, r) => n + r.call.promptTokens, 0),
      latencyMs: rows.reduce((n, r) => n + r.call.latencyMs, 0),
      cost: rows.reduce((n, r) => n + r.call.cost, 0),
      truncated: rows.filter(r => r.call.finishReason === 'length').length };
  });
}
export function replayStudy() {
  const evidence = [];
  const protocol = JSON.parse(readFileSync(resolve(STUDY, 'protocol.json'), 'utf8'));
  assert.deepEqual(protocol.sourceHashes, sourceHashes());
  for (const run of studyRuns()) {
    assert.equal(run.status, 'complete', 'Never count incomplete run as completed');
    const script = run.parentId ? 'control.ts' : 'run-api.ts';
    assert.equal(run.parentId ? run.scriptHash : run.runnerHash,
      digest(readFileSync(resolve(BENCHMARK, 'suite/study', script), 'utf8')));
    const ledger = JSON.parse(readFileSync(resolve(STUDY, 'runs', run.id, 'ledger.json'), 'utf8'));
    const seen = new Set<string>(), callIds = new Set<string>(); let cost = 0;
    for (const row of run.rows as StudyRow[]) {
      const task = taskForV2(getSpec(row.caseId));
      assert.deepEqual(row.answer, parseJSON(row.call.content));
      assert.deepEqual(row.verdict, evaluate(task, row.answer));
      const k = [row.caseId, row.model ?? run.model, row.arm].join('|');
      assert.ok(!seen.has(k)); seen.add(k);
      assert.ok(!callIds.has(row.call.id)); callIds.add(row.call.id);
      assert.ok(protocol.cases.some((s: { id: string }) => s.id === row.caseId));
      const charge = ledger.charges.find((c: { generationId: string }) => c.generationId === row.call.id);
      assert.equal(charge.status, 'settled'); assert.equal(charge.actual, row.call.cost); cost += row.call.cost;
      if (!row.arm) assert.deepEqual(row.input, task.public);
      if (row.arm) {
        const expectedInput = structuredClone(task.public);
        if (row.arm === 'no-image') {
          expectedInput.imageTitles = [];
          expectedInput.prompt += ' Control condition: images are withheld. Use only the remaining public information.';
          assert.equal(row.images.length, 0);
        }
        if (row.arm === 'relative') expectedInput.input.target = relative(decode(expectedInput.input.target)!);
        if (row.arm === 'symbolic-reference') {
          expectedInput.imageTitles = []; expectedInput.input.reference = task.target;
          expectedInput.prompt += ' Privileged diagnostic: use the supplied full symbolic reference; images are omitted.';
          assert.equal(row.images.length, 0);
        }
        if (row.arm === 'mismatched-images') {
          const parent = studyRuns().find(r => r.id === run.parentId);
          const donor = parent.rows.find((r: StudyRow) => r.caseId === row.imageDonor && r.model === run.model);
          assert.notEqual(getSpec(donor.caseId).modelId, getSpec(row.caseId).modelId);
          assert.deepEqual(row.images, donor.images);
        }
        assert.deepEqual(row.input, expectedInput);
      }
      if (row.reusedFirstCall) {
        const parent = studyRuns().find(r => r.id === run.parentId);
        assert.deepEqual(row.reusedFirstCall, parent.rows.find((r: StudyRow) => r.caseId === row.caseId && r.model === run.model).call);
        assert.equal(row.feedback, row.arm === 'reflection'
          ? 'Review the previous answer once. No new scene information is supplied. Return final JSON.'
          : `Review the previous answer with this target-blind legality report: ${JSON.stringify(legalityFeedback(parseJSON(row.reusedFirstCall.content)))}. Return final JSON.`);
      }
      for (const file of row.images ?? []) {
        const image = readFileSync(resolve(STUDY, 'inputs', file));
        assert.equal(digest(image.toString('base64')), file.slice(7, -4));
      }
    }
    assert.ok(Math.abs(cost - (run.campaignAfter - run.campaignBefore)) < 1e-8);
    assert.equal(run.rows.length, run.selection?.length ?? protocol.cases.length * protocol.settings.models.length);
    atomicJson(resolve(STUDY, 'runs', run.id, 'summary.json'), summarize(run));
    evidence.push({ id: run.id, cases: run.rows.length, newCost: cost, allScoresMatch: true, receiptsSettled: true,
      rawRunSha256: createHash('sha256').update(readFileSync(resolve(STUDY, 'runs', run.id, 'run.json'))).digest('hex') });
  }
  atomicJson(resolve(STUDY, 'replay.json'), evidence); return evidence;
}
