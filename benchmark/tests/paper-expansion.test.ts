import assert from 'node:assert/strict';
import { test } from 'node:test';
import { admissibleAnswer, ambiguityCases, dominoTilings, publicAmbiguityInput, scoreSetAnswer,
  sharedSupport, solvePublicAmbiguity, tilingStructure } from '../suite/study/ambiguity';
import { paperModelCeiling, PAPER_MODELS } from '../suite/study/paper-models';
import { independentCheck } from '../suite/research/independent-check';
import { scoreAmbiguityBatch } from '../suite/study/ambiguity-score';

test('finite tilings agree with independent recurrence counts and have unique cell coverage', () => {
  const count = (width: number) => {
    const dp = [1, 1];
    for (let i = 2; i <= width; i++) dp[i] = dp[i - 1] + dp[i - 2];
    return dp[width];
  };
  for (const width of [2, 3, 4, 5, 6]) {
    const layouts = dominoTilings(width);
    assert.equal(layouts.length, count(width));
    assert.equal(new Set(layouts.map(r => JSON.stringify(r))).size, layouts.length);
    for (const layout of layouts) {
      const occupied = layout.flatMap(p => [[p.x, p.z], [p.x + Number(p.turn === 0), p.z + Number(p.turn === 1)]]);
      assert.equal(new Set(occupied.map(v => v.join(','))).size, width * 2);
    }
  }
  assert.throws(() => dominoTilings(7));
});

test('all grammar layouts remain valid with balanced source grouping and immutable v2 isolation', () => {
  const data = ambiguityCases();
  assert.equal(data.families.length, 9);
  assert.equal(data.cases.length, 600);
  assert.equal(new Set(data.cases.map(r => r.id)).size, 600);
  for (const family of data.families) {
    for (const s of family.structures) assert.deepEqual(independentCheck(s.parts).issues, []);
    const rows = data.cases.filter(r => r.group === family.group);
    assert.equal(rows.filter(r => r.condition === 'exterior').length, rows.filter(r => r.condition === 'support-disclosed').length);
    assert.ok(rows.some(r => r.condition === 'exterior' && r.expected === 'undetermined'));
    assert.ok(rows.filter(r => r.condition === 'support-disclosed').every(r => r.expected !== 'undetermined'));
  }
});

test('support oracle agrees with independent contact-edge intersections', () => {
  for (const t of dominoTilings(4)) {
    const s = tilingStructure(4, t), check = independentCheck(s.parts);
    const ids = s.parts.filter(p => p.color === 'blue').map(p => p.id);
    for (const b of ids.slice(1)) {
      const a = ids[0];
      const links = (id: string) => check.contacts.filter(e => e.pair.split('|').includes(id))
        .flatMap(e => e.pair.split('|').filter(q => q !== id && q.startsWith('inside')));
      assert.equal(sharedSupport(s, a, b), links(a).some(p => links(b).includes(p)));
    }
  }
});

test('set-valued answers separate ambiguity from deterministic negatives and format failures', () => {
  assert.equal(admissibleAnswer([true, false]), 'undetermined');
  assert.equal(admissibleAnswer([true, true]), 'yes');
  assert.equal(admissibleAnswer([false]), 'no');
  assert.throws(() => admissibleAnswer([]));
  assert.equal(scoreSetAnswer('undetermined', { answer: 'yes' }).falseCertainty, 1);
  assert.equal(scoreSetAnswer('no', { answer: 'undetermined' }).unnecessaryAbstention, 1);
  for (const answer of [null, {}, [], { answer: true }, { answer: ['yes'] }]) {
    assert.equal(scoreSetAnswer('yes', answer).format, 0);
    assert.equal(scoreSetAnswer('yes', answer).success, 0);
  }
});

test('public ambiguity export hides labels and enumeration solves every declared information condition', () => {
  const { cases, families } = ambiguityCases();
  for (const row of cases) {
    const input = publicAmbiguityInput(row, families.find(f => f.group === row.group)!.structures[0]);
    assert.ok(!Object.hasOwn(input, 'expected') && !Object.hasOwn(input.input, 'answerSet'));
    assert.ok(input.input.knownParts.every(p => !(p.color === 'red' && p.y === input.input.unknownY)));
    assert.equal(input.input.disclosedSupports === null, row.condition === 'exterior');
    assert.equal(solvePublicAmbiguity(input).answer, row.expected);
  }
});

test('new model reservation covers image and text budgets without touching the historical model registry', () => {
  assert.equal(PAPER_MODELS.length, 4);
  for (const model of PAPER_MODELS) {
    const plain = paperModelCeiling(model, [{ role: 'user', content: 'test' }]);
    const visual = paperModelCeiling(model, [{ role: 'user', content: [
      { type: 'text', text: 'test' }, { type: 'image_url', image_url: { url: 'data:image/png;base64,AA==' } },
    ] }]);
    assert.ok(plain > 2200 * model.completion / 1e6);
    assert.ok(visual > plain + .005);
  }
  assert.throws(() => paperModelCeiling(PAPER_MODELS[0], [{ role: 'user', content: 'x'.repeat(50001) }]));
});

test('ambiguity submission scoring preserves missing rows, class balance and conditional denominators', () => {
  const cases = [
    { id: 'a', group: 'g1', condition: 'exterior', expected: 'undetermined' as const },
    { id: 'b', group: 'g2', condition: 'exterior', expected: 'no' as const },
    { id: 'c', group: 'g2', condition: 'disclosed', expected: 'yes' as const },
  ];
  const report = scoreAmbiguityBatch(cases, [{ caseId: 'a', answer: { answer: 'yes' } }, { caseId: 'b', answer: { answer: 'no' } }]);
  assert.equal(report.rows.length, 3);
  const ext = report.conditions[0], disclosed = report.conditions[1];
  assert.equal(ext.balancedAccuracy, .5);
  assert.deepEqual(ext.falseCertainty, { numerator: 1, denominator: 1, rate: 1 });
  assert.equal(disclosed.missing, 1);
  assert.equal(disclosed.successes, 0);
  assert.equal(disclosed.falseCertainty.rate, null);
  assert.throws(() => scoreAmbiguityBatch(cases, [{ caseId: 'bad', answer: {} }]), /Unknown/);
  assert.throws(() => scoreAmbiguityBatch(cases, [{ caseId: 'a', answer: {} }, { caseId: 'a', answer: {} }]), /Duplicate/);
});
