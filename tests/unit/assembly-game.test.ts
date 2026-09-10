import { afterEach, describe, expect, it, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { modelCatalog } from '../../atlas.config';
import { assemblyDifficulty } from '../../src/assembly/difficulty';
import {
  auditAssemblyStep, groupAssemblyMaterials, partOrientationMatches, partQuarterTurn,
} from '../../src/assembly/orientation';
import type { PartInstance } from '../../src/model/types';
import type { AtlasManifest } from '../../src/model/types';
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
      placedPositions: { brick_000001: [4, 8, 12] },
      completed: false,
      updatedAt: 123,
    })).toBe(true);
    expect(readModelAssemblyProgress('31028-sailboat')).toMatchObject({
      completedStep: 3,
      placedIds: ['brick_000001'],
      placedTurns: { brick_000001: 1 },
      placedPositions: { brick_000001: [4, 8, 12] },
      completed: false,
    });
    saveModelAssemblyProgress('31028-sailboat', {
      completedStep: 7,
      placedIds: [],
      placedTurns: {},
      placedPositions: {},
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
      bounds: { min: [-4, -4, -8], max: [4, 4, 8] },
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
    const step = {
      id: 'step-1',
      title: 'Step',
      sourceFile: 'model.ldr',
      sourceStep: 1,
      instanceIds: ['brick_1', 'brick_2'],
      kind: 'parts' as const,
    };
    expect(auditAssemblyStep(
      step,
      [part, turned],
      ['brick_1'],
      { brick_1: 0 },
      { brick_1: [0, 0, 0] },
    ).ok).toBe(false);
    expect(auditAssemblyStep(step, [part, turned], ['brick_1', 'brick_2'], {
      brick_1: 0,
      brick_2: 0,
    }, {
      brick_1: [0, 0, 0],
      brick_2: [0, 0, 0],
    })).toMatchObject({
      ok: true,
      missingIds: [],
      unexpectedIds: [],
      wrongOrientationIds: [],
      wrongPositionIds: [],
    });
  });

  it('audits every catalog step against exact instances and authored orientation', () => {
    for (const model of modelCatalog) {
      const manifest = JSON.parse(
        readFileSync(`public/models/${model.id}/manifest.json`, 'utf8'),
      ) as AtlasManifest;
      for (const step of manifest.instructions?.steps ?? []) {
        const expected = new Set(step.instanceIds);
        const parts = manifest.instances.filter(part => expected.has(part.instanceId));
        if (step.kind === 'placement') {
          expect(auditAssemblyStep(step, [], [], {}, {}, true).ok, `${model.id}:${step.id}`).toBe(true);
          expect(auditAssemblyStep(step, [], [], {}, {}, false).ok, `${model.id}:${step.id}:missing`).toBe(false);
          continue;
        }
        const turns = Object.fromEntries(parts.map(part => [
          part.instanceId,
          0 as const,
        ]));
        const positions = Object.fromEntries(parts.map(part => [
          part.instanceId,
          [0, 1, 2].map(axis =>
            (part.bounds.min[axis] + part.bounds.max[axis]) / 2) as [number, number, number],
        ]));
        expect(
          auditAssemblyStep(step, parts, step.instanceIds, turns, positions).ok,
          `${model.id}:${step.id}`,
        ).toBe(true);
        if (step.instanceIds.length) {
          expect(
            auditAssemblyStep(step, parts, step.instanceIds.slice(1), turns, positions).ok,
            `${model.id}:${step.id}:missing`,
          ).toBe(false);
        }
      }
    }
  });
});
