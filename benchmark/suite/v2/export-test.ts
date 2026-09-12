import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { PNG } from 'pngjs';
import { atomicJson } from '../../core/budget';
import { BENCHMARK } from '../storage';
import { digest } from '../data';
import { DIRECTORY, sourceHashes } from './build';
import { jsonLines } from './verify';
import { getSpec, taskForV2 } from './cases';

const dir = resolve(BENCHMARK, '.runtime/casebank-exports/selection-11834ad4590d368f');
const selection = JSON.parse(readFileSync(resolve(dir, 'selection.json'), 'utf8'));
const report = JSON.parse(readFileSync(resolve(dir, 'export.json'), 'utf8'));
assert.deepEqual(report.sourceHashes, sourceHashes());
const seen = new Set<string>(), images = new Set<string>();
for await (const row of jsonLines(resolve(dir, 'inputs.jsonl'))) {
  assert.ok(!seen.has(row.caseId)); seen.add(row.caseId);
  assert.deepEqual(row.input, taskForV2(getSpec(row.caseId)).public);
  assert.deepEqual(Object.keys(row).sort(), ['caseId', 'images', 'input', 'system']);
  assert.equal(row.images.length, row.input.imageTitles.length);
  for (const image of row.images) {
    const bytes = readFileSync(resolve(dir, image)), png = PNG.sync.read(bytes);
    assert.equal(digest(bytes.toString('base64')), image.slice(7, -4));
    assert.equal(png.width, 640); assert.equal(png.height, 480); images.add(image);
  }
}
assert.deepEqual([...seen], selection.caseIds);
const evidence = { checkedAt: new Date().toISOString(), inputs: seen.size, uniqueImages: images.size,
  allInputPayloadsMatch: true, allImageHashesMatch: true, hiddenFaultLabelsExcluded: true,
  scope: 'Two deterministic held-out objects across all 23 task conditions; full dataset images generated on demand.', apiRequests: 0 };
atomicJson(resolve(DIRECTORY, 'export-verification.json'), evidence); console.log(JSON.stringify(evidence, null, 2));
