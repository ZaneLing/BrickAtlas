import { CATALOG, type Part } from '../shared';

// Deliberately does not import the benchmark's geometry/score implementation.
export function independentCheck(parts: Part[]) {
  const occupied = new Map<string, string>(), issues = new Set<string>(), ids = new Set<string>();
  const joins = new Map<string, number>();
  const cell = (x: number, y: number, z: number) => `${x},${y},${z}`;
  for (const p of parts) {
    const c = CATALOG[p.partId];
    if (!c || ids.has(p.id) || ![0, 1, 2, 3].includes(p.turn)
      || ![p.x, p.y, p.z].every(n => Number.isInteger(n) && n >= 0 && n <= 24)) {
      issues.add('schema'); continue;
    }
    ids.add(p.id);
    const w = p.turn % 2 ? c.d : c.w, d = p.turn % 2 ? c.w : c.d;
    if (p.x + w > 32 || p.y + c.h > 32 || p.z + d > 32) issues.add('bounds');
    let supported = p.y === 0;
    for (let x = p.x; x < p.x + w; x++) for (let z = p.z; z < p.z + d; z++) {
      const lower = occupied.get(cell(x, p.y - 1, z));
      if (lower) {
        supported = true;
        const key = [lower, p.id].sort().join('|');
        joins.set(key, (joins.get(key) ?? 0) + 1);
      }
      for (let y = p.y; y < p.y + c.h; y++) if (occupied.has(cell(x, y, z))) issues.add('collision');
      for (let y = p.y + c.h; y <= 32; y++) if (occupied.has(cell(x, y, z))) issues.add('blocked_insertion');
    }
    if (!supported) issues.add('unsupported_prefix');
    for (let x = p.x; x < p.x + w; x++) for (let z = p.z; z < p.z + d; z++)
      for (let y = p.y; y < p.y + c.h; y++) occupied.set(cell(x, y, z), p.id);
  }
  return { issues: [...issues], cells: occupied.size,
    contacts: [...joins.entries()].map(([pair, studs]) => ({ pair, studs })) };
}
