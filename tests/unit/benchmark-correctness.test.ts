import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { Group, Quaternion, Vector3 } from 'three';
import { BenchmarkScene } from '../../src/benchmark/Scene';
import { score, replay } from '../../src/benchmark/engine';
import type { Task } from '../../src/benchmark/types';
import { infoGain } from '../../benchmark/suite/mechanism/tasks';
import { semanticKey } from '../../benchmark/suite/hierarchy3/tasks';
import { build, physicsEvidence } from '../../benchmark/suite/hierarchy3/physics';
import { models } from '../../benchmark/suite/hierarchy3/models';
import { validateModel } from '../../benchmark/suite/hierarchy3/validate';
import type RAPIER from '@dimforge/rapier3d-compat';

const catalog = JSON.parse(readFileSync('benchmark/hierarchy-v3/catalog.json', 'utf8'));
const bundles = catalog.map((m: any) => JSON.parse(readFileSync(`benchmark/hierarchy-v3/models/${m.id}.json`, 'utf8')));
const tasks: Task[] = bundles.flatMap((b: any) => b.tasks);
describe('Hierarchy-3 correctness gates', () => {
  it('information gain obeys zero/full information boundaries and ranks same-cost observations', () => {
    const worlds = ['a', 'b', 'c', 'd'];
    const uninformative = infoGain(worlds, { id: 'none', label: '', cost: 1, returns: { a: 'x', b: 'x', c: 'x', d: 'x' } });
    const full = infoGain(worlds, { id: 'full', label: '', cost: 1, returns: { a: 'a', b: 'b', c: 'c', d: 'd' } });
    expect(uninformative.informationGain).toBe(0);
    expect(full.informationGain).toBe(2);
    expect(full.efficiency).toBeGreaterThan(uninformative.efficiency);
  });
  it('keeps set and ordered vector semantics distinct', () => {
    expect(semanticKey({ family: 'next-module' }, ['b', 'a'])).toBe(semanticKey({ family: 'next-module' }, ['a', 'b']));
    expect(semanticKey({ family: 'translate' }, [0, 1, 2])).not.toBe(semanticKey({ family: 'translate' }, [2, 1, 0]));
  });
  it('accepts every reference and rejects every wrong choice or one-bit set mutation', () => {
    expect(tasks).toHaveLength(2304);
    for (const t of tasks) {
      expect(score(t, t.answer).success, t.id).toBe(1);
      if (!t.options) continue;
      const keys = t.options.map(o => semanticKey(t, o.value));
      expect(new Set(keys).size, t.id).toBe(keys.length);
      for (const o of t.options) {
        if (t.format === 'single-choice') expect(score(t, { choiceId: o.id }).success, t.id)
          .toBe(Number(o.id === t.answer.choiceId));
        else {
          const ids = new Set<string>(t.answer.choiceIds);
          if (ids.has(o.id)) ids.delete(o.id); else ids.add(o.id);
          expect(score(t, { choiceIds: [...ids] }).success, t.id).toBe(0);
        }
      }
    }
  });
  it('rejects missing/repeated actions, premature release, and trap actions', () => {
    for (const t of tasks.filter(t => t.format === 'actions')) {
      const ids = t.answer.actionIds as string[];
      expect(replay(t, ids.slice(0, -1)).success, t.id).toBe(0);
      expect(replay(t, [ids[0], ids[0], ...ids.slice(1)]).success, t.id).toBe(0);
      expect(replay(t, ['unknown']).success, t.id).toBe(0);
      if (t.input.actions.some((a: any) => a.id === 'skip-inspection'))
        expect(replay(t, ['skip-inspection', ...ids]).success, t.id).toBe(0);
    }
  });
  it('rejects overlapping resource schedules and policies outside budget', () => {
    for (const t of tasks.filter(t => t.format === 'schedule'))
      expect(score(t, { starts: Object.fromEntries(t.input.jobs.map((j: any) => [j.id, 0])) }).success, t.id).toBe(0);
    for (const t of tasks.filter(t => t.family === 'budget-policy'))
      expect(score(t, { ...t.answer, queryId: t.input.queries.find((q: any) => q.cost > t.input.budget).id }).success, t.id).toBe(0);
  });
  it('selection/isolation cannot resurrect absent modules in a paused frame', () => {
    const scene = Object.create(BenchmarkScene.prototype) as any;
    scene.modules = new Map([['built', new Group()], ['unbuilt', new Group()]]);
    scene.sourceColors = new Map(); scene.isolated = false; scene.selected = null;
    scene.state({ activeModules: ['built'], colors: {} });
    scene.highlight('built');
    expect(scene.modules.get('unbuilt').visible).toBe(false);
    scene.highlight('unbuilt', true);
    expect([...scene.modules.values()].some((g: Group) => g.visible)).toBe(false);
    scene.highlight(null);
    expect(scene.modules.get('built').visible).toBe(true);
    expect(scene.modules.get('unbuilt').visible).toBe(false);
  });
  it('all released geometry and nominal constraints satisfy fixed tolerances', () => {
    for (const b of bundles) {
      expect(b.validation.penetrations, b.model.id).toEqual([]);
      expect(b.validation.anchors.every((a: any) => a.initialAnchorError < 1e-7), b.model.id).toBe(true);
      expect(b.physics.nominalPointDrift, b.model.id).toBeLessThan(0.35);
      expect(b.physics.nominalAngularDrift, b.model.id).toBeLessThan(0.15);
      expect(b.physics.jointResiduals.every((j: any) => j.residual < 0.02), b.model.id).toBe(true);
    }
  });
  it('enforces all declared limits in the engine, including a driven revolute stop', async () => {
    for (const m of models()) {
      const b = await build(m);
      try {
        for (const j of m.joints.filter(j => j.limits && ['revolute', 'prismatic'].includes(j.type))) {
          const runtime = b.joints.get(j.id)! as RAPIER.RevoluteImpulseJoint;
          expect(runtime.limitsEnabled(), `${m.id}/${j.id}`).toBe(true);
          expect(runtime.limitsMin()).toBeCloseTo(j.limits![0], 5);
          expect(runtime.limitsMax()).toBeCloseTo(j.limits![1], 5);
        }
        if (m.id === 'camera-gimbal') {
          (b.joints.get('yoke-joint') as RAPIER.RevoluteImpulseJoint).configureMotorPosition(1.4, 60000, 1500);
          for (let i = 0; i < 240; i++) b.world.step();
          const r = b.bodies.get('yoke')!.rotation();
          expect(2 * Math.atan2(r.z, r.w)).toBeLessThan(0.805);
        }
      } finally { b.world.free(); }
    }
  });
  it('rejects real penetration even when the pair has a declared joint', async () => {
    const m = models().find(m => m.id === 'camera-gimbal')!;
    const mount = m.modules.find(m => m.id === 'mount')!, base = m.modules.find(m => m.anchored)!;
    const first = m.parts.find(p => p.moduleId === base.id)!;
    m.parts.push({ ...structuredClone(first), id: 'penetration-negative-control', moduleId: mount.id,
      position: new Vector3(...first.position).add(new Vector3(...base.position)).sub(new Vector3(...mount.position)).toArray() });
    await expect(validateModel(m)).rejects.toThrow('inter-module penetration');
  });
  it('preserves force application and sampled representative-point response after changing local origin', async () => {
    const m = models().find(m => m.id === 'camera-gimbal')!, changed = structuredClone(m);
    const module = changed.modules.find(x => x.id === changed.taskConfig.loadModule)!;
    const delta = new Vector3(10, 0, 0);
    module.position = new Vector3(...module.position).add(delta.clone().applyQuaternion(new Quaternion(...module.rotation))).toArray();
    for (const p of changed.parts.filter(p => p.moduleId === module.id))
      p.position = new Vector3(...p.position).sub(delta).toArray();
    for (const j of changed.joints) {
      if (j.parent === module.id) j.anchorParent = new Vector3(...j.anchorParent).sub(delta).toArray();
      if (j.child === module.id) j.anchorChild = new Vector3(...j.anchorChild).sub(delta).toArray();
    }
    const before = await physicsEvidence(m), after = await physicsEvidence(changed);
    before.impulsePoint.forEach((v, i) => expect(after.impulsePoint[i]).toBeCloseTo(v, 4));
    before.trace.forEach((v, i) => expect(after.trace[i].displacement).toBeCloseTo(v.displacement, 4));
  });
});
