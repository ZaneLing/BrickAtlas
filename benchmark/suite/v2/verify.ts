import assert from 'node:assert/strict';
import { createReadStream, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createGunzip } from 'node:zlib';
import { createInterface } from 'node:readline';
import { createHash } from 'node:crypto';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { DIRECTORY, sourceHashes } from './build';
import { caseSpecs, getSpec, taskForV2 } from './cases';
import { groundTruth } from './ground-truth';
import { dataset } from './dataset';

export async function* jsonLines(path: string) {
  const input = createReadStream(path);
  const stream = path.endsWith('.gz') ? input.pipe(createGunzip()) : input;
  for await (const line of createInterface({ input: stream, crlfDelay: Infinity })) if (line.trim()) yield JSON.parse(line);
}
export async function verifyCasebank() {
  const manifest = JSON.parse(readFileSync(resolve(DIRECTORY, 'manifest.json'), 'utf8'));
  assert.deepEqual(sourceHashes(), manifest.sourceHashes);
  assert.equal(digest(dataset()), manifest.datasetHash);
  assert.equal(digest(caseSpecs()), manifest.caseSpecHash);
  const hashes = new Map<string, string>(), seen = new Set<string>();
  let rowsChecked = 0, truths = 0, inputs = 0, renders = 0;
  for await (const row of jsonLines(resolve(DIRECTORY, 'case-index.jsonl.gz'))) {
    assert.ok(!hashes.has(row.id)); hashes.set(row.id, row.groundTruthHash);
  }
  assert.equal(hashes.size, manifest.cases);
  for (const shard of manifest.shards) {
    const path = resolve(DIRECTORY, shard.filename);
    assert.equal(createHash('sha256').update(readFileSync(path)).digest('hex'), shard.compressedSha256);
    const hash = createHash('sha256'); let count = 0;
    const stream = createReadStream(path).pipe(createGunzip());
    for await (const line of createInterface({ input: stream, crlfDelay: Infinity })) {
      hash.update(line + '\n'); const row = JSON.parse(line); count++;
      if (shard.filename.startsWith('ground-truth-')) {
        assert.ok(!seen.has(row.caseId)); seen.add(row.caseId);
        assert.equal(digest(row), hashes.get(row.caseId));
        const regenerated = groundTruth(taskForV2(getSpec(row.caseId)));
        assert.deepEqual(row, regenerated); truths++;
      } else if (shard.filename.startsWith('inputs-')) {
        const t = taskForV2(getSpec(row.caseId)); assert.deepEqual(t.public, row.input);
        assert.ok(!('target' in row) && !('oracle' in row) && !('frames' in row) && !('spec' in row)); inputs++;
      } else if (shard.filename.startsWith('render-private-')) {
        assert.deepEqual(row.frames, taskForV2(getSpec(row.caseId)).frames); renders++;
      }
    }
    assert.equal(count, shard.rows); assert.equal(hash.digest('hex'), shard.jsonlSha256); rowsChecked += count;
    console.log(JSON.stringify({ verifiedShard: shard.filename, count }));
  }
  assert.equal(truths, manifest.cases); assert.equal(inputs, truths); assert.equal(renders, truths);
  const evidence = { version: manifest.version, checkedAt: new Date().toISOString(), shards: manifest.shards.length,
    rowsChecked, groundTruthsRegenerated: truths, publicInputsVerified: inputs, renderRecipesVerified: renders,
    sourceHashesMatch: true, everyCaseHashVerified: true, missingOrDuplicateCases: 0, apiRequests: 0, humanReviews: 0 };
  atomicJson(resolve(DIRECTORY, 'verification.json'), evidence); return evidence;
}
