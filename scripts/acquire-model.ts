import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { hash } from './ldraw';
import { modelCatalog } from '../atlas.config';

const resources = [
  ...modelCatalog.map(model => ({ file: model.sourceFile, url: model.downloadUrl!, sha256: model.sourceHash })),
  {
    file: 'assets-source/ldraw-library/complete.zip',
    url: 'https://library.ldraw.org/library/updates/complete.zip',
    sha256: 'd2a695868ed2b3957c45b022a6451908edab22cc043179dd61d18dd382b35e11',
  },
];

await mkdir('assets-source/ldraw-library', { recursive: true });
await mkdir('assets-source/set-original', { recursive: true });
await mkdir('assets-source/license', { recursive: true });
for (const resource of resources) {
  if (!existsSync(resource.file)) {
    execFileSync('curl', ['-fL', '--retry', '2', '--max-time', '240', resource.url, '-o', resource.file], { stdio: 'inherit' });
  }
  const actual = hash(await readFile(resource.file));
  if (actual !== resource.sha256) throw new Error(`Source changed: ${resource.file}. Expected ${resource.sha256}, got ${actual}. Re-lock explicitly; do not silently update.`);
  console.log(`Verified ${resource.file}`);
}
const provenance = {
  acquiredAt: '2026-09-08',
  model: { title: 'Brick Atlas model catalog', author: 'Per-model authors in atlas.config.ts', license: 'CC BY 2.0', page: 'https://library.ldraw.org/omr/sets' },
  library: { version: 'complete.zip snapshot 2026-08-31', policy: 'Each file license is checked; originals and HISTORY are retained.' },
  resources,
  changes: ['Dependency closure packed without modifying original files', 'Geometry converted to millimetres (+Y up)', 'Deterministic instance metadata and editorial functional groups', 'Geometry batching and lossless gzip; no decimation'],
};
await writeFile('assets-source/provenance.json', JSON.stringify(provenance, null, 2) + '\n');
const pages = [
  ['model-page.html', provenance.model.page],
  ['omr-policy.html', 'https://www.ldraw.org/docs-main/official-model-repository-omr/rules-and-procedures-for-the-official-model-repository.html'],
];
for (const [file, url] of pages) {
  const target = `assets-source/license/${file}`;
  if (!existsSync(target)) execFileSync('curl', ['-fLs', '--retry', '2', '--max-time', '60', url, '-o', target]);
}
console.log('Source lock and license snapshots ready.');
