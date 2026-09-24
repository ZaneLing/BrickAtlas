import type { LDrawTask } from './ldrawTypes';
export const LDRAW_REVIEW_KEY = 'brickatlas:ldraw1:reviews:v1';
const VERSION = 'brickatlas-ldraw-1';
export interface LDrawReview {
  taskId: string; modelId: string; sourceHash: string; decision: 'pass' | 'fail';
  reason: string; reviewedAt: string; benchmarkVersion: typeof VERSION;
  difficulty: string; title: string; references: LDrawTask['references'];
}
type StorageLike = Pick<Storage, 'getItem' | 'setItem'>;
function storage(): StorageLike | null { try { return localStorage; } catch { return null; } }
function valid(value: unknown): value is LDrawReview {
  if (!value || typeof value !== 'object') return false;
  const r = value as LDrawReview;
  return r.benchmarkVersion === VERSION && typeof r.taskId === 'string' && r.taskId.startsWith('ld1-')
    && typeof r.modelId === 'string' && typeof r.sourceHash === 'string' && /^[0-9a-f]{64}$/.test(r.sourceHash)
    && (r.decision === 'pass' || r.decision === 'fail') && typeof r.reason === 'string'
    && (r.decision !== 'fail' || !!r.reason.trim()) && Number.isFinite(Date.parse(r.reviewedAt))
    && Array.isArray(r.references) && r.references.every(ref => typeof ref.id === 'string' && /^B\d{4,}$/.test(ref.label));
}
export function loadLDrawReviews(store: StorageLike | null = storage()): Record<string, LDrawReview> {
  try {
    const rows: unknown = JSON.parse(store?.getItem(LDRAW_REVIEW_KEY) ?? '[]');
    return Object.fromEntries(Array.isArray(rows) ? rows.filter(valid).map(r => [r.taskId, r]) : []);
  } catch { return {}; }
}
export function persistLDrawReviews(rows: Record<string, LDrawReview>, store: StorageLike | null = storage()) {
  if (!store) throw new Error('浏览器存储不可用，请启用后再保存审核');
  store.setItem(LDRAW_REVIEW_KEY, JSON.stringify(Object.values(rows).filter(valid)));
  return rows;
}
export function makeLDrawReview(task: LDrawTask, sourceHash: string, decision: 'pass' | 'fail', reason: string): LDrawReview {
  if (decision === 'fail' && !reason.trim()) throw new Error('不通过时必须填写理由');
  const record: LDrawReview = { taskId: task.id, modelId: task.modelId, sourceHash, decision, reason: reason.trim(),
    reviewedAt: new Date().toISOString(), benchmarkVersion: VERSION, difficulty: task.difficulty, title: task.title,
    references: task.references };
  if (!valid(record)) throw new Error('审核记录无效');
  return record;
}
export function ldrawReviewBatch(records: Record<string, LDrawReview>, totalTasks: number) {
  const rows = Object.values(records).filter(valid);
  return { schemaVersion: 1, benchmarkVersion: VERSION, exportedAt: new Date().toISOString(),
    summary: { totalTasks, reviewed: rows.length, passed: rows.filter(r => r.decision === 'pass').length,
      failed: rows.filter(r => r.decision === 'fail').length, pending: Math.max(0, totalTasks - rows.length) },
    records: rows };
}
export function importLDrawReviews(raw: string, store: StorageLike | null = storage()) {
  const batch = JSON.parse(raw);
  if (batch.schemaVersion !== 1 || batch.benchmarkVersion !== VERSION || !Array.isArray(batch.records) || !batch.records.every(valid))
    throw new Error('审核文件版本或记录无效；旧批次请使用历史导出');
  const rows = loadLDrawReviews(store);
  for (const r of batch.records as LDrawReview[]) if (!rows[r.taskId] || rows[r.taskId].reviewedAt < r.reviewedAt) rows[r.taskId] = r;
  return persistLDrawReviews(rows, store);
}
export function downloadJson(value: unknown, filename: string) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(value, null, 2) + '\n'], { type: 'application/json' }));
  const link = document.createElement('a'); link.href = url; link.download = filename; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 0);
}
