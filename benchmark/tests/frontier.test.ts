import assert from 'node:assert/strict';
import test from 'node:test';
import { cells, bom, dims, footprint } from '../suite/geometry';
import { frontierModels } from '../suite/frontier/models';
import { frontierTasks } from '../suite/frontier/tasks';
import { evaluateFrontier } from '../suite/frontier/evaluate';
import { accessClosure, cascade, parseStructure, validate } from '../suite/frontier/geometry';
import { scoreSubmissions } from '../suite/frontier/score';

test('frontier: six deep structures are version-isolated and all 48 controls separate', () => {
  assert.equal(frontierModels().length, 6);
  assert.equal(frontierTasks().length, 48);
  for (const m of frontierModels()) {
    assert.ok(m.stats.parts >= 150 && m.stats.parts <= 512);
    assert.ok(m.stats.extent.z >= 14);
  }
  for (const t of frontierTasks()) {
    assert.equal(evaluateFrontier(t, t.oracle).success, 1, t.id);
    assert.equal(evaluateFrontier(t, t.negative).success, 0, t.id);
    for (const bad of [null, [], {}, { actions: 'text' }]) assert.equal(evaluateFrontier(t, bad).success, 0);
  }
});

test('frontier: cell-map collision and support cross-check every model', () => {
  for (const m of frontierModels()) {
    const occupied = new Map<string, string>();
    for (const p of m.structure.parts) for (const c of cells([p])) {
      assert.ok(!occupied.has(c), `${m.id}/${c}`); occupied.set(c, p.id);
    }
    for (const p of m.structure.parts.filter(p => p.y > 0)) {
      const d = dims(p);
      let supported = false;
      for (let x = p.x; x < p.x + d.w; x++) for (let z = p.z; z < p.z + d.d; z++)
        if (occupied.has(`${x},${p.y - 1},${z}`)) supported = true;
      assert.ok(supported, `${m.id}/${p.id}`);
    }
  }
});

test('frontier: minimum access closure agrees with independent upward graph traversal', () => {
  for (const t of frontierTasks().filter(t => t.kind === 'access-certificate')) {
    const parts = t.input.structure.parts;
    const seen = new Set<string>(), queue = [...t.input.serviceIds];
    while (queue.length) {
      const id = queue.shift()!;
      if (seen.has(id)) continue;
      seen.add(id);
      const p = parts.find((p: any) => p.id === id);
      for (const q of parts) if (q.y > p.y && footprint(p, q)) queue.push(q.id);
    }
    assert.deepEqual([...seen].sort(), accessClosure(parts, t.input.serviceIds).map(p => p.id).sort());
    const bad = structuredClone(t.oracle); bad.order.reverse();
    assert.equal(evaluateFrontier(t, bad).success, 0);
  }
});

test('frontier: schema rejects coercion, duplicate IDs, bad yaw and coordinate overflow', () => {
  const s = frontierModels()[0].structure;
  for (const change of [{ partId: ['3003'] }, { color: ['red'] }, { turn: 4 }, { x: 96 }, { y: 1.5 }]) {
    const copy = structuredClone(s); Object.assign(copy.parts[0], change);
    assert.equal(parseStructure(copy), null);
  }
  assert.equal(parseStructure({ version: 1, parts: [s.parts[0], s.parts[0]] }), null);
  const copy = structuredClone(s); copy.parts[0].x = 95;
  assert.ok(validate(copy.parts).includes('bounds'));
});

test('frontier: alternate exact inventory tiling passes and overlap/stock fail', () => {
  const t = frontierTasks().find(t => t.kind === 'inventory-cover')!;
  const alternate = { tiles: t.oracle.tiles.map((p: any) => ({ ...p, x: 8 - p.x - dims(p).w, z: 4 - p.z - dims(p).d, turn: (p.turn + 2) % 4 })) };
  assert.equal(evaluateFrontier(t, alternate).success, 1);
  const bad = structuredClone(t.oracle); bad.tiles[1] = { ...bad.tiles[0] };
  assert.equal(evaluateFrontier(t, bad).success, 0);
});

test('frontier: finite hidden topology worlds preserve cells/BOM and are valid', () => {
  for (const t of frontierTasks().filter(t => t.kind === 'ambiguity-set')) {
    const worlds = t.input.hypotheses.map((h: any) => [...t.input.knownStructure.parts,
      ...t.input.grammar.flatMap((g: any) => g.alternatives[h.layouts[g.id]])]);
    const signature = (ps: any[]) => JSON.stringify([...cells(ps, true)].sort());
    for (const ps of worlds) {
      assert.deepEqual(validate(ps), []);
      assert.equal(signature(ps), signature(worlds[0]));
      assert.deepEqual(bom(ps), bom(worlds[0]));
    }
    assert.equal(evaluateFrontier(t, { possibleIds: ['h0'] }).metrics.falseCertainty, 1);
  }
});

test('frontier: inspection evaluates all worlds, alternative order and budget', () => {
  const t = frontierTasks().find(t => t.kind === 'inspection-policy')!;
  assert.equal(evaluateFrontier(t, { queryId: 'q-all', branches: Object.fromEntries(t.input.hypotheses.map((h: string) => [h, { hypothesisId: h }])) }).success, 0);
  const alt = structuredClone(t); alt.input.budget = 9;
  assert.equal(evaluateFrontier(alt, { queryId: 'q-all', branches: Object.fromEntries(t.input.hypotheses.map((h: string) => [h, { hypothesisId: h }])) }).success, 1);
  const repeated = { queryId: 'q0', branches: { lengthwise: { queryId: 'q0', branches: {} }, crosswise: { hypothesisId: 'h1' } } };
  assert.equal(evaluateFrontier(t, repeated).success, 0);
});

test('frontier: planning omissions, duplicates, extra cycles and repair overreach rejected', () => {
  const t = frontierTasks().find(t => t.kind === 'service-plan')!;
  const a = structuredClone(t.oracle); a.actions.pop();
  assert.equal(evaluateFrontier(t, a).success, 0);
  const extra = { actions: [...t.oracle.actions, ...t.oracle.actions] };
  assert.equal(evaluateFrontier(t, extra).success, 0);
  const s = frontierTasks().find(t => t.kind === 'parallel-schedule')!;
  assert.equal(evaluateFrontier(s, { batches: s.oracle.batches.slice(1) }).success, 0);
  const r = frontierTasks().find(t => t.kind === 'distributed-repair')!;
  const bad = structuredClone(r.oracle); bad.replacements.push(r.input.current.parts[0]);
  assert.equal(evaluateFrontier(r, bad).success, 0);
});

test('frontier: counterfactual closure agrees with bottom-up surviving support graph', () => {
  for (const t of frontierTasks().filter(t => t.kind === 'minimal-intervention')) {
    const gone = new Set<string>(t.oracle.removeIds);
    for (const p of [...t.input.structure.parts].sort((a, b) => a.y - b.y))
      if (p.y > 0 && !t.input.structure.parts.some((q: any) => !gone.has(q.id)
        && q.y + dims(q).h === p.y && footprint(p, q))) gone.add(p.id);
    assert.deepEqual([...gone].sort(), cascade(t.input.structure.parts, t.oracle.removeIds));
  }
});

test('frontier: submission denominators retain missing rows and reject unknown or duplicate IDs', () => {
  const t = frontierTasks()[0];
  const result = scoreSubmissions([{ id: t.id, answer: t.oracle }]);
  assert.equal(result.expected, 48); assert.equal(result.missing, 47);
  assert.equal(result.byKind['service-plan'].cases, 6);
  assert.equal(result.byKind['service-plan'].success, 1);
  assert.throws(() => scoreSubmissions([{ id: 'unknown', answer: {} }]));
  assert.throws(() => scoreSubmissions([{ id: t.id }, { id: t.id }]));
});
