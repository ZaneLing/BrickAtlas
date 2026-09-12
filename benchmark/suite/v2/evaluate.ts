import { type Part, type Verdict, type Kind } from '../shared';
import { bom, bounds, cells, compare, components, decode, dims, edges, f1, insertIssue, key, removeIssue, validate } from '../geometry';
import { surfaceSignature } from '../research/tasks';
import type { CaseTask } from './cases';

export const COMMON = ['format', 'valid', 'success'] as const;
const STRUCTURE = ['partPrecision', 'partRecall', 'partF1', 'bomPrecision', 'bomRecall', 'bomF1',
  'edgeF1', 'occupancyIoU', 'coloredOccupancyIoU', 'surfacePrecision', 'surfaceRecall', 'surfaceF1',
  'fullStructureSuccess', 'visibleSurfaceSuccess', 'countAccuracy', 'collisionFree', 'supported', 'withinBounds'];
export function metricNames(kind: Kind) {
  const extra: Record<Kind, string[]> = {
    parts: ['partIdAccuracy', 'colorAccuracy', 'studsAccuracy', 'fieldAccuracy'],
    relations: ['connectedAccuracy', 'aboveAccuracy', 'contactStudsAccuracy', 'shortestPathAccuracy', 'fieldAccuracy'],
    reconstruct: STRUCTURE,
    generate: ['constraintAccuracy', 'extentSuccess', 'anchorSuccess', 'pieceBudgetSuccess', 'colorCountSuccess',
      'connectivitySuccess', 'branchingSuccess', 'collisionFree', 'supported', 'withinBounds'],
    complete: [...STRUCTURE, 'preservation', 'additionPrecision', 'additionRecall', 'additionF1'],
    edit: [...STRUCTURE, 'preservation', 'editTargetSuccess'],
    plan: ['legalPrefix', 'coverage', 'submittedCoverage', 'lengthAccuracy', 'duplicateFree'],
    repair: [...STRUCTURE, 'preservation', 'localizationPrecision', 'localizationRecall', 'localizationF1',
      'restorationSuccess', 'trueNegative', 'falseAlarm'],
  };
  return [...COMMON, ...extra[kind]];
}
export function emptyMetrics(task: CaseTask) {
  const metrics: Verdict['metrics'] = { format: 0, success: 0, valid: 0,
    ...Object.fromEntries(metricNames(task.spec.kind).map(k => [k, 0])) };
  if (task.spec.kind === 'repair' && task.changedIds.length) { metrics.falseAlarm = null; metrics.trueNegative = null; }
  return metrics;
}
function matches(target: Part[], actual: Part[]) {
  const pool = new Map<string, number>();
  for (const p of target) pool.set(key(p), (pool.get(key(p)) ?? 0) + 1);
  let n = 0;
  for (const p of actual) if ((pool.get(key(p)) ?? 0) > 0) { n++; pool.set(key(p), pool.get(key(p))! - 1); }
  return n;
}
function subtract(actual: Part[], unchanged: Part[]) {
  const rest = [...actual];
  for (const p of unchanged) {
    const i = rest.findIndex(q => key(q) === key(p)); if (i >= 0) rest.splice(i, 1);
  }
  return rest;
}
const precision = (n: number, actual: number, expected: number) => actual ? n / actual : Number(expected === 0);
const recall = (n: number, expected: number) => expected ? n / expected : 1;
function overlapMetrics(target: Part[], actual: Part[]) {
  const sim = compare(target, actual), n = matches(target, actual), tb = bom(target), ab = bom(actual);
  const bn = Object.keys(tb).reduce((sum, k) => sum + Math.min(tb[k], ab[k] ?? 0), 0);
  const tc = cells(target, true), ac = cells(actual, true);
  const ts = surfaceSignature(target), as = surfaceSignature(actual), sn = [...ts].filter(s => as.has(s)).length;
  return { ...sim, partPrecision: precision(n, actual.length, target.length), partRecall: recall(n, target.length),
    bomPrecision: precision(bn, actual.length, target.length), bomRecall: recall(bn, target.length),
    coloredOccupancyIoU: [...tc].filter(c => ac.has(c)).length / Math.max(1, new Set([...tc, ...ac]).size),
    surfacePrecision: precision(sn, as.size, ts.size), surfaceRecall: recall(sn, ts.size), surfaceF1: f1(sn, ts.size, as.size),
    countAccuracy: 1 - Math.abs(target.length - actual.length) / Math.max(target.length, actual.length, 1) };
}
export interface Evaluation extends Verdict {
  diagnostics: { submittedParts: number | null; expectedParts: number | null; firstInvalidStep: number | null;
    matchedParts: number | null; missingParts: string[]; extraParts: string[] };
}
export function evaluate(task: CaseTask, answer: unknown): Evaluation {
  const kind = task.spec.kind, metrics = emptyMetrics(task);
  const diagnostics: Evaluation['diagnostics'] = { submittedParts: null, expectedParts: task.target.parts.length,
    firstInvalidStep: null, matchedParts: null, missingParts: [], extraParts: [] };
  const result = (issues: string[]): Evaluation => ({ metrics, issues, diagnostics });
  if (!answer || typeof answer !== 'object' || Array.isArray(answer)) return result(['format']);
  const a = answer as Record<string, unknown>;
  if (kind === 'parts' || kind === 'relations') {
    const expected = task.oracle as Record<string, unknown>, fields = Object.keys(expected);
    const metricKeys = kind === 'parts' ? ['partIdAccuracy', 'colorAccuracy', 'studsAccuracy']
      : ['connectedAccuracy', 'aboveAccuracy', 'contactStudsAccuracy', 'shortestPathAccuracy'];
    let format = true, n = 0;
    fields.forEach((field, i) => {
      if (typeof a[field] !== typeof expected[field] || typeof a[field] === 'number' && !Number.isInteger(a[field])) format = false;
      const correct = Number(a[field] === expected[field]); metrics[metricKeys[i]] = correct; n += correct;
    });
    metrics.format = Number(format); metrics.valid = Number(format);
    metrics.fieldAccuracy = n / fields.length; metrics.success = Number(format && n === fields.length);
    return result(metrics.success ? [] : [format ? 'answer_mismatch' : 'format']);
  }
  if (kind === 'plan') {
    if (!Array.isArray(a.order) || a.order.length > 128 || a.order.some(id => typeof id !== 'string')) return result(['format']);
    metrics.format = 1;
    const order = a.order as string[], target = task.target.parts, seen = new Set<string>();
    const assemble = task.spec.variant === 'assemble', issues: string[] = [];
    let current = assemble ? [] : structuredClone(target), prefix = 0;
    for (const [i, id] of order.entries()) {
      const p = target.find(p => p.id === id);
      const issue = !p ? 'unknown_id' : seen.has(id) ? 'duplicate_id'
        : assemble ? insertIssue(current, p) : removeIssue(current, id);
      if (issue) { issues.push(issue); diagnostics.firstInvalidStep = i; break; }
      seen.add(id); prefix++; current = assemble ? [...current, p!] : current.filter(q => q.id !== id);
    }
    metrics.legalPrefix = prefix / target.length; metrics.coverage = seen.size / target.length;
    metrics.submittedCoverage = new Set(order.filter(id => target.some(p => p.id === id))).size / target.length;
    metrics.lengthAccuracy = 1 - Math.abs(order.length - target.length) / Math.max(order.length, target.length);
    metrics.duplicateFree = Number(new Set(order).size === order.length);
    if (prefix !== target.length || order.length !== target.length) issues.push('incomplete');
    metrics.valid = Number(!issues.length); metrics.success = metrics.valid;
    return result(issues);
  }
  // Reject oversized arrays before passing them to the frozen decoder.
  const raw = kind === 'repair' ? a.structure : a;
  if (raw && typeof raw === 'object' && 'parts' in raw && Array.isArray(raw.parts) && raw.parts.length > 64) return result(['piece_limit']);
  const decoded = decode(raw);
  if (!decoded) return result(['structure_format']);
  const actual = decoded.parts, issues = validate(actual);
  metrics.format = 1; metrics.valid = Number(!issues.length);
  diagnostics.submittedParts = actual.length;
  metrics.collisionFree = Number(!issues.includes('overlap'));
  metrics.supported = Number(!issues.includes('unsupported'));
  metrics.withinBounds = Number(!issues.includes('out_of_bounds'));
  if (kind === 'generate') {
    const requirements = task.public.input.requirements as {
      extent: { x: number; y: number; z: number }; maxPieces: number; minColors: number; components: number; minMaximumDegree: number;
    };
    const box = actual.length ? bounds(actual) : null, links = edges(actual);
    const checks = {
      extentSuccess: !!box && ['x', 'y', 'z'].every(k => box[k as keyof typeof box] === requirements.extent[k as keyof typeof box]),
      anchorSuccess: !!actual.length && ['x', 'y', 'z'].every(k => Math.min(...actual.map(p => p[k as 'x' | 'y' | 'z'])) === 0),
      pieceBudgetSuccess: actual.length > 0 && actual.length <= requirements.maxPieces,
      colorCountSuccess: new Set(actual.map(p => p.color)).size >= requirements.minColors,
      connectivitySuccess: components(actual) === requirements.components,
      branchingSuccess: actual.some(p => links.filter(e => e.a === p.id || e.b === p.id).length >= requirements.minMaximumDegree),
    };
    for (const [k, v] of Object.entries(checks)) metrics[k] = Number(v);
    metrics.constraintAccuracy = Object.values(checks).filter(Boolean).length / 6;
    metrics.success = Number(metrics.valid === 1 && metrics.constraintAccuracy === 1);
    return result([...issues, ...Object.entries(checks).filter(([, v]) => !v).map(([k]) => k)]);
  }
  const sim = overlapMetrics(task.target.parts, actual), { exact, ...numeric } = sim;
  Object.assign(metrics, numeric);
  metrics.fullStructureSuccess = Number(exact); metrics.visibleSurfaceSuccess = Number(metrics.valid === 1 && sim.bomF1 === 1 && sim.surfaceF1 === 1);
  diagnostics.matchedParts = matches(task.target.parts, actual);
  diagnostics.missingParts = subtract(task.target.parts, actual).map(p => p.id);
  diagnostics.extraParts = subtract(actual, task.target.parts).map(p => p.id);
  if (task.source) {
    const unchanged = task.source.parts.filter(p => !task.changedIds.includes(p.id));
    metrics.preservation = unchanged.length ? matches(unchanged, actual) / unchanged.length : 1;
    if (kind === 'complete') {
      const expectedAdded = subtract(task.target.parts, unchanged), added = subtract(actual, unchanged), n = matches(expectedAdded, added);
      metrics.additionPrecision = precision(n, added.length, expectedAdded.length);
      metrics.additionRecall = recall(n, expectedAdded.length); metrics.additionF1 = f1(n, expectedAdded.length, added.length);
    }
  }
  let success = (task.spec.condition === 'ordinary' && ['reconstruct', 'complete', 'repair'].includes(kind)
    ? metrics.visibleSurfaceSuccess : metrics.fullStructureSuccess) === 1 && (metrics.preservation ?? 1) === 1;
  if (kind === 'repair') {
    if (!Array.isArray(a.faultIds) || a.faultIds.some(id => typeof id !== 'string') || new Set(a.faultIds).size !== a.faultIds.length) {
      metrics.format = 0; metrics.valid = 0; success = false; issues.push('faultIds_format');
    } else {
      const ids = a.faultIds as string[], n = ids.filter(id => task.changedIds.includes(id)).length;
      metrics.localizationPrecision = precision(n, ids.length, task.changedIds.length);
      metrics.localizationRecall = recall(n, task.changedIds.length);
      metrics.localizationF1 = f1(n, task.changedIds.length, ids.length);
      metrics.restorationSuccess = Number(exact);
      if (!task.changedIds.length) { metrics.falseAlarm = Number(ids.length > 0); metrics.trueNegative = Number(!ids.length); }
      success = success && metrics.localizationF1 === 1;
    }
  }
  if (kind === 'edit') metrics.editTargetSuccess = Number(exact);
  metrics.success = Number(success);
  return result(issues.length ? issues : success ? [] : ['target_mismatch']);
}
