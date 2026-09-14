import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { bom, cells, contact, dims, validate } from '../geometry';
import { independentCheck } from '../research/independent-check';
import { surfaceSignature } from '../research/tasks';
import type { Part, Structure } from '../shared';
import { STUDY } from './protocol';

export type Domino = { x: number; z: number; turn: number };
export type SetAnswer = 'yes' | 'no' | 'undetermined';
export const AMBIGUITY_DIR = resolve(STUDY, 'ambiguity');

// Exact finite grammar: every cell of a 2-by-W interior is covered once by a domino.
export function dominoTilings(width: number): Domino[][] {
  assert.ok(Number.isInteger(width) && width >= 2 && width <= 6);
  const results: Domino[][] = [];
  const search = (occupied: Set<number>, placed: Domino[]) => {
    const next = Array.from({ length: width * 2 }, (_, i) => i).find(i => !occupied.has(i));
    if (next === undefined) { results.push(placed); return; }
    const x = next % width, z = Math.floor(next / width);
    for (const [dx, dz, turn] of [[1, 0, 0], [0, 1, 1]]) {
      const q = (z + dz) * width + x + dx;
      if (x + dx >= width || z + dz >= 2 || occupied.has(q)) continue;
      search(new Set([...occupied, next, q]), [...placed, { x, z, turn }]);
    }
  };
  search(new Set(), []);
  return results;
}

export function tilingStructure(width: 2 | 4 | 6, tiling: Domino[], layers = 1): Structure {
  assert.ok(Number.isInteger(layers) && layers >= 1 && layers <= 3);
  const parts: Part[] = [];
  const add = (id: string, partId: string, x: number, y: number, z: number,
    turn = 0, color: Part['color'] = 'gray') => parts.push({ id, partId, x, y, z, turn, color });
  const base = { 2: '3031', 4: '3032', 6: '3035' }[width];
  const beam = { 2: '3010', 4: '3009', 6: '3008' }[width];
  add('floor', base, 0, 0, 0);
  for (let level = 0; level <= layers; level++) {
    const y = 1 + 3 * level;
    add(`front${level}`, beam, 0, y, 0);
    add(`back${level}`, beam, 0, y, 3);
    add(`left${level}`, '3004', 0, y, 1, 1);
    add(`right${level}`, '3004', width + 1, y, 1, 1);
    if (level < layers) {
      const layout = level === layers - 1 ? tiling : dominoTilings(width)[0];
      for (const [i, p] of layout.entries()) add(`inside${level}-${i}`, '3004', p.x + 1, y, p.z + 1, p.turn, 'red');
    } else {
      for (let z = 0; z < 2; z++) for (let x = 0; x < width; x++) add(`probe${x}-${z}`, '3005', x + 1, y, z + 1, 0, 'blue');
    }
  }
  add('roof', base, 0, 1 + 3 * (layers + 1), 0);
  return { version: 1, parts: parts.sort((a, b) => a.y - b.y || a.id.localeCompare(b.id)) };
}

export function sharedSupport(structure: Structure, aId: string, bId: string): boolean {
  const a = structure.parts.find(p => p.id === aId), b = structure.parts.find(p => p.id === bId);
  assert.ok(a && b && aId !== bId);
  return structure.parts.some(p => p.y + dims(p).h === a.y && p.y + dims(p).h === b.y
    && contact(p, a) > 0 && contact(p, b) > 0);
}

export function admissibleAnswer(values: boolean[]): SetAnswer {
  assert.ok(values.length > 0, 'Nonempty admissible set required');
  return values.every(Boolean) ? 'yes' : values.every(v => !v) ? 'no' : 'undetermined';
}

export function scoreSetAnswer(expected: SetAnswer, answer: unknown) {
  const valid = !!answer && typeof answer === 'object' && !Array.isArray(answer)
    && ['yes', 'no', 'undetermined'].includes((answer as any).answer);
  const predicted = valid ? (answer as { answer: SetAnswer }).answer : null;
  return { format: Number(valid), success: Number(predicted === expected),
    falseCertainty: expected === 'undetermined' ? Number(predicted === 'yes' || predicted === 'no') : null,
    unnecessaryAbstention: expected !== 'undetermined' ? Number(predicted === 'undetermined') : null };
}

export function publicAmbiguityInput(row: any, reference: Structure) {
  const unknownY = 1 + 3 * (row.layers - 1);
  return { id: row.id, group: row.group, condition: row.condition,
    prompt: 'Do the two queried blue pieces share at least one directly supporting red brick? Answer yes or no only if every admissible hidden tiling agrees; otherwise answer undetermined.',
    input: { grammar: row.grammar, width: row.width, layers: row.layers, unknownY,
      knownParts: reference.parts.filter(p => !(p.color === 'red' && p.y === unknownY)),
      unknownInventory: { partId: '3004', color: 'red', count: row.width },
      query: [row.a, row.b], disclosedSupports: row.disclosure },
    responseSchema: { answer: 'yes|no|undetermined' },
    scope: 'Finite-grammar reasoning with symbolic known geometry. Not a pure visual-perception test.' };
}

export function solvePublicAmbiguity(row: ReturnType<typeof publicAmbiguityInput>) {
  const { input } = row, layouts = dominoTilings(input.width);
  const candidates = input.disclosedSupports !== null ? [input.disclosedSupports as Part[]]
    : layouts.map(t => t.map((p, i) => ({ id: `unknown${i}`, partId: '3004', color: 'red' as const,
      x: p.x + 1, y: input.unknownY, z: p.z + 1, turn: p.turn })));
  const values = candidates.map(parts => {
    const s: Structure = { version: 1, parts: [...input.knownParts, ...parts] };
    assert.deepEqual(validate(s.parts), []);
    return sharedSupport(s, input.query[0], input.query[1]);
  });
  return { answer: admissibleAnswer(values) };
}

export function ambiguityCases() {
  const families: any[] = [], cases: any[] = [];
  for (const width of [2, 4, 6] as const) for (const layers of [1, 2, 3]) {
    const layouts = dominoTilings(width), structures = layouts.map(t => tilingStructure(width, t, layers));
    for (const s of structures) {
      assert.ok(s.parts.length <= 64);
      assert.deepEqual(validate(s.parts), []);
      assert.deepEqual(independentCheck(s.parts).issues, []);
      assert.deepEqual(bom(s.parts), bom(structures[0].parts));
      assert.deepEqual(cells(s.parts, true), cells(structures[0].parts, true));
      assert.deepEqual(surfaceSignature(s.parts), surfaceSignature(structures[0].parts));
    }
    const group = digest({ version: 'ambiguity-1', width, layers });
    families.push({ group, width, layers, admissibleLayouts: layouts.length, structures });
    const probes = structures[0].parts.filter(p => p.color === 'blue');
    for (let i = 0; i < probes.length; i++) for (const b of probes.slice(i + 1)) {
      const a = probes[i], answers = structures.map(s => sharedSupport(s, a.id, b.id));
      const base = { group, width, layers, a: a.id, b: b.id, answerSet: [...new Set(answers)].sort(),
        grammar: 'Fixed shell and probe poses. Unknown top internal layer is any complete tiling of the 2-by-W interior by identical red 1x2 bricks. All lower layers are fixed.' };
      const supportIds = structures[0].parts.filter(p => p.y === 1 + 3 * (layers - 1) && p.color === 'red').map(p => p.id);
      const observations = [
        { condition: 'exterior', indices: structures.map((_, i) => i), disclosure: null },
        { condition: 'support-disclosed', indices: [0], disclosure: structures[0].parts.filter(p => supportIds.includes(p.id)) },
      ];
      for (const observation of observations) {
        const values = observation.indices.map(i => answers[i]);
        const spec = { ...base, condition: observation.condition, admissibleIndices: observation.indices,
          disclosure: observation.disclosure, expected: admissibleAnswer(values) };
        cases.push({ id: digest(spec).slice(0, 24), ...spec });
      }
    }
  }
  return { families, cases };
}

export function ambiguityAudit(verify = false) {
  const { families, cases } = ambiguityCases();
  const publicRows = cases.map(row => publicAmbiguityInput(row, families.find(f => f.group === row.group)!.structures[0]));
  const rows = cases.map(c => ({ ...c,
    oracle: scoreSetAnswer(c.expected, { answer: c.expected }),
    enumeration: scoreSetAnswer(c.expected, solvePublicAmbiguity(publicRows.find(r => r.id === c.id)!)),
    alwaysNo: scoreSetAnswer(c.expected, { answer: 'no' }),
    alwaysUnknown: scoreSetAnswer(c.expected, { answer: 'undetermined' }),
    firstWitness: scoreSetAnswer(c.expected, { answer: sharedSupport(
      families.find(f => f.group === c.group)!.structures[0], c.a, c.b) ? 'yes' : 'no' }) }));
  const conditions = ['exterior', 'support-disclosed'].map(condition => {
    const selected = rows.filter(c => c.condition === condition);
    return { condition, cases: selected.length, groups: families.length,
      counts: Object.fromEntries(['yes', 'no', 'undetermined'].map(a => [a, selected.filter(c => c.expected === a).length])),
      baselines: Object.fromEntries(['oracle', 'enumeration', 'alwaysNo', 'alwaysUnknown', 'firstWitness'].map(method => {
        const score = (r: any) => r[method].success as number;
        const macro = families.map(f => {
          const groupRows = selected.filter(c => c.group === f.group);
          return groupRows.reduce((n, r) => n + score(r), 0) / groupRows.length;
        });
        const perClass = ['yes', 'no', 'undetermined'].map(label => {
          const matching = selected.filter(r => r.expected === label);
          return { label, n: matching.length, accuracy: matching.length
            ? matching.reduce((n, r) => n + score(r), 0) / matching.length : null };
        });
        const present = perClass.filter(r => r.accuracy !== null);
        return [method, { correct: selected.reduce((n, r) => n + score(r), 0),
          total: selected.length, sourceMacro: macro.reduce((a, b) => a + b, 0) / macro.length,
          perClass, balancedAccuracy: present.reduce((n, r) => n + r.accuracy!, 0) / present.length }];
      })) };
  });
  const result = { version: 'ambiguity-1', sourceHash: digest(readFileSync(fileURLToPath(import.meta.url), 'utf8')),
    publicInputHash: digest(publicRows),
    families, rows, conditions, sourceGroups: families.length, cases: cases.length,
    apiRequests: 0, humanReviews: 0, status: 'verified-development-extension',
    limitations: ['Nine parametrized grammar families, not nine independently sourced semantic categories.',
      'Exact answer sets are exhaustive only within the disclosed finite domino grammar, not all arbitrary brick layouts.',
      'Equal grid surfaces are verified; renderer pixel equality is a separate audit.',
      'Symbolic support disclosure changes information. New extension is not pooled with frozen v2 results.',
      'Part-level statements concern nominal contacts, not stability or forces.'] };
  const path = resolve(AMBIGUITY_DIR, 'audit.json');
  const publicText = publicRows.map(r => JSON.stringify(r)).join('\n') + '\n';
  if (verify) {
    assert.deepEqual(JSON.parse(readFileSync(path, 'utf8')), result);
    assert.equal(readFileSync(resolve(AMBIGUITY_DIR, 'public.jsonl'), 'utf8'), publicText);
  } else {
    atomicJson(path, result);
    writeFileSync(resolve(AMBIGUITY_DIR, 'public.jsonl'), publicText);
  }
  return { groups: families.length, cases: cases.length, layouts: families.reduce((n, f) => n + f.structures.length, 0), conditions };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  console.log(JSON.stringify(ambiguityAudit(process.argv.includes('--verify'))));
}
