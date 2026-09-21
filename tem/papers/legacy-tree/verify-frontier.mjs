import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
const root = resolve(import.meta.dirname, '..');
const read = p => JSON.parse(readFileSync(resolve(root, p), 'utf8'));
const sha = p => createHash('sha256').update(readFileSync(resolve(root, p))).digest('hex');
const manifest = read('frontier-cases/manifest.json'), evidence = read('paper/frontier-evidence.json');
assert.equal(manifest.version, 'brickatlas-frontier-1');
assert.equal(manifest.models.length, 6);
assert.equal(manifest.cases, 48);
assert.equal(manifest.placedParts, 1509);
for (const [p, hash] of Object.entries(manifest.files)) assert.equal(sha('frontier-cases/' + p), hash, p);
for (const [p, hash] of Object.entries(manifest.sourceHashes)) assert.equal(sha('suite/frontier/' + p), hash, p);
assert.equal(sha('frontier-cases/manifest.json'), evidence.manifestSha256);
assert.equal(sha('suite/frontier/compose.py'), evidence.generatorSha256);
for (const [p, hash] of Object.entries(evidence.outputs)) assert.equal(sha(p), hash, p);
const rows = read('frontier-cases/baselines.json'), cases = read('frontier-cases/cases.json');
assert.equal(rows.length, 48);
assert.ok(rows.every(r => r.solver.success === 1 && r.modelInference === false));
assert.ok(cases.every(c => c.good.success === 1 && c.bad.success === 0));
for (const c of cases) {
  const pub = read('frontier-cases/' + c.stem + '-public.json');
  assert.ok(!('oracle' in pub) && !('negative' in pub) && !('highlight' in pub));
}
let links = 0;
for (const path of ['FRONTIER_REPORT.zh-CN.md', 'frontier-cases/REPORT.zh-CN.md']) {
  const text = readFileSync(resolve(root, path), 'utf8');
  for (const [, url] of text.matchAll(/!?\[[^\]]*\]\(([^)]+)\)/g)) {
    if (url.includes('://')) continue;
    assert.ok(existsSync(resolve(root, path, '..', url)), url); links++;
  }
}
console.log(JSON.stringify({ verified: true, models: 6, cases: 48, parts: 1509,
  publicSolver: 48, controlPairs: 48, reportLinks: links, modelInferences: 0 }));
