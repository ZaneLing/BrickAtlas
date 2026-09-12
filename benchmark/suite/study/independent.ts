import { CATALOG, type Part } from '../shared';

// Independent cell enumerations: no geometry.ts, v2/evaluate.ts or oracle imports.
function size(p: Part) {
  const d = CATALOG[p.partId];
  return { x: p.turn % 2 ? d.d : d.w, y: d.h, z: p.turn % 2 ? d.w : d.d };
}
function signature(p: Part) { return JSON.stringify([p.partId, p.color, p.x, p.y, p.z, size(p)]); }
function bag(values: string[]) {
  const m = new Map<string, number>(); for (const x of values) m.set(x, (m.get(x) ?? 0) + 1); return m;
}
function common(a: string[], b: string[]) {
  const left = bag(a), right = bag(b);
  return [...left].reduce((n, [k, v]) => n + Math.min(v, right.get(k) ?? 0), 0);
}
function enumerate(parts: Part[]) {
  const occupied = new Map<string, Part[]>(), faces = new Map<string, Set<string>>();
  for (const p of parts) {
    const d = size(p), bottom = new Set<string>(), top = new Set<string>();
    for (let x = p.x; x < p.x + d.x; x++) for (let z = p.z; z < p.z + d.z; z++) {
      bottom.add(`${x},${p.y},${z}`); top.add(`${x},${p.y + d.y},${z}`);
      for (let y = p.y; y < p.y + d.y; y++) {
        const k = `${x},${y},${z}`; occupied.set(k, [...(occupied.get(k) ?? []), p]);
      }
    }
    faces.set(p.id + ':bottom', bottom); faces.set(p.id + ':top', top);
  }
  const links: { a: string; b: string; studs: number }[] = [];
  for (const lower of parts) for (const upper of parts) if (lower.id !== upper.id) {
    const top = faces.get(lower.id + ':top')!, bottom = faces.get(upper.id + ':bottom')!;
    const studs = [...top].filter(k => bottom.has(k)).length;
    if (studs) links.push({ a: lower.id, b: upper.id, studs });
  }
  return { occupied, links };
}
export function independentGeometry(parts: Part[]) {
  const { occupied, links } = enumerate(parts);
  const collisionFree = [...occupied.values()].every(ps => ps.length === 1);
  const supported = parts.every(p => !p.y || links.some(e => e.b === p.id));
  const withinBounds = parts.every(p => {
    const d = size(p); return p.x + d.x <= 32 && p.y + d.y <= 32 && p.z + d.z <= 32;
  });
  return { collisionFree, supported, withinBounds, links, occupied };
}
function firstHits(cells: Map<string, Part[]>) {
  const rays = new Map<string, { depth: number; point: string }>();
  for (const [point, parts] of cells) {
    const xyz = point.split(',').map(Number);
    for (let a = 0; a < 3; a++) {
      const k = `${a}:${xyz.filter((_, i) => i !== a)}`;
      if (!rays.has(k) || rays.get(k)!.depth < xyz[a]) rays.set(k, { depth: xyz[a], point: `${a}:${point}:${parts[0].color}` });
    }
  }
  return [...rays.values()].map(x => x.point);
}
export function independentMetrics(target: Part[], actual: Part[]) {
  const t = independentGeometry(target), a = independentGeometry(actual);
  const f1 = (n: number, x: number, y: number) => x + y ? 2 * n / (x + y) : 1;
  const pm = common(target.map(signature), actual.map(signature));
  const bm = common(target.map(p => `${p.partId}:${p.color}`), actual.map(p => `${p.partId}:${p.color}`));
  const tc = [...t.occupied.keys()], ac = [...a.occupied.keys()];
  const colored = (m: Map<string, Part[]>) => [...new Set([...m].flatMap(([k, ps]) => ps.map(p => `${k}:${p.color}`)))];
  const ts = firstHits(t.occupied), as = firstHits(a.occupied), sm = common(ts, as);
  const iou = (x: string[], y: string[]) => { const n = common(x, y); return n / Math.max(1, x.length + y.length - n); };
  const edgeSignature = (e: { a: string; b: string; studs: number }, parts: Part[]) =>
    JSON.stringify([[signature(parts.find(p => p.id === e.a)!), signature(parts.find(p => p.id === e.b)!)].sort(), e.studs]);
  const tm = t.links.map(e => edgeSignature(e, target)), am = a.links.map(e => edgeSignature(e, actual));
  return {
    partF1: f1(pm, target.length, actual.length), bomF1: f1(bm, target.length, actual.length),
    occupancyIoU: iou(tc, ac), coloredOccupancyIoU: iou(colored(t.occupied), colored(a.occupied)),
    surfaceF1: f1(sm, ts.length, as.length), edgeF1: f1(common(tm, am), tm.length, am.length),
    collisionFree: Number(a.collisionFree), supported: Number(a.supported), withinBounds: Number(a.withinBounds),
  };
}

export function independentRelations(parts: Part[], aId: string, bId: string) {
  const { links } = independentGeometry(parts), a = parts.find(p => p.id === aId)!, b = parts.find(p => p.id === bId)!;
  const distance = new Map([[aId, 0]]);
  // Bellman-Ford relaxation differs from the GT's breadth-first traversal.
  for (let i = 0; i < parts.length; i++) for (const e of links) for (const [x, y] of [[e.a, e.b], [e.b, e.a]]) {
    if (distance.has(x) && (distance.get(y) ?? Infinity) > distance.get(x)! + 1) distance.set(y, distance.get(x)! + 1);
  }
  const contact = links.find(e => e.a === aId && e.b === bId || e.b === aId && e.a === bId);
  return { connected: !!contact, above: a.y >= b.y + size(b).y,
    contactStuds: contact?.studs ?? 0, shortestPath: distance.get(bId) ?? -1 };
}
