import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { relative, resolve } from 'node:path';
import { Quaternion, Vector3 } from 'three';
import { modelTasks, semanticKey, VERSION } from '../hierarchy3/tasks';
import { validateModel } from '../hierarchy3/validate';
import { score, solveActions } from '../../../src/benchmark/engine';
import type { Model } from '../hierarchy3/models';
import type { Task } from '../../../src/benchmark/types';
import { expansionModels, FAMILIES } from './models';

export const ROOT = resolve(import.meta.dirname, '../../..');
export const BASE = resolve(ROOT, 'benchmark/hierarchy-v3');
export const OUT = resolve(ROOT, 'benchmark/hierarchy-v3-expanded');
export const WEB = resolve(ROOT, 'public/benchmark');
export const REVISION = 'hierarchy3-expanded-144';
export const read = (path: string) => JSON.parse(readFileSync(path, 'utf8'));
export const sha = (path: string) => createHash('sha256').update(readFileSync(path)).digest('hex');
export const write = (path: string, value: unknown) => {
  mkdirSync(resolve(path, '..'), { recursive: true });
  writeFileSync(path, JSON.stringify(value, null, 2) + '\n');
};

export function geometryFingerprint(m: Model) {
  const points = m.parts.map(p => {
    const mod = m.modules.find(x => x.id === p.moduleId)!;
    return { shape: p.shape, size: p.size,
      position: new Vector3(...p.position).applyQuaternion(new Quaternion(...mod.rotation)).add(new Vector3(...mod.position)).toArray(),
      rotation: new Quaternion(...mod.rotation).multiply(new Quaternion(...p.rotation)).toArray() };
  });
  const origin = [0, 1, 2].map(i => Math.min(...points.map(p => p.position[i])));
  const normalized = points.map(p => ({ ...p, size: p.size.map(v => +v.toFixed(6)),
    position: p.position.map((v, i) => +(v - origin[i]).toFixed(6)), rotation: p.rotation.map(v => +v.toFixed(6)) }));
  return createHash('sha256').update(JSON.stringify(normalized.sort((a, b) => JSON.stringify(a).localeCompare(JSON.stringify(b))))).digest('hex');
}

export async function release() {
  const original = read(resolve(BASE, 'catalog.json')) as Array<{ id: string }>;
  const sources = original.map(m => ({ model: read(resolve(BASE, 'models', `${m.id}.json`)).model as Model, retained: true }))
    .concat(expansionModels().map(model => ({ model, retained: false })))
    .sort((a, b) => a.model.difficulty.localeCompare(b.model.difficulty) || a.model.id.localeCompare(b.model.id));
  assert.equal(sources.length, 144);
  assert.equal(new Set(sources.map(s => s.model.id)).size, 144);
  const fingerprints = new Map<string, string[]>(), tasks: Task[] = [], catalog: any[] = [], quality: any[] = [], controls: any[] = [];
  const unchanged: Array<{ modelId: string; sha256: string }> = [];
  for (const { model, retained } of sources) {
    const fingerprint = geometryFingerprint(model);
    if (!retained) assert.ok(!fingerprints.has(fingerprint), `Duplicate expansion geometry: ${model.id}`);
    fingerprints.set(fingerprint, [...fingerprints.get(fingerprint) ?? [], model.id]);
    assert.equal(new Set(model.parts.map(p => p.id)).size, model.parts.length);
    assert.equal(new Set(model.modules.map(m => m.id)).size, model.modules.length);
    assert.equal(new Set(model.joints.map(j => j.id)).size, model.joints.length);
    assert.equal(new Set(model.assemblyOrder).size, model.modules.length);
    assert.ok(model.parts.every(p => [...p.position, ...p.size, ...p.rotation].every(Number.isFinite)
      && p.size.every(n => n > 0) && Math.abs(new Quaternion(...p.rotation).length() - 1) < 1e-7));
    const visited = new Set<string>();
    for (const id of model.assemblyOrder) {
      assert.ok(model.modules.some(m => m.id === id));
      assert.ok(model.joints.filter(j => j.child === id).every(j => visited.has(j.parent)), `${model.id}: dependency order`);
      visited.add(id);
    }
    const validation = await validateModel(model);
    // Retained files, questions and simulation evidence are byte-preserved.
    const record = retained ? read(resolve(BASE, 'models', `${model.id}.json`))
      : { version: VERSION, revision: REVISION, model, ...await modelTasks(model), validation };
    assert.ok(record.physics.nominalWithinTolerance, `${model.id}: nominal protocol`);
    assert.equal(record.tasks.length, 48);
    for (const task of record.tasks as Task[]) {
      assert.equal(score(task, task.answer).success, 1, task.id);
      if (task.options) {
        const keys = task.options.map(o => semanticKey(task, o.value));
        assert.equal(new Set(keys).size, keys.length, task.id);
        for (const option of task.options) if (task.format === 'single-choice')
          assert.equal(score(task, { choiceId: option.id }).success, Number(option.id === task.answer.choiceId), task.id);
      }
      if (task.format === 'actions') assert.equal(score(task, solveActions(task)).success, 1, task.id);
      const control = task.format === 'single-choice' ? { choiceId: 'A' }
        : task.format === 'multiple-choice' ? { choiceIds: [] } : task.format === 'actions' ? { actionIds: [] } : {};
      controls.push({ id: task.id, modelId: model.id, difficulty: task.difficulty, layer: task.layer,
        family: task.family, oracleCheck: score(task, task.answer),
        publicActionSolver: task.format === 'actions' ? score(task, solveActions(task)) : null,
        constantOrEmpty: score(task, control) });
    }
    tasks.push(...record.tasks);
    const local = resolve(OUT, 'models', `${model.id}.json`);
    mkdirSync(resolve(local, '..'), { recursive: true });
    if (retained) {
      copyFileSync(resolve(BASE, 'models', `${model.id}.json`), local);
      unchanged.push({ modelId: model.id, sha256: sha(local) });
    } else write(local, record);
    // Publish after the entire release has passed all gates.
    catalog.push({ id: model.id, name: model.name, nameZh: model.nameZh, difficulty: model.difficulty,
      family: model.family, lineage: model.lineage, retained, parts: model.parts.length,
      modules: model.modules.length, joints: model.joints.length, tasks: record.tasks.length, geometryFingerprint: fingerprint });
    quality.push({ modelId: model.id, ...validation, ...record.geometry,
      nominalPointDrift: record.physics.nominalPointDrift, nominalAngularDrift: record.physics.nominalAngularDrift,
      maxJointResidual: Math.max(...record.physics.jointResiduals.map((j: any) => j.residual)),
      nominalWithinTolerance: record.physics.nominalWithinTolerance });
    if (catalog.length % 12 === 0) console.log(`Validated ${catalog.length}/144 models`);
  }
  const levels = ['D1', 'D2', 'D3', 'D4'].map(difficulty => {
    const selected = catalog.filter(m => m.difficulty === difficulty);
    assert.equal(selected.length, 36);
    return { id: difficulty, models: selected.length, newModels: selected.filter(m => !m.retained).length,
      tasks: tasks.filter(t => t.difficulty === difficulty).length,
      parts: selected.reduce((s, m) => s + m.parts, 0), minParts: Math.min(...selected.map(m => m.parts)),
      maxParts: Math.max(...selected.map(m => m.parts)), modules: selected.reduce((s, m) => s + m.modules, 0) };
  });
  assert.equal(tasks.length, 6912); assert.equal(new Set(tasks.map(t => t.id)).size, tasks.length);
  const distributions = [...new Set(tasks.map(t => t.family))].map(family => {
    const ts = tasks.filter(t => t.family === family), counts: Record<string, number> = {};
    assert.equal(ts.length, 144);
    for (const t of ts) {
      const value = t.format === 'single-choice' ? t.options!.find(o => o.id === t.answer.choiceId)!.value
        : t.format === 'multiple-choice' ? t.options!.filter(o => t.answer.choiceIds.includes(o.id)).map(o => o.value).sort() : t.answer;
      const key = semanticKey(t, value); counts[key] = (counts[key] ?? 0) + 1;
    }
    return { family, n: ts.length, uniqueAnswers: Object.keys(counts).length,
      semanticMajorityAccuracy: Math.max(...Object.values(counts)) / ts.length, frequency: counts };
  });
  const audit = { version: VERSION, revision: REVISION, sourceObjects: 144, retainedLayouts: 48, newLayouts: 96,
    tasks: tasks.length, taskFamilies: 48, newTaskInstances: 4608, expansionConstructorFamilies: FAMILIES.length,
    uniqueGeometries: fingerprints.size, retainedGeometryDuplicates: [...fingerprints.values()].filter(ids => ids.length > 1),
    levels, parts: catalog.reduce((s, m) => s + m.parts, 0), modules: catalog.reduce((s, m) => s + m.modules, 0),
    joints: catalog.reduce((s, m) => s + m.joints, 0), nominalWithinTolerance: quality.filter(q => q.nominalWithinTolerance).length,
    byLayer: Object.fromEntries(['atomic', 'metacognitive', 'procedural', 'integrative'].map(l => [l, tasks.filter(t => t.layer === l).length])),
    publicActionSolver: controls.filter(c => c.publicActionSolver?.success).length,
    modelInference: 'No new paid calls; 7/16 historical pilot applies only to retained base-48 tasks',
    scope: 'Digital compound modules, cuboid contacts, fixed foundation and finite-force servos; no commercial LEGO connector or robot-path certification' };
  write(resolve(OUT, 'audit.json'), audit);
  write(resolve(OUT, 'catalog.json'), catalog);
  write(resolve(OUT, 'public.json'), tasks.map(({ answer, ...task }) => task));
  write(resolve(OUT, 'answers.json'), tasks.map(t => ({ id: t.id, answer: t.answer })));
  write(resolve(OUT, 'quality.json'), quality);
  write(resolve(OUT, 'controls.json'), controls);
  write(resolve(OUT, 'answer-distributions.json'), distributions);
  write(resolve(OUT, 'retained-compatibility.json'), { base: 'hierarchy-v3', unchanged,
    preservedTaskCount: 2304, reviewStorageKey: 'brickatlas:hierarchy3:reviews:v1' });
  for (const entry of catalog) copyFileSync(resolve(OUT, 'models', `${entry.id}.json`), resolve(WEB, 'models', `${entry.id}.json`));
  for (const name of ['audit.json', 'catalog.json']) copyFileSync(resolve(OUT, name), resolve(WEB, name));
  manifest(); return audit;
}

export function manifest() {
  const list = (dir: string): string[] => readdirSync(dir, { withFileTypes: true }).flatMap(e =>
    e.isDirectory() ? list(resolve(dir, e.name)) : [resolve(dir, e.name)]);
  if (!existsSync(OUT)) return;
  const paths = [...list(OUT).filter(p => !p.endsWith('manifest.json')),
    ...list(resolve(ROOT, 'benchmark/suite/hierarchy3-expanded')), ...list(resolve(ROOT, 'benchmark/suite/hierarchy3')),
    ...list(resolve(ROOT, 'src/benchmark')), resolve(ROOT, 'src/app/App.tsx')];
  write(resolve(OUT, 'manifest.json'), { version: VERSION, revision: REVISION,
    files: Object.fromEntries(paths.map(p => [relative(ROOT, p), sha(p)])) });
}
export function syncDocs() {
  for (const name of ['main.pdf', 'supplement.pdf', 'main.zh-CN.md'])
    copyFileSync(resolve(ROOT, 'benchmark/paper', name), resolve(WEB, 'docs', name));
  for (const name of ['REPORT.zh-CN.md', 'QUESTION_BANK.zh-CN.md'])
    copyFileSync(resolve(OUT, name), resolve(WEB, 'docs', name));
  for (const name of ['matrix', 'library', 'teaser'])
    copyFileSync(resolve(OUT, `${name}.png`), resolve(WEB, 'figures', `expanded-${name}.png`));
}
if (process.argv[1] === import.meta.filename) {
  if (process.argv.includes('--manifest')) manifest();
  else if (process.argv.includes('--docs')) syncDocs();
  else console.log(JSON.stringify(await release()));
}
