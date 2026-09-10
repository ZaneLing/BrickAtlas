import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import { initialState, type ExplorerState } from '../model/types';
import { readLocal, writeLocal } from '../app/storage';

type BuildProgress = Record<string, number>;
export function sanitizeBuildProgress(value: unknown): BuildProgress {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return {};
  return Object.fromEntries(Object.entries(value).slice(0, 500).filter(([id, step]) =>
    /^[\w-]{1,100}$/.test(id) && typeof step === 'number' && Number.isSafeInteger(step) && step >= 0 && step <= 10000));
}

function preferences(viewer: ExplorerState) {
  return { quality: viewer.quality, background: viewer.background, edges: viewer.edges, grid: viewer.grid };
}
interface ViewerStore {
  viewer: ExplorerState;
  activeModelId: string | null;
  selectedBrickId: string | null;
  hiddenBrickIds: string[];
  isolatedBrickIds: string[] | null;
  explodeProgress: number;
  currentBuildStep: number | null;
  buildProgress: BuildProgress;
  patch: (update: Partial<ExplorerState>) => void;
  update: (updater: (state: ExplorerState) => ExplorerState) => void;
  loadModel: (modelId: string, mode: 'explore' | 'build', stepCount: number) => void;
  reset: (mode?: 'explore' | 'build') => void;
}

const aliases = (viewer: ExplorerState) => ({
  selectedBrickId: viewer.selection[0] ?? null,
  hiddenBrickIds: viewer.hiddenBrickIds,
  isolatedBrickIds: viewer.isolation,
  explodeProgress: viewer.explosion,
  currentBuildStep: viewer.buildStep,
});

export const useViewerStore = create<ViewerStore>()(persist(set => ({
  viewer: initialState,
  activeModelId: null,
  ...aliases(initialState),
  buildProgress: {},
  patch: update => set(state => {
    const viewer = { ...state.viewer, ...update };
    const progress = viewer.buildStep !== null && state.activeModelId
      ? { ...state.buildProgress, [state.activeModelId]: viewer.buildStep }
      : state.buildProgress;
    return { viewer, ...aliases(viewer), buildProgress: progress };
  }),
  update: updater => set(state => {
    const viewer = updater(state.viewer);
    return { viewer, ...aliases(viewer), buildProgress: viewer.buildStep !== null && state.activeModelId
      ? { ...state.buildProgress, [state.activeModelId]: viewer.buildStep } : state.buildProgress };
  }),
  loadModel: (modelId, mode, stepCount) => set(state => {
    const saved = Math.min(sanitizeBuildProgress(state.buildProgress)[modelId] ?? 0, stepCount);
    const viewer = { ...initialState, ...preferences(state.viewer), buildStep: mode === 'build' ? saved : null };
    return { activeModelId: modelId, viewer, ...aliases(viewer) };
  }),
  reset: mode => set(state => {
    const viewer = { ...initialState, buildStep: mode === 'build' ? 0 : null, revision: state.viewer.revision + 1 };
    return { viewer, ...aliases(viewer), buildProgress: mode === 'build' && state.activeModelId
      ? { ...state.buildProgress, [state.activeModelId]: 0 } : state.buildProgress };
  }),
}), {
  name: 'brick-atlas-viewer',
  storage: createJSONStorage(() => ({
    getItem: readLocal,
    setItem: (key, value) => { writeLocal(key, value); },
    removeItem: key => { try { localStorage.removeItem(key); } catch { /* Storage can be disabled. */ } },
  })),
  partialize: state => ({ buildProgress: state.buildProgress, preferences: preferences(state.viewer) }),
  merge: (persisted, current) => {
    const saved = persisted as { buildProgress?: unknown; preferences?: Partial<ExplorerState> } | null;
    const p = saved?.preferences;
    const viewer = { ...current.viewer };
    if (p && ['auto', 'high', 'ultra', 'low'].includes(p.quality!)) viewer.quality = p.quality!;
    if (p && ['studio', 'white', 'dark'].includes(p.background!)) viewer.background = p.background!;
    if (typeof p?.edges === 'boolean') viewer.edges = p.edges;
    if (typeof p?.grid === 'boolean') viewer.grid = p.grid;
    return { ...current, viewer, ...aliases(viewer), buildProgress: sanitizeBuildProgress(saved?.buildProgress) };
  },
}));
