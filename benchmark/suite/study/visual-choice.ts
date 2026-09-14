import assert from 'node:assert/strict';
import { PNG } from 'pngjs';
import { CATALOG, type Part, type FrameSpec } from '../shared';
import { dims, key, validate } from '../geometry';

export const VISUAL_CHOICE_VERSION = 'blue-mask-analysis-synthesis-1';
export const MATCH_VIEWS = ['top', 'front', 'side'] as const;
export interface ChoicePose { label: string; x: number; y: number; z: number; turn: number }
export interface ChoiceInput {
  billOfMaterials: Record<string, number>;
  query: { partId: string; color: string };
  candidates: ChoicePose[];
  convention: { origin: string };
}
export interface Hypothesis { poseKey: string; label: string; parts: Part[] }
export interface Mask { width: number; height: number; pixels: Uint8Array; count: number }

export function choiceHypotheses(input: ChoiceInput): Hypothesis[] {
  assert.equal(input?.query?.color, 'blue', 'Only canonical blue-query tasks are supported');
  assert.ok(Object.hasOwn(CATALOG, input.query.partId));
  assert.equal(input.convention?.origin, 'Minimum X/Y/Z of the entire structure are each 0.');
  const entries = Object.entries(input.billOfMaterials);
  assert.equal(entries.length, 2, 'Two-piece BOM required');
  assert.ok(entries.every(([, n]) => n === 1));
  assert.equal(input.billOfMaterials[`${input.query.partId}:blue`], 1);
  const baseEntry = entries.find(([id]) => id.endsWith(':gray'));
  assert.ok(baseEntry, 'One gray base is required');
  const baseId = baseEntry[0].slice(0, -5);
  assert.ok(Object.hasOwn(CATALOG, baseId));
  assert.equal(input.candidates.length, 4);
  assert.equal(new Set(input.candidates.map(c => c.label)).size, 4);
  const hypotheses: Hypothesis[] = [];
  const candidateKeys = new Set<string>();
  for (const c of input.candidates) {
    assert.match(c.label, /^[A-D]$/);
    assert.ok([c.x, c.y, c.z, c.turn].every(Number.isInteger));
    assert.ok([c.x, c.y, c.z].every(v => v >= 0 && v <= 24));
    assert.ok(c.turn >= 0 && c.turn < 4);
    assert.equal(c.y, CATALOG[baseId].h, 'Only blue-on-gray supported stacks are covered');
    const query: Part = { id: 'query', partId: input.query.partId, color: 'blue',
      x: c.x, y: c.y, z: c.z, turn: c.turn };
    const poseKey = key(query);
    assert.ok(!candidateKeys.has(poseKey), 'Distinct candidate footprints required'); candidateKeys.add(poseKey);
    const q = dims(query);
    for (const turn of CATALOG[baseId].w === CATALOG[baseId].d ? [0] : [0, 1]) {
      // A grounded two-piece stack has base Y=0. Min-X/Z and contact bound the remaining positions.
      const xs = c.x > 0 ? [0] : Array.from({ length: Math.min(25, q.w) }, (_, i) => i);
      const zs = c.z > 0 ? [0] : Array.from({ length: Math.min(25, q.d) }, (_, i) => i);
      for (const x of xs) for (const z of zs) {
        const base: Part = { id: 'base', partId: baseId, color: 'gray', x, y: 0, z, turn };
        if (!validate([base, query]).length) hypotheses.push({ poseKey, label: c.label, parts: [base, query] });
      }
    }
  }
  assert.ok(hypotheses.length > 0 && hypotheses.length <= 512, 'Unsupported hypothesis count');
  return hypotheses.sort((a, b) => a.poseKey.localeCompare(b.poseKey)
    || key(a.parts[0]).localeCompare(key(b.parts[0])));
}

export function blueMask(bytes: Buffer): Mask {
  const png = PNG.sync.read(bytes);
  assert.equal(png.width, 640); assert.equal(png.height, 480);
  const pixels = new Uint8Array(png.width * png.height);
  let count = 0;
  // Remove title/footer. Chroma segmentation excludes grid numbers, neutral base and background.
  for (let y = 32; y < 448; y++) for (let x = 0; x < png.width; x++) {
    const i = y * png.width + x, o = i * 4;
    const [r, g, b, a] = png.data.subarray(o, o + 4);
    if (a > 127 && b > 80 && b > r * 1.25 && b > g * 1.1) { pixels[i] = 1; count++; }
  }
  return { width: png.width, height: png.height, pixels, count };
}

export function maskDistance(a: Mask, b: Mask) {
  assert.equal(a.width, b.width); assert.equal(a.height, b.height);
  assert.equal(a.pixels.length, b.pixels.length);
  let intersection = 0;
  for (let i = 0; i < a.pixels.length; i++) intersection += a.pixels[i] & b.pixels[i];
  const union = a.count + b.count - intersection;
  return union ? 1 - intersection / union : null;
}

export function selectVisualChoice(scores: { label: string; poseKey: string; distance: number }[]) {
  assert.ok(scores.every(s => Number.isFinite(s.distance) && s.distance >= 0 && s.distance <= 1));
  const best = new Map<string, typeof scores[number]>();
  for (const s of scores) {
    const previous = best.get(s.poseKey);
    if (previous) assert.equal(previous.label, s.label);
    if (!previous || s.distance < previous.distance) best.set(s.poseKey, s);
  }
  const ranking = [...best.values()].sort((a, b) => a.distance - b.distance || a.poseKey.localeCompare(b.poseKey));
  const margin = ranking.length > 1 ? ranking[1].distance - ranking[0].distance : null;
  const winner = ranking.length === 4 && margin !== null && margin > 1e-9 ? ranking[0] : null;
  return { answer: winner ? { choice: winner.label } : null, selectedKey: winner?.poseKey ?? null, margin, ranking };
}

export async function solveVisualChoice(input: ChoiceInput, reference: Partial<Record<typeof MATCH_VIEWS[number], Buffer>>,
  render: (frame: FrameSpec) => Promise<Buffer>) {
  const hypotheses = choiceHypotheses(input);
  const views = MATCH_VIEWS.filter(v => reference[v]);
  if (!views.length) return { ...selectVisualChoice([]), reason: 'no-image', hypotheses: hypotheses.length };
  const observed = new Map(views.map(v => [v, blueMask(reference[v]!)]));
  if ([...observed.values()].some(m => m.count === 0)) {
    return { ...selectVisualChoice([]), reason: 'query-mask-missing', hypotheses: hypotheses.length };
  }
  const scores = [];
  for (const h of hypotheses) {
    let distance = 0;
    for (const view of views) {
      const template = await render({ parts: h.parts, view, layer: null, title: `Ordinary assembled ${view}` });
      const d = maskDistance(observed.get(view)!, blueMask(template));
      assert.notEqual(d, null); distance += d!;
    }
    scores.push({ label: h.label, poseKey: h.poseKey, distance: distance / views.length });
  }
  const result = selectVisualChoice(scores);
  return { ...result, reason: result.answer ? 'selected' : 'ambiguous', hypotheses: hypotheses.length };
}
