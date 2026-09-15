import assert from 'node:assert/strict';
import { type Part } from '../shared';
import { dims } from '../geometry';
import { frontierModels } from '../frontier/models';
import { slabTiles } from '../frontier/tasks';
import { validate } from '../frontier/geometry';

export interface Scan {
  id: string; cost: number; axis: 'x' | 'z'; y: number; fixed: number; start: number; end: number;
}
export interface World { id: string; parts: Part[] }
export interface ObservationInput {
  worlds: World[]; queries: Scan[]; observed: Array<{ queryId: string; value: string }>; budget: number;
}
export interface ObservationCase {
  id: string; sourceGroup: string; tier: number; input: ObservationInput;
  referenceWorldId: string; slots: string[];
}
export type Policy = { hypothesisId: string } | { queryId: string; branches: Record<string, Policy> };

// A section scanner returns run lengths of individual brick interiors, not hidden assignment labels.
export function scan(parts: Part[], q: Scan): string {
  const labels: string[] = [];
  for (let t = q.start; t < q.end; t++) {
    const x = q.axis === 'x' ? t : q.fixed, z = q.axis === 'z' ? t : q.fixed;
    const p = parts.find(p => {
      const d = dims(p);
      return p.y === q.y && x >= p.x && x < p.x + d.w && z >= p.z && z < p.z + d.d;
    });
    labels.push(p?.id ?? '.');
  }
  const runs: string[] = [];
  for (let i = 0; i < labels.length;) {
    let j = i + 1;
    while (j < labels.length && labels[j] === labels[i]) j++;
    runs.push(`${labels[i] === '.' ? 'gap' : 'brick'}:${j - i}`); i = j;
  }
  return runs.join('|');
}
export function admissible(input: ObservationInput) {
  return input.worlds.filter(w => input.observed.every(o =>
    scan(w.parts, input.queries.find(q => q.id === o.queryId)!) === o.value));
}

export function optimalPolicy(input: ObservationInput, worlds = input.worlds): { cost: number; policy: Policy } {
  const memo = new Map<string, { cost: number; policy: Policy }>();
  const solve = (ws: World[]): { cost: number; policy: Policy } => {
    if (ws.length === 1) return { cost: 0, policy: { hypothesisId: ws[0].id } };
    const key = ws.map(w => w.id).sort().join(',');
    const old = memo.get(key); if (old) return old;
    let best: { cost: number; policy: Policy } = { cost: Infinity, policy: { hypothesisId: '?' } };
    for (const q of input.queries) {
      const groups = new Map<string, World[]>();
      for (const w of ws) {
        const v = scan(w.parts, q); groups.set(v, [...(groups.get(v) ?? []), w]);
      }
      if (groups.size < 2) continue;
      const children = [...groups].map(([v, group]) => [v, solve(group)] as const);
      const cost = q.cost + Math.max(...children.map(([, c]) => c.cost));
      if (cost < best.cost) best = { cost, policy: {
        queryId: q.id, branches: Object.fromEntries(children.map(([v, c]) => [v, c.policy])),
      } };
    }
    memo.set(key, best); return best;
  };
  return solve(worlds);
}

export function evaluatePolicy(input: ObservationInput, raw: unknown) {
  let solved = 0, worstCost = 0;
  const traces: Array<{ world: string; queries: string[]; cost: number; correct: boolean }> = [];
  for (const world of input.worlds) {
    let node: any = raw, cost = 0, valid = true;
    const seen = new Set<string>();
    while (node && typeof node === 'object' && !Array.isArray(node) && typeof node.queryId === 'string') {
      const q = input.queries.find(q => q.id === node.queryId);
      if (!q || seen.has(q.id) || !node.branches || typeof node.branches !== 'object'
        || Array.isArray(node.branches) || node.hypothesisId !== undefined) { valid = false; break; }
      seen.add(q.id); cost += q.cost;
      node = node.branches[scan(world.parts, q)];
    }
    const correct = valid && node && typeof node === 'object' && !Array.isArray(node)
      && node.queryId === undefined && node.hypothesisId === world.id && cost <= input.budget;
    if (correct) solved++;
    worstCost = Math.max(worstCost, cost);
    traces.push({ world: world.id, queries: [...seen], cost, correct: Boolean(correct) });
  }
  return { success: Number(solved === input.worlds.length), coverage: solved / input.worlds.length, worstCost, traces };
}

export class ScanEpisode {
  private spent = 0;
  private seen = new Set<string>();
  private finished = false;
  readonly events: unknown[] = [];
  constructor(private input: ObservationInput, private worldId: string) {
    assert.ok(input.worlds.some(w => w.id === worldId));
  }
  query(id: string) {
    assert.ok(!this.finished && !this.seen.has(id), 'finished_or_duplicate');
    const q = this.input.queries.find(q => q.id === id);
    assert.ok(q && this.spent + q.cost <= this.input.budget, 'unknown_or_budget');
    this.seen.add(id); this.spent += q.cost;
    const value = scan(this.input.worlds.find(w => w.id === this.worldId)!.parts, q);
    this.events.push({ queryId: id, value, cost: q.cost }); return { value, spent: this.spent };
  }
  submit(id: string) {
    assert.ok(!this.finished, 'finished'); this.finished = true;
    const result = { success: Number(id === this.worldId), spent: this.spent };
    this.events.push({ submitted: id, ...result }); return result;
  }
}

let cached: ObservationCase[] | undefined;
export function observationCases() {
  if (cached) return cached;
  cached = frontierModels().flatMap((model, mi) => [0, 1, 2].map(tier => {
    const n = 2 + tier, plates = model.structure.parts.filter(p => p.y === 0 && p.partId === '3035');
    const slots = Array.from({ length: n }, (_, k) => plates[(mi + k * (tier + 1)) % plates.length]);
    assert.equal(new Set(slots.map(p => p.id)).size, n);
    const selected = new Set(slots.map(p => p.id));
    const patterns = Array.from({ length: 2 ** n }, (_, k) => k)
      .filter(k => tier !== 1 || ((k & 1) === ((k >> 1) & 1)) || ((k >> 2) & 1) === mi % 2);
    const worlds: World[] = patterns.map((mask, i) => ({
      // Shared labels deliberately remain comparable, so constant-answer audits cannot pass merely by renaming.
      id: `h${i}`, parts: [...model.structure.parts.filter(p => !selected.has(p.id)),
        ...slots.flatMap((p, k) => slabTiles(p, ((mask >> k) & 1) ? 'crosswise' : 'lengthwise'))],
    }));
    for (const w of worlds) assert.deepEqual(validate(w.parts), []);
    const queries: Scan[] = slots.flatMap((p, k) => [
      { id: `q${2 * k}`, cost: 1 + ((mi + tier + k) % 4), axis: (mi + k) % 2 ? 'z' as const : 'x' as const,
        y: 0, fixed: (mi + k) % 2 ? p.x + 1 : p.z + 1, start: (mi + k) % 2 ? p.z : p.x,
        end: (mi + k) % 2 ? p.z + 4 : p.x + 8 },
      { id: `q${2 * k + 1}`, cost: 2 + ((mi * 2 + k) % 4), axis: 'x' as const,
        y: 0, fixed: p.z, start: p.x, end: p.x + 8 },
    ]);
    // A wide section may reveal multiple slots when aligned; unlike the legacy table, geometry determines its partition.
    const p = slots[mi % n];
    queries.push({ id: `q${queries.length}`, cost: 2 + tier, axis: 'x', y: 0,
      fixed: p.z + 1, start: 0, end: Math.max(...plates.map(p => p.x + 8)) });
    const world = worlds[(mi * 3 + tier * 5 + 1) % worlds.length];
    const q = queries[(mi + tier * 2) % queries.length];
    const input: ObservationInput = { worlds, queries, observed: [{ queryId: q.id, value: scan(world.parts, q) }], budget: 0 };
    input.budget = optimalPolicy(input).cost;
    assert.ok(Number.isFinite(input.budget));
    return { id: `f2-${model.id}-observation-${tier}`, sourceGroup: model.id, tier,
      input, referenceWorldId: world.id, slots: slots.map(p => p.id) };
  }));
  return cached;
}
