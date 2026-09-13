import { test } from 'node:test';
import assert from 'node:assert/strict';
import { observedGroups, exposureRecords } from '../suite/study/exposure';
import { sourceGate, EXTERNAL_SOURCE_CANDIDATES } from '../suite/study/source-policy';
import { summarizeAudit, type AuditLabel } from '../suite/study/human-audit';
import { orderQuestions, orderScenes, orderScore } from '../suite/study/order-study';
import { pairedOrderEffect } from '../suite/study/order-run';
import { summarizeReadiness } from '../suite/study/readiness';

test('external source release requires actual assets and permission, not a public URL', () => {
  for (const a of EXTERNAL_SOURCE_CANDIDATES) {
    const result = sourceGate(a); assert.equal(result.readyForRelease, false);
    assert.ok(result.missing.includes('permission-evidence')); assert.ok(result.missing.includes('actual-assets'));
  }
});
test('prepared groups are not falsely marked as model-observed', () => {
  const records = exposureRecords(), observed = observedGroups(records);
  const onlyPrepared = records.filter(r => r.role === 'prepared-calibration' && !observed.has(r.group));
  assert.ok(onlyPrepared.length > 0);
  for (const r of onlyPrepared) assert.ok(!records.some(q => q.group === r.group && q.role !== 'prepared-calibration'));
});
test('human audit fails closed on duplicates, wrong version and synthetic attestation', () => {
  const items = [{ id: 'item' }] as any;
  const label: AuditLabel = { itemId: 'item', reviewerCode: 'human_a', packetHash: 'hash',
    judgment: 'accept', notes: 'Specific actual review notes', independent: true, humanAttested: true };
  assert.equal(summarizeAudit(items, [], 'hash').completeConsensus, false);
  assert.equal(summarizeAudit(items, [label], 'hash').completeConsensus, false);
  assert.throws(() => summarizeAudit(items, [label, label], 'hash'), /Duplicate/);
  assert.throws(() => summarizeAudit(items, [label], 'other'), /packet/);
  assert.throws(() => summarizeAudit(items, [{ ...label, humanAttested: false } as any], 'hash'));
  const disagreement = summarizeAudit(items, [label, { ...label, reviewerCode: 'human_b', judgment: 'reject' }], 'hash');
  assert.equal(disagreement.requiresAdjudication, 1); assert.equal(disagreement.completeConsensus, false);
  const agreed = summarizeAudit(items, [label, { ...label, reviewerCode: 'human_b' }], 'hash');
  assert.equal(agreed.completeConsensus, true); assert.equal(agreed.independenceVerifiedExternally, false);
});
test('order replication freezes 12 new sources and separates repeat from permutation', () => {
  const scenes = orderScenes(), observed = observedGroups(exposureRecords(false)), qs = orderQuestions();
  assert.equal(scenes.length, 12); assert.equal(new Set(scenes.map(s => s.group)).size, 12);
  assert.ok(scenes.every(s => !observed.has(s.group))); assert.equal(qs.length, 48);
  for (const q of qs) assert.equal(orderScore(q, JSON.stringify({ choice: q.expected })).success, 1);
  for (const q of qs.filter(q => q.arm === 'original')) {
    const repeated = qs.find(r => r.group === q.group && r.arm === 'repeat')!;
    const permuted = qs.find(r => r.group === q.group && r.arm === 'permuted')!;
    assert.deepEqual(q.input, repeated.input); assert.deepEqual(q.frames, repeated.frames);
    assert.notEqual(q.expected, permuted.expected);
  }
  for (const label of 'ABCD') assert.equal(qs.filter(q => q.arm === 'original' && q.expected === label).length, 3);
});
test('paired order endpoint subtracts resampling mismatch and keeps missing pairs null', () => {
  assert.equal(pairedOrderEffect(null, 'a', 'b'), null);
  assert.deepEqual(pairedOrderEffect('a', 'b', 'a'), { repeatMismatch: 1, permutationMismatch: 0, excessMismatch: -1 });
  assert.deepEqual(pairedOrderEffect('a', 'b', 'c'), { repeatMismatch: 1, permutationMismatch: 1, excessMismatch: 0 });
  assert.deepEqual(pairedOrderEffect('a', 'a', 'b'), { repeatMismatch: 0, permutationMismatch: 1, excessMismatch: 1 });
});
test('research readiness cannot turn partial engineering checks into completion', () => {
  const gates = [{ id: 'code', passed: true, evidence: ['test.json'], reason: 'tests' },
    { id: 'human', passed: false, evidence: [], reason: 'no labels' }];
  assert.equal(summarizeReadiness(gates).allPassed, false);
  assert.deepEqual(summarizeReadiness(gates).pending, ['human']);
  assert.throws(() => summarizeReadiness([]));
  assert.throws(() => summarizeReadiness([gates[0], gates[0]]));
});
