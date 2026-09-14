import { test } from 'node:test';
import assert from 'node:assert/strict';
import { PNG } from 'pngjs';
import { blueMask, choiceHypotheses, maskDistance, selectVisualChoice, solveVisualChoice,
  type ChoiceInput } from '../suite/study/visual-choice';
import { key, validate } from '../suite/geometry';
import type { Part, FrameSpec } from '../suite/shared';
import { visualChoiceInputs } from '../suite/study/visual-choice-run';

const input: ChoiceInput = { query: { partId: '3005', color: 'blue' },
  billOfMaterials: { '3035:gray': 1, '3005:blue': 1 },
  convention: { origin: 'Minimum X/Y/Z of the entire structure are each 0.' },
  candidates: [...'ABCD'].map((label, x) => ({ label, x, y: 1, z: 1, turn: 0 })) };
function image(x: number, neutral = false) {
  const png = new PNG({ width: 640, height: 480 }); png.data.fill(255);
  for (let y = 120; y < 170; y++) for (let px = x; px < x + 30; px++) {
    const i = (y * 640 + px) * 4;
    png.data[i] = neutral ? 100 : 20; png.data[i + 1] = 100; png.data[i + 2] = neutral ? 100 : 210;
  }
  return PNG.sync.write(png);
}
const render = async (frame: FrameSpec) => image(40 + 50 * frame.parts[1].x);

test('two-piece hypotheses exhaust supported base poses without a hidden base anchor', () => {
  const hypotheses = choiceHypotheses(input);
  const expected: string[] = [];
  for (const c of input.candidates) for (const turn of [0, 1]) for (let x = 0; x <= 24; x++) for (let z = 0; z <= 24; z++) {
    const base: Part = { id: 'base', partId: '3035', color: 'gray', x, y: 0, z, turn };
    const query: Part = { id: 'query', partId: '3005', color: 'blue', x: c.x, y: c.y, z: c.z, turn: c.turn };
    if (!Math.min(x, c.x) && !Math.min(z, c.z) && !validate([base, query]).length) {
      expected.push(`${c.label}:${key(base)}:${key(query)}`);
    }
  }
  assert.deepEqual(hypotheses.map(h => `${h.label}:${key(h.parts[0])}:${key(h.parts[1])}`).sort(), expected.sort());
  const wide = structuredClone(input);
  wide.query.partId = '3003'; wide.billOfMaterials = { '3035:gray': 1, '3003:blue': 1 };
  assert.ok(choiceHypotheses(wide).some(h => h.parts[0].x > 0 && h.parts[1].x === 0));
});

test('candidate domain checks reject unsupported colors, identities, heights and duplicate poses', () => {
  assert.throws(() => choiceHypotheses({ ...input, query: { ...input.query, color: 'red' } }));
  assert.throws(() => choiceHypotheses({ ...input, billOfMaterials: { '3035:gray': 2, '3005:blue': 1 } }));
  assert.throws(() => choiceHypotheses({ ...input, candidates: input.candidates.map(c => ({ ...c, y: 0 })) }));
  assert.throws(() => choiceHypotheses({ ...input, candidates: input.candidates.map(c => ({ ...c, x: 1 })) }));
  assert.throws(() => choiceHypotheses({ ...input, candidates: input.candidates.map(c => ({ ...c, turn: 4 })) }));
});

test('blue masks ignore neutral changes and overlays and detect true spatial displacement', () => {
  const a = image(40), b = image(90), neutral = image(40, true);
  assert.equal(blueMask(a).count, 1500);
  assert.equal(maskDistance(blueMask(a), blueMask(a)), 0);
  assert.equal(maskDistance(blueMask(a), blueMask(b)), 1);
  assert.equal(blueMask(neutral).count, 0);
  const png = PNG.sync.read(a);
  for (let x = 0; x < 640; x++) for (const y of [10, 460]) {
    const i = (y * 640 + x) * 4; png.data[i] = 0; png.data[i + 1] = 0; png.data[i + 2] = 255;
  }
  assert.equal(maskDistance(blueMask(a), blueMask(PNG.sync.write(png))), 0);
});

test('visual decision ignores label order, abstains on ties and requires four scored candidates', () => {
  const scores = [...'ABCD'].map((label, i) => ({ label, poseKey: `pose${i}`, distance: i / 4 }));
  assert.deepEqual(selectVisualChoice(scores), selectVisualChoice([...scores].reverse()));
  assert.equal(selectVisualChoice(scores).answer?.choice, 'A');
  assert.equal(selectVisualChoice(scores.slice(1)).answer, null);
  assert.equal(selectVisualChoice(scores.map(s => ({ ...s, distance: 0 }))).answer, null);
  assert.throws(() => selectVisualChoice([{ ...scores[0], distance: NaN }]));
});

test('solver responds to reference pixels, remaps permuted labels and does not read hidden fields', async () => {
  const copy = structuredClone(input);
  const before = structuredClone(copy);
  const a = await solveVisualChoice(copy, { top: image(40) }, render);
  assert.equal(a.answer?.choice, 'A');
  const b = await solveVisualChoice(copy, { top: image(90) }, render);
  assert.equal(b.answer?.choice, 'B'); assert.notEqual(a.selectedKey, b.selectedKey);
  const permuted = { ...copy, candidates: [...copy.candidates.slice(1), copy.candidates[0]].map((c, i) => ({ ...c, label: 'ABCD'[i] })) };
  const p = await solveVisualChoice(permuted, { top: image(40) }, render);
  assert.equal(p.answer?.choice, 'D'); assert.equal(p.selectedKey, a.selectedKey);
  assert.deepEqual(copy, before);
  const hidden = Object.defineProperty(copy, 'oracle', { get() { throw new Error('Oracle access forbidden'); } });
  assert.equal((await solveVisualChoice(hidden, { top: image(40) }, render)).answer?.choice, 'A');
});

test('no-image and missing-blue controls abstain before rendering candidates', async () => {
  const forbidden = async () => { throw new Error('Rendering should not happen'); };
  assert.equal((await solveVisualChoice(input, {}, forbidden)).reason, 'no-image');
  assert.equal((await solveVisualChoice(input, { top: image(40, true) }, forbidden)).reason, 'query-mask-missing');
});

test('public development selection contains 60 questions but only 16 source objects', () => {
  const rows = visualChoiceInputs();
  assert.equal(rows.length, 60); assert.equal(new Set(rows.map(r => r.group)).size, 16);
  for (const r of rows) {
    assert.ok(choiceHypotheses(r.input).length > 0);
    assert.ok(!Object.hasOwn(r, 'oracle') && !Object.hasOwn(r, 'target'));
  }
});
