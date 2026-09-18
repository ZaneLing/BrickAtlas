import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { score } from '../../../src/benchmark/engine';
import type { LDrawBundle, LDrawTask } from '../../../src/benchmark/ldrawTypes';
const root = resolve(import.meta.dirname, '../../..');
export function scoreLDrawBatch(raw: unknown) {
  if (!Array.isArray(raw)) throw new Error('Expected [{id, answer}]');
  const catalog = JSON.parse(readFileSync(resolve(root, 'benchmark/ldraw-v1/catalog.json'), 'utf8'));
  const tasks: LDrawTask[] = catalog.flatMap((m: any) =>
    (JSON.parse(readFileSync(resolve(root, 'public/benchmark/ldraw/models', `${m.id}.json`), 'utf8')) as LDrawBundle).tasks);
  const ids = new Set(tasks.map(t => t.id)), submissions = new Map<string, unknown>();
  for (const row of raw) {
    if (!row || typeof row !== 'object' || !ids.has(row.id)) throw new Error('Unknown task ID');
    if (submissions.has(row.id)) throw new Error(`Duplicate task ID: ${row.id}`);
    submissions.set(row.id, row.answer);
  }
  const rows = tasks.map(t => ({ id: t.id, modelId: t.modelId, family: t.family, modality: t.modality,
    submitted: submissions.has(t.id), verdict: score(t, submissions.get(t.id)) }));
  const success = rows.reduce((s, r) => s + r.verdict.success, 0);
  const by = (key: 'family' | 'modelId' | 'modality') => Object.fromEntries([...new Set(rows.map(r => r[key]))].map(k => {
    const group = rows.filter(r => r[key] === k);
    return [k, { total: group.length, success: group.reduce((s, r) => s + r.verdict.success, 0) }];
  }));
  return { version: 'brickatlas-ldraw-1', expected: tasks.length, submitted: submissions.size,
    missing: tasks.length - submissions.size, success, accuracy: success / tasks.length,
    byFamily: by('family'), bySource: by('modelId'), byModality: by('modality'), rows };
}
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  if (!process.argv[2] || !process.argv[3]) throw new Error('Usage: tsx score.ts submissions.json scores.json');
  const result = scoreLDrawBatch(JSON.parse(readFileSync(process.argv[2], 'utf8')));
  writeFileSync(process.argv[3], JSON.stringify(result, null, 2) + '\n');
  console.log(`${result.success}/${result.expected} exact successes; ${result.missing} missing`);
}
