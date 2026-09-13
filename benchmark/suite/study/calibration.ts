import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { gunzipSync } from 'node:zlib';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { dataset } from '../v2/dataset';
import { caseSpecs, taskForV2 } from '../v2/cases';
import { sourceHashes } from '../v2/build';
import { STUDY, selection } from './protocol';
import { observabilityWitness } from './observability';

export function calibrationSelection() {
  const excluded = new Set(selection().map(s => s.group));
  for (const split of ['train', 'validation']) {
    const raw = gunzipSync(readFileSync(resolve(STUDY, 'training-data', split + '.jsonl.gz')));
    for (const line of raw.toString('utf8').trim().split('\n')) excluded.add(JSON.parse(line).group);
  }
  const available = dataset().filter(m => m.split === 'validation' && !excluded.has(m.group));
  const policies = [...new Set(available.map(m => m.policy))].sort();
  assert.equal(policies.length, 6, 'Policy-held-out families have no validation data');
  const objects = policies.flatMap(policy => {
    const pools = ['small', 'medium', 'large'].map(difficulty =>
      available.filter(m => m.policy === policy && m.difficulty === difficulty)
        .sort((a, b) => digest(`calibration-v1:${a.group}`).localeCompare(digest(`calibration-v1:${b.group}`))));
    const selected: typeof available = [];
    // Some policies have no medium/large objects; balance only available bins.
    while (selected.length < 6) {
      assert.ok(pools.some(pool => pool.length), `Insufficient validation objects: ${policy}`);
      for (const pool of pools) {
        if (pool.length && selected.length < 6) selected.push(pool.shift()!);
      }
    }
    return selected;
  });
  assert.equal(new Set(objects.map(m => m.group)).size, 36);
  const ids = new Set(objects.map(m => m.id));
  const cases = caseSpecs().filter(s => ids.has(s.modelId) && ['ordinary', 'default'].includes(s.condition));
  assert.equal(cases.length, 468);
  return { objects, cases, excluded: [...excluded].sort() };
}

export function freezeCalibration() {
  const { objects, cases, excluded } = calibrationSelection();
  const protocol = { version: 'calibration-v1', status: 'inputs-frozen-not-evaluated', sourceHashes: sourceHashes(),
    selectionUsesModelOutcomes: false, split: 'validation', excludedGroupsHash: digest(excluded),
    sourceGroups: objects.map(m => ({ id: m.id, group: m.group, policy: m.policy, difficulty: m.difficulty })),
    cases, hash: digest(cases), modelCalls: 0,
    scope: '36 previously unused validation objects, 6 per seen policy, round-robin across available piece-count bins. Missing bins are not invented. Development calibration only; not a new independent test or semantic dataset.',
    protocol: {
      primaryQuestion: 'Do format-valid outputs and visual similarity predict downstream structural success?',
      tracks: ['fixed-minimal-harness', 'constrained-decoding-separate-track', 'target-blind-feedback-separate-track'],
      reporting: ['all-response-denominators', 'format-conditional-diagnostics', 'source-group-paired-changes', 'per-policy-size-strata',
        'input-output-tokens', 'truncation', 'raw-responses', 'model-harness-separation'],
      confirmatoryTest: 'Not selected. Freeze a separately sourced, licensed test only after calibration. Existing public v2 is development evidence.',
      unknownHiddenState: 'Allow undetermined/set-valued answers or extra observations when admissible reconstructions disagree on the queried relation.',
      gates: ['Validate trivial symbolic interface controls before interpreting visual failure.',
        'No test-driven prompt selection. Record all calibration variants, including failures.',
        'No claim of semantic or causal transfer without independent objects, baseline comparisons and uncertainty.',
        'Human accept/reject judgments and source licensing remain external evidence requirements.'],
    } };
  const path = resolve(STUDY, 'calibration/protocol.json');
  if (existsSync(path)) assert.deepEqual(JSON.parse(readFileSync(path, 'utf8')), protocol, 'Frozen calibration changed');
  atomicJson(path, protocol);
  const questions = cases.map(spec => {
    const task = taskForV2(spec);
    return { caseId: spec.id, public: task.public, requiredViews: task.frames.map(f => ({ view: f.view, title: f.title })),
      imagesExported: false };
  });
  atomicJson(resolve(STUDY, 'calibration/questions.json'), questions);

  // This reviewer packet intentionally omits automatic verdicts and candidate sources.
  const witness = observabilityWitness();
  const packet = { version: 'observability-review-1', scope: 'One diagnostic family, not a representative dataset audit.',
    instructions: 'Inspect supplied structures independently; judge nominal geometry and whether the same visual evidence can determine the queried internal support. Null fields mean not reviewed. Record uncertainty rather than guessing.',
    items: [witness.target, witness.alternative].map((structure, i) => ({
      itemId: digest(`review-witness:${i}`).slice(0, 16), structure,
      questions: ['Is the structure nominally collision-free and supported?',
        'Which piece directly supports both blue pieces from below, or is there none?',
        'Can that shared-support answer be inferred uniquely from external assembled views and BOM alone?'],
    })).sort((a, b) => a.itemId.localeCompare(b.itemId)),
    completedIndependentReviews: 0,
    responseTemplate: { reviewerCode: null, itemId: null, nominallyValid: null, sharedSupportIds: null,
      identifiableFromExterior: null, rationale: null, uncertain: null },
    procedure: 'Two independent reviewers before discussion, retain disagreements, adjudicate separately. Do not distribute automated witness scores before labels are locked. Public source code can unblind this development packet.' };
  atomicJson(resolve(STUDY, 'calibration/reviewer-packet.json'), packet);
  return { validationObjects: objects.length, cases: cases.length, modelCalls: 0, humanReviews: 0, testFrozen: false };
}
