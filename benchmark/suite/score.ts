import { type Part, type Verdict } from './shared';
import { cells, compare, decode, f1, insertIssue, key, removeIssue, validate } from './geometry';
import type { Task } from './tasks';

const failure = (reason: string): Verdict => ({ metrics: { format: 0, valid: 0, success: 0 }, issues: [reason] });
export function parseJSON(text: string): unknown {
  try { return JSON.parse(text.trim().replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '')); }
  catch { return null; }
}
export function legalityFeedback(answer: unknown) {
  const raw = answer && typeof answer === 'object' && 'structure' in answer ? answer.structure : answer;
  const s = decode(raw);
  return s ? { syntax: true, legality: validate(s.parts) }
    : { syntax: Boolean(answer && typeof answer === 'object'), legality: ['No decodable structure; for QA/planning, check the requested response schema.'] };
}
function retained(expected: Part[], actual: Part[]) {
  const pool = new Map<string, number>();
  for (const p of actual) pool.set(key(p), (pool.get(key(p)) ?? 0) + 1);
  let count = 0;
  for (const p of expected) if ((pool.get(key(p)) ?? 0) > 0) {
    count++; pool.set(key(p), pool.get(key(p))! - 1);
  }
  return expected.length ? count / expected.length : 1;
}
export function score(task: Task, answer: unknown): Verdict {
  if (!answer || typeof answer !== 'object' || Array.isArray(answer)) return failure('Expected JSON object');
  const a = answer as Record<string, unknown>, kind = task.public.kind;
  if (kind === 'parts' || kind === 'relations') {
    const expected = task.oracle as Record<string, unknown>;
    const types = Object.keys(expected).every(k => typeof a[k] === typeof expected[k]);
    if (!types) return failure('Missing or incorrectly typed answer field');
    const accuracy = Object.keys(expected).filter(k => a[k] === expected[k]).length / Object.keys(expected).length;
    return { metrics: { format: 1, valid: 1, success: Number(accuracy === 1), fieldAccuracy: accuracy },
      issues: accuracy === 1 ? [] : ['answer_mismatch'] };
  }
  if (kind === 'plan') {
    if (!Array.isArray(a.order) || a.order.length > 64 || a.order.some(id => typeof id !== 'string')) return failure('Invalid order array');
    const order = a.order as string[], assemble = task.public.input.direction === 'assemble';
    let current = assemble ? [] : structuredClone(task.target.parts);
    const used = new Set<string>();
    const issues: string[] = [];
    let prefix = 0;
    for (const id of order) {
      const p = task.target.parts.find(p => p.id === id);
      if (!p || used.has(id)) { issues.push('unknown_or_duplicate_id'); break; }
      const issue = assemble ? insertIssue(current, p) : removeIssue(current, id);
      if (issue) { issues.push(issue); break; }
      current = assemble ? [...current, p] : current.filter(q => q.id !== id);
      used.add(id); prefix++;
    }
    if (prefix !== task.target.parts.length || order.length !== task.target.parts.length) issues.push('incomplete');
    return { metrics: { format: 1, valid: Number(!issues.length), success: Number(!issues.length),
      legalPrefix: prefix / task.target.parts.length, coverage: used.size / task.target.parts.length }, issues };
  }
  const program = decode(kind === 'repair' ? a.structure : answer);
  if (!program || !program.parts.length) return failure('Invalid or empty structure program');
  const issues = validate(program.parts);
  const valid = Number(issues.length === 0), sim = compare(task.target.parts, program.parts);
  const metrics: Verdict['metrics'] = {
    format: 1, valid, success: Number(sim.exact), partF1: sim.partF1, bomF1: sim.bomF1,
    edgeF1: sim.edgeF1, occupancyIoU: sim.occupancyIoU,
  };
  if (kind === 'generate') {
    const allowed = task.public.input.allowedColors as string[];
    const colorsOK = program.parts.every(p => allowed.includes(p.color));
    metrics.constraintSuccess = Number(sim.occupancyIoU === 1 && colorsOK);
    metrics.success = valid * metrics.constraintSuccess;
    // A different tiling is valid here: reference part-level scores are not generation metrics.
    delete metrics.partF1; delete metrics.edgeF1; delete metrics.bomF1;
    if (!colorsOK) issues.push('color_constraint');
  }
  if (kind === 'complete' || kind === 'edit' || kind === 'repair') {
    const unchanged = task.source!.parts.filter(p => !task.changedIds.includes(p.id));
    metrics.preservation = retained(unchanged, program.parts);
  }
  if (kind === 'repair') {
    if (!Array.isArray(a.faultIds) || a.faultIds.some(id => typeof id !== 'string')
      || new Set(a.faultIds).size !== a.faultIds.length) return failure('faultIds must be a unique string array');
    const correct = (a.faultIds as string[]).filter(id => task.changedIds.includes(id)).length;
    metrics.localizationF1 = f1(correct, task.changedIds.length, a.faultIds.length);
    metrics.restorationSuccess = Number(sim.exact);
    metrics.success *= Number(metrics.localizationF1 === 1);
    metrics.falseAlarm = task.changedIds.length === 0 ? Number(a.faultIds.length > 0) : null;
  }
  if (!metrics.success && !issues.length) issues.push('target_mismatch');
  return { metrics, issues };
}

export function baseline(task: Task, name: 'oracle' | 'empty' | 'copy-input'): unknown {
  if (name === 'oracle') return structuredClone(task.oracle);
  if (name === 'empty') return {};
  const current = task.public.input.current ?? task.public.input.structure ?? { version: 1, parts: [] };
  return task.public.kind === 'repair' ? { structure: current, faultIds: [] } : current;
}
