import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { resolve, relative } from 'node:path';
import { createHash } from 'node:crypto';
import { atomicJson } from '../../core/budget';
import { STUDY } from './protocol';
import { localEvidenceRuns, replayLocalEvidence } from './local-evidence';
import { LOCAL_JOBS, localMatrixComplete } from './local-contract';
import { studyRuns } from './results';
import { SUITE } from '../storage';

const walk = (path: string): string[] => readdirSync(path).flatMap(name => {
  const file = resolve(path, name); return statSync(file).isDirectory() ? walk(file) : [file];
});
const evidenceNames = ['strict-audit.json', 'strict-roundtrip.json', 'mutation-audit.json',
  'independent-audit.json', 'exact-near-duplicates.json', 'connector-audit.json',
  'render-verification.json', 'training-bundle-verification.json', 'backend-corpus-check.json',
  'merge-verification.json', 'training-token-audit.json', 'test-token-audit.json'];
const evidence = Object.fromEntries(evidenceNames.map(name => [name, JSON.parse(readFileSync(resolve(STUDY, name), 'utf8'))]));
assert.equal(evidence['strict-audit.json'].oracleCases, 117910);
assert.deepEqual(evidence['strict-audit.json'].differences, []);
assert.equal(evidence['mutation-audit.json'].checks, 107520);
assert.equal(evidence['render-verification.json'].allImagesMatchTaskRecipes, true);
assert.equal(evidence['backend-corpus-check.json'].cases, 337);
assert.equal(evidence['backend-corpus-check.json'].allTokenAndPixelDigestsMatch, true);
assert.equal(evidence['training-bundle-verification.json'].hashesVerified, true);
assert.equal(evidence['training-token-audit.json'].cases, 840);
assert.equal(evidence['training-token-audit.json'].promptLabelsMasked, true);
const locals = localEvidenceRuns(), api = studyRuns();
const completedNames = locals.map(run => `${run.manifest.condition}-seed${run.manifest.seed}`);
const trainingMatrixComplete = localMatrixComplete(completedNames);
if (process.argv.includes('--require-complete')) assert.ok(trainingMatrixComplete, 'Training matrix is incomplete');
replayLocalEvidence();
const trained = completedNames.filter(name => name !== 'base-seed17').sort();
const merges = evidence['merge-verification.json'].runs;
assert.deepEqual(merges.map((run: any) => run.job).sort(), trained, 'Merge audit does not cover the published jobs');
assert.ok(merges.every((run: any) => run.passed === true && run.adaptedMatrices === 60
  && run.unchangedTensors === 411 && Number.isFinite(run.maxAbsoluteCPUMergeDifference)));
assert.equal(api.reduce((n, r) => n + r.rows.length, 0), 730);
assert.ok(api.every(r => r.status === 'complete'));
const files = walk(STUDY).filter(path => !path.endsWith('/release-manifest.json')
  && !relative(STUDY, path).startsWith('.local-import-'));
const sensitive = /sk-or-v1-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}|github_pat_[a-zA-Z0-9_]{20,}/;
for (const path of files.filter(p => /\.(json|jsonl|md|txt|tex)$/.test(p))) {
  const raw = readFileSync(path, 'utf8');
  assert.ok(!sensitive.test(raw), `Credential-like content in ${relative(STUDY, path)}`);
  assert.ok(!raw.includes('/Users/bytedance/'), `Machine-local path in ${relative(STUDY, path)}`);
}
const manifest = { checkedAt: new Date().toISOString(), completedLocalJobs: locals.length, plannedLocalJobs: LOCAL_JOBS.length,
  completedLocalJobNames: completedNames, pendingLocalJobs: LOCAL_JOBS.filter(name => !completedNames.includes(name)),
  trainingMatrixComplete, newPaidRequests: 730, credentialScanPassed: true,
  noMachineLocalPaths: true, evidence,
  sourceHashes: Object.fromEntries(walk(resolve(SUITE, 'study')).filter(path => /\.(ts|py|mjs|txt)$/.test(path)).map(path =>
    [relative(SUITE, path), createHash('sha256').update(readFileSync(path)).digest('hex')])),
  hashes: Object.fromEntries(files.map(path => [relative(STUDY, path),
    createHash('sha256').update(readFileSync(path)).digest('hex')])) };
atomicJson(resolve(STUDY, 'release-manifest.json'), manifest);
console.log(JSON.stringify({ files: files.length, completedLocalJobs: locals.length,
  trainingMatrixComplete, credentialScanPassed: true }));
