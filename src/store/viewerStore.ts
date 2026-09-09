import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import { initialState, type ExplorerState } from '../model/types';
import { readLocal, writeLocal } from '../app/storage';

type BuildProgress = Record<string, number>;
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
    const saved = Math.min(state.buildProgress[modelId] ?? 0, stepCount);
    const viewer = { ...initialState, buildStep: mode === 'build' ? saved : null };
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
  partialize: state => ({ buildProgress: state.buildProgress }),
}));
