import { readFile, writeFile } from 'node:fs/promises';
import { modelCatalog } from '../atlas.config';
import type { AtlasManifest } from '../src/model/types';

const summaries = Object.fromEntries(await Promise.all(modelCatalog.map(async model => {
  const manifest = JSON.parse(await readFile(`public/models/${model.id}/manifest.json`, 'utf8')) as AtlasManifest;
  if (manifest.model.id !== model.id || manifest.sourceHash !== model.sourceHash) throw new Error(`Catalog source mismatch: ${model.id}`);
  return [model.id, {
    stats: manifest.stats,
    treeNodes: manifest.submodels.length + manifest.groups.length,
    steps: manifest.instructions?.steps.length ?? 0,
    provenance: manifest.instructions?.provenance ?? 'editorial',
  }];
})));
const output = `${JSON.stringify(summaries)}\n`;
await writeFile('public/models/catalog.json', output);
console.log(`Catalog: ${modelCatalog.length} models, ${Buffer.byteLength(output)} bytes`);
