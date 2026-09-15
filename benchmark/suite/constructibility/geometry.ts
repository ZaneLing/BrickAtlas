import { type Part } from '../shared';
import { dims, footprint } from '../geometry';
import { LIMITS, exact, validate } from '../frontier/geometry';

export const VERSION = 'brickatlas-constructibility-1';
export const APPROACHES = ['west', 'east', 'north', 'south'] as const;
export type Approach = typeof APPROACHES[number];
export interface PlacementStep { id: string; approach: Approach }

export interface PlanAudit {
  success: number;
  complete: number;
  firstFailure: number | null;
  reason: string | null;
  legalPrefixLength: number;
  legalPrefixRate: number;
  prefixSupportScore: number;
  minimumSupportFraction: number;
  accessibleStepRate: number;
  finalParts: Part[];
}

const overlap = (a0: number, a1: number, b0: number, b1: number) =>
  Math.max(a0, b0) < Math.min(a1, b1);

function sideStrip(part: Part, approach: Approach) {
  const d = dims(part);
  if (approach === 'west') return { x0: part.x - 1, x1: part.x, z0: part.z, z1: part.z + d.d };
  if (approach === 'east') return { x0: part.x + d.w, x1: part.x + d.w + 1, z0: part.z, z1: part.z + d.d };
  if (approach === 'north') return { x0: part.x, x1: part.x + d.w, z0: part.z - 1, z1: part.z };
  return { x0: part.x, x1: part.x + d.w, z0: part.z + d.d, z1: part.z + d.d + 1 };
}

function bodyIssue(parts: Part[], part: Part) {
  if (parts.some(p => p.id === part.id)) return 'duplicate';
  const d = dims(part);
  if ([part.x, part.y, part.z].some(v => !Number.isInteger(v) || v < 0 || v > LIMITS.coordinate)
    || part.x + d.w > LIMITS.extent || part.y + d.h > LIMITS.extent || part.z + d.d > LIMITS.extent) {
    return 'bounds';
  }
  if (parts.some(p => footprint(p, part) > 0
    && p.y < part.y + d.h && part.y < p.y + dims(p).h)) return 'collision';
  if (part.y > 0 && !parts.some(p => p.y + dims(p).h === part.y && footprint(p, part) > 0)) {
    return 'support';
  }
  if (parts.some(p => p.y >= part.y + d.h && footprint(p, part) > 0)) return 'body_path';
  return null;
}

/**
 * A one-stud side strip models room for a top-down placement tool to release
 * the part. It is a deterministic accessibility proxy, not robot kinematics.
 */
export function placementIssue(parts: Part[], part: Part, approach: Approach) {
  if (!APPROACHES.includes(approach)) return 'approach';
  const issue = bodyIssue(parts, part);
  if (issue) return issue;
  const strip = sideStrip(part, approach);
  const blocked = parts.some(p => {
    const d = dims(p);
    return p.y + d.h > part.y
      && overlap(p.x, p.x + d.w, strip.x0, strip.x1)
      && overlap(p.z, p.z + d.d, strip.z0, strip.z1);
  });
  return blocked ? 'tool_clearance' : null;
}

export function placementApproaches(parts: Part[], part: Part) {
  return APPROACHES.filter(approach => !placementIssue(parts, part, approach));
}

export function removalIssue(parts: Part[], id: string, approach: Approach) {
  const part = parts.find(p => p.id === id);
  if (!part) return 'unknown';
  if (!APPROACHES.includes(approach)) return 'approach';
  const d = dims(part), strip = sideStrip(part, approach);
  if (parts.some(p => p.id !== id && p.y >= part.y + d.h && footprint(p, part) > 0)) return 'body_path';
  if (parts.some(p => p.id !== id && p.y + dims(p).h > part.y
    && overlap(p.x, p.x + dims(p).w, strip.x0, strip.x1)
    && overlap(p.z, p.z + dims(p).d, strip.z0, strip.z1))) return 'tool_clearance';
  return null;
}

export function removalApproaches(parts: Part[], id: string) {
  return APPROACHES.filter(approach => !removalIssue(parts, id, approach));
}

export function supportFraction(parts: Part[], part: Part) {
  if (part.y === 0) return 1;
  const area = dims(part).w * dims(part).d;
  return Math.min(1, parts.filter(p => p.id !== part.id && p.y + dims(p).h === part.y)
    .reduce((sum, p) => sum + footprint(p, part), 0) / area);
}

export function auditPlan(target: Part[], raw: unknown): PlanAudit {
  const parsed = (raw as { steps?: unknown })?.steps;
  const empty: PlanAudit = { success: 0, complete: 0, firstFailure: 0, reason: 'format',
    legalPrefixLength: 0, legalPrefixRate: 0, prefixSupportScore: 0,
    minimumSupportFraction: 0, accessibleStepRate: 0, finalParts: [] };
  if (!Array.isArray(parsed) || parsed.length > LIMITS.parts) return empty;
  const steps: unknown[] = parsed;
  let state: Part[] = [], legal = 0;
  const support: number[] = [];
  for (let index = 0; index < steps.length; index++) {
    const step = steps[index] as PlacementStep;
    if (!step || typeof step.id !== 'string' || !APPROACHES.includes(step.approach)) {
      return finish(index, 'format');
    }
    const part = target.find(p => p.id === step.id);
    if (!part) return finish(index, 'unknown');
    const issue = placementIssue(state, part, step.approach);
    if (issue) return finish(index, issue);
    state.push({ ...part }); legal++;
    support.push(supportFraction(state, part));
  }
  return finish(null, null);

  function finish(firstFailure: number | null, reason: string | null): PlanAudit {
    const complete = Number(firstFailure === null && steps.length === target.length && exact(target, state));
    const rate = legal / Math.max(1, target.length);
    return {
      success: Number(complete && validate(state).length === 0),
      complete,
      firstFailure,
      reason,
      legalPrefixLength: legal,
      legalPrefixRate: rate,
      prefixSupportScore: support.reduce((sum, value) => sum + value, 0) / Math.max(1, support.length),
      minimumSupportFraction: support.length ? Math.min(...support) : 0,
      accessibleStepRate: rate,
      finalParts: state,
    };
  }
}

export function solvePlan(parts: Part[]): PlacementStep[] {
  const centerX = Math.max(...parts.map(p => p.x + dims(p).w)) / 2;
  const centerZ = Math.max(...parts.map(p => p.z + dims(p).d)) / 2;
  const remaining = [...parts];
  const state: Part[] = [], steps: PlacementStep[] = [];
  while (remaining.length) {
    const ranked = [...remaining].sort((a, b) => {
      const da = (a.x + dims(a).w / 2 - centerX) ** 2 + (a.z + dims(a).d / 2 - centerZ) ** 2;
      const db = (b.x + dims(b).w / 2 - centerX) ** 2 + (b.z + dims(b).d / 2 - centerZ) ** 2;
      return a.y - b.y || da - db || a.id.localeCompare(b.id);
    });
    const next = ranked.map(part => ({ part, approaches: placementApproaches(state, part) }))
      .find(candidate => candidate.approaches.length);
    if (!next) throw new Error(`no_accessible_plan:${remaining.length}`);
    const approach = next.approaches[0];
    steps.push({ id: next.part.id, approach });
    state.push({ ...next.part });
    remaining.splice(remaining.findIndex(p => p.id === next.part.id), 1);
  }
  const audit = auditPlan(parts, { steps });
  if (!audit.success) throw new Error(`invalid_constructibility_plan:${audit.firstFailure}:${audit.reason}`);
  return steps;
}

export function executeRemoval(parts: Part[], id: string, approach: Approach) {
  const issue = removalIssue(parts, id, approach);
  return { issue, parts: issue ? parts : parts.filter(p => p.id !== id) };
}

export function executePlacement(parts: Part[], part: Part, approach: Approach) {
  const issue = placementIssue(parts, part, approach);
  return { issue, parts: issue ? parts : [...parts, { ...part }] };
}
