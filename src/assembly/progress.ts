import { readLocal, writeLocal } from '../app/storage';

export const ASSEMBLY_PROGRESS_KEY = 'brick-atlas-assembly-game-v1';

export interface ModelAssemblyProgress {
  completedStep: number;
  placedIds: string[];
  placedTurns?: Record<string, 0 | 1 | 2 | 3>;
  placedPositions?: Record<string, [number, number, number]>;
  completed: boolean;
  updatedAt: number;
}

export type AssemblyProgressMap = Record<string, ModelAssemblyProgress>;

export function readAssemblyProgress(): AssemblyProgressMap {
  try {
    const raw = readLocal(ASSEMBLY_PROGRESS_KEY) ?? '{}';
    if (raw.length > 4_000_000) return {};
    const parsed = JSON.parse(raw) as AssemblyProgressMap;
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return {};
    return Object.fromEntries(Object.entries(parsed).slice(0, 500)
      .filter(([id, value]) =>
        /^[\w-]{1,100}$/.test(id) && value
        && Number.isInteger(value.completedStep)
        && value.completedStep >= 0 && value.completedStep <= 10000
        && Array.isArray(value.placedIds)
        && value.placedIds.length <= 5000
        && value.placedIds.every(id => typeof id === 'string' && id.length <= 100)
        && typeof value.completed === 'boolean',
      )
      .map(([modelId, value]) => [modelId, {
        ...value,
        completed: value.completed && value.completedStep > 0,
        updatedAt: Number.isFinite(value.updatedAt) && value.updatedAt >= 0 ? value.updatedAt : 0,
        placedIds: [...new Set(value.placedIds)],
        placedTurns: value.placedTurns
          && typeof value.placedTurns === 'object'
          && !Array.isArray(value.placedTurns)
          ? Object.fromEntries(Object.entries(value.placedTurns).filter(([id, turn]) => value.placedIds.includes(id) && [0, 1, 2, 3].includes(turn)))
          : {},
        placedPositions: value.placedPositions
          && typeof value.placedPositions === 'object'
          && !Array.isArray(value.placedPositions)
          ? Object.fromEntries(Object.entries(value.placedPositions).filter(([id, position]) =>
            value.placedIds.includes(id) && Array.isArray(position)
            && position.length === 3
            && position.every(n => Number.isFinite(n) && Math.abs(n) <= 1_000_000)))
          : {},
      }]));
  } catch {
    return {};
  }
}

export function readModelAssemblyProgress(modelId: string): ModelAssemblyProgress {
  return readAssemblyProgress()[modelId] ?? {
    completedStep: 0,
    placedIds: [],
    placedTurns: {},
    placedPositions: {},
    completed: false,
    updatedAt: 0,
  };
}

export function saveModelAssemblyProgress(modelId: string, progress: ModelAssemblyProgress) {
  const all = readAssemblyProgress();
  return writeLocal(ASSEMBLY_PROGRESS_KEY, JSON.stringify({
    ...all,
    [modelId]: progress,
  }));
}

export function clearModelAssemblyProgress(modelId: string) {
  const all = readAssemblyProgress();
  delete all[modelId];
  return writeLocal(ASSEMBLY_PROGRESS_KEY, JSON.stringify(all));
}

export function completedAssemblyModels() {
  return new Set(
    Object.entries(readAssemblyProgress())
      .filter(([, progress]) => progress.completed)
      .map(([modelId]) => modelId),
  );
}
