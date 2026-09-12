import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS, BENCHMARK, SYSTEM } from '../storage';
import { digest } from '../data';
import type { SuiteRenderer } from '../render';
import { researchModels } from './dataset';
import { researchSelection } from './run';
import { researchTaskFor, researchScore } from './tasks';

export async function exportResearchInputs(renderer: SuiteRenderer) {
  const dir = resolve(BENCHMARK, '.runtime/research-exports');
  mkdirSync(resolve(dir, 'images'), { recursive: true });
  const selection = researchSelection(), rows = [];
  for (const entry of selection) {
    const task = researchTaskFor(researchModels().find(m => m.id === entry.modelId)!, entry.kind, entry.condition);
    const images = [];
    for (const frame of task.frames) {
      const rendered = await renderer.render(frame), path = `images/${rendered.hash}.png`;
      writeFileSync(resolve(dir, path), rendered.buffer); images.push(path);
    }
    rows.push({ taskId: entry.taskId, condition: entry.condition, system: SYSTEM, input: task.public, images,
      modality: images.length ? 'RGB+text' : 'text/structure' });
  }
  writeFileSync(resolve(dir, 'inputs.jsonl'), rows.map(r => JSON.stringify(r)).join('\n') + '\n');
  atomicJson(resolve(dir, 'manifest.json'), { cases: rows.length, selectionHash: digest(selection), privilegedCondition: 'symbolic',
    note: 'Fixed public pilot inputs, not a private test. No scorer geometry included beyond explicitly symbolic condition.' });
  return { cases: rows.length, output: '.runtime/research-exports/inputs.jsonl', apiCalls: 0 };
}
export function scoreResearchPredictions(path: string) {
  const lines = readFileSync(resolve(path), 'utf8').split('\n').filter(Boolean)
    .map(line => JSON.parse(line) as { taskId: string; answer: unknown });
  const selection = researchSelection(), known = new Set(selection.map(s => s.taskId));
  if (new Set(lines.map(l => l.taskId)).size !== lines.length) throw new Error('Duplicate task ID');
  if (lines.some(l => !known.has(l.taskId))) throw new Error('Unknown task ID');
  const rows = selection.map(entry => {
    const submitted = lines.find(l => l.taskId === entry.taskId);
    const task = researchTaskFor(researchModels().find(m => m.id === entry.modelId)!, entry.kind, entry.condition);
    return { ...entry, missing: !submitted, verdict: researchScore(task, submitted?.answer ?? null) };
  });
  const result = { selectionHash: digest(selection), cases: rows.length, rows };
  atomicJson(resolve(ARTIFACTS, 'research/external-scores.json'), result);
  return result;
}
