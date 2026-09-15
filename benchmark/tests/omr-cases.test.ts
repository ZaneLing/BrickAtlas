import assert from 'node:assert/strict';
import test from 'node:test';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { omrCaseRegistry } from '../suite/omr/registry';

const root = resolve(import.meta.dirname, '../..');

test('omr cases: primary registry contains complete objects and source-named subassemblies only', () => {
  const registry = omrCaseRegistry(root);
  assert.deepEqual(registry.summary, {
    wholeModels: 15,
    semanticSubassemblies: 39,
    totalCases: 54,
    sourceModelFiles: 15,
    sourceFamilies: 13,
    placedInstances: 9935,
    uniqueParts: 624,
    colors: 42,
    instructionSteps: 1752,
    sourceInstructionModels: 7,
    editorialInstructionModels: 8,
    minWholeParts: 36,
    maxWholeParts: 4281,
  });
  assert.equal(registry.status, 'primary-object-source');
  assert.equal(new Set([...registry.wholeModels, ...registry.semanticSubassemblies].map(c => c.id)).size, 54);
  assert.ok(registry.semanticSubassemblies.every(c =>
    c.instances >= 6 && !/step\d+|minifig|lamp|cone/i.test(c.title)));
});

test('omr cases: every whole model retains a licensed source, preview, and source group', () => {
  const registry = omrCaseRegistry(root);
  for (const c of registry.wholeModels) {
    assert.equal(c.license, 'CC BY 2.0');
    assert.match(c.sourceUrl, /^https:\/\/library\.ldraw\.org\/omr\/sets\//);
    assert.equal(c.sourceGroup, c.sourceModelId);
    assert.ok(c.instances >= 36);
    const preview = resolve(root, c.preview);
    assert.ok(existsSync(preview), c.id);
    assert.ok(readFileSync(preview).length > 10_000, c.id);
  }
});

test('omr cases: alternate builds share set families and derived parts never become independent sources', () => {
  const registry = omrCaseRegistry(root);
  const byId = new Map(registry.wholeModels.map(c => [c.sourceModelId, c]));
  assert.equal(byId.get('31027')!.sourceFamily, byId.get('31027-kart')!.sourceFamily);
  assert.equal(byId.get('31028')!.sourceFamily, byId.get('31028-sailboat')!.sourceFamily);
  for (const c of registry.semanticSubassemblies) {
    assert.equal(c.sourceGroup, c.sourceModelId);
    assert.equal(c.sourceFamily, byId.get(c.sourceModelId)!.sourceFamily);
  }
});

test('omr cases: random-growth policy names do not enter the primary registry', () => {
  const encoded = JSON.stringify(omrCaseRegistry(root));
  for (const name of ['tip-walk', 'low-fan', 'shallow-terrace', 'plate-network',
    'column-field', 'alternating-beams', 'two-support-bridge', 'enclosed-shell']) {
    assert.ok(!encoded.includes(name), name);
  }
});

test('omr cases: publication figures use complete OMR objects, not procedural policy renders', () => {
  const main = readFileSync(resolve(root, 'benchmark/paper/main.tex'), 'utf8');
  const supplement = readFileSync(resolve(root, 'benchmark/paper/supplement.tex'), 'utf8');
  assert.ok(main.includes('figures/omr-whole-models.pdf'));
  assert.ok(supplement.includes('figures/omr-whole-models.pdf'));
  for (const name of ['tip-walk.png', 'low-fan.png', 'shallow-terrace.png',
    'plate-network.png', 'column-field.png', 'alternating-beams.png',
    'two-support-bridge.png', 'enclosed-shell.png']) {
    assert.ok(!main.includes(name), name);
    assert.ok(!supplement.includes(name), name);
  }
});
