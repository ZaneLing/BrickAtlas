import type { Task, Action, ReplayFrame } from './types';

export function replay(task: Task, ids: unknown): { success: number; frames: ReplayFrame[]; issue: string | null } {
  const facts = new Set<string>(task.input.initialFacts ?? []);
  const active = new Set<string>(task.input.initialModules ?? []);
  const colors: Record<string, string> = {};
  let cost = 0, issue: string | null = null;
  const frames: ReplayFrame[] = [];
  const snapshot = (actionId: string | null, accepted: boolean) => frames.push({
    step: frames.length, actionId, accepted, issue, facts: [...facts].sort(),
    activeModules: [...active].sort(), colors: { ...colors }, cost,
  });
  snapshot(null, true);
  if (!Array.isArray(ids) || ids.some(id => typeof id !== 'string'))
    return { success: 0, frames, issue: 'actionIds must be a string array' };
  const catalog = new Map<string, Action>((task.input.actions ?? []).map((a: Action) => [a.id, a]));
  for (const id of ids) {
    const a = catalog.get(id);
    issue = !a ? `unknown action ${id}` : a.requires.some(f => !facts.has(f)) ? `precondition ${id}`
      : a.forbids?.some(f => facts.has(f)) ? `forbidden state ${id}`
        : cost + a.cost > task.input.budget ? 'budget exceeded' : null;
    if (issue || !a) { snapshot(id, false); break; }
    a.deletes.forEach(f => facts.delete(f)); a.adds.forEach(f => facts.add(f)); cost += a.cost;
    if (a.visual) {
      if (a.visual.visible === false) active.delete(a.visual.moduleId);
      if (a.visual.visible === true) active.add(a.visual.moduleId);
      if (a.visual.color) colors[a.visual.moduleId] = a.visual.color;
    }
    snapshot(id, true);
  }
  const success = !issue && task.input.goalFacts.every((f: string) => facts.has(f))
    && (task.input.absentFacts ?? []).every((f: string) => !facts.has(f));
  return { success: Number(success), frames, issue: issue ?? (success ? null : 'goal not reached') };
}

export function score(task: Task, raw: unknown) {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return { success: 0, validFormat: 0 };
  const a = raw as Record<string, any>;
  if (task.format === 'actions') {
    const r = replay(task, a.actionIds);
    return { success: r.success, validFormat: Number(Array.isArray(a.actionIds)), issue: r.issue };
  }
  if (task.format === 'schedule') {
    const jobs = task.input.jobs as Array<{ id: string; duration: number; resource: string; after: string[] }>;
    const starts = a.starts;
    if (!starts || typeof starts !== 'object' || Array.isArray(starts)
      || Object.keys(starts).length !== jobs.length
      || jobs.some(j => !Number.isInteger(starts[j.id]) || starts[j.id] < 0)) return { success: 0, validFormat: 0 };
    const end = (id: string) => starts[id] + jobs.find(j => j.id === id)!.duration;
    const dependencies = jobs.every(j => j.after.every(id => starts[j.id] >= end(id)));
    const resources = jobs.every((j, i) => jobs.slice(i + 1).every(k => j.resource !== k.resource
      || end(j.id) <= starts[k.id] || end(k.id) <= starts[j.id]));
    return { success: Number(dependencies && resources && Math.max(...jobs.map(j => end(j.id))) <= task.input.deadline),
      validFormat: 1 };
  }
  if (task.format === 'policy') {
    const query = task.input.queries.find((q: any) => q.id === a.queryId);
    if (!query || !a.decisions || typeof a.decisions !== 'object') return { success: 0, validFormat: 0 };
    const success = query.cost <= task.input.budget && task.input.worlds.every((world: any) =>
      a.decisions[query.returns[world.id]] === world.action);
    return { success: Number(success), validFormat: 1 };
  }
  if (task.format === 'single-choice') return {
    success: Number(a.choiceId === task.answer.choiceId),
    validFormat: Number(typeof a.choiceId === 'string' && !!task.options?.some(o => o.id === a.choiceId)),
  };
  const values = a.choiceIds;
  const valid = Array.isArray(values) && values.every(v => typeof v === 'string' && task.options?.some(o => o.id === v))
    && new Set(values).size === values.length;
  return { success: Number(valid && JSON.stringify([...values].sort()) === JSON.stringify([...task.answer.choiceIds].sort())),
    validFormat: Number(valid) };
}

// Kahn-like public-precondition solver; no reference answer is read.
export function solveActions(task: Task) {
  let facts = new Set<string>(task.input.initialFacts);
  const relevant = new Set<string>(task.input.goalFacts);
  const catalog = task.input.actions as Action[];
  for (let n = 0; n < catalog.length; n++) for (const a of catalog)
    if (a.adds.some(f => relevant.has(f))) a.requires.forEach(f => relevant.add(f));
  const ids: string[] = [], remaining = catalog.filter(a => a.adds.some(f => relevant.has(f))
    && !a.adds.some(f => (task.input.absentFacts ?? []).includes(f)));
  for (let n = 0; n < task.input.actions.length; n++) {
    if (task.input.goalFacts.every((f: string) => facts.has(f))) break;
    const a = remaining.find(a => a.requires.every(f => facts.has(f))
      && !(a.forbids ?? []).some(f => facts.has(f)));
    if (!a) break;
    ids.push(a.id); remaining.splice(remaining.indexOf(a), 1);
    a.deletes.forEach(f => facts.delete(f)); a.adds.forEach(f => facts.add(f));
  }
  return { actionIds: ids };
}
