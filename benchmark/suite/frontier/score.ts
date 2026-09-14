import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { frontierTasks, KINDS } from './tasks';
import { evaluateFrontier } from './evaluate';
import { FRONTIER_VERSION } from './geometry';

export function scoreSubmissions(raw: unknown) {
  assert.ok(Array.isArray(raw), 'Expected [{id,answer}]');
  const tasks = frontierTasks(), byId = new Map(tasks.map(t => [t.id, t]));
  const predictions = new Map<string, any>();
  for (const row of raw) {
    assert.ok(row && typeof row === 'object' && typeof row.id === 'string' && byId.has(row.id), 'Unknown case ID');
    assert.ok(!predictions.has(row.id), 'Duplicate case ID');
    predictions.set(row.id, row.answer);
  }
  const rows = tasks.map(t => {
    const present = predictions.has(t.id);
    return { id: t.id, modelId: t.modelId, kind: t.kind, present,
      answer: present ? predictions.get(t.id) : null,
      result: evaluateFrontier(t, predictions.get(t.id)) };
  });
  return { version: FRONTIER_VERSION, sourceGroups: 6, expected: tasks.length, submitted: predictions.size,
    missing: tasks.length - predictions.size, rows,
    byKind: Object.fromEntries(KINDS.map(kind => {
      const group = rows.filter(r => r.kind === kind);
      return [kind, { cases: group.length, success: group.filter(r => r.result.success === 1).length,
        coverage: group.filter(r => r.present).length / group.length }];
    })),
    note: 'Missing and malformed predictions stay in all applicable task denominators. No pooled cross-task ranking.' };
}
if (process.argv[1] && resolve(process.argv[1]) === resolve(import.meta.filename)) {
  const [input, output] = process.argv.slice(2);
  assert.ok(input && output, 'Usage: score.ts predictions.json output.json');
  const result = scoreSubmissions(JSON.parse(readFileSync(input, 'utf8')));
  writeFileSync(output, JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify({ expected: result.expected, submitted: result.submitted, missing: result.missing, byKind: result.byKind }));
}
