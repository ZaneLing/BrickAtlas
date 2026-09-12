import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { getSpec } from '../v2/cases';
import { clusterBootstrap } from '../v2/batch';
import { STUDY } from './protocol';
import { localEvidenceRuns } from './local-evidence';
import { LOCAL_JOBS, localMatrixComplete } from './local-contract';

export function localStatistics() {
  const runs = localEvidenceRuns();
  const base = runs.find(r => r.manifest.condition === 'base');
  const rows = runs.flatMap(run => {
    const keys = [...new Set(run.rows.map(r => {
      const s = getSpec(r.caseId); return [s.kind, s.variant, s.condition, s.split].join('|');
    }))];
    return keys.map(stratum => {
      const selected = run.rows.filter(r => {
        const s = getSpec(r.caseId); return [s.kind, s.variant, s.condition, s.split].join('|') === stratum;
      });
      const groups = [...new Set(selected.map(r => getSpec(r.caseId).group))];
      const fields = [...new Set(selected.flatMap(r => Object.keys(r.verdict.metrics)))];
      return { run: run.id, condition: run.manifest.condition, seed: run.manifest.seed, stratum, n: selected.length,
        sourceGroups: groups.length, metrics: Object.fromEntries(fields.map(field => {
          const values = selected.map(r => r.verdict.metrics[field]).filter((v): v is number => typeof v === 'number');
          return [field, { value: values.length ? values.reduce((n, v) => n + v, 0) / values.length : null, denominator: values.length }];
        })),
        successInterval: clusterBootstrap(groups.map(group => {
          const values = selected.filter(r => getSpec(r.caseId).group === group);
          return values.reduce((n, r) => n + r.verdict.metrics.success, 0) / values.length;
        })) };
    });
  });
  const compare = (beforeRun: typeof runs[number], run: typeof runs[number]) => {
    return [...new Set(rows.filter(r => r.run === run.id).map(r => r.stratum))].map(stratum => {
      const specs = run.rows.filter(r => {
        const s = getSpec(r.caseId); return [s.kind, s.variant, s.condition, s.split].join('|') === stratum;
      });
      const changes = specs.map(r => {
        const before = beforeRun.rows.find(b => b.caseId === r.caseId)!;
        return { caseId: r.caseId, group: getSpec(r.caseId).group,
          before: before.verdict.metrics.success, after: r.verdict.metrics.success };
      });
      const groups = [...new Set(changes.map(r => r.group))];
      return { beforeRun: beforeRun.id, run: run.id, stratum, n: changes.length, sourceGroups: groups.length,
        gains: changes.filter(r => r.after > r.before).length, losses: changes.filter(r => r.after < r.before).length,
        deltaInterval: clusterBootstrap(groups.map(group => {
          const values = changes.filter(r => r.group === group);
          return values.reduce((n, r) => n + r.after - r.before, 0) / values.length;
        })), changes };
    });
  };
  const paired = runs.filter(r => r.manifest.condition !== 'base').flatMap(run => {
    assert.ok(base, 'Base run required for pairing'); return compare(base, run);
  });
  const conditionPairs = [17, 29, 43].flatMap(seed =>
    [['single', 'multi'], ['single', 'leave-edit'], ['leave-edit', 'multi']].flatMap(([a, b]) => {
      const before = runs.find(r => r.manifest.condition === a && r.manifest.seed === seed);
      const after = runs.find(r => r.manifest.condition === b && r.manifest.seed === seed);
      return before && after ? compare(before, after) : [];
    }));
  const seedGroups = [...new Set(rows.map(r => [r.condition, r.stratum].join('|')))].map(key => {
    const selected = rows.filter(r => [r.condition, r.stratum].join('|') === key);
    const values = selected.map(r => r.metrics.success.value!);
    const mean = values.reduce((n, v) => n + v, 0) / values.length;
    return { key, seeds: selected.map(r => r.seed), mean,
      sampleStandardDeviation: values.length > 1 ? Math.sqrt(values.reduce((n, v) => n + (v - mean) ** 2, 0) / (values.length - 1)) : null };
  });
  const budgets = runs.map(run => {
    const steps = JSON.parse(readFileSync(resolve(run.dir, 'steps.json'), 'utf8'));
    return { run: run.id, steps: steps.length, supervisedTokens: run.manifest.supervised_tokens,
      trainingInputTokens: steps.reduce((n: number, s: any) => n + s.samples.reduce((n: number, r: any) => n + r.input_tokens, 0), 0),
      trainingImageUses: steps.reduce((n: number, s: any) => n + s.samples.reduce((n: number, r: any) => n + r.images, 0), 0),
      elapsedSeconds: run.manifest.completed_at - run.manifest.started_at,
      inferenceTokens: run.rows.reduce((n, r) => n + r.call.promptTokens + r.call.completionTokens, 0),
      truncated: run.rows.filter(r => r.call.finishReason === 'length').length };
  });
  const result = { completedJobs: runs.length, plannedJobs: LOCAL_JOBS.length,
    completeMatrix: localMatrixComplete(runs.map(run => `${run.manifest.condition}-seed${run.manifest.seed}`)),
    rows, pairedToBase: paired, pairedConditions: conditionPairs, seedGroups, budgets,
    caveats: ['Seed dispersion is not an independent-object confidence interval.',
      'Only leave-edit/rotate tests the excluded training task variant; recolor/remove were not trained in any condition.',
      'Equal answer supervision and updates are not equal compute. No confirmatory or causal transfer claim.'] };
  atomicJson(resolve(STUDY, 'local-statistics.json'), result);
  return { completedJobs: runs.length, strata: rows.length, completeMatrix: result.completeMatrix };
}
