import type { Task } from './types';

export const REVIEW_STORAGE_KEY = 'brickatlas:hierarchy3:reviews:v1';
export const REVIEW_SCHEMA_VERSION = 1;
export const BENCHMARK_VERSION = 'brickatlas-hierarchy-3';

export type ReviewDecision = 'pass' | 'fail';

export interface ReviewRecord {
  taskId: string;
  modelId: string;
  difficulty: string;
  layer: Task['layer'];
  family: string;
  title: string;
  decision: ReviewDecision;
  reason: string;
  reviewedAt: string;
  benchmarkVersion: typeof BENCHMARK_VERSION;
}

export interface ReviewBatch {
  schemaVersion: typeof REVIEW_SCHEMA_VERSION;
  benchmarkVersion: typeof BENCHMARK_VERSION;
  batchId: string;
  exportedAt: string;
  summary: {
    totalTasks: number;
    reviewed: number;
    passed: number;
    failed: number;
    pending: number;
  };
  records: ReviewRecord[];
}

type StorageLike = Pick<Storage, 'getItem' | 'setItem' | 'removeItem'>;
const validLayer = new Set<Task['layer']>(['atomic', 'metacognitive', 'procedural', 'integrative']);

function browserStorage(): StorageLike | null {
  try { return typeof localStorage === 'undefined' ? null : localStorage; } catch { return null; }
}

function validRecord(value: unknown): value is ReviewRecord {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false;
  const row = value as Partial<ReviewRecord>;
  return typeof row.taskId === 'string' && row.taskId.startsWith('h3-')
    && typeof row.modelId === 'string' && !!row.modelId
    && typeof row.difficulty === 'string'
    && validLayer.has(row.layer as Task['layer'])
    && typeof row.family === 'string' && typeof row.title === 'string'
    && (row.decision === 'pass' || row.decision === 'fail')
    && typeof row.reason === 'string'
    && (row.decision !== 'fail' || !!row.reason.trim())
    && typeof row.reviewedAt === 'string' && Number.isFinite(Date.parse(row.reviewedAt))
    && row.benchmarkVersion === BENCHMARK_VERSION;
}

export function loadReviews(storage: StorageLike | null = browserStorage()) {
  const records: Record<string, ReviewRecord> = {};
  if (!storage) return records;
  try {
    const value = JSON.parse(storage.getItem(REVIEW_STORAGE_KEY) ?? '[]');
    if (!Array.isArray(value)) return records;
    for (const row of value) if (validRecord(row)) records[row.taskId] = row;
  } catch { /* Corrupt local drafts fail closed. */ }
  return records;
}

export function storeReviews(records: Record<string, ReviewRecord>, storage: StorageLike | null = browserStorage()) {
  if (!storage) return;
  const rows = Object.values(records).filter(validRecord).sort((a, b) => a.taskId.localeCompare(b.taskId));
  storage.setItem(REVIEW_STORAGE_KEY, JSON.stringify(rows));
}

export function reviewTask(task: Task, decision: ReviewDecision, reason: string, reviewedAt = new Date().toISOString()) {
  if (decision === 'fail' && !reason.trim()) throw new Error('不通过时必须填写理由');
  const record: ReviewRecord = {
    taskId: task.id,
    modelId: task.modelId,
    difficulty: task.difficulty,
    layer: task.layer,
    family: task.family,
    title: task.title,
    decision,
    reason: reason.trim(),
    reviewedAt,
    benchmarkVersion: BENCHMARK_VERSION,
  };
  if (!validRecord(record)) throw new Error('审核记录格式无效');
  return record;
}

export function removeReview(taskId: string, storage: StorageLike | null = browserStorage()) {
  const records = loadReviews(storage);
  delete records[taskId];
  storeReviews(records, storage);
  return records;
}

export function saveReview(record: ReviewRecord, storage: StorageLike | null = browserStorage()) {
  if (!validRecord(record)) throw new Error('审核记录格式无效');
  const records = loadReviews(storage);
  records[record.taskId] = record;
  storeReviews(records, storage);
  return records;
}

export function createReviewBatch(records: Record<string, ReviewRecord>, totalTasks: number, now = new Date()) {
  const rows = Object.values(records).filter(validRecord).sort((a, b) =>
    a.difficulty.localeCompare(b.difficulty) || a.modelId.localeCompare(b.modelId)
      || a.layer.localeCompare(b.layer) || a.taskId.localeCompare(b.taskId));
  const passed = rows.filter(row => row.decision === 'pass').length;
  const failed = rows.length - passed;
  const stamp = now.toISOString();
  return {
    schemaVersion: REVIEW_SCHEMA_VERSION,
    benchmarkVersion: BENCHMARK_VERSION,
    batchId: `hierarchy3-review-${stamp.replaceAll(':', '-').replace(/\.\d{3}Z$/, 'Z')}`,
    exportedAt: stamp,
    summary: { totalTasks, reviewed: rows.length, passed, failed, pending: Math.max(0, totalTasks - rows.length) },
    records: rows,
  } satisfies ReviewBatch;
}

export function importReviewBatch(raw: string, storage: StorageLike | null = browserStorage()) {
  let value: unknown;
  try { value = JSON.parse(raw); } catch { throw new Error('审核文件不是有效 JSON'); }
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('审核文件格式无效');
  const batch = value as Partial<ReviewBatch>;
  if (batch.schemaVersion !== REVIEW_SCHEMA_VERSION || batch.benchmarkVersion !== BENCHMARK_VERSION
    || !Array.isArray(batch.records)) throw new Error('审核文件版本不匹配');
  if (!batch.records.every(validRecord)) throw new Error('审核文件包含无效记录');
  const records = loadReviews(storage);
  for (const row of batch.records) {
    const previous = records[row.taskId];
    if (!previous || Date.parse(row.reviewedAt) >= Date.parse(previous.reviewedAt)) records[row.taskId] = row;
  }
  storeReviews(records, storage);
  return records;
}

export function clearReviews(storage: StorageLike | null = browserStorage()) {
  storage?.removeItem(REVIEW_STORAGE_KEY);
  return {} as Record<string, ReviewRecord>;
}
