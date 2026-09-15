import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { evaluateMechanismTask } from './evaluate';
import { mechanismTasks, MECHANISM_VERSION } from './tasks';

export async function scoreMechanismResponses(raw: unknown) {
  assert.ok(Array.isArray(raw), 'Expected [{id,answer}]');
  const tasks = await mechanismTasks();
  const allowed = new Set(tasks.map(t => t.id));
  const answers = new Map<string, unknown>();
  for (const row of raw) {
    assert.ok(row && typeof row.id === 'string' && allowed.has(row.id), 'unknown_id');
    assert.ok(!answers.has(row.id), 'duplicate_id');
    answers.set(row.id, row.answer);
  }
  const rows = tasks.map(task => ({
    id: task.id,
    sourceGroup: task.sourceGroup,
    kind: task.kind,
    capability: task.capability,
    present: answers.has(task.id),
    result: evaluateMechanismTask(task, answers.get(task.id)),
  }));
  const kinds = [...new Set(rows.map(row => row.kind))];
  return {
    version: MECHANISM_VERSION,
    expected: rows.length,
    submitted: answers.size,
    missing: rows.length - answers.size,
    rows,
    byKind: Object.fromEntries(kinds.map(kind => {
      const selected = rows.filter(row => row.kind === kind);
      return [kind, { cases: selected.length, successes: selected.filter(row => row.result.success).length,
        sourceGroups: new Set(selected.map(row => row.sourceGroup)).size }];
    })),
    inference: 'Six original design sources; derived tasks are paired within source and are not independent samples.',
  };
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(import.meta.filename)) {
  const [input, output] = process.argv.slice(2);
  assert.ok(input && output, 'score.ts predictions.json output.json');
  const result = await scoreMechanismResponses(JSON.parse(readFileSync(input, 'utf8')));
  writeFileSync(output, JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify({ expected: result.expected, submitted: result.submitted,
    missing: result.missing, byKind: result.byKind }));
}
