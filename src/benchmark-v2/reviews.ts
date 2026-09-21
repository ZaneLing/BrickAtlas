export const VERSION = 'brickatlas-ldraw-2';
export const STORAGE = 'brickatlas-ldraw-2-reviews-v1';
export interface ReviewUnit {
  id: string; kind: 'task' | 'pair'; sourceId: string; sourceHash: string; contentHash: string;
  operands: { id: string; label: string }[]; required: boolean; title: string;
  family?: string; modality?: string; reasons: string[];
}
export interface ReviewIndex {
  version: string; releaseHash: string; units: ReviewUnit[];
  summary: { sources: number; parts: number; tasks: number; humanQueue: number; physicalQueue: number };
}
export interface ReviewRecord {
  id: string; kind: 'task' | 'pair'; sourceId: string; sourceHash: string; contentHash: string;
  operands: ReviewUnit['operands']; reviewer: string; decision: string; rationale: string; updatedAt: string;
}
export interface ReviewBatch {
  schema: 'ldraw2-review-batch-v1'; version: typeof VERSION; releaseHash: string; records: ReviewRecord[];
}
export const decisions = {
  task: { pass: '通过', fail: '不通过', uncertain: '无法判定' },
  pair: { 'intended-mating': '正常嵌合', 'mesh-approximation': '网格近似', 'source-defect': '源模型问题', unresolved: '仍待确认' },
};
export const keyOf = (r: Pick<ReviewRecord, 'id' | 'reviewer'>) => JSON.stringify([r.id, r.reviewer]);
export function emptyBatch(index: ReviewIndex): ReviewBatch {
  return { schema: 'ldraw2-review-batch-v1', version: VERSION, releaseHash: index.releaseHash, records: [] };
}
export function validateBatch(raw: unknown, index: ReviewIndex): ReviewBatch {
  if (!raw || typeof raw !== 'object') throw new Error('审核文件必须是 JSON 对象');
  const b = raw as ReviewBatch;
  if (b.schema !== 'ldraw2-review-batch-v1' || b.version !== VERSION || b.releaseHash !== index.releaseHash)
    throw new Error('版本或题集内容已变化，不能合并旧版审核');
  if (!Array.isArray(b.records)) throw new Error('审核记录格式错误');
  const units = new Map(index.units.map(u => [u.id, u])), seen = new Set<string>();
  for (const r of b.records) {
    if (!r || typeof r !== 'object') throw new Error('审核记录格式错误');
    const u = units.get(r.id);
    if (!u || r.kind !== u.kind || r.sourceId !== u.sourceId || r.sourceHash !== u.sourceHash
      || r.contentHash !== u.contentHash || JSON.stringify(r.operands) !== JSON.stringify(u.operands))
      throw new Error(`未知或已变化的题目/零件对：${String(r.id)}`);
    if (typeof r.reviewer !== 'string' || !r.reviewer.trim() || r.reviewer !== r.reviewer.trim()
      || typeof r.rationale !== 'string' || !r.rationale.trim()
      || !Object.hasOwn(decisions[u.kind], r.decision)
      || typeof r.updatedAt !== 'string' || !Number.isFinite(Date.parse(r.updatedAt)))
      throw new Error('每条记录必须包含审核人、有效结论、理由和时间');
    const key = keyOf(r);
    if (seen.has(key)) throw new Error('同一审核人对同一项目有重复记录');
    seen.add(key);
  }
  // Normalize to known fields; never retain arbitrary imported properties.
  return { ...emptyBatch(index), records: b.records.map(r => ({
    id: r.id, kind: r.kind, sourceId: r.sourceId, sourceHash: r.sourceHash,
    contentHash: r.contentHash, operands: r.operands.map(o => ({ id: o.id, label: o.label })),
    reviewer: r.reviewer, decision: r.decision, rationale: r.rationale, updatedAt: r.updatedAt,
  })) };
}
export function mergeBatch(current: ReviewBatch, incoming: unknown, index: ReviewIndex): ReviewBatch {
  const next = validateBatch(incoming, index), old = validateBatch(current, index);
  const records = new Map(old.records.map(r => [keyOf(r), r]));
  for (const r of next.records) {
    const previous = records.get(keyOf(r));
    if (previous && JSON.stringify(previous) !== JSON.stringify(r))
      throw new Error(`同一审核人的记录存在冲突：${r.id}。请保留原文件并人工合并。`);
    records.set(keyOf(r), r);
  }
  return { ...emptyBatch(index), records: [...records.values()] };
}
export function makeRecord(unit: ReviewUnit, reviewer: string, decision: string, rationale: string): ReviewRecord {
  return { id: unit.id, kind: unit.kind, sourceId: unit.sourceId, sourceHash: unit.sourceHash,
    contentHash: unit.contentHash, operands: unit.operands, reviewer: reviewer.trim(),
    decision, rationale: rationale.trim(), updatedAt: new Date().toISOString() };
}
export function download(value: unknown, filename: string) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(value, null, 2) + '\n'], { type: 'application/json' }));
  const a = document.createElement('a'); a.href = url; a.download = filename; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
