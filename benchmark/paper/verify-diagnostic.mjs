import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
const root = resolve(import.meta.dirname, '..'), data = resolve(root, 'diagnostic-v2');
const read = p => JSON.parse(readFileSync(resolve(data, p), 'utf8'));
const hash = b => createHash('sha256').update(b).digest('hex');
const verification = read('verification.json'), protocol = read('frozen-protocol.json'), rows = read('public.json');
assert.equal(verification.version, 'brickatlas-diagnostic-2');
assert.equal(rows.length, 138);
assert.equal(new Set(rows.map(r => r.id)).size, rows.length);
assert.equal(new Set(rows.map(r => r.sourceGroup)).size, 6);
assert.equal(hash(JSON.stringify(rows)), protocol.publicPayloadSha256);
for (const [path, sha] of Object.entries(verification.files))
  assert.equal(hash(readFileSync(resolve(data, path))), sha, path);
for (const [path, sha] of Object.entries(read('source-manifest.json')))
  assert.equal(hash(readFileSync(resolve(root, 'suite/frontier2', path))), sha, path);
for (const row of rows) {
  assert.ok(!Object.hasOwn(row, 'oracle') && !Object.hasOwn(row, 'case'));
  if (row.condition === 'layers') {
    assert.ok(!Object.hasOwn(row.input, 'reference'));
    for (const image of row.input.referenceImages) assert.ok(existsSync(resolve(data, image.path)), image.path);
  }
}
const audit = read('audit.json');
assert.equal(audit.oldSetSuccess, 0);
assert.equal(audit.bestFixedSetSuccess, 2);
assert.equal(audit.bestFixedPolicySuccess, 3);
assert.equal(audit.deadlineSerialSuccess, 0);
assert.equal(read('stage-public.json').length, 216);
assert.equal(read('visual-scores.json').strata['maintenance:layers'].success, 36);
assert.ok(read('human-review-template.json').every(r => r.reviewerId === null && r.correctness === null));
const report = readFileSync(resolve(root, 'DIAGNOSTIC_UPGRADE.zh-CN.md'), 'utf8');
for (const [, path] of report.matchAll(/!?\[[^\]]*\]\(([^)]+)\)/g))
  if (!path.includes('://')) assert.ok(existsSync(resolve(root, path)), path);
console.log(JSON.stringify({ verified: true, records: 138, stageViews: 216, sourceGroups: 6,
  fixedSet: '2/18', fixedTree: '3/18', oldSet: '0/18', visualControl: '36/36', modelInferences: 0 }));
