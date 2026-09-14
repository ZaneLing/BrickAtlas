import { dims } from '../geometry';
import { type Part } from '../shared';
import { accessClosure, cascade, dependencies, exact, insertion, LIMITS, parseStructure, removal } from './geometry';
import { type FrontierTask, sameSet, subsets } from './tasks';

export interface Result { success: number; metrics: Record<string, number | null>; issues: string[]; finalParts?: Part[] }
const object = (x: any) => x && typeof x === 'object' && !Array.isArray(x);
const strings = (x: any): x is string[] => Array.isArray(x) && x.every(v => typeof v === 'string') && new Set(x).size === x.length;
export function evaluateFrontier(task: FrontierTask, answer: any): Result {
  const metrics: Result['metrics'] = {}, issues: string[] = [];
  const fail = (reason: string): Result => ({ success: 0, metrics, issues: [...issues, reason] });
  if (!object(answer)) return fail('format');
  const input = task.input;
  switch (task.kind) {
    case 'service-plan': {
      if (!Array.isArray(answer.actions) || answer.actions.length > LIMITS.actions) return fail('action_schema');
      let current: Part[] = structuredClone(input.current.parts);
      let done = 0;
      for (const a of answer.actions) {
        if (!object(a) || typeof a.id !== 'string' || !['remove', 'place'].includes(a.op)) return fail('action_schema');
        const p: Part | undefined = input.target.parts.find((p: Part) => p.id === a.id);
        const issue = a.op === 'remove' ? removal(current, a.id) : p ? insertion(current, p) : 'unknown';
        if (issue) {
          metrics.legalPrefix = done / Math.max(1, answer.actions.length);
          return { ...fail(issue), finalParts: current };
        }
        current = a.op === 'remove' ? current.filter(p => p.id !== a.id) : [...current, { ...p! }];
        done++;
      }
      const lowerBound = 2 * accessClosure(input.current.parts, input.serviceIds).length;
      metrics.actions = answer.actions.length; metrics.lowerBound = lowerBound;
      metrics.finalExact = Number(exact(input.target.parts, current));
      metrics.legalPrefix = 1; metrics.excessActions = Math.max(0, answer.actions.length - lowerBound);
      if (!metrics.finalExact) issues.push('target');
      if (answer.actions.length > input.maxActions) issues.push('budget');
      return { success: Number(!issues.length), metrics, issues, finalParts: current };
    }
    case 'access-certificate': {
      const required = accessClosure(input.structure.parts, input.serviceIds).map(p => p.id);
      if (!sameSet(answer.removeIds, required) || !sameSet(answer.order, required)) return fail('minimum_set');
      let current: Part[] = [...input.structure.parts];
      for (const id of answer.order) {
        const issue = removal(current, id);
        if (issue) return fail(issue);
        current = current.filter(p => p.id !== id);
      }
      metrics.removals = required.length;
      return { success: 1, metrics, issues, finalParts: current };
    }
    case 'parallel-schedule': {
      if (!Array.isArray(answer.batches) || answer.batches.length > LIMITS.parts
        || !answer.batches.every((b: any) => strings(b) && b.length > 0 && b.length <= input.workers)) return fail('batch_schema');
      const parts: Part[] = input.structure.parts, deps = dependencies(parts), done = new Set<string>();
      for (const batch of answer.batches) {
        if (batch.some((id: string) => !Object.hasOwn(deps, id) || done.has(id) || !deps[id].every(p => done.has(p)))) return fail('precedence');
        batch.forEach((id: string) => done.add(id));
      }
      metrics.coverage = done.size / parts.length; metrics.makespan = answer.batches.length;
      metrics.workerLowerBound = Math.ceil(parts.length / input.workers);
      if (done.size !== parts.length) return fail('incomplete');
      return { success: 1, metrics, issues };
    }
    case 'minimal-intervention': {
      if (!strings(answer.removeIds) || !answer.removeIds.every((id: string) => input.allowedIds.includes(id))) return fail('allowed_set');
      const propagated = cascade(input.structure.parts, answer.removeIds);
      const optimum = Math.min(...subsets<string>(input.allowedIds).filter(ids => cascade(input.structure.parts, ids).includes(input.goalId)).map(ids => ids.length));
      metrics.removals = answer.removeIds.length; metrics.optimum = optimum;
      if (!propagated.includes(input.goalId)) return fail('goal_survives');
      if (!sameSet(answer.cascadeIds, propagated)) return fail('cascade_set');
      if (answer.removeIds.length !== optimum) return fail('nonminimal');
      return { success: 1, metrics, issues, finalParts: input.structure.parts.filter((p: Part) => !propagated.includes(p.id)) };
    }
    case 'inventory-cover': {
      if (!Array.isArray(answer.tiles) || answer.tiles.length > input.maxTiles) return fail('tile_schema');
      const covered = new Set<string>(), used: Record<string, number> = {};
      for (const t of answer.tiles) {
        if (!object(t) || typeof t.partId !== 'string' || !Object.hasOwn(input.stock, t.partId)
          || ![0, 1, 2, 3].includes(t.turn) || ![t.x, t.z].every(Number.isInteger)) return fail('tile_schema');
        const d = dims(t);
        if (t.x < 0 || t.z < 0 || t.x + d.w > input.region.w || t.z + d.d > input.region.d) return fail('tile_bounds');
        used[t.partId] = (used[t.partId] ?? 0) + 1;
        if (used[t.partId] > input.stock[t.partId]) return fail('stock');
        for (let x = t.x; x < t.x + d.w; x++) for (let z = t.z; z < t.z + d.d; z++) {
          const key = `${x},${z}`;
          if (covered.has(key)) return fail('overlap'); covered.add(key);
        }
      }
      const area = input.region.w * input.region.d;
      const areas = Object.entries(input.stock).flatMap(([partId, count]) => {
        const d = dims({ partId, turn: 0 }); return Array(Number(count)).fill(d.w * d.d) as number[];
      }).sort((a, b) => b - a);
      let capacity = 0, lowerBound = 0;
      while (capacity < area && lowerBound < areas.length) capacity += areas[lowerBound++];
      metrics.coverage = covered.size / area; metrics.tiles = answer.tiles.length; metrics.lowerBound = lowerBound;
      if (covered.size !== area) return fail('uncovered');
      if (answer.tiles.length !== lowerBound) return fail('nonminimal');
      const original: Part = input.structure.parts.find((p: Part) => p.id === input.replaceId);
      const replacements: Part[] = answer.tiles.map((t: any, i: number) => ({
        id: `replacement-${i}`, color: original.color, partId: t.partId, turn: t.turn,
        x: original.x + (original.turn % 2 ? t.z : t.x), y: original.y,
        z: original.z + (original.turn % 2 ? t.x : t.z),
      }));
      return { success: 1, metrics, issues,
        finalParts: [...input.structure.parts.filter((p: Part) => p.id !== original.id), ...replacements] };
    }
    case 'ambiguity-set': {
      const hs = input.hypotheses.filter((h: any) => Object.entries(input.observations).every(([id, layout]) => h.layouts[id] === layout));
      metrics.admissible = hs.length;
      metrics.falseCertainty = Number(Array.isArray(answer.possibleIds) && answer.possibleIds.length === 1 && hs.length > 1);
      if (!sameSet(answer.possibleIds, hs.map((h: any) => h.id))) return fail('admissible_set');
      return { success: 1, metrics, issues };
    }
    case 'inspection-policy': {
      let solved = 0, worst = 0;
      for (const h of input.hypotheses as string[]) {
        let node = answer, cost = 0; const seen = new Set<string>();
        while (object(node) && typeof node.queryId === 'string') {
          const q = input.queries.find((q: any) => q.id === node.queryId);
          if (!q || seen.has(q.id) || seen.size >= input.queries.length || !object(node.branches)) break;
          seen.add(q.id); cost += q.cost;
          node = node.branches[q.returns[h]];
        }
        worst = Math.max(worst, cost);
        if (object(node) && node.hypothesisId === h && node.queryId === undefined && cost <= input.budget) solved++;
      }
      metrics.worldCoverage = solved / input.hypotheses.length; metrics.worstCost = worst;
      if (solved !== input.hypotheses.length) return fail('policy_coverage_or_budget');
      return { success: 1, metrics, issues };
    }
    case 'distributed-repair': {
      const current: Part[] = input.current.parts, target: Part[] = input.reference.parts;
      const wrong = current.filter(p => {
        const q = target.find(t => t.id === p.id)!;
        return ['partId', 'color', 'x', 'y', 'z', 'turn'].some(k => p[k as keyof Part] !== q[k as keyof Part]);
      }).map(p => p.id);
      if (!sameSet(answer.faultIds, wrong) || !Array.isArray(answer.replacements)) return fail('fault_set');
      const patches = parseStructure({ version: 1, parts: answer.replacements });
      if (!patches || !sameSet(patches.parts.map(p => p.id), wrong)) return fail('patch_schema');
      const final = current.map(p => patches.parts.find(q => q.id === p.id) ?? p);
      metrics.finalExact = Number(exact(target, final)); metrics.changedRecall = metrics.finalExact;
      if (!metrics.finalExact) return fail('patch_target');
      return { success: 1, metrics, issues, finalParts: final };
    }
  }
}

export function renderNegative(task: FrontierTask): Part[] {
  if (task.kind === 'minimal-intervention') return task.input.structure.parts;
  if (task.kind === 'inventory-cover') {
    const p: Part = task.input.structure.parts.find((p: Part) => p.id === task.input.replaceId);
    return task.input.structure.parts.filter((q: Part) => q.id !== p.id);
  }
  return task.input.current?.parts ?? task.input.structure?.parts ?? [];
}
