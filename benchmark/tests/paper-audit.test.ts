import { test } from 'node:test';
import assert from 'node:assert/strict';
import { copyInputAnswer, inventory, summarizeControls, type ControlRow } from '../suite/study/paper-audit';
import { caseSpecs, taskForV2 } from '../suite/v2/cases';
import { dataset } from '../suite/v2/dataset';
import { evaluateStrict } from '../suite/study/strict-evaluate';

test('paper inventory counts source objects separately from instances and absent types', () => {
  const data = dataset().slice(0, 3), report = inventory(data);
  assert.equal(report.sourceGroups, 3);
  assert.equal(report.instances, data.reduce((n, r) => n + r.structure.parts.length, 0));
  assert.equal(report.catalogTypes, 25);
  assert.equal(report.assembledTypes + report.absentTypes.length, 25);
  assert.equal(report.partTypes.find(t => t.partId === '3035')!.objects, 3);
  assert.equal(report.partTypes.reduce((n, t) => n + t.instances, 0), report.instances);
  assert.throws(() => inventory([]), /Nonempty/);
  assert.throws(() => inventory([data[0], data[0]]), /Duplicate/);
});

test('copy predictor consumes public current only and cannot alter the source', () => {
  const spec = caseSpecs().find(s => s.kind === 'complete' && s.condition === 'ordinary')!;
  const task = taskForV2(spec), before = structuredClone(task.public);
  const answer = copyInputAnswer(task.public) as typeof task.source;
  assert.deepEqual(answer, task.public.input.current);
  const score = evaluateStrict(task, answer);
  assert.equal(score.metrics.success, 0);
  assert.equal(score.metrics.preservation, 1);
  assert.equal(score.metrics.additionF1, 0);
  const n = task.source!.parts.length, total = task.target.parts.length;
  assert.equal(score.metrics.partF1, 2 * n / (n + total));
  answer!.parts.pop();
  assert.deepEqual(task.public, before);
  assert.throws(() => copyInputAnswer({ ...task.public, kind: 'reconstruct' }), /requires/);
});

test('no-fault control is a real true negative, not a positive repair solution', () => {
  for (const variant of ['none', 'color', 'shift']) {
    const spec = caseSpecs().find(s => s.kind === 'repair' && s.variant === variant && s.condition === 'ordinary')!;
    const task = taskForV2(spec);
    const verdict = evaluateStrict(task, copyInputAnswer(task.public));
    assert.equal(verdict.metrics.success, Number(variant === 'none'));
    assert.equal(verdict.metrics.falseAlarm, variant === 'none' ? 0 : null);
  }
});

test('control aggregation retains metric-specific null denominators and refuses pseudoreplication', () => {
  const row: ControlRow = { caseId: 'a', group: 'g', kind: 'repair', variant: 'shift',
    condition: 'ordinary', split: 'test_id', policy: 'p', metrics: { success: 0, falseAlarm: null } };
  const summary = summarizeControls([row])[0];
  assert.deepEqual(summary.metrics.success, { mean: 0, denominator: 1 });
  assert.deepEqual(summary.metrics.falseAlarm, { mean: null, denominator: 0 });
  assert.throws(() => summarizeControls([row, row]), /Duplicate/);
  assert.throws(() => summarizeControls([row, { ...row, caseId: 'b' }]), /Repeated source/);
  assert.throws(() => summarizeControls([{ ...row, metrics: { success: NaN } }]), /Nonfinite/);
});
