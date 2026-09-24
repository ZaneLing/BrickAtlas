import { score as legacyScore } from '../benchmark/engine';
import type { Task } from '../benchmark/types';
import type { V2Task } from '../../benchmark/suite/ldraw-v2/types';

/** Shared by the offline scorer and the answer-bearing human review UI. */
export function score(task: V2Task, raw: unknown) {
  if (task.format === 'integer') {
    const value = raw && typeof raw === 'object' && !Array.isArray(raw) ? (raw as { value?: unknown }).value : undefined;
    const valid = typeof value === 'number' && Number.isSafeInteger(value);
    return { success: Number(valid && value === task.answer.value), validFormat: Number(valid) };
  }
  const result = legacyScore(task as Task, raw);
  if (task.format === 'actions') {
    const ids = (raw as { actionIds?: unknown } | null)?.actionIds;
    return { ...result, validFormat: Number(Array.isArray(ids) && ids.every(id => typeof id === 'string')) };
  }
  return result;
}
