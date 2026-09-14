import { bom, bounds, cells, compare, components, decode, insertIssue, key, removeIssue, validate } from '../geometry';
import type { Part, Structure } from '../shared';
import type { ChallengeTask } from './tasks';

export interface ChallengeVerdict {
  success: number;
  metrics: Record<string, number>;
  issues: string[];
}

const sameSet = (a: unknown, expected: string[]) =>
  Array.isArray(a) && a.every(v => typeof v === 'string')
  && a.length === expected.length && new Set(a).size === a.length
  && expected.every(v => a.includes(v));

function structureAnswer(answer: unknown) {
  if (answer && typeof answer === 'object' && 'structure' in answer) {
    return decode((answer as { structure: unknown }).structure);
  }
  return decode(answer);
}

function exactStructure(task: ChallengeTask, answer: unknown) {
  const structure = structureAnswer(answer), metrics: Record<string, number> = {
    format: Number(Boolean(structure)), valid: 0, partF1: 0, edgeF1: 0, exact: 0,
  };
  if (!structure) return { success: 0, metrics, issues: ['format'] };
  const comparison = compare(task.target.parts, structure.parts);
  metrics.valid = Number(validate(structure.parts).length === 0);
  metrics.partF1 = comparison.partF1;
  metrics.edgeF1 = comparison.edgeF1;
  metrics.exact = Number(comparison.exact);
  if (task.source) {
    const actualKeys = new Set(structure.parts.map(p => key(p)));
    const protectedParts = task.source.parts.filter(p => !task.changedIds.includes(p.id));
    const changedTarget = task.target.parts.filter(p => task.changedIds.includes(p.id));
    metrics.preservation = protectedParts.length
      ? protectedParts.filter(p => actualKeys.has(key(p))).length / protectedParts.length : 1;
    metrics.changedTargetRecall = changedTarget.length
      ? changedTarget.filter(p => actualKeys.has(key(p))).length / changedTarget.length : 1;
  }
  return { success: metrics.exact, metrics, issues: metrics.exact ? [] : ['target_mismatch'] };
}

function recovery(task: ChallengeTask, answer: unknown): ChallengeVerdict {
  const actions = answer && typeof answer === 'object' && Array.isArray((answer as any).actions)
    ? (answer as any).actions : null;
  const metrics: Record<string, number> = { format: Number(Boolean(actions)), legalPrefix: 0, finalExact: 0 };
  if (!actions) return { success: 0, metrics, issues: ['format'] };
  let current = structuredClone(task.source?.parts ?? []), legal = 0;
  for (const action of actions) {
    if (!action || !['remove', 'place'].includes(action.type) || typeof action.id !== 'string') break;
    if (action.type === 'remove') {
      const issue = removeIssue(current, action.id);
      if (issue) break;
      current = current.filter(p => p.id !== action.id);
    } else {
      const part = task.target.parts.find(p => p.id === action.id);
      if (!part || current.some(p => p.id === action.id) || insertIssue(current, part)) break;
      current = [...current, part];
    }
    legal++;
  }
  metrics.legalPrefix = actions.length ? legal / actions.length : 0;
  metrics.finalExact = Number(compare(task.target.parts, current).exact);
  const success = Number(legal === actions.length && metrics.finalExact === 1);
  return { success, metrics, issues: success ? [] : [legal < actions.length ? 'illegal_action' : 'target_mismatch'] };
}

function constrained(task: ChallengeTask, answer: unknown): ChallengeVerdict {
  const structure = structureAnswer(answer), metrics: Record<string, number> = {
    format: Number(Boolean(structure)), valid: 0, extent: 0, connected: 0,
    inventory: 0, anchors: 0, roofCoverage: 0, colorRoles: 0,
  };
  if (!structure) return { success: 0, metrics, issues: ['format'] };
  const requirements = task.private.requirements as {
    extent: { x: number; y: number; z: number }; inventory: Record<string, number>;
    anchors: Part[]; minRoofCells: number; minColors: number; minParts: number; maxParts: number;
  };
  const actualBom = bom(structure.parts), actualBounds = structure.parts.length ? bounds(structure.parts) : null;
  metrics.valid = Number(validate(structure.parts).length === 0
    && structure.parts.length >= requirements.minParts && structure.parts.length <= requirements.maxParts);
  metrics.extent = Number(Boolean(actualBounds)
    && ['x', 'y', 'z'].every(axis => actualBounds![axis as keyof typeof actualBounds] === requirements.extent[axis as keyof typeof requirements.extent]));
  metrics.connected = Number(components(structure.parts) === 1);
  metrics.inventory = Number(Object.entries(actualBom).every(([name, count]) => count <= (requirements.inventory[name] ?? 0)));
  const actualKeys = new Set(structure.parts.map(p => key(p)));
  metrics.anchors = Number(requirements.anchors.every(p => actualKeys.has(key(p))));
  metrics.roofCoverage = Number(cells(structure.parts.filter(p => p.y >= 7)).size >= requirements.minRoofCells);
  metrics.colorRoles = Number(new Set(structure.parts.map(p => p.color)).size >= requirements.minColors);
  const success = Number(Object.values(metrics).every(Boolean));
  return { success, metrics, issues: success ? [] : Object.entries(metrics).filter(([, value]) => !value).map(([name]) => name) };
}

export function evaluateChallenge(task: ChallengeTask, answer: unknown): ChallengeVerdict {
  if (task.kind === 'recovery-plan') return recovery(task, answer);
  if (task.kind === 'support-counterfactual') {
    const actual = answer && typeof answer === 'object' ? (answer as any).unsupportedIds : null;
    const expected = (task.oracle as { unsupportedIds: string[] }).unsupportedIds;
    const exact = Number(sameSet(actual, expected));
    return { success: exact, metrics: { format: Number(Array.isArray(actual)), setExact: exact }, issues: exact ? [] : ['set_mismatch'] };
  }
  if (task.kind === 'multi-fault-repair') {
    const base = exactStructure(task, answer);
    const actual = answer && typeof answer === 'object' ? (answer as any).faultIds : null;
    const expected = (task.oracle as { faultIds: string[] }).faultIds;
    const localization = Number(sameSet(actual, expected));
    const success = Number(base.success === 1 && localization === 1);
    return { success, metrics: { ...base.metrics, faultSetExact: localization },
      issues: success ? [] : [...base.issues, ...(localization ? [] : ['fault_mismatch'])] };
  }
  if (task.kind === 'active-inspection') {
    const actual = answer as { queryId?: string; answer?: string } | null;
    const expected = task.oracle as { queryId: string; answer: string };
    const query = Number(actual?.queryId === expected.queryId), result = Number(actual?.answer === expected.answer);
    const option = (task.input.queryOptions as Array<{ id: string; cost: number }>).find(o => o.id === actual?.queryId);
    const success = Number(query === 1 && result === 1);
    return { success, metrics: { format: Number(Boolean(actual)), queryExact: query, answerExact: result,
      queryCost: option?.cost ?? 0 }, issues: success ? [] : ['answer_mismatch'] };
  }
  if (task.kind === 'graph-reasoning') {
    const actual = answer as { shortestPath?: number; articulationIds?: unknown } | null;
    const expected = task.oracle as { shortestPath: number; articulationIds: string[] };
    const path = Number(actual?.shortestPath === expected.shortestPath);
    const articulation = Number(sameSet(actual?.articulationIds, expected.articulationIds));
    const success = Number(path === 1 && articulation === 1);
    return { success, metrics: { format: Number(Boolean(actual)), pathExact: path, articulationSetExact: articulation },
      issues: success ? [] : ['answer_mismatch'] };
  }
  if (task.kind === 'pose-estimation') {
    const actual = answer as Record<string, unknown> | null, expected = task.oracle as Record<string, number>;
    const fields = ['x', 'y', 'z', 'turn'];
    const correct = fields.filter(field => actual?.[field] === expected[field]).length;
    const success = Number(correct === fields.length);
    return { success, metrics: { format: Number(Boolean(actual)), poseFieldAccuracy: correct / fields.length, exact: success },
      issues: success ? [] : ['answer_mismatch'] };
  }
  if (task.kind === 'step-selection') {
    const actual = answer && typeof answer === 'object' ? (answer as any).legalIds : null;
    const expected = (task.oracle as { legalIds: string[] }).legalIds;
    const exact = Number(sameSet(actual, expected));
    return { success: exact, metrics: { format: Number(Array.isArray(actual)), setExact: exact },
      issues: exact ? [] : ['selection_mismatch'] };
  }
  if (task.kind === 'constrained-redesign') return constrained(task, answer);
  return exactStructure(task, answer);
}
