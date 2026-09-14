import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const read = path => JSON.parse(readFileSync(resolve(here, path), 'utf8'));
const sha = path => createHash('sha256').update(readFileSync(resolve(here, path))).digest('hex');
const figures = read('figure-evidence.json'), audit = read('audit-evidence.json');
assert.equal(sha('generate-figures.py'), figures.generatorSha256);
assert.equal(sha('generate-audit.mjs'), audit.generatorSha256);
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
for (const paper of ['main', 'supplement']) {
  const report = read(paper === 'main' ? 'pdf-verification.json' : 'supplement-verification.json');
  assert.equal(sha(paper + '.pdf'), report.pdfSha256, 'Stale PDF check');
  assert.equal(report.overfullBoxes, false);
  assert.equal(report.unresolvedCitationsOrReferences, false);
}
assert.ok(read('pdf-verification.json').mainContentPageUpperBound <= 8);
console.log(JSON.stringify({ verified: true, figures: figures.figures.length,
  plannedTables: plan.tables.length, unmeasuredCells: cells, mainContentPages: read('pdf-verification.json').mainContentPageUpperBound }));
