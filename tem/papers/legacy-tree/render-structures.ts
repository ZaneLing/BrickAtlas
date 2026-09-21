import assert from 'node:assert/strict';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { chromium } from '@playwright/test';
import { PNG } from 'pngjs';
import { atomicJson } from '../core/budget';
import { dataset, POLICIES } from '../suite/v2/dataset';
import { caseSpecs, taskForV2 } from '../suite/v2/cases';
import { evaluateStrict } from '../suite/study/strict-evaluate';
import { heightPlan } from '../suite/study/algorithms';
import { publicAlgorithm } from '../suite/v2/baseline';
import { ambiguityCases, AMBIGUITY_DIR } from '../suite/study/ambiguity';
import { insertIssue } from '../suite/geometry';
import type { PaperFrame } from '../suite/web/paper-render';
import type { Part } from '../suite/shared';

const HERE = dirname(fileURLToPath(import.meta.url)), out = resolve(HERE, 'figures/structures');
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ headless: true, channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1000, height: 750 } });
const url = process.env.BRICKATLAS_URL ?? 'http://127.0.0.1:5175';
const images: any[] = [];
const sha = (b: Buffer) => createHash('sha256').update(b).digest('hex');
try {
  await page.goto(url + '/paper-render.html');
  await page.waitForFunction(() => typeof window.atlasPaperRender === 'function');
  async function render(name: string, frame: PaperFrame, metadata: Record<string, unknown> = {}) {
    const result = await page.evaluate(frame => window.atlasPaperRender(frame), frame);
    const bytes = Buffer.from(result.png.split(',')[1], 'base64'), decoded = PNG.sync.read(bytes);
    const pixels = decoded.data;
    let foreground = 0, edgeForeground = 0;
    for (let i = 0; i < pixels.length; i += 4) {
      if (pixels[i] < 245 || pixels[i + 1] < 245 || pixels[i + 2] < 245) {
        foreground++;
        const x = (i / 4) % decoded.width, y = Math.floor(i / 4 / decoded.width);
        if (x < 3 || x >= decoded.width - 3 || y < 3 || y >= decoded.height - 3) edgeForeground++;
      }
    }
    assert.ok(foreground > 1000 && foreground < decoded.width * decoded.height * .85, `Blank/unframed ${name}`);
    assert.equal(edgeForeground, 0, `Clipped ${name}`);
    writeFileSync(resolve(out, name + '.png'), bytes);
    images.push({ name, file: `figures/structures/${name}.png`, sha256: sha(bytes), frame, metadata,
      pixels: { foreground, edgeForeground, width: decoded.width, height: decoded.height } });
    return decoded;
  }
  const models = dataset(), specs = caseSpecs();
  for (const policy of POLICIES) {
    const pool = models.filter(m => m.policy === policy);
    const median = [...pool].sort((a, b) => a.structure.parts.length - b.structure.parts.length)[320].structure.parts.length;
    const chosen = pool.sort((a, b) => Math.abs(a.structure.parts.length - median) - Math.abs(b.structure.parts.length - median)
      || a.group.localeCompare(b.group))[0];
    await render(`gallery-${policy}`, { parts: chosen.structure.parts }, { group: chosen.group, policy, selection: 'median-size then group hash' });
  }
  const object = models.filter(m => m.policy === 'low-fan' && m.structure.parts.length >= 18 && m.structure.parts.length <= 22)
    .sort((a, b) => a.group.localeCompare(b.group))[0];
  const task = (kind: string, variant: string) => taskForV2(specs.find(s => s.group === object.group
    && s.kind === kind && s.variant === variant && ['ordinary', 'default'].includes(s.condition))!);
  const completion = task('complete', 'suffix'), rotation = task('edit', 'rotate'),
    repair = task('repair', 'shift'), recolor = task('edit', 'recolor'), reconstruction = task('reconstruct', 'full'),
    relation = task('relations', 'contact'), generation = task('generate', 'constraints');
  for (const t of [completion, rotation, repair, recolor, reconstruction, relation, generation]) {
    assert.equal(evaluateStrict(t, t.oracle).metrics.success, 1);
  }
  await render('reconstruct-input', { parts: reconstruction.target.parts }, { caseId: reconstruction.spec.id, role: 'illustrated RGB input' });
  await render('reconstruct-gt', { parts: reconstruction.target.parts, explode: 1.3 }, { caseId: reconstruction.spec.id, role: 'ground truth, display-only exploded by bottom layer' });
  await render('complete-input', { parts: completion.source!.parts, frameParts: completion.target.parts }, { caseId: completion.spec.id, role: 'current prefix' });
  await render('complete-gt', { parts: completion.target.parts, highlightIds: completion.changedIds }, { caseId: completion.spec.id, role: 'ground truth, additions outlined' });
  await render('edit-input', { parts: rotation.source!.parts }, { caseId: rotation.spec.id, role: 'current' });
  await render('edit-gt', { parts: rotation.target.parts }, { caseId: rotation.spec.id, role: 'rotated ground truth' });
  await render('repair-input', { parts: repair.source!.parts, frameParts: [...repair.source!.parts, ...repair.target.parts], highlightIds: repair.changedIds },
    { caseId: repair.spec.id, role: 'shift fault outlined' });
  await render('repair-gt', { parts: repair.target.parts, frameParts: [...repair.source!.parts, ...repair.target.parts], highlightIds: repair.changedIds },
    { caseId: repair.spec.id, role: 'restored ground truth' });
  await render('relation', { parts: relation.target.parts, highlightIds: [String(relation.public.input.a), String(relation.public.input.b)] },
    { caseId: relation.spec.id, oracle: relation.oracle, role: 'symbolic query illustrated; queried parts outlined' });
  await render('generation', { parts: generation.target.parts }, { caseId: generation.spec.id, constraints: generation.public.input.requirements, role: 'one satisfying witness, not a unique answer' });
  await render('recolor-gt', { parts: recolor.target.parts }, { caseId: recolor.spec.id, operation: recolor.public.input.operation, role: 'recolored ground truth' });
  const part = reconstruction.target.parts.find(p => p.partId !== '3035')!;
  await render('recognition', { parts: [{ ...part, x: 0, y: 0, z: 0 }] }, { role: 'catalog recognition exemplar', partId: part.partId });

  const planning = specs.filter(s => s.kind === 'plan' && s.variant === 'assemble' && s.difficulty === 'medium'
    && s.policy === 'two-support-bridge')
    .sort((a, b) => a.id.localeCompare(b.id));
  const failed = planning.map(s => {
    const t = taskForV2(s), greedy = publicAlgorithm(t.public) as { order: string[] };
    return { t, greedy };
  }).find(({ t, greedy }) => greedy.order.length < t.target.parts.length)!;
  const t = failed.t, ordered = (heightPlan(t.public) as { order: string[] }).order;
  assert.equal(evaluateStrict(t, { order: ordered }).metrics.success, 1);
  const n = ordered.length;
  let previous = 0;
  for (const [i, fraction] of [.25, .5, .75, 1].entries()) {
    const count = Math.ceil(n * fraction), ids = ordered.slice(0, count);
    const verdict = evaluateStrict(t, { order: ids });
    assert.equal(verdict.diagnostics.firstInvalidStep, null);
    await render(`step-${i + 1}`, { parts: ids.map(id => t.target.parts.find(p => p.id === id)!),
      frameParts: t.target.parts, highlightIds: ids.slice(previous) },
    { caseId: t.spec.id, prefix: ids, count, total: n, legalPrefix: verdict.metrics.legalPrefix });
    previous = count;
  }
  const current = failed.greedy.order.map(id => t.target.parts.find(p => p.id === id)!);
  const remaining = t.target.parts.find(p => !failed.greedy.order.includes(p.id))!;
  assert.ok(insertIssue(current, remaining));
  const rejected = evaluateStrict(t, { order: [...failed.greedy.order, remaining.id] });
  assert.equal(rejected.diagnostics.firstInvalidStep, failed.greedy.order.length);
  await render('step-blocked', { parts: current, frameParts: t.target.parts, explode: .8 }, { caseId: t.spec.id, order: failed.greedy.order,
    attemptedId: remaining.id, issue: insertIssue(current, remaining), rejection: rejected.diagnostics });
  await render('step-target', { parts: t.target.parts, explode: .8, highlightIds: [remaining.id] },
    { caseId: t.spec.id, role: 'exploded target showing the missing blocked piece; display-only layer offsets' });

  const ambiguity = ambiguityCases(), first = ambiguity.families[0];
  for (const [i, s] of first.structures.entries()) {
    await render(`hidden-exterior-${i}`, { parts: s.parts }, { group: first.group, role: 'sealed exterior' });
    await render(`hidden-exploded-${i}`, { parts: s.parts.filter((p: Part) => p.color !== 'gray' || p.id === 'floor' || p.id === 'roof'),
      frameParts: s.parts, explode: 1.5, highlightIds: ['probe0-1', 'probe1-1', ...s.parts.filter((p: Part) => p.color === 'red').map((p: Part) => p.id)] },
      { group: first.group, role: 'disclosed ground truth; side walls omitted and display-only layer offsets; queried blue pair outlined' });
  }
  const pixelChecks: any[] = [];
  // New presentation renderer only: this does not certify equality under arbitrary renderers.
  for (const family of ambiguity.families) for (const view of ['iso', 'top', 'front', 'side'] as const) {
    let reference: PNG | undefined;
    for (const [i, s] of family.structures.entries()) {
      const result = await page.evaluate(frame => window.atlasPaperRender(frame), { parts: s.parts, view });
      const pixels = PNG.sync.read(Buffer.from(result.png.split(',')[1], 'base64'));
      if (!reference) reference = pixels;
      let changed = 0, maximum = 0;
      for (let k = 0; k < pixels.data.length; k += 4) {
        const delta = Math.max(...[0, 1, 2].map(c => Math.abs(pixels.data[k + c] - reference!.data[k + c])));
        if (delta) changed++; maximum = Math.max(maximum, delta);
      }
      pixelChecks.push({ group: family.group, layout: i, view, changedPixels: changed, maximumChannelDifference: maximum,
        pixelSha256: sha(pixels.data) });
    }
  }
  const sources = Object.fromEntries(['render-structures.ts', '../suite/web/paper-render.ts', '../suite/study/ambiguity.ts'].map(p =>
    [p, sha(readFileSync(resolve(HERE, p)))]));
  const manifest = { version: 'paper-structures-1', images, sources, selectedTaskGroup: object.group,
    provenance: 'All shapes are actual v2 targets/sources or verified finite-grammar witnesses. Exploded views are display-only, never model observations.',
    apiRequests: 0, pixelChecks, totalRenders: images.length + pixelChecks.length };
  writeFileSync(resolve(HERE, 'structure-evidence.json'), JSON.stringify(manifest, null, 2) + '\n');
  atomicJson(resolve(AMBIGUITY_DIR, 'render-verification.json'), {
    renderer: 'paper-render-1', sourceHashes: sources, comparisons: pixelChecks.length,
    allPixelIdentical: pixelChecks.every(r => r.changedPixels === 0), maxChangedPixels: Math.max(...pixelChecks.map(r => r.changedPixels)),
    rows: pixelChecks, scope: 'Same fixed cameras, renderer and GPU; not human calibration or arbitrary renderer equivalence.' });
  console.log(JSON.stringify({ images: images.length, comparisons: pixelChecks.length,
    identical: pixelChecks.every(r => r.changedPixels === 0), maxChangedPixels: Math.max(...pixelChecks.map(r => r.changedPixels)) }));
} finally { await browser.close(); }
