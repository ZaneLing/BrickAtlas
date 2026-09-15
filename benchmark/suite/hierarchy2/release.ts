import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync, readFileSync, readdirSync, existsSync, copyFileSync } from 'node:fs';
import { resolve, relative } from 'node:path';
import { createHash } from 'node:crypto';
import { models } from './models';
import { modelTasks, VERSION, ATOMIC, META } from './tasks';
import { score, solveActions } from '../../../src/benchmark/engine';
import type { Task } from '../../../src/benchmark/types';

const root = resolve(import.meta.dirname, '../../..');
export const OUT = resolve(root, 'benchmark/hierarchy-v2');
export const WEB = resolve(root, 'public/benchmark');
export const sha = (path: string) => createHash('sha256').update(readFileSync(path)).digest('hex');
const write = (path: string, value: unknown) => {
  mkdirSync(resolve(path, '..'), { recursive: true });
  writeFileSync(path, JSON.stringify(value, null, 2) + '\n');
};

export async function release() {
  const all = models();
  assert.equal(all.length, 40);
  const tasks: Task[] = [], catalog: any[] = [], quality: any[] = [], controls: any[] = [];
  for (const model of all) {
    assert.equal(new Set(model.parts.map(p => p.id)).size, model.parts.length);
    assert.equal(new Set(model.modules.map(m => m.id)).size, model.modules.length);
    assert.ok(model.parts.every(p => model.modules.some(m => m.id === p.moduleId)
      && [...p.position, ...p.rotation, ...p.size].every(Number.isFinite) && p.size.every(n => n > 0)));
    const visited = new Set(model.modules.filter(m => m.anchored).map(m => m.id));
    for (const id of model.assemblyOrder) {
      assert.ok(model.joints.filter(j => j.child === id).every(j => visited.has(j.parent)), `${model.id}:${id} order`);
      visited.add(id);
    }
    assert.equal(visited.size, model.modules.length);
    const built = await modelTasks(model);
    tasks.push(...built.tasks);
    const record = { model, ...built };
    write(resolve(OUT, 'models', `${model.id}.json`), record);
    write(resolve(WEB, 'models', `${model.id}.json`), record);
    catalog.push({ id: model.id, name: model.name, nameZh: model.nameZh, difficulty: model.difficulty,
      family: model.family, lineage: model.lineage, parts: model.parts.length, modules: model.modules.length,
      joints: model.joints.length, tasks: built.tasks.length });
    quality.push({ modelId: model.id, difficulty: model.difficulty, ...built.geometry,
      nominalDrift: built.physics.nominalDrift, nominalWithinTolerance: built.physics.nominalWithinTolerance,
      simulatorScope: built.physics.scope });
    for (const t of built.tasks) {
      const predicted = t.format === 'actions' ? solveActions(t) : t.answer;
      const control = t.format === 'single-choice' ? { choiceId: 'A' }
        : t.format === 'multiple-choice' ? { choiceIds: [] }
          : t.format === 'actions' ? { actionIds: [] } : {};
      controls.push({ id: t.id, difficulty: t.difficulty, layer: t.layer, family: t.family,
        oracleCheck: score(t, t.answer), publicActionSolver: t.format === 'actions' ? score(t, predicted) : null,
        constantOrEmpty: score(t, control) });
    }
    console.log(`${model.difficulty} ${model.id}: ${model.parts.length} parts / ${built.tasks.length} tasks`);
  }
  const levels = ['D1', 'D2', 'D3', 'D4'].map(id => {
    const selected = catalog.filter(m => m.difficulty === id);
    assert.equal(selected.length, 10);
    return { id, models: selected.length, parts: selected.reduce((s, m) => s + m.parts, 0),
      minParts: Math.min(...selected.map(m => m.parts)), maxParts: Math.max(...selected.map(m => m.parts)),
      tasks: tasks.filter(t => t.difficulty === id).length };
  });
  const audit = { version: VERSION, status: 'public-development', sourceObjects: all.length,
    newLayouts: 22, retainedLayouts: 18, independentHumanDesigners: 0,
    tasks: tasks.length, atomicFamilies: ATOMIC.length, metacognitiveFamilies: META.length,
    proceduralFamilies: 4, integrativeFamilies: 3, levels,
    parts: catalog.reduce((s, m) => s + m.parts, 0),
    modules: catalog.reduce((s, m) => s + m.modules, 0),
    joints: catalog.reduce((s, m) => s + m.joints, 0),
    byLayer: Object.fromEntries(['atomic', 'metacognitive', 'procedural', 'integrative']
      .map(layer => [layer, tasks.filter(t => t.layer === layer).length])),
    nominalWithinTolerance: quality.filter(q => q.nominalWithinTolerance).length,
    simulationModels: all.length,
    modelInference: existsSync(resolve(OUT, 'pilot/run.json'))
      ? '16-cell pilot archived separately; historical scores are not pooled'
      : 'not run on Hierarchy-2; historical scores are separate',
    physicsBoundary: 'cuboid envelopes, compound rigid modules, fixed base; no certified LEGO buildability or calibrated material safety',
  };
  write(resolve(OUT, 'catalog.json'), catalog); write(resolve(WEB, 'catalog.json'), catalog);
  write(resolve(OUT, 'public.json'), tasks.map(({ answer, ...task }) => task));
  write(resolve(OUT, 'answers.json'), tasks.map(t => ({ id: t.id, answer: t.answer })));
  write(resolve(OUT, 'quality.json'), quality); write(resolve(OUT, 'controls.json'), controls);
  write(resolve(OUT, 'audit.json'), audit); write(resolve(WEB, 'audit.json'), audit);
  manifest();
  return audit;
}
export function manifest() {
  const list = (dir: string): string[] => readdirSync(dir, { withFileTypes: true }).flatMap(entry =>
    entry.isDirectory() ? list(resolve(dir, entry.name)) : [resolve(dir, entry.name)]);
  if (!existsSync(OUT)) return;
  const paths = [...list(OUT).filter(p => !p.endsWith('manifest.json')),
    ...list(resolve(root, 'benchmark/suite/hierarchy2')), ...list(resolve(root, 'src/benchmark'))];
  write(resolve(OUT, 'manifest.json'), { version: VERSION,
    files: Object.fromEntries(paths.map(p => [relative(root, p), sha(p)])) });
}
export function syncDocs() {
  mkdirSync(resolve(WEB, 'docs'), { recursive: true });
  mkdirSync(resolve(WEB, 'figures'), { recursive: true });
  for (const name of ['main.pdf', 'supplement.pdf', 'main.zh-CN.md'])
    copyFileSync(resolve(root, 'benchmark/paper', name), resolve(WEB, 'docs', name));
  for (const name of ['REPORT.zh-CN.md', 'QUESTION_BANK.zh-CN.md'])
    copyFileSync(resolve(OUT, name), resolve(WEB, 'docs', name));
  for (const name of ['hierarchy2-matrix', 'hierarchy2-pilot', 'hierarchy2-library'])
    copyFileSync(resolve(OUT, `${name}.png`), resolve(WEB, 'figures', `${name}.png`));
}
if (process.argv[1] === import.meta.filename) {
  if (process.argv.includes('--manifest')) manifest();
  else if (process.argv.includes('--docs')) syncDocs();
  else console.log(JSON.stringify(await release()));
}
