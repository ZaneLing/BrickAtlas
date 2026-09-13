import assert from 'node:assert/strict';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { bom, cells, contact, dims, edges, validate } from '../geometry';
import { digest } from '../data';
import { type Part, type Structure } from '../shared';
import { independentCheck } from '../research/independent-check';
import { surfaceSignature } from '../research/tasks';
import { type CaseTask } from '../v2/cases';
import { evaluateStrict } from './strict-evaluate';
import { STUDY } from './protocol';

export function observabilityWitness() {
  const parts: Part[] = [];
  const add = (id: string, partId: string, x: number, y: number, z: number, turn = 0, color: Part['color'] = 'gray') =>
    parts.push({ id, partId, x, y, z, turn, color });
  add('floor', '3031', 0, 0, 0);
  for (const y of [1, 4]) {
    add(`front${y}`, '3010', 0, y, 0);
    add(`back${y}`, '3010', 0, y, 3);
    add(`left${y}`, '3004', 0, y, 1, 1);
    add(`right${y}`, '3004', 3, y, 1, 1);
  }
  add('inside1', '3004', 1, 1, 1, 0, 'red');
  add('inside2', '3004', 1, 1, 2, 0, 'red');
  add('probe1', '3005', 1, 4, 1, 0, 'blue');
  add('probe2', '3005', 2, 4, 1, 0, 'blue');
  add('roof', '3031', 0, 7, 0);
  const target: Structure = { version: 1, parts: parts.sort((a, b) => a.y - b.y || a.id.localeCompare(b.id)) };
  const alternative = structuredClone(target);
  Object.assign(alternative.parts.find(p => p.id === 'inside1')!, { x: 1, z: 1, turn: 1 });
  Object.assign(alternative.parts.find(p => p.id === 'inside2')!, { x: 2, z: 1, turn: 1 });
  return { target, alternative };
}

function commonLowerSupports(s: Structure) {
  const a = s.parts.find(p => p.id === 'probe1')!, b = s.parts.find(p => p.id === 'probe2')!;
  return s.parts.filter(p => p.y + dims(p).h === a.y && contact(p, a) > 0 && contact(p, b) > 0).map(p => p.id);
}

export function witnessTask(target: Structure, condition: 'ordinary' | 'layers' | 'symbolic' = 'ordinary'): CaseTask {
  const spec = { id: 'observability-witness', modelId: 'observability-witness', group: 'hidden-tiling-1',
    kind: 'reconstruct' as const, variant: 'full', condition, split: 'validation' as const, policy: 'hand-constructed-witness',
    difficulty: 'diagnostic' };
  return { spec, target, source: null, changedIds: [], oracle: target, frames: [],
    public: { id: spec.id, kind: spec.kind, family: spec.policy, split: spec.split, input: { billOfMaterials: bom(target.parts) },
      prompt: 'Evaluator-only diagnostic witness, not a model trial.', responseSchema: {}, imageTitles: [] } };
}

export function observabilityAudit() {
  const { target, alternative } = observabilityWitness();
  const checks = [target, alternative].map(s => independentCheck([...s.parts].sort((a, b) => a.y - b.y)));
  for (const [i, s] of [target, alternative].entries()) {
    assert.deepEqual(validate(s.parts), []); assert.deepEqual(checks[i].issues, []);
    const actual = edges(s.parts).map(e => ({ pair: [e.a, e.b].sort().join('|'), studs: e.studs }));
    assert.deepEqual(actual.sort((a, b) => a.pair.localeCompare(b.pair)),
      checks[i].contacts.sort((a, b) => a.pair.localeCompare(b.pair)));
  }
  assert.deepEqual(bom(target.parts), bom(alternative.parts));
  assert.deepEqual([...cells(target.parts, true)].sort(), [...cells(alternative.parts, true)].sort());
  assert.deepEqual([...surfaceSignature(target.parts)].sort(), [...surfaceSignature(alternative.parts)].sort());
  const degrees = (s: Structure) => s.parts.map(p => edges(s.parts).filter(e => e.a === p.id || e.b === p.id).length).sort((a, b) => a - b);
  assert.notDeepEqual(degrees(target), degrees(alternative), 'Connectivity difference must survive instance renaming');
  const sharedSupports = [target, alternative].map(commonLowerSupports);
  assert.deepEqual(sharedSupports, [['inside1'], []]);
  const scores = Object.fromEntries((['ordinary', 'layers', 'symbolic'] as const).map(condition => [
    condition, evaluateStrict(witnessTask(target, condition), alternative),
  ]));
  assert.equal(scores.ordinary.metrics.success, 1);
  assert.equal(scores.layers.metrics.success, 0); assert.equal(scores.symbolic.metrics.success, 0);
  const result = { version: 'observability-witness-1', independentSourceFamilies: 1, structures: 2,
    sourceHash: digest({ target, alternative }), target, alternative, checks, scores,
    degreeSequences: [degrees(target), degrees(alternative)], sharedLowerSupports: sharedSupports,
    sameColoredOccupancy: true, samePositiveAxisSurface: true, sameBOM: true,
    conclusion: 'The current visual acceptance relation does not imply contact-graph equivalence or the same shared-support answer.',
    scope: 'One constructive grid witness, not population prevalence, a neural result, human validation, or pixel-identical rendering proof.',
    requiredProtocol: 'A downstream query whose answer varies across admissible hidden layouts needs additional observations or a set-valued/undetermined answer; never force one hidden reference.',
    apiRequests: 0 };
  atomicJson(resolve(STUDY, 'observability-witness.json'), result);
  return { families: 1, structures: 2, ordinaryAccepts: true, graphsDiffer: true, humanReviews: 0 };
}
