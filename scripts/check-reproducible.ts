import { readFile, writeFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { hash } from './ldraw';
import { atlasConfig } from '../atlas.config';

const base = `public/models/${atlasConfig.id}/`;
async function fingerprints() {
  const manifest = JSON.parse(await readFile(base + 'manifest.json', 'utf8'));
  const names = ['manifest.json', 'model.packed.mpd', 'credits.json', 'provenance.json', 'attribution.txt', 'build-report.json', ...manifest.chunks.map((c: { url: string }) => c.url)];
  return Object.fromEntries(await Promise.all(names.map(async name => [name, hash(await readFile(base + name))])));
}
const before = await fingerprints();
execFileSync(process.execPath, ['node_modules/tsx/dist/cli.mjs', 'scripts/build-assets.ts', '--offline'], { stdio: 'pipe' });
const after = await fingerprints();
if (JSON.stringify(before) !== JSON.stringify(after)) throw new Error('Offline rebuild was not byte-identical');
const report = { result: 'pass', method: 'Rebuild using only the checked-in dependency subset, without reading complete.zip or accessing the network', files: after };
await writeFile('assets-built/reproducibility-report.json', JSON.stringify(report, null, 2) + '\n');
console.log(`PASS: ${Object.keys(after).length} artifacts reproduced byte-for-byte from the locked offline subset.`);
