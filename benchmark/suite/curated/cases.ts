import assert from 'node:assert/strict';
import { type Color, type Part, type Structure } from '../shared';
import { canonicalGeometry, insertIssue, validate } from '../geometry';
import { independentCheck } from '../research/independent-check';

export const CURATED_VERSION = 'brickatlas-curated-casebank-1';
export type CuratedDifficulty = 'easy' | 'medium' | 'hard';
export type CuratedStyle = 'furniture' | 'architecture' | 'infrastructure' | 'landmark';
export interface CuratedCase {
  id: string;
  name: string;
  difficulty: CuratedDifficulty;
  style: CuratedStyle;
  description: string;
  designIntent: string[];
  palette: Partial<Record<Color, string>>;
  structure: Structure;
  assemblyOrder: string[];
  difficultyProfile: {
    parts: number;
    occupiedLevels: number;
    occlusion: 'low' | 'medium' | 'high';
    supportReasoning: 'single' | 'multiple' | 'spanning';
  };
}

interface Builder {
  parts: Part[];
  add: (role: string, partId: string, color: Color, x: number, y: number, z: number, turn?: number) => Part;
}
function builder(): Builder {
  const parts: Part[] = [];
  const counts = new Map<string, number>();
  return { parts, add(role, partId, color, x, y, z, turn = 0) {
    const index = (counts.get(role) ?? 0) + 1; counts.set(role, index);
    const p = { id: `${role}-${index}`, partId, color, x, y, z, turn };
    parts.push(p); return p;
  } };
}
function finalize(meta: Omit<CuratedCase, 'structure' | 'assemblyOrder' | 'difficultyProfile'>, b: Builder,
  profile: Omit<CuratedCase['difficultyProfile'], 'parts' | 'occupiedLevels'>): CuratedCase {
  const structure: Structure = { version: 1, parts: b.parts };
  assert.deepEqual(validate(structure.parts), [], meta.id);
  const assembly = [...structure.parts].sort((a, q) => a.y - q.y || a.id.localeCompare(q.id));
  assert.deepEqual(independentCheck(assembly).issues, [], meta.id);
  let current: Part[] = [];
  for (const p of assembly) {
    assert.equal(insertIssue(current, p), null, `${meta.id}/${p.id}`);
    current = [...current, p];
  }
  assert.ok(new Set(structure.parts.map(p => p.color)).size >= 2
    && new Set(structure.parts.map(p => p.color)).size <= 4, `${meta.id}: palette`);
  assert.deepEqual([...new Set(structure.parts.map(p => p.color))].sort(),
    Object.keys(meta.palette).sort(), `${meta.id}: palette roles`);
  return { ...meta, structure, assemblyOrder: assembly.map(p => p.id),
    difficultyProfile: { ...profile, parts: structure.parts.length,
      occupiedLevels: new Set(structure.parts.map(p => p.y)).size } };
}
function base(id: string, name: string, difficulty: CuratedDifficulty, style: CuratedStyle,
  description: string, palette: CuratedCase['palette'], designIntent: string[]) {
  return { id, name, difficulty, style, description, palette, designIntent,
    provenance: undefined };
}

function gardenBench() {
  const b = builder();
  b.add('ground', '3035', 'green', 0, 0, 0);
  for (const [x, z] of [[2, 1], [5, 1], [2, 2], [5, 2]]) b.add('leg', '3005', 'gray', x, 1, z);
  b.add('seat', '3710', 'red', 2, 4, 1); b.add('seat', '3710', 'red', 2, 4, 2);
  b.add('back', '3010', 'red', 2, 5, 2);
  return finalize(base('easy-garden-bench', 'Garden Bench', 'easy', 'furniture',
    'A symmetric park bench with four legs, a thin seat and a raised backrest.',
    { green: 'ground', gray: 'supports', red: 'seat and backrest' },
    ['Recognizable side profile', 'Three functional color roles', 'Single-support local reasoning']),
  b, { occlusion: 'low', supportReasoning: 'single' });
}
function staircase() {
  const b = builder();
  b.add('ground', '3035', 'gray', 0, 0, 0);
  for (let strip = 0; strip < 4; strip++) for (let level = 0; level <= strip; level++) {
    b.add('step', '3001', 'white', strip * 2, 1 + 3 * level, 0, 1);
  }
  b.add('landing', '3020', 'blue', 6, 13, 0, 1);
  return finalize(base('easy-staircase', 'Four-Step Staircase', 'easy', 'architecture',
    'A monotonic four-step staircase terminating in a blue landing.',
    { gray: 'foundation', white: 'steps', blue: 'landing' },
    ['Monotonic height profile', 'Repeated modular unit', 'Explicit terminal region']),
  b, { occlusion: 'low', supportReasoning: 'single' });
}
function gardenGate() {
  const b = builder();
  b.add('ground', '3035', 'green', 0, 0, 0);
  for (const x of [0, 6]) for (const y of [1, 4, 7]) b.add('pillar', '3003', 'white', x, y, 1);
  b.add('lintel', '3007', 'blue', 0, 10, 1);
  b.add('roof', '3034', 'blue', 0, 13, 1);
  b.add('sign', '3004', 'yellow', 3, 14, 1);
  return finalize(base('easy-garden-gate', 'Garden Gate', 'easy', 'architecture',
    'A balanced gateway with two white pillars, a blue lintel and a centered sign.',
    { green: 'ground', white: 'pillars', blue: 'lintel and roof', yellow: 'sign' },
    ['Bilateral symmetry', 'Clear central opening', 'Spanning lintel']),
  b, { occlusion: 'low', supportReasoning: 'multiple' });
}
function picnicTable() {
  const b = builder();
  b.add('ground', '3035', 'green', 0, 0, 0);
  for (const [x, z] of [[2, 1], [5, 1], [2, 2], [5, 2]]) b.add('table-leg', '3005', 'gray', x, 1, z);
  b.add('tabletop', '3710', 'red', 2, 4, 1); b.add('tabletop', '3710', 'red', 2, 4, 2);
  for (const [x, z] of [[2, 0], [5, 0], [2, 3], [5, 3]]) b.add('bench-leg', '3024', 'gray', x, 1, z);
  b.add('bench', '3710', 'red', 2, 2, 0); b.add('bench', '3710', 'red', 2, 2, 3);
  return finalize(base('easy-picnic-table', 'Picnic Table', 'easy', 'furniture',
    'A red tabletop flanked by two lower benches on a green ground plate.',
    { green: 'ground', gray: 'legs', red: 'tabletop and benches' },
    ['Separated seating and tabletop heights', 'Repeated supports', 'Front/back symmetry']),
  b, { occlusion: 'low', supportReasoning: 'multiple' });
}
function canalBridge() {
  const b = builder();
  b.add('water', '3035', 'blue', 0, 0, 0);
  for (const x of [0, 6]) for (const y of [1, 4, 7]) b.add('pier', '3003', 'gray', x, y, 1);
  b.add('deck', '3035', 'white', 0, 10, 0);
  for (const z of [0, 3]) for (const x of [0, 3, 7]) b.add('rail-post', '3005', 'red', x, 11, z);
  b.add('rail', '3460', 'red', 0, 14, 0); b.add('rail', '3460', 'red', 0, 14, 3);
  return finalize(base('medium-canal-bridge', 'Canal Bridge', 'medium', 'infrastructure',
    'A white bridge deck spanning two gray piers over blue water, with red guard rails.',
    { blue: 'water', gray: 'piers', white: 'deck', red: 'guard rails' },
    ['Two separated supports', 'Spanning deck', 'Paired guard rails']),
  b, { occlusion: 'medium', supportReasoning: 'spanning' });
}
function pavilion() {
  const b = builder();
  b.add('ground', '3035', 'green', 0, 0, 0);
  for (const [x, z] of [[0, 0], [7, 0], [0, 3], [7, 3]]) for (const y of [1, 4, 7]) {
    b.add('column', '3005', 'white', x, y, z);
  }
  b.add('roof', '3035', 'red', 0, 10, 0);
  b.add('roof-cap', '3031', 'yellow', 2, 11, 0);
  b.add('bench', '3710', 'yellow', 2, 1, 1); b.add('bench', '3710', 'yellow', 2, 1, 2);
  return finalize(base('medium-pavilion', 'Park Pavilion', 'medium', 'architecture',
    'An open four-column pavilion with a red roof, yellow cap and yellow interior benches.',
    { green: 'ground', white: 'columns', red: 'roof', yellow: 'roof cap and benches' },
    ['Open interior', 'Four-column support', 'Layered roof']),
  b, { occlusion: 'medium', supportReasoning: 'multiple' });
}
function townhouse() {
  const b = builder();
  b.add('foundation', '3035', 'gray', 0, 0, 0);
  for (const y of [1, 4, 7]) b.add('back-wall', '3008', 'white', 0, y, 0);
  for (const x of [0, 7]) for (const y of [1, 4, 7]) b.add('side-wall', '3004', 'white', x, y, 1, 1);
  for (const y of [1, 4]) {
    b.add('front-wall', '3004', 'white', 0, y, 3); b.add('front-wall', '3004', 'white', 6, y, 3);
  }
  b.add('front-beam', '3008', 'white', 0, 7, 3);
  b.add('roof', '3035', 'blue', 0, 10, 0);
  b.add('doorstep', '3020', 'red', 2, 1, 2);
  return finalize(base('medium-townhouse', 'Townhouse', 'medium', 'architecture',
    'A white enclosed house with a centered front doorway, blue roof and red doorstep.',
    { gray: 'foundation', white: 'walls', blue: 'roof', red: 'doorstep' },
    ['Enclosed shell', 'Front doorway', 'Occluded interior']),
  b, { occlusion: 'high', supportReasoning: 'multiple' });
}
function watchtower() {
  const b = builder();
  b.add('ground', '3035', 'green', 0, 0, 0);
  for (const y of [1, 4, 7, 10]) b.add('shaft', '3003', 'gray', 3, y, 1);
  b.add('platform', '3031', 'gray', 2, 13, 0);
  for (const [x, z] of [[2, 0], [5, 0], [2, 3], [5, 3]]) b.add('post', '3005', 'white', x, 14, z);
  b.add('rail', '3710', 'white', 2, 17, 0); b.add('rail', '3710', 'white', 2, 17, 3);
  b.add('rail', '3710', 'white', 2, 18, 0, 1); b.add('rail', '3710', 'white', 5, 18, 0, 1);
  b.add('roof', '3031', 'red', 2, 19, 0);
  return finalize(base('medium-watchtower', 'Watchtower', 'medium', 'landmark',
    'A tall gray shaft carrying a lookout platform, white rails and red roof.',
    { green: 'ground', gray: 'shaft and platform', white: 'rails', red: 'roof' },
    ['Tall vertical dependency', 'Observation platform', 'Perimeter railing']),
  b, { occlusion: 'medium', supportReasoning: 'multiple' });
}
function doubleSpanBridge() {
  const b = builder();
  b.add('water', '3035', 'blue', 0, 0, 0); b.add('water', '3035', 'blue', 8, 0, 0);
  for (const x of [0, 6, 8, 14]) for (const y of [1, 4, 7]) b.add('pier', '3003', 'gray', x, y, 1);
  b.add('deck', '3035', 'white', 0, 10, 0); b.add('deck', '3035', 'white', 8, 10, 0);
  for (const z of [0, 3]) for (const x of [0, 7, 8, 15]) b.add('rail-post', '3005', 'red', x, 11, z);
  for (const z of [0, 3]) {
    b.add('rail', '3460', 'red', 0, 14, z); b.add('rail', '3460', 'red', 8, 14, z);
  }
  return finalize(base('hard-double-span-bridge', 'Double-Span Bridge', 'hard', 'infrastructure',
    'A two-segment white deck carried by four gray piers over a continuous blue channel.',
    { blue: 'water', gray: 'piers', white: 'deck', red: 'guard rails' },
    ['Two connected spans', 'Four support towers', 'Long repeated rail system']),
  b, { occlusion: 'medium', supportReasoning: 'spanning' });
}
function lighthouse() {
  const b = builder();
  b.add('water', '3035', 'blue', 0, 0, 0); b.add('water', '3035', 'blue', 0, 0, 4);
  b.add('rock', '3031', 'white', 2, 1, 2);
  for (const [i, y] of [2, 5, 8, 11, 14, 17].entries()) {
    b.add('tower', '3003', i % 2 ? 'red' : 'white', 3, y, 3);
  }
  b.add('gallery', '3031', 'white', 2, 20, 2);
  for (const [x, z] of [[2, 2], [5, 2], [2, 5], [5, 5]]) b.add('lantern', '3005', 'yellow', x, 21, z);
  b.add('roof', '3031', 'red', 2, 24, 2);
  return finalize(base('hard-lighthouse', 'Lighthouse', 'hard', 'landmark',
    'A striped red-and-white lighthouse on a white rock base, surrounded by blue water.',
    { blue: 'water', white: 'foundation, gallery, and light tower bands', red: 'tower bands and roof', yellow: 'lantern' },
    ['Tall alternating tower', 'Cantilevered gallery', 'Four-point lantern support']),
  b, { occlusion: 'medium', supportReasoning: 'multiple' });
}
function station() {
  const b = builder();
  b.add('platform', '3035', 'gray', 0, 0, 0); b.add('platform', '3035', 'gray', 8, 0, 0);
  for (const x of [0, 8]) for (const y of [1, 4]) b.add('back-wall', '3008', 'white', x, y, 0);
  for (const x of [0, 5, 10, 15]) for (const y of [1, 4]) b.add('column', '3005', 'white', x, y, 3);
  b.add('roof', '3035', 'blue', 0, 7, 0); b.add('roof', '3035', 'blue', 8, 7, 0);
  b.add('bench', '3710', 'red', 2, 1, 2); b.add('bench', '3710', 'red', 10, 1, 2);
  b.add('sign', '3004', 'red', 7, 8, 1);
  return finalize(base('hard-railway-station', 'Railway Station', 'hard', 'architecture',
    'A long white station canopy with two blue roof modules, red benches and a centered sign.',
    { gray: 'platform', white: 'walls and columns', blue: 'canopy', red: 'benches and sign' },
    ['Two-module footprint', 'Repeated columns', 'Long roof alignment']),
  b, { occlusion: 'high', supportReasoning: 'multiple' });
}
function pagoda() {
  const b = builder();
  b.add('ground', '3035', 'green', 0, 0, 0);
  for (const [x, z] of [[0, 0], [7, 0], [0, 3], [7, 3]]) for (const y of [1, 4]) b.add('lower-column', '3005', 'white', x, y, z);
  b.add('lower-roof', '3035', 'red', 0, 7, 0);
  b.add('upper-floor', '3031', 'yellow', 2, 8, 0);
  for (const [x, z] of [[2, 0], [5, 0], [2, 3], [5, 3]]) for (const y of [9, 12]) b.add('upper-column', '3005', 'white', x, y, z);
  b.add('upper-roof', '3031', 'red', 2, 15, 0);
  b.add('spire', '3003', 'yellow', 3, 16, 1); b.add('spire', '3003', 'yellow', 3, 19, 1);
  b.add('cap', '3022', 'red', 3, 22, 1);
  return finalize(base('hard-two-tier-pagoda', 'Two-Tier Pagoda', 'hard', 'landmark',
    'A symmetric two-tier pavilion with white columns, red roofs and a yellow central spire.',
    { green: 'ground', white: 'columns', red: 'roofs and cap', yellow: 'upper floor and spire' },
    ['Two nested structural scales', 'Strong bilateral symmetry', 'Deep vertical dependency']),
  b, { occlusion: 'high', supportReasoning: 'multiple' });
}

let cache: CuratedCase[] | undefined;
export function curatedCases() {
  if (cache) return cache;
  const cases = [gardenBench(), staircase(), gardenGate(), picnicTable(),
    canalBridge(), pavilion(), townhouse(), watchtower(),
    doubleSpanBridge(), lighthouse(), station(), pagoda()];
  assert.equal(new Set(cases.map(c => c.id)).size, cases.length);
  assert.equal(new Set(cases.map(c => canonicalGeometry(c.structure.parts))).size, cases.length);
  for (const difficulty of ['easy', 'medium', 'hard']) assert.equal(cases.filter(c => c.difficulty === difficulty).length, 4);
  cache = cases; return cases;
}
