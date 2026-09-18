import { readFileSync, writeFileSync, mkdirSync, copyFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import type { AtlasManifest } from '../../../src/model/types';
import { numberedPart, publicTask, type LDrawAudit, type LDrawBundle, type LDrawEntry } from '../../../src/benchmark/ldrawTypes';
import { generateQuestions } from './questions';
import { inventorySimilarity, shapeSimilarity, sourceFingerprint } from './diversity';
import { score } from '../../../src/benchmark/engine';

const root = resolve(import.meta.dirname, '../../..'), data = resolve(root, 'benchmark/ldraw-v1');
const site = resolve(root, 'public/benchmark/ldraw');
const read = (path: string) => JSON.parse(readFileSync(path, 'utf8'));
const hash = (path: string) => createHash('sha256').update(readFileSync(path)).digest('hex');
const write = (path: string, value: unknown) => writeFileSync(path, JSON.stringify(value, null, 2) + '\n');
for (const dir of ['models', 'inputs', 'sources']) mkdirSync(resolve(site, dir), { recursive: true });
const candidates = read(resolve(data, 'candidates.json'));
const retained: Array<{ manifest: AtlasManifest; bundle: LDrawBundle; sourceFile: string }> = [];
const exclusions: Array<{ id: string; reason: string }> = [];
const fingerprints = new Set<string>(), sets = new Set<string>();
for (const config of candidates) {
  if (config.status !== 'prepared') { exclusions.push({ id: config.id, reason: config.reason }); continue; }
  const manifest: AtlasManifest = read(resolve(root, 'public/models', config.id, 'manifest.json'));
  const audit: LDrawAudit = read(resolve(data, 'audits', `${config.id}.json`));
  let reason = '';
  const fingerprint = sourceFingerprint(manifest.instances);
  if (audit.duplicatePlacements) reason = `${audit.duplicatePlacements} duplicate source placements`;
  else if (!(audit.connectorCoverage >= .9)) reason = `Connector coverage below 90% (${audit.connectorCoverage})`;
  else if (audit.collisionStatus !== 'complete') reason = 'Incomplete inset-mesh audit';
  else if (fingerprints.has(fingerprint) || sets.has(config.setNumber)) reason = 'Duplicate geometry or set family';
  if (reason) { exclusions.push({ id: config.id, reason }); continue; }
  if (hash(resolve(root, config.sourceFile)) !== manifest.sourceHash || manifest.sourceHash !== config.sourceHash)
    throw new Error(`Source hash mismatch: ${config.id}`);
  if (hash(resolve(root, 'public/models', config.id, 'manifest.json')) !== audit.manifestSha256)
    throw new Error(`Stale audit: ${config.id}`);
  fingerprints.add(fingerprint); sets.add(config.setNumber);
  const n = manifest.instances.length, difficulty = n <= 150 ? 'D1' : n <= 400 ? 'D2' : n <= 1000 ? 'D3' : 'D4';
  const tasks = generateQuestions(manifest, audit, difficulty);
  const entry: LDrawEntry = {
    id: config.id, sourceModelId: config.id, name: config.title, nameZh: config.subtitle,
    difficulty, parts: n, modules: manifest.submodels.length, tasks: tasks.length,
    sourceUrl: config.sourceUrl, author: config.author, license: config.license,
    sourceHash: config.sourceHash, setNumber: config.setNumber,
    connectorCoverage: audit.connectorCoverage, intersectionCandidates: audit.nonMatingCollisionPairs.length,
    sourceSteps: manifest.instructions?.provenance === 'source' ? manifest.instructions.steps.length : 0,
  };
  const bundle: LDrawBundle = {
    version: 'brickatlas-ldraw-1', entry, tasks, parts: manifest.instances.map(numberedPart), audit,
    instructions: manifest.instructions?.provenance === 'source' ? {
      ...manifest.instructions, disclaimer: 'Author STEP visibility replay. No insertion trajectory or physical assembly claim.',
      steps: manifest.instructions.steps.map(({ stagingOffset: _offset, motionInstanceIds: _motion, ...s }) => ({ ...s, kind: 'parts' })),
    } : undefined,
  };
  for (const task of tasks) {
    if (!score(task, task.answer).success) throw new Error(`Invalid reference answer: ${task.id}`);
    if (score(task, task.format === 'actions' ? { actionIds: [] } : { choiceId: '__invalid__' }).success)
      throw new Error(`Invalid negative control: ${task.id}`);
  }
  write(resolve(site, 'models', `${config.id}.json`), bundle);
  write(resolve(site, 'inputs', `${config.id}.json`), {
    version: bundle.version, modelId: config.id, sourceHash: config.sourceHash,
    numberedInstances: bundle.parts.map(({ id, label }) => ({ id, label })), tasks: tasks.map(publicTask),
    interaction: 'Numbered 3D model; focus, isolate, rotate, zoom and explode. Only source STEP replay is enabled.',
  });
  copyFileSync(resolve(root, config.sourceFile), resolve(site, 'sources', `${config.id}.mpd`));
  retained.push({ manifest, bundle, sourceFile: config.sourceFile });
}
const pairs = retained.flatMap((a, i) => retained.slice(i + 1).map(b => ({
  a: a.bundle.entry.id, b: b.bundle.entry.id,
  inventoryJaccard: inventorySimilarity(a.manifest.instances, b.manifest.instances),
  centeredShapeScore: shapeSimilarity(a.manifest.instances, b.manifest.instances),
}))).sort((a, b) => b.inventoryJaccard - a.inventoryJaccard);
const catalog = retained.map(r => r.bundle.entry).sort((a, b) => a.parts - b.parts);
write(resolve(site, 'catalog.json'), catalog);
write(resolve(data, 'catalog.json'), catalog);
const tasks = retained.flatMap(r => r.bundle.tasks);
const count = (values: string[]) => Object.fromEntries([...new Set(values)].sort().map(k => [k, values.filter(x => x === k).length]));
const report = {
  version: 'brickatlas-ldraw-1', status: 'source-faithful-review-release', models: retained.length, setFamilies: sets.size,
  tasks: tasks.length, parts: catalog.reduce((sum, m) => sum + m.parts, 0),
  sourceStepModels: catalog.filter(m => m.sourceSteps > 0).length, difficulty: count(catalog.map(m => m.difficulty)),
  taskFamilies: count(tasks.map(t => t.family)), layers: count(tasks.map(t => t.layer)),
  excluded: exclusions, diversityPairs: pairs, measuredModelResults: 0,
  checks: { referenceAnswers: tasks.length, invalidAnswersRejected: tasks.length, duplicateGeometry: 0, sourceHashes: retained.length },
  limits: [
    'Original source CAD models; no geometric repair or hidden supports.',
    'Connector coverage measures catalog support, not connectedness or physical stability.',
    'Non-mating mesh intersections are review candidates, not automatically defects.',
    'D1-D4 are part-count bands (<=150, <=400, <=1000, >1000), not calibrated difficulty.',
    'Inventory and centered-shape similarity are screens, not an independence guarantee.',
    'Hierarchy-3 is retired; none of its physics scores or pilot results transfer to this release.',
  ],
  sources: retained.map(r => ({ ...r.bundle.entry, sourceFile: r.sourceFile,
    manifestSha256: r.bundle.audit.manifestSha256, geometryFingerprint: sourceFingerprint(r.manifest.instances),
    componentSizes: r.bundle.audit.componentSizes, unsupportedInstances: r.bundle.audit.unsupported.length })),
};
write(resolve(data, 'release.json'), report);
write(resolve(site, 'release.json'), report);
copyFileSync(resolve(data, 'PROTOCOL.md'), resolve(site, 'PROTOCOL.md'));
console.log(JSON.stringify({ models: report.models, tasks: report.tasks, parts: report.parts, families: report.taskFamilies, excluded: exclusions.length }, null, 2));
