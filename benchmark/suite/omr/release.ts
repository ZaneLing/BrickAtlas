import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { omrCaseRegistry } from './registry';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '../../..');
const output = resolve(root, 'benchmark/omr-cases-v1');
const sha = (path: string) => createHash('sha256').update(readFileSync(path)).digest('hex');
const write = (name: string, value: unknown) =>
  writeFileSync(resolve(output, name), JSON.stringify(value, null, 2) + '\n');

export function releaseOmrCases() {
  mkdirSync(output, { recursive: true });
  const registry = omrCaseRegistry(root);
  write('manifest.json', registry);
  write('summary.json', registry.summary);
  const attribution = [
    '# OMR/LDraw Attribution',
    '',
    'All source files are preserved under `assets-source/set-original/` and released under the license recorded below.',
    'LDraw library dependencies retain their per-file authors and license records in each `public/models/<id>/credits.json`.',
    '',
    '| Model | Author / OMR author | License | Source |',
    '|---|---|---|---|',
    ...registry.wholeModels.map(c =>
      `| ${c.setNumber} ${c.title} | ${c.author.replaceAll('|', '\\|')} | ${c.license} | ${c.sourceUrl} |`),
    '',
  ].join('\n');
  writeFileSync(resolve(output, 'ATTRIBUTION.md'), attribution);
  const files = ['README.md', 'ATTRIBUTION.md', 'manifest.json', 'summary.json'];
  write('release-manifest.json', {
    version: registry.version,
    files: Object.fromEntries(files.map(name => [name, sha(resolve(output, name))])),
    sourceManifests: Object.fromEntries(registry.wholeModels.map(c => [
      c.sourceModelId,
      sha(resolve(root, `public/models/${c.sourceModelId}/manifest.json`)),
    ])),
  });
  console.log(JSON.stringify(registry.summary));
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url))) {
  releaseOmrCases();
}
