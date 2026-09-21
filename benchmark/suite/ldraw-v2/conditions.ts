import type { Condition, PublicTask } from './types';

export const conditions: Condition[] = ['standard', 'text-without-image', 'graph-edges-withheld',
  'full-scene', 'background-mask', 'operand-only', 'choice-order', 'edge-order', 'id-permutation',
  'wrong-image', 'camera-perturbation', 'color-nuisance', 'multi-view', 'graph-intervention'];
export function eligible(task: PublicTask, condition: Condition) {
  if (['full-scene', 'background-mask', 'operand-only', 'text-without-image', 'wrong-image',
    'camera-perturbation', 'multi-view'].includes(condition)) return task.modality === 'visual';
  if (condition === 'color-nuisance') return task.family === 'shape-match';
  if (['graph-edges-withheld', 'edge-order', 'graph-intervention'].includes(condition)) return !!task.input.edges;
  if (condition === 'choice-order') return !!task.options;
  if (condition === 'id-permutation') return /B\d{4,}/.test(task.promptEn + JSON.stringify(task.options));
  return true;
}
export function operandLabels(task: PublicTask) {
  return [...new Set((task.promptEn + JSON.stringify(task.options ?? [])).match(/B\d{4,}/g) ?? [])].sort();
}
export function labelPermutation(value: unknown) {
  const labels = [...new Set(JSON.stringify(value).match(/B\d{4,}/g) ?? [])].sort();
  // Fresh labels guarantee an actual renaming even for one-operand color items.
  return Object.fromEntries(labels.map((label, i) => [label, `B${90001 + labels.length - i}`]));
}
export function replaceLabels<T>(value: T, mapping: Record<string, string>): T {
  return JSON.parse(JSON.stringify(value).replace(/B\d{4,}/g, label => mapping[label] ?? label));
}
export function alteredGraph(task: PublicTask): PublicTask {
  const t = structuredClone(task), target = operandLabels(t).find(l => t.promptEn.includes(l))!;
  if (t.family === 'neighbors') {
    const edge = t.input.edges.find((e: string[]) => e.includes(target));
    if (!edge) throw new Error('No incident edge for intervention');
    const neighbor = edge.find((label: string) => label !== target);
    t.input.edges = t.input.edges.filter((e: string[]) => !(e.includes(target) && e.includes(neighbor)));
  } else if (t.family === 'graph-removal') {
    const nodes: string[] = t.input.nodes.filter((n: string) => n !== target);
    const reached = new Set([nodes[0]]);
    for (let i = 0; i < nodes.length; i++) for (const [a, b] of t.input.edges) {
      if (a === target || b === target) continue;
      if (reached.has(a)) reached.add(b);
      if (reached.has(b)) reached.add(a);
    }
    const other = nodes.find(n => !reached.has(n));
    if (!other) throw new Error('No distinct components for intervention');
    t.input.edges.push([nodes[0], other]);
  } else throw new Error('Graph intervention is restricted to edge-based families');
  // Protocol labels these as hypothetical graphs. Keep all non-edge fields
  // unchanged so the paired request isolates the edge intervention.
  return t;
}
