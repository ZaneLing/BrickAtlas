import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { type Part, type Structure } from '../shared';
import { dims, footprint, key } from '../geometry';
import { frontierModels } from '../frontier/models';
import { accessClosure, exact, insertion, parseStructure, removal, validate } from '../frontier/geometry';
import { sameSet } from '../frontier/tasks';

export const VERSION = 'brickatlas-diagnostic-2';
export interface Action { op: 'remove' | 'place'; id: string; part?: Part }
export interface Diagnosis { faultIds: string[]; replacements: Part[] }
export interface Access { removeIds: string[]; order: string[] }
export interface Repair { actions: Action[] }
export type Condition = 'symbolic' | 'layers';
export interface MaintenanceCase {
  id: string; sourceGroup: string; tier: number; context: 'local' | 'full';
  current: Structure; target: Structure; faultIds: string[];
  referenceAssets: Array<{ path: string; bottomY: number }>;
  oracle: { diagnosis: Diagnosis; access: Access; repair: Repair };
  factors: { totalParts: number; relevantParts: number; faultCount: number; accessDepth: number; optimalActions: number };
}

function localContext(parts: Part[], ids: string[]) {
  const selected = new Set(accessClosure(parts, ids).map(p => p.id));
  for (const p of [...parts].sort((a, b) => b.y - a.y)) {
    if (!selected.has(p.id)) continue;
    for (const q of parts) if (q.y + dims(q).h === p.y && footprint(p, q)) selected.add(q.id);
  }
  return parts.filter(p => selected.has(p.id));
}
const opaque = (group: string, id: string) => 'p' + createHash('sha256').update(group + '/' + id).digest('hex').slice(0, 12);
let cached: MaintenanceCase[] | undefined;
export function maintenanceCases() {
  if (cached) return cached;
  cached = frontierModels().flatMap((model, mi) => {
    const parts = model.structure.parts.map(p => ({ ...p, id: opaque(model.id, p.id) }))
      .sort((a, b) => a.id.localeCompare(b.id));
    const options = parts.filter(p => p.y >= 3).map(p => ({ p, n: accessClosure(parts, [p.id]).length }))
      .sort((a, b) => a.n - b.n || a.p.id.localeCompare(b.p.id));
    return [0, 1, 2].flatMap(tier => {
      const faultCount = mi === 0 && tier === 0 ? 0 : tier + 1;
      const picked = options.slice(Math.floor((options.length - 4) * [0, .5, .9][tier]),
        Math.floor((options.length - 4) * [0, .5, .9][tier]) + Math.max(1, faultCount));
      const focusIds = picked.map(x => x.p.id), faultIds = focusIds.slice(0, faultCount);
      const neighborhood = localContext(parts, focusIds);
      return (['local', 'full'] as const).map(context => {
        const target: Structure = { version: 1, parts: context === 'full' ? parts : neighborhood };
        const current: Structure = { version: 1, parts: target.parts.map(p => faultIds.includes(p.id)
          ? { ...p, color: p.color === 'red' ? 'blue' as const : 'red' as const } : { ...p }) };
        assert.deepEqual(validate(current.parts), []);
        const closure = accessClosure(current.parts, faultIds);
        const actions: Action[] = [...closure.map(p => ({ op: 'remove' as const, id: p.id })),
          ...[...closure].reverse().map(p => ({ op: 'place' as const, id: p.id,
            ...(faultIds.includes(p.id) ? { part: target.parts.find(q => q.id === p.id)! } : {}) }))];
        const id = `f2-${model.id}-maintenance-${tier}-${context}`;
        const levels = [...new Set(target.parts.map(p => p.y))].sort((a, b) => a - b);
        return { id, sourceGroup: model.id, tier, context, current, target, faultIds,
          referenceAssets: levels.map(y => ({ path: `images/${id}-layer-${y}.png`, bottomY: y })),
          oracle: { diagnosis: { faultIds, replacements: target.parts.filter(p => faultIds.includes(p.id)) },
            access: { removeIds: closure.map(p => p.id), order: closure.map(p => p.id) }, repair: { actions } },
          factors: { totalParts: current.parts.length, relevantParts: closure.length, faultCount,
            accessDepth: new Set(closure.map(p => p.y)).size, optimalActions: actions.length } };
      });
    });
  });
  return cached;
}

export function publicMaintenance(c: MaintenanceCase, condition: Condition) {
  return {
    version: VERSION, id: `${c.id}-${condition}`, sourceGroup: c.sourceGroup, condition,
    prompt: `Diagnose the current assembly against the supplied reference, certify the minimum access set,
and repair it under vertical-only removal/insertion. Return {diagnosis:{faultIds,replacements},
access:{removeIds,order},repair:{actions:[{op,id,part?}]}}. Coordinates are integer studs X/Z and plate heights Y.
Each elevated part needs direct support; overlapping overhead parts block vertical access.
No in-place repaint. Remove puts an instance into inventory. Place consumes it at its current pose,
or at the optional supplied replacement Part with the SAME ID. Unknown IDs and repeated placements fail.
Final structure and original IDs must be restored; minimum action count is scored separately.
No-fault cases require empty fault, access and action sets. All three stages see identical evidence.
For layers, reference top views disclose all parts at each bottom Y. Images show an X/Z grid with
X right, Z down, origin and unit spacing marked. Reference instance IDs are not drawn.
This is nominal grid maintenance, not force simulation or robot control.`,
    input: { current: c.current, ...(condition === 'symbolic' ? { reference: c.target } : {
      referenceImages: c.referenceAssets, referenceCondition: 'calibrated-bottom-Y-layers',
      projection: { originPixels: [60, 100], pixelsPerStud: 20, xDirection: 'right', zDirection: 'down' },
    }) },
  };
}

export function scoreMaintenance(c: MaintenanceCase, raw: any) {
  const d = raw?.diagnosis, a = raw?.access, r = raw?.repair;
  const empty = { success: 0, diagnosisExact: 0, accessExact: 0, repairExact: 0, minimumRepair: 0,
    coherent: 0, allCorrectAndCoherent: 0, actions: 0, legalActions: 0, issues: [] as string[] };
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return { ...empty, issues: ['format'] };
  const issues: string[] = [];
  const expected = c.oracle.access.removeIds;
  const patches = parseStructure({ version: 1, parts: d?.replacements });
  const diagnosisExact = Boolean(patches && sameSet(d?.faultIds, c.faultIds)
    && sameSet(patches.parts.map(p => p.id), c.faultIds)
    && patches.parts.every(p => key(p) === key(c.target.parts.find(q => q.id === p.id)!)));
  let accessExact = sameSet(a?.removeIds, expected) && sameSet(a?.order, expected);
  if (accessExact) {
    let state = [...c.current.parts];
    for (const id of a.order) {
      if (removal(state, id)) { accessExact = false; break; }
      state = state.filter(p => p.id !== id);
    }
  }
  let state = [...c.current.parts], legalActions = 0, legal = Array.isArray(r?.actions) && r.actions.length <= 2048;
  const inventory = new Map<string, Part>(), removed = new Set<string>();
  if (legal) for (const action of r.actions) {
    if (!action || typeof action !== 'object' || typeof action.id !== 'string'
      || !['remove', 'place'].includes(action.op)) { legal = false; issues.push('action_schema'); break; }
    if (action.op === 'remove') {
      if (removal(state, action.id)) { legal = false; issues.push('illegal_remove'); break; }
      inventory.set(action.id, state.find(p => p.id === action.id)!); removed.add(action.id);
      state = state.filter(p => p.id !== action.id);
    } else {
      const old = inventory.get(action.id);
      const part = action.part === undefined ? old : parseStructure({ version: 1, parts: [action.part] })?.parts[0];
      if (!old || !part || part.id !== action.id || insertion(state, part)) {
        legal = false; issues.push('illegal_place'); break;
      }
      state.push(part); inventory.delete(action.id);
    }
    legalActions++;
  }
  const repairExact = legal && inventory.size === 0 && exact(c.target.parts, state)
    && c.target.parts.every(p => state.some(q => q.id === p.id && key(q) === key(p)));
  const actionCount = Array.isArray(r?.actions) ? r.actions.length : 0;
  const minimumRepair = repairExact && actionCount === c.factors.optimalActions;
  // Coherence is evaluated independently from correctness, so consistently wrong answers are visible.
  const idsValid = Array.isArray(d?.faultIds) && d.faultIds.every((id: unknown) =>
    typeof id === 'string' && c.current.parts.some(p => p.id === id))
    && new Set(d.faultIds).size === d.faultIds.length;
  const predictedClosure = idsValid ? accessClosure(c.current.parts, d.faultIds).map(p => p.id) : [];
  const coherent = Boolean(idsValid && sameSet(a?.removeIds, predictedClosure)
    && sameSet([...removed], predictedClosure) && legal && patches
    && sameSet(patches.parts.map(p => p.id), d.faultIds)
    && patches.parts.every(p => state.some(q => q.id === p.id && key(q) === key(p))));
  const all = diagnosisExact && accessExact && minimumRepair && coherent;
  if (!diagnosisExact) issues.push('diagnosis'); if (!accessExact) issues.push('access');
  if (!repairExact) issues.push('final'); if (!minimumRepair) issues.push('nonminimal_or_incomplete');
  return { success: Number(all), diagnosisExact: Number(diagnosisExact), accessExact: Number(accessExact),
    repairExact: Number(repairExact), minimumRepair: Number(minimumRepair), coherent: Number(coherent),
    allCorrectAndCoherent: Number(all), actions: actionCount, legalActions, issues };
}

export function solveSymbolic(input: { current: Structure; reference: Structure }) {
  const faultIds = input.current.parts.filter(p => {
    const q = input.reference.parts.find(q => q.id === p.id);
    return !q || key(p) !== key(q);
  }).map(p => p.id);
  const closure = accessClosure(input.current.parts, faultIds), replacements = input.reference.parts.filter(p => faultIds.includes(p.id));
  return { diagnosis: { faultIds, replacements },
    access: { removeIds: closure.map(p => p.id), order: closure.map(p => p.id) },
    repair: { actions: [...closure.map(p => ({ op: 'remove', id: p.id })),
      ...[...closure].reverse().map(p => ({ op: 'place', id: p.id,
        ...(faultIds.includes(p.id) ? { part: replacements.find(q => q.id === p.id)! } : {}) }))] } };
}
