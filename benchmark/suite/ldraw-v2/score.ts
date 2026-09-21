import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { score } from '../../../src/benchmark-v2/scoring';
export { score } from '../../../src/benchmark-v2/scoring';
import type { InternalBundle, V2Task } from './types';
import { alteredGraph } from './conditions';
import { deriveAnswer } from './oracle';
import type { AtlasManifest } from '../../../src/model/types';
const root = resolve(import.meta.dirname, '../../..');
export function scoreLDrawBatch(raw: unknown, expectedIds?: string[], graphIntervention = false) {
  if (!Array.isArray(raw)) throw new Error('Expected [{id, answer}]');
  const catalog = JSON.parse(readFileSync(resolve(root, 'benchmark/ldraw-v2/catalog.json'), 'utf8'));
  const allTasks: V2Task[] = catalog.flatMap((m: any) => {
    const bundle: InternalBundle = JSON.parse(readFileSync(resolve(root, 'public/benchmark/ldraw-v2/models', `${m.id}.json`), 'utf8'));
    if (bundle.role !== 'internal-scoring-review' || bundle.version !== 'brickatlas-ldraw-2') throw new Error('Wrong scoring role/version');
    return bundle.tasks;
  });
  if (expectedIds && (new Set(expectedIds).size !== expectedIds.length || expectedIds.some(id => !allTasks.some(t => t.id === id))))
    throw new Error('Invalid preregistered task list');
  const tasks = expectedIds ? allTasks.filter(t => expectedIds.includes(t.id)) : allTasks;
  const ids = new Set(tasks.map(t => t.id)), submissions = new Map<string, unknown>();
  for (const row of raw) {
    if (!row || typeof row !== 'object' || !ids.has(row.id)) throw new Error('Unknown task ID');
    if (submissions.has(row.id)) throw new Error(`Duplicate task ID: ${row.id}`);
    submissions.set(row.id, row.answer);
  }
  const rows = tasks.map(t => {
    const scoringTask = graphIntervention
      ? { ...t, answer: deriveAnswer(alteredGraph(t), { instances: [] } as unknown as AtlasManifest) } : t;
    return { id: t.id, modelId: t.modelId, family: t.family, modality: t.modality,
      submitted: submissions.has(t.id), verdict: score(scoringTask, submissions.get(t.id)) };
  });
  const success = rows.reduce((s, r) => s + r.verdict.success, 0);
  const by = (key: 'family' | 'modelId' | 'modality') => Object.fromEntries([...new Set(rows.map(r => r[key]))].map(k => {
    const group = rows.filter(r => r[key] === k);
    return [k, { total: group.length, success: group.reduce((s, r) => s + r.verdict.success, 0) }];
  }));
  const sources = Object.values(by('modelId'));
  return { version: 'brickatlas-ldraw-2', expected: tasks.length, submitted: submissions.size,
    missing: tasks.length - submissions.size, success, accuracy: tasks.length ? success / tasks.length : null,
    macroSourceAccuracy: sources.length ? sources.reduce((s, r) => s + r.success / r.total, 0) / sources.length : null,
    byFamily: by('family'), bySource: by('modelId'), byModality: by('modality'), rows };
}
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  if (!process.argv[2] || !process.argv[3]) throw new Error('Usage: tsx score.ts submissions.json scores.json');
  const result = scoreLDrawBatch(JSON.parse(readFileSync(process.argv[2], 'utf8')));
  writeFileSync(process.argv[3], JSON.stringify(result, null, 2) + '\n');
  console.log(`${result.success}/${result.expected} exact successes; ${result.missing} missing`);
}
