import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';

const here = import.meta.dirname, root = resolve(here, '..');
const read = p => readFileSync(resolve(root, p), 'utf8');
const sha = p => createHash('sha256').update(readFileSync(resolve(root, p))).digest('hex');
const gallery = JSON.parse(read('review-gallery/verification.json'));
for (const [p, hash] of Object.entries(gallery.sha256)) {
  assert.equal(sha('review-gallery/' + p), hash, p);
}
assert.equal(gallery.authoredModels, 18);
assert.equal(gallery.controlCases, 36);
assert.equal(gallery.proceduralModelsRendered, 5120);
assert.equal(gallery.proceduralCaseLinks, 10240);
assert.deepEqual(gallery.blankImages, []);
const sources = ['paper/main.tex', 'paper/supplement.tex', 'paper/reference-manual.tex', 'paper/frontier-manual.tex', 'paper/diagnostic-manual.tex'];
const keys = [...read('paper/references.bib').matchAll(/@\w+\{([^,]+),/g)].map(m => m[1]);
assert.equal(new Set(keys).size, keys.length);
const used = new Set(sources.flatMap(p => [...read(p).matchAll(/\\cite(?:\[[^\]]*\])?\{([^}]+)\}/g)]
  .flatMap(m => m[1].split(','))));
assert.deepEqual([...used].filter(k => !keys.includes(k)), []);
assert.deepEqual(keys.filter(k => !used.has(k)), []);
let links = 0;
for (const path of ['REVIEW_REPORT.zh-CN.md', 'review-gallery/REPORT.zh-CN.md']) {
  for (const match of read(path).matchAll(/!?\[[^\]]*\]\(([^)]+)\)/g)) {
    const url = match[1];
    if (url.includes('://') || url.startsWith('#')) continue;
    assert.ok(existsSync(resolve(root, path, '..', url.split('#')[0])), `${path}: ${url}`);
    links++;
  }
}
const result = { citations: keys.length, usedCitations: used.size, undefinedCitations: 0,
  allModels: 5138, authoredModels: 18, proceduralModels: 5120, scoredControlPairs: 36,
  localReportLinks: links, modelInferences: 0,
  galleryVerificationSha256: sha('review-gallery/verification.json'),
  referenceManualSha256: sha('paper/reference-manual.tex'),
  caseStudiesSha256: sha('paper/tables/review-case-studies.tex'),
  bibliographySha256: sha('paper/references.bib'),
  note: 'Citation-key integrity and gallery hashes; not proof of human semantic validity or externally replicated inference.' };
writeFileSync(resolve(here, 'review-evidence.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result));
