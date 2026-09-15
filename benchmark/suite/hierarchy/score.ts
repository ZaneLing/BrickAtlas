import { readFileSync } from 'node:fs';
import { evaluateHierarchyTask } from './evaluate';
import { hierarchyTasks } from './tasks';

interface SubmissionRow {
  id: string;
  answer: unknown;
}

export function scoreHierarchyResponses(raw: unknown) {
  if (!Array.isArray(raw)) throw new Error('Submission must be an array');
  const rows = raw as SubmissionRow[];
  if (rows.some(row => !row || typeof row.id !== 'string')) throw new Error('Every row needs a string id');
  const ids = rows.map(row => row.id);
  if (new Set(ids).size !== ids.length) throw new Error('Duplicate task id');
  const tasks = hierarchyTasks(), byId = new Map(tasks.map(task => [task.id, task]));
  for (const id of ids) if (!byId.has(id)) throw new Error(`Unknown task id: ${id}`);
  const answers = new Map(rows.map(row => [row.id, row.answer]));
  const scored = tasks.map(task => ({
    id: task.id,
    sourceGroup: task.sourceGroup,
    difficulty: task.difficulty,
    layer: task.layer,
    format: task.format,
    missing: !answers.has(task.id),
    result: evaluateHierarchyTask(task, answers.get(task.id)),
  }));
  const aggregate = (key: 'difficulty' | 'layer' | 'format') =>
    Object.fromEntries([...new Set(scored.map(row => row[key]))].map(value => {
      const selected = scored.filter(row => row[key] === value);
      return [value, {
        expected: selected.length,
        answered: selected.filter(row => !row.missing).length,
        success: selected.reduce((sum, row) => sum + row.result.success, 0),
      }];
    }));
  return {
    version: 'brickatlas-hierarchy-1',
    expected: tasks.length,
    answered: scored.filter(row => !row.missing).length,
    missing: scored.filter(row => row.missing).length,
    success: scored.reduce((sum, row) => sum + row.result.success, 0),
    byDifficulty: aggregate('difficulty'),
    byLayer: aggregate('layer'),
    byFormat: aggregate('format'),
    rows: scored,
  };
}

if (process.argv[1] && process.argv[1].endsWith('score.ts')) {
  const path = process.argv[2];
  if (!path) throw new Error('Usage: hierarchy:score <submission.json>');
  console.log(JSON.stringify(scoreHierarchyResponses(JSON.parse(readFileSync(path, 'utf8'))), null, 2));
}
