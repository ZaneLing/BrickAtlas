import { dims, footprint, key } from '../geometry';
import { type Part } from '../shared';
import { type publicTask } from './tasks';

type Public = ReturnType<typeof publicTask>;

// The solver receives only exported public fields, not FrontierTask.oracle or model modules.
export function publicSolver(task: Public): unknown {
  const i = task.input;
  if (task.kind === 'service-plan' || task.kind === 'access-certificate') {
    const parts: Part[] = i.current?.parts ?? i.structure.parts;
    const selected = new Set<string>(i.serviceIds);
    for (const p of [...parts].sort((a, b) => a.y - b.y)) {
      if (parts.some(q => selected.has(q.id) && p.y >= q.y + dims(q).h && footprint(p, q))) selected.add(p.id);
    }
    const ids = parts.filter(p => selected.has(p.id)).sort((a, b) => b.y - a.y).map(p => p.id);
    return task.kind === 'access-certificate' ? { removeIds: ids, order: ids }
      : { actions: [...ids.map(id => ({ op: 'remove', id })), ...[...ids].reverse().map(id => ({ op: 'place', id }))] };
  }
  if (task.kind === 'distributed-repair') {
    const replacements = i.reference.parts.filter((p: Part) => key(p) !== key(i.current.parts.find((q: Part) => q.id === p.id)));
    return { faultIds: replacements.map((p: Part) => p.id), replacements };
  }
  if (task.kind === 'ambiguity-set') return { possibleIds: i.hypotheses.filter((h: any) =>
    Object.entries(i.observations).every(([id, v]) => h.layouts[id] === v)).map((h: any) => h.id) };
  if (task.kind === 'parallel-schedule') {
    const remaining = new Map<string, Part>(i.structure.parts.map((p: Part) => [p.id, p])), batches: string[][] = [];
    while (remaining.size) {
      const batch = [...remaining.values()].filter(p => ![...remaining.values()].some(q =>
        q.id !== p.id && q.y + dims(q).h <= p.y && footprint(p, q))).slice(0, i.workers).map(p => p.id);
      if (!batch.length) throw new Error('cycle');
      batches.push(batch); batch.forEach(id => remaining.delete(id));
    }
    return { batches };
  }
  if (task.kind === 'minimal-intervention') {
    const ids: string[] = i.allowedIds;
    for (let count = 0; count <= ids.length; count++) for (let mask = 0; mask < 2 ** ids.length; mask++) {
      const forced = ids.filter((_, k) => mask & (1 << k));
      if (forced.length !== count) continue;
      const gone = new Set(forced);
      for (const p of [...i.structure.parts].sort((a, b) => a.y - b.y))
        if (p.y && !i.structure.parts.some((q: Part) => !gone.has(q.id) && q.y + dims(q).h === p.y && footprint(p, q))) gone.add(p.id);
      if (gone.has(i.goalId)) return { removeIds: forced, cascadeIds: [...gone] };
    }
    return { removeIds: [], cascadeIds: [] };
  }
  if (task.kind === 'inventory-cover') {
    const areas = Object.entries(i.stock).flatMap(([partId, n]) => Array(Number(n)).fill(dims({ partId, turn: 0 })).map(d => d.w * d.d)).sort((a, b) => b - a);
    let capacity = 0, minimum = 0;
    while (capacity < i.region.w * i.region.d) capacity += areas[minimum++];
    const occupied = new Set<string>(), used: Record<string, number> = {};
    const search = (tiles: any[]): any[] | null => {
      if (occupied.size === i.region.w * i.region.d) return tiles;
      if (tiles.length >= minimum) return null;
      let x = 0, z = 0;
      outer: for (z = 0; z < i.region.d; z++) for (x = 0; x < i.region.w; x++) if (!occupied.has(`${x},${z}`)) break outer;
      for (const partId of Object.keys(i.stock)) for (const turn of [0, 1]) {
        if ((used[partId] ?? 0) >= i.stock[partId]) continue;
        const d = dims({ partId, turn });
        if (x + d.w > i.region.w || z + d.d > i.region.d) continue;
        const cells = Array.from({ length: d.w }, (_, dx) => Array.from({ length: d.d }, (_, dz) => `${x + dx},${z + dz}`)).flat();
        if (cells.some(c => occupied.has(c))) continue;
        cells.forEach(c => occupied.add(c)); used[partId] = (used[partId] ?? 0) + 1;
        const result = search([...tiles, { partId, turn, x, z }]);
        cells.forEach(c => occupied.delete(c)); used[partId]--;
        if (result) return result;
      }
      return null;
    };
    return { tiles: search([]) ?? [] };
  }
  if (task.kind === 'inspection-policy') {
    const solve = (worlds: string[], used: string[]): { cost: number; node: any } => {
      if (worlds.length === 1) return { cost: 0, node: { hypothesisId: worlds[0] } };
      let best = { cost: Infinity, node: {} as any };
      for (const q of i.queries.filter((q: any) => !used.includes(q.id))) {
        const groups: Record<string, string[]> = {};
        for (const h of worlds) (groups[q.returns[h]] ??= []).push(h);
        if (Object.keys(groups).length < 2) continue;
        const branches = Object.fromEntries(Object.entries(groups).map(([v, hs]) => [v, solve(hs, [...used, q.id])]));
        const cost = q.cost + Math.max(...Object.values(branches).map(b => b.cost));
        if (cost < best.cost) best = { cost, node: { queryId: q.id,
          branches: Object.fromEntries(Object.entries(branches).map(([v, b]) => [v, b.node])) } };
      }
      return best;
    };
    return solve(i.hypotheses, []).node;
  }
}

export function shortcut(task: Public): unknown {
  const i = task.input;
  switch (task.kind) {
    case 'service-plan': return { actions: i.target.parts.filter((p: Part) =>
      key(p) !== key(i.current.parts.find((q: Part) => q.id === p.id))).map((p: Part) => ({ op: 'place', id: p.id })) };
    case 'access-certificate': return { removeIds: i.serviceIds, order: i.serviceIds };
    case 'parallel-schedule': return { batches: [...i.structure.parts].sort((a, b) => a.y - b.y).map(p => [p.id]) };
    case 'minimal-intervention': return { removeIds: [i.allowedIds[0]], cascadeIds: [i.allowedIds[0]] };
    case 'inventory-cover': return { tiles: [0, 4].flatMap(x => [0, 2].map(z => ({ partId: '3020', x, z, turn: 0 }))) };
    case 'ambiguity-set': return { possibleIds: [i.hypotheses[0].id] };
    case 'inspection-policy': return { hypothesisId: i.hypotheses[0] };
    case 'distributed-repair': return { faultIds: [], replacements: [] };
  }
}
