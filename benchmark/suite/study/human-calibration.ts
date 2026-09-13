import assert from 'node:assert/strict';
import { digest } from '../data';
import { random } from '../v2/dataset';
import { summarizeAudit, type AuditItem, type AuditLabel } from './human-audit';

export interface Adjudication {
  version: 'human-adjudication-1';
  packetHash: string;
  itemId: string;
  reviewedLabelsHash: string;
  adjudicatorCode: string;
  judgment: 'accept' | 'reject' | 'uncertain';
  humanAttested: true;
  independent: true;
  notes: string;
  evidence: string;
}
export interface AutomaticJudgment { itemId: string; accepted: boolean }
export interface CalibrationItem extends Pick<AuditItem, 'id' | 'caseId' | 'group'> { stratum: string }

export function reviewedLabelsHash(labels: AuditLabel[]) {
  return digest([...labels].sort((a, b) => a.reviewerCode.localeCompare(b.reviewerCode)).map(l => ({
    itemId: l.itemId, reviewerCode: l.reviewerCode, packetHash: l.packetHash,
    judgment: l.judgment, independent: l.independent, humanAttested: l.humanAttested, notes: l.notes,
  })));
}

export function resolveHumanDecisions(items: CalibrationItem[], labels: AuditLabel[],
  adjudications: Adjudication[], packetHash: string) {
  assert.ok(items.length > 0 && new Set(items.map(i => i.id)).size === items.length, 'Unique nonempty packet required');
  assert.ok(items.every(i => [i.id, i.group, i.caseId, i.stratum].every(v => typeof v === 'string' && v.length > 0)));
  const audit = summarizeAudit(items, labels, packetHash), byItem = new Map(audit.perItem.map(i => [i.itemId, i]));
  const adjudicated = new Map<string, Adjudication>();
  for (const record of adjudications) {
    assert.ok(record && typeof record === 'object' && !Array.isArray(record), 'Invalid adjudication');
    assert.equal(record.version, 'human-adjudication-1');
    assert.equal(record.packetHash, packetHash, 'Adjudication packet mismatch');
    const item = byItem.get(record.itemId), originals = labels.filter(l => l.itemId === record.itemId);
    assert.ok(item?.requiresAdjudication, 'Adjudication requires conflicting or uncertain double review');
    assert.ok(!adjudicated.has(record.itemId), 'Duplicate adjudication; use a new version for corrections');
    assert.equal(record.reviewedLabelsHash, reviewedLabelsHash(originals), 'Stale adjudication label hash');
    assert.match(record.adjudicatorCode, /^[A-Za-z0-9_-]{3,40}$/);
    assert.ok(originals.every(l => l.reviewerCode !== record.adjudicatorCode), 'Reviewer cannot adjudicate own item');
    assert.ok(['accept', 'reject', 'uncertain'].includes(record.judgment));
    assert.equal(record.humanAttested, true); assert.equal(record.independent, true);
    assert.ok(typeof record.notes === 'string' && record.notes.trim().length >= 8);
    assert.ok(typeof record.evidence === 'string' && record.evidence.trim().length >= 8);
    adjudicated.set(record.itemId, record);
  }
  const decisions = items.map(item => {
    const review = byItem.get(item.id)!, adjudication = adjudicated.get(item.id);
    const judgment = adjudication?.judgment ?? review.consensus;
    return { ...item, reviewers: review.reviewers,
      status: !review.reviewers ? 'unreviewed' : !review.doubleReviewed ? 'single-review'
        : adjudication ? adjudication.judgment === 'uncertain' ? 'adjudicated-uncertain' : 'adjudicated'
          : review.consensus ? 'consensus' : 'awaiting-adjudication',
      judgment: judgment === 'accept' || judgment === 'reject' ? judgment : null };
  });
  return { audit, decisions };
}

interface Counts { numerator: number; denominator: number }
export function sourceRatio(groups: Counts[], seed = 731, resamples = 1000) {
  assert.ok(Number.isInteger(resamples) && resamples > 0);
  assert.ok(groups.every(g => Number.isInteger(g.numerator) && Number.isInteger(g.denominator)
    && g.numerator >= 0 && g.denominator >= g.numerator));
  const numerator = groups.reduce((n, g) => n + g.numerator, 0);
  const denominator = groups.reduce((n, g) => n + g.denominator, 0);
  const contributingGroups = groups.filter(g => g.denominator > 0).length;
  const rng = random(seed);
  const samples: number[] = [];
  let undefinedResamples = 0;
  if (contributingGroups >= 2) {
    // Resample whole sources, preserving all candidate/variant rows and their denominators.
    for (let i = 0; i < resamples; i++) {
      let n = 0, d = 0;
      for (let j = 0; j < groups.length; j++) {
        const g = groups[Math.floor(rng() * groups.length)]; n += g.numerator; d += g.denominator;
      }
      if (d) samples.push(n / d); else undefinedResamples++;
    }
    samples.sort((a, b) => a - b);
  }
  return { numerator, denominator, rate: denominator ? numerator / denominator : null,
    sourceGroups: groups.length, contributingGroups, seed, requestedResamples: resamples,
    validResamples: samples.length, undefinedResamples,
    interval: samples.length >= 2 ? {
      low: samples[Math.floor((samples.length - 1) * 0.025)],
      high: samples[Math.ceil((samples.length - 1) * 0.975)],
    } : null,
    limitation: 'Conditional empirical source bootstrap, not a population guarantee. A degenerate zero-error interval is not proof of zero error. Fewer than two contributing sources has no interval.' };
}

export function humanCalibration(items: CalibrationItem[], automatic: AutomaticJudgment[],
  labels: AuditLabel[], adjudications: Adjudication[], packetHash: string) {
  const { audit, decisions } = resolveHumanDecisions(items, labels, adjudications, packetHash);
  assert.equal(automatic.length, items.length, 'Automatic judgment coverage mismatch');
  const auto = new Map(automatic.map(a => [a.itemId, a.accepted]));
  assert.equal(auto.size, items.length, 'Duplicate automatic judgment');
  assert.ok(items.every(i => typeof auto.get(i.id) === 'boolean'), 'Missing or nonboolean automatic judgment');
  const aggregate = (selected: typeof decisions) => {
    const groups = [...new Set(selected.map(i => i.group))].sort();
    const resolved = selected.filter(i => i.judgment !== null);
    const pairRows = selected.map(i => {
      const ls = labels.filter(l => l.itemId === i.id);
      const counts = { allPairs: 0, agreeingPairs: 0, binaryPairs: 0, binaryAgreeingPairs: 0 };
      for (let a = 0; a < ls.length; a++) for (let b = a + 1; b < ls.length; b++) {
        counts.allPairs++; counts.agreeingPairs += Number(ls[a].judgment === ls[b].judgment);
        if (ls[a].judgment !== 'uncertain' && ls[b].judgment !== 'uncertain') {
          counts.binaryPairs++; counts.binaryAgreeingPairs += Number(ls[a].judgment === ls[b].judgment);
        }
      }
      return { group: i.group, ...counts };
    });
    const metric = (den: (i: typeof decisions[number]) => boolean, num: (i: typeof decisions[number]) => boolean) =>
      sourceRatio(groups.map(group => {
        const rows = resolved.filter(i => i.group === group && den(i));
        return { denominator: rows.length, numerator: rows.filter(num).length };
      }));
    const agreement = (binary: boolean) => sourceRatio(groups.map(group => {
      const pairs = pairRows.filter(p => p.group === group);
      return { numerator: pairs.reduce((n, p) => n + (binary ? p.binaryAgreeingPairs : p.agreeingPairs), 0),
        denominator: pairs.reduce((n, p) => n + (binary ? p.binaryPairs : p.allPairs), 0) };
    }));
    return { queued: selected.length, sourceGroups: groups.length, resolved: resolved.length,
      coverage: selected.length ? resolved.length / selected.length : null,
      statuses: Object.fromEntries(['unreviewed', 'single-review', 'consensus', 'awaiting-adjudication', 'adjudicated', 'adjudicated-uncertain']
        .map(status => [status, selected.filter(i => i.status === status).length])),
      confusion: {
        humanAcceptAutoAccept: resolved.filter(i => i.judgment === 'accept' && auto.get(i.id)).length,
        humanAcceptAutoReject: resolved.filter(i => i.judgment === 'accept' && !auto.get(i.id)).length,
        humanRejectAutoAccept: resolved.filter(i => i.judgment === 'reject' && auto.get(i.id)).length,
        humanRejectAutoReject: resolved.filter(i => i.judgment === 'reject' && !auto.get(i.id)).length,
      },
      falseAcceptance: metric(i => i.judgment === 'reject', i => auto.get(i.id)!),
      falseRejection: metric(i => i.judgment === 'accept', i => !auto.get(i.id)),
      disagreement: metric(() => true, i => auto.get(i.id) !== (i.judgment === 'accept')),
      agreementAllJudgments: agreement(false), agreementBinaryOnly: agreement(true),
      uncertainLabels: labels.filter(l => selected.some(i => i.id === l.itemId) && l.judgment === 'uncertain').length };
  };
  const overall = aggregate(decisions);
  return { version: 'human-calibration-1', packetHash, submissions: labels.length,
    reviewers: audit.reviewers, adjudications: adjudications.length,
    independenceVerifiedExternally: false, allItemsResolved: overall.resolved === items.length,
    overall, strata: [...new Set(items.map(i => i.stratum))].sort().map(stratum =>
      ({ stratum, ...aggregate(decisions.filter(i => i.stratum === stratum)) })),
    limitations: ['Self-attestations and hashes do not verify human identity or independence.',
      'Rates condition on resolved human labels; unreviewed, single-review and uncertain items remain in coverage denominators.',
      'False acceptance is auto-accept / human-reject; false rejection is auto-reject / human-accept.',
      'Reviewer agreement uses original labels before adjudication; all-judgment agreement includes uncertain/uncertain pairs.',
      'Sources, not candidates, tasks, reviewers or model counts, are bootstrap units. Pairwise agreement is not chance-corrected kappa.',
      'No identities, private notes or adjudication evidence text are included in this aggregate report.'] };
}
