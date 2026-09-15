import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { score } from '../../../src/benchmark/engine';
import type { Task } from '../../../src/benchmark/types';
import { OUT } from './release';

export function scoreBatch(submission: unknown) {
  if (!Array.isArray(submission)) throw new Error('Expected [{id, answer}]');
  const catalog = JSON.parse(readFileSync(resolve(OUT, 'catalog.json'), 'utf8'));
  const tasks: Task[] = catalog.flatMap((m: any) =>
    JSON.parse(readFileSync(resolve(OUT, 'models', `${m.id}.json`), 'utf8')).tasks);
  const validIds = new Set(tasks.map(t => t.id));
  const answers = new Map<string, unknown>();
  for (const row of submission) {
    if (!row || typeof row.id !== 'string' || !validIds.has(row.id)) throw new Error('Unknown/malformed task ID');
    if (answers.has(row.id)) throw new Error('Duplicate task ID');
    answers.set(row.id, row.answer);
  }
  const rows = tasks.map(t => ({ id: t.id, modelId: t.modelId, difficulty: t.difficulty,
    layer: t.layer, family: t.family, missing: !answers.has(t.id), verdict: score(t, answers.get(t.id)) }));
  const cells = ['D1', 'D2', 'D3', 'D4'].flatMap(difficulty =>
    ['atomic', 'metacognitive', 'procedural', 'integrative'].map(layer => {
      const rs = rows.filter(r => r.difficulty === difficulty && r.layer === layer);
      return { difficulty, layer, expected: rs.length, answered: rs.filter(r => !r.missing).length,
        success: rs.reduce((s, r) => s + r.verdict.success, 0) };
    }));
  return { expected: tasks.length, answered: answers.size, missing: tasks.length - answers.size, cells, rows };
}
if (process.argv[1] === import.meta.filename) {
  if (!process.argv[2]) throw new Error('Usage: h2:score predictions.json');
  console.log(JSON.stringify(scoreBatch(JSON.parse(readFileSync(process.argv[2], 'utf8'))), null, 2));
}
