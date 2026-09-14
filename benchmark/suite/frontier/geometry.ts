import { CATALOG, COLORS, type Part, type Structure } from '../shared';
import { dims, footprint, key } from '../geometry';

export const FRONTIER_VERSION = 'brickatlas-frontier-1';
export const LIMITS = { parts: 512, coordinate: 95, extent: 96, actions: 2048 };
export const RULES = `Frontier grid: integer X/Z studs and Y plate heights; origins 0..95,
bodies inside [0,96]^3, at most 512 parts, same 25 rectangular part types and six colors.
Quarter-turn yaw 0..3; odd yaw swaps width/depth. No collision; each elevated part
needs a direct supporting stud. Only vertical removal/insertion; any overhead
footprint overlap blocks passage. This is nominal geometry, not force or robot physics.
IDs identify tracked instances in actions; geometry answers accept symmetric yaw.
Return one JSON object. All task budgets and information privileges are explicit.`;

export function parseStructure(raw: unknown): Structure | null {
  if (!raw || typeof raw !== 'object') return null;
  const s = raw as Structure;
  if (s.version !== 1 || !Array.isArray(s.parts) || s.parts.length > LIMITS.parts) return null;
  if (!s.parts.every(p => p && typeof p === 'object'
    && typeof p.id === 'string' && /^[\w-]{1,60}$/.test(p.id)
    && typeof p.partId === 'string' && Object.hasOwn(CATALOG, p.partId)
    && typeof p.color === 'string' && Object.hasOwn(COLORS, p.color)
    && [0, 1, 2, 3].includes(p.turn)
    && [p.x, p.y, p.z].every(v => Number.isInteger(v) && v >= 0 && v <= LIMITS.coordinate))) return null;
  if (new Set(s.parts.map(p => p.id)).size !== s.parts.length) return null;
  return { version: 1, parts: s.parts.map(p => ({ ...p })) };
}

export function validate(parts: Part[]): string[] {
  if (!parseStructure({ version: 1, parts })) return ['schema'];
  const issues = new Set<string>();
  if (!parts.length) issues.add('empty');
  for (const p of parts) {
    const d = dims(p);
    if (p.x + d.w > LIMITS.extent || p.y + d.h > LIMITS.extent || p.z + d.d > LIMITS.extent) issues.add('bounds');
    if (parts.some(q => q !== p && footprint(p, q) > 0
      && p.y < q.y + dims(q).h && q.y < p.y + d.h)) issues.add('collision');
    if (p.y > 0 && !parts.some(q => q !== p && q.y + dims(q).h === p.y && footprint(p, q) > 0)) issues.add('support');
  }
  return [...issues];
}

export function insertion(parts: Part[], p: Part) {
  if (parts.some(q => q.id === p.id)) return 'duplicate';
  return validate([...parts, p])[0]
    ?? (parts.some(q => q.y >= p.y + dims(p).h && footprint(p, q) > 0) ? 'blocked' : null);
}

export function removal(parts: Part[], id: string) {
  const p = parts.find(q => q.id === id);
  if (!p) return 'unknown';
  if (parts.some(q => q.id !== id && q.y >= p.y + dims(p).h && footprint(p, q) > 0)) return 'blocked';
  const rest = parts.filter(q => q.id !== id);
  return rest.length ? validate(rest)[0] ?? null : null;
}

export function exact(a: Part[], b: Part[]) {
  const tokens = (ps: Part[]) => ps.map(p => key(p)).sort().join('|');
  return tokens(a) === tokens(b) && validate(b).length === 0;
}

// Every overhead overlap must be removed, recursively, under the vertical-only contract.
export function accessClosure(parts: Part[], ids: string[]) {
  const selected = new Set(ids);
  let changed = true;
  while (changed) {
    changed = false;
    for (const p of parts.filter(q => selected.has(q.id))) {
      for (const q of parts) if (!selected.has(q.id) && q.y >= p.y + dims(p).h && footprint(p, q)) {
        selected.add(q.id); changed = true;
      }
    }
  }
  return parts.filter(p => selected.has(p.id)).sort((a, b) => b.y - a.y || a.id.localeCompare(b.id));
}

export function cascade(parts: Part[], forced: string[]) {
  const gone = new Set(forced);
  let changed = true;
  while (changed) {
    changed = false;
    for (const p of parts) if (!gone.has(p.id) && p.y > 0
      && !parts.some(q => !gone.has(q.id) && q.y + dims(q).h === p.y && footprint(p, q))) {
      gone.add(p.id); changed = true;
    }
  }
  return [...gone].sort();
}

export function dependencies(parts: Part[]) {
  return Object.fromEntries(parts.map(p => [p.id, parts.filter(q =>
    q.id !== p.id && q.y + dims(q).h <= p.y && footprint(p, q) > 0).map(q => q.id)]));
}

export function schedule(parts: Part[], workers: number) {
  const deps = dependencies(parts), done = new Set<string>(), batches: string[][] = [];
  while (done.size < parts.length) {
    const batch = parts.filter(p => !done.has(p.id) && deps[p.id].every(id => done.has(id)))
      .sort((a, b) => a.y - b.y || a.id.localeCompare(b.id)).slice(0, workers).map(p => p.id);
    if (!batch.length) throw new Error('dependency_cycle');
    batches.push(batch); batch.forEach(id => done.add(id));
  }
  return batches;
}
