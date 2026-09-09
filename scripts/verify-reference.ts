import { readFile, writeFile } from 'node:fs/promises';
import { strict as assert } from 'node:assert';
import { Box3, Matrix4, Vector3, type Group } from 'three';
import { LDrawLoader } from 'three/addons/loaders/LDrawLoader.js';
import { LDrawConditionalLineMaterial } from 'three/addons/materials/LDrawConditionalLineMaterial.js';
import { splitMpd, resolveFile } from './ldraw';
import type { AtlasManifest } from '../src/model/types';

const base = 'public/models/5867/';
const source = await readFile('assets-source/set-original/5867-1.mpd', 'utf8');
const manifest: AtlasManifest = JSON.parse(await readFile(`${base}manifest.json`, 'utf8'));
const files = splitMpd(await readFile(`${base}model.packed.mpd`, 'utf8'));
const colors = await readFile(`${base}LDConfig.ldr`, 'utf8');
const dependencies = [...files.values()].filter(f => f.name.endsWith('.dat'));
const loader = new LDrawLoader();
loader.setConditionalLineMaterial(LDrawConditionalLineMaterial);
const fileMap: Record<string, string> = {};
for (const file of files.values()) {
  for (const line of file.lines) {
    if (line.text.startsWith('1 ')) {
      const ref = line.text.split(/\s+/).slice(14).join(' ');
      fileMap[ref] = resolveFile(files, ref).name;
    }
  }
}
for (const file of dependencies) fileMap[file.name.replace(/^(parts|p)\//, '')] = file.name;
loader.setFileMap(fileMap);
// The original hierarchical MPD is loaded independently of the manifest flattener.
const root = await new Promise<Group>((resolve, reject) => loader.parse(
  source.replace(/\n/, `\n${colors}\n`) + '\n' + dependencies.map(f => `0 FILE ${f.name}\n${f.text}`).join('\n'), resolve, reject,
));
root.applyMatrix4(new Matrix4().makeScale(0.4, -0.4, -0.4));
root.updateMatrixWorld(true);
const remaining = new Set(manifest.instances.map(p => p.index));
let maximumMatrixError = 0, maximumBoundsError = 0;
function visit(group: Group) {
  if (group.name.toLowerCase().endsWith('.dat')) {
    const number = group.name.replace(/^parts\//, '').replace(/\.dat$/, '');
    const candidate = [...remaining].map(i => manifest.instances[i]).find(p => p.partNumber === number &&
      p.originalMatrix.every((n, i) => Math.abs(n - group.matrixWorld.elements[i]) < 0.001));
    assert(candidate, `Unmatched original instance: ${group.name}`);
    remaining.delete(candidate.index);
    maximumMatrixError = Math.max(maximumMatrixError, ...candidate.originalMatrix.map((n, i) => Math.abs(n - group.matrixWorld.elements[i])));
    const box = new Box3().setFromObject(group, true);
    const expected = new Box3(new Vector3(...candidate.bounds.min), new Vector3(...candidate.bounds.max));
    maximumBoundsError = Math.max(maximumBoundsError, box.min.distanceTo(expected.min), box.max.distanceTo(expected.max));
    return;
  }
  for (const child of group.children) if ((child as Group).isGroup) visit(child as Group);
}
visit(root);
assert.equal(remaining.size, 0);
assert(maximumBoundsError < 0.01, `Bounds mismatch: ${maximumBoundsError} mm`);
const report = {
  baseline: 'Unmodified hierarchical source MPD parsed by Three.js LDrawLoader',
  instancesCompared: manifest.instances.length,
  maximumMatrixError, maximumBoundsErrorMm: maximumBoundsError,
  result: 'pass',
  note: 'Independent from semantic flattening, but uses the same geometry library. External LDView/Safari/real-device manual checks remain separate.',
};
await writeFile('assets-built/reference-report.json', JSON.stringify(report, null, 2) + '\n');
console.log(report);
