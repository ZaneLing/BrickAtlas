import { CATALOG, COLORS, type Edge, type Part, type RelativeNode, type Structure } from './shared';

export const dims = (p: Pick<Part, 'partId' | 'turn'>) => {
  const s = CATALOG[p.partId];
  if (!s) throw new Error('unknown_part');
  return { w: p.turn % 2 ? s.d : s.w, d: p.turn % 2 ? s.w : s.d, h: s.h };
};
export function isPart(value: unknown): value is Part {
  if (!value || typeof value !== 'object') return false;
  const p = value as Part;
  return typeof p.id === 'string' && /^[\w-]{1,60}$/.test(p.id)
    && Object.hasOwn(CATALOG, p.partId) && Object.hasOwn(COLORS, p.color)
    && [0, 1, 2, 3].includes(p.turn)
    && [p.x, p.y, p.z].every(n => Number.isInteger(n) && n >= 0 && n <= 24);
}
export function decode(value: unknown): Structure | null {
  if (!value || typeof value !== 'object') return null;
  const o = value as Record<string, unknown>;
  if (o.version !== 1 || Boolean(o.parts) === Boolean(o.nodes)) return null;
  let parts: Part[] = [];
  if (Array.isArray(o.parts)) {
    if (!o.parts.every(isPart)) return null;
    parts = o.parts.map(p => ({ id: p.id, partId: p.partId, color: p.color, x: p.x, y: p.y, z: p.z, turn: p.turn }));
  } else if (Array.isArray(o.nodes)) {
    if (o.nodes.length > 64) return null;
    for (const n of o.nodes as RelativeNode[]) {
      if (!n || !Array.isArray(n.offset) || n.offset.length !== 3
        || !n.offset.every(v => Number.isInteger(v) && Math.abs(v) <= 32)) return null;
      const parent = parts.find(p => p.id === n.parent);
      if (n.parent !== null && !parent) return null;
      const p = { id: n.id, partId: n.partId, color: n.color, turn: n.turn,
        x: (parent?.x ?? 0) + n.offset[0], y: (parent?.y ?? 0) + n.offset[1], z: (parent?.z ?? 0) + n.offset[2] };
      if (!isPart(p)) return null;
      parts.push(p);
    }
  } else return null;
  if (parts.length > 64 || new Set(parts.map(p => p.id)).size !== parts.length) return null;
  return { version: 1, parts };
}
export function relative(s: Structure) {
  const nodes: RelativeNode[] = s.parts.map((p, i) => {
    const parent = s.parts[i - 1];
    return { id: p.id, partId: p.partId, color: p.color, parent: parent?.id ?? null,
      offset: [p.x - (parent?.x ?? 0), p.y - (parent?.y ?? 0), p.z - (parent?.z ?? 0)], turn: p.turn };
  });
  return { version: 1, nodes };
}
export const footprint = (a: Part, b: Part) => {
  const x = dims(a), y = dims(b);
  return Math.max(0, Math.min(a.x + x.w, b.x + y.w) - Math.max(a.x, b.x))
    * Math.max(0, Math.min(a.z + x.d, b.z + y.d) - Math.max(a.z, b.z));
};
export function contact(a: Part, b: Part) {
  return a.y + dims(a).h === b.y || b.y + dims(b).h === a.y ? footprint(a, b) : 0;
}
export function edges(parts: Part[]): Edge[] {
  return parts.flatMap((a, i) => parts.slice(i + 1).flatMap(b => {
    const studs = contact(a, b);
    return studs ? [{ a: a.id, b: b.id, studs }] : [];
  }));
}
export function components(parts: Part[]) {
  const unvisited = new Set(parts.map(p => p.id));
  let count = 0;
  for (const root of parts) {
    if (!unvisited.delete(root.id)) continue;
    count++;
    const stack = [root];
    while (stack.length) {
      const a = stack.pop()!;
      for (const b of parts) if (unvisited.has(b.id) && contact(a, b)) {
        unvisited.delete(b.id); stack.push(b);
      }
    }
  }
  return count;
}
export function validate(parts: Part[]): string[] {
  if (parts.length > 64 || parts.some(p => !isPart(p))) return ['invalid_part'];
  const issues = new Set<string>();
  if (!parts.length) issues.add('empty');
  if (new Set(parts.map(p => p.id)).size !== parts.length) issues.add('duplicate_id');
  for (const p of parts) {
    const s = dims(p);
    if (p.x + s.w > 32 || p.y + s.h > 32 || p.z + s.d > 32) issues.add('out_of_bounds');
    if (parts.some(q => p !== q && footprint(p, q) > 0 && p.y < q.y + dims(q).h && p.y + s.h > q.y)) issues.add('overlap');
    if (p.y > 0 && !parts.some(q => p !== q && q.y + dims(q).h === p.y && footprint(p, q) > 0)) issues.add('unsupported');
  }
  return [...issues];
}
export function removeIssue(parts: Part[], id: string) {
  const p = parts.find(p => p.id === id);
  if (!p) return 'unknown_id';
  if (parts.some(q => q.id !== id && q.y >= p.y + dims(p).h && footprint(p, q) > 0)) return 'blocked';
  const rest = parts.filter(q => q.id !== id);
  return rest.length ? validate(rest)[0] ?? null : null;
}
export function insertIssue(parts: Part[], p: Part) {
  const issue = validate([...parts, p])[0];
  if (issue) return issue;
  return parts.some(q => q.y >= p.y + dims(p).h && footprint(p, q) > 0) ? 'blocked' : null;
}
export function bom(parts: Part[]) {
  const result: Record<string, number> = {};
  for (const p of parts) result[`${p.partId}:${p.color}`] = (result[`${p.partId}:${p.color}`] ?? 0) + 1;
  return result;
}
export function cells(parts: Part[], colored = false) {
  const out = new Set<string>();
  for (const p of parts) {
    const d = dims(p);
    for (let x = p.x; x < p.x + d.w; x++) for (let z = p.z; z < p.z + d.d; z++)
      for (let y = p.y; y < p.y + d.h; y++) out.add(`${x},${y},${z}${colored ? ':' + p.color : ''}`);
  }
  return out;
}
export const key = (p: Part, color = true) => {
  const d = dims(p);
  return [p.partId, color ? p.color : '', p.x, p.y, p.z, d.w, d.d].join(':');
};
export const f1 = (correct: number, expected: number, actual: number) =>
  expected + actual ? 2 * correct / (expected + actual) : 1;
export function compare(target: Part[], actual: Part[]) {
  const pools = new Map<string, string[]>();
  for (const p of target) pools.set(key(p), [...(pools.get(key(p)) ?? []), p.id]);
  const mapping = new Map<string, string>();
  for (const p of actual) {
    const id = pools.get(key(p))?.pop();
    if (id) mapping.set(p.id, id);
  }
  const tEdges = new Set(edges(target).map(e => [e.a, e.b, String(e.studs)].join('|')));
  const edgeKey = (a: string, b: string, n: number) => [...[a, b].sort(), n].join('|');
  const canonicalEdges = new Set(edges(target).map(e => edgeKey(e.a, e.b, e.studs)));
  const aEdges = edges(actual);
  const correctEdges = aEdges.filter(e => mapping.has(e.a) && mapping.has(e.b)
    && canonicalEdges.has(edgeKey(mapping.get(e.a)!, mapping.get(e.b)!, e.studs))).length;
  const tc = cells(target), ac = cells(actual);
  const intersection = [...tc].filter(c => ac.has(c)).length;
  const tb = bom(target), ab = bom(actual);
  const bomMatches = Object.keys(tb).reduce((n, k) => n + Math.min(tb[k], ab[k] ?? 0), 0);
  return {
    partF1: f1(mapping.size, target.length, actual.length),
    bomF1: f1(bomMatches, target.length, actual.length),
    edgeF1: f1(correctEdges, tEdges.size, aEdges.length),
    occupancyIoU: intersection / Math.max(1, new Set([...tc, ...ac]).size),
    exact: mapping.size === target.length && actual.length === target.length && !validate(actual).length,
  };
}
export function canonicalGeometry(parts: Part[]) {
  return [0, 1, 2, 3].map(turn => {
    let rotated = parts.map(p => ({ ...p }));
    for (let i = 0; i < turn; i++) rotated = rotated.map(p => ({
      ...p, x: -p.z - dims(p).d, z: p.x, turn: (p.turn + 1) % 4,
    }));
    const x = Math.min(...rotated.map(p => p.x)), z = Math.min(...rotated.map(p => p.z));
    const y = Math.min(...rotated.map(p => p.y));
    return rotated.map(p => key({ ...p, x: p.x - x, y: p.y - y, z: p.z - z }, false)).sort().join('|');
  }).sort()[0];
}
export function bounds(parts: Part[]) {
  return { x: Math.max(...parts.map(p => p.x + dims(p).w)), y: Math.max(...parts.map(p => p.y + dims(p).h)),
    z: Math.max(...parts.map(p => p.z + dims(p).d)) };
}
