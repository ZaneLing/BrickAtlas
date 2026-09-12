import { CATALOG, type FrameSpec, type Kind, type Part, type Structure, type Verdict } from '../shared';
import { taskFor, type Task } from '../tasks';
import { score } from '../score';
import { bom, bounds, cells, components, decode, dims, edges, f1, validate } from '../geometry';
import { digest } from '../data';
import { type ResearchRecord } from './dataset';

export type Condition = 'ordinary' | 'layers' | 'symbolic';
export interface ResearchTask extends Task { condition: Condition }
function ordinaryFrames(parts: Part[]): FrameSpec[] {
  return (['iso', 'top', 'front', 'side'] as const).map(view => ({
    parts, view, layer: null, title: `Ordinary assembled ${view}; no hidden layers revealed`,
  }));
}
export function surfaceSignature(parts: Part[]) {
  const rayMaps = [new Map<string, { depth: number; point: string }>(), new Map<string, { depth: number; point: string }>(), new Map<string, { depth: number; point: string }>()];
  for (const p of parts) {
    const d = dims(p);
    for (let x = p.x; x < p.x + d.w; x++) for (let y = p.y; y < p.y + d.h; y++) for (let z = p.z; z < p.z + d.d; z++) {
      const coords = [x, y, z];
      for (let axis = 0; axis < 3; axis++) {
        const ray = coords.filter((_, i) => i !== axis).join(':');
        const previous = rayMaps[axis].get(ray);
        if (!previous || coords[axis] > previous.depth) {
          rayMaps[axis].set(ray, { depth: coords[axis], point: `${axis}:${x}:${y}:${z}:${p.color}` });
        }
      }
    }
  }
  return new Set(rayMaps.flatMap(map => [...map.values()].map(x => x.point)));
}
export function researchTaskFor(model: ResearchRecord, kind: Kind, condition: Condition = 'ordinary'): ResearchTask {
  const t = taskFor({ ...model, id: digest(model.id).slice(0, 20) }, kind) as ResearchTask;
  t.condition = condition;
  t.public.id = digest(`${model.id}:${kind}:${condition}:research-task-v1`).slice(0, 24);
  t.public.input = { ...t.public.input, condition, coordinateSystem: 'min X/Z corner anchored at 0; X/Z studs, Y plate layers' };
  const target = t.target.parts;
  if (kind === 'generate') {
    const box = bounds(target), e = edges(target), degrees = target.map(p => e.filter(e => e.a === p.id || e.b === p.id).length);
    const requirements = { extent: box, maxPieces: Math.min(64, target.length + 8), minColors: 2,
      connectedComponents: 1, minMaximumDegree: Math.min(3, Math.max(...degrees)) };
    t.public.prompt = `Design any connected, supported brick assembly whose extents are ${box.x} studs along X, ${box.z} studs along Z, and ${box.y} plate layers high. Anchor minimum X,Y,Z at zero. Use at least two colors, at most ${requirements.maxPieces} pieces, and at least one part with ${requirements.minMaximumDegree} directly connected neighbors. Different valid layouts are welcome. No target voxel mask is supplied.`;
    t.public.input = { condition: 'text-constraints', requirements };
  }
  if (kind === 'edit') {
    t.source = structuredClone(model.structure);
    const old = t.source.parts, box = bounds(old);
    t.target = { version: 1, parts: old.map(p => ({ ...p, x: box.z - p.z - dims(p).d, z: p.x, turn: (p.turn + 1) % 4 })) };
    t.oracle = t.target;
    t.changedIds = old.map(p => p.id);
    t.public.prompt = 'Rotate the entire assembly by a quarter-turn about the vertical axis, mapping positive X toward positive Z. Keep every Y coordinate, part type and color. Translate the rotated result so minimum X and minimum Z remain zero. Return the full structure.';
    t.public.input = { condition: 'symbolic-spatial-edit', current: t.source, operation: 'quarter-turn-X-to-Z' };
  }
  if (kind === 'repair') {
    t.source = structuredClone(t.target);
    const leaf = [...t.source.parts].sort((a, b) => b.y + dims(b).h - a.y - dims(a).h)[0];
    const fault = model.seed % 3;
    t.changedIds = fault === 0 ? [] : [leaf.id];
    if (fault === 1) leaf.color = leaf.color === 'blue' ? 'red' : 'blue';
    if (fault === 2) leaf.x += 1;
    t.public.input = { ...t.public.input, current: t.source };
    t.oracle = { structure: t.target, faultIds: t.changedIds };
  }
  if (['reconstruct', 'complete', 'repair'].includes(kind)) {
    if (condition === 'ordinary') {
      t.frames = ordinaryFrames(t.target.parts);
      t.public.prompt = kind === 'reconstruct'
        ? 'Recover a complete legal structure from the ordinary assembled RGB views and the supplied BOM. Return the complete structure.'
        : kind === 'complete'
          ? 'Complete the supplied partial structure to match the ordinary assembled RGB views and BOM. Preserve every supplied piece. Return the complete structure.'
          : 'Repair the supplied CURRENT structure against the ordinary assembled RGB views and BOM. Return {structure, faultIds}; faultIds are the wrong CURRENT piece IDs, or [] if there is no fault. Preserve correct pieces.';
      t.public.prompt += ' Hidden layouts need not equal a private reference. Scoring requires matching colored first-hit surfaces along the positive X/Y/Z viewing axes, legal geometry and the supplied BOM. No layer oracle is provided.';
    } else if (condition === 'symbolic') {
      t.frames = [];
      t.public.input.reference = t.target;
      t.public.prompt += ' This is the privileged SYMBOLIC diagnostic: the complete reference program is supplied. Do not label this a visual result.';
    }
  }
  t.public.imageTitles = t.frames.map(f => f.title);
  return t;
}
export function researchScore(task: ResearchTask, answer: unknown): Verdict {
  if (task.public.kind === 'generate') {
    const structure = decode(answer);
    if (!structure?.parts.length) return { metrics: { format: 0, valid: 0, success: 0 }, issues: ['invalid_structure'] };
    const requirements = task.public.input.requirements as {
      extent: { x: number; y: number; z: number }; maxPieces: number; minColors: number; minMaximumDegree: number;
    };
    const p = structure.parts, box = bounds(p), links = edges(p);
    const conditions = {
      extent: ['x', 'y', 'z'].every(axis => box[axis as keyof typeof box] === requirements.extent[axis as keyof typeof box]),
      anchored: ['x', 'y', 'z'].every(axis => Math.min(...p.map(p => p[axis as 'x' | 'y' | 'z'])) === 0),
      pieceBudget: p.length <= requirements.maxPieces,
      colors: new Set(p.map(p => p.color)).size >= requirements.minColors,
      connected: components(p) === 1,
      branching: Math.max(...p.map(p => links.filter(e => e.a === p.id || e.b === p.id).length)) >= requirements.minMaximumDegree,
    };
    const issues = validate(p), correct = Object.values(conditions).filter(Boolean).length;
    return { metrics: { format: 1, valid: Number(!issues.length), success: Number(!issues.length && correct === 6),
      constraintAccuracy: correct / 6 }, issues: [...issues, ...Object.entries(conditions).filter(([, ok]) => !ok).map(([k]) => k)] };
  }
  const verdict = score(task, answer);
  if (['reconstruct', 'complete', 'repair'].includes(task.public.kind)) {
    const s = decode(task.public.kind === 'repair' && answer && typeof answer === 'object' && 'structure' in answer ? answer.structure : answer);
    if (s) {
      const expected = surfaceSignature(task.target.parts), actual = surfaceSignature(s.parts);
      const overlap = [...expected].filter(p => actual.has(p)).length;
      verdict.metrics.fullStructureSuccess = verdict.metrics.success;
      verdict.metrics.surfaceF1 = f1(overlap, expected.size, actual.size);
      const fullyValid = verdict.metrics.valid === 1 && verdict.metrics.bomF1 === 1 && verdict.metrics.surfaceF1 === 1
        && (verdict.metrics.preservation ?? 1) === 1
        && (task.public.kind !== 'repair' || verdict.metrics.localizationF1 === 1);
      verdict.metrics.success = Number(fullyValid);
      verdict.metrics.visibleSurfaceSuccess = Number(fullyValid);
      if (fullyValid) verdict.issues = [];
    }
  }
  return verdict;
}
