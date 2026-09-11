import { CATALOG, COLORS } from '../shared/catalog';
import type { Blueprint, Brick, InventoryItem, Score } from '../shared/types';

export function size(part: Pick<Brick, 'partId' | 'turn'>) {
  const item = CATALOG[part.partId as keyof typeof CATALOG];
  if (!item) throw new Error('Unknown part');
  return {
    w: part.turn % 2 ? item.depth : item.width,
    d: part.turn % 2 ? item.width : item.depth,
    h: item.height,
  };
}

export function validBrick(value: unknown): value is Brick {
  if (!value || typeof value !== 'object') return false;
  const b = value as Brick;
  return typeof b.id === 'string' && /^[\w-]{1,64}$/.test(b.id)
    && Object.hasOwn(CATALOG, b.partId) && Object.hasOwn(COLORS, b.color)
    && [0, 1, 2, 3].includes(b.turn)
    && [b.x, b.z].every(n => Number.isInteger(n) && n >= -8 && n <= 16)
    && Number.isInteger(b.y) && b.y >= 0 && b.y <= 16;
}

export function overlapsXZ(a: Brick, b: Brick) {
  const x = size(a), y = size(b);
  return a.x < b.x + y.w && a.x + x.w > b.x && a.z < b.z + y.d && a.z + x.d > b.z;
}

export function connected(a: Brick, b: Brick) {
  return overlapsXZ(a, b) && (a.y + size(a).h === b.y || b.y + size(b).h === a.y);
}

export function validateWorld(parts: Brick[]): string | null {
  if (parts.length > 32 || !parts.every(validBrick)) return 'invalid_part';
  if (new Set(parts.map(p => p.id)).size !== parts.length) return 'duplicate_id';
  for (const part of parts) {
    if (parts.some(other => other !== part && overlapsXZ(part, other)
      && part.y < other.y + size(other).h && part.y + size(part).h > other.y)) return 'overlap';
    if (part.y > 0 && !parts.some(other => other !== part
      && other.y + size(other).h === part.y && overlapsXZ(part, other))) return 'unsupported';
  }
  return null;
}

export function edges(parts: Brick[]) {
  const result: [string, string][] = [];
  parts.forEach((a, index) => {
    for (const b of parts.slice(index + 1)) if (connected(a, b)) {
      result.push([a.id, b.id].sort() as [string, string]);
    }
  });
  return result;
}

export function components(parts: Brick[]) {
  const unvisited = new Set(parts.map(p => p.id));
  let count = 0;
  for (const p of parts) {
    if (!unvisited.delete(p.id)) continue;
    count++;
    const stack = [p];
    while (stack.length) {
      const a = stack.pop()!;
      for (const b of parts) if (unvisited.has(b.id) && connected(a, b)) {
        unvisited.delete(b.id);
        stack.push(b);
      }
    }
  }
  return count;
}

export function removalIssue(parts: Brick[], id: string) {
  const part = parts.find(p => p.id === id);
  if (!part) return 'unknown_id';
  if (parts.some(other => other.id !== id && overlapsXZ(part, other)
    && other.y >= part.y + size(part).h)) return 'blocked_above';
  return validateWorld(parts.filter(p => p.id !== id));
}

export function bom(parts: Brick[]): InventoryItem[] {
  const items = new Map<string, InventoryItem>();
  for (const p of parts) {
    const key = `${p.partId}:${p.color}`;
    const item = items.get(key) ?? { partId: p.partId, color: p.color, count: 0 };
    item.count++;
    items.set(key, item);
  }
  return [...items.values()].sort((a, b) =>
    a.partId.localeCompare(b.partId) || a.color.localeCompare(b.color));
}

export function canonical(part: Brick) {
  const s = size(part);
  return [part.partId, part.color, part.x, part.y, part.z, s.w, s.d].join(':');
}

export function scoreWorld(expected: Brick[], actual: Brick[]): Score {
  const valid = validateWorld(actual) === null;
  const malformed = actual.some(part => !validBrick(part));
  if (malformed) return {
    exact: false, partF1: 0, edgeF1: 0, matched: 0, expected: expected.length,
    extra: actual.length, missing: expected.length, valid: false,
  };
  // Exact grid poses define equivalence classes, so multiset matching is optimal.
  const pools = new Map<string, string[]>();
  expected.forEach(p => pools.set(canonical(p), [...(pools.get(canonical(p)) ?? []), p.id]));
  const mapping = new Map<string, string>();
  const seenActual = new Set<string>();
  let matched = 0;
  for (const part of actual) {
    if (seenActual.has(part.id)) continue;
    seenActual.add(part.id);
    const id = pools.get(canonical(part))?.pop();
    if (id) { mapping.set(part.id, id); matched++; }
  }
  const expectedEdges = new Set(edges(expected).map(e => JSON.stringify(e)));
  const actualEdges = edges(actual);
  const correctEdges = new Set(actualEdges.flatMap(([a, b]) => {
    if (!mapping.has(a) || !mapping.has(b)) return [];
    const key = JSON.stringify([mapping.get(a)!, mapping.get(b)!].sort());
    return expectedEdges.has(key) ? [key] : [];
  })).size;
  const f1 = (correct: number, a: number, b: number) => a + b ? 2 * correct / (a + b) : 1;
  return {
    exact: valid && matched === expected.length && actual.length === expected.length,
    partF1: f1(matched, expected.length, actual.length),
    edgeF1: f1(correctEdges, expectedEdges.size, actualEdges.length),
    matched, expected: expected.length, extra: actual.length - matched,
    missing: expected.length - matched, valid,
  };
}

export function parseBlueprint(value: unknown): Blueprint | null {
  if (!value || typeof value !== 'object') return null;
  const b = value as Blueprint;
  if (b.version !== 1 || !Array.isArray(b.parts) || !b.parts.length
    || b.parts.length > 32 || !b.parts.every(validBrick)
    || new Set(b.parts.map(p => p.id)).size !== b.parts.length) return null;
  return { version: 1, parts: b.parts.map(p => ({
    id: p.id, partId: p.partId, color: p.color, x: p.x, y: p.y, z: p.z, turn: p.turn,
  })) };
}

export function compileBlueprint(blueprint: Blueprint, inventory: InventoryItem[]) {
  const placed: Brick[] = [];
  const available = structuredClone(inventory);
  for (const p of blueprint.parts) {
    const item = available.find(i => i.partId === p.partId && i.color === p.color);
    const issue = validateWorld([...placed, p]);
    if (!item?.count || issue) return { ok: false, placed, issue: issue ?? 'no_inventory' };
    item.count--;
    placed.push(p);
  }
  return { ok: true, placed, issue: null };
}
