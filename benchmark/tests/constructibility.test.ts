import assert from 'node:assert/strict';
import test from 'node:test';
import { insertion } from '../suite/frontier/geometry';
import { constructibilityCases } from '../suite/constructibility/cases';
import {
  clarificationOracle,
  evaluateConstructibility,
  scoreClarification,
} from '../suite/constructibility/evaluate';
import { auditPlan, placementIssue, solvePlan } from '../suite/constructibility/geometry';
import { scoreConstructibility } from '../suite/constructibility/score';
import { frontierModels } from '../suite/frontier/models';

test('constructibility: all six large structures have a complete accessible plan', () => {
  for (const model of frontierModels()) {
    const plan = solvePlan(model.structure.parts);
    const audit = auditPlan(model.structure.parts, { steps: plan });
    assert.equal(plan.length, model.structure.parts.length);
    assert.equal(audit.success, 1, model.id);
    assert.equal(audit.legalPrefixRate, 1);
    assert.ok(audit.minimumSupportFraction > 0);
  }
});

test('constructibility: 78 conditions retain four separate capability families', () => {
  const cases = constructibilityCases();
  assert.equal(cases.length, 78);
  assert.deepEqual(Object.fromEntries([...new Set(cases.map(c => c.kind))].map(kind =>
    [kind, cases.filter(c => c.kind === kind).length])), {
    'sequence-audit': 18,
    'blocked-recovery': 18,
    'stockout-replan': 6,
    'clarify-or-commit': 36,
  });
  assert.equal(new Set(cases.map(c => c.sourceGroup)).size, 6);
});

test('constructibility: sequence audits distinguish support, clearance, and valid plans', () => {
  for (const c of constructibilityCases().filter(c => c.kind === 'sequence-audit')) {
    assert.equal(evaluateConstructibility(c, c.oracle).success, 1, c.id);
    const actual = auditPlan(c.input.target.parts, c.input.candidate);
    if (c.variant === 'valid') assert.equal(actual.success, 1);
    if (c.variant === 'unsupported-first') assert.equal(actual.reason, 'support');
    if (c.variant === 'clearance-dead-end') {
      assert.equal(actual.reason, 'tool_clearance');
      const step = c.input.candidate.steps[actual.firstFailure!];
      const state = actual.finalParts;
      const part = c.input.target.parts.find(p => p.id === step.id)!;
      assert.equal(insertion(state, part), null, 'body-only vertical rule should miss this failure');
      assert.equal(placementIssue(state, part, step.approach), 'tool_clearance');
    }
  }
});

test('constructibility: blocked recovery requires diagnosis, minimum rollback, and continuation', () => {
  for (const c of constructibilityCases().filter(c => c.kind === 'blocked-recovery')) {
    const oracle = evaluateConstructibility(c, c.oracle);
    assert.equal(oracle.success, 1, c.id);
    assert.ok(c.oracle.recovery.length >= 3);
    assert.equal(evaluateConstructibility(c, {
      diagnosis: c.oracle.diagnosis,
      recovery: [],
      continuation: c.oracle.continuation,
    }).success, 0);
    const wrong = structuredClone(c.oracle);
    wrong.diagnosis.reason = 'support' as any;
    assert.equal(evaluateConstructibility(c, wrong).success, 0);
  }
});

test('constructibility: stockout plans conserve stock, cover the unavailable volume, and continue', () => {
  for (const c of constructibilityCases().filter(c => c.kind === 'stockout-replan')) {
    assert.equal(evaluateConstructibility(c, c.oracle).success, 1, c.id);
    assert.equal(evaluateConstructibility(c, {
      placements: [{ part: c.input.unavailablePart, approach: 'west' }],
      continuation: [],
    }).success, 0);
    const overlap = structuredClone(c.oracle);
    overlap.placements[1].part = { ...overlap.placements[0].part, id: 'overlap-copy' };
    assert.equal(evaluateConstructibility(c, overlap).success, 0);
  }
});

test('constructibility: ambiguity requires calibrated abstention and resolved cases require commitment', () => {
  const cases = constructibilityCases().filter(c => c.kind === 'clarify-or-commit');
  assert.equal(cases.filter(c => c.variant === 'ambiguous').length, 18);
  assert.equal(cases.filter(c => c.variant === 'resolved').length, 18);
  for (const c of cases) {
    const oracle = clarificationOracle(c);
    assert.equal(scoreClarification(c, oracle).success, 1, c.id);
    const overconfident = {
      possibleIds: ['h0'],
      probabilities: Object.fromEntries(c.input.worlds.map(w => [w.id, Number(w.id === 'h0')])),
      decision: 'h0',
      nextQueryId: null,
    };
    if (c.variant === 'ambiguous') {
      const result = scoreClarification(c, overconfident);
      assert.equal(result.success, 0);
      assert.equal(result.falseCertainty, 1);
    }
  }
});

test('constructibility: missing answers stay in the denominator; unknown and duplicate IDs reject', () => {
  const cases = constructibilityCases();
  const empty = scoreConstructibility([]);
  assert.equal(empty.expected, 78);
  assert.equal(empty.missing, 78);
  assert.ok(empty.rows.every(row => row.result.success === 0));
  assert.throws(() => scoreConstructibility([{ id: 'unknown', answer: {} }]));
  assert.throws(() => scoreConstructibility([{ id: cases[0].id }, { id: cases[0].id }]));
});
