import assert from 'node:assert/strict';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { BENCHMARK, SUITE } from '../storage';
import { getSpec, taskForV2 } from '../v2/cases';
import { STUDY } from './protocol';
import { auditItems } from './human-audit';
import { EVALUATOR_VERSION, evaluateStrict } from './strict-evaluate';
import { humanCalibration, resolveHumanDecisions, reviewedLabelsHash } from './human-calibration';
import { importAuditRecords, readAuditRecords, type AuditRecordKind } from './human-records';
import { imageEvidence } from './calibration-export';

const PRIVATE = resolve(BENCHMARK, '.runtime/study-human-audit');
const PUBLIC = resolve(STUDY, 'human-audit');
const CONTRACT = resolve(PUBLIC, 'calibration-contract.json');

function calibrationContext() {
  const packet = JSON.parse(readFileSync(resolve(PUBLIC, 'packet.json'), 'utf8'));
  const actual = auditItems();
  assert.equal(packet.version, 'human-audit-v2-1');
  assert.equal(packet.packetHash, digest(packet.items));
  assert.deepEqual(packet.items, actual, 'Review packet differs from current task inputs');
  const images = [...new Set(actual.flatMap(i => i.images))].sort();
  for (const path of images) {
    assert.match(path, /^images\/[a-f0-9]{64}\.png$/);
    assert.equal(imageEvidence(readFileSync(resolve(STUDY, 'inputs', path))).hash, path.slice(7, -4));
  }
  const automatic = actual.map(item => {
    const success = evaluateStrict(taskForV2(getSpec(item.caseId)), item.answer).metrics.success;
    assert.ok(success === 0 || success === 1, 'Automatic acceptance must be binary');
    return { itemId: item.id, accepted: success === 1 };
  });
  const items = actual.map(i => {
    const spec = getSpec(i.caseId);
    return { id: i.id, group: i.group, caseId: i.caseId, stratum: `${spec.kind}/${spec.variant}/${spec.condition}` };
  });
  const sources = ['study/strict-evaluate.ts', 'v2/evaluate.ts', 'geometry.ts', 'shared.ts',
    'research/tasks.ts', 'v2/dataset.ts', 'study/human-calibration.ts'];
  const contract = { version: 'human-calibration-contract-1', packetHash: packet.packetHash,
    evaluatorVersion: EVALUATOR_VERSION, automaticJudgmentsHash: digest(automatic),
    sourceHashes: Object.fromEntries(sources.map(path => [path, digest(readFileSync(resolve(SUITE, path), 'utf8'))])),
    items: items.length, sourceGroups: new Set(items.map(i => i.group)).size, imageFiles: images.length,
    endpoints: ['false-acceptance-given-human-reject', 'false-rejection-given-human-accept',
      'original-reviewer-pair-agreement', 'resolved-coverage'],
    resampling: { unit: 'source-group', seed: 731, samples: 1000 },
    scope: 'Frozen development-packet calibration, not full task/domain coverage or independent human evidence.' };
  return { items, automatic, packetHash: packet.packetHash as string, contract };
}

export function freezeHumanCalibration() {
  const context = calibrationContext();
  if (existsSync(CONTRACT)) assert.deepEqual(JSON.parse(readFileSync(CONTRACT, 'utf8')), context.contract,
    'Calibration contract changed; preserve existing evidence and create a new protocol version');
  else {
    const records = readAuditRecords(PRIVATE);
    assert.equal(records.labels.length + records.adjudications.length, 0, 'Freeze must precede review records');
    atomicJson(CONTRACT, context.contract);
  }
  return context.contract;
}

export function verifyHumanCalibration() {
  const context = calibrationContext();
  assert.deepEqual(JSON.parse(readFileSync(CONTRACT, 'utf8')), context.contract,
    'Frozen calibration inputs, judgments or sources changed');
  return { ...context.contract, verified: true, humanLabelsVerified: false, apiRequests: 0 };
}

export function importHumanReview(kind: AuditRecordKind, file: string) {
  assert.ok(file, 'A JSONL input file is required');
  verifyHumanCalibration();
  const context = calibrationContext();
  const raw = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(readFileSync(resolve(file)));
  return importAuditRecords(PRIVATE, kind, raw, records => {
    resolveHumanDecisions(context.items, records.labels, records.adjudications, context.packetHash);
  });
}

export function humanAdjudicationQueue() {
  verifyHumanCalibration();
  const context = calibrationContext(), records = readAuditRecords(PRIVATE);
  const { decisions } = resolveHumanDecisions(context.items, records.labels, records.adjudications, context.packetHash);
  const queue = decisions.filter(i => i.status === 'awaiting-adjudication').map(i => {
    const originals = records.labels.filter(l => l.itemId === i.id);
    return { itemId: i.id, packetHash: context.packetHash, reviewedLabelsHash: reviewedLabelsHash(originals),
      originalLabels: originals, instruction: 'A different human must inspect the packet and these original reviews. Preserve uncertainty and cite evidence; no automatic majority vote.' };
  });
  atomicJson(resolve(PRIVATE, 'adjudication-queue.json'), queue);
  return { queued: queue.length, privateOutput: 'benchmark/.runtime/study-human-audit/adjudication-queue.json' };
}

export function reportHumanCalibration() {
  verifyHumanCalibration();
  const context = calibrationContext(), records = readAuditRecords(PRIVATE);
  const analysis = humanCalibration(context.items, context.automatic, records.labels, records.adjudications, context.packetHash);
  const result = { ...analysis, inputBatchHashes: records.batches,
    contractHash: digest(context.contract), apiRequests: 0 };
  const path = resolve(PUBLIC, 'calibration.json');
  if (existsSync(path)) {
    const previous = JSON.parse(readFileSync(path, 'utf8'));
    assert.ok(previous.inputBatchHashes.every((hash: string) => records.batches.includes(hash)),
      'Private review batches missing or modified; refuse to erase published evidence');
  }
  const snapshot = resolve(PUBLIC, 'calibration-history', `${digest(result)}.json`);
  if (existsSync(snapshot)) assert.deepEqual(JSON.parse(readFileSync(snapshot, 'utf8')), result);
  else atomicJson(snapshot, result);
  atomicJson(path, result);
  const m = result.overall;
  const rate = (r: typeof m.falseAcceptance) => r.rate === null ? 'N/A (no denominator)'
    : `${r.numerator}/${r.denominator} (${(100 * r.rate).toFixed(1)}%); source CI ${
      r.interval ? `[${r.interval.low.toFixed(3)}, ${r.interval.high.toFixed(3)}]` : 'N/A'}`;
  writeFileSync(resolve(PUBLIC, 'CALIBRATION.md'), `# Human Metric Calibration\n\n` +
    `Submitted labels: ${result.submissions}; reviewers: ${result.reviewers}; adjudications: ${result.adjudications}.\n` +
    `Resolved: ${m.resolved}/${m.queued}; source groups: ${m.sourceGroups}. Independently verified identity: no.\n\n` +
    '| Endpoint | Result |\n| --- | --- |\n' +
    `| False acceptance / human reject | ${rate(m.falseAcceptance)} |\n` +
    `| False rejection / human accept | ${rate(m.falseRejection)} |\n` +
    `| Original pair agreement, including uncertainty | ${rate(m.agreementAllJudgments)} |\n` +
    `| Original pair agreement, binary only | ${rate(m.agreementBinaryOnly)} |\n\n` +
    'No-denominator rates are unavailable, never zero. Original labels and adjudication notes remain private; ' +
    'hashes identify ingested batches but do not authenticate humans. Readiness remains separate from ingestion success.\n\n' +
    result.limitations.map(l => `- ${l}`).join('\n') + '\n');
  return result;
}
