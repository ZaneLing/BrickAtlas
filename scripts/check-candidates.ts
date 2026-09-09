import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { LDrawLoader } from 'three/addons/loaders/LDrawLoader.js';
import { LDrawConditionalLineMaterial } from 'three/addons/materials/LDrawConditionalLineMaterial.js';
import type { Group } from 'three';
import { hash } from './ldraw';

const root = 'https://raw.githubusercontent.com/mrdoob/three.js/r180/examples/models/ldraw/officialLibrary/models/';
const samples = [
  { name: 'car', path: 'car.ldr_Packed.mpd', decision: 'Pipeline smoke test only; not an official release set.' },
  { name: 'radar-truck', path: '889-1-RadarTruck.mpd_Packed.mpd', decision: 'Valid small OMR-based example, rejected in favour of a larger vehicle with more submodels.' },
];
await mkdir('assets-source/candidates', { recursive: true });
const report = [];
for (const sample of samples) {
  const path = `assets-source/candidates/${sample.name}.mpd`;
  const url = root + sample.path;
  if (!existsSync(path)) execFileSync('curl', ['-fLs', '--max-time', '60', url, '-o', path]);
  const text = await readFile(path, 'utf8');
  const loader = new LDrawLoader();
  loader.setConditionalLineMaterial(LDrawConditionalLineMaterial);
  const model = await new Promise<Group>((resolve, reject) => loader.parse(text, resolve, reject));
  let instances = 0;
  function count(group: Group) {
    if (group.name.toLowerCase().endsWith('.dat')) { instances++; return; }
    for (const child of group.children) if ((child as Group).isGroup) count(child as Group);
  }
  count(model);
  report.push({
    name: sample.name, sourceUrl: url, sha256: hash(text), loaderAuthor: model.userData.author, instances,
    modelLicenseHeader: text.split(/^0 FILE /m)[0].match(/^0 !LICENSE (.+)$/m)?.[1]?.trim() ?? 'No explicit model license in preamble; not a release candidate',
    decision: sample.decision, warnings: 'These are technical reference fixtures; not served by the application.',
  });
}
report.push({
  name: '5867 Super Speedster', sourceUrl: 'https://library.ldraw.org/omr/sets/1431',
  sha256: hash(await readFile('assets-source/set-original/5867-1.mpd')), loaderAuthor: 'Takeshi Takahashi [RainbowDolphin]',
  instances: 278, modelLicenseHeader: 'Redistributable under CCAL version 2.0 : see CAreadme.txt',
  decision: 'Selected: 278 instances, 7 source submodels, license confirmed, all dependency headers validated.',
  warnings: 'No STEP metadata. See classification.json for editorial groups.',
});
await writeFile('assets-built/candidate-report.json', JSON.stringify(report, null, 2) + '\n');
console.log(report);
