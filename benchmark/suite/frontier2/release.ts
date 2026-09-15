import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { maintenanceCases, publicMaintenance, scoreMaintenance, solveSymbolic, VERSION } from './maintenance';
import { observationCases, admissible, optimalPolicy, evaluatePolicy, scan } from './observation';
import { frontierModels } from '../frontier/models';
import { frontierTasks } from '../frontier/tasks';
import { sameSet } from '../frontier/tasks';
import { schedule } from '../frontier/geometry';
import { evaluateFrontier } from '../frontier/evaluate';
import { poseCases, publicPose, scorePose } from './pose';

export const OUTPUT = resolve(import.meta.dirname, '../../diagnostic-v2');
const hash = (x: string) => createHash('sha256').update(x).digest('hex');
const write = (name: string, value: unknown) => writeFileSync(resolve(OUTPUT, name), JSON.stringify(value, null, 2) + '\n');
export function schedulingCases() {
  return frontierModels().flatMap(m => [2, 4, 8].map(workers => {
    const base = frontierTasks().find(t => t.modelId === m.id && t.kind === 'parallel-schedule')!;
    const batches = schedule(m.structure.parts, workers);
    return { ...base, id: `f2-${m.id}-schedule-${workers}`, input: {
      ...base.input, structure: m.structure, workers, maxRounds: batches.length,
    }, prompt: base.prompt + ` Deadline ${batches.length} rounds is mandatory; a feasible witness exists.
This is not a proven optimal deadline. Score legality, coverage and deadline separately.`,
    oracle: { batches } };
  }));
}
export function scoreSchedule(c: ReturnType<typeof schedulingCases>[number], answer: unknown) {
  const base = evaluateFrontier(c, answer);
  const makespan = base.metrics.makespan ?? Infinity;
  return { ...base, success: Number(base.success && makespan <= c.input.maxRounds),
    deadlineMet: Number(Number.isFinite(makespan) && makespan <= c.input.maxRounds) };
}

export function exportRelease() {
  mkdirSync(OUTPUT, { recursive: true }); mkdirSync(resolve(OUTPUT, 'images'), { recursive: true });
  const ms = maintenanceCases(), os = observationCases(), ss = schedulingCases();
  const publicRows: any[] = [], privateRows: any[] = [], algorithmRows: any[] = [];
  for (const c of ms) {
    for (const condition of ['symbolic', 'layers'] as const) {
      const pub = publicMaintenance(c, condition);
      publicRows.push({ ...pub, kind: 'maintenance' });
      privateRows.push({ id: pub.id, case: c, oracle: c.oracle });
      const result = scoreMaintenance(c, solveSymbolic({ current: c.current, reference: c.target }));
      assert.equal(result.success, 1, c.id);
      algorithmRows.push({ id: pub.id, kind: 'maintenance', condition,
        result: condition === 'symbolic' ? result : null,
        method: condition === 'symbolic' ? 'public-symbolic-solver' : 'unmeasured-image-baseline' });
    }
  }
  const answers = os.map(c => ({ possibleIds: admissible(c.input).map(w => w.id) }));
  const policies = os.map(c => optimalPolicy(c.input).policy);
  for (const [index, c] of os.entries()) {
    for (const kind of ['admissible-set', 'scan-policy'] as const) {
      const input = structuredClone(c.input);
      if (kind === 'scan-policy') input.observed = [];
      const pub = { version: VERSION, id: c.id + '-' + kind, sourceGroup: c.sourceGroup, kind,
        prompt: `Candidate worlds contain complete nominal geometry. A section scan at bottom Y walks integer
cells along axis X or Z and returns ordered runs 'brick:N' or 'gap:N'; adjacent cells in the same
part merge; different adjacent parts do not merge. IDs and colors do not enter scan values.
Queries have stated integer costs. There is NO precomputed answer table.
${kind === 'admissible-set' ? 'Return {possibleIds} for all worlds consistent with the supplied observations.'
    : 'Return {queryId,branches:{scanValue:subpolicy}} or {hypothesisId}. Identify ALL worlds within the worst-case budget, with no repeated queries on a path. No prior observation is supplied.'}`,
        input };
      publicRows.push(pub);
      const answer = kind === 'admissible-set' ? answers[index] : policies[index];
      privateRows.push({ id: pub.id, case: c, oracle: answer });
      algorithmRows.push({ id: pub.id, kind, condition: 'geometry', method: 'public-geometry-enumerator',
        result: kind === 'scan-policy' ? evaluatePolicy(input, answer) : { success: 1 } });
    }
  }
  for (const c of ss) {
    publicRows.push({ version: VERSION, id: c.id, sourceGroup: c.modelId, kind: 'deadline-schedule',
      prompt: c.prompt, input: c.input });
    privateRows.push({ id: c.id, case: c, oracle: c.oracle });
    assert.equal(scoreSchedule(c, c.oracle).success, 1);
    algorithmRows.push({ id: c.id, kind: 'deadline-schedule', condition: 'symbolic', method: 'public-list-schedule',
      result: scoreSchedule(c, c.oracle) });
  }
  for (const c of poseCases()) for (const condition of ['symbolic', 'layers'] as const) {
    const pub = publicPose(c, condition);
    publicRows.push(pub); privateRows.push({ id: pub.id, case: c, oracle: c.oracle });
    assert.equal(scorePose(c, c.oracle).success, 1);
    algorithmRows.push({ id: pub.id, kind: 'pose-patch', condition, method: 'unmeasured-mixed-pose-baseline', result: null });
  }
  const setTransfer = answers.map(answer => os.map(c => Number(sameSet(answer.possibleIds, admissible(c.input).map(w => w.id)))));
  const policyTransfer = policies.map(answer => os.map(c => evaluatePolicy(c.input, answer).success));
  // Keep common h/q IDs: this transfer audit would otherwise be trivially defeated by renaming.
  const oldSet = ['h0', 'h2', 'h4', 'h6'];
  const wrongCoherent = { diagnosis: { faultIds: [], replacements: [] }, access: { removeIds: [], order: [] }, repair: { actions: [] } };
  const nontrivial = ms.find(c => c.faultIds.length && c.context === 'full')!;
  const contradictory = structuredClone(nontrivial.oracle); contradictory.diagnosis = { faultIds: [], replacements: [] };
  const audit = {
    version: VERSION, sourceGroups: 6, publicRecords: publicRows.length, modelInferences: 0,
    setTransfer, policyTransfer,
    bestFixedSetSuccess: Math.max(...setTransfer.map(row => row.reduce((a, b) => a + b, 0))),
    bestFixedPolicySuccess: Math.max(...policyTransfer.map(row => row.reduce((a, b) => a + b, 0))),
    observationCases: os.length,
    oldSetSuccess: os.filter(c => sameSet(oldSet, admissible(c.input).map(w => w.id))).length,
    geometryAblation: 'No precomputed partitions in input. Geometry-blind fixed-answer transfer is measured above; learned geometry ablation is unmeasured.',
    contradictory: scoreMaintenance(nontrivial, contradictory),
    consistentlyWrong: scoreMaintenance(nontrivial, wrongCoherent),
    deadlineSerialSuccess: ss.filter(c => scoreSchedule(c, { batches: c.input.structure.parts.map((p: any) => [p.id]) }).success).length,
    matchedContextPairs: ms.filter(c => c.context === 'full').map(c => {
      const local = ms.find(l => l.sourceGroup === c.sourceGroup && l.tier === c.tier && l.context === 'local')!;
      assert.deepEqual(c.oracle, local.oracle);
      return { sourceGroup: c.sourceGroup, tier: c.tier, fullParts: c.factors.totalParts,
        localParts: local.factors.totalParts, identicalAnswer: true, ...c.factors };
    }),
    observationFactors: os.map(c => ({ id: c.id, sourceGroup: c.sourceGroup, tier: c.tier,
      worlds: c.input.worlds.length, queries: c.input.queries.length, optimumCost: c.input.budget,
      uniqueQueryPartitions: new Set(c.input.queries.map(q => c.input.worlds.map(w => scan(w.parts, q)).join(';'))).size,
      answerSize: admissible(c.input).length })),
  };
  assert.ok(audit.bestFixedSetSuccess < os.length / 2);
  assert.ok(audit.bestFixedPolicySuccess < os.length / 2);
  assert.equal(audit.contradictory.coherent, 0);
  assert.equal(audit.consistentlyWrong.coherent, 1);
  assert.equal(audit.consistentlyWrong.success, 0);
  assert.equal(audit.deadlineSerialSuccess, 0);
  write('public.json', publicRows); write('review-private.json', privateRows);
  write('stage-public.json', publicRows.filter(r => r.kind === 'maintenance').flatMap(r =>
    ['diagnosis', 'access', 'repair'].map(stage => ({
      ...r, parentId: r.id, id: `${r.id}/${stage}`, stage,
      prompt: r.prompt + `\nIndependent-stage evaluation: return ONLY the ${stage} object, not the other stages.
Do not consume answers from other requests. Current/reference information stays identical.`,
    }))));
  write('algorithm-results.json', algorithmRows); write('audit.json', audit);
  write('frozen-protocol.json', {
    version: VERSION, status: 'public-development-not-confirmatory', frozenBeforeNewModelInferences: true,
    recordCount: publicRows.length, sourceGroups: 6,
    publicPayloadSha256: hash(JSON.stringify(publicRows)),
    sourceGroupPolicy: 'All tiers, contexts, modalities and counterfactuals from one authored source stay grouped.',
    heldOutEvaluation: 'Leave-one-source-out adapters are allowed; these six public authored sources are NOT independent confirmation.',
    primaryEndpoint: 'allCorrectAndCoherent for maintenance; separate per-condition scores',
    secondary: ['diagnosisExact', 'accessExact', 'repairExact', 'minimumRepair', 'coherent', 'policyCoverage', 'deadlineMet'],
    baselines: ['fixed-answer-transfer', 'no-operation', 'public-symbolic', 'known-renderer-color', 'serial-schedule'],
    experiments: ['matched local/full context with identical answer', 'symbolic/layer-reference pairing',
      'geometry removal versus intact geometry', 'same-order repeat versus permutation'],
    costs: { inferenceLatencyMs: null, inputTokens: null, outputTokens: null, billedUsd: null, peakMemoryBytes: null },
    externalConfirmation: null, humanCalibration: null, modelResults: null,
    budgetRule: 'Determine context/output feasibility before model selection; freeze per-task caps identically across models. Truncation remains failure.',
  });
  write('human-review-template.json', ms.filter(c => c.context === 'full').map(c => ({
    caseId: c.id, reviewerId: null, correctness: null, relevance: null, difficulty: null,
    elapsedSeconds: null, notes: null,
  })));
  const sources = ['observation.ts', 'maintenance.ts', 'pose.ts', 'release.ts', 'score.ts', 'visual.py', 'render.ts', 'compose.py'];
  write('source-manifest.json', Object.fromEntries(sources.map(p => [p, hash(readFileSync(resolve(import.meta.dirname, p), 'utf8'))])));
  console.log(JSON.stringify({ records: publicRows.length, bestFixedSet: audit.bestFixedSetSuccess,
    bestFixedPolicy: audit.bestFixedPolicySuccess, denominator: os.length, oldSet: audit.oldSetSuccess }));
}
if (process.argv[1] && resolve(process.argv[1]) === resolve(import.meta.filename)) exportRelease();
