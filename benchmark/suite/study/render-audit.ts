import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { gunzipSync } from 'node:zlib';
import { atomicJson } from '../../core/budget';
import { BENCHMARK, SYSTEM } from '../storage';
import { SuiteRenderer } from '../render';
import { digest } from '../data';
import { getSpec, taskForV2 } from '../v2/cases';
import { STUDY, selection, type Prepared } from './protocol';

const { url } = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
const renderer = new SuiteRenderer(url), cache = new Map<string, string>();
const prepared: Prepared[] = JSON.parse(readFileSync(resolve(STUDY, 'inputs/prepared.json'), 'utf8'));
const publicRows = readFileSync(resolve(STUDY, 'inputs/public.jsonl'), 'utf8').trim().split('\n').map(l => JSON.parse(l));
assert.deepEqual(prepared.map(r => r.spec), selection());
assert.deepEqual(publicRows, prepared.map(r => ({ caseId: r.spec.id, system: SYSTEM, input: r.input, images: r.images })));
const trainingRows = ['train', 'validation'].flatMap(split =>
  gunzipSync(readFileSync(resolve(STUDY, 'training-data', split + '.jsonl.gz'))).toString('utf8').trim().split('\n').map(l => JSON.parse(l)));
const rows = [...prepared.map(r => ({ caseId: r.spec.id, input: r.input, images: r.images })),
  ...trainingRows.map(r => ({ caseId: r.caseId, input: r.input, images: r.images }))];
let imageUses = 0, cases = 0;
try {
  for (const row of rows) {
    const task = taskForV2(getSpec(row.caseId));
    assert.deepEqual(row.input, task.public); assert.equal(row.images.length, task.frames.length);
    for (const [index, frame] of task.frames.entries()) {
      const key = digest(frame);
      if (!cache.has(key)) cache.set(key, (await renderer.render(frame)).hash);
      assert.equal(row.images[index], `images/${cache.get(key)}.png`, `${row.caseId}: frame ${index}`);
      imageUses++;
    }
    cases++;
    if (cases % 100 === 0) console.log(JSON.stringify({ cases, total: rows.length, uniqueRenders: cache.size }));
  }
} finally { await renderer.close(); }
const result = { checkedAt: new Date().toISOString(), cases, testCases: prepared.length, trainingAndValidationCases: trainingRows.length,
  imageUses, uniqueRenders: cache.size, allImagesMatchTaskRecipes: true, publicPayloadsExact: true,
  scope: 'Same pinned renderer/browser on this machine; not cross-GPU raster identity.', apiRequests: 0 };
atomicJson(resolve(STUDY, 'render-verification.json'), result);
console.log(JSON.stringify(result));
