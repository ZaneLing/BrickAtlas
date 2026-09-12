import { test } from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { researchModels } from '../suite/research/dataset';
import { independentCheck } from '../suite/research/independent-check';
import { auditConnectors } from '../suite/research/connectors';
import { researchTaskFor, researchScore, surfaceSignature } from '../suite/research/tasks';
import { researchSelection } from '../suite/research/run';
import { reviewQueue, loadReviews, submitReview } from '../suite/research/review';
import { TASKS, type Part } from '../suite/shared';
import { edges } from '../suite/geometry';
import { BENCHMARK } from '../suite/storage';

test('composition grammar produces 576 distinct geometries without color expansion', () => {
  const data = researchModels();
  assert.equal(data.length, 576);
  assert.equal(new Set(data.map(m => m.group)).size, data.length);
  const seen = new Map<string, string>();
  for (const m of data) {
    if (seen.has(m.topology)) assert.equal(seen.get(m.topology), m.split);
    seen.set(m.topology, m.split);
    const check = independentCheck(m.structure.parts);
    assert.deepEqual(check.issues, []);
    assert.equal(check.contacts.reduce((n, e) => n + e.studs, 0), edges(m.structure.parts).reduce((n, e) => n + e.studs, 0));
  }
});
for (const kind of TASKS) test(`research ${kind}: all targets pass all declared information conditions`, () => {
  for (const m of researchModels()) for (const condition of ['ordinary', 'layers', 'symbolic'] as const) {
    const task = researchTaskFor(m, kind, condition);
    assert.equal(researchScore(task, task.oracle).metrics.success, 1, `${m.id}/${condition}`);
    assert.equal(researchScore(task, {}).metrics.success, 0);
    if (condition === 'ordinary' && ['reconstruct', 'complete', 'repair'].includes(kind)) {
      assert.equal(task.frames.length, 4);
      assert.ok(!('reference' in task.public.input));
      assert.ok(task.frames.every(f => f.layer === null));
    }
  }
});
test('visible surface scoring does not demand one unobservable hidden arrangement', () => {
  const p = (id: string, partId: string, color: Part['color'], x: number, y: number, z: number, turn = 0): Part => ({ id, partId, color, x, y, z, turn });
  const parts = [
    p('base', '3035', 'gray', 0, 0, 0), p('front', '3008', 'red', 0, 1, 3), p('back', '3008', 'red', 0, 1, 0),
    p('left', '3004', 'red', 0, 1, 1, 1), p('right', '3004', 'red', 7, 1, 1, 1),
    p('inside-a', '3004', 'blue', 2, 1, 1), p('inside-b', '3004', 'blue', 4, 1, 2), p('roof', '3035', 'yellow', 0, 4, 0),
  ];
  const alternative = parts.map(p => p.id === 'inside-a' ? { ...p, turn: 1 } : p.id === 'inside-b' ? { ...p, turn: 1, z: 1 } : p);
  assert.deepEqual(surfaceSignature(parts), surfaceSignature(alternative));
  const task = researchTaskFor(researchModels()[0], 'reconstruct', 'ordinary');
  task.target = { version: 1, parts };
  const result = researchScore(task, { version: 1, parts: alternative });
  assert.equal(result.metrics.fullStructureSuccess, 0); assert.equal(result.metrics.success, 1);
  const wrong = alternative.map(p => p.id === 'roof' ? { ...p, color: 'green' as const } : p);
  assert.equal(researchScore(task, { version: 1, parts: wrong }).metrics.success, 0);
});
test('constraint generation accepts a different color design without target voxel masks', () => {
  const t = researchTaskFor(researchModels()[0], 'generate');
  assert.ok(!('volume' in t.public.input));
  const alternative = { version: 1, parts: t.target.parts.map((p, i) => ({ ...p, color: i ? 'red' : 'blue' })) };
  assert.equal(researchScore(t, alternative).metrics.success, 1);
});
test('independent checker detects floating, colliding and obstructed insertion cases', () => {
  const p: Part = { id: 'p', partId: '3001', color: 'red', x: 0, y: 0, z: 0, turn: 0 };
  assert.ok(independentCheck([{ ...p, y: 10 }]).issues.includes('unsupported_prefix'));
  assert.ok(independentCheck([p, { ...p, id: 'q' }]).issues.includes('collision'));
});
test('connector annotations agree with all grid types and generated structures', {
  skip: !existsSync(resolve(BENCHMARK, '.runtime/vendor/bricknet/normalized-connectors.json')),
}, () => {
  const result = auditConnectors();
  assert.equal(result.allAgree, true);
  assert.equal(result.partChecks.length, 25);
  assert.equal(result.assembliesChecked, 576);
});
test('paired experiment reuses the same heldout objects and distinct source families', () => {
  const selection = researchSelection();
  assert.equal(selection.length, 56);
  assert.equal(new Set(selection.map(s => s.modelId)).size, 4);
  const data = researchModels().filter(m => selection.some(s => s.modelId === m.id));
  assert.equal(new Set(data.map(m => m.family)).size, 4);
  assert.ok(data.every(m => ['test_id', 'test_ood'].includes(m.split)));
});
test('human review requires acknowledgement and never creates production reviews during tests', () => {
  const before = loadReviews().length, sampleId = reviewQueue()[0].id;
  const directory = mkdtempSync(resolve(tmpdir(), 'brick-review-fixture-'));
  try {
    assert.throws(() => submitReview({ sampleId }, directory));
    const row = { sampleId, reviewer: 'fixture_only', judgment: 'uncertain', notes: 'Test fixture, not a human review.',
      independent: false, acknowledged: true };
    submitReview(row, directory);
    assert.equal(loadReviews(directory).length, 1);
    assert.throws(() => submitReview(row, directory), /already submitted/);
  } finally { rmSync(directory, { recursive: true }); }
  assert.equal(loadReviews().length, before);
});
