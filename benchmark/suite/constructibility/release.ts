import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { constructibilityCases, publicCase } from './cases';
import { clarificationOracle, evaluateConstructibility } from './evaluate';
import { VERSION, auditPlan, solvePlan } from './geometry';
import { frontierModels } from '../frontier/models';

export const OUTPUT = resolve(import.meta.dirname, '../../constructibility-v1');
const hash = (value: string) => createHash('sha256').update(value).digest('hex');
const write = (name: string, value: unknown) =>
  writeFileSync(resolve(OUTPUT, name), JSON.stringify(value, null, 2) + '\n');

function oracleFor(c: ReturnType<typeof constructibilityCases>[number]) {
  return c.kind === 'clarify-or-commit' ? clarificationOracle(c) : c.oracle;
}

export function exportConstructibility() {
  mkdirSync(OUTPUT, { recursive: true });
  const cases = constructibilityCases();
  const publicRows = cases.map(publicCase);
  const privateRows = cases.map(c => ({ id: c.id, sourceGroup: c.sourceGroup,
    kind: c.kind, oracle: oracleFor(c) }));
  const algorithmRows = cases.map(c => {
    const answer = oracleFor(c);
    const result = evaluateConstructibility(c, answer);
    assert.equal(result.success, 1, c.id);
    return { id: c.id, sourceGroup: c.sourceGroup, kind: c.kind,
      method: c.kind === 'clarify-or-commit' ? 'public-finite-world-enumerator' : 'public-constraint-solver',
      result };
  });
  const byKind = Object.fromEntries([...new Set(cases.map(c => c.kind))].map(kind =>
    [kind, cases.filter(c => c.kind === kind).length]));
  const plans = frontierModels().map(model => {
    const plan = solvePlan(model.structure.parts), audit = auditPlan(model.structure.parts, { steps: plan });
    return {
      sourceGroup: model.id,
      parts: model.structure.parts.length,
      steps: plan.length,
      prefixSupportScore: audit.prefixSupportScore,
      minimumSupportFraction: audit.minimumSupportFraction,
      accessibleStepRate: audit.accessibleStepRate,
      exact: audit.success,
    };
  });
  const shortcuts = {
    sequenceAlwaysValid: cases.filter(c => c.kind === 'sequence-audit'
      && evaluateConstructibility(c, {
        firstFailure: null, reason: null,
        legalPrefixLength: c.input.candidate.steps.length, constructible: true,
      }).success).length,
    recoveryNoOperation: cases.filter(c => c.kind === 'blocked-recovery'
      && evaluateConstructibility(c, {
        diagnosis: { failedId: c.input.failedStep.id, reason: 'tool_clearance' },
        recovery: [], continuation: [],
      }).success).length,
    stockoutUseUnavailable: cases.filter(c => c.kind === 'stockout-replan'
      && evaluateConstructibility(c, {
        placements: [{ part: c.input.unavailablePart, approach: 'west' }],
        continuation: [],
      }).success).length,
    clarificationAlwaysCommitH0: cases.filter(c => c.kind === 'clarify-or-commit'
      && evaluateConstructibility(c, {
        possibleIds: ['h0'],
        probabilities: Object.fromEntries(c.input.worlds.map(w => [w.id, Number(w.id === 'h0')])),
        decision: 'h0',
        nextQueryId: null,
      }).success).length,
  };
  const audit = {
    version: VERSION,
    status: 'public-development-not-confirmatory',
    sourceGroups: new Set(cases.map(c => c.sourceGroup)).size,
    records: cases.length,
    byKind,
    plans,
    shortcuts,
    claims: {
      measured: [
        'nominal per-prefix support and collision validity',
        'top-down body passage with one-stud side-tool clearance',
        'minimum local rollback under the declared discrete action model',
        'finite-stock exact-volume replacement',
        'finite-world posterior and cost-aware next-query selection',
      ],
      notMeasured: [
        'force balance or calibrated physical stability',
        'continuous robot motion, grasp success, or human ergonomics',
        'clutch force, tolerance, wear, vibration, or external load',
        'kinematic mechanisms such as gears, axles, and hinges',
        'open-world uncertainty or natural-image active perception',
      ],
    },
  };
  const protocol = {
    version: VERSION,
    frozenBeforeLearnedModelRuns: true,
    sourceStatus: 'Six previously public authored Frontier sources; development set only.',
    taskCounts: byKind,
    primaryEndpoints: {
      'sequence-audit': 'failure index + failure reason + constructible decision',
      'blocked-recovery': 'diagnosis + minimum legal recovery + legal continuation',
      'stockout-replan': 'stock-valid minimum cover + legal continuation',
      'clarify-or-commit': 'admissible set + uniform posterior + calibrated decision + optimal next query',
    },
    reporting: [
      'Keep four task families separate; no weighted overall score.',
      'Use source-grouped statistics; derived conditions are not independent samples.',
      'Separate raw model output from parser, planner, and tool-assisted results.',
      'Missing, malformed, truncated, duplicate, and unknown-ID submissions remain in denominators.',
      'Report symbolic results as symbolic reasoning, not image-only or physical-robot performance.',
    ],
    geometry: {
      coordinates: 'integer X/Z studs and Y plate heights',
      insertion: 'top-down body sweep',
      releaseClearance: 'one empty stud strip on one named side above the target base',
      support: 'at least one directly supporting stud',
      caveat: 'deterministic nominal proxy; not calibrated mechanics or robot kinematics',
    },
    costs: { inputTokens: null, outputTokens: null, latencyMs: null, billedUsd: null },
    modelResults: null,
    humanCalibration: null,
    independentConfirmation: null,
  };
  const sources = ['geometry.ts', 'cases.ts', 'evaluate.ts', 'score.ts', 'release.ts'];
  const sourceManifest = Object.fromEntries(sources.map(name =>
    [name, hash(readFileSync(resolve(import.meta.dirname, name), 'utf8'))]));
  write('public.json', publicRows);
  write('oracle-private.json', privateRows);
  write('algorithm-results.json', algorithmRows);
  write('audit.json', audit);
  write('frozen-protocol.json', protocol);
  write('source-manifest.json', sourceManifest);
  const releaseFiles = ['README.md', 'public.json', 'oracle-private.json', 'algorithm-results.json',
    'audit.json', 'frozen-protocol.json', 'source-manifest.json'];
  write('manifest.json', {
    version: VERSION,
    publicSha256: hash(JSON.stringify(publicRows)),
    oracleSha256: hash(JSON.stringify(privateRows)),
    protocolSha256: hash(JSON.stringify(protocol)),
    files: releaseFiles,
    fileSha256: Object.fromEntries(releaseFiles.map(name =>
      [name, hash(readFileSync(resolve(OUTPUT, name), 'utf8'))])),
  });
  console.log(JSON.stringify({ version: VERSION, records: cases.length, sourceGroups: audit.sourceGroups,
    byKind, shortcuts }));
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(import.meta.filename)) {
  exportConstructibility();
}
