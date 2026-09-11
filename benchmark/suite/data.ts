import { createHash } from 'node:crypto';
import { CATALOG, VERSION, type Color, type DatasetSummary, type Part, type Split, type Structure } from './shared';
import { bounds, canonicalGeometry, edges, insertIssue, validate } from './geometry';

export const digest = (v: unknown) => createHash('sha256').update(typeof v === 'string' ? v : JSON.stringify(v)).digest('hex');
export interface ModelRecord {
  id: string; group: string; family: string; split: Split;
  description: string; parameters: { width: number; depth: number; height: number; palette: number };
  structure: Structure; connections: ReturnType<typeof edges>;
  provenance: { source: 'procedural'; license: 'CC0-1.0'; generator: string };
}
export const FAMILIES = ['bridge', 'bench', 'shelf', 'wall', 'tower', 'platform', 'staircase', 'gate'] as const;
const WIDTHS = [4, 6, 8], DEPTHS = [2, 4], HEIGHTS = [1, 2, 3];
const PALETTES: [Color, Color][] = [['red', 'yellow'], ['blue', 'white'], ['green', 'gray'], ['yellow', 'blue']];

function generate(family: string, width: number, depth: number, height: number, palette: number): Part[] {
  const parts: Part[] = [];
  const [body, accent] = PALETTES[palette];
  function add(w: number, d: number, h: number, x: number, y: number, z: number, color: Color) {
    const found = Object.entries(CATALOG).find(([, c]) => c.w === w && c.d === d && c.h === h);
    const reverse = Object.entries(CATALOG).find(([, c]) => c.w === d && c.d === w && c.h === h);
    if (!found && !reverse) {
      // Tile wide surfaces with available 2-stud strips; no invented part types.
      if (d > 2 && d % 2 === 0) { for (let dz = 0; dz < d; dz += 2) add(w, 2, h, x, y, z + dz, color); return; }
      throw new Error(`No catalog brick ${w}x${d}x${h}`);
    }
    parts.push({ id: `p${parts.length + 1}`, partId: (found ?? reverse)![0], color, x, y, z, turn: found ? 0 : 1 });
  }
  function posts(y: number, count = height) {
    for (let level = 0; level < count; level++) for (const x of [0, width - 1]) for (const z of [0, depth - 1]) {
      add(1, 1, 3, x, y + level * 3, z, body);
    }
  }
  if (family === 'bridge') {
    for (let level = 0; level < height; level++) for (const x of [0, width - 1]) add(1, depth, 3, x, level * 3, 0, body);
    add(width, depth, 1, 0, height * 3, 0, accent);
  } else if (family === 'bench') {
    posts(0);
    add(width, depth, 1, 0, height * 3, 0, accent);
    add(width, 1, 3, 0, height * 3 + 1, depth - 1, body);
  } else if (family === 'shelf') {
    add(width, depth, 1, 0, 0, 0, accent);
    posts(1);
    add(width, depth, 1, 0, height * 3 + 1, 0, accent);
    posts(height * 3 + 2, 1);
    add(width, depth, 1, 0, height * 3 + 5, 0, accent);
  } else if (family === 'wall') {
    add(width, depth, 1, 0, 0, 0, accent);
    for (let level = 0; level < height; level++) {
      add(width, 1, 3, 0, 1 + level * 3, Math.floor(depth / 2), body);
    }
  } else if (family === 'tower') {
    add(width, depth, 1, 0, 0, 0, accent);
    for (let level = 0; level < height; level++) {
      add(2, 2, 3, Math.floor((width - 2) / 2), 1 + level * 3, Math.floor((depth - 2) / 2), body);
    }
    add(width, depth, 1, 0, height * 3 + 1, 0, accent);
  } else if (family === 'platform') {
    for (let level = 0; level < height; level++) {
      add(width, depth, 3, 0, level * 3, 0, body);
    }
    add(width, depth, 1, 0, height * 3, 0, accent);
  } else if (family === 'staircase') {
    add(width, depth, 1, 0, 0, 0, accent);
    for (let x = 0; x < width; x += 2) for (let level = 0; level <= Math.min(x / 2, height); level++) {
      add(2, 2, 3, x, 1 + level * 3, 0, body);
    }
  } else if (family === 'gate') {
    add(width, depth, 1, 0, 0, 0, accent);
    for (let level = 0; level < height; level++) for (const x of [0, width - 1]) {
      add(1, 1, 3, x, 1 + level * 3, Math.floor(depth / 2), body);
    }
    add(width, 1, 1, 0, height * 3 + 1, Math.floor(depth / 2), accent);
  }
  return parts.sort((a, b) => a.y - b.y || a.x - b.x || a.z - b.z).map((p, i) => ({ ...p, id: `p${i + 1}` }));
}

let cache: ModelRecord[] | undefined;
export function models(): ModelRecord[] {
  if (cache) return cache;
  const records: ModelRecord[] = [], seen = new Set<string>();
  for (const family of FAMILIES) for (const width of WIDTHS) for (const depth of DEPTHS)
    for (const height of HEIGHTS) for (let palette = 0; palette < PALETTES.length; palette++) {
      const parts = generate(family, width, depth, height, palette);
      if (validate(parts).length) throw new Error(`${family} invalid: ${validate(parts)}`);
      const placed: Part[] = [];
      for (const p of parts) {
        const issue = insertIssue(placed, p);
        if (issue) throw new Error(`${family} invalid sequence: ${issue}`);
        placed.push(p);
      }
      const group = digest(canonicalGeometry(parts)).slice(0, 20);
      const id = digest({ group, palette }).slice(0, 20);
      if (seen.has(id)) continue;
      seen.add(id);
      const bucket = parseInt(group.slice(0, 8), 16) % 10;
      const split: Split = ['staircase', 'gate'].includes(family) ? 'test_ood'
        : bucket < 7 ? 'train' : bucket < 8 ? 'validation' : 'test_id';
      const box = bounds(parts);
      records.push({
        id, group, family, split, parameters: { width, depth, height, palette },
        description: `A ${family} built from ${PALETTES[palette][0]} bricks and ${PALETTES[palette][1]} plates. Bounding box ${box.x} x ${box.z} studs, ${box.y} plate layers.`,
        structure: { version: 1, parts }, connections: edges(parts),
        provenance: { source: 'procedural', license: 'CC0-1.0', generator: VERSION },
      });
    }
  const splits = new Map<string, Split>();
  for (const m of records) {
    if (splits.has(m.group) && splits.get(m.group) !== m.split) throw new Error('Geometry split leakage');
    splits.set(m.group, m.split);
  }
  cache = records;
  return records;
}

export function summary(): DatasetSummary {
  const data = models(), splits: Record<string, number> = {}, families: Record<string, number> = {};
  for (const m of data) {
    splits[m.split] = (splits[m.split] ?? 0) + 1;
    families[m.family] = (families[m.family] ?? 0) + 1;
  }
  return { version: VERSION, digest: digest(data), models: data.length,
    groups: new Set(data.map(m => m.group)).size, tasks: data.length * 8, splits, families,
    catalogParts: Object.keys(CATALOG).length };
}
