import assert from 'node:assert/strict';
import { type Part } from '../shared';
import { dims, footprint } from '../geometry';
import { accessClosure, cascade, FRONTIER_VERSION, RULES, schedule } from './geometry';
import { frontierModels, type FrontierModel } from './models';

export const KINDS = ['service-plan', 'access-certificate', 'parallel-schedule', 'minimal-intervention',
  'inventory-cover', 'ambiguity-set', 'inspection-policy', 'distributed-repair'] as const;
export type FrontierKind = typeof KINDS[number];
export interface FrontierTask {
  id: string; modelId: string; kind: FrontierKind; prompt: string;
  input: Record<string, any>; oracle: any; negative: any; highlight: string[];
}
export const sorted = (ids: string[]) => [...ids].sort();
export const sameSet = (a: unknown, b: string[]) => Array.isArray(a)
  && a.every(x => typeof x === 'string') && new Set(a).size === a.length
  && JSON.stringify(sorted(a)) === JSON.stringify(sorted(b));
export function subsets<T>(xs: T[]): T[][] {
  return xs.reduce<T[][]>((out, x) => [...out, ...out.map(s => [...s, x])], [[]]);
}

export function hypotheses(slots: Part[]) {
  return Array.from({ length: 2 ** slots.length }, (_, i) => ({
    id: `h${i}`, layouts: Object.fromEntries(slots.map((p, k) => [p.id, (i >> k) & 1 ? 'crosswise' : 'lengthwise'])),
  }));
}
export function slabTiles(p: Part, mode: string): Part[] {
  const offsets = mode === 'lengthwise'
    ? [0, 4].flatMap(x => [0, 2].map(z => ({ x, z, turn: 0 })))
    : [0, 2, 4, 6].map(x => ({ x, z: 0, turn: 1 }));
  return offsets.map((o, i) => ({ ...p, id: `${p.id}-tile${i}`, partId: '3020',
    x: p.x + o.x, z: p.z + o.z, turn: o.turn }));
}

function task(model: FrontierModel, kind: FrontierKind, prompt: string, input: Record<string, any>,
  oracle: any, negative: any, highlight: string[]): FrontierTask {
  return { id: `${FRONTIER_VERSION}-${model.id}-${kind}`, modelId: model.id, kind,
    prompt: RULES + '\n' + prompt, input, oracle, negative, highlight };
}

export function modelTasks(model: FrontierModel): FrontierTask[] {
  const parts = model.structure.parts;
  // Pick buried service targets by geometric access burden, never by model outcomes.
  const candidates = parts.filter(p => p.y >= 3 && p.y <= 9).map(p => ({ p, closure: accessClosure(parts, [p.id]) }))
    .filter(x => x.closure.length >= 4 && x.closure.length <= 40)
    .sort((a, b) => b.closure.length - a.closure.length || a.p.id.localeCompare(b.p.id));
  assert.ok(candidates.length, model.id);
  const target = candidates[0].p, closure = candidates[0].closure;
  const source = parts.map(p => p.id === target.id ? { ...p, color: p.color === 'red' ? 'blue' as const : 'red' as const } : { ...p });
  const actions = [...closure.map(p => ({ op: 'remove', id: p.id })),
    ...[...closure].reverse().map(p => ({ op: 'place', id: p.id }))];
  const common = { current: { version: 1, parts: source }, target: model.structure, serviceIds: [target.id] };
  const tasks = [
    task(model, 'service-plan',
      'Replace the marked buried component and restore the entire target. Only remove/place by ID; place uses the target inventory pose/color. Minimize action count. Every intermediate state must remain valid. Output {actions:[{op,id}]}.',
      { ...common, maxActions: actions.length, actionCosts: { remove: 1, place: 1 } },
      { actions }, { actions: [{ op: 'remove', id: target.id }, { op: 'place', id: target.id }] }, [target.id]),
    task(model, 'access-certificate',
      'Return the minimum set of IDs that must be removed to access every service ID, including the service IDs. Also certify an executable removal order. Output {removeIds,order}; no detached group moves.',
      { structure: model.structure, serviceIds: [target.id] },
      { removeIds: closure.map(p => p.id), order: closure.map(p => p.id) },
      { removeIds: [target.id], order: [target.id] }, closure.map(p => p.id)),
  ];
  const workers = 4, batches = schedule(parts, workers);
  tasks.push(task(model, 'parallel-schedule',
    'Schedule all IDs in synchronous rounds with four abstract workers. Prerequisites are every lower part whose footprint overlaps; ALL must be in earlier rounds. At most four IDs per round; each ID once. Return {batches:[IDs]}. Report makespan; optimality is not required and no robot motion is modeled.',
    { structure: model.structure, workers, precedence: 'all-lower-overlap' }, { batches },
    { batches: [parts.map(p => p.id)] }, []));
  const top = [...parts].filter(p => p.y > 3).sort((a, b) => b.y - a.y)
    .find(p => parts.filter(q => q.y + dims(q).h === p.y && footprint(p, q)).length >= 2)!;
  assert.ok(top, model.id);
  const supports = parts.filter(q => q.y + dims(q).h === top.y && footprint(top, q));
  const pool = [...supports, ...parts.filter(p => p.y === supports[0].y && !supports.includes(p)).slice(0, 2)].slice(0, 12);
  const validCuts = subsets(pool.map(p => p.id)).filter(ids => cascade(parts, ids).includes(top.id));
  const min = Math.min(...validCuts.map(s => s.length)), cut = validCuts.find(s => s.length === min)!;
  tasks.push(task(model, 'minimal-intervention',
    'Choose a minimum-cardinality subset of allowed IDs whose forced simultaneous deletion makes the goal disappear under iterative zero-direct-support propagation. Forced deletions ignore access, and this is NOT force simulation. Output {removeIds,cascadeIds}, where cascadeIds includes forced deletions.',
    { structure: model.structure, allowedIds: pool.map(p => p.id), goalId: top.id },
    { removeIds: cut, cascadeIds: cascade(parts, cut) }, { removeIds: [], cascadeIds: [] }, [top.id, ...pool.map(p => p.id)]));
  const roof = [...parts].reverse().find(p => p.partId === '3035')!;
  const fullTiles = [0, 4].flatMap(dx => [0, 2].map(dz => ({ partId: '3020', x: dx, z: dz, turn: 0 })));
  const largeStock = 1 + model.stats.parts % 3;
  const tiles = fullTiles.flatMap((t, i) => i < largeStock ? [t] : [
    { partId: '3022', x: t.x, z: t.z, turn: 0 }, { partId: '3022', x: t.x + 2, z: t.z, turn: 0 },
  ]);
  tasks.push(task(model, 'inventory-cover',
    'Retile the marked 8x4 plate footprint using ONLY the stated stock. Coordinates are local X/Z offsets; all plates share the replaced plate bottom Y, color and height. Cover every cell exactly once, without protrusion. Minimize number of pieces; accept any optimal tiling. Output {tiles:[{partId,x,z,turn}]}. Only occupied slab equivalence is claimed, not identical seams or stud connectivity.',
    { structure: model.structure, replaceId: roof.id, region: { w: 8, d: 4 },
      stock: { '3020': largeStock, '3022': (4 - largeStock) * 2, '3023': 4 }, maxTiles: 12 },
    { tiles }, { tiles: tiles.slice(1) }, [roof.id]));
  const slots = parts.filter(p => p.partId === '3035' && p.turn === 0 && p.y === 0).slice(0, 3);
  const hidden = slots.map(p => p.id);
  assert.equal(hidden.length, 3);
  const hs = hypotheses(slots);
  const known = parts.filter(p => !hidden.includes(p.id));
  const grammar = slots.map(p => ({ id: p.id, alternatives: {
    lengthwise: slabTiles(p, 'lengthwise'), crosswise: slabTiles(p, 'crosswise'),
  } }));
  const queries = hidden.map((id, i) => ({ id: `q${i}`, cost: i + 1,
    returns: Object.fromEntries(hs.map(h => [h.id, h.layouts[id]])) }));
  queries.push({ id: 'q-all', cost: 9, returns: Object.fromEntries(hs.map(h => [h.id, h.id])) });
  tasks.push(task(model, 'ambiguity-set',
    'The three marked foundation slabs each admit two four-brick tilings with the same colored occupied cells and BOM but different internal seams. Only knownStructure, finite grammar and the stated seam observation are disclosed; there is no seam RGB. Return {possibleIds} for EVERY compatible layout assignment. Do not choose one arbitrary hidden topology.',
    { knownStructure: { version: 1, parts: known }, grammar, hypotheses: hs, observations: { [hidden[0]]: 'lengthwise' } },
    { possibleIds: hs.filter(h => h.layouts[hidden[0]] === 'lengthwise').map(h => h.id) },
    { possibleIds: ['h0'] }, hidden));
  const policy = (depth: number, active: typeof hs): any => depth === hidden.length
    ? { hypothesisId: active[0].id }
    : { queryId: `q${depth}`, branches: Object.fromEntries(['lengthwise', 'crosswise'].map(layout => [
      layout, policy(depth + 1, active.filter(h => h.layouts[hidden[depth]] === layout)),
    ])) };
  tasks.push(task(model, 'inspection-policy',
    'Return a contingent policy that identifies every admissible hidden assignment: {queryId,branches:{returnedValue:subpolicy}} or leaf {hypothesisId}. Query table and costs are public; one query per node, no repeated query on a path. Worst-case total cost <=6. All eight worlds are scored, not just one lucky trace.',
    { knownStructure: { version: 1, parts: known }, grammar, hypotheses: hs.map(h => h.id), queries, budget: 6 },
    policy(0, hs), { hypothesisId: 'h0' }, hidden));
  const faultIds = [target.id, roof.id, parts.find(p => p.y >= 6 && p.id !== target.id && p.id !== roof.id)!.id];
  const damaged = parts.map(p => p.id === faultIds[0] ? { ...p, x: p.x + 1 }
    : p.id === faultIds[1] ? { ...p, turn: (p.turn + 1) % 4 }
    : p.id === faultIds[2] ? { ...p, color: p.color === 'red' ? 'blue' as const : 'red' as const } : p);
  tasks.push(task(model, 'distributed-repair',
    'Locate all corrupted current IDs against the full reference, then return ONLY replacement parts. Preserve every unlisted current part. Output {faultIds,replacements:[Part]}; repairs are a structural patch, not an executable physical action sequence. Exact IDs are required for patch addressing.',
    { current: { version: 1, parts: damaged }, reference: model.structure },
    { faultIds, replacements: parts.filter(p => faultIds.includes(p.id)) },
    { faultIds: [], replacements: [] }, faultIds));
  return tasks;
}

let cache: FrontierTask[] | undefined;
export function frontierTasks() { return cache ??= frontierModels().flatMap(modelTasks); }
export function publicTask(t: FrontierTask) {
  return { version: FRONTIER_VERSION, id: t.id, modelId: t.modelId, kind: t.kind, prompt: t.prompt, input: t.input };
}
