import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url)), root = resolve(here, '../curated-cases');
const sha = (path: string) => createHash('sha256').update(readFileSync(path)).digest('hex');
const manifest = JSON.parse(readFileSync(resolve(root, 'manifest.json'), 'utf8'));
const figures = JSON.parse(readFileSync(resolve(root, 'contact-sheet-evidence.json'), 'utf8'));
assert.equal(manifest.version, 'brickatlas-curated-casebank-1');
assert.equal(manifest.models.length, 12); assert.equal(manifest.tasks.length, 8);
assert.equal(figures.manifestSha256, sha(resolve(root, 'manifest.json')));
for (const [path, hash] of Object.entries(figures.outputs)) assert.equal(sha(resolve(root, path)), hash);
for (const [path, hash] of Object.entries(figures.paperOutputs)) assert.equal(sha(resolve(here, 'figures', path)), hash);
const tex = (s: unknown) => String(s).replaceAll('_', '\\_').replaceAll('&', '\\&');
const rows = manifest.models.map((m: any) =>
  `${tex(m.name)} & ${m.difficulty} & ${m.style} & ${m.parts} & ${m.colors} & ${m.occupiedLevels} & ${m.occlusion} / ${m.supportReasoning} \\\\`);
writeFileSync(resolve(here, 'tables/curated-cases.tex'),
  '% Generated from curated-cases/manifest.json; do not edit.\n' + rows.join('\n') + '\n');
const source = readFileSync(fileURLToPath(import.meta.url));
writeFileSync(resolve(here, 'curated-evidence.json'), JSON.stringify({
  version: manifest.version, models: 12, tasks: 8,
  difficulty: Object.fromEntries(['easy', 'medium', 'hard'].map(d => [d, manifest.models.filter((m: any) => m.difficulty === d).length])),
  manifestSha256: sha(resolve(root, 'manifest.json')),
  contactSheetEvidenceSha256: sha(resolve(root, 'contact-sheet-evidence.json')),
  generatorSha256: createHash('sha256').update(source).digest('hex'),
  files: manifest.files.length,
  paperFigures: figures.paperOutputs,
  scope: 'Original explicitly authored qualitative/calibration structures; not pooled with the v2 population or model results.',
}, null, 2) + '\n');
console.log(JSON.stringify({ models: 12, tasks: 8, files: manifest.files.length }));
