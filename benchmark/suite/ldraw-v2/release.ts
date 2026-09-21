import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync, copyFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import type { AtlasManifest } from '../../../src/model/types';
import type { LDrawBundle } from '../../../src/benchmark/ldrawTypes';
import type { InternalBundle } from './types';
import { generateQuestions, finalizeQuestions } from './questions';
import { root, data, site, publicTask, hash, serializeModelRequest } from './publish';
import { score } from './score';

const read = (p: string) => JSON.parse(readFileSync(p, 'utf8'));
const write = (p: string, v: unknown) => { mkdirSync(resolve(p, '..'), { recursive: true }); writeFileSync(p, JSON.stringify(v, null, 2) + '\n'); };
execFileSync('python3', [resolve(import.meta.dirname, 'freeze.py'), '--verify']);
assert.equal(read(resolve(data, 'phase-0-checks.json')).status, 'passed', 'Phase 0 required');
const catalog = read(resolve(root, 'benchmark/ldraw-v1/catalog.json'));
const bundles: InternalBundle[] = catalog.map((entry: any) => {
  const v1: LDrawBundle = read(resolve(root, 'public/benchmark/ldraw/models', `${entry.id}.json`));
  const manifest: AtlasManifest = read(resolve(root, 'public/models', entry.id, 'manifest.json'));
  assert.equal(hash(readFileSync(resolve(root, 'public/models', entry.id, 'manifest.json'))), v1.audit.manifestSha256);
  const tasks = generateQuestions(manifest, v1.audit, entry.difficulty);
  assert.equal(tasks.length, v1.tasks.length);
  return { ...structuredClone(v1), version: 'brickatlas-ldraw-2', role: 'internal-scoring-review', tasks };
});
const all = bundles.flatMap(b => b.tasks);
const construction = finalizeQuestions(all);
const snapshots = [];
for (const bundle of bundles) {
  for (const task of bundle.tasks) {
    assert.equal(score(task, task.answer).success, 1, task.id);
    if (task.visualInput) {
      const old = task.id.replace(/^ld2-/, 'ld1-');
      const target = resolve(root, 'public', task.visualInput.numberedView);
      mkdirSync(resolve(target, '..'), { recursive: true });
      copyFileSync(resolve(root, 'public/benchmark/ldraw/inputs/views', `${old}.png`), target);
    }
  }
  write(resolve(site, 'models', `${bundle.entry.id}.json`), bundle);
  const input = { version: bundle.version, role: 'model-input', modelId: bundle.entry.id,
    sourceHash: bundle.entry.sourceHash, tasks: bundle.tasks.map(publicTask) };
  write(resolve(site, 'inputs', `${bundle.entry.id}.json`), input);
  for (const task of input.tasks) {
    const request = serializeModelRequest(task, 'standard', undefined, path =>
      `data:image/png;base64,${readFileSync(resolve(root, 'public', path)).toString('base64')}`);
    const path = resolve(data, 'request-snapshots/standard', `${task.id}.json`);
    write(path, request);
    snapshots.push({ taskId: task.id, file: path.slice(root.length + 1), sha256: hash(readFileSync(path)) });
  }
}
const count = (xs: string[]) => Object.fromEntries([...new Set(xs)].sort().map(k => [k, xs.filter(x => x === k).length]));
const release = {
  version: 'brickatlas-ldraw-2', status: 'development-awaiting-quality-gates',
  models: catalog.length, parts: catalog.reduce((s: number, e: any) => s + e.parts, 0), tasks: all.length,
  families: count(all.map(t => t.family)), modalities: count(all.map(t => t.modality)),
  formats: count(all.map(t => t.format)), layers: count(all.map(t => t.layer)), construction,
  modelExperimentStatus: 'proposed-not-run', humanVisualReviewStatus: 'pending',
  formatChange: '73 graph-removal items use integer response; graphs and semantic answers unchanged.',
  visualInput: 'Frozen v1 operand isolation images copied to a distinct v2 namespace; paired full/crop renders are separate conditions.',
};
assert.equal(all.length, 617);
write(resolve(data, 'catalog.json'), catalog);
write(resolve(site, 'catalog.json'), catalog);
write(resolve(data, 'release.json'), release);
write(resolve(site, 'release.json'), release);
write(resolve(data, 'request-snapshots/manifest.json'), { version: release.version, condition: 'standard',
  purpose: 'Actual serialized messages with image bytes; dry-run, no API call', requests: snapshots });
execFileSync('python3', [resolve(import.meta.dirname, 'freeze.py'), '--verify']);
console.log(JSON.stringify(release, null, 2));
