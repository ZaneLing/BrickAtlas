import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS, listRuns } from '../storage';
import { TASKS } from '../shared';
import { RESEARCH_VERSION } from './dataset';
import { groupResearch, type ResearchRun } from './run';
import { PAIRED_VERSION, type PairedRun } from './paired';

// Enumerate the empirical cluster bootstrap exactly for the four object groups.
export function clusterInterval(values: number[]) {
  if (!values.length || values.length > 6 || values.some(v => !Number.isFinite(v))) throw new Error('Expected 1-6 finite cluster means');
  const means: number[] = [];
  const visit = (sum: number, depth: number) => {
    if (depth === values.length) { means.push(sum / values.length); return; }
    for (const value of values) visit(sum + value, depth + 1);
  };
  visit(0, 0); means.sort((a, b) => a - b);
  return { mean: values.reduce((a, b) => a + b, 0) / values.length,
    low: means[Math.floor(0.025 * (means.length - 1))], high: means[Math.ceil(0.975 * (means.length - 1))],
    clusters: values.length, resamples: means.length };
}
export function writeStatistics() {
  const runs = listRuns(), main = runs.find(r => r.version === RESEARCH_VERSION && r.status === 'complete') as ResearchRun;
  if (!main) throw new Error('Main experiment missing');
  const condition = (id: string) => main.cases.find(c => c.taskId === id)!.condition;
  const taskRows = groupResearch(main);
  const objectRows = main.models.flatMap(model => [...new Set(main.results.map(r => r.modelId))].map(modelId => {
    const rows = main.results.filter(r => r.model === model && r.modelId === modelId && condition(r.taskId) === 'ordinary');
    return { model, modelId, split: rows[0].split, family: rows[0].family,
      successes: rows.reduce((n, r) => n + r.verdict.metrics.success, 0), n: rows.length,
      tasks: Object.fromEntries(rows.map(r => [r.kind, r.verdict.metrics.success])) };
  }));
  const defaultSummary = main.models.map(model => ({ model,
    ...clusterInterval(objectRows.filter(r => r.model === model).map(r => r.successes / r.n)),
    note: 'Eight task-default inputs, not an aggregate visual-intelligence score.' }));
  const visibility = main.models.flatMap(model => ['reconstruct', 'complete', 'repair'].flatMap(kind =>
    ['layers', 'symbolic'].map(arm => {
      const base = main.results.filter(r => r.model === model && r.kind === kind && condition(r.taskId) === 'ordinary');
      const differences = base.map(r => main.results.find(q => q.model === model && q.kind === kind
        && q.modelId === r.modelId && condition(q.taskId) === arm)!.verdict.metrics.success - r.verdict.metrics.success);
      return { model, kind, comparison: `${arm}-ordinary`, ...clusterInterval(differences) };
    })));
  const paired = runs.filter(r => r.version === PAIRED_VERSION) as unknown as PairedRun[];
  const pairedRows = paired.flatMap(run => ['all', 'generate', 'reconstruct', 'repair'].map(kind => {
    const rows = run.results.filter(r => kind === 'all' || r.kind === kind);
    const pairs = rows.map(row => {
      const first = main.results.find(r => r.taskId === row.taskId && r.model === row.model)!;
      return { modelId: row.modelId, first: first.verdict.metrics.success, final: row.verdict.metrics.success };
    });
    const groups = [...new Set(pairs.map(p => p.modelId))];
    const deltas = groups.map(id => {
      const group = pairs.filter(p => p.modelId === id);
      return group.reduce((n, p) => n + p.final - p.first, 0) / group.length;
    });
    return { arm: run.paired.arm, kind, n: rows.length,
      before: pairs.reduce((n, p) => n + p.first, 0), after: pairs.reduce((n, p) => n + p.final, 0),
      gained: pairs.filter(p => !p.first && p.final).length, lost: pairs.filter(p => p.first && !p.final).length,
      delta: clusterInterval(deltas), newCost: rows.flatMap(r => r.calls.slice(1)).reduce((n, c) => n + c.cost, 0) };
  }));
  const pairedContrast = ['all', 'generate', 'reconstruct', 'repair'].flatMap(kind => {
    const reflection = paired.find(r => r.paired.arm === 'reflection'), validation = paired.find(r => r.paired.arm === 'validation');
    if (!reflection || !validation) return [];
    const rows = reflection.results.filter(r => kind === 'all' || r.kind === kind);
    const groups = [...new Set(rows.map(r => r.modelId))];
    return [{ kind, comparison: 'validation-reflection', ...clusterInterval(groups.map(id => {
      const group = rows.filter(r => r.modelId === id);
      return group.reduce((n, r) => n + validation.results.find(q => q.taskId === r.taskId)!.verdict.metrics.success
        - r.verdict.metrics.success, 0) / group.length;
    })) }];
  });
  const failures = taskRows.map(g => {
    const rows = main.results.filter(r => r.model === g.model && r.kind === g.kind && condition(r.taskId) === g.condition);
    return { model: g.model, kind: g.kind, condition: g.condition,
      formatFailures: rows.filter(r => r.verdict.metrics.format === 0).length,
      truncated: rows.filter(r => r.calls.some(c => c.finishReason === 'length')).length,
      meanOutputTokens: rows.reduce((n, r) => n + r.calls[0].completionTokens, 0) / rows.length,
      meanLatencyMs: rows.reduce((n, r) => n + r.calls[0].latencyMs, 0) / rows.length };
  });
  const training = JSON.parse(readFileSync(resolve(ARTIFACTS, 'research/local-training-summary.json'), 'utf8'));
  const multiRates = training.rows.filter((r: { condition: string }) => r.condition === 'multi')
    .map((r: { successes: number; cases: number }) => r.successes / r.cases) as number[];
  const seedMean = multiRates.reduce((a, b) => a + b, 0) / multiRates.length;
  const seedSD = Math.sqrt(multiRates.reduce((n, v) => n + (v - seedMean) ** 2, 0) / (multiRates.length - 1));
  const value = { taskRows, objectRows, defaultSummary, visibility, pairedRows, pairedContrast, failures,
    localTraining: training, multiSeed: { n: multiRates.length, mean: seedMean, sampleSD: seedSD },
    limitations: ['Four source objects, correlated tasks; bootstrap is descriptive and can be degenerate.',
      'No p-values or confirmatory significance claims. Public procedural pilot.',
      'Twelve generator labels are not twelve independent mechanisms; OOD label is not proof of mechanism OOD.',
      'Paired arms run sequentially, no counterbalanced provider-time control; refinement is not autonomous tool use.',
      'Training uses the old grid-v1 split, not the new composition dataset. Step-matched, not token-matched.'] };
  atomicJson(resolve(ARTIFACTS, 'research/statistics.json'), value);
  const fraction = (n: number) => `${(n * 100).toFixed(1)}%`;
  writeFileSync(resolve(ARTIFACTS, 'research/STATISTICS.md'), `# Exploratory statistics

Same four source objects; eight task-default inputs. Conditions are NEVER pooled.
Intervals are exact empirical object-cluster bootstrap percentiles (256 resamples),
not evidence of adequate population coverage; zero-width intervals are possible at n=4.

| Model | Task | Ordinary success / 4 | Layers / 4 | Symbolic / 4 |
| --- | --- | ---: | ---: | ---: |
${main.models.flatMap(model => TASKS.map(kind => `| ${model} | ${kind} | ${['ordinary', 'layers', 'symbolic'].map(c => {
  const row = taskRows.find(r => r.model === model && r.kind === kind && r.condition === c);
  return row ? Math.round((row.metrics.success ?? 0) * row.n) : 'N/A';
}).join(' | ')} |`)).join('\n')}

## Same-first-response control

| Arm | Task | n | Before | After | Gained | Lost | New USD |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
${pairedRows.map(r => `| ${r.arm} | ${r.kind} | ${r.n} | ${r.before} | ${r.after} | ${r.gained} | ${r.lost} | ${r.newCost.toFixed(8)} |`).join('\n')}

## Training

Three multi-task seeds: mean ${fraction(seedMean)}, sample SD ${fraction(seedSD)}.
All successes are editing cases; no evidence of broad task transfer.
NLL decreases are separate from execution success. Base/single have only one seed.
Local text tasks use the original grid-v1 split, not the composition experiment.

## Limits

${value.limitations.map(s => '- ' + s).join('\n')}

Full per-object vectors, visibility contrasts, validation-minus-reflection contrasts,
failure counts, latency, output tokens and training data are in statistics.json.
`);
  return { objects: objectRows.length / main.models.length, taskRows: taskRows.length, pairedRows, multiSeed: value.multiSeed };
}
