import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { resolve, relative } from 'node:path';
import { createHash } from 'node:crypto';
import { atomicJson } from '../../core/budget';
import { STUDY } from './protocol';
import { localEvidenceRuns, replayLocalEvidence } from './local-evidence';
import { LOCAL_JOBS, localMatrixComplete } from './local-contract';
import { studyRuns } from './results';
import { SUITE } from '../storage';
import { replayInterfaceProbes } from './interface-probes';
import { verifyCalibrationInputs } from './calibration-export';
import { replayModelValidation } from './model-validation';
import { replayLadder } from './reconstruction-ladder';
import { replayPoseProbes } from './pose-run';
import { replayOrderStudy } from './order-run';
import { researchReadiness } from './readiness';
import { verifyHumanCalibration } from './human-calibration-run';
import { reportVisualChoice } from './visual-choice-report';

const walk = (path: string): string[] => readdirSync(path).flatMap(name => {
  const file = resolve(path, name); return statSync(file).isDirectory() ? walk(file) : [file];
});
const evidenceNames = ['strict-audit.json', 'strict-roundtrip.json', 'mutation-audit.json',
  'independent-audit.json', 'exact-near-duplicates.json', 'connector-audit.json',
  'render-verification.json', 'training-bundle-verification.json', 'backend-corpus-check.json',
  'merge-verification.json', 'training-token-audit.json', 'test-token-audit.json',
  'failure-diagnostics.json', 'observability-witness.json', 'calibration/protocol.json',
  'calibration/input-verification.json', 'ui/verification.json', 'clean-verification.json'];
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
assert.equal(evidence['failure-diagnostics.json'].rows.length, 4100);
assert.equal(evidence['observability-witness.json'].scores.ordinary.metrics.success, 1);
assert.equal(evidence['observability-witness.json'].scores.symbolic.metrics.success, 0);
assert.equal(evidence['calibration/protocol.json'].status, 'inputs-frozen-not-evaluated');
assert.equal(evidence['calibration/protocol.json'].cases.length, 468);
assert.equal(evidence['ui/verification.json'].cases, 730);
assert.equal(evidence['ui/verification.json'].localCases, 3370);
assert.deepEqual(evidence['ui/verification.json'].errors, []);
assert.equal(evidence['clean-verification.json'].passed, true);
assert.ok(evidence['clean-verification.json'].commands.includes('verify-calibration'));
assert.deepEqual(verifyCalibrationInputs(), evidence['calibration/input-verification.json']);
assert.equal(replayInterfaceProbes().actualModelCalls, 36);
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
const validation = existsSync(resolve(STUDY, 'model-validation/run.json')) ? replayModelValidation() : null;
const ladder = existsSync(resolve(STUDY, 'model-validation/ladder/run.json')) ? replayLadder() : null;
const normalized = existsSync(resolve(STUDY, 'model-validation/ladder-normalized/run.json')) ? replayLadder(true) : null;
const pose = existsSync(resolve(STUDY, 'pose-probes/run.json')) ? replayPoseProbes() : null;
const order = existsSync(resolve(STUDY, 'order-study/run.json')) ? replayOrderStudy() : null;
const orderAnalysis = order ? JSON.parse(readFileSync(resolve(STUDY, 'order-study/analysis.json'), 'utf8')) : null;
if (order) {
  assert.equal(order.status, 'complete');
  assert.equal(order.responses, 192);
  assert.equal(order.sourceGroups, 12);
  assert.ok(evidence['clean-verification.json'].commands.includes('replay-order-study'));
}
for (const command of ['exposure-audit', 'human-audit-status', 'research-readiness']) {
  assert.ok(evidence['clean-verification.json'].commands.includes(command));
}
const humanCalibration = verifyHumanCalibration();
assert.ok(evidence['clean-verification.json'].commands.includes('verify-human-calibration'));
const visualChoice = existsSync(resolve(STUDY, 'visual-choice/run.json')) ? await reportVisualChoice() : null;
if (visualChoice) assert.ok(evidence['clean-verification.json'].commands.includes('report-visual-choice'));
const readiness = researchReadiness();
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
  additionalValidation: validation, additionalLadder: ladder ? {
    status: ladder.status, responses: ladder.responses, newCost: ladder.newCost, sourceGroups: ladder.sourceGroups,
  } : null,
  normalizedLadder: normalized ? { status: normalized.status, responses: normalized.responses,
    newCost: normalized.newCost, sourceGroups: normalized.sourceGroups } : null,
  poseProbes: pose ? { status: pose.status, responses: pose.responses, newCost: pose.newCost } : null,
  orderStudy: order ? { status: order.status, responses: order.responses,
    sourceGroups: order.sourceGroups, newCost: orderAnalysis.newCost } : null,
  researchReadiness: { allPassed: readiness.allPassed, passed: readiness.passed, pending: readiness.pending },
  humanCalibration: { packetHash: humanCalibration.packetHash, frozenReferenceVerified: humanCalibration.verified,
    humanLabelsVerified: false, items: humanCalibration.items, sourceGroups: humanCalibration.sourceGroups },
  visualChoice: visualChoice ? { status: visualChoice.status, predictions: visualChoice.predictions,
    replacements: visualChoice.replacements, renders: visualChoice.renders, apiRequests: 0 } : null,
  noMachineLocalPaths: true,
  evidence: Object.fromEntries(Object.entries(evidence).map(([name, report]) => [name,
    name === 'failure-diagnostics.json'
      ? { version: report.version, responses: report.rows.length, strata: report.groups.length, apiRequests: report.apiRequests }
      : report])),
  sourceHashes: Object.fromEntries(walk(resolve(SUITE, 'study')).filter(path => /\.(ts|py|mjs|txt)$/.test(path)).map(path =>
    [relative(SUITE, path), createHash('sha256').update(readFileSync(path)).digest('hex')])),
  hashes: Object.fromEntries(files.map(path => [relative(STUDY, path),
    createHash('sha256').update(readFileSync(path)).digest('hex')])) };
atomicJson(resolve(STUDY, 'release-manifest.json'), manifest);
console.log(JSON.stringify({ files: files.length, completedLocalJobs: locals.length,
  trainingMatrixComplete, credentialScanPassed: true, researchReady: readiness.allPassed }));
