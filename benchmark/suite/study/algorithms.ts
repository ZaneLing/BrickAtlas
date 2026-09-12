import type { PublicTask, Part } from '../shared';
import { decode, dims } from '../geometry';
import { dataset } from '../v2/dataset';
import { independentGeometry, independentRelations } from './independent';

// For this vertical grid domain, bottom-up sorting is a complete constructive plan
// on valid structures: supporters are lower; future pieces cannot block insertion.
export function heightPlan(input: PublicTask): unknown {
  const target = decode(input.input.target); if (!target) return null;
  const order = [...target.parts].sort((a, b) => a.y - b.y || a.id.localeCompare(b.id));
  if (input.input.direction === 'disassemble') order.reverse();
  return { order: order.map(p => p.id) };
}
export function independentQA(input: PublicTask) {
  const structure = decode(input.input.structure);
  return structure ? independentRelations(structure.parts, String(input.input.a), String(input.input.b)) : null;
}
let training: { id: string; group: string; parts: Part[]; bom: Record<string, number>; box: number[] }[] | undefined;
export function trainRetrieval(input: PublicTask) {
  if (!training) training = dataset().filter(m => m.split === 'train').map(m => ({
    id: m.id, group: m.group, parts: m.structure.parts,
    bom: Object.fromEntries([...new Set(m.structure.parts.map(p => `${p.partId}:${p.color}`))]
      .map(k => [k, m.structure.parts.filter(p => `${p.partId}:${p.color}` === k).length])),
    box: [m.parameters.width, m.parameters.height, m.parameters.depth],
  }));
  if (!['reconstruct', 'complete', 'generate', 'repair'].includes(input.kind)) return null;
  const bom = input.input.billOfMaterials as Record<string, number> | undefined;
  const extent = (input.input.requirements as { extent?: { x: number; y: number; z: number } } | undefined)?.extent;
  if (!bom && !extent) return null;
  let best = training[0], score = -Infinity;
  for (const candidate of training) {
    const rank = bom ? Object.entries(bom).reduce((n, [k, v]) => n + Math.min(v, candidate.bom[k] ?? 0), 0)
      / (Object.values(bom).reduce((a, b) => a + b, 0) + candidate.parts.length)
      : -candidate.box.reduce((n, value, i) => n + Math.abs(value - [extent!.x, extent!.y, extent!.z][i]), 0);
    if (rank > score) { best = candidate; score = rank; }
  }
  const structure = { version: 1, parts: structuredClone(best.parts) };
  return { answer: input.kind === 'repair' ? { structure, faultIds: [] } : structure,
    retrieved: { id: best.id, group: best.group, split: 'train', similarity: score },
    note: 'BOM/envelope retrieval, no image access. Full retrieved structure; no target-aware adaptation.' };
}
export function independentPlanCheck(input: PublicTask, order: string[]) {
  const target = decode(input.input.target)!;
  const assemble = input.input.direction === 'assemble', seen = new Set<string>();
  let state = assemble ? [] as Part[] : [...target.parts];
  for (const id of order) {
    const p = target.parts.find(p => p.id === id);
    if (!p || seen.has(id)) return false;
    const next = assemble ? [...state, p] : state.filter(q => q.id !== id);
    const shape = independentGeometry(next);
    if (!shape.collisionFree || !shape.supported || !shape.withinBounds) return false;
    const d = dims(p);
    // Independently use occupied cells above the footprint to inspect the corridor.
    for (let x = p.x; x < p.x + d.w; x++) for (let z = p.z; z < p.z + d.d; z++) {
      for (let y = p.y + d.h; y < 32; y++) if (shape.occupied.has(`${x},${y},${z}`)) return false;
    }
    state = next; seen.add(id);
  }
  return seen.size === target.parts.length;
}
