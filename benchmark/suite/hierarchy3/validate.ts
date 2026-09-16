import assert from 'node:assert/strict';
import { Box3, Quaternion, Vector3 } from 'three';
import { bodyGeometry, partEnvelope, studs } from '../../../src/benchmark/geometry';
import type { Model } from './models';
import { build } from './physics';
import type RAPIER from '@dimforge/rapier3d-compat';

export async function validateModel(model: Model) {
  const get = (id: string) => {
    const m = model.modules.find(m => m.id === id); assert.ok(m, `${model.id}: unknown module ${id}`); return m;
  };
  const worldPoint = (id: string, point: number[]) => {
    const m = get(id);
    return new Vector3(...point).applyQuaternion(new Quaternion(...m.rotation)).add(new Vector3(...m.position));
  };
  for (const m of model.modules) {
    assert.ok(m.mass > 0);
    assert.ok(Math.abs(new Quaternion(...m.rotation).length() - 1) < 1e-8);
  }
  let verticesChecked = 0;
  for (const p of model.parts) {
    get(p.moduleId);
    const { center, half } = partEnvelope(p);
    const bounds = new Box3(center.clone().sub(half), center.clone().add(half)).expandByScalar(1e-6);
    const geometry = bodyGeometry(p), positions = geometry.getAttribute('position');
    for (let i = 0; i < positions.count; i++) {
      assert.ok(bounds.containsPoint(new Vector3().fromBufferAttribute(positions, i)), `${model.id}:${p.id} body outside envelope`);
      verticesChecked++;
    }
    geometry.dispose();
    for (const stud of studs(p)) for (const sign of [-1, 1]) {
      assert.ok(bounds.containsPoint(new Vector3(...stud.position).add(new Vector3(sign * stud.radius, sign * stud.height / 2, sign * stud.radius))));
    }
  }
  const anchors = model.joints.map(j => {
    get(j.parent); get(j.child);
    const error = worldPoint(j.parent, j.anchorParent).distanceTo(worldPoint(j.child, j.anchorChild));
    assert.ok(error < 1e-7 || j.type === 'spring', `${model.id}:${j.id} anchor mismatch ${error}`);
    if (j.axis) assert.ok(Math.abs(new Vector3(...j.axis).length() - 1) < 1e-7);
    return { jointId: j.id, initialAnchorError: error };
  });
  // Narrow-phase oriented cuboid contacts, including directly joined modules.
  const b = await build(model), penetrations: any[] = [], limits: any[] = [];
  try {
    for (const j of model.joints.filter(j => j.limits && ['revolute', 'prismatic'].includes(j.type))) {
      const joint = b.joints.get(j.id)! as RAPIER.RevoluteImpulseJoint;
      assert.ok(joint.limitsEnabled(), `${model.id}/${j.id}: disabled limits`);
      assert.ok(Math.abs(joint.limitsMin() - j.limits![0]) < 1e-6);
      assert.ok(Math.abs(joint.limitsMax() - j.limits![1]) < 1e-6);
      limits.push({ jointId: j.id, enabled: true, min: joint.limitsMin(), max: joint.limitsMax() });
    }
    b.world.propagateModifiedBodyPositionsToColliders();
    for (let i = 0; i < model.modules.length; i++) for (let j = i + 1; j < model.modules.length; j++) {
      const a = model.modules[i].id, c = model.modules[j].id;
      const ba = b.bodies.get(a)!, bc = b.bodies.get(c)!;
      let distance = 0;
      for (let u = 0; u < ba.numColliders(); u++) for (let v = 0; v < bc.numColliders(); v++) {
        const hit = ba.collider(u).contactCollider(bc.collider(v), 0);
        if (hit) distance = Math.min(distance, hit.distance);
      }
      if (distance < -0.005) penetrations.push({ modules: [a, c], depth: -distance });
    }
  } finally { b.world.free(); }
  assert.deepEqual(penetrations, [], `${model.id}: inter-module penetration`);
  return { verticesChecked, anchors, limits, penetrations, contactTolerance: 0.005 };
}
