import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url)), root = resolve(here, '../challenge-cases');
const sha = (path: string) => createHash('sha256').update(readFileSync(path)).digest('hex');
const manifest = JSON.parse(readFileSync(resolve(root, 'manifest.json'), 'utf8'));
const figures = JSON.parse(readFileSync(resolve(root, 'figure-evidence.json'), 'utf8'));
assert.equal(manifest.version, 'brickatlas-challenge-casebank-1');
assert.equal(manifest.models.length, 6);
assert.equal(manifest.tasks.length, 12);
assert.equal(manifest.totals.placedPartInstances, 329);
assert.equal(figures.manifestSha256, sha(resolve(root, 'manifest.json')));
for (const file of manifest.files) assert.equal(sha(resolve(root, file.path)), file.sha256, file.path);
for (const [path, hash] of Object.entries(figures.outputs)) assert.equal(sha(resolve(root, path)), hash, path);
for (const [path, hash] of Object.entries(figures.paperOutputs)) {
  assert.equal(sha(resolve(here, 'figures', path)), hash, path);
}

const tex = (value: unknown) => String(value).replaceAll('_', '\\_').replaceAll('&', '\\&');
writeFileSync(resolve(here, 'tables/challenge-models.tex'),
  '% Generated from challenge-cases/manifest.json; do not edit.\n'
  + manifest.models.map((model: any) =>
    `${tex(model.name)} & ${model.tier} & ${model.domain} & ${model.parts} & ${tex(model.capabilityPressure.join('; '))} \\\\`)
    .join('\n') + '\n');
writeFileSync(resolve(here, 'tables/challenge-tasks.tex'),
  '% Generated from challenge-cases/manifest.json; do not edit.\n'
  + manifest.tasks.map((task: any) => {
    const model = manifest.models.find((item: any) => item.id === task.sourceId);
    return `${tex(task.kind)} & ${tex(model.name)} & ${model.parts} & \\unmeasured \\\\`;
  }).join('\n') + '\n');

writeFileSync(resolve(here, 'challenge-evidence.json'), JSON.stringify({
  version: manifest.version,
  models: manifest.models.length,
  tasks: manifest.tasks.length,
  placedPartInstances: manifest.totals.placedPartInstances,
  minParts: manifest.totals.minParts,
  maxParts: manifest.totals.maxParts,
  manifestSha256: sha(resolve(root, 'manifest.json')),
  figureEvidenceSha256: sha(resolve(root, 'figure-evidence.json')),
  generatorSha256: sha(fileURLToPath(import.meta.url)),
  files: manifest.files.length,
  paperFigures: figures.paperOutputs,
  measuredModelResults: 0,
  scope: 'Advanced stress-test layer. Oracle validation is complete; model evaluation is not yet run.',
}, null, 2) + '\n');
console.log(JSON.stringify(manifest.totals));
