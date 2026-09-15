import assert from 'node:assert/strict';
import { type Part, type Structure } from '../shared';
import { cells, dims } from '../geometry';
import { exact, validate } from '../frontier/geometry';
import { frontierModels } from '../frontier/models';
import { admissible, observationCases, scan } from '../frontier2/observation';
import {
  APPROACHES,
  VERSION,
  type Approach,
  type PlacementStep,
  auditPlan,
  executePlacement,
  executeRemoval,
  placementApproaches,
  placementIssue,
  removalApproaches,
  solvePlan,
} from './geometry';

export type ConstructibilityKind =
  | 'sequence-audit'
  | 'blocked-recovery'
  | 'stockout-replan'
  | 'clarify-or-commit';

export interface SequenceCase {
  id: string;
  sourceGroup: string;
  kind: 'sequence-audit';
  variant: 'valid' | 'unsupported-first' | 'clearance-dead-end';
  input: { target: Structure; candidate: { steps: PlacementStep[] } };
  oracle: { firstFailure: number | null; reason: string | null; legalPrefixLength: number; constructible: boolean };
}

export interface ProcessAction {
  op: 'remove' | 'place';
  id: string;
  approach: Approach;
}

export interface RecoveryCase {
  id: string;
  sourceGroup: string;
  kind: 'blocked-recovery';
  tier: number;
  input: {
    target: Structure;
    current: Structure;
    failedStep: PlacementStep;
    continuationIds: string[];
    maxRecoveryActions: number;
  };
  oracle: {
    diagnosis: { failedId: string; reason: 'tool_clearance' };
    recovery: ProcessAction[];
    continuation: PlacementStep[];
  };
}

export interface StockoutCase {
  id: string;
  sourceGroup: string;
  kind: 'stockout-replan';
  input: {
    target: Structure;
    current: Structure;
    unavailableId: string;
    unavailablePart: Part;
    stock: Record<string, number>;
    optimalReplacementPieces: number;
    continuationIds: string[];
  };
  oracle: { placements: Array<{ part: Part; approach: Approach }>; continuation: PlacementStep[] };
}

export interface ClarificationCase {
  id: string;
  sourceGroup: string;
  kind: 'clarify-or-commit';
  variant: 'ambiguous' | 'resolved';
  input: {
    worlds: Array<{ id: string; parts: Part[] }>;
    queries: Array<{ id: string; cost: number; axis: 'x' | 'z'; y: number; fixed: number; start: number; end: number }>;
    observed: Array<{ queryId: string; value: string }>;
    prior: 'uniform';
  };
  referenceWorldId: string;
}

export type ConstructibilityCase = SequenceCase | RecoveryCase | StockoutCase | ClarificationCase;

const summary = (audit: ReturnType<typeof auditPlan>) => ({
  firstFailure: audit.firstFailure,
  reason: audit.reason,
  legalPrefixLength: audit.legalPrefixLength,
  constructible: Boolean(audit.success),
});

const planCache = new Map<string, PlacementStep[]>();
const blockedCache = new Map<string, ReturnType<typeof blockedCandidates>>();
function planFor(sourceGroup: string, parts: Part[]) {
  const old = planCache.get(sourceGroup);
  if (old) return old;
  const plan = solvePlan(parts);
  planCache.set(sourceGroup, plan);
  return plan;
}

function blockedCandidates(parts: Part[]) {
  const levels = [...new Set(parts.map(p => p.y))].sort((a, b) => a - b);
  return levels.flatMap(y => {
    const checkpoint = parts.filter(p => p.y <= y);
    return checkpoint.filter(part => part.y === y
      && placementApproaches(checkpoint.filter(p => p.id !== part.id), part).length === 0
      && validate(checkpoint.filter(p => p.id !== part.id)).length === 0)
      .map(part => ({ part, checkpoint }));
  });
}

function blockedFor(sourceGroup: string, parts: Part[]) {
  const old = blockedCache.get(sourceGroup);
  if (old) return old;
  const result = blockedCandidates(parts);
  blockedCache.set(sourceGroup, result);
  return result;
}

function sequenceCases(): SequenceCase[] {
  return frontierModels().flatMap(model => {
    const target = model.structure.parts;
    const good = planFor(model.id, target);
    const elevated = [...target].filter(p => p.y > 0).sort((a, b) => b.y - a.y || a.id.localeCompare(b.id))[0];
    const unsupported = [{ id: elevated.id, approach: APPROACHES[0] }, ...good.filter(s => s.id !== elevated.id)];
    const blocked = blockedFor(model.id, target);
    assert.ok(blocked.length >= 3, `${model.id}: insufficient enclosed positions`);
    const chosen = blocked[Math.floor(blocked.length / 2)];
    const delayed = chosen.part;
    const before = solvePlan(chosen.checkpoint.filter(p => p.id !== delayed.id));
    const clearance = [...before, { id: delayed.id, approach: APPROACHES[0] }];
    const definitions = [
      ['valid', good],
      ['unsupported-first', unsupported],
      ['clearance-dead-end', clearance],
    ] as const;
    return definitions.map(([variant, steps]) => {
      const audit = auditPlan(target, { steps });
      if (variant === 'valid') assert.equal(audit.success, 1);
      else assert.equal(audit.success, 0);
      if (variant === 'unsupported-first') assert.equal(audit.reason, 'support');
      if (variant === 'clearance-dead-end') assert.equal(audit.reason, 'tool_clearance');
      return {
        id: `c1-${model.id}-sequence-${variant}`,
        sourceGroup: model.id,
        kind: 'sequence-audit' as const,
        variant,
        input: { target: model.structure, candidate: { steps } },
        oracle: summary(audit),
      };
    });
  });
}

function findPlacementOrder(state: Part[], missing: Part[]) {
  const visit = (current: Part[], left: Part[], steps: PlacementStep[]): PlacementStep[] | null => {
    if (!left.length) return steps;
    for (const part of left) for (const approach of placementApproaches(current, part)) {
      const next = executePlacement(current, part, approach);
      if (next.issue) continue;
      const result = visit(next.parts, left.filter(p => p.id !== part.id), [...steps, { id: part.id, approach }]);
      if (result) return result;
    }
    return null;
  };
  return visit(state, missing, []);
}

function minimumRecovery(current: Part[], missing: Part) {
  const queue: Array<{ state: Part[]; removed: Array<{ part: Part; approach: Approach }> }> = [
    { state: current, removed: [] },
  ];
  const seen = new Set(['']);
  for (let cursor = 0; cursor < queue.length; cursor++) {
    const node = queue[cursor];
    const placements = findPlacementOrder(node.state, [missing, ...node.removed.map(r => r.part)]);
    if (placements) {
      return {
        actions: [
          ...node.removed.map(r => ({ op: 'remove' as const, id: r.part.id, approach: r.approach })),
          ...placements.map(step => ({ op: 'place' as const, ...step })),
        ],
        removed: node.removed.length,
      };
    }
    if (node.removed.length >= 4) continue;
    for (const part of node.state.filter(p => p.y === missing.y)) {
      const approaches = removalApproaches(node.state, part.id);
      if (!approaches.length) continue;
      const ids = [...node.removed.map(r => r.part.id), part.id].sort();
      const key = ids.join('|');
      if (seen.has(key)) continue;
      seen.add(key);
      const next = executeRemoval(node.state, part.id, approaches[0]);
      if (!next.issue) queue.push({ state: next.parts,
        removed: [...node.removed, { part, approach: approaches[0] }] });
    }
  }
  throw new Error(`no_recovery:${missing.id}`);
}

function recoveryCases(): RecoveryCase[] {
  return frontierModels().flatMap(model => {
    const target = model.structure.parts, fullPlan = planFor(model.id, target);
    const candidates = blockedFor(model.id, target);
    assert.ok(candidates.length >= 3);
    const selected = [candidates[0], candidates[Math.floor(candidates.length / 2)], candidates.at(-1)!];
    return selected.map(({ part: failed, checkpoint }, tier) => {
      const current = checkpoint.filter(p => p.id !== failed.id);
      const recovery = minimumRecovery(current, failed);
      assert.ok(recovery.removed > 0);
      const checkpointIds = new Set(checkpoint.map(p => p.id));
      const continuation = fullPlan.filter(s => !checkpointIds.has(s.id)).slice(0, 12);
      let state = [...current];
      for (const action of recovery.actions) {
        if (action.op === 'remove') state = executeRemoval(state, action.id, action.approach).parts;
        else state = executePlacement(state, target.find(p => p.id === action.id)!, action.approach).parts;
      }
      assert.ok(exact(checkpoint, state));
      for (const step of continuation) {
        const result = executePlacement(state, target.find(p => p.id === step.id)!, step.approach);
        assert.equal(result.issue, null); state = result.parts;
      }
      return {
        id: `c1-${model.id}-recovery-${tier}`,
        sourceGroup: model.id,
        kind: 'blocked-recovery' as const,
        tier,
        input: {
          target: model.structure,
          current: { version: 1 as const, parts: current },
          failedStep: { id: failed.id, approach: APPROACHES[0] },
          continuationIds: continuation.map(s => s.id),
          maxRecoveryActions: recovery.actions.length,
        },
        oracle: {
          diagnosis: { failedId: failed.id, reason: 'tool_clearance' as const },
          recovery: recovery.actions,
          continuation,
        },
      };
    });
  });
}

function replacementCandidates(original: Part) {
  return [
    { id: `${original.id}-sub-a`, partId: '3031', color: original.color,
      x: original.x, y: original.y, z: original.z, turn: 0 },
    { id: `${original.id}-sub-b`, partId: '3031', color: original.color,
      x: original.x + 4, y: original.y, z: original.z, turn: 0 },
  ] satisfies Part[];
}

function stockoutCases(): StockoutCase[] {
  return frontierModels().map(model => {
    const target = model.structure.parts, plan = planFor(model.id, target);
    const eligible = plan.map((step, index) => ({ step, index, part: target.find(p => p.id === step.id)! }))
      .filter(x => x.part.y === 0 && x.part.partId === '3035' && x.index >= 2);
    let chosen: typeof eligible[number] | undefined;
    let placements: Array<{ part: Part; approach: Approach }> | undefined;
    for (const candidate of eligible) {
      const current = plan.slice(0, candidate.index).map(s => target.find(p => p.id === s.id)!);
      const replacement = replacementCandidates(candidate.part);
      const order = findPlacementOrder(current, replacement);
      if (!order) continue;
      chosen = candidate;
      placements = order.map(step => ({ part: replacement.find(p => p.id === step.id)!, approach: step.approach }));
      break;
    }
    assert.ok(chosen && placements, `${model.id}: no stockout witness`);
    const current = plan.slice(0, chosen.index).map(s => target.find(p => p.id === s.id)!);
    const continuation = plan.slice(chosen.index + 1, chosen.index + 13);
    let state = [...current];
    for (const step of placements) {
      const result = executePlacement(state, step.part, step.approach);
      assert.equal(result.issue, null); state = result.parts;
    }
    for (const step of continuation) {
      const result = executePlacement(state, target.find(p => p.id === step.id)!, step.approach);
      assert.equal(result.issue, null); state = result.parts;
    }
    return {
      id: `c1-${model.id}-stockout`,
      sourceGroup: model.id,
      kind: 'stockout-replan' as const,
      input: {
        target: model.structure,
        current: { version: 1 as const, parts: current },
        unavailableId: chosen.part.id,
        unavailablePart: chosen.part,
        stock: { '3031': 2, '3020': 4, '3710': 8 },
        optimalReplacementPieces: 2,
        continuationIds: continuation.map(s => s.id),
      },
      oracle: { placements, continuation },
    };
  });
}

function resolvedObservations(c: ReturnType<typeof observationCases>[number]) {
  const world = c.input.worlds.find(w => w.id === c.referenceWorldId)!;
  const observed = [...c.input.observed];
  for (const query of c.input.queries) {
    if (observed.some(o => o.queryId === query.id)) continue;
    observed.push({ queryId: query.id, value: scan(world.parts, query) });
    if (admissible({ ...c.input, observed }).length === 1) break;
  }
  assert.equal(admissible({ ...c.input, observed }).length, 1);
  return observed;
}

function clarificationCases(): ClarificationCase[] {
  return observationCases().flatMap(c => (['ambiguous', 'resolved'] as const).map(variant => ({
    id: `c1-${c.id.replace(/^f2-/, '')}-clarification-${variant}`,
    sourceGroup: c.sourceGroup,
    kind: 'clarify-or-commit' as const,
    variant,
    input: {
      worlds: c.input.worlds,
      queries: c.input.queries,
      observed: variant === 'ambiguous' ? c.input.observed : resolvedObservations(c),
      prior: 'uniform' as const,
    },
    referenceWorldId: c.referenceWorldId,
  })));
}

let cached: ConstructibilityCase[] | undefined;
export function constructibilityCases() {
  if (cached) return cached;
  cached = [...sequenceCases(), ...recoveryCases(), ...stockoutCases(), ...clarificationCases()];
  assert.equal(cached.length, 78);
  return cached;
}

export function publicCase(c: ConstructibilityCase) {
  const common = { version: VERSION, id: c.id, sourceGroup: c.sourceGroup, kind: c.kind };
  if (c.kind === 'sequence-audit') return { ...common,
    prompt: `Audit the supplied candidate construction sequence under the declared nominal support and
one-stud tool-clearance contract. Return {firstFailure,reason,legalPrefixLength,constructible}.
firstFailure is zero-based or null. Do not reorder or repair the candidate.`,
    input: c.input,
  };
  if (c.kind === 'blocked-recovery') return { ...common,
    prompt: `The next placement failed. Diagnose its first failure, perform the minimum number of
clearance-aware remove/place actions needed to restore the checkpoint, then place every continuationId
exactly once in any legal order. Return {diagnosis:{failedId,reason},recovery:[{op,id,approach}],
continuation:[{id,approach}]}. Placement geometry comes from target. Removal and placement require
a clear one-stud side strip named west/east/north/south. Do not alter any other part.`,
    input: c.input,
  };
  if (c.kind === 'stockout-replan') return { ...common,
    prompt: `The unavailable target part cannot be used. Cover exactly its occupied region at the same
height and color with available stock, using the minimum piece count and legal tool-clearance approaches,
then place every continuationId exactly once. Return
{placements:[{part:{id,partId,color,x,y,z,turn},approach}],continuation:[{id,approach}]}.
Replacement IDs must be new and unique.`,
    input: c.input,
  };
  return { ...common,
    prompt: `Candidate worlds have a uniform prior. Condition on every supplied scan observation.
Return {possibleIds,probabilities,decision,nextQueryId}. probabilities maps every candidate world ID
to its posterior probability and must sum to one. decision is the unique world ID when resolved,
otherwise "abstain". If unresolved, nextQueryId must maximize expected entropy reduction per unit cost
among unobserved queries; ties are accepted. If resolved, nextQueryId is null.`,
    input: c.input,
  };
}

export const cellSignature = (parts: Part[]) => [...cells(parts)].sort();
export const regionSignature = (part: Part) => cellSignature([part]);
export const validateStructure = (parts: Part[]) => validate(parts);
export const exactStructure = (a: Part[], b: Part[]) => exact(a, b);
export const partDimensions = (part: Part) => dims(part);
export const checkPlacement = (parts: Part[], part: Part, approach: Approach) =>
  placementIssue(parts, part, approach);
