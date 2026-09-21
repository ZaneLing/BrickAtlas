/** Current release verifier. Historical attestations stay in versioned evidence files. */
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
const root = resolve(import.meta.dirname, '../..'), data = resolve(root, 'benchmark/ldraw-v1');
const read = p => JSON.parse(readFileSync(p, 'utf8'));
const hash = p => createHash('sha256').update(readFileSync(p)).digest('hex');
const release = read(resolve(data, 'release.json')), verification = read(resolve(data, 'verification.json'));
assert.equal(release.version, 'brickatlas-ldraw-1');
assert.equal(release.models, 24); assert.equal(release.tasks, 617); assert.equal(release.parts, 15334);
assert.equal(verification.sources, release.models); assert.equal(verification.instances, release.parts);
assert.equal(verification.tasks, release.tasks);
assert.equal(verification.negativeControls, 1606);
assert.equal(release.measuredModelResults, 0);
const catalog = read(resolve(data, 'catalog.json'));
assert.deepEqual(read(resolve(root, 'public/benchmark/catalog.json')), catalog);
assert.deepEqual(read(resolve(root, 'public/benchmark/ldraw/catalog.json')), catalog);
assert.equal(existsSync(resolve(root, 'public/benchmark/models')), false, 'Synthetic models remain in the active site');
const capture = read(resolve(data, 'capture.json'));
assert.equal(capture.models.length, release.models);
for (const m of capture.models) {
  const entry = catalog.find(e => e.id === m.id);
  assert.equal(m.sourceHash, entry.sourceHash); assert.equal(m.loadedInstances, entry.parts);
  assert.equal(m.numberedRenderVersion, 2);
  assert.deepEqual(m.errors, []);
  for (const img of m.images) assert.equal(hash(resolve(root, 'benchmark/paper/figures/ldraw', img.file)), img.sha256);
}
const inputs = read(resolve(data, 'input-renders.json'));
const visualIds = new Set();
for (const entry of catalog) {
  const b = read(resolve(root, 'public/benchmark/ldraw/models', entry.id + '.json'));
  const input = read(resolve(root, 'public/benchmark/ldraw/inputs', entry.id + '.json'));
  assert.equal(b.parts.length, entry.parts); assert.equal(input.tasks.length, b.tasks.length);
  assert.equal(hash(resolve(root, 'public/benchmark/ldraw/sources', entry.id + '.mpd')), entry.sourceHash);
  assert.equal(b.audit.duplicatePlacements, 0);
  assert.ok(b.audit.connectorCoverage >= .9);
  for (const t of input.tasks) {
    assert.ok(!('answer' in t) && !('evidenceDetail' in t));
    if (t.modality === 'visual') {
      visualIds.add(t.id);
      assert.deepEqual(t.input, {});
      assert.ok(!('sourceModel' in t.visualInput));
      const image = inputs.images.find(r => r.taskId === t.id);
      assert.ok(image); assert.equal(image.renderVersion, 2); assert.deepEqual(image.references, t.references);
      assert.equal(hash(resolve(root, 'public', t.visualInput.numberedView)), image.sha256);
    }
  }
}
assert.equal(visualIds.size, 140); assert.equal(inputs.images.length, 140);
const worked = read(resolve(data, 'worked-renders.json'));
assert.equal(worked.frames.length, 6);
for (const f of worked.frames) assert.equal(hash(resolve(root, 'benchmark/paper/figures/ldraw', f.file)), f.sha256);
const derivatives = read(resolve(data, 'figure-derivatives.json'));
for (const image of derivatives.images) {
  assert.equal(hash(resolve(root, 'benchmark/paper/figures/ldraw', image.source)), image.sourceSha256);
  assert.equal(hash(resolve(root, 'benchmark/paper/figures/ldraw', image.file)), image.sha256);
}
const paper = resolve(root, 'benchmark/paper');
const publication = read(resolve(paper, 'ldraw-publication.json'));
assert.equal(hash(resolve(root, publication.generator)), publication.generatorSha256);
for (const [p, digest] of Object.entries(publication.inputs)) assert.equal(hash(resolve(root, p)), digest);
for (const plot of publication.plots) {
  for (const [ext, digest] of Object.entries(plot.files)) assert.equal(hash(resolve(paper, 'analysis', plot.name + '.' + ext)), digest);
}
assert.equal(publication.plots.length, 4);
for (const [file, digest] of Object.entries(publication.analysisFiles)) assert.equal(hash(resolve(paper, 'analysis', file)), digest);
const plan = read(resolve(paper, 'ldraw-experiments.json'));
assert.equal(hash(resolve(paper, 'ldraw-experiments.json')), publication.experimentPlanSha256);
assert.equal(plan.status, 'proposed-not-run');
assert.equal(plan.tables.length, 9);
let blankCells = 0;
for (const table of plan.tables) {
  const source = readFileSync(resolve(paper, `ldraw-plan-${table.id}.tex`), 'utf8');
  const rows = source.split('\\midrule\n')[1].split('\\bottomrule')[0].trim().split('\n');
  assert.equal(rows.length, table.rows.length);
  for (let i = 0; i < table.rows.length; i++) {
    const row = table.rows[i];
    assert.deepEqual(Object.keys(row.results), table.metrics);
    assert.ok(Object.values(row.results).every(v => v === null), 'Unrun numeric result is not null');
    const cells = rows[i].replace(/\\\\$/, '').split('&');
    assert.equal(cells.length, table.descriptors.length + table.metrics.length);
    assert.ok(cells.slice(table.descriptors.length).every(c => c.trim() === ''), 'Unrun table result cell is not blank');
    blankCells += table.metrics.length;
  }
}
assert.equal(blankCells, publication.prospectiveResultCells);
const publicationRenders = read(resolve(data, 'publication-renders.json'));
assert.equal(publicationRenders.frames.length, 9);
assert.equal(publicationRenders.sourceHash, catalog.find(m => m.id === 'omr-42102').sourceHash);
assert.deepEqual(publicationRenders.frames.map(f => f.snapshot.visibleInstances), [3, 5, 8, 10, 12, 14, 128, 129, 128]);
for (const f of publicationRenders.frames) {
  assert.equal(hash(resolve(paper, 'figures/ldraw', f.file)), f.sha256);
  assert.ok(f.snapshot.offsets.every(v => v.every(n => n === 0)), 'Publication capture moved a source instance');
}
for (const group of [publicationRenders.frames.slice(0, 6), publicationRenders.frames.slice(6)]) {
  for (const f of group) for (const key of ['camera', 'target'])
    assert.ok(f.snapshot[key].every((v, i) => Math.abs(v - group[0].snapshot[key][i]) <= .05),
      `Camera framing differs for ${f.file}`);
}
const cases = readFileSync(resolve(paper, 'ldraw-cases.tex'), 'utf8');
assert.equal((cases.match(/\\item \\textbf/g) ?? []).length, 617);
assert.equal((cases.match(/\\textit\{Options:\}/g) ?? []).length, 542);
assert.equal((cases.match(/\\textit\{Reference output:\}/g) ?? []).length, 617);
for (const name of ['main', 'supplement']) {
  const source = readFileSync(resolve(paper, name + '.tex'), 'utf8');
  assert.ok(!/[\u3400-\u4dbf\u4e00-\u9fff]/u.test(source));
  for (const block of source.matchAll(/\\begin\{figure\*?\}([\s\S]*?)\\end\{figure\*?\}/g))
    assert.ok(!block[1].includes('\\caption'), 'Caption beneath a figure');
}
const browserTests = read(resolve(data, 'browser-tests.json'));
assert.equal(browserTests.stats.expected, 3); assert.equal(browserTests.stats.unexpected, 0);
assert.equal(browserTests.stats.flaky, 0);
for (const name of ['main', 'supplement']) {
  const report = read(resolve(root, 'benchmark/paper', name === 'main' ? 'pdf-verification.json' : 'supplement-verification.json'));
  assert.equal(hash(resolve(root, 'benchmark/paper', name + '.pdf')), report.pdfSha256);
  assert.equal(hash(resolve(root, 'public/benchmark/docs', name + '.pdf')), report.pdfSha256);
  assert.equal(report.cjkTextFound, false);
  assert.equal(report.overfullBoxes, false);
  assert.equal(report.unresolvedCitationsOrReferences, false);
  assert.equal(report.figureCaptionsAbsent, true);
  assert.equal(report.vectorPlotSourceFiles.length, 4);
}
const files = [
  'benchmark/suite/ldraw/release.ts', 'benchmark/suite/ldraw/questions.ts', 'benchmark/suite/ldraw/verify.ts',
  'benchmark/suite/ldraw/audit.py', 'src/benchmark/LDrawBenchmarkPage.tsx', 'src/benchmark/NumberedOverlay.ts',
  'src/benchmark/ldrawTypes.ts', 'src/benchmark/ldrawReviewStore.ts', 'src/workers/geometry.worker.ts',
  'src/scene/AtlasScene.ts', 'src/benchmark/engine.ts', 'benchmark/paper/main.tex', 'benchmark/paper/supplement.tex',
  'benchmark/ldraw-v1/release.json', 'benchmark/ldraw-v1/verification.json', 'benchmark/ldraw-v1/capture.json',
  'benchmark/ldraw-v1/input-renders.json', 'benchmark/ldraw-v1/figure-derivatives.json',
  'benchmark/ldraw-v1/browser-tests.json', 'benchmark/ldraw-v1/tool-evidence.json',
  'benchmark/suite/ldraw/paper.py', 'benchmark/suite/ldraw/score.ts',
  'benchmark/suite/ldraw/publication.py', 'benchmark/suite/ldraw/capture-publication.ts',
  'benchmark/paper/ldraw-publication.json', 'benchmark/paper/ldraw-experiments.json',
  'benchmark/paper/ldraw-operators.tex', 'benchmark/paper/ldraw-step-trace.tex',
  'benchmark/ldraw-v1/publication-renders.json',
];
const evidence = { version: release.version, models: release.models, parts: release.parts, tasks: release.tasks,
  visualInputs: visualIds.size, canonicalViews: capture.models.length * 4, workedFrames: worked.frames.length,
  publicationFrames: publicationRenders.frames.length, vectorPlots: publication.plots.length, unrunResultCells: blankCells,
  hashes: Object.fromEntries(files.map(p => [p, hash(resolve(root, p))])) };
writeFileSync(resolve(root, 'benchmark/paper/ldraw-evidence.json'), JSON.stringify(evidence, null, 2) + '\n');
console.log(JSON.stringify({ ...evidence, hashes: undefined }));
