import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { BENCHMARK } from '../storage';
import { taskForV2 } from '../v2/cases';
import { STUDY, selection } from './protocol';
import { evaluateStrict } from './strict-evaluate';
import { copyInputAnswer } from './model-validation-report';
import type { PublicTask } from '../shared';
import { readAuditRecords } from './human-records';

export interface AuditItem {
  id: string; caseId: string; group: string; publicInput: PublicTask;
  answer: unknown; reference: unknown; images: string[];
}
export interface AuditLabel {
  itemId: string; reviewerCode: string; packetHash: string; judgment: 'accept' | 'reject' | 'uncertain';
  independent: true; humanAttested: true; notes: string;
}

export function auditItems(): AuditItem[] {
  const specs = selection(), prepared = JSON.parse(readFileSync(resolve(STUDY, 'inputs/prepared.json'), 'utf8'));
  const policies = [...new Set(specs.filter(s => s.kind !== 'parts').map(s => s.policy))].sort();
  const rows = policies.flatMap(policy => ['relations', 'reconstruct', 'complete', 'edit', 'plan', 'repair'].flatMap(kind => {
    const spec = specs.find(s => s.policy === policy && s.kind === kind)!;
    const task = taskForV2(spec), candidate = copyInputAnswer(task.public);
    const altered: any = structuredClone(task.oracle);
    if (kind === 'relations') altered.connected = !altered.connected;
    else if (kind === 'plan') altered.order = altered.order.slice(1);
    else {
      const structure = kind === 'repair' ? altered.structure : altered;
      structure.parts[0].color = structure.parts[0].color === 'blue' ? 'red' : 'blue';
    }
    return [task.oracle, candidate ?? altered].map((answer, variant) => ({
      id: digest({ version: 'human-audit-v2-1', caseId: spec.id, variant }).slice(0, 24),
      caseId: spec.id, group: spec.group, publicInput: task.public,
      answer, reference: task.oracle, images: prepared.find((p: any) => p.spec.id === spec.id).images,
    }));
  }));
  assert.equal(rows.length, 96);
  return rows.sort((a, b) => a.id.localeCompare(b.id));
}

export function summarizeAudit(items: Pick<AuditItem, 'id'>[], labels: AuditLabel[], packetHash: string) {
  assert.ok(items.length > 0 && new Set(items.map(i => i.id)).size === items.length, 'Unique nonempty packet required');
  const validIds = new Set(items.map(i => i.id)), seen = new Set<string>();
  for (const label of labels) {
    assert.ok(label && typeof label === 'object' && !Array.isArray(label), 'Invalid review label');
    assert.ok(validIds.has(label.itemId), 'Unknown review item');
    assert.equal(label.packetHash, packetHash, 'Review is for a different packet');
    assert.match(label.reviewerCode, /^[A-Za-z0-9_-]{3,40}$/);
    assert.ok(['accept', 'reject', 'uncertain'].includes(label.judgment));
    assert.equal(label.independent, true); assert.equal(label.humanAttested, true);
    assert.ok(typeof label.notes === 'string' && label.notes.trim().length >= 8);
    const key = `${label.itemId}:${label.reviewerCode}`; assert.ok(!seen.has(key), 'Duplicate reviewer/item'); seen.add(key);
  }
  const perItem = items.map(item => {
    const rs = labels.filter(l => l.itemId === item.id);
    const judgments = [...new Set(rs.map(l => l.judgment))];
    return { itemId: item.id, reviewers: rs.length, doubleReviewed: rs.length >= 2,
      requiresAdjudication: rs.length >= 2 && (judgments.length > 1 || judgments.includes('uncertain')),
      consensus: rs.length >= 2 && judgments.length === 1 && judgments[0] !== 'uncertain' ? judgments[0] : null };
  });
  return { version: 'human-audit-v2-1', packetHash, queued: items.length, submissions: labels.length,
    reviewers: new Set(labels.map(l => l.reviewerCode)).size,
    doubleReviewed: perItem.filter(r => r.doubleReviewed).length,
    consensusItems: perItem.filter(r => r.consensus).length,
    requiresAdjudication: perItem.filter(r => r.requiresAdjudication).length,
    completeConsensus: items.length > 0 && perItem.every(r => r.consensus),
    perItem, independenceVerifiedExternally: false,
    scope: 'Self-attested independent human labels, not authenticated reviewer identity. Disagreement is never resolved by majority vote automatically.' };
}
export function prepareHumanAudit() {
  const items = auditItems(), packetHash = digest(items);
  const packet = { version: 'human-audit-v2-1', packetHash, items,
    instruction: 'Two independent reviewers label acceptance under the declared public task and reference. A reference may be only one valid answer. Review images from ../inputs/. Do not consult automatic scores before submitting labels. Record uncertainty and reasons.',
    outputSchema: { itemId: 'one packet item', packetHash, reviewerCode: 'pseudonym',
      judgment: 'accept|reject|uncertain', independent: true, humanAttested: true, notes: 'specific explanation, at least eight characters' },
    limitations: ['Scores and candidate sources are omitted; public source code can unblind this development packet.',
      '96 candidates from 48 task cases, not 96 independent source objects.',
      'Not representative of external semantic data, physical validity or all generator policies/variants.'] };
  const path = resolve(STUDY, 'human-audit/packet.json');
  if (existsSync(path)) assert.deepEqual(JSON.parse(readFileSync(path, 'utf8')), packet);
  atomicJson(path, packet);
  // Private judge key is not part of the public reviewer packet.
  const specs = new Map(selection().map(s => [s.id, s]));
  atomicJson(resolve(BENCHMARK, '.runtime/study-human-audit/judge-key.json'),
    items.map(i => ({ id: i.id, verdict: evaluateStrict(taskForV2(specs.get(i.caseId)!), i.answer) })));
  return { candidates: items.length, cases: new Set(items.map(i => i.caseId)).size,
    sourceGroups: new Set(items.map(i => i.group)).size, packetHash };
}
export function humanAuditStatus() {
  const items = auditItems(), packetHash = digest(items);
  const { labels } = readAuditRecords(resolve(BENCHMARK, '.runtime/study-human-audit'));
  const status = summarizeAudit(items, labels, packetHash);
  const path = resolve(STUDY, 'human-audit/status.json');
  if (existsSync(path)) assert.ok(JSON.parse(readFileSync(path, 'utf8')).submissions <= status.submissions,
    'Private review labels missing; refuse to erase published status');
  atomicJson(path, status);
  return status;
}
