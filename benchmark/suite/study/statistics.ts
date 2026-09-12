import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { getSpec } from '../v2/cases';
import { clusterBootstrap } from '../v2/batch';
import { STUDY } from './protocol';
import { studyRuns, summarize, type StudyRow } from './results';

function correlation(x: number[], y: number[]) {
  const mx = x.reduce((a, b) => a + b, 0) / x.length, my = y.reduce((a, b) => a + b, 0) / y.length;
  const vx = x.reduce((n, v) => n + (v - mx) ** 2, 0), vy = y.reduce((n, v) => n + (v - my) ** 2, 0);
  return vx && vy ? x.reduce((n, v, i) => n + (v - mx) * (y[i] - my), 0) / Math.sqrt(vx * vy) : null;
}
export function statistics() {
  const main = studyRuns().find(r => r.id.endsWith('-api') && r.status === 'complete');
  if (!main) throw new Error('Completed API run required');
  const groups = summarize(main), rows = main.rows as StudyRow[];
  const models = [...new Set(rows.map(r => r.model))];
  const objectIds = [...new Set(rows.filter(r => getSpec(r.caseId).kind !== 'parts').map(r => getSpec(r.caseId).modelId))];
  const tasks = ['relations', 'reconstruct', 'generate', 'complete', 'edit', 'plan', 'repair'];
  const objects = models.flatMap(model => objectIds.map(id => ({
    model, id, values: Object.fromEntries(tasks.map(kind => {
      const selected = rows.filter(r => r.model === model && getSpec(r.caseId).modelId === id && getSpec(r.caseId).kind === kind);
      return [kind, selected.reduce((n, r) => n + r.verdict.metrics.success, 0) / selected.length];
    })),
  })));
  const correlations = models.flatMap(model => tasks.flatMap((a, i) => tasks.slice(i + 1).map(b => {
    const selected = objects.filter(o => o.model === model);
    return { model, a, b, n: selected.length, pearson: correlation(selected.map(o => o.values[a]), selected.map(o => o.values[b])),
      warning: 'Exploratory task-object association, not causal or confirmatory. Null means constant marginals.' };
  })));
  const controls = studyRuns().find(r => r.id.endsWith('-controls') && r.status === 'complete');
  const paired = controls ? [...new Set(controls.rows.map((r: StudyRow) => r.arm))].map(arm => {
    const selected = controls.rows.filter((r: StudyRow) => r.arm === arm) as StudyRow[];
    const changes = selected.map(r => {
      const first = rows.find(q => q.caseId === r.caseId && q.model === controls.model)!;
      return { caseId: r.caseId, first: first.verdict.metrics.success, final: r.verdict.metrics.success,
        surfaceChange: (r.verdict.metrics.surfaceF1 ?? 0) - (first.verdict.metrics.surfaceF1 ?? 0) };
    });
    return { arm, n: changes.length, before: changes.reduce((n, c) => n + c.first, 0),
      after: changes.reduce((n, c) => n + c.final, 0),
      gains: changes.filter(c => !c.first && c.final).length, losses: changes.filter(c => c.first && !c.final).length,
      deltaInterval: clusterBootstrap(changes.map(c => c.final - c.first)), changes };
  }) : [];
  const result = { mainRun: main.id, groups, objects, correlations, paired,
    caveats: ['24 assembly objects, not 337 independent objects. Known catalog query set counted separately.',
      'Two API model families; repeated/control subset eight objects. Not broad or powered model ranking.',
      'No rejection of null or causal transfer based on these exploratory correlations.'],
    controlsComplete: !!controls };
  atomicJson(resolve(STUDY, 'statistics.json'), result);
  return { cases: rows.length, objects: objectIds.length, models, paired };
}
