import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { atomicJson } from '../core/budget';
import { RULES, TASKS, VERSION, CATALOG, type Kind, type Mode, type PublicTask, type Split, type Verdict } from './shared';
import { digest, models, summary, type ModelRecord } from './data';
import { taskFor } from './tasks';
import { baseline, score } from './score';
import type { CallResult } from '../core/openrouter';

export const SUITE = dirname(fileURLToPath(import.meta.url));
export const BENCHMARK = resolve(SUITE, '..');
export const ARTIFACTS = resolve(SUITE, 'artifacts');
export const SYSTEM = `${RULES}\nPublic catalog: ${JSON.stringify(CATALOG)}\nNo tools or target feedback are available on the one-shot track. Follow task-specific response schema.`;
export interface Selection { modelId: string; kind: Kind; split: Split; taskId: string }
export interface ResultRow {
  taskId: string; modelId: string; group: string; family: string; split: Split; kind: Kind;
  model: string; mode: Mode; representation: 'absolute' | 'relative';
  input: PublicTask; frames: string[]; answers: unknown[]; calls: CallResult[];
  verdict: Verdict; status: 'complete' | 'error'; error?: string;
}
export interface SuiteRun {
  version: string; id: string; status: 'running' | 'complete' | 'error';
  startedAt: string; completedAt: string | null; error?: string;
  datasetHash: string; protocolHash: string; sourceFiles: Record<string, string>;
  selection: Selection[]; selectionHash: string; models: string[]; mode: Mode;
  representation: 'absolute' | 'relative'; pricing: unknown;
  results: ResultRow[]; campaignBefore: number; campaignAfter: number;
}
export function sourceHashes() {
  const entries: Record<string, string> = {};
  for (const file of ['shared.ts', 'geometry.ts', 'data.ts', 'tasks.ts', 'score.ts', 'storage.ts', 'runner.ts', 'render.ts', 'web/viewer.ts', 'web/render.ts']) {
    entries[file] = digest(readFileSync(resolve(SUITE, file), 'utf8'));
  }
  entries['../core/openrouter.ts'] = digest(readFileSync(resolve(BENCHMARK, 'core/openrouter.ts'), 'utf8'));
  entries['../core/budget.ts'] = digest(readFileSync(resolve(BENCHMARK, 'core/budget.ts'), 'utf8'));
  return entries;
}
export function defaultSelection(representation: 'absolute' | 'relative' = 'absolute'): Selection[] {
  const result: Selection[] = [];
  for (const kind of TASKS) for (const split of ['test_id', 'test_ood'] as Split[]) {
    const candidates = models().filter(m => m.split === split && m.parameters.palette === 0);
    candidates.sort((a, b) => digest(`${kind}:${a.group}`).localeCompare(digest(`${kind}:${b.group}`)));
    const m = candidates[0];
    const task = taskFor(m, kind, representation);
    result.push({ modelId: m.id, kind, split, taskId: task.public.id });
  }
  return result;
}
export function resolveTask(taskId: string) {
  for (const m of models()) for (const kind of TASKS) {
    const task = taskFor(m, kind);
    if (task.public.id === taskId) return { model: m, task };
  }
  return null;
}
export function buildData() {
  mkdirSync(resolve(ARTIFACTS, 'dataset'), { recursive: true });
  atomicJson(resolve(ARTIFACTS, 'dataset/manifest.json'), {
    ...summary(), splitUnit: 'colorless translation/yaw canonical geometry',
    familyHoldout: ['staircase', 'gate'], license: 'CC0-1.0',
    geometry: '25 catalog entries, rectilinear bodies; stud graph; no force/robot simulation',
    release: 'public-development', independentHumanDesigns: 0,
  });
  const exports = resolve(BENCHMARK, '.runtime/suite-exports');
  mkdirSync(exports, { recursive: true });
  writeFileSync(resolve(exports, 'models.jsonl'), models().map(m => JSON.stringify(m)).join('\n') + '\n');
  atomicJson(resolve(ARTIFACTS, 'dataset/examples.json'), models().filter(m => m.parameters.palette === 0).filter((m, i, a) => a.findIndex(x => x.family === m.family) === i));
  return summary();
}
export function runBaselines() {
  const counts: Record<string, { n: number; success: number }> = {};
  for (const m of models()) for (const kind of TASKS) {
    const task = taskFor(m, kind);
    for (const name of ['oracle', 'empty', 'copy-input'] as const) {
      const key = `${name}/${kind}/${m.split}`;
      const row = counts[key] ?? { n: 0, success: 0 };
      row.n++; row.success += score(task, baseline(task, name)).metrics.success;
      counts[key] = row;
      if (name === 'oracle' && row.success !== row.n) throw new Error(`Oracle failure: ${task.public.id}`);
    }
  }
  atomicJson(resolve(ARTIFACTS, 'baseline.json'), {
    version: VERSION, datasetHash: summary().digest, disclaimer: 'Oracle is a verifier test, not a learned model.', counts,
  });
  return counts;
}
export function exportSFT() {
  const dir = resolve(BENCHMARK, '.runtime/suite-exports');
  mkdirSync(dir, { recursive: true });
  const counts: Record<string, number> = {};
  for (const split of ['train', 'validation'] as Split[]) {
    const rows = models().filter(m => m.split === split).flatMap(m => TASKS.map(kind => {
      const t = taskFor(m, kind);
      return { taskId: t.public.id, group: m.group, split, kind, needsImages: t.frames.length > 0,
        messages: [{ role: 'system', content: SYSTEM }, { role: 'user', content: JSON.stringify(t.public) },
          { role: 'assistant', content: JSON.stringify(t.oracle) }],
        renderRequests: t.frames };
    }));
    writeFileSync(resolve(dir, `${split}.sft.jsonl`), rows.map(r => JSON.stringify(r)).join('\n') + '\n');
    counts[split] = rows.length;
  }
  atomicJson(resolve(ARTIFACTS, 'training-export.json'), {
    counts, path: '.runtime/suite-exports', testLabelsExported: false,
    status: 'training recipes exported; no neural weights trained',
    note: 'Multimodal rows require rendering renderRequests into images before training. Do not train them as text-only.',
  });
  return counts;
}
export function auditOMR() {
  const root = resolve(BENCHMARK, '../public/models');
  const items = readdirSync(root, { withFileTypes: true }).filter(e => e.isDirectory()).map(e => {
    const file = resolve(root, e.name, 'manifest.json');
    const m = JSON.parse(readFileSync(file, 'utf8'));
    return { id: m.model.id, title: m.model.title, author: m.model.author, sourceUrl: m.model.sourceUrl,
      license: m.model.license, sourceHash: m.sourceHash, parts: m.stats.instances,
      uniqueParts: m.stats.uniqueParts, connectorGroundTruth: false, includedInScoredSuite: false };
  });
  atomicJson(resolve(ARTIFACTS, 'omr-audit.json'), {
    status: 'read-only inventory; not a certified connector dataset', items,
  });
  return items.length;
}
export function listRuns(): SuiteRun[] {
  const path = resolve(ARTIFACTS, 'runs');
  return existsSync(path) ? readdirSync(path).filter(id => /^[\w.-]+$/.test(id)
    && existsSync(resolve(path, id, 'run.json'))).sort().reverse()
    .map(id => JSON.parse(readFileSync(resolve(path, id, 'run.json'), 'utf8'))) : [];
}
export function groupResults(run: SuiteRun) {
  return run.models.flatMap(model => TASKS.map(kind => {
    const rows = run.results.filter(r => r.model === model && r.kind === kind);
    const done = rows.filter(r => r.status === 'complete');
    const metricKeys = [...new Set(done.flatMap(r => Object.keys(r.verdict.metrics)))];
    const metrics: Record<string, number | null> = {};
    for (const key of metricKeys) {
      const values = done.map(r => r.verdict.metrics[key]).filter((v): v is number => typeof v === 'number');
      metrics[key] = values.length ? values.reduce((a, b) => a + b, 0) / values.length : null;
    }
    return { model, kind, n: done.length, errors: rows.length - done.length, metrics,
      cost: rows.flatMap(r => r.calls).reduce((n, c) => n + c.cost, 0) };
  }));
}
