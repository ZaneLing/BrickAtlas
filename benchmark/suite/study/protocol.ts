import { resolve } from 'node:path';
import { mkdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { atomicJson } from '../../core/budget';
import { dataset, POLICIES } from '../v2/dataset';
import { caseSpecs, taskForV2, type CaseSpec } from '../v2/cases';
import { sourceHashes } from '../v2/build';
import { ARTIFACTS, BENCHMARK, SYSTEM } from '../storage';
import { digest } from '../data';
import { SuiteRenderer } from '../render';

export const STUDY = resolve(ARTIFACTS, 'study');
export function selection() {
  const models = dataset().filter(m => m.split.startsWith('test_'));
  const selected = POLICIES.flatMap(policy => {
    const pool = models.filter(m => m.policy === policy).sort((a, b) => digest('study-v1:' + a.group).localeCompare(digest('study-v1:' + b.group)));
    const selected = new Set<string>();
    for (const difficulty of ['small', 'medium', 'large']) {
      const m = pool.find(m => m.difficulty === difficulty && !selected.has(m.id)) ?? pool.find(m => !selected.has(m.id))!;
      selected.add(m.id);
    }
    return [...selected];
  });
  const ids = new Set(selected);
  const cases = caseSpecs().filter(s => ids.has(s.modelId) && ['ordinary', 'default'].includes(s.condition));
  const catalog = caseSpecs().filter(s => s.kind === 'parts');
  const types = [...new Set(catalog.map(s => s.modelId.split('-')[1]))];
  cases.push(...types.map((type, i) => catalog.filter(s => s.modelId.split('-')[1] === type)[i % 6]));
  return cases;
}
export interface Prepared { spec: CaseSpec; input: ReturnType<typeof taskForV2>['public']; images: string[] }
export async function prepareStudy() {
  const cases = selection(), hash = digest(cases), dir = resolve(STUDY, 'inputs');
  mkdirSync(resolve(dir, 'images'), { recursive: true });
  const protocol = { version: 'study-v1', cases, hash, sourceHashes: sourceHashes(),
    settings: { temperature: 0, maxTokens: 2200, models: ['openai/gpt-4.1-mini', 'google/gemini-2.5-flash'] },
    scope: '24 source objects, three per policy with available size strata, plus 25 known catalog queries. All tasks, task-default inputs. Not a statistically powered population leaderboard.',
    selectionUsesOutcomes: false };
  if (existsSync(resolve(STUDY, 'protocol.json'))
    && digest(JSON.parse(readFileSync(resolve(STUDY, 'protocol.json'), 'utf8'))) !== digest(protocol)) throw new Error('Frozen protocol differs');
  atomicJson(resolve(STUDY, 'protocol.json'), protocol);
  const info = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
  const renderer = new SuiteRenderer(info.url), rows: Prepared[] = [], cache = new Map<string, string>();
  try {
    for (const [i, spec] of cases.entries()) {
      const task = taskForV2(spec), images = [];
      for (const f of task.frames) {
        const k = digest(f); let path = cache.get(k);
        if (!path) {
          const r = await renderer.render(f); path = `images/${r.hash}.png`; cache.set(k, path);
          writeFileSync(resolve(dir, path), r.buffer);
        }
        images.push(path);
      }
      rows.push({ spec, input: task.public, images });
      if (i % 50 === 0) console.log(JSON.stringify({ prepared: i, total: cases.length }));
    }
  } finally { await renderer.close(); }
  atomicJson(resolve(dir, 'prepared.json'), rows);
  writeFileSync(resolve(dir, 'public.jsonl'), rows.map(r => JSON.stringify({ caseId: r.spec.id, system: SYSTEM, input: r.input, images: r.images })).join('\n') + '\n');
  return { cases: rows.length, objects: new Set(rows.filter(r => r.spec.kind !== 'parts').map(r => r.spec.modelId)).size, images: cache.size };
}
