import type { PublicTask, Part } from '../shared';
import { bounds, decode, dims, insertIssue, key, removeIssue } from '../geometry';
import { relationOracle } from './cases';

// This baseline accepts ONLY public input, never a CaseTask or evaluator target.
export function publicAlgorithm(task: PublicTask): unknown {
  const input = task.input;
  if (task.kind === 'relations') {
    const s = decode(input.structure);
    const a = s?.parts.find(p => p.id === input.a), b = s?.parts.find(p => p.id === input.b);
    return s && a && b ? relationOracle(s.parts, a, b) : null;
  }
  if (task.kind === 'plan') {
    const s = decode(input.target); if (!s) return null;
    const assemble = input.direction === 'assemble', order = [];
    let current: Part[] = assemble ? [] : structuredClone(s.parts);
    const remaining = new Set(s.parts.map(p => p.id));
    while (remaining.size) {
      const next = s.parts.find(p => remaining.has(p.id) && !(assemble ? insertIssue(current, p) : removeIssue(current, p.id)));
      if (!next) break;
      remaining.delete(next.id); order.push(next.id);
      current = assemble ? [...current, next] : current.filter(p => p.id !== next.id);
    }
    return { order };
  }
  if (task.kind === 'edit') {
    const s = decode(input.current); if (!s) return null;
    if (input.operation === 'quarter-turn-positive-X-to-positive-Z') {
      const box = bounds(s.parts);
      return { version: 1, parts: s.parts.map(p => ({ ...p, x: box.z - p.z - dims(p).d, z: p.x, turn: (p.turn + 1) % 4 })) };
    }
    const op = input.operation as { type: string; id?: string; from?: string; to?: Part['color'] };
    if (op.type === 'remove') return { version: 1, parts: s.parts.filter(p => p.id !== op.id) };
    if (op.type === 'recolor') return { version: 1, parts: s.parts.map(p => p.color === op.from ? { ...p, color: op.to! } : p) };
  }
  const reference = decode(input.reference);
  if (reference) {
    if (task.kind === 'repair') {
      const current = decode(input.current), remaining = [...reference.parts], faults = [];
      for (const p of current?.parts ?? []) {
        const i = remaining.findIndex(q => key(p) === key(q));
        if (i >= 0) remaining.splice(i, 1); else faults.push(p.id);
      }
      return { structure: reference, faultIds: faults };
    }
    return reference;
  }
  return null;
}
