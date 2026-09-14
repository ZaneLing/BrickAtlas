import assert from 'node:assert/strict';
import { type Color, type Part, type Structure } from '../shared';
import { bounds, components, dims, footprint } from '../geometry';
import { insertion, validate, dependencies } from './geometry';

export interface FrontierModel {
  id: string; name: string; domain: string; tier: string; description: string;
  palette: Partial<Record<Color, string>>; structure: Structure;
  modules: Record<string, string[]>; stats: { parts: number; layers: number; depth: number; types: number; extent: ReturnType<typeof bounds> };
}
class Builder {
  parts: Part[] = [];
  modules: Record<string, string[]> = {};
  add(role: string, partId: string, color: Color, x: number, y: number, z: number, turn = 0) {
    const id = `p${String(this.parts.length + 1).padStart(4, '0')}`;
    this.parts.push({ id, partId, color, x, y, z, turn });
    (this.modules[role] ??= []).push(id);
  }
  floor(role: string, color: Color, x: number, y: number, z: number, nx: number, nz: number) {
    for (let i = 0; i < nx; i++) for (let j = 0; j < nz; j++) this.add(role, '3035', color, x + i * 8, y, z + j * 4);
  }
  foundation(nx: number, nz: number, color: Color = 'gray') {
    this.floor('foundation', color, 0, 0, 0, nx, nz);
    for (let i = 1; i < nx; i++) for (let j = 0; j < nz; j++) this.add('foundation-tie', '3020', color, i * 8 - 2, 1, j * 4);
    for (let j = 1; j < nz; j++) for (let i = 0; i < nx; i++) this.add('foundation-tie', '3020', color, i * 8 + 2, 1, j * 4 - 1, 1);
    this.floor('ground-floor', color, 0, 2, 0, nx, nz);
  }
  columns(role: string, color: Color, xs: number[], zs: number[], y: number, levels: number) {
    for (const x of xs) for (const z of zs) for (let h = 0; h < levels; h++) this.add(role, '3003', color, x, y + h * 3, z);
  }
}

function finish(b: Builder, id: string, name: string, domain: string, tier: string,
  description: string, palette: FrontierModel['palette']): FrontierModel {
  assert.ok(b.parts.length >= 100 && b.parts.length <= 512, `${id}: ${b.parts.length}`);
  const conflicts = b.parts.flatMap((p, i) => b.parts.slice(i + 1).filter(q => footprint(p, q)
    && p.y < q.y + dims(q).h && q.y < p.y + dims(p).h).map(q => `${p.id}/${q.id}`));
  const unsupported = b.parts.filter(p => p.y && !b.parts.some(q =>
    q.y + dims(q).h === p.y && footprint(p, q))).map(p => p.id);
  assert.deepEqual(validate(b.parts), [], `${id}: collisions=${conflicts} unsupported=${unsupported}`);
  assert.equal(components(b.parts), 1, `${id}: disconnected`);
  const ordered = [...b.parts].sort((a, c) => a.y - c.y);
  const prefix: Part[] = [];
  for (const p of ordered) {
    assert.equal(insertion(prefix, p), null, `${id}/${p.id}`); prefix.push(p);
  }
  assert.deepEqual([...new Set(b.parts.map(p => p.color))].sort(), Object.keys(palette).sort());
  const deps = dependencies(b.parts), depth: Record<string, number> = {};
  for (const p of ordered) depth[p.id] = 1 + Math.max(0, ...deps[p.id].map(i => depth[i]));
  return { id, name, domain, tier, description, palette, structure: { version: 1, parts: b.parts }, modules: b.modules,
    stats: { parts: b.parts.length, layers: new Set(b.parts.map(p => p.y)).size,
      depth: Math.max(...Object.values(depth)), types: new Set(b.parts.map(p => p.partId)).size, extent: bounds(b.parts) } };
}

function courtyard() {
  const b = new Builder(); b.foundation(4, 6);
  for (const y of [3, 6, 9]) {
    for (const x of [0, 8, 16, 24]) {
      b.add('outer-wall', '3007', 'white', x, y, 0);
      b.add('outer-wall', '3007', 'white', x, y, 22);
    }
    for (const z of [2, 6, 10, 14, 18]) for (const x of [0, 30]) b.add('outer-wall', '3001', 'white', x, y, z, 1);
  }
  for (const x of [4, 10, 20, 26]) b.columns('arcade', 'white', [x], [4, 18], 3, 3);
  b.floor('roof-north', 'red', 0, 12, 0, 4, 2); b.floor('roof-south', 'red', 0, 12, 16, 4, 2);
  for (const x of [0, 28]) for (const z of [8, 12]) b.add('roof-side', '3031', 'red', x, 12, z);
  b.floor('pool', 'blue', 8, 3, 8, 2, 2);
  for (const x of [6, 24]) for (const z of [8, 12]) b.add('seating', '3001', 'white', x, 3, z, 1);
  return finish(b, 'courtyard-museum', 'Courtyard Museum', 'civic architecture', 'structural',
    'A deep open courtyard, four perimeter galleries, paired arcades and a central pool; roofs are separate service regions.',
    { gray: 'foundation', white: 'masonry and seating', red: 'gallery roofs', blue: 'courtyard pool' });
}

function terminal() {
  const b = new Builder(); b.foundation(5, 4);
  b.columns('platform-columns', 'white', [0, 8, 16, 24, 32, 38], [0, 6, 10, 14], 3, 4);
  for (const y of [3, 6]) for (const x of [0, 8, 16, 24, 32]) b.add('back-wall', '3008', 'white', x, y, 0);
  // The rear wall occupies the first row; move it between the column rows.
  b.parts.filter(p => b.modules['back-wall'].includes(p.id)).forEach(p => { p.z = 2; });
  b.floor('main-canopy', 'blue', 0, 15, 0, 5, 4);
  for (const x of [4, 12, 20, 28, 34]) for (const z of [4, 10]) b.add('platform-seat', '3010', 'red', x, 3, z);
  b.columns('clock-tower', 'white', [16, 22], [4, 10], 16, 4);
  b.floor('tower-roof', 'red', 16, 28, 4, 1, 2);
  for (const z of [4, 8]) b.add('tower-crest', '3031', 'blue', 18, 29, z);
  return finish(b, 'intercity-terminal', 'Intercity Terminal', 'transport infrastructure', 'structural',
    'A 40-stud station with deep platforms, ten benches, a full canopy and an independently serviceable clock tower.',
    { gray: 'platform', white: 'structure', blue: 'canopy and crest', red: 'seats and tower roof' });
}

function citadel() {
  const b = new Builder(); b.foundation(4, 6, 'green');
  for (const [x, z] of [[0, 0], [24, 0], [0, 16], [24, 16]]) {
    for (const y of [3, 6, 9, 12, 15, 18]) {
      b.add('tower-wall', '3007', 'gray', x, y, z);
      b.add('tower-wall', '3007', 'gray', x, y, z + 6);
      for (const dx of [0, 6]) b.add('tower-wall', '3001', 'gray', x + dx, y, z + 2, 1);
    }
    b.floor('tower-cap', 'white', x, 21, z, 1, 2);
    for (const dx of [0, 3, 6]) for (const dz of [0, 6]) b.add('battlement', '3003', 'gray', x + dx, 22, z + dz);
  }
  for (const z of [0, 22]) for (const x of [8, 16]) for (const y of [3, 6, 9])
    b.add('curtain-wall', '3007', 'gray', x, y, z);
  for (const x of [0, 30]) for (const y of [3, 6, 9]) b.add('curtain-wall', '3007', 'gray', x, y, 8, 1);
  for (const x of [8, 16]) for (const z of [0, 20]) b.add('wall-walk', '3035', 'white', x, 12, z);
  return finish(b, 'four-tower-citadel', 'Four-Tower Citadel', 'fortified architecture', 'systems',
    'Four hollow six-course towers, connected curtain walls, elevated walkways and aligned battlements around an open court.',
    { green: 'ground', gray: 'masonry', white: 'caps and walkways' });
}

function vessel() {
  const b = new Builder();
  b.floor('keel', 'gray', 0, 0, 4, 5, 2);
  for (const x of [6, 14, 22, 30]) b.add('keel-tie', '3020', 'gray', x, 1, 6);
  for (const x of [2, 10, 18, 26, 34]) b.add('keel-tie', '3020', 'gray', x, 1, 7, 1);
  for (const x of [2, 10, 18, 26, 34]) b.add('keel-tie', '3022', 'gray', x, 1, 4);
  b.floor('lower-hull', 'blue', 0, 2, 2, 5, 3);
  for (const y of [3, 6, 9]) {
    for (const x of [0, 8, 16, 24, 32]) for (const z of [2, 12]) b.add('hull-wall', '3007', 'blue', x, y, z);
    for (const x of [0, 38]) for (const z of [4, 8]) b.add('end-wall', '3001', 'blue', x, y, z, 1);
  }
  b.columns('hold-ribs', 'blue', [4, 12, 20, 28, 36], [6], 3, 3);
  b.floor('deck', 'white', 0, 12, 2, 5, 3);
  b.columns('bridge', 'white', [0, 6], [2, 6, 10], 13, 3);
  b.floor('bridge-roof', 'blue', 0, 22, 2, 1, 3);
  for (const x of [12, 22, 32]) for (const z of [4, 8]) for (const y of [13, 16, 19])
    b.add('cargo', '3001', 'red', x, y, z);
  for (const x of [8, 16, 24, 32]) for (const z of [2, 13]) b.add('deck-rail', '3460', 'white', x, 13, z);
  return finish(b, 'coastal-cargo-vessel', 'Coastal Cargo Vessel', 'maritime transport', 'structural',
    'A widened hull above a narrow keel, enclosed hold, removable deck, six cargo stacks and a raised navigation bridge; no moving propulsion.',
    { gray: 'keel', blue: 'hull and bridge roof', white: 'deck and bridge', red: 'cargo' });
}

function plant() {
  const b = new Builder(); b.foundation(5, 6);
  for (const x of [0, 16, 32]) {
    for (const y of [3, 6, 9, 12, 15]) for (const z of [0, 6]) b.add('reactor-wall', '3007', 'white', x, y, z);
    for (const y of [3, 6, 9, 12, 15]) for (const dx of [0, 6]) b.add('reactor-wall', '3001', 'white', x + dx, y, 2, 1);
    b.floor('reactor-cap', 'blue', x, 18, 0, 1, 2);
    b.columns('exhaust', 'red', [x + 2], [2], 19, 4);
    b.add('exhaust-cap', '3031', 'gray', x + 1, 31, 1);
  }
  b.columns('gallery-support', 'white', [0, 8, 16, 24, 32, 38], [12, 16, 20], 3, 4);
  b.floor('service-gallery', 'blue', 0, 15, 12, 5, 3);
  for (const x of [0, 8, 16, 24, 32]) b.add('service-rail', '3008', 'red', x, 16, 23);
  for (const x of [8, 24]) {
    b.add('link', '3035', 'gray', x - 2, 19, 4);
    b.add('link', '3035', 'gray', x + 6, 19, 4);
    b.add('link-tie', '3020', 'gray', x + 4, 20, 4);
  }
  return finish(b, 'process-service-plant', 'Process Service Plant', 'industrial maintenance', 'systems',
    'Three hollow process towers with exhaust stacks, a rear access gallery and capped service links; nominal support only, not fluid simulation.',
    { gray: 'foundation and links', white: 'walls and supports', blue: 'caps and gallery', red: 'exhaust and rails' });
}

function archive() {
  const b = new Builder(); b.foundation(4, 4);
  for (let level = 0; level < 4; level++) {
    const y = 3 + level * 10;
    b.columns(`storey-${level}`, 'white', [0, 8, 16, 24, 30], [0, 6, 10, 14], y, 3);
    for (const x of [4, 12, 20]) for (const z of [4, 10]) {
      b.add(`shelves-${level}`, '3010', 'blue', x, y, z);
      b.add(`shelves-${level}`, '3010', 'blue', x, y + 3, z);
    }
    b.floor(`floor-${level}`, level === 3 ? 'red' : 'gray', 0, y + 9, 0, 4, 4);
  }
  return finish(b, 'four-storey-archive', 'Four-Storey Archive', 'multi-level building', 'long-horizon',
    'Four deep open-sided storeys, 48 shelf bricks and independently supported floor panels; buried repairs propagate through multiple floors.',
    { gray: 'foundation and floors', white: 'columns', blue: 'shelves', red: 'roof' });
}

let cache: FrontierModel[] | undefined;
export function frontierModels() {
  return cache ??= [courtyard(), terminal(), vessel(), citadel(), plant(), archive()];
}
