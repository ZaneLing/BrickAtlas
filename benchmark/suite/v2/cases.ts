import { CATALOG, COLORS, type FrameSpec, type Kind, type Part, type Structure } from '../shared';
import { bom, bounds, contact, dims, edges, key } from '../geometry';
import { digest } from '../data';
import type { Task } from '../tasks';
import { dataset, VERSION, type RecordV2 } from './dataset';
import { independentCheck } from '../research/independent-check';

export type Condition = 'ordinary' | 'layers' | 'symbolic' | 'default';
export interface CaseSpec {
  id: string; modelId: string; group: string; kind: Kind; variant: string; condition: Condition;
  split: RecordV2['split']; policy: string; difficulty: string;
}
export interface CaseTask extends Task { spec: CaseSpec }
export const structureSchema = { version: 1, parts: [{ id: 'piece', partId: '3005', color: 'red', x: 0, y: 0, z: 0, turn: 0 }] };
const specsById = new Map<string, CaseSpec>(), modelsById = new Map<string, RecordV2>();
let cached: CaseSpec[] | undefined;
export function caseSpecs() {
  if (cached) return cached;
  const result: CaseSpec[] = [];
  const push = (modelId: string, group: string, kind: Kind, variant: string, condition: Condition,
    split: CaseSpec['split'], policy: string, difficulty: string) => {
    const id = digest({ version: VERSION, modelId, kind, variant, condition }).slice(0, 24);
    const s = { id, modelId, group, kind, variant, condition, split, policy, difficulty };
    result.push(s); specsById.set(id, s);
  };
  // Catalog questions are not duplicated once per assembly or counted as unseen parts.
  for (const partId of Object.keys(CATALOG).sort()) for (const color of Object.keys(COLORS)) {
    const modelId = `catalog-${partId}-${color}`;
    push(modelId, `catalog-${partId}`, 'parts', color, 'ordinary', 'test_id', 'known-catalog', 'isolated');
  }
  for (const m of dataset()) {
    modelsById.set(m.id, m);
    const variants: [Kind, string, Condition[]][] = [
      ['relations', 'contact', ['default']], ['relations', 'separated', ['default']],
      ['reconstruct', 'full', ['ordinary', 'layers', 'symbolic']],
      ['generate', 'constraints', ['default']],
      ['complete', 'suffix', ['ordinary', 'layers', 'symbolic']],
      ['edit', 'rotate', ['default']], ['edit', 'recolor', ['default']], ['edit', 'remove', ['default']],
      ['plan', 'assemble', ['default']], ['plan', 'disassemble', ['default']],
      ['repair', 'none', ['ordinary', 'layers', 'symbolic']],
      ['repair', 'color', ['ordinary', 'layers', 'symbolic']],
      ['repair', 'shift', ['ordinary', 'layers', 'symbolic']],
    ];
    for (const [kind, variant, conditions] of variants) for (const c of conditions) {
      push(m.id, m.group, kind, variant, c, m.split, m.policy, m.difficulty);
    }
  }
  cached = result; return result;
}
export function getSpec(id: string) {
  caseSpecs(); const s = specsById.get(id);
  if (!s) throw new Error('Unknown v2 case'); return s;
}
function visualFrames(parts: Part[], condition: Condition): FrameSpec[] {
  if (condition === 'symbolic') return [];
  if (condition === 'layers') return [{ parts, view: 'iso', layer: null, title: 'Assembled reference' },
    ...[...new Set(parts.map(p => p.y))].sort((a, b) => a - b).map(y => ({
      parts: parts.filter(p => p.y === y), view: 'top' as const, layer: y, title: `Only pieces whose bottom Y=${y}; other pieces removed`,
    }))];
  return (['iso', 'top', 'front', 'side'] as const).map(view => ({ parts, view, layer: null, title: `Ordinary assembled ${view}` }));
}
export function relationOracle(parts: Part[], a: Part, b: Part) {
  const check = independentCheck([...parts].sort((p, q) => p.y - q.y));
  const neighbors = new Map(parts.map(p => [p.id, [] as string[]]));
  for (const e of check.contacts) {
    const [x, y] = e.pair.split('|'); neighbors.get(x)!.push(y); neighbors.get(y)!.push(x);
  }
  const distance = new Map([[a.id, 0]]), queue = [a.id];
  for (let i = 0; i < queue.length; i++) for (const next of neighbors.get(queue[i])!) {
    if (!distance.has(next)) { distance.set(next, distance.get(queue[i])! + 1); queue.push(next); }
  }
  const pair = [a.id, b.id].sort().join('|');
  return { connected: check.contacts.some(e => e.pair === pair), above: a.y >= b.y + dims(b).h,
    contactStuds: check.contacts.find(e => e.pair === pair)?.studs ?? 0, shortestPath: distance.get(b.id) ?? -1 };
}
export function taskForV2(spec: CaseSpec): CaseTask {
  caseSpecs();
  let target: Structure, source: Structure | null = null;
  let oracle: unknown, changedIds: string[] = [], frames: FrameSpec[] = [];
  let input: Record<string, unknown> = {}, prompt = '', schema: Record<string, unknown> = structureSchema;
  if (spec.kind === 'parts') {
    const [, partId, color] = spec.modelId.split('-');
    const p: Part = { id: 'query', partId, color: color as Part['color'], x: 0, y: 0, z: 0, turn: 0 };
    target = { version: 1, parts: [p] };
    frames = visualFrames([p], 'ordinary').slice(0, 2);
    oracle = { partId, color, studs: CATALOG[partId].w * CATALOG[partId].d };
    prompt = 'Identify the isolated known-catalog part, its color and top stud count. Return JSON.';
    schema = { partId: 'string', color: 'string', studs: 'integer' };
  } else {
    const m = modelsById.get(spec.modelId)!;
    target = structuredClone(m.structure);
    target.parts = target.parts.map((p, i) => ({ ...p, id: 'p' + digest(`${m.group}:${i}`).slice(0, 10) }));
    const parts = target.parts, n = m.seed;
    oracle = target;
    if (spec.kind === 'relations') {
      const pairs = parts.flatMap((a, i) => parts.slice(i + 1).filter(b =>
        (contact(a, b) > 0) === (spec.variant === 'contact')).map(b => [a, b]));
      if (!pairs.length) throw new Error('Relation stratum absent');
      let [a, b] = pairs[n % pairs.length]; if (n % 2) [a, b] = [b, a];
      input = { structure: target, a: a.id, b: b.id };
      oracle = relationOracle(parts, a, b);
      prompt = 'For a and b in the supplied structure, report direct stud connection, whether the whole body of a is at or above the top of b, number of directly mating studs, and shortest undirected stud-graph path length (-1 if disconnected).';
      schema = { connected: 'boolean', above: 'boolean', contactStuds: 'integer', shortestPath: 'integer' };
    } else if (spec.kind === 'generate') {
      const links = edges(parts);
      input = { requirements: { extent: bounds(parts), maxPieces: Math.min(64, parts.length + 8),
        minColors: 2, components: 1, minMaximumDegree: Math.min(3, Math.max(...parts.map(p => links.filter(e => e.a === p.id || e.b === p.id).length))) } };
      prompt = 'Design any legal grid assembly meeting all requirements: exact extents, minimum X/Y/Z=0, piece budget, at least minColors distinct colors, the specified connected component count, and at least one piece with minMaximumDegree directly connected neighbors. No reference volume or unique layout is required.';
    } else if (spec.kind === 'complete') {
      const count = Math.max(1, Math.floor(parts.length / 4));
      source = { version: 1, parts: structuredClone(parts.slice(0, -count)) };
      changedIds = parts.slice(-count).map(p => p.id);
      input = { current: source, billOfMaterials: bom(parts) };
      prompt = 'Complete the partial structure. Preserve every supplied piece in type, pose and color; output IDs may change. Return the full structure matching the reference information and BOM.';
    } else if (spec.kind === 'edit') {
      source = structuredClone(target);
      if (spec.variant === 'rotate') {
        const box = bounds(parts);
        target = { version: 1, parts: parts.map(p => ({ ...p, x: box.z - p.z - dims(p).d, z: p.x, turn: (p.turn + 1) % 4 })) };
        changedIds = parts.map(p => p.id);
        input = { current: source, operation: 'quarter-turn-positive-X-to-positive-Z' };
        prompt = 'Rotate the entire assembly a quarter-turn mapping positive X toward positive Z. Preserve Y, types and colors; translate minimum X/Z back to zero. Return the full structure.';
      } else if (spec.variant === 'recolor') {
        const color = parts[n % parts.length].color, replacement = color === 'blue' ? 'green' : 'blue';
        changedIds = parts.filter(p => p.color === color).map(p => p.id);
        for (const p of parts) if (p.color === color) p.color = replacement;
        input = { current: source, operation: { type: 'recolor', from: color, to: replacement } };
        prompt = `Recolor every ${color} piece to ${replacement}. Preserve all other properties and pieces. Return the full structure.`;
      } else {
        const top = [...parts].sort((a, b) => b.y + dims(b).h - a.y - dims(a).h)[0];
        changedIds = [top.id]; parts.splice(parts.indexOf(top), 1);
        input = { current: source, operation: { type: 'remove', id: top.id } };
        prompt = `Remove only ${top.id}, preserving every other piece. Return the full structure.`;
      }
      oracle = target;
    } else if (spec.kind === 'plan') {
      input = { target: { version: 1, parts: [...parts].sort((a, b) => a.id.localeCompare(b.id)) }, direction: spec.variant };
      oracle = { order: (spec.variant === 'assemble' ? parts : [...parts].reverse()).map(p => p.id) };
      schema = { order: ['piece ID'] };
      prompt = `Return all piece IDs exactly once in any executable ${spec.variant} order. Support, collision and vertical insertion/removal constraints apply. Do not output a final structure instead of a plan.`;
    } else if (spec.kind === 'repair') {
      source = structuredClone(target);
      const top = [...source.parts].sort((a, b) => b.y + dims(b).h - a.y - dims(a).h)[0];
      if (spec.variant !== 'none') changedIds = [top.id];
      if (spec.variant === 'color') top.color = top.color === 'blue' ? 'red' : 'blue';
      if (spec.variant === 'shift') {
        const candidates = [{ ...top, x: top.x + 1 }, { ...top, x: top.x - 1 },
          { ...top, z: top.z + 1 }, { ...top, z: top.z - 1 }];
        const shifted = candidates.find(p => p.x >= 0 && p.x <= 24 && p.z >= 0 && p.z <= 24
          && !source!.parts.some(q => q.id !== p.id && key(q) === key(p)));
        if (!shifted) throw new Error('No unambiguous exposed shift available');
        top.x = shifted.x; top.z = shifted.z;
      }
      input = { current: source, billOfMaterials: bom(parts) };
      oracle = { structure: target, faultIds: changedIds };
      schema = { structure: structureSchema, faultIds: ['wrong current piece ID; [] when no fault'] };
      prompt = 'Repair the current structure against the reference information and BOM. Return the full corrected structure and faultIds identifying wrong CURRENT pieces. There may be no fault; then faultIds is []. Preserve correct pieces.';
    } else {
      input = { billOfMaterials: bom(parts) };
      prompt = 'Reconstruct a complete legal structure from the supplied reference information and BOM. IDs may be arbitrary.';
    }
    if (['reconstruct', 'complete', 'repair'].includes(spec.kind)) {
      frames = visualFrames(target.parts, spec.condition);
      if (spec.condition === 'symbolic') input.reference = target;
      prompt += spec.condition === 'ordinary'
        ? ' Ordinary RGB only: alternate hidden layouts are allowed if colored positive-X/Y/Z first-hit grid surfaces, BOM, legal geometry and required preservation match.'
        : spec.condition === 'layers'
          ? ' Layer views disclose all pieces: full type/color/pose reconstruction is required, up to per-part yaw symmetry.'
          : ' Privileged SYMBOLIC reference: full type/color/pose reconstruction is required. This is not a visual result.';
    }
  }
  return { spec, target, source, oracle, changedIds, frames,
    public: { id: spec.id, kind: spec.kind, split: spec.split, family: spec.policy,
      prompt, input, responseSchema: schema, imageTitles: frames.map(f => f.title) } };
}
