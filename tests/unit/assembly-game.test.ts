import { afterEach, describe, expect, it, vi } from 'vitest';
import { modelCatalog } from '../../atlas.config';
import { assemblyDifficulty } from '../../src/assembly/difficulty';
import {
  clearModelAssemblyProgress, completedAssemblyModels, readModelAssemblyProgress,
  saveModelAssemblyProgress,
} from '../../src/assembly/progress';

function memoryStorage() {
  const values = new Map<string, string>();
  return {
    getItem: (key: string) => values.get(key) ?? null,
    setItem: (key: string, value: string) => { values.set(key, value); },
    removeItem: (key: string) => { values.delete(key); },
  };
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe('assembly game progression', () => {
  it('assigns all catalog models to difficulty levels one through five', () => {
    const values = modelCatalog.map(model => assemblyDifficulty(model.id));
    expect(values.every(value => value >= 1 && value <= 5)).toBe(true);
    expect(new Set(values)).toEqual(new Set([1, 2, 3, 4, 5]));
  });

  it('persists partial progress and exposes completion badges', () => {
    vi.stubGlobal('localStorage', memoryStorage());
    expect(readModelAssemblyProgress('31028-sailboat').completedStep).toBe(0);
    expect(saveModelAssemblyProgress('31028-sailboat', {
      completedStep: 3,
      placedIds: ['brick_000001'],
      completed: false,
      updatedAt: 123,
    })).toBe(true);
    expect(readModelAssemblyProgress('31028-sailboat')).toMatchObject({
      completedStep: 3,
      placedIds: ['brick_000001'],
      completed: false,
    });
    saveModelAssemblyProgress('31028-sailboat', {
      completedStep: 7,
      placedIds: [],
      completed: true,
      updatedAt: 456,
    });
    expect(completedAssemblyModels().has('31028-sailboat')).toBe(true);
    clearModelAssemblyProgress('31028-sailboat');
    expect(completedAssemblyModels().has('31028-sailboat')).toBe(false);
  });
});
