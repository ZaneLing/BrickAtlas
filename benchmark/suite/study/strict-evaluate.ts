import type { CaseTask } from '../v2/cases';
import { evaluate } from '../v2/evaluate';

export const EVALUATOR_VERSION = 'v2-strict-schema-1';
export function structureSchemaValid(value: unknown): boolean {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false;
  const s = value as Record<string, unknown>;
  if (s.version !== 1) return false;
  if (Object.hasOwn(s, 'parts') === Object.hasOwn(s, 'nodes')) return false;
  if (Object.hasOwn(s, 'parts')) {
    return Array.isArray(s.parts) && s.parts.length <= 64 && s.parts.every(p => p && typeof p === 'object'
      && !Array.isArray(p) && typeof p.id === 'string' && typeof p.partId === 'string' && typeof p.color === 'string'
      && [p.x, p.y, p.z, p.turn].every(v => typeof v === 'number' && Number.isInteger(v)));
  }
  return Array.isArray(s.nodes) && s.nodes.length <= 64 && s.nodes.every(p => p && typeof p === 'object'
    && !Array.isArray(p) && typeof p.id === 'string' && typeof p.partId === 'string' && typeof p.color === 'string'
    && (p.parent === null || typeof p.parent === 'string') && typeof p.turn === 'number' && Number.isInteger(p.turn)
    && Array.isArray(p.offset) && p.offset.length === 3 && p.offset.every((x: unknown) => typeof x === 'number' && Number.isInteger(x)));
}
export function evaluateStrict(task: CaseTask, answer: unknown) {
  if (['parts', 'relations', 'plan'].includes(task.spec.kind)) return evaluate(task, answer);
  const raw = task.spec.kind === 'repair' && answer && typeof answer === 'object' && 'structure' in answer ? answer.structure : answer;
  if (!structureSchemaValid(raw)) {
    const failure = evaluate(task, null);
    failure.issues = ['strict_structure_schema']; return failure;
  }
  return evaluate(task, answer);
}
