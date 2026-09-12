import { atomicJson } from '../../core/budget';
import { resolve } from 'node:path';
import { ARTIFACTS } from '../storage';
import { TASKS } from '../shared';
import { baseline } from '../score';
import { researchModels } from './dataset';
import { researchTaskFor, researchScore, type Condition } from './tasks';

export function researchBaselines() {
  const result = [];
  for (const kind of TASKS) for (const condition of (['reconstruct', 'complete', 'repair'].includes(kind)
    ? ['ordinary', 'layers', 'symbolic'] : ['ordinary']) as Condition[]) {
    for (const name of ['oracle', 'empty', 'copy-input'] as const) {
      const groups = new Map<string, { n: number; success: number }>();
      for (const model of researchModels()) {
        const task = researchTaskFor(model, kind, condition), verdict = researchScore(task, baseline(task, name));
        const key = model.split, row = groups.get(key) ?? { n: 0, success: 0 };
        row.n++; row.success += verdict.metrics.success; groups.set(key, row);
      }
      for (const [split, row] of groups) result.push({ name, kind, condition, split, ...row });
    }
  }
  const report = { rows: result, oracleIsModel: false,
    note: 'Diagnostic floors and scorer ceiling, not learned or retrieval baselines. 576 objects; test inputs are never added to training.' };
  atomicJson(resolve(ARTIFACTS, 'research/baselines.json'), report);
  return { rows: result.length, evaluated: result.reduce((n, r) => n + r.n, 0),
    oracleFailures: result.filter(r => r.name === 'oracle').reduce((n, r) => n + r.n - r.success, 0) };
}
