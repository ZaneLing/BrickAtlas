import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { expansionModels } from '../../benchmark/suite/hierarchy3-expanded/models';
import { BASE, OUT, geometryFingerprint, read } from '../../benchmark/suite/hierarchy3-expanded/release';
import { semanticKey } from '../../benchmark/suite/hierarchy3/tasks';
import { validateModel } from '../../benchmark/suite/hierarchy3/validate';
import { score, solveActions } from '../../src/benchmark/engine';
import { createReviewBatch, importReviewBatch, reviewTask } from '../../src/benchmark/reviewStore';
import { scoreBatch } from '../../benchmark/suite/hierarchy3-expanded/score';
import type { Task } from '../../src/benchmark/types';

const catalog = read(resolve(OUT, 'catalog.json')) as any[];
const bundles = catalog.map(m => read(resolve(OUT, 'models', `${m.id}.json`)));
const tasks: Task[] = bundles.flatMap(b => b.tasks);
describe('144-model compatible expansion', () => {
  it('adds 96 geometrically distinct models with complete crossed coverage', () => {
    expect(catalog).toHaveLength(144); expect(tasks).toHaveLength(6912);
    expect(new Set(tasks.map(t => t.id)).size).toBe(6912);
    const added = expansionModels();
    expect(added).toHaveLength(96);
    expect(new Set(added.map(geometryFingerprint)).size).toBe(96);
    for (const level of ['D1', 'D2', 'D3', 'D4']) {
      expect(catalog.filter(m => m.difficulty === level)).toHaveLength(36);
      expect(added.filter(m => m.difficulty === level)).toHaveLength(24);
      for (const family of new Set(tasks.map(t => t.family)))
        expect(tasks.filter(t => t.difficulty === level && t.family === family)).toHaveLength(36);
    }
  });
  it('preserves all 48 old files and accepts exported old review decisions', () => {
    for (const m of catalog.filter(m => m.retained))
      expect(readFileSync(resolve(OUT, 'models', `${m.id}.json`))
        .equals(readFileSync(resolve(BASE, 'models', `${m.id}.json`))), m.id).toBe(true);
    const task = tasks.find(t => t.id === 'h3-camera-gimbal-identify')!;
    const row = reviewTask(task, 'fail', '人类原有审核理由');
    const oldBatch = createReviewBatch({ [task.id]: row }, 2304);
    let value: string | null = null;
    const storage = { getItem: () => value, setItem: (_: string, v: string) => { value = v; }, removeItem: () => { value = null; } };
    const merged = importReviewBatch(JSON.stringify(oldBatch), storage);
    const expanded = createReviewBatch(merged, tasks.length);
    expect(expanded.records[0]).toEqual(row);
    expect(expanded.summary).toEqual({ totalTasks: 6912, reviewed: 1, passed: 0, failed: 1, pending: 6911 });
  });
  it('accepts references and rejects incorrect choices and truncated action programs', () => {
    for (const t of tasks.filter(t => t.modelId.startsWith('exp-'))) {
      expect(score(t, t.answer).success, t.id).toBe(1);
      expect(score(t, {}).success, t.id).toBe(0);
      if (t.options) {
        const keys = t.options.map(o => semanticKey(t, o.value));
        expect(new Set(keys).size, t.id).toBe(keys.length);
        for (const o of t.options) if (t.format === 'single-choice') {
          expect(score(t, { choiceId: o.id }).success, t.id).toBe(Number(t.answer.choiceId === o.id));
        } else {
          const ids = new Set<string>(t.answer.choiceIds);
          if (ids.has(o.id)) ids.delete(o.id); else ids.add(o.id);
          expect(score(t, { choiceIds: [...ids] }).success, t.id).toBe(0);
        }
      }
      if (t.format === 'actions') {
        expect(score(t, solveActions(t)).success, t.id).toBe(1);
        expect(score(t, { actionIds: t.answer.actionIds.slice(0, -1) }).success, t.id).toBe(0);
        expect(score({ ...t, input: { ...t.input, budget: 0 } }, t.answer).success, t.id).toBe(0);
      }
    }
  });
  it('independently recomputes selected graph, pose, inventory and belief answers', () => {
    const answer = (t: Task) => t.options!.find(o => o.id === t.answer.choiceId)!.value;
    for (const b of bundles.filter(b => b.model.id.startsWith('exp-'))) {
      for (const t of b.tasks as Task[]) {
        if (t.family === 'count') expect(answer(t)).toBe(b.model.parts.filter((p: any) => p.moduleId === t.targetModule).length);
        if (t.family === 'inventory') expect(answer(t)).toBe(t.input.available - t.input.required);
        if (t.family === 'rotate') {
          const difference = t.input.targetYaw - t.input.currentYaw;
          expect(answer(t)).toBe(difference < -180 ? difference + 360 : difference >= 180 ? difference - 360 : difference);
        }
        if (t.family === 'parent') expect(answer(t)).toEqual([...new Set(b.model.joints.filter((j: any) => j.child === t.targetModule).map((j: any) => j.parent))].sort());
        if (t.family === 'posterior') {
          const compatible = t.input.worlds.filter((_: string, i: number) => t.input.observationByWorld[i] === t.input.observed);
          expect(answer(t)).toBe(compatible.includes('jammed') ? 1 / compatible.length : 0);
        }
      }
    }
  });
  it('keeps fixed physical tolerances and validates every new primitive construction family live', async () => {
    for (const b of bundles) {
      expect(b.validation.penetrations, b.model.id).toEqual([]);
      expect(b.physics.nominalPointDrift, b.model.id).toBeLessThan(0.35);
      expect(b.physics.nominalAngularDrift, b.model.id).toBeLessThan(0.15);
      expect(b.physics.jointResiduals.every((j: any) => j.residual < 0.02), b.model.id).toBe(true);
      expect(b.validation.limits.every((j: any) => j.enabled), b.model.id).toBe(true);
    }
    for (const m of expansionModels().filter(m => m.difficulty === 'D1'))
      expect((await validateModel(m)).penetrations).toEqual([]);
  });
  it('scores the expanded denominator and rejects unknown or duplicate submissions', () => {
    const report = scoreBatch([{ id: tasks[0].id, answer: tasks[0].answer }]);
    expect(report.expected).toBe(6912);
    expect(report.missing).toBe(6911);
    expect(report.rows.reduce((n, row) => n + row.verdict.success, 0)).toBe(1);
    expect(() => scoreBatch([{ id: 'unknown', answer: {} }])).toThrow('Unknown');
    expect(() => scoreBatch([{ id: tasks[0].id }, { id: tasks[0].id }])).toThrow('Duplicate');
  });
});
