import { test } from 'node:test';
import assert from 'node:assert/strict';
import { diagnoseResponse, diagnosticSummary, FAILURE_STAGES } from '../suite/study/failure-diagnostics';
import { observabilityWitness, witnessTask } from '../suite/study/observability';
import { interfaceProbes } from '../suite/study/interface-probes';
import { calibrationSelection } from '../suite/study/calibration';
import { evaluateStrict } from '../suite/study/strict-evaluate';
import { bom, cells, contact, dims, edges } from '../suite/geometry';
import { independentCheck } from '../suite/research/independent-check';
import { surfaceSignature } from '../suite/research/tasks';

test('failure stages distinguish parse, envelope, domain, geometry and correctness without rescuing responses', () => {
  const { target } = observabilityWitness(), task = witnessTask(target);
  const classify = (answer: unknown) => diagnoseResponse(task, JSON.stringify(answer), 'stop');
  assert.equal(diagnoseResponse(task, 'not JSON', 'length').stage, 'json');
  assert.equal(diagnoseResponse(task, 'not JSON', 'length').tokenLimitReached, true);
  assert.equal(classify(null).jsonParsed, true);
  assert.equal(classify(null).stage, 'response-schema');
  const envelope = classify({ prompt: 'copy', input: {}, responseSchema: {}, structure: target });
  assert.equal(envelope.stage, 'response-schema'); assert.equal(envelope.nestedStructure, true);
  assert.equal(envelope.verdict.metrics.success, 0); assert.equal(envelope.envelopeFields.length, 3);
  const invalid = structuredClone(target); invalid.parts[0].turn = 12;
  assert.equal(classify(invalid).stage, 'structure-domain');
  const overlap = structuredClone(target); overlap.parts.push({ ...target.parts[0], id: 'duplicate-pose' });
  assert.equal(classify(overlap).stage, 'geometry');
  assert.equal(classify(target).stage, 'success');
  assert.equal(diagnoseResponse(task, '```json\n' + JSON.stringify(target) + '\n```', 'stop').stage, 'success');
});

test('diagnostic summaries preserve failure denominators and null conditional metrics', () => {
  const task = witnessTask(observabilityWitness().target);
  const rows = [diagnoseResponse(task, 'bad', 'stop'), diagnoseResponse(task, '{}', 'length')];
  const report = diagnosticSummary(rows);
  assert.equal(report.n, 2);
  assert.equal(report.allResponses.success.denominator, 2);
  assert.equal(report.formatAcceptedOnly.success.denominator, 0);
  assert.equal(report.formatAcceptedOnly.success.value, null);
  assert.equal(FAILURE_STAGES.reduce((n, stage) => n + report.stages[stage], 0), 2);
});

test('hidden tilings have equal observations but unequal connectivity independent of piece IDs', () => {
  const { target, alternative } = observabilityWitness();
  for (const s of [target, alternative]) assert.deepEqual(independentCheck(s.parts).issues, []);
  assert.deepEqual(bom(target.parts), bom(alternative.parts));
  assert.deepEqual(cells(target.parts, true), cells(alternative.parts, true));
  assert.deepEqual(surfaceSignature(target.parts), surfaceSignature(alternative.parts));
  const degrees = (s: typeof target) => s.parts.map(p => edges(s.parts).filter(e => [e.a, e.b].includes(p.id)).length).sort();
  assert.notDeepEqual(degrees(target), degrees(alternative));
  const shared = (s: typeof target) => {
    const probes = s.parts.filter(p => p.color === 'blue');
    return s.parts.filter(p => probes.every(q => p.y + dims(p).h === q.y && contact(p, q) > 0)).length;
  };
  assert.equal(shared(target), 1); assert.equal(shared(alternative), 0);
  for (const condition of ['ordinary', 'layers', 'symbolic'] as const) {
    assert.equal(evaluateStrict(witnessTask(target, condition), alternative).metrics.success, condition === 'ordinary' ? 1 : 0);
  }
  const renamed = structuredClone(alternative);
  renamed.parts.forEach((p, i) => { p.id = `renamed${i}`; });
  assert.equal(evaluateStrict(witnessTask(target), renamed).metrics.success, 1);
});

test('trivial probe controls accept all oracles and both arms preserve task information', () => {
  const probes = interfaceProbes(); assert.equal(probes.length, 18);
  for (const p of probes) {
    assert.equal(evaluateStrict(p.task, p.task.oracle).metrics.success, 1, p.id);
    const other = probes.find(q => q.count === p.count && q.operation === p.operation && q.arm !== p.arm)!;
    const input = JSON.parse(p.user), paired = JSON.parse(other.user);
    for (const field of ['prompt', 'input', 'responseSchema']) assert.deepEqual(input[field], paired[field]);
    assert.ok(!Object.hasOwn(input, 'oracle'));
  }
});

test('calibration objects exclude all previous train, validation and test study groups', () => {
  const { objects, cases, excluded } = calibrationSelection();
  assert.equal(objects.length, 36); assert.equal(cases.length, 468);
  assert.ok(objects.every(o => o.split === 'validation' && !excluded.includes(o.group)));
  assert.equal(new Set(cases.map(c => c.group)).size, 36);
  assert.equal(new Set(objects.map(o => o.policy)).size, 6);
  for (const policy of new Set(objects.map(o => o.policy))) {
    assert.equal(objects.filter(o => o.policy === policy).length, 6);
  }
  assert.ok(objects.filter(o => o.policy === 'tip-walk').every(o => o.difficulty === 'small'));
  assert.deepEqual(calibrationSelection().objects, objects);
});
