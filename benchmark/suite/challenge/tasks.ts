import assert from 'node:assert/strict';
import { bom, bounds, cells, dims, edges, footprint, insertIssue, validate } from '../geometry';
import { digest } from '../data';
import type { FrameSpec, Part, Structure } from '../shared';
import { challengeModels, CHALLENGE_VERSION, type ChallengeModel } from './models';
import { evaluateChallenge } from './evaluate';

export const CHALLENGE_KINDS = [
  'recovery-plan', 'support-counterfactual', 'compound-edit', 'multi-fault-repair',
  'active-inspection', 'graph-reasoning', 'distributed-completion', 'module-transplant',
  'step-selection', 'pose-estimation', 'scene-reconstruction', 'constrained-redesign',
] as const;
export type ChallengeKind = typeof CHALLENGE_KINDS[number];

export interface ChallengeTask {
  id: string;
  kind: ChallengeKind;
  model: ChallengeModel;
  prompt: string;
  input: Record<string, unknown>;
  responseSchema: Record<string, unknown>;
  frames: FrameSpec[];
  source: Structure | null;
  target: Structure;
  oracle: unknown;
  changedIds: string[];
  private: Record<string, unknown>;
}

const views = (parts: Part[], prefix: string): FrameSpec[] =>
  (['iso', 'top', 'front', 'side'] as const).map(view => ({ parts, view, layer: null, title: `${prefix}: ${view}` }));

function byId(id: string) {
  const model = challengeModels().find(item => item.id === id);
  assert.ok(model);
  return model;
}

function make(model: ChallengeModel, kind: ChallengeKind, prompt: string, input: Record<string, unknown>,
  responseSchema: Record<string, unknown>, target: Structure, source: Structure | null,
  oracle: unknown, changedIds: string[], frames: FrameSpec[] = [], privateData: Record<string, unknown> = {}) {
  const task: ChallengeTask = {
    id: digest({ version: CHALLENGE_VERSION, model: model.id, kind }).slice(0, 24),
    kind, model, prompt, input, responseSchema, target, source, oracle, changedIds,
    frames, private: privateData,
  };
  assert.equal(evaluateChallenge(task, oracle).success, 1, `${model.id}/${kind}`);
  return task;
}

function cascade(parts: Part[], forced: Set<string>) {
  let remaining = parts.filter(p => !forced.has(p.id));
  const unsupported: string[] = [];
  while (true) {
    const lost = remaining.filter(p => p.y > 0 && !remaining.some(q =>
      q.id !== p.id && q.y + dims(q).h === p.y && footprint(p, q) > 0));
    if (!lost.length) break;
    unsupported.push(...lost.map(p => p.id));
    const ids = new Set(lost.map(p => p.id));
    remaining = remaining.filter(p => !ids.has(p.id));
  }
  return unsupported.sort();
}

function graphAnswer(parts: Part[], start: string, goal: string) {
  const adjacency = new Map(parts.map(p => [p.id, [] as string[]]));
  for (const edge of edges(parts)) {
    adjacency.get(edge.a)!.push(edge.b);
    adjacency.get(edge.b)!.push(edge.a);
  }
  const distance = new Map([[start, 0]]), queue = [start];
  for (let i = 0; i < queue.length; i++) for (const next of adjacency.get(queue[i])!) {
    if (!distance.has(next)) {
      distance.set(next, distance.get(queue[i])! + 1);
      queue.push(next);
    }
  }
  let time = 0;
  const discovery = new Map<string, number>(), low = new Map<string, number>();
  const articulation = new Set<string>();
  const visit = (id: string, parent: string | null) => {
    discovery.set(id, ++time);
    low.set(id, time);
    let children = 0;
    for (const next of adjacency.get(id)!) {
      if (next === parent) continue;
      if (!discovery.has(next)) {
        children++;
        visit(next, id);
        low.set(id, Math.min(low.get(id)!, low.get(next)!));
        if (parent !== null && low.get(next)! >= discovery.get(id)!) articulation.add(id);
      } else low.set(id, Math.min(low.get(id)!, discovery.get(next)!));
    }
    if (parent === null && children > 1) articulation.add(id);
  };
  visit(parts[0].id, null);
  return { shortestPath: distance.get(goal) ?? -1, articulationIds: [...articulation].sort() };
}

let cached: ChallengeTask[] | undefined;
export function challengeTasks() {
  if (cached) return cached;
  const tasks: ChallengeTask[] = [];

  const bridge = byId('expert-truss-bridge');
  const retained = new Set(bridge.structure.parts.filter(p =>
    p.id.startsWith('base-') || p.id.startsWith('base-seam-')
    || (p.id.startsWith('pier-') && [0, 8, 22].includes(p.x))
    || p.id.startsWith('deck-') && !p.id.startsWith('deck-seam-')).map(p => p.id));
  const bridgeSource: Structure = { version: 1, parts: bridge.structure.parts.filter(p => retained.has(p.id)) };
  assert.deepEqual(validate(bridgeSource.parts), []);
  const removeDecks = bridge.structure.parts.filter(p => p.id.startsWith('deck-') && !p.id.startsWith('deck-seam-'))
    .map(p => ({ type: 'remove', id: p.id }));
  const afterRemoval = new Set([...retained].filter(id => !removeDecks.some(action => action.id === id)));
  const recoveryActions = [...removeDecks, ...bridge.assemblyOrder.filter(id => !afterRemoval.has(id))
    .map(id => ({ type: 'place', id }))];
  tasks.push(make(bridge, 'recovery-plan',
    'Recover from a legal but blocked deck-first state. Return remove/place actions that reach the complete target without reordering by the evaluator.',
    { current: bridgeSource, target: bridge.structure }, { actions: [{ type: 'remove|place', id: 'piece ID' }] },
    bridge.structure, bridgeSource, { actions: recoveryActions },
    bridge.structure.parts.filter(p => !retained.has(p.id)).map(p => p.id),
    views(bridge.structure.parts, 'Target bridge')));

  const forced = new Set(bridge.structure.parts.filter(p => p.id.startsWith('pier-') && [0, 4].includes(p.x)).map(p => p.id));
  const unsupportedIds = cascade(bridge.structure.parts, forced);
  assert.ok(unsupportedIds.length >= 4);
  tasks.push(make(bridge, 'support-counterfactual',
    'If the declared two support columns disappear simultaneously, report every additional piece removed by iterative loss of direct stud support.',
    { structure: bridge.structure, forcedRemoveIds: [...forced].sort() }, { unsupportedIds: ['piece ID'] },
    bridge.structure, null, { unsupportedIds }, unsupportedIds));

  const station = byId('expert-grand-terminal');
  const compoundParts = station.structure.parts
    .filter(p => !['bench-2', 'bench-4'].includes(p.id))
    .map(p => p.color === 'blue' ? { ...p, color: 'red' as const } : { ...p });
  compoundParts.push(
    { id: 'roof-light-1', partId: '3005', color: 'yellow', x: 4, y: 11, z: 1, turn: 0 },
    { id: 'roof-light-2', partId: '3005', color: 'yellow', x: 19, y: 11, z: 1, turn: 0 },
  );
  const compoundTarget: Structure = { version: 1, parts: compoundParts };
  assert.deepEqual(validate(compoundTarget.parts), []);
  tasks.push(make(station, 'compound-edit',
    'Apply all clauses atomically: recolor the blue canopy red, remove bench-2 and bench-4, add the two specified yellow roof lights, and preserve every other part.',
    { current: station.structure, operations: [
      { type: 'recolor-role', role: 'canopy', from: 'blue', to: 'red' },
      { type: 'remove', ids: ['bench-2', 'bench-4'] },
      { type: 'add', parts: compoundParts.filter(p => p.id.startsWith('roof-light-')) },
    ] }, { version: 1, parts: ['full target structure'] },
    compoundTarget, station.structure, compoundTarget,
    [...station.structure.parts.filter(p => p.color === 'blue').map(p => p.id), 'bench-2', 'bench-4', 'roof-light-1', 'roof-light-2']));

  const faultyStation = structuredClone(station.structure);
  faultyStation.parts.find(p => p.id === 'clock-roof-1')!.x += 1;
  faultyStation.parts.find(p => p.id === 'bench-1')!.color = 'yellow';
  faultyStation.parts.push({ id: 'intruder-1', partId: '3005', color: 'green', x: 2, y: 11, z: 1, turn: 0 });
  assert.deepEqual(validate(faultyStation.parts), []);
  const stationFaults = ['bench-1', 'clock-roof-1', 'intruder-1'];
  tasks.push(make(station, 'multi-fault-repair',
    'Repair three simultaneous faults: one recolor, one shifted part, and one extra part. Return the corrected structure and all wrong CURRENT IDs.',
    { current: faultyStation, billOfMaterials: bom(station.structure.parts) },
    { structure: { version: 1, parts: ['part'] }, faultIds: ['current piece ID'] },
    station.structure, faultyStation, { structure: station.structure, faultIds: stationFaults },
    stationFaults, views(station.structure.parts, 'Reference terminal')));

  const gate = byId('expert-fortress-gatehouse');
  tasks.push(make(gate, 'active-inspection',
    'Choose the minimum-cost inspection that reveals the complete gate-beam layer, then answer whether two parallel spanning beams exist.',
    { initialViews: ['front', 'side'], queryOptions: [
      { id: 'rear-rgb', cost: 1, reveals: 'rear exterior only' },
      { id: 'top-rgb', cost: 1, reveals: 'assembled top view with occlusion' },
      { id: 'layer-y-13', cost: 2, reveals: 'all and only parts whose bottom Y=13' },
      { id: 'symbolic-graph', cost: 4, reveals: 'complete typed contact graph' },
    ] }, { queryId: 'string', answer: 'one-beam|two-parallel-beams' },
    gate.structure, null, { queryId: 'layer-y-13', answer: 'two-parallel-beams' }, [],
    [{ parts: gate.structure.parts, view: 'front', layer: null, title: 'Initial front view' },
      { parts: gate.structure.parts, view: 'side', layer: null, title: 'Initial side view' }]));

  const gateStart = 'tower-merlon-1', gateGoal = 'tower-merlon-8';
  const gateGraph = graphAnswer(gate.structure.parts, gateStart, gateGoal);
  assert.ok(gateGraph.shortestPath > 3 && gateGraph.articulationIds.length > 0);
  tasks.push(make(gate, 'graph-reasoning',
    'Return the shortest stud-contact path length between the queried merlons and every articulation piece in the full contact graph.',
    { structure: gate.structure, startId: gateStart, goalId: gateGoal },
    { shortestPath: 'integer', articulationIds: ['piece ID'] },
    gate.structure, null, gateGraph, gateGraph.articulationIds));

  const temple = byId('advanced-stepped-temple');
  const templeMissing = temple.structure.parts.filter(p =>
    p.id.startsWith('lower-column-') && p.x === 4 || p.id.startsWith('upper-column-') && p.x === 8);
  const templeMissingIds = new Set(templeMissing.map(p => p.id));
  const templeSource: Structure = { version: 1, parts: temple.structure.parts.filter(p => !templeMissingIds.has(p.id)) };
  assert.deepEqual(validate(templeSource.parts), []);
  tasks.push(make(temple, 'distributed-completion',
    'Restore eight missing columns distributed across both tiers. Preserve every supplied part exactly; the missing region is not a suffix.',
    { current: templeSource, billOfMaterials: bom(temple.structure.parts) },
    { version: 1, parts: ['full target structure'] },
    temple.structure, templeSource, temple.structure, [...templeMissingIds], views(temple.structure.parts, 'Reference temple')));

  const movedIds = new Set(temple.structure.parts.filter(p => p.id.startsWith('upper-') || p.id.startsWith('spire-')).map(p => p.id));
  const movedTemple: Structure = { version: 1, parts: temple.structure.parts.map(p =>
    movedIds.has(p.id) ? { ...p, x: p.x + 4 } : { ...p }) };
  assert.deepEqual(validate(movedTemple.parts), []);
  tasks.push(make(temple, 'module-transplant',
    'Move the complete upper pavilion four studs toward +X as a rigid module. Preserve its internal layout and every lower-tier part.',
    { current: temple.structure, moduleIds: [...movedIds].sort(), translation: [4, 0, 0] },
    { version: 1, parts: ['full target structure'] },
    movedTemple, temple.structure, movedTemple, [...movedIds]));

  const aqueduct = byId('expert-double-deck-aqueduct');
  const aqueductPrefix: Structure = { version: 1, parts: aqueduct.structure.parts.filter(p => p.y <= 17) };
  const candidates = [
    ...aqueduct.structure.parts.filter(p => p.y === 18).slice(0, 6),
    ...aqueduct.structure.parts.filter(p => p.y === 21).slice(0, 3),
  ];
  const legalIds = candidates.filter(p => insertIssue(aqueductPrefix.parts, p) === null).map(p => p.id).sort();
  assert.equal(legalIds.length, 6);
  tasks.push(make(aqueduct, 'step-selection',
    'Select every candidate that can legally be inserted next into the current partial aqueduct. Do not use the target order as an answer.',
    { current: aqueductPrefix, candidates: candidates.map(({ id, partId, color }) => ({ id, partId, color })) },
    { legalIds: ['candidate ID'] }, aqueduct.structure, aqueductPrefix, { legalIds }, legalIds));

  const selected = aqueduct.structure.parts.find(p => p.id.startsWith('parapet-post-') && p.y === 18 && p.x === 15)!;
  const poseCurrent: Structure = { version: 1, parts: aqueduct.structure.parts.filter(p =>
    p.y <= 17 || p.y === 18 && p.id !== selected.id) };
  const pose = { x: selected.x, y: selected.y, z: selected.z, turn: selected.turn };
  tasks.push(make(aqueduct, 'pose-estimation',
    'Place the selected repeated pier into its exact target pose from the current state and reference views.',
    { current: poseCurrent, selected: { id: selected.id, partId: selected.partId, color: selected.color } },
    { x: 'integer', y: 'integer', z: 'integer', turn: '0|1|2|3' },
    aqueduct.structure, poseCurrent, pose, [selected.id], views(aqueduct.structure.parts, 'Reference aqueduct')));

  const market = byId('advanced-covered-market');
  tasks.push(make(market, 'scene-reconstruction',
    'Reconstruct the complete 53-part market from four views and its bill of materials. Repeated columns and signs remain distinct instances.',
    { billOfMaterials: bom(market.structure.parts) }, { version: 1, parts: ['full structure'] },
    market.structure, null, market.structure, [], views(market.structure.parts, 'Market view')));

  const redesignRequirements = {
    extent: bounds(market.structure.parts), inventory: bom(market.structure.parts),
    anchors: market.structure.parts.filter(p => p.id.startsWith('base-') || p.id.startsWith('base-seam-')),
    minRoofCells: cells(market.structure.parts.filter(p => p.y >= 7)).size,
    minColors: 4, minParts: 45, maxParts: 64,
  };
  const marketFoundation: Structure = { version: 1, parts: redesignRequirements.anchors };
  tasks.push(make(market, 'constrained-redesign',
    'Design any connected market hall that preserves the supplied foundation, stays within inventory, matches the exact extent, uses four color roles, and meets the roof-coverage threshold.',
    { foundation: marketFoundation, requirements: {
      extent: redesignRequirements.extent, inventory: redesignRequirements.inventory,
      anchorIds: redesignRequirements.anchors.map(p => p.id), minRoofCells: redesignRequirements.minRoofCells,
      minColors: redesignRequirements.minColors, minParts: redesignRequirements.minParts, maxParts: redesignRequirements.maxParts,
    } },
    { version: 1, parts: ['any satisfying structure'] },
    market.structure, marketFoundation, market.structure, [], [],
    { requirements: redesignRequirements }));

  assert.equal(tasks.length, 12);
  assert.equal(new Set(tasks.map(task => task.kind)).size, 12);
  cached = tasks;
  return tasks;
}
