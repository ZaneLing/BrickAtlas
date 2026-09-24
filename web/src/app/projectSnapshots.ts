import { readLocal, writeLocal } from './storage';

export interface ProjectSnapshot {
  id: string;
  name: string;
  savedAt: number;
  data: string;
}
export const snapshotKey = (space: 'diy' | 'compose') => `brick-atlas-${space}-snapshots-v1`;

export function readSnapshots(key: string): ProjectSnapshot[] {
  try {
    const raw = readLocal(key);
    if (!raw || raw.length > 12_000_000) return [];
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed) || parsed.length > 8) return [];
    return parsed.filter((item): item is ProjectSnapshot => item
      && typeof item.id === 'string' && item.id.length <= 100
      && typeof item.name === 'string' && item.name.length <= 100
      && Number.isFinite(item.savedAt)
      && typeof item.data === 'string' && item.data.length <= 4_000_000);
  } catch { return []; }
}

export function saveSnapshot(key: string, name: string, data: string): boolean {
  const snapshots = readSnapshots(key);
  if (snapshots.length >= 8 || data.length > 4_000_000) return false;
  const next = JSON.stringify([{ id: crypto.randomUUID(), name: name.slice(0, 100), savedAt: Date.now(), data }, ...snapshots]);
  return next.length <= 12_000_000 && writeLocal(key, next);
}

export function removeSnapshot(key: string, id: string) {
  return writeLocal(key, JSON.stringify(readSnapshots(key).filter(item => item.id !== id)));
}
