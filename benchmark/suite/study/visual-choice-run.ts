import assert from 'node:assert/strict';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { SUITE } from '../storage';
import { SuiteRenderer } from '../render';
import { STUDY } from './protocol';
import { imageEvidence } from './calibration-export';
import { choiceHypotheses, MATCH_VIEWS, solveVisualChoice, VISUAL_CHOICE_VERSION, type ChoiceInput } from './visual-choice';

export const VISUAL_CHOICE_DIR = resolve(STUDY, 'visual-choice');
function sourceHashes() {
  return Object.fromEntries(['study/visual-choice.ts', 'study/visual-choice-run.ts',
    'web/viewer.ts', 'render.ts', 'shared.ts', 'geometry.ts', 'data.ts'].map(p =>
    [p, digest(readFileSync(resolve(SUITE, p), 'utf8'))]));
}
export function visualChoiceInputs() {
  return ['pose-probes', 'order-study'].flatMap(cohort => {
    const protocol = JSON.parse(readFileSync(resolve(STUDY, cohort, 'protocol.json'), 'utf8'));
    return protocol.rows.filter((r: any) => Array.isArray(r.input.candidates)).map((r: any) => ({
      cohort, id: r.id as string, group: r.group as string, arm: r.arm as string,
      input: r.input as ChoiceInput, images: r.images as string[],
    }));
  });
}
export type VisualInput = ReturnType<typeof visualChoiceInputs>[number];
function references(row: VisualInput) {
  assert.ok(row.images.length === 0 || row.images.length === 4);
  return Object.fromEntries(MATCH_VIEWS.flatMap((view, i) => {
    if (!row.images.length) return [];
    const file = row.images[i + 1];
    assert.match(file, /^images\/[a-f0-9]{64}\.png$/);
    const bytes = readFileSync(resolve(STUDY, row.cohort, file));
    assert.equal(imageEvidence(bytes).hash, file.slice(7, -4));
    return [[view, bytes]];
  }));
}
export function freezeVisualChoice() {
  const inputs = visualChoiceInputs();
  for (const row of inputs) { choiceHypotheses(row.input); references(row); }
  const contract = { version: VISUAL_CHOICE_VERSION, sources: sourceHashes(), inputHash: digest(inputs),
    questions: inputs.length, sourceGroups: new Set(inputs.map(r => r.group)).size,
    views: MATCH_VIEWS, matching: 'Mean 1-blue-mask-IoU over top/front/side; minimum over legal base hypotheses per candidate.',
    tie: 'Abstain on equal best candidate scores; do not break ties by label.',
    noImage: 'Abstain without rendering; no hidden geometry or expected answers are loaded by the solver.',
    controls: 'Cyclic next-source image replacement on original/choice-rgb; report changes separately, not as valid task accuracy.',
    limits: ['Two canonical blue-on-gray parts, known BOM/candidates, nominal grid/support and minimum-corner origin.',
      'Uses the exact public renderer: algorithmic render-matching control, not a general VLM, human test or novel model.',
      'Designed after observing development failures. Existing 4+12 sources are development, not independent confirmation.',
      'Chroma masks omit neutral base/grid/text and title/footer. This is not OCR or learned segmentation.'] };
  const path = resolve(VISUAL_CHOICE_DIR, 'protocol.json');
  if (existsSync(path)) assert.deepEqual(JSON.parse(readFileSync(path, 'utf8')), contract);
  else atomicJson(path, contract);
  return contract;
}

export async function runVisualChoice(renderer: SuiteRenderer) {
  const protocol = freezeVisualChoice(), rows = visualChoiceInputs(), path = resolve(VISUAL_CHOICE_DIR, 'run.json');
  assert.ok(!existsSync(path), 'Preserve existing visual baseline run');
  mkdirSync(resolve(VISUAL_CHOICE_DIR, 'templates'), { recursive: true });
  const frames: Record<string, { image: string; frame: Parameters<SuiteRenderer['render']>[0] }> = {};
  const cache = new Map<string, Buffer>();
  const render = async (frame: Parameters<SuiteRenderer['render']>[0]) => {
    const hash = digest(frame);
    if (!cache.has(hash)) {
      const r = await renderer.render(frame);
      assert.equal(imageEvidence(r.buffer).hash, r.hash);
      const image = `templates/${r.hash}.png`;
      writeFileSync(resolve(VISUAL_CHOICE_DIR, image), r.buffer);
      cache.set(hash, r.buffer); frames[hash] = { image, frame };
    }
    return cache.get(hash)!;
  };
  const run = { version: VISUAL_CHOICE_VERSION, protocolHash: digest(protocol), status: 'running',
    rows: [] as any[], replacements: [] as any[], error: null as string | null, renders: 0, elapsedMs: 0 };
  const start = performance.now();
  const save = () => {
    run.renders = cache.size; run.elapsedMs = performance.now() - start;
    atomicJson(resolve(VISUAL_CHOICE_DIR, 'templates.json'), frames); atomicJson(path, run);
  };
  save();
  try {
    for (const row of rows) {
      const began = performance.now();
      const prediction = await solveVisualChoice(row.input, references(row), render);
      run.rows.push({ cohort: row.cohort, id: row.id, group: row.group, arm: row.arm,
        inputHash: digest(row), prediction, elapsedMs: performance.now() - began });
      save();
      console.log(JSON.stringify({ completed: run.rows.length, planned: rows.length, renders: cache.size }));
    }
    const originals = rows.filter(r => ['original', 'choice-rgb'].includes(r.arm));
    for (const [i, row] of originals.entries()) {
      const donor = originals[(i + 1) % originals.length];
      const prediction = await solveVisualChoice(row.input, references(donor), render);
      run.replacements.push({ cohort: row.cohort, id: row.id, donorCohort: donor.cohort, donorId: donor.id, prediction });
      save();
    }
    run.status = 'complete';
  } catch (error) { run.status = 'failed'; run.error = (error as Error).message; throw error; }
  finally { save(); }
  return { status: run.status, predictions: run.rows.length, replacements: run.replacements.length,
    renders: run.renders, elapsedMs: run.elapsedMs, apiRequests: 0 };
}

export async function replayVisualChoice() {
  const protocol = freezeVisualChoice(), rows = visualChoiceInputs();
  const run = JSON.parse(readFileSync(resolve(VISUAL_CHOICE_DIR, 'run.json'), 'utf8'));
  assert.equal(run.version, VISUAL_CHOICE_VERSION); assert.equal(run.protocolHash, digest(protocol));
  assert.equal(run.status, 'complete'); assert.equal(run.rows.length, rows.length);
  const frames = JSON.parse(readFileSync(resolve(VISUAL_CHOICE_DIR, 'templates.json'), 'utf8'));
  const cache = new Map<string, Buffer>();
  const render = async (frame: Parameters<SuiteRenderer['render']>[0]) => {
    const hash = digest(frame), item = frames[hash];
    assert.ok(item, 'Missing candidate render'); assert.deepEqual(item.frame, frame);
    assert.match(item.image, /^templates\/[a-f0-9]{64}\.png$/);
    if (!cache.has(hash)) {
      const bytes = readFileSync(resolve(VISUAL_CHOICE_DIR, item.image));
      assert.equal(imageEvidence(bytes).hash, item.image.slice(10, -4)); cache.set(hash, bytes);
    }
    return cache.get(hash)!;
  };
  for (const [i, row] of rows.entries()) {
    const result = run.rows[i];
    assert.equal(result.cohort, row.cohort); assert.equal(result.id, row.id);
    assert.equal(result.group, row.group); assert.equal(result.arm, row.arm);
    assert.equal(result.inputHash, digest(row));
    assert.deepEqual(await solveVisualChoice(row.input, references(row), render), result.prediction);
  }
  const originals = rows.filter(r => ['original', 'choice-rgb'].includes(r.arm));
  assert.equal(run.replacements.length, originals.length);
  for (const [i, row] of originals.entries()) {
    const donor = originals[(i + 1) % originals.length], result = run.replacements[i];
    assert.equal(result.cohort, row.cohort); assert.equal(result.id, row.id);
    assert.equal(result.donorCohort, donor.cohort); assert.equal(result.donorId, donor.id);
    assert.deepEqual(await solveVisualChoice(row.input, references(donor), render), result.prediction);
  }
  assert.equal(cache.size, run.renders); assert.equal(Object.keys(frames).length, cache.size);
  return { status: run.status, predictions: rows.length, replacements: originals.length, renders: cache.size,
    apiRequests: 0, limitation: 'Re-executes solver from public inputs and stored rendered templates; no fresh browser rasterization.' };
}
