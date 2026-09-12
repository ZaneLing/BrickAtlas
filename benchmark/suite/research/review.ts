import { appendFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { digest } from '../data';
import { BENCHMARK } from '../storage';
import { researchModels, RULES } from './dataset';

export interface HumanReview {
  sampleId: string; reviewer: string; judgment: 'acceptable' | 'problem' | 'uncertain';
  notes: string; independent: boolean; acknowledged: true; submittedAt: string;
}
export function reviewQueue() {
  const records = researchModels(), result = [];
  const buckets = RULES.map(family => records.filter(m => m.family === family)
    .sort((a, b) => digest(a.group + 'review').localeCompare(digest(b.group + 'review'))));
  for (let n = 0; result.length < 200; n++) for (const bucket of buckets) {
    if (result.length < 200 && bucket[n]) result.push(bucket[n]);
  }
  return result;
}
export function loadReviews(root = resolve(BENCHMARK, '.runtime/human-review')): HumanReview[] {
  const path = resolve(root, 'reviews.jsonl');
  return existsSync(path) ? readFileSync(path, 'utf8').split('\n').filter(Boolean).map(line => JSON.parse(line)) : [];
}
export function submitReview(input: unknown, root = resolve(BENCHMARK, '.runtime/human-review')) {
  const row = input as Partial<HumanReview>;
  if (!row || !reviewQueue().some(m => m.id === row.sampleId)
    || typeof row.reviewer !== 'string' || !/^[A-Za-z0-9_-]{3,40}$/.test(row.reviewer)
    || !['acceptable', 'problem', 'uncertain'].includes(row.judgment ?? '')
    || typeof row.notes !== 'string' || row.notes.trim().length < 8 || row.notes.length > 4000
    || typeof row.independent !== 'boolean' || row.acknowledged !== true) throw new Error('Complete a real review, notes and explicit acknowledgement');
  const records = loadReviews(root);
  if (records.some(r => r.sampleId === row.sampleId && r.reviewer === row.reviewer)) throw new Error('This reviewer already submitted this sample');
  const result: HumanReview = { sampleId: row.sampleId!, reviewer: row.reviewer,
    judgment: row.judgment!, notes: row.notes.trim(), independent: row.independent,
    acknowledged: true, submittedAt: new Date().toISOString() };
  mkdirSync(root, { recursive: true });
  appendFileSync(resolve(root, 'reviews.jsonl'), JSON.stringify(result) + '\n', { mode: 0o600 });
  return result;
}
export function reviewSummary() {
  const records = loadReviews(), samples = new Set(records.map(r => r.sampleId));
  let doubleReviewed = 0, disagreements = 0;
  for (const sample of samples) {
    const rows = records.filter(r => r.sampleId === sample && r.independent);
    if (new Set(rows.map(r => r.reviewer)).size >= 2) {
      doubleReviewed++;
      if (new Set(rows.map(r => r.judgment)).size > 1) disagreements++;
    }
  }
  return { queued: reviewQueue().length, submissions: records.length, reviewedSamples: samples.size,
    doubleReviewed, disagreements, independentReviewers: new Set(records.filter(r => r.independent).map(r => r.reviewer)).size,
    attestation: 'Self-declared independence, not verified identity. No automatic annotations counted as humans.' };
}
