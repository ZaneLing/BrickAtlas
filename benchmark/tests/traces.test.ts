import { test } from 'node:test';
import assert from 'node:assert/strict';
import { listRuns } from '../suite/storage';
import { buildTrace, differences } from '../suite/traces';
import { models, digest } from '../suite/data';
import { PAIRED_VERSION, type PairedRun } from '../suite/research/paired';
import { RESEARCH_VERSION } from '../suite/research/dataset';
import type { ResearchRun } from '../suite/research/run';

test('all historical cases migrate without changing responses, scores or costs', () => {
  let cases = 0, calls = 0;
  for (const run of listRuns()) for (let index = 0; index < run.results.length; index++) {
    const row = run.results[index], trace = buildTrace(run, index);
    assert.equal(trace.evidence.scoreMatches, true);
    assert.deepEqual(trace.verdict, row.verdict);
    assert.equal(trace.events.filter(e => e.kind === 'response').length, row.calls.length);
    assert.ok(Math.abs(trace.events.reduce((n, e) => n + e.cost, 0) - trace.evidence.cost) < 1e-8);
    for (const [i, event] of trace.events.entries()) {
      assert.equal(event.id, i);
      assert.equal(event.timestamp, null);
      assert.equal(digest(trace.states[event.after]), event.after);
      if (i) assert.equal(event.before, trace.events[i - 1].after);
      if (event.kind === 'response') assert.equal(event.provenance, 'recorded');
      if (event.kind === 'unfold' || event.kind === 'execute' || event.kind === 'score') assert.equal(event.provenance, 'derived');
    }
    if (row.kind !== 'plan') assert.equal(trace.events.some(e => e.actor === 'environment' && e.kind === 'execute'), false);
    if (row.kind === 'relations') assert.equal(trace.evidence.outputMeaning, 'context-only');
    cases++; calls += row.calls.length;
  }
  assert.ok(cases >= 70); assert.ok(calls >= 102);
});
test('successful disassembly targets an empty final scene, not a missing full model', () => {
  let checked = 0;
  for (const run of listRuns()) for (const [i, row] of run.results.entries()) {
    if (row.kind === 'plan' && row.input.input.direction === 'disassemble' && row.verdict.metrics.success) {
      const trace = buildTrace(run, i);
      assert.equal(trace.reference.length, 0); assert.equal(trace.output.length, 0);
      assert.deepEqual(trace.differences, []); checked++;
    }
  }
  assert.ok(checked > 0);
});
test('unchanged poses with different IDs match; wrong color, nearby pose and missing pieces are labeled', () => {
  const p = models()[0].structure.parts[0];
  assert.deepEqual(differences([p], [{ ...p, id: 'other' }]), []);
  assert.equal(differences([p], [{ ...p, id: 'other', color: p.color === 'red' ? 'blue' : 'red' }])[0].kind, 'color');
  assert.equal(differences([p], [{ ...p, id: 'other', x: p.x + 1 }])[0].kind, 'pose');
  assert.equal(differences([p], [])[0].kind, 'missing');
  assert.equal(differences([], [p])[0].kind, 'extra');
});
test('historical source corruption fails closed instead of fabricating a replay', () => {
  const run = structuredClone(listRuns()[0]);
  run.results[0].input.prompt += 'corrupted';
  assert.throws(() => buildTrace(run, 0), /version differs/);
  assert.throws(() => buildTrace(run, -1), /Unknown case/);
});
test('paired trace preserves receipts but charges only new responses and labels reflection honestly', () => {
  const parent = structuredClone(listRuns().find(r => r.version === RESEARCH_VERSION)) as ResearchRun;
  assert.ok(parent);
  const source = parent.results[0];
  const run: PairedRun = { ...parent, version: PAIRED_VERSION, mode: 'paired-reflection',
    paired: { parentRun: parent.id, arm: 'reflection', reusedFirstResponse: true },
    results: [{ ...source, mode: 'paired-reflection', refinementPrompt: 'Review without new information.',
      calls: [source.calls[0], { ...source.calls[0], id: 'synthetic-test-only' }], answers: [source.answers[0], source.answers[0]] }] };
  const trace = buildTrace(run, 0), responses = trace.events.filter(e => e.kind === 'response');
  assert.equal(trace.evidence.cost, source.calls[0].cost);
  assert.equal(responses[0].cost, 0);
  assert.equal((responses[0].payload as { originalReceiptCost: number }).originalReceiptCost, source.calls[0].cost);
  assert.equal(trace.evidence.reusedFirstResponse, true);
  const feedback = trace.events.find(e => e.kind === 'feedback')!;
  assert.equal(feedback.payload, run.results[0].refinementPrompt);
  assert.equal(feedback.title, '无新增信息的反思指令');
});
