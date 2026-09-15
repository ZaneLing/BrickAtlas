import assert from 'node:assert/strict';
import test from 'node:test';
import { dims } from '../suite/geometry';
import { maintenanceCases, publicMaintenance, scoreMaintenance, solveSymbolic } from '../suite/frontier2/maintenance';
import { observationCases, admissible, optimalPolicy, evaluatePolicy, scan, ScanEpisode } from '../suite/frontier2/observation';
import { schedulingCases, scoreSchedule } from '../suite/frontier2/release';
import { scoreResponses, scoreStageResponses } from '../suite/frontier2/score';
import { sameSet } from '../suite/frontier/tasks';
import { poseCases, publicPose, scorePose } from '../suite/frontier2/pose';

test('diagnostic-v2: oracle chains are correct; local/full pairs preserve the exact answer', () => {
  const cases = maintenanceCases();
  assert.equal(cases.length, 36);
  for (const c of cases) {
    assert.equal(scoreMaintenance(c, c.oracle).success, 1, c.id);
    assert.equal(scoreMaintenance(c, solveSymbolic({ current: c.current, reference: c.target })).success, 1);
    if (c.context === 'full') {
      const local = cases.find(l => l.sourceGroup === c.sourceGroup && l.tier === c.tier && l.context === 'local')!;
      assert.deepEqual(c.oracle, local.oracle);
      assert.ok(c.factors.totalParts > local.factors.totalParts);
    }
  }
});

test('diagnostic-v2: malformed and missing stages fail; no-fault requires no intervention', () => {
  for (const c of maintenanceCases()) {
    for (const raw of [undefined, null, {}, [], { diagnosis: c.oracle.diagnosis }])
      assert.equal(scoreMaintenance(c, raw).success, 0);
  }
  const clean = maintenanceCases().find(c => c.faultIds.length === 0)!;
  assert.equal(scoreMaintenance(clean, clean.oracle).success, 1);
});

test('diagnostic-v2: coherence is neither individual nor joint correctness', () => {
  const c = maintenanceCases().find(c => c.tier === 2 && c.context === 'full')!;
  const wrong = { diagnosis: { faultIds: [], replacements: [] }, access: { removeIds: [], order: [] }, repair: { actions: [] } };
  const w = scoreMaintenance(c, wrong);
  assert.equal(w.coherent, 1); assert.equal(w.success, 0);
  const contradictory = structuredClone(c.oracle);
  contradictory.diagnosis = wrong.diagnosis;
  const r = scoreMaintenance(c, contradictory);
  assert.equal(r.repairExact, 1); assert.equal(r.accessExact, 1); assert.equal(r.coherent, 0);
});

test('diagnostic-v2: actions conserve inventory and reject duplicate placement and forged ID', () => {
  const c = maintenanceCases().find(c => c.tier === 2)!;
  const duplicate = structuredClone(c.oracle);
  duplicate.repair.actions.push(duplicate.repair.actions.at(-1)!);
  assert.equal(scoreMaintenance(c, duplicate).repairExact, 0);
  const forged = structuredClone(c.oracle);
  forged.repair.actions[0].id = 'invented';
  assert.equal(scoreMaintenance(c, forged).repairExact, 0);
  const budget = structuredClone(c.oracle);
  budget.repair.actions = [...budget.repair.actions, ...budget.repair.actions];
  assert.equal(scoreMaintenance(c, budget).minimumRepair, 0);
});

test('diagnostic-v2: image payload never contains reference JSON or private target IDs', () => {
  for (const c of maintenanceCases()) {
    const image = publicMaintenance(c, 'layers');
    assert.ok(!Object.hasOwn(image.input, 'reference'));
    assert.ok(!Object.hasOwn(image, 'oracle'));
    assert.ok(!Object.hasOwn(image, 'faultIds'));
    assert.ok('referenceImages' in image.input);
    const encoded = JSON.stringify(image.input.referenceImages);
    assert.ok(!encoded.includes('parts') && !encoded.includes('color'));
    assert.ok(image.input.referenceImages!.length > 0);
  }
});

test('diagnostic-v2: scan runs agree with independent interval intersection', () => {
  for (const c of observationCases()) for (const q of c.input.queries) for (const w of c.input.worlds) {
    const spans = w.parts.filter(p => p.y === q.y).flatMap(p => {
      const d = dims(p), a = q.axis === 'x' ? p.x : p.z, b = a + (q.axis === 'x' ? d.w : d.d);
      const perpendicular = q.axis === 'x' ? p.z : p.x, length = q.axis === 'x' ? d.d : d.w;
      return q.fixed >= perpendicular && q.fixed < perpendicular + length && b > q.start && a < q.end
        ? [{ start: Math.max(a, q.start), end: Math.min(b, q.end) }] : [];
    }).sort((a, b) => a.start - b.start);
    let cursor = q.start; const runs: string[] = [];
    for (const s of spans) {
      if (s.start > cursor) runs.push(`gap:${s.start - cursor}`);
      runs.push(`brick:${s.end - s.start}`); cursor = s.end;
    }
    if (cursor < q.end) runs.push(`gap:${q.end - cursor}`);
    assert.equal(scan(w.parts, q), runs.join('|'));
  }
});

test('diagnostic-v2: genuine grammar sizes and fixed-template transfer are bounded', () => {
  const cs = observationCases();
  assert.deepEqual([...new Set(cs.map(c => c.input.worlds.length))], [4, 6, 16]);
  const answers = cs.map(c => admissible(c.input).map(w => w.id));
  const best = Math.max(...answers.map(a => cs.filter(c => sameSet(a, admissible(c.input).map(w => w.id))).length));
  assert.equal(best, 2);
  assert.equal(cs.filter(c => sameSet(['h0', 'h2', 'h4', 'h6'], admissible(c.input).map(w => w.id))).length, 0);
  const policies = cs.map(c => optimalPolicy(c.input).policy);
  assert.ok(Math.max(...policies.map(p => cs.filter(c => evaluatePolicy(c.input, p).success).length)) <= 3);
});

test('diagnostic-v2: all-world policies, budget boundaries, episode query-return', () => {
  for (const c of observationCases()) {
    const p = optimalPolicy(c.input);
    assert.equal(evaluatePolicy(c.input, p.policy).success, 1);
    assert.equal(evaluatePolicy({ ...c.input, budget: p.cost - 1 }, p.policy).success, 0);
    assert.equal(evaluatePolicy(c.input, { hypothesisId: c.input.worlds[0].id }).success, 0);
  }
  const c = observationCases()[0], q = c.input.queries[0];
  const episode = new ScanEpisode(c.input, c.referenceWorldId);
  assert.equal(episode.query(q.id).value, scan(c.input.worlds.find(w => w.id === c.referenceWorldId)!.parts, q));
  assert.throws(() => episode.query(q.id));
  assert.equal(episode.submit(c.referenceWorldId).success, 1);
  assert.throws(() => episode.submit(c.referenceWorldId));
});

test('diagnostic-v2: candidate/query order is invariant; geometry removal destroys identifiability', () => {
  for (const c of observationCases()) {
    const reversed = { ...c.input, worlds: [...c.input.worlds].reverse(), queries: [...c.input.queries].reverse() };
    assert.ok(sameSet(admissible(c.input).map(w => w.id), admissible(reversed).map(w => w.id)));
    assert.equal(optimalPolicy(reversed).cost, optimalPolicy(c.input).cost);
    const blind = { ...c.input, worlds: c.input.worlds.map(w => ({ ...w, parts: [] })) };
    assert.equal(optimalPolicy(blind).cost, Infinity);
  }
});

test('diagnostic-v2: scheduling deadline rejects serial shortcut but not feasible parallel plans', () => {
  for (const c of schedulingCases()) {
    assert.equal(scoreSchedule(c, c.oracle).success, 1);
    assert.equal(scoreSchedule(c, { batches: [...c.input.structure.parts].sort((a, b) => a.y - b.y).map(p => [p.id]) }).success, 0);
  }
});

test('diagnostic-v2: all 138 denominators retain missing responses; unknown and duplicate IDs reject', () => {
  const empty = scoreResponses([]);
  assert.equal(empty.expected, 138); assert.equal(empty.missing, 138);
  assert.ok(empty.rows.every(r => r.result.success === 0));
  assert.throws(() => scoreResponses([{ id: 'unknown' }]));
  const id = maintenanceCases()[0].id + '-symbolic';
  assert.throws(() => scoreResponses([{ id }, { id }]));
});

test('diagnostic-v2: mixed pose faults require geometry corrections, not color-only copying', () => {
  for (const c of poseCases()) {
    assert.equal(scorePose(c, c.oracle).success, 1);
    assert.equal(scorePose(c, { faultIds: [], replacements: [] }).success, 0);
    const wrong = structuredClone(c.oracle);
    wrong.replacements[0] = c.current.parts.find(p => p.id === wrong.replacements[0].id)!;
    assert.equal(scorePose(c, wrong).success, 0);
    const alternate = structuredClone(c.oracle);
    alternate.replacements[0].turn = (alternate.replacements[0].turn + 2) % 4;
    assert.equal(scorePose(c, alternate).success, 1);
    assert.ok(!Object.hasOwn(publicPose(c, 'layers').input, 'reference'));
  }
});

test('diagnostic-v2: independently elicited stage outputs merge without repairing missing answers', () => {
  const c = maintenanceCases()[3], id = c.id + '-symbolic';
  const rows = Object.entries(c.oracle).map(([stage, answer]) => ({ id, stage, answer }));
  const full = scoreStageResponses(rows);
  assert.equal(full.rows.find(r => r.id === id)!.result.success, 1);
  const partial = scoreStageResponses(rows.slice(1));
  assert.equal(partial.rows.find(r => r.id === id)!.result.success, 0);
  assert.equal(partial.missingStages, 214);
  assert.throws(() => scoreStageResponses([...rows, rows[0]]));
});
