import assert from 'node:assert/strict';
import { type Color, type Part, type Structure } from '../shared';
import { components, insertIssue, validate } from '../geometry';
import { independentCheck } from '../research/independent-check';

export const CHALLENGE_VERSION = 'brickatlas-challenge-casebank-1';
export type ChallengeTier = 'advanced' | 'expert';

export interface ChallengeModel {
  id: string;
  name: string;
  tier: ChallengeTier;
  domain: 'infrastructure' | 'architecture' | 'landmark';
  description: string;
  capabilityPressure: string[];
  palette: Partial<Record<Color, string>>;
  structure: Structure;
  assemblyOrder: string[];
}

interface Builder {
  parts: Part[];
  add: (role: string, partId: string, color: Color, x: number, y: number, z: number, turn?: number) => Part;
}

function builder(): Builder {
  const parts: Part[] = [], counts = new Map<string, number>();
  return { parts, add(role, partId, color, x, y, z, turn = 0) {
    const index = (counts.get(role) ?? 0) + 1;
    counts.set(role, index);
    const part = { id: `${role}-${index}`, partId, color, x, y, z, turn };
    parts.push(part);
    return part;
  } };
}

function stripBase(b: Builder, color: Color, seamZ = 2) {
  for (const x of [0, 8, 16]) b.add('base', '3035', color, x, 0, 0);
  for (const x of [6, 14]) b.add('base-seam', '3710', color, x, 1, seamZ);
}

function finish(meta: Omit<ChallengeModel, 'structure' | 'assemblyOrder'>, b: Builder): ChallengeModel {
  const structure: Structure = { version: 1, parts: b.parts };
  assert.ok(structure.parts.length >= 45 && structure.parts.length <= 64, `${meta.id}: size`);
  assert.deepEqual(validate(structure.parts), [], meta.id);
  assert.equal(components(structure.parts), 1, `${meta.id}: disconnected`);
  const ordered = [...structure.parts].sort((a, q) => a.y - q.y || a.id.localeCompare(q.id));
  assert.deepEqual(independentCheck(ordered).issues, [], meta.id);
  let prefix: Part[] = [];
  for (const part of ordered) {
    assert.equal(insertIssue(prefix, part), null, `${meta.id}/${part.id}`);
    prefix = [...prefix, part];
  }
  const colors = [...new Set(structure.parts.map(p => p.color))].sort();
  assert.deepEqual(colors, Object.keys(meta.palette).sort(), `${meta.id}: palette`);
  return { ...meta, structure, assemblyOrder: ordered.map(p => p.id) };
}

function trussBridge() {
  const b = builder();
  stripBase(b, 'blue', 3);
  for (const x of [0, 4, 8, 12, 16, 22]) {
    for (const y of [1, 4, 7, 10]) b.add('pier', '3003', 'gray', x, y, 1);
  }
  for (const x of [0, 8, 16]) b.add('deck', '3035', 'white', x, 13, 0);
  for (const x of [6, 14]) b.add('deck-seam', '3710', 'white', x, 14, 2);
  for (const z of [0, 3]) for (const x of [0, 3, 7, 8, 15, 16, 20, 23]) {
    b.add('rail-post', '3005', 'red', x, 14, z);
  }
  for (const z of [0, 3]) for (const x of [0, 8, 16]) b.add('rail', '3460', 'red', x, 17, z);
  return finish({
    id: 'expert-truss-bridge', name: 'Three-Span Truss Bridge', tier: 'expert', domain: 'infrastructure',
    description: 'A 24-stud three-span bridge with six four-brick piers, continuous deck seams, and paired rail systems.',
    capabilityPressure: ['56-part long-horizon plan', 'Multiple legal frontiers', 'Recoverable deck-first dead end'],
    palette: { blue: 'water', gray: 'piers', white: 'deck', red: 'rails' },
  }, b);
}

function grandTerminal() {
  const b = builder();
  stripBase(b, 'gray');
  for (const y of [1, 4, 7]) {
    for (const x of [0, 8, 16]) b.add('back-wall', '3008', 'white', x, y, 0);
    for (const x of [0, 4, 8, 12, 16, 20, 23]) b.add('front-column', '3005', 'white', x, y, 3);
  }
  for (const x of [0, 8, 16]) b.add('canopy', '3035', 'blue', x, 10, 0);
  for (const x of [6, 14]) b.add('canopy-seam', '3710', 'blue', x, 11, 2);
  for (const x of [1, 6, 11, 16, 20]) b.add('bench', '3710', 'red', x, 1, 1);
  b.add('clock-floor', '3031', 'blue', 10, 11, 0);
  for (const y of [12, 15]) for (const [x, z] of [[10, 0], [13, 0], [10, 3], [13, 3]]) {
    b.add('clock-column', '3005', 'white', x, y, z);
  }
  b.add('clock-roof', '3031', 'red', 10, 18, 0);
  return finish({
    id: 'expert-grand-terminal', name: 'Grand Railway Terminal', tier: 'expert', domain: 'architecture',
    description: 'A 24-stud station with repeated bays, a continuous canopy, five benches, and an elevated clock pavilion.',
    capabilityPressure: ['55-part scene reconstruction', 'Repeated-instance disambiguation', 'Compound regional edit'],
    palette: { gray: 'platform', white: 'walls and columns', blue: 'canopy', red: 'benches and clock roof' },
  }, b);
}

function gatehouse() {
  const b = builder();
  stripBase(b, 'green');
  for (const x of [0, 2, 4, 18, 20, 22]) for (const y of [1, 4, 7, 10]) {
    b.add('tower', '3001', 'gray', x, y, 0, 1);
  }
  for (const z of [0, 3]) {
    b.add('gate-beam', '3008', 'white', 4, 13, z);
    b.add('gate-beam', '3008', 'white', 12, 13, z);
  }
  for (const z of [0, 3]) for (const x of [0, 2, 21, 23]) b.add('tower-merlon', '3005', 'red', x, 13, z);
  for (const z of [0, 3]) for (const x of [4, 7, 10, 13, 16, 19]) b.add('gate-merlon', '3005', 'red', x, 16, z);
  return finish({
    id: 'expert-fortress-gatehouse', name: 'Fortress Gatehouse', tier: 'expert', domain: 'architecture',
    description: 'Twin four-level towers connected by a deep gate beam and two rows of crenellations.',
    capabilityPressure: ['53-part occlusion', 'Long graph paths', 'Inspection choice under hidden structure'],
    palette: { green: 'ground', gray: 'tower masonry', white: 'gate beams', red: 'crenellations' },
  }, b);
}

function steppedTemple() {
  const b = builder();
  stripBase(b, 'green');
  for (const y of [1, 4]) for (const z of [0, 3]) for (const x of [0, 4, 8, 12, 16, 20, 23]) {
    b.add('lower-column', '3005', 'white', x, y, z);
  }
  for (const x of [0, 8, 16]) b.add('lower-roof', '3035', 'red', x, 7, 0);
  b.add('upper-floor', '3035', 'yellow', 8, 8, 0);
  for (const y of [9, 12]) for (const [x, z] of [[8, 0], [15, 0], [8, 3], [15, 3]]) {
    b.add('upper-column', '3005', 'white', x, y, z);
  }
  b.add('upper-roof', '3035', 'red', 8, 15, 0);
  for (const y of [16, 19, 22]) b.add('spire', '3003', 'yellow', 11, y, 1);
  return finish({
    id: 'advanced-stepped-temple', name: 'Stepped Temple Complex', tier: 'advanced', domain: 'landmark',
    description: 'A 24-stud colonnade supporting a centered upper pavilion and three-stage spire.',
    capabilityPressure: ['49-part distributed completion', 'Nested subassembly transform', 'Strong symmetry traps'],
    palette: { green: 'ground', white: 'columns', red: 'roofs', yellow: 'upper floor and spire' },
  }, b);
}

function aqueduct() {
  const b = builder();
  stripBase(b, 'blue', 3);
  for (const x of [0, 4, 8, 12, 16, 22]) {
    for (const y of [1, 4, 7]) b.add('lower-pier', '3003', 'gray', x, y, 1);
  }
  for (const x of [0, 8, 16]) b.add('lower-deck', '3035', 'white', x, 10, 0);
  for (const x of [0, 4, 8, 12, 16, 22]) for (const y of [11, 14]) {
    b.add('upper-pier', '3003', 'gray', x, y, 1);
  }
  for (const x of [0, 8, 16]) b.add('channel', '3035', 'blue', x, 17, 0);
  for (const z of [0, 3]) for (const x of [0, 3, 7, 8, 15, 16, 20, 23]) {
    b.add('parapet-post', '3005', 'red', x, 18, z);
  }
  for (const z of [0, 3]) for (const x of [0, 8, 16]) b.add('parapet', '3460', 'red', x, 21, z);
  return finish({
    id: 'expert-double-deck-aqueduct', name: 'Double-Deck Aqueduct', tier: 'expert', domain: 'infrastructure',
    description: 'A 63-part two-level aqueduct with repeated piers, a raised channel, and long parapets.',
    capabilityPressure: ['Fine-grained next-part selection', 'Pose estimation among repeated bays', '63-part output length'],
    palette: { blue: 'foundation and channel', gray: 'piers', white: 'lower deck', red: 'parapets' },
  }, b);
}

function coveredMarket() {
  const b = builder();
  stripBase(b, 'green');
  for (const y of [1, 4]) for (const z of [0, 3]) for (const x of [0, 4, 8, 12, 16, 20, 23]) {
    b.add('column', '3005', 'white', x, y, z);
  }
  for (const x of [0, 8, 16]) b.add('roof', '3035', 'red', x, 7, 0);
  for (const x of [1, 6, 11, 16, 20]) b.add('stall', '3710', 'yellow', x, 1, 1);
  for (const x of [0, 4, 8, 12, 16, 20]) b.add('awning', '3020', 'yellow', x, 8, 1);
  for (const x of [1, 5, 9, 13, 17, 21]) b.add('roof-sign', '3004', 'red', x, 9, 1);
  return finish({
    id: 'advanced-covered-market', name: 'Covered Market Hall', tier: 'advanced', domain: 'architecture',
    description: 'A repeated seven-bay market hall with stalls, roof awnings, and aligned signs.',
    capabilityPressure: ['53-part multi-view reconstruction', 'Inventory-constrained redesign', 'Repeated-part correspondence'],
    palette: { green: 'floor', white: 'columns', red: 'roof and signs', yellow: 'stalls and awnings' },
  }, b);
}

let cached: ChallengeModel[] | undefined;
export function challengeModels() {
  if (!cached) {
    cached = [trussBridge(), grandTerminal(), gatehouse(), steppedTemple(), aqueduct(), coveredMarket()];
    assert.equal(new Set(cached.map(model => model.id)).size, cached.length);
  }
  return cached;
}
