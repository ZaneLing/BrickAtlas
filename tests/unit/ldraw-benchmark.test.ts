import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { score, replay } from '../../src/benchmark/engine';
import { generateQuestions } from '../../benchmark/suite/ldraw/questions';
import { scoreLDrawBatch } from '../../benchmark/suite/ldraw/score';
import { LDRAW_REVIEW_KEY, importLDrawReviews, ldrawReviewBatch, loadLDrawReviews, makeLDrawReview, persistLDrawReviews } from '../../src/benchmark/ldrawReviewStore';
import type { LDrawBundle } from '../../src/benchmark/ldrawTypes';
const read = (p: string) => JSON.parse(readFileSync(p, 'utf8'));
const catalog = read('benchmark/ldraw-v1/catalog.json');
const bundles: LDrawBundle[] = catalog.map((m: any) => read(`public/benchmark/ldraw/models/${m.id}.json`));
const answer = (t: LDrawBundle['tasks'][number]) => t.options!.find(o => o.id === t.answer.choiceId)!.value;
describe('Original LDraw benchmark', () => {
  it('keeps missing submissions in the denominator and rejects duplicate or foreign IDs', () => {
    const task = bundles[0].tasks[0];
    const result = scoreLDrawBatch([{ id: task.id, answer: task.answer }]);
    expect(result).toMatchObject({ expected: 617, submitted: 1, missing: 616, success: 1 });
    expect(Object.values(result.bySource).reduce((n, r) => n + r.total, 0)).toBe(617);
    expect(() => scoreLDrawBatch([{ id: 'unknown', answer: {} }])).toThrow('Unknown');
    expect(() => scoreLDrawBatch([{ id: task.id }, { id: task.id }])).toThrow('Duplicate');
  });
  it('recomputes answers from original instance attributes and independent graph traversal', () => {
    for (const bundle of bundles) {
      const manifest = read(`public/models/${bundle.entry.id}/manifest.json`);
      const parts = new Map<string, any>(manifest.instances.map((p: any) => [p.instanceId, p]));
      expect(generateQuestions(manifest, bundle.audit, bundle.entry.difficulty)).toEqual(bundle.tasks);
      for (const t of bundle.tasks) {
        expect(score(t, t.answer).success, t.id).toBe(1);
        const p = parts.get(t.references[0]?.id);
        if (t.family === 'color') expect(answer(t)).toBe(p.colorCode);
        if (t.family === 'shape-match') expect(parts.get(answer(t)).partNumber).toBe(p.partNumber);
        if (t.family === 'graph-removal') {
          const remaining = new Set<string>(t.input.nodes.filter((v: string) => v !== t.references[0].label));
          let count = 0;
          while (remaining.size) {
            count++;
            const stack: string[] = [remaining.values().next().value!]; remaining.delete(stack[0]);
            while (stack.length) {
              const v = stack.pop()!;
              for (const [a, b] of t.input.edges) {
                const w = a === v ? b : b === v ? a : null;
                if (w && remaining.has(w)) { remaining.delete(w); stack.push(w); }
              }
            }
          }
          expect(answer(t)).toBe(count);
        }
        if (t.family === 'source-step') {
          expect(bundle.instructions?.provenance).toBe('source');
          expect(answer(t)).toBe(bundle.instructions!.steps.findIndex(s => s.instanceIds.includes(p.instanceId)) + 1);
        }
        if (t.format === 'actions') {
          expect(replay(t, t.answer.actionIds.slice(0, -1)).success).toBe(0);
          expect(replay(t, ['unknown']).success).toBe(0);
        }
      }
    }
  }, 30000);
  it('binds unique instance numbers and publishes no visual answer metadata', () => {
    expect(new Set(catalog.map((m: any) => m.setNumber)).size).toBe(catalog.length);
    for (const bundle of bundles) {
      const input = read(`public/benchmark/ldraw/inputs/${bundle.entry.id}.json`);
      expect(input.numberedInstances.every((r: any) => Object.keys(r).sort().join() === 'id,label')).toBe(true);
      for (const t of input.tasks) {
        expect(t).not.toHaveProperty('answer'); expect(t).not.toHaveProperty('evidenceDetail');
        if (t.modality === 'visual') expect(t.input).toEqual({});
        for (const r of t.references) expect(bundle.parts.find(p => p.id === r.id)?.label).toBe(r.label);
      }
      expect(bundle.audit.duplicatePlacements).toBe(0);
      expect(bundle.audit.connectorCoverage).toBeGreaterThanOrEqual(.9);
      expect(bundle.audit.sourceGeometryModified).toBe(false);
    }
  });
  it('keeps old human feedback and rejects incomplete or mismatched new reviews', () => {
    const values = new Map([['brickatlas:hierarchy3:reviews:v1', 'historical feedback unchanged']]);
    const storage = { getItem: (k: string) => values.get(k) ?? null, setItem: (k: string, v: string) => { values.set(k, v); } };
    const b = bundles[0], t = b.tasks[0];
    expect(() => makeLDrawReview(t, b.entry.sourceHash, 'fail', ' ')).toThrow('必须');
    const record = makeLDrawReview(t, b.entry.sourceHash, 'fail', '编号与观察需要复核');
    persistLDrawReviews({ [t.id]: record }, storage);
    expect(loadLDrawReviews(storage)[t.id]).toEqual(record);
    expect(values.get('brickatlas:hierarchy3:reviews:v1')).toBe('historical feedback unchanged');
    const batch = ldrawReviewBatch({ [t.id]: record }, 617);
    expect(importLDrawReviews(JSON.stringify(batch), storage)).toEqual({ [t.id]: record });
    expect(() => importLDrawReviews(JSON.stringify({ ...batch, benchmarkVersion: 'brickatlas-hierarchy-3' }), storage)).toThrow();
    values.set(LDRAW_REVIEW_KEY, JSON.stringify([{ ...record, reason: '' }]));
    expect(loadLDrawReviews(storage)).toEqual({});
  });
});
