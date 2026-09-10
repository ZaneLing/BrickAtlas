import { readLocal, writeLocal } from '../app/storage';

export const ASSEMBLY_PROGRESS_KEY = 'brick-atlas-assembly-game-v1';

export interface ModelAssemblyProgress {
  completedStep: number;
  placedIds: string[];
  placedTurns?: Record<string, 0 | 1 | 2 | 3>;
  completed: boolean;
  updatedAt: number;
}

export type AssemblyProgressMap = Record<string, ModelAssemblyProgress>;

export function readAssemblyProgress(): AssemblyProgressMap {
  try {
    const parsed = JSON.parse(readLocal(ASSEMBLY_PROGRESS_KEY) ?? '{}') as AssemblyProgressMap;
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return {};
    return Object.fromEntries(Object.entries(parsed)
      .filter(([, value]) =>
        value
        && Number.isInteger(value.completedStep)
        && value.completedStep >= 0
        && Array.isArray(value.placedIds)
        && value.placedIds.every(id => typeof id === 'string')
        && typeof value.completed === 'boolean',
      )
      .map(([modelId, value]) => [modelId, {
        ...value,
        placedTurns: value.placedTurns
          && typeof value.placedTurns === 'object'
          && !Array.isArray(value.placedTurns)
          && Object.values(value.placedTurns).every(turn => [0, 1, 2, 3].includes(turn))
          ? value.placedTurns
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
