import assert from 'node:assert/strict';
import { bom, bounds, components, edges } from '../geometry';
import { type FrameSpec, type Kind, type Part, type PublicTask, type Structure } from '../shared';
import { digest } from '../data';
import { relationOracle, structureSchema, type CaseTask, type Condition } from '../v2/cases';
import { evaluateStrict } from '../study/strict-evaluate';
import { curatedCases, type CuratedCase } from './cases';

export interface CuratedTask {
  task: CaseTask;
  model: CuratedCase;
  display: {
    title: string;
    inputLabel: string;
    groundTruthLabel: string;
    highlightIds: string[];
  };
}
function views(parts: Part[], prefix: string): FrameSpec[] {
  return (['iso', 'top', 'front', 'side'] as const).map(view => ({
    parts, view, layer: null, title: `${prefix}: ${view}`,
  }));
}
function spec(model: CuratedCase, kind: Kind, variant: string, condition: Condition) {
  return { id: digest({ version: 'curated-tasks-1', model: model.id, kind, variant, condition }).slice(0, 24),
    modelId: model.id, group: model.id, kind, variant, condition, split: 'validation' as const,
    policy: model.style, difficulty: model.difficulty };
}
function make(model: CuratedCase, kind: Kind, variant: string, condition: Condition, target: Structure,
  source: Structure | null, oracle: unknown, changedIds: string[], frames: FrameSpec[],
  input: Record<string, unknown>, prompt: string, responseSchema: Record<string, unknown>,
  display: CuratedTask['display']): CuratedTask {
  const s = spec(model, kind, variant, condition);
  const publicTask: PublicTask = { id: s.id, kind, split: s.split, family: model.style,
    prompt, input, responseSchema, imageTitles: frames.map(f => f.title) };
  const task: CaseTask = { spec: s, target, source, oracle, changedIds, frames, public: publicTask };
  const answer = kind === 'repair' ? { structure: target, faultIds: changedIds }
    : kind === 'plan' ? oracle : oracle;
  assert.equal(evaluateStrict(task, answer).metrics.success, 1, `${model.id}/${kind}`);
  return { task, model, display };
}
function byId(id: string) {
  const model = curatedCases().find(c => c.id === id);
  assert.ok(model); return model;
}
function degree(parts: Part[]) {
  const graph = edges(parts);
  return Math.max(...parts.map(p => graph.filter(e => e.a === p.id || e.b === p.id).length));
}

let cache: CuratedTask[] | undefined;
export function curatedTasks() {
  if (cache) return cache;
  const tasks: CuratedTask[] = [];

  const bench = byId('easy-garden-bench');
  const part = bench.structure.parts.find(p => p.id === 'back-1')!;
  const isolated: Structure = { version: 1, parts: [{ ...part, id: 'query', x: 0, y: 0, z: 0 }] };
  tasks.push(make(bench, 'parts', 'known-catalog', 'ordinary', isolated, null,
    { partId: part.partId, color: part.color, studs: 4 }, [], views(isolated.parts, 'Isolated query'),
    {}, 'Identify the isolated catalog part, color, and top-stud count.',
    { partId: 'string', color: 'string', studs: 'integer' },
    { title: 'Part recognition', inputLabel: 'Isolated part', groundTruthLabel: 'Type + color + studs', highlightIds: ['query'] }));

  const tower = byId('medium-watchtower'), a = tower.structure.parts.find(p => p.id === 'shaft-4')!,
    b = tower.structure.parts.find(p => p.id === 'platform-1')!;
  const relation = relationOracle(tower.structure.parts, a, b);
  tasks.push(make(tower, 'relations', 'contact', 'default', tower.structure, null, relation, [],
    [],
    { structure: tower.structure, a: a.id, b: b.id },
    'Report direct connection, vertical ordering, mating studs, and shortest contact-graph path.',
    { connected: 'boolean', above: 'boolean', contactStuds: 'integer', shortestPath: 'integer' },
    { title: 'Structural relation', inputLabel: 'Two queried parts', groundTruthLabel: 'Typed relation tuple', highlightIds: [a.id, b.id] }));

  const gate = byId('easy-garden-gate');
  tasks.push(make(gate, 'reconstruct', 'full', 'ordinary', gate.structure, null, gate.structure, [],
    views(gate.structure.parts, 'Ordinary RGB'), { billOfMaterials: bom(gate.structure.parts) },
    'Reconstruct a legal assembly matching the supplied views and bill of materials.',
    structureSchema, { title: 'Multi-view reconstruction', inputLabel: 'Four assembled views + BOM',
      groundTruthLabel: 'Full typed pose multiset', highlightIds: [] }));

  const pavilion = byId('medium-pavilion'), box = bounds(pavilion.structure.parts);
  const requirements = { extent: box, maxPieces: pavilion.structure.parts.length + 3,
    minColors: 4, components: components(pavilion.structure.parts), minMaximumDegree: degree(pavilion.structure.parts) };
  tasks.push(make(pavilion, 'generate', 'constraints', 'default', pavilion.structure, null, pavilion.structure, [],
    [], { requirements },
    'Design any legal assembly satisfying the exact public constraints and anchored at minimum X/Y/Z=0; the shown ground truth is one valid witness.',
    structureSchema, { title: 'Constrained generation', inputLabel: 'Six structural constraints',
      groundTruthLabel: 'One satisfying witness', highlightIds: [] }));

  const bridge = byId('medium-canal-bridge'), retained = new Set(bridge.structure.parts
    .filter(p => ['water', 'pier', 'deck'].some(role => p.id.startsWith(`${role}-`))).map(p => p.id));
  const bridgeSource: Structure = { version: 1, parts: bridge.structure.parts.filter(p => retained.has(p.id)) };
  const additions = bridge.structure.parts.filter(p => !retained.has(p.id)).map(p => p.id);
  tasks.push(make(bridge, 'complete', 'curated-suffix', 'ordinary', bridge.structure, bridgeSource,
    bridge.structure, additions, views(bridge.structure.parts, 'Reference'),
    { current: bridgeSource, billOfMaterials: bom(bridge.structure.parts) },
    'Complete the bridge while preserving every supplied piece.',
    structureSchema, { title: 'Structure completion', inputLabel: 'Bridge missing guard rails + reference + BOM',
      groundTruthLabel: 'Guard rails restored', highlightIds: additions }));

  const station = byId('hard-railway-station'), stationTarget: Structure = { version: 1,
    parts: station.structure.parts.map(p => p.color === 'blue' ? { ...p, color: 'red' as const } : p) };
  const changed = station.structure.parts.filter(p => p.color === 'blue').map(p => p.id);
  tasks.push(make(station, 'edit', 'recolor-roof', 'default', stationTarget, station.structure,
    stationTarget, changed, [],
    { current: station.structure, operation: { type: 'recolor', from: 'blue', to: 'red' } },
    'Recolor every blue canopy piece red and preserve all other parts.', structureSchema,
    { title: 'Instruction editing', inputLabel: 'Station + recolor command',
      groundTruthLabel: 'Red canopy, geometry preserved', highlightIds: changed }));

  const longBridge = byId('hard-double-span-bridge');
  tasks.push(make(longBridge, 'plan', 'assemble', 'default', longBridge.structure, null,
    { order: longBridge.assemblyOrder }, [], [],
    { target: longBridge.structure, direction: 'assemble' },
    'Return all IDs exactly once in an executable vertical assembly order.', { order: ['piece ID'] },
    { title: 'Executable planning', inputLabel: 'Target geometry',
      groundTruthLabel: 'Verified legal sequence', highlightIds: [] }));

  const lighthouse = byId('hard-lighthouse'), faulty = structuredClone(lighthouse.structure);
  const roof = faulty.parts.find(p => p.id === 'roof-1')!; roof.x += 1;
  tasks.push(make(lighthouse, 'repair', 'shift', 'ordinary', lighthouse.structure, faulty,
    { structure: lighthouse.structure, faultIds: ['roof-1'] }, ['roof-1'],
    views(lighthouse.structure.parts, 'Reference'),
    { current: faulty, billOfMaterials: bom(lighthouse.structure.parts) },
    'Repair the shifted roof and identify the faulty current part ID.',
    { structure: structureSchema, faultIds: ['piece ID'] },
    { title: 'Fault repair', inputLabel: 'Faulty lighthouse + reference',
      groundTruthLabel: 'Roof restored + fault localized', highlightIds: ['roof-1'] }));

  assert.equal(tasks.length, 8);
  cache = tasks; return tasks;
}
