import { type Part } from '../shared';
import { cells, key } from '../geometry';
import { exact, parseStructure } from '../frontier/geometry';
import { sameSet } from '../frontier/tasks';
import { admissible, scan } from '../frontier2/observation';
import {
  type ClarificationCase,
  type ConstructibilityCase,
  type RecoveryCase,
  type SequenceCase,
  type StockoutCase,
} from './cases';
import {
  APPROACHES,
  auditPlan,
  executePlacement,
  executeRemoval,
  type PlacementStep,
} from './geometry';

const object = (value: unknown): value is Record<string, any> =>
  Boolean(value) && typeof value === 'object' && !Array.isArray(value);
const uniqueStrings = (value: unknown): value is string[] =>
  Array.isArray(value) && value.every(v => typeof v === 'string')
  && new Set(value).size === value.length;

export function scoreSequence(c: SequenceCase, raw: unknown) {
  const answer = object(raw) ? raw : {};
  const audit = auditPlan(c.input.target.parts, c.input.candidate);
  const failureIndexExact = Number(answer.firstFailure === audit.firstFailure);
  const reasonExact = Number(answer.reason === audit.reason);
  const prefixLengthExact = Number(answer.legalPrefixLength === audit.legalPrefixLength);
  const decisionExact = Number(answer.constructible === Boolean(audit.success));
  return {
    success: Number(failureIndexExact && reasonExact && prefixLengthExact && decisionExact),
    failureIndexExact,
    reasonExact,
    prefixLengthExact,
    decisionExact,
    observed: {
      legalPrefixRate: audit.legalPrefixRate,
      prefixSupportScore: audit.prefixSupportScore,
      minimumSupportFraction: audit.minimumSupportFraction,
      accessibleStepRate: audit.accessibleStepRate,
    },
  };
}

function expectedCheckpoint(c: RecoveryCase) {
  const ids = new Set([...c.input.current.parts.map(p => p.id), c.input.failedStep.id]);
  return c.input.target.parts.filter(p => ids.has(p.id));
}

export function scoreRecovery(c: RecoveryCase, raw: unknown) {
  const answer = object(raw) ? raw : {};
  const diagnosisExact = Number(answer.diagnosis?.failedId === c.input.failedStep.id
    && answer.diagnosis?.reason === 'tool_clearance');
  const actions = Array.isArray(answer.recovery) ? answer.recovery : [];
  let state = c.input.current.parts.map(p => ({ ...p }));
  const inventory = new Map<string, Part>();
  let legalActions = 0, legal = Array.isArray(answer.recovery);
  for (const action of actions) {
    if (!object(action) || !['remove', 'place'].includes(action.op)
      || typeof action.id !== 'string' || !APPROACHES.includes(action.approach)) {
      legal = false; break;
    }
    if (action.op === 'remove') {
      const part = state.find(p => p.id === action.id);
      if (!part || inventory.has(action.id)) { legal = false; break; }
      const result = executeRemoval(state, action.id, action.approach);
      if (result.issue) { legal = false; break; }
      inventory.set(action.id, part); state = result.parts;
    } else {
      const target = c.input.target.parts.find(p => p.id === action.id);
      const available = action.id === c.input.failedStep.id
        ? !c.input.current.parts.some(p => p.id === action.id)
        : inventory.has(action.id);
      if (!target || !available) { legal = false; break; }
      const result = executePlacement(state, target, action.approach);
      if (result.issue) { legal = false; break; }
      inventory.delete(action.id); state = result.parts;
    }
    legalActions++;
  }
  const checkpoint = expectedCheckpoint(c);
  const recoveryExact = Number(legal && inventory.size === 0 && exact(checkpoint, state)
    && checkpoint.every(p => state.some(q => q.id === p.id && key(q) === key(p))));
  const minimumRecovery = Number(recoveryExact && actions.length === c.input.maxRecoveryActions);
  const continuation = Array.isArray(answer.continuation) ? answer.continuation : [];
  let continuationLegal = Boolean(recoveryExact && uniqueStrings(continuation.map((s: any) => s?.id))
    && sameSet(continuation.map((s: any) => s.id), c.input.continuationIds));
  let continuationSteps = 0;
  if (continuationLegal) for (const step of continuation as PlacementStep[]) {
    if (!step || !APPROACHES.includes(step.approach)) { continuationLegal = false; break; }
    const part = c.input.target.parts.find(p => p.id === step.id);
    if (!part) { continuationLegal = false; break; }
    const result = executePlacement(state, part, step.approach);
    if (result.issue) { continuationLegal = false; break; }
    state = result.parts; continuationSteps++;
  }
  const expectedFinal = [...checkpoint,
    ...c.input.target.parts.filter(p => c.input.continuationIds.includes(p.id))];
  const continuationExact = Number(continuationLegal && exact(expectedFinal, state));
  const all = diagnosisExact && minimumRecovery && continuationExact;
  return {
    success: Number(all),
    diagnosisExact,
    legalRecovery: Number(legal),
    recoveryExact,
    minimumRecovery,
    continuationExact,
    legalActions,
    continuationSteps,
    recoveryActions: actions.length,
    recoveryOptimum: c.input.maxRecoveryActions,
  };
}

function signature(parts: Part[]) {
  return [...cells(parts)].sort().join('|');
}

export function scoreStockout(c: StockoutCase, raw: unknown) {
  const answer = object(raw) ? raw : {};
  const rows = Array.isArray(answer.placements) ? answer.placements : [];
  const parsed = parseStructure({ version: 1, parts: rows.map((row: any) => row?.part) });
  const idsNew = Boolean(parsed && parsed.parts.every(p => !c.input.target.parts.some(q => q.id === p.id)));
  const used: Record<string, number> = {};
  for (const part of parsed?.parts ?? []) used[part.partId] = (used[part.partId] ?? 0) + 1;
  const stockValid = Number(Boolean(parsed && Object.entries(used)
    .every(([partId, count]) => count <= (c.input.stock[partId] ?? 0))));
  const regionExact = Number(Boolean(parsed
    && signature(parsed.parts) === signature([c.input.unavailablePart])
    && parsed.parts.every(p => p.color === c.input.unavailablePart.color)));
  const minimumPieces = Number(Boolean(parsed && parsed.parts.length === c.input.optimalReplacementPieces));
  let state = c.input.current.parts.map(p => ({ ...p }));
  let placementsLegal = Boolean(parsed && rows.length === parsed.parts.length && idsNew);
  let legalPlacements = 0;
  if (placementsLegal) for (let index = 0; index < rows.length; index++) {
    const approach = rows[index]?.approach;
    if (!APPROACHES.includes(approach)) { placementsLegal = false; break; }
    const result = executePlacement(state, parsed!.parts[index], approach);
    if (result.issue) { placementsLegal = false; break; }
    state = result.parts; legalPlacements++;
  }
  const continuation = Array.isArray(answer.continuation) ? answer.continuation : [];
  let continuationLegal = placementsLegal && uniqueStrings(continuation.map((s: any) => s?.id))
    && sameSet(continuation.map((s: any) => s.id), c.input.continuationIds);
  let continuationSteps = 0;
  if (continuationLegal) for (const step of continuation as PlacementStep[]) {
    if (!step || !APPROACHES.includes(step.approach)) { continuationLegal = false; break; }
    const part = c.input.target.parts.find(p => p.id === step.id);
    if (!part) { continuationLegal = false; break; }
    const result = executePlacement(state, part, step.approach);
    if (result.issue) { continuationLegal = false; break; }
    state = result.parts; continuationSteps++;
  }
  const processExact = Number(placementsLegal && continuationLegal);
  const success = stockValid && regionExact && minimumPieces && processExact;
  return {
    success: Number(success),
    stockValid,
    regionExact,
    minimumPieces,
    processExact,
    legalPlacements,
    continuationSteps,
  };
}

function posterior(c: ClarificationCase) {
  return admissible({ ...c.input, budget: 0 });
}

function entropy(counts: number[], total: number) {
  return counts.reduce((sum, count) => {
    const p = count / total;
    return count ? sum - p * Math.log2(p) : sum;
  }, 0);
}

export function queryUtilities(c: ClarificationCase) {
  const worlds = posterior(c);
  const seen = new Set(c.input.observed.map(o => o.queryId));
  const priorEntropy = Math.log2(worlds.length);
  return c.input.queries.filter(q => !seen.has(q.id)).map(query => {
    const groups = new Map<string, number>();
    for (const world of worlds) {
      const value = scan(world.parts, query);
      groups.set(value, (groups.get(value) ?? 0) + 1);
    }
    const conditionalEntropy = entropy([...groups.values()], worlds.length);
    const informationGain = priorEntropy - conditionalEntropy;
    return {
      queryId: query.id,
      cost: query.cost,
      informationGain,
      efficiency: informationGain / query.cost,
      partitions: groups.size,
    };
  });
}

export function optimalNextQueries(c: ClarificationCase) {
  const worlds = posterior(c);
  if (worlds.length <= 1) return [];
  const rows = queryUtilities(c);
  const best = Math.max(...rows.map(row => row.efficiency));
  return rows.filter(row => Math.abs(row.efficiency - best) < 1e-12 && row.informationGain > 0)
    .map(row => row.queryId);
}

export function scoreClarification(c: ClarificationCase, raw: unknown) {
  const answer = object(raw) ? raw : {};
  const worlds = posterior(c), possibleIds = worlds.map(w => w.id).sort();
  const possibleExact = Number(sameSet(answer.possibleIds, possibleIds));
  const probabilities = object(answer.probabilities) ? answer.probabilities : {};
  const allIds = c.input.worlds.map(w => w.id);
  const numeric = allIds.every(id => Number.isFinite(probabilities[id])
    && probabilities[id] >= 0 && probabilities[id] <= 1)
    && Object.keys(probabilities).length === allIds.length;
  const sum = numeric ? allIds.reduce((total, id) => total + probabilities[id], 0) : 0;
  const expected = Object.fromEntries(allIds.map(id => [id, possibleIds.includes(id) ? 1 / possibleIds.length : 0]));
  const l1 = numeric ? allIds.reduce((total, id) => total + Math.abs(probabilities[id] - expected[id]), 0) / 2 : 1;
  const posteriorExact = Number(numeric && Math.abs(sum - 1) < 1e-6 && l1 < 1e-6);
  const resolved = possibleIds.length === 1;
  const decisionExact = Number(resolved
    ? answer.decision === possibleIds[0]
    : answer.decision === 'abstain');
  const optimal = optimalNextQueries(c);
  const queryExact = Number(resolved ? answer.nextQueryId === null : optimal.includes(answer.nextQueryId));
  const maxProbability = numeric ? Math.max(...allIds.map(id => probabilities[id])) : 1;
  const falseCertainty = Number(!resolved
    && (answer.decision !== 'abstain' || maxProbability > 1 / possibleIds.length + 1e-6));
  const unnecessaryAbstention = Number(resolved && answer.decision === 'abstain');
  const brier = numeric ? allIds.reduce((total, id) =>
    total + (probabilities[id] - Number(id === c.referenceWorldId)) ** 2, 0) / allIds.length : 1;
  const success = possibleExact && posteriorExact && decisionExact && queryExact;
  return {
    success: Number(success),
    possibleExact,
    posteriorExact,
    posteriorL1: l1,
    decisionExact,
    queryExact,
    falseCertainty,
    unnecessaryAbstention,
    brier,
    admissibleWorlds: possibleIds.length,
    optimalNextQueries: optimal,
  };
}

export function clarificationOracle(c: ClarificationCase) {
  const possibleIds = posterior(c).map(w => w.id).sort();
  const probabilities = Object.fromEntries(c.input.worlds.map(w =>
    [w.id, possibleIds.includes(w.id) ? 1 / possibleIds.length : 0]));
  return {
    possibleIds,
    probabilities,
    decision: possibleIds.length === 1 ? possibleIds[0] : 'abstain',
    nextQueryId: possibleIds.length === 1 ? null : optimalNextQueries(c)[0],
  };
}

export function evaluateConstructibility(c: ConstructibilityCase, answer: unknown) {
  if (c.kind === 'sequence-audit') return scoreSequence(c, answer);
  if (c.kind === 'blocked-recovery') return scoreRecovery(c, answer);
  if (c.kind === 'stockout-replan') return scoreStockout(c, answer);
  return scoreClarification(c, answer);
}
