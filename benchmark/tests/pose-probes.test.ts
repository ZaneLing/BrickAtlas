import { test } from 'node:test';
import assert from 'node:assert/strict';
import { poseQuestions, poseScenes, scorePose } from '../suite/study/pose-probes';
import { key } from '../suite/geometry';
import { validationCases } from '../suite/study/model-validation';
import { ladderTasks } from '../suite/study/reconstruction-ladder';

test('pose probes have four distinct unused sources, zero origin and balanced choices', () => {
  const excluded = new Set([...validationCases().chosen.map(s => s.group), ...ladderTasks().map(t => t.task.spec.group)]);
  const scenes = poseScenes(), qs = poseQuestions();
  assert.equal(scenes.length, 4); assert.equal(qs.length, 24);
  assert.equal(new Set(scenes.map(s => s.geometry)).size, 4);
  for (const s of scenes) {
    assert.ok(!excluded.has(s.group));
    for (const k of ['x', 'y', 'z'] as const) assert.equal(Math.min(...s.target.parts.map(p => p[k])), 0);
  }
  for (const arm of ['choice-rgb', 'choice-permuted', 'choice-no-image']) {
    assert.deepEqual(qs.filter(q => q.arm === arm).map(q => (q.oracle as any).choice).sort(), ['A', 'B', 'C', 'D']);
  }
});

test('all oracle responses pass but malformed fields do not gain credit', () => {
  for (const q of poseQuestions()) {
    assert.equal(scorePose(q, JSON.stringify(q.oracle)).success, 1, q.arm);
    for (const raw of ['null', '[]', '{}', 'not json', '{"choice":["A"]}']) assert.equal(scorePose(q, raw).success, 0);
    if (q.arm.startsWith('pose')) {
      const a = { ...q.query, x: String(q.query.x) };
      assert.equal(scorePose(q, JSON.stringify(a)).format, 0);
      assert.equal(scorePose(q, JSON.stringify({ ...q.query, turn: (q.query.turn + 2) % 4 })).success, 1);
      assert.equal(scorePose(q, JSON.stringify({ ...q.query, x: q.query.x + 1 })).success, 0);
    }
  }
});

test('candidate permutation preserves poses but moves the correct label', () => {
  const questions = poseQuestions();
  for (const original of questions.filter(q => q.arm === 'choice-rgb')) {
    const permuted = questions.find(q => q.group === original.group && q.arm === 'choice-permuted')!;
    assert.deepEqual(original.candidates.map(p => key({ ...original.query, ...p })).sort(),
      permuted.candidates.map(p => key({ ...original.query, ...p })).sort());
    assert.notEqual((original.oracle as any).choice, (permuted.oracle as any).choice);
    const outcomes = original.candidates.map(c => scorePose(original, JSON.stringify({ choice: c.label })).success);
    assert.equal(outcomes.reduce((a, b) => a + b, 0), 1, 'Uniform guess expectation must be 1/4');
  }
});

test('images and symbolic truth respect arm boundaries', () => {
  for (const q of poseQuestions()) {
    assert.equal('reference' in q.input, q.arm === 'pose-symbolic');
    assert.equal(q.frames.length, ['choice-no-image', 'pose-symbolic'].includes(q.arm) ? 0 : 4);
    assert.equal('candidates' in q.input, q.arm.startsWith('choice'));
    assert.ok(!('oracle' in q.input));
  }
});
