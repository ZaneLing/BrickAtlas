import { afterEach, describe, expect, it, vi } from 'vitest';
import { modelCatalog } from '../../atlas.config';
import { assemblyDifficulty } from '../../src/assembly/difficulty';
import {
  groupAssemblyMaterials, partOrientationMatches, partQuarterTurn,
} from '../../src/assembly/orientation';
import type { PartInstance } from '../../src/model/types';
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
      placedTurns: { brick_000001: 1 },
      completed: false,
      updatedAt: 123,
    })).toBe(true);
    expect(readModelAssemblyProgress('31028-sailboat')).toMatchObject({
      completedStep: 3,
      placedIds: ['brick_000001'],
      placedTurns: { brick_000001: 1 },
      completed: false,
    });
    saveModelAssemblyProgress('31028-sailboat', {
      completedStep: 7,
      placedIds: [],
      placedTurns: {},
      completed: true,
      updatedAt: 456,
    });
    expect(completedAssemblyModels().has('31028-sailboat')).toBe(true);
    clearModelAssemblyProgress('31028-sailboat');
    expect(completedAssemblyModels().has('31028-sailboat')).toBe(false);
  });

  it('groups directional parts by quarter turn and validates orientation', () => {
    const part = {
      partNumber: '3040b',
      colorCode: '4',
      displayName: 'Slope Brick 45 1 x 2',
      colorName: 'Red',
      colorHex: '#c91a09',
      tags: ['slope'],
      originalMatrix: [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
      instanceId: 'brick_1',
    } as PartInstance;
    const turned = {
      ...part,
      instanceId: 'brick_2',
      originalMatrix: [0, 0, -1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    };
    expect(partQuarterTurn(part)).toBe(0);
    expect(partQuarterTurn(turned)).toBe(3);
    expect(partOrientationMatches(turned, 0)).toBe(false);
    expect(partOrientationMatches(turned, 3)).toBe(true);
    expect(groupAssemblyMaterials([part, turned])).toHaveLength(2);
  });
});
