import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { score, replay } from '../../src/benchmark/engine';
import type { Task } from '../../src/benchmark/types';

const root = resolve(import.meta.dirname, '../..'), out = resolve(root, 'benchmark/hierarchy-v3-expanded');
const read = (name: string) => JSON.parse(readFileSync(resolve(out, name), 'utf8'));
const hash = (path: string) => createHash('sha256').update(readFileSync(path)).digest('hex');
const catalog = read('catalog.json'), bundles = catalog.map((m: any) => read(`models/${m.id}.json`));
const tasks: Task[] = bundles.flatMap((b: any) => b.tasks);
const distributions = read('answer-distributions.json');
const controls = read('controls.json');
const range = (values: number[]) => [Math.min(...values), Math.max(...values)];
const median = (values: number[]) => {
  const v = [...values].sort((a, b) => a - b), mid = Math.floor(v.length / 2);
  return v.length % 2 ? v[mid] : (v[mid - 1] + v[mid]) / 2;
};
const mean = (values: number[]) => values.reduce((s, v) => s + v, 0) / values.length;
const structural = bundles.map((b: any) => {
  const depth: Record<string, number> = {};
  for (const id of b.model.assemblyOrder) depth[id] = 1 + Math.max(0, ...b.model.joints.filter((j: any) => j.child === id).map((j: any) => depth[j.parent]));
  return { id: b.model.id, difficulty: b.model.difficulty, parts: b.model.parts.length,
    modules: b.model.modules.length, joints: b.model.joints.length, depth: Math.max(...Object.values(depth)),
    leaves: b.model.modules.filter((m: any) => !b.model.joints.some((j: any) => j.parent === m.id)).length,
    pointDrift: b.physics.nominalPointDrift, angularDrift: b.physics.nominalAngularDrift,
    residual: Math.max(...b.physics.jointResiduals.map((j: any) => j.residual)) };
});
const levels = ['D1', 'D2', 'D3', 'D4'].map(level => {
  const rows = structural.filter((r: any) => r.difficulty === level), ts = tasks.filter(t => t.difficulty === level);
  const choices = ts.filter(t => t.options);
  return { level, models: rows.length, tasks: ts.length,
    parts: { range: range(rows.map((r: any) => r.parts)), median: median(rows.map((r: any) => r.parts)) },
    modules: { range: range(rows.map((r: any) => r.modules)), median: median(rows.map((r: any) => r.modules)) },
    depth: { range: range(rows.map((r: any) => r.depth)), median: median(rows.map((r: any) => r.depth)) },
    choices: choices.length,
    constantChoicePass: choices.reduce((n, t) => n + score(t, t.format === 'single-choice' ? { choiceId: 'A' } : { choiceIds: [] }).success, 0),
    uniformChoiceExpectation: mean(choices.map(t => t.format === 'single-choice' ? 1 / t.options!.length : 1 / 2 ** t.options!.length)),
    actionRange: range(ts.filter(t => t.format === 'actions').map(t => t.answer.actionIds.length)),
  };
});
const families = [...new Set(tasks.map(t => t.family))].map(family => {
  const rows = tasks.filter(t => t.family === family), t = rows[0];
  const steps = rows.filter(t => t.format === 'actions').map(t => t.answer.actionIds.length);
  return { family, layer: t.layer, format: t.format, evidence: t.evidence, n: rows.length,
    ...(steps.length ? { steps: range(steps), medianSteps: median(steps) } : {}),
    semanticMajority: distributions.find((r: any) => r.family === family).semanticMajorityAccuracy };
});
const pilotPath = resolve(root, 'benchmark/hierarchy-v3/pilot/run.json');
const pilot = JSON.parse(readFileSync(pilotPath, 'utf8'));
const pilotRows = pilot.results.map((r: any) => {
  const task = tasks.find(t => t.id === r.id)!;
  const strict = score(task, r.prediction);
  const candidate = task.format === 'actions' && !Array.isArray(r.prediction?.actionIds)
    ? Object.values(r.prediction ?? {}).find((v: any) => Array.isArray(v) && v.every((x: unknown) => typeof x === 'string')) : undefined;
  return { id: r.id, difficulty: r.difficulty, family: r.family, format: task.format,
    strictSuccess: strict.success, validFormat: strict.validFormat,
    // Post-hoc syntax normalization is a diagnostic, never the official score.
    diagnosticRenamedFieldSuccess: candidate ? replay(task, candidate).success : null };
});
const metrics = { revision: 'hierarchy3-expanded-144', levels, families, structural,
  formats: Object.fromEntries([...new Set(tasks.map(t => t.format))].map(format => [format, tasks.filter(t => t.format === format).length])),
  physics: { maxPointDrift: Math.max(...structural.map((r: any) => r.pointDrift)),
    maxAngularDrift: Math.max(...structural.map((r: any) => r.angularDrift)), maxJointResidual: Math.max(...structural.map((r: any) => r.residual)) },
  controls: { referencePassed: controls.reduce((s: number, r: any) => s + r.oracleCheck.success, 0),
    actionSolverPassed: controls.filter((r: any) => r.publicActionSolver?.success).length,
    constantOrEmptyPassed: controls.reduce((s: number, r: any) => s + r.constantOrEmpty.success, 0) },
  pilot: { source: 'historical base48', n: pilotRows.length, strictPassed: pilotRows.reduce((n: number, r: any) => n + r.strictSuccess, 0), rows: pilotRows },
  sources: Object.fromEntries(['catalog.json', 'public.json', 'answers.json', 'controls.json', 'quality.json', 'answer-distributions.json']
    .map(p => [`benchmark/hierarchy-v3-expanded/${p}`, hash(resolve(out, p))]).concat([
      ['benchmark/hierarchy-v3/pilot/run.json', hash(pilotPath)],
      ['benchmark/paper/analyze-publication.ts', hash(import.meta.filename)],
      ...catalog.map((m: any) => [`benchmark/hierarchy-v3-expanded/models/${m.id}.json`, hash(resolve(out, `models/${m.id}.json`))]),
    ])) };
mkdirSync(resolve(import.meta.dirname, 'tables'), { recursive: true });
writeFileSync(resolve(import.meta.dirname, 'publication-analysis.json'), JSON.stringify(metrics, null, 2) + '\n');
const texRange = (r: number[]) => r[0] === r[1] ? `${r[0]}` : `${r[0]}--${r[1]}`;
writeFileSync(resolve(import.meta.dirname, 'tables/publication-structure.tex'), levels.map(l =>
  `${l.level} & ${l.models} & ${texRange(l.parts.range)} & ${l.parts.median} & ${texRange(l.modules.range)} & ${texRange(l.depth.range)} & ${l.tasks} \\\\`).join('\n') + '\n');
writeFileSync(resolve(import.meta.dirname, 'tables/publication-controls.tex'), levels.map(l =>
  `${l.level} & ${l.choices} & ${l.constantChoicePass} & ${(100 * l.constantChoicePass / l.choices).toFixed(1)} & ${(100 * l.uniformChoiceExpectation).toFixed(1)} & ${texRange(l.actionRange)} \\\\`).join('\n') + '\n');
writeFileSync(resolve(import.meta.dirname, 'tables/publication-families.tex'), families.map(f =>
  `${f.family} & ${f.format} & ${f.n} & ${(100 * f.semanticMajority).toFixed(1)} & ${f.steps ? texRange(f.steps) : '--'} \\\\`).join('\n') + '\n');
console.log(JSON.stringify({ levels, physics: metrics.physics, formats: metrics.formats, controls: metrics.controls, pilot: metrics.pilot }));
