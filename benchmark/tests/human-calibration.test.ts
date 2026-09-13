import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { humanCalibration, resolveHumanDecisions, reviewedLabelsHash, sourceRatio,
  type Adjudication, type CalibrationItem } from '../suite/study/human-calibration';
import { importAuditRecords, readAuditRecords, type AuditRecords } from '../suite/study/human-records';
import { summarizeAudit, type AuditLabel } from '../suite/study/human-audit';
import { verifyHumanCalibration } from '../suite/study/human-calibration-run';

// Synthetic unit fixtures only; never imported into the real reviewer store.
const packetHash = 'synthetic-unit-packet';
const items: CalibrationItem[] = ['a', 'b', 'c', 'd'].map((id, i) =>
  ({ id, caseId: `case-${id}`, group: i === 3 ? 'source-2' : 'source-1', stratum: i < 2 ? 'edit' : 'repair' }));
function label(itemId: string, reviewerCode: string, judgment: AuditLabel['judgment']): AuditLabel {
  return { itemId, reviewerCode, judgment, packetHash, independent: true, humanAttested: true,
    notes: 'SYNTHETIC unit fixture, not actual human evidence' };
}
const pair = (id: string, judgment: AuditLabel['judgment']) => [label(id, 'test_a', judgment), label(id, 'test_b', judgment)];
function adjudication(originals: AuditLabel[], judgment: Adjudication['judgment'] = 'reject'): Adjudication {
  return { version: 'human-adjudication-1', packetHash, itemId: originals[0].itemId,
    reviewedLabelsHash: reviewedLabelsHash(originals), adjudicatorCode: 'test_c', judgment,
    independent: true, humanAttested: true, notes: 'SYNTHETIC reason fixture', evidence: 'SYNTHETIC reference fixture' };
}
const automatic = items.map(i => ({ itemId: i.id, accepted: i.id !== 'd' }));

test('frozen real review reference verifies inputs and images without claiming human judgments', () => {
  const reference = verifyHumanCalibration();
  assert.equal(reference.items, 96); assert.equal(reference.sourceGroups, 8);
  assert.equal(reference.imageFiles, 32); assert.equal(reference.verified, true);
  assert.equal(reference.humanLabelsVerified, false); assert.equal(reference.apiRequests, 0);
});

test('no human labels means missing rates, not perfect metric validity', () => {
  const report = humanCalibration(items, automatic, [], [], packetHash);
  assert.equal(report.overall.coverage, 0); assert.equal(report.overall.resolved, 0);
  assert.equal(report.overall.falseAcceptance.rate, null); assert.equal(report.overall.falseRejection.rate, null);
  assert.equal(report.overall.agreementAllJudgments.rate, null);
  assert.equal(report.overall.falseAcceptance.interval, null);
  assert.equal(report.allItemsResolved, false); assert.equal(report.independenceVerifiedExternally, false);
});

test('source bootstrap preserves all candidate counts instead of treating each as an object', () => {
  const labels = items.flatMap(i => pair(i.id, 'reject'));
  const report = humanCalibration(items, automatic, labels, [], packetHash);
  assert.equal(report.overall.falseAcceptance.numerator, 3);
  assert.equal(report.overall.falseAcceptance.denominator, 4);
  assert.equal(report.overall.falseAcceptance.rate, 0.75);
  assert.equal(report.overall.falseAcceptance.sourceGroups, 2);
  assert.equal(report.overall.falseRejection.rate, null);
  assert.equal(report.overall.agreementAllJudgments.rate, 1);
  assert.equal(report.strata.length, 2);
  assert.deepEqual(humanCalibration(items, automatic, [...labels].reverse(), [], packetHash), report);
  assert.equal(sourceRatio([{ numerator: 0, denominator: 1000 }]).interval, null);
  assert.equal(sourceRatio([{ numerator: 0, denominator: 1000 }]).contributingGroups, 1);
});

test('calibration confusion matrix has the declared human-reference error directions', () => {
  const labels = [...pair('a', 'reject'), ...pair('b', 'accept'), ...pair('c', 'reject'), ...pair('d', 'accept')];
  const report = humanCalibration(items, automatic, labels, [], packetHash);
  assert.deepEqual(report.overall.confusion, { humanAcceptAutoAccept: 1, humanAcceptAutoReject: 1,
    humanRejectAutoAccept: 2, humanRejectAutoReject: 0 });
  assert.equal(report.overall.falseAcceptance.rate, 1);
  assert.equal(report.overall.falseRejection.rate, 0.5);
  assert.equal(report.overall.disagreement.rate, 0.75);
});

test('adjudication resolves disagreement without rewriting original agreement', () => {
  const labels = [label('a', 'test_a', 'accept'), label('a', 'test_b', 'reject')];
  const before = structuredClone(labels);
  const report = humanCalibration(items, automatic, labels, [adjudication(labels)], packetHash);
  assert.equal(report.overall.resolved, 1); assert.equal(report.overall.falseAcceptance.rate, 1);
  assert.equal(report.overall.agreementAllJudgments.rate, 0);
  assert.equal(report.overall.statuses.adjudicated, 1);
  assert.equal(report.overall.statuses.unreviewed, 3);
  assert.deepEqual(labels, before); assert.equal(report.allItemsResolved, false);
  const raw = JSON.stringify(report);
  assert.ok(!raw.includes('test_a') && !raw.includes('SYNTHETIC reason') && !raw.includes('SYNTHETIC reference'));
});

test('uncertainty, single reviews and unresolved disagreement never become binary truth', () => {
  const labels = [...pair('a', 'uncertain'), label('b', 'test_a', 'accept'),
    label('c', 'test_a', 'accept'), label('c', 'test_b', 'uncertain')];
  const uncertain = adjudication(labels.filter(l => l.itemId === 'a'), 'uncertain');
  const report = humanCalibration(items, automatic, labels, [uncertain], packetHash);
  assert.equal(report.overall.resolved, 0);
  assert.equal(report.overall.statuses['adjudicated-uncertain'], 1);
  assert.equal(report.overall.statuses['single-review'], 1);
  assert.equal(report.overall.statuses['awaiting-adjudication'], 1);
  assert.equal(report.overall.uncertainLabels, 3);
  assert.equal(report.overall.agreementAllJudgments.rate, 0.5);
  assert.equal(report.overall.agreementBinaryOnly.rate, null);
});

test('adjudications reject wrong packet, stale labels, self-review and duplicate decisions', () => {
  const labels = [label('a', 'test_a', 'accept'), label('a', 'test_b', 'reject')];
  const record = adjudication(labels);
  assert.equal(reviewedLabelsHash([...labels].reverse()), record.reviewedLabelsHash);
  const check = (r: Adjudication[]) => resolveHumanDecisions(items, labels, r, packetHash);
  assert.throws(() => check([{ ...record, packetHash: 'wrong' }]), /packet/);
  assert.throws(() => check([{ ...record, reviewedLabelsHash: 'wrong' }]), /Stale/);
  assert.throws(() => check([{ ...record, adjudicatorCode: 'test_a' }]), /own item/);
  assert.throws(() => check([record, record]), /Duplicate adjudication/);
  assert.throws(() => check([{ ...record, humanAttested: false } as any]));
  assert.throws(() => check([{ ...record, evidence: '' }]));
  assert.throws(() => resolveHumanDecisions(items, pair('a', 'accept'), [record], packetHash), /conflicting/);
  assert.throws(() => resolveHumanDecisions(items, [labels[0]], [record], packetHash), /double review/);
  assert.throws(() => resolveHumanDecisions(items, [...labels, label('a', 'test_d', 'reject')], [record], packetHash), /Stale/);
});

test('empty or malformed calibration identities and automatic coverage fail closed', () => {
  assert.throws(() => humanCalibration([], [], [], [], packetHash), /nonempty/);
  assert.throws(() => humanCalibration([items[0], items[0]], automatic, [], [], packetHash), /Unique/);
  assert.throws(() => humanCalibration(items, automatic.slice(1), [], [], packetHash), /coverage/);
  assert.throws(() => humanCalibration(items, [...automatic.slice(1), automatic[1]], [], [], packetHash), /Duplicate/);
  assert.throws(() => humanCalibration(items, automatic.map(i => ({ ...i, accepted: 1 } as any)), [], [], packetHash), /nonboolean/);
  assert.throws(() => summarizeAudit(items, [null] as any, packetHash), /Invalid review label/);
  assert.throws(() => sourceRatio([{ numerator: 2, denominator: 1 }]));
});

test('review imports are atomic, immutable and idempotent without leaking private notes', () => {
  const dir = mkdtempSync(resolve(tmpdir(), 'brick-human-unit-'));
  const validate = (r: AuditRecords) => { resolveHumanDecisions(items, r.labels, r.adjudications, packetHash); };
  try {
    const raw = '\uFEFF' + pair('a', 'reject').map(l => JSON.stringify(l)).join('\r\n') + '\r\n';
    const first = importAuditRecords(dir, 'labels', raw, validate);
    assert.equal(first.imported, true);
    const file = resolve(dir, 'batches', `${first.batchHash}.json`), bytes = readFileSync(file, 'utf8');
    assert.equal(JSON.parse(bytes).raw, raw);
    assert.equal(importAuditRecords(dir, 'labels', raw, validate).imported, false);
    assert.equal(readAuditRecords(dir).labels.length, 2);
    assert.throws(() => importAuditRecords(dir, 'labels', raw.trim(), validate), /Duplicate/);
    assert.throws(() => importAuditRecords(dir, 'labels', '{"notes":"private broken line"', validate), /line 1/);
    assert.equal(readFileSync(file, 'utf8'), bytes);
    assert.equal(readdirSync(resolve(dir, 'batches')).length, 1);
    writeFileSync(file, bytes.replace('SYNTHETIC', 'TAMPERED'));
    assert.throws(() => readAuditRecords(dir), /integrity/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('imports preserve originals across adjudication and refuse stale or concurrent changes', () => {
  const dir = mkdtempSync(resolve(tmpdir(), 'brick-human-unit-'));
  const validate = (r: AuditRecords) => { resolveHumanDecisions(items, r.labels, r.adjudications, packetHash); };
  const labels = [label('a', 'test_a', 'accept'), label('a', 'test_b', 'reject')];
  try {
    importAuditRecords(dir, 'labels', labels.map(l => JSON.stringify(l)).join('\n'), validate);
    const record = adjudication(labels);
    importAuditRecords(dir, 'adjudications', JSON.stringify(record), validate);
    const before = readAuditRecords(dir);
    assert.throws(() => importAuditRecords(dir, 'labels', JSON.stringify(label('a', 'test_d', 'reject')), validate), /Stale/);
    assert.deepEqual(readAuditRecords(dir), before);
    writeFileSync(resolve(dir, 'import.lock'), 'synthetic lock');
    assert.throws(() => importAuditRecords(dir, 'labels', JSON.stringify(label('b', 'test_a', 'accept')), validate), /EEXIST/);
    assert.deepEqual(readAuditRecords(dir), before);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
