import assert from 'node:assert/strict';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { BENCHMARK, SYSTEM } from '../storage';
import { dataset, POLICIES } from '../v2/dataset';
import { caseSpecs, taskForV2 } from '../v2/cases';
import { digest } from '../data';
import { SuiteRenderer } from '../render';
import { STUDY, selection } from './protocol';

export async function prepareTraining() {
  const dir = resolve(BENCHMARK, '.runtime/study-training'); mkdirSync(resolve(dir, 'images'), { recursive: true });
  const modelIds: Record<string, Set<string>> = {};
  for (const [split, count] of [['train', 16], ['validation', 4]] as const) {
    modelIds[split] = new Set(POLICIES.slice(0, 6).flatMap(policy =>
      dataset().filter(m => m.split === split && m.policy === policy)
        .sort((a, b) => digest('sft-study:' + a.group).localeCompare(digest('sft-study:' + b.group)))
        .slice(0, count).map(m => m.id)));
  }
  const testGroups = new Set(selection().map(s => s.group));
  assert.ok(dataset().filter(m => modelIds.train.has(m.id)).every(m => !testGroups.has(m.group)));
  const selected = caseSpecs().filter(s => modelIds[s.split]?.has(s.modelId)
    && ['ordinary', 'default'].includes(s.condition)
    && (['reconstruct', 'generate', 'complete'].includes(s.kind)
      || s.kind === 'relations' && s.variant === 'contact'
      || s.kind === 'edit' && s.variant === 'rotate'
      || s.kind === 'plan' && s.variant === 'assemble'
      || s.kind === 'repair' && s.variant === 'color'));
  const info = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
  const renderer = new SuiteRenderer(info.url), cache = new Map<string, string>();
  const rows: Record<string, unknown[]> = { train: [], validation: [] };
  try {
    for (const [i, s] of selected.entries()) {
      const task = taskForV2(s), images = [];
      for (const f of task.frames) {
        const k = digest(f); let path = cache.get(k);
        if (!path) {
          const image = await renderer.render(f); path = `images/${image.hash}.png`;
          writeFileSync(resolve(dir, path), image.buffer); cache.set(k, path);
        }
        images.push(path);
      }
      rows[s.split].push({ caseId: s.id, group: s.group, split: s.split, kind: s.kind, system: SYSTEM,
        input: task.public, images, answer: task.oracle });
      if (i % 100 === 0) console.log(JSON.stringify({ trainingPrepared: i, total: selected.length }));
    }
  } finally { await renderer.close(); }
  for (const split of ['train', 'validation']) writeFileSync(resolve(dir, split + '.jsonl'), rows[split].map(r => JSON.stringify(r)).join('\n') + '\n');
  const manifest = { trainObjects: modelIds.train.size, validationObjects: modelIds.validation.size,
    trainRows: rows.train.length, validationRows: rows.validation.length, images: cache.size,
    testGroupsExcluded: true, splitUnit: 'source geometry', taskKinds: 7,
    note: 'Catalog recognition held out; seven assembly task families. VLM reads actual rendered PNGs. No target geometry injected into visual inputs.',
    hashes: Object.fromEntries(['train', 'validation'].map(s => [s, digest(rows[s])])),
    experiment: 'Small multimodal training pilot, not convergence or population confirmation.' };
  atomicJson(resolve(dir, 'manifest.json'), manifest); atomicJson(resolve(STUDY, 'training-data.json'), manifest);
  return manifest;
}
