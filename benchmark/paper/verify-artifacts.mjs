import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import './verify-hierarchy3.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const read = path => JSON.parse(readFileSync(resolve(here, path), 'utf8'));
const sha = path => createHash('sha256').update(readFileSync(resolve(here, path))).digest('hex');
const figures = read('figure-evidence.json'), audit = read('audit-evidence.json');
const curated = read('curated-evidence.json');
const challenge = read('challenge-evidence.json');
const constructibility = read('constructibility-evidence.json');
const mechanism = read('mechanism-evidence.json');
assert.equal(sha('generate-figures.py'), figures.generatorSha256);
assert.equal(sha('generate-audit.mjs'), audit.generatorSha256);
assert.equal(sha('generate-curated.ts'), curated.generatorSha256);
assert.equal(sha('../curated-cases/manifest.json'), curated.manifestSha256);
assert.equal(sha('../curated-cases/contact-sheet-evidence.json'), curated.contactSheetEvidenceSha256);
const curatedManifest = read('../curated-cases/manifest.json');
assert.equal(curatedManifest.models.length, 12); assert.equal(curatedManifest.tasks.length, 8);
for (const file of curatedManifest.files) assert.equal(sha('../curated-cases/' + file.path), file.sha256, file.path);
for (const [path, hash] of Object.entries(curated.paperFigures)) assert.equal(sha('figures/' + path), hash, path);
assert.equal(sha('generate-challenge.ts'), challenge.generatorSha256);
assert.equal(sha('../challenge-cases-v2/manifest.json'), challenge.manifestSha256);
assert.equal(sha('../challenge-cases-v2/figure-evidence.json'), challenge.figureEvidenceSha256);
const challengeManifest = read('../challenge-cases-v2/manifest.json');
assert.equal(challengeManifest.version, 'brickatlas-challenge-casebank-2');
for (const [path, hash] of Object.entries(challengeManifest.sourceHashes)) {
  const text = readFileSync(resolve(here, '../suite', path), 'utf8');
  assert.equal(createHash('sha256').update(text).digest('hex'), hash, path);
}
assert.equal(challengeManifest.models.length, 6); assert.equal(challengeManifest.tasks.length, 12);
assert.equal(challengeManifest.totals.placedPartInstances, 329);
for (const file of challengeManifest.files) assert.equal(sha('../challenge-cases-v2/' + file.path), file.sha256, file.path);
for (const [path, hash] of Object.entries(challenge.paperFigures)) assert.equal(sha('figures/' + path), hash, path);
assert.equal(challenge.measuredModelResults, 0);
assert.equal(constructibility.version, 'brickatlas-constructibility-1');
assert.equal(constructibility.sourceGroups, 6);
assert.equal(constructibility.records, 78);
assert.equal(sha('generate-constructibility.mjs'), constructibility.generatorSha256);
assert.equal(sha('../constructibility-v1/public.json'), constructibility.publicSha256);
assert.equal(sha('../constructibility-v1/audit.json'), constructibility.auditSha256);
assert.equal(sha('../constructibility-v1/frozen-protocol.json'), constructibility.protocolSha256);
assert.equal(sha('../constructibility-v1/algorithm-results.json'), constructibility.algorithmResultsSha256);
assert.equal(read('../constructibility-v1/algorithm-results.json').filter(row => row.result.success === 1).length, 78);
assert.equal(mechanism.version, 'brickatlas-mechanism-1');
assert.equal(mechanism.models, 6);
assert.equal(mechanism.tasks, 48);
assert.equal(mechanism.apiRun.requests, 96);
assert.equal(sha('generate-mechanism.mjs'), mechanism.hashes.generator);
assert.equal(sha('../mechanism-v1/audit.json'), mechanism.hashes.audit);
assert.equal(sha('../mechanism-v1/models.json'), mechanism.hashes.models);
assert.equal(sha('../mechanism-v1/public.json'), mechanism.hashes.public);
assert.equal(sha('../mechanism-v1/results/local-qwen3-0.6b.scores.json'), mechanism.hashes.localScores);
assert.equal(sha('../mechanism-v1/results/' + read('../mechanism-v1/results/latest.json').path), mechanism.hashes.apiRun);
assert.equal(sha('figures/mechanism-models.pdf'), mechanism.hashes.modelFigure);
assert.equal(sha('figures/mechanism-tasks.pdf'), mechanism.hashes.taskFigure);
assert.equal(figures.figures.length, 5);
for (const [path, hash] of Object.entries(figures.sourcesSha256)) assert.equal(sha('../' + path), hash, path);
for (const [path, hash] of Object.entries(figures.outputSha256)) assert.equal(sha('figures/' + path), hash, path);
assert.equal(sha(audit.audit.path), audit.audit.sha256);
assert.equal(sha('experiments.json'), audit.experimentPlanSha256);
const plan = read('experiments.json');
assert.equal(plan.status, 'proposed-not-frozen');
let cells = 0;
for (const table of plan.tables) {
  const tex = readFileSync(resolve(here, 'tables/planned-' + table.id + '.tex'), 'utf8');
  const expected = table.rows.length * table.columns.length;
  assert.equal((tex.match(/\\unmeasured/g) ?? []).length, expected);
  assert.ok(table.rows.every(r => r.values.length === table.columns.length && r.values.every(v => v === null)));
  cells += expected;
}
assert.equal(cells, audit.unmeasuredCells);
const expanded = read('expanded-evidence.json'), structures = read('structure-evidence.json');
const plates = read('structure-figure-evidence.json');
assert.equal(expanded.models, 8);
assert.equal(expanded.newCalls, 156);
assert.equal(expanded.ambiguityCases, 600);
assert.equal(expanded.allPixelIdentical, true);
assert.equal(sha('generate-expanded.ts'), expanded.generatorHash);
for (const [path, hash] of Object.entries(expanded.sourceHashes)) assert.equal(sha('../suite/artifacts/study/' + path), hash, path);
for (const [path, hash] of Object.entries(structures.sources)) assert.equal(sha(path), hash, path);
for (const image of structures.images) {
  assert.equal(sha(image.file), image.sha256, image.file);
  assert.ok(image.pixels.foreground > 1000 && image.pixels.edgeForeground === 0);
}
assert.equal(structures.images.length, 30);
assert.equal(sha('compose-structures.py'), plates.generatorSha256);
assert.equal(sha('structure-evidence.json'), plates.renderManifestSha256);
for (const [path, hash] of Object.entries(plates.outputSha256)) assert.equal(sha('figures/' + path), hash, path);
for (const paper of ['main', 'supplement']) {
  const report = read(paper === 'main' ? 'pdf-verification.json' : 'supplement-verification.json');
  assert.equal(sha(paper + '.pdf'), report.pdfSha256, 'Stale PDF check');
  assert.equal(report.overfullBoxes, false);
  assert.equal(report.unresolvedCitationsOrReferences, false);
}
assert.ok(read('pdf-verification.json').mainContentPageUpperBound <= 8);
console.log(JSON.stringify({ verified: true, figures: figures.figures.length + plates.figures.length
    + Object.keys(curated.paperFigures).length + Object.keys(challenge.paperFigures).length,
  curatedModels: curated.models, curatedTasks: curated.tasks, curatedFiles: curated.files, renders3D: structures.images.length,
  challengeModels: challenge.models, challengeTasks: challenge.tasks, challengeParts: challenge.placedPartInstances,
  constructibilityCases: constructibility.records,
  mechanismModels: mechanism.models, mechanismTasks: mechanism.tasks,
  models: expanded.models, newCalls: expanded.newCalls, ambiguityCases: expanded.ambiguityCases,
  plannedTables: plan.tables.length, unmeasuredCells: cells, mainContentPages: read('pdf-verification.json').mainContentPageUpperBound }));
