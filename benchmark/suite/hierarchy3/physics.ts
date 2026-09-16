import RAPIER from '@dimforge/rapier3d-compat';
import { Box3, Matrix4, Quaternion, Vector3 } from 'three';
import type { Model } from './models';
import type { Vec3 } from '../mechanism/types';
import { partEnvelope } from '../../../src/benchmark/geometry';

const v = (a: number[]) => ({ x: a[0], y: a[1], z: a[2] });
const q = (a: number[]) => ({ x: a[0], y: a[1], z: a[2], w: a[3] });
const transform = (p: number[], r: number[]) =>
  new Matrix4().compose(new Vector3(...p), new Quaternion(...r), new Vector3(1, 1, 1));
let ready: Promise<void> | undefined;

export function geometry(model: Model) {
  const boxes = model.parts.map(p => {
    const module = model.modules.find(m => m.id === p.moduleId)!;
    const matrix = transform(module.position, module.rotation).multiply(transform(p.position, p.rotation));
    const { half, center } = partEnvelope(p);
    const box = new Box3(center.clone().sub(half), center.clone().add(half)).applyMatrix4(matrix);
    return { id: p.id, moduleId: p.moduleId, box };
  });
  const bounds = new Box3();
  for (const { box } of boxes) bounds.union(box);
  const centers = Object.fromEntries(model.modules.map(m => {
    const box = new Box3();
    boxes.filter(p => p.moduleId === m.id).forEach(p => box.union(p.box));
    return [m.id, box.getCenter(new Vector3()).toArray()];
  }));
  let interModuleEnvelopeOverlaps = 0;
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    if (boxes[i].moduleId === boxes[j].moduleId) continue;
    const size = boxes[i].box.clone().intersect(boxes[j].box).getSize(new Vector3());
    if (Math.min(size.x, size.y, size.z) > 0.04) interModuleEnvelopeOverlaps++;
  }
  return { bounds: { min: bounds.min.toArray(), max: bounds.max.toArray() },
    centers, interModuleEnvelopeOverlaps };
}

export async function build(model: Model) {
  await (ready ??= RAPIER.init());
  const world = new RAPIER.World({ x: 0, y: -9.81, z: 0 });
  world.timestep = 1 / 120; world.numSolverIterations = 64;
  const bodies = new Map<string, RAPIER.RigidBody>();
  for (const m of model.modules) {
    const desc = m.anchored ? RAPIER.RigidBodyDesc.fixed()
      : RAPIER.RigidBodyDesc.dynamic().setLinearDamping(0.4).setAngularDamping(0.6);
    const body = world.createRigidBody(desc.setTranslation(...m.position).setRotation(q(m.rotation)));
    bodies.set(m.id, body);
    const parts = model.parts.filter(p => p.moduleId === m.id);
    for (const p of parts) {
      const { half, center } = partEnvelope(p);
      center.applyQuaternion(new Quaternion(...p.rotation)).add(new Vector3(...p.position));
      world.createCollider(RAPIER.ColliderDesc.cuboid(half.x, half.y, half.z)
        .setTranslation(center.x, center.y, center.z).setRotation(q(p.rotation)).setMass(m.mass / parts.length), body);
    }
  }
  const joints = new Map<string, RAPIER.ImpulseJoint>();
  for (const j of model.joints) {
    const a = v(j.anchorParent), b = v(j.anchorChild);
    const data = j.type === 'fixed' ? RAPIER.JointData.fixed(a, q([0, 0, 0, 1]), b, q([0, 0, 0, 1]))
      : j.type === 'revolute' ? RAPIER.JointData.revolute(a, b, v(j.axis ?? [0, 1, 0]))
        : j.type === 'prismatic' ? RAPIER.JointData.prismatic(a, b, v(j.axis ?? [1, 0, 0]))
          : RAPIER.JointData.spring(j.restLength ?? 0, j.stiffness ?? 60, j.damping ?? 10, a, b);
    if (j.limits && ['revolute', 'prismatic'].includes(j.type)) {
      data.limitsEnabled = true; data.limits = j.limits;
    }
    const joint = world.createImpulseJoint(data, bodies.get(j.parent)!, bodies.get(j.child)!, true);
    joint.setContactsEnabled(true); joints.set(j.id, joint);
    if (j.type === 'revolute' || j.type === 'prismatic') {
      const motor = joint as RAPIER.RevoluteImpulseJoint;
      if (j.limits) motor.setLimits(j.limits[0], j.limits[1]);
      // Finite force position servos; the setting is part of the public protocol.
      motor.configureMotorModel(RAPIER.MotorModel.ForceBased);
      motor.configureMotorPosition(0, 60000, 1500); motor.setMotorMaxForce(20000);
    }
  }
  return { world, bodies, joints };
}

export async function physicsEvidence(model: Model) {
  const shape = geometry(model), service = model.taskConfig.serviceModule;
  const b = await build(model);
  try {
    // Static query colliders are built separately so dynamic settling cannot relabel access.
    const query = new RAPIER.World({ x: 0, y: 0, z: 0 });
    for (const p of model.parts.filter(p => p.moduleId !== service)) {
      const m = model.modules.find(m => m.id === p.moduleId)!;
      const { half, center } = partEnvelope(p);
      const matrix = transform(m.position, m.rotation).multiply(transform(p.position, p.rotation))
        .multiply(new Matrix4().makeTranslation(center.x, center.y, center.z));
      const pos = new Vector3(), rot = new Quaternion(); matrix.decompose(pos, rot, new Vector3());
      query.createCollider(RAPIER.ColliderDesc.cuboid(half.x, half.y, half.z)
        .setTranslation(pos.x, pos.y, pos.z).setRotation(rot));
    }
    query.step();
    const center = shape.centers[service];
    const paths = ([0, 1, 2] as const).map(axis => {
      const start = [...center] as Vec3;
      start[axis] = shape.bounds.max[axis] + 4;
      const end = [...center] as Vec3;
      const hit = query.castShape(v(start), q([0, 0, 0, 1]),
        v(end.map((n, i) => n - start[i])), new RAPIER.Cuboid(0.18, 0.18, 0.18), 0, 1, true);
      return { id: `path-${axis}`, start, end, halfExtents: [0.18, 0.18, 0.18],
        clear: !hit, timeOfImpact: hit?.time_of_impact ?? null };
    });
    query.free();
    for (let i = 0; i < 120; i++) b.world.step();
    const nominalDrift = Math.max(...model.modules.map(m => {
      const p = b.bodies.get(m.id)!.translation();
      return Math.hypot(p.x - m.position[0], p.y - m.position[1], p.z - m.position[2]);
    }));
    const moduleMotion = model.modules.map(m => {
      const body = b.bodies.get(m.id)!, position = body.translation(), rotation = body.rotation();
      const initialRotation = new Quaternion(...m.rotation), currentRotation = new Quaternion(rotation.x, rotation.y, rotation.z, rotation.w);
      const point = new Vector3(...shape.centers[m.id]).sub(new Vector3(...m.position)).applyQuaternion(initialRotation.clone().invert());
      const currentPoint = point.clone().applyQuaternion(currentRotation).add(new Vector3(position.x, position.y, position.z));
      return { moduleId: m.id, pointDisplacement: currentPoint.distanceTo(new Vector3(...shape.centers[m.id])),
        angularDisplacement: initialRotation.angleTo(currentRotation) };
    });
    const nominalPointDrift = Math.max(...moduleMotion.map(m => m.pointDisplacement));
    const nominalAngularDrift = Math.max(...moduleMotion.map(m => m.angularDisplacement));
    const jointResiduals = model.joints.filter(j => j.type !== 'spring').map(j => {
      const a = b.bodies.get(j.parent)!, c = b.bodies.get(j.child)!;
      const worldPoint = (body: RAPIER.RigidBody, point: Vec3) => {
        const r = body.rotation(), p = body.translation();
        return new Vector3(...point).applyQuaternion(new Quaternion(r.x, r.y, r.z, r.w)).add(new Vector3(p.x, p.y, p.z));
      };
      const delta = worldPoint(c, j.anchorChild).sub(worldPoint(a, j.anchorParent));
      if (j.type === 'prismatic') {
        const r = a.rotation(), axis = new Vector3(...(j.axis ?? [1, 0, 0])).applyQuaternion(new Quaternion(r.x, r.y, r.z, r.w));
        delta.addScaledVector(axis, -delta.dot(axis));
      }
      return { jointId: j.id, residual: delta.length() };
    });
    const loadId = model.taskConfig.loadModule;
    const load = b.bodies.get(loadId)!, loadModule = model.modules.find(m => m.id === loadId)!;
    const localPoint = new Vector3(...shape.centers[loadId]).sub(new Vector3(...loadModule.position))
      .applyQuaternion(new Quaternion(...loadModule.rotation).invert());
    const representativePoint = () => {
      const position = load.translation(), rotation = load.rotation();
      return localPoint.clone().applyQuaternion(new Quaternion(rotation.x, rotation.y, rotation.z, rotation.w))
        .add(new Vector3(position.x, position.y, position.z));
    };
    const start = representativePoint();
    load.applyImpulseAtPoint({ x: 10, y: 1.8, z: 3.5 },
      { x: start.x, y: start.y + 1, z: start.z }, true);
    const trace: Array<{ time: number; displacement: number }> = [];
    for (let i = 0; i < 120; i++) {
      b.world.step();
      if (i % 12 === 0 || i === 119) {
        const p = representativePoint();
        trace.push({ time: (i + 1) / 120, displacement: Math.hypot(p.x - start.x, p.y - start.y, p.z - start.z) });
      }
    }
    if (![nominalDrift, ...trace.map(r => r.displacement)].every(Number.isFinite))
      throw new Error(`${model.id}: nonfinite simulation`);
    return { engine: 'Rapier 0.20.0', hz: 120, solverIterations: 64, nominalDrift,
      nominalPointDrift, nominalAngularDrift, moduleMotion, jointResiduals,
      motor: { model: 'force-based', stiffness: 60000, damping: 1500, maxForce: 20000, target: 0 },
      nominalWithinTolerance: nominalPointDrift < 0.35 && nominalAngularDrift < 0.15
        && jointResiduals.every(j => j.residual < 0.02),
      paths, impulse: [10, 1.8, 3.5], impulsePoint: [start.x, start.y + 1, start.z],
      tracePoint: 'initial geometric envelope center attached to load module', trace,
      scope: 'stud-inclusive conservative cuboids; anchored base; force-limited position servos; no clutch/material calibration' };
  } finally { b.world.free(); }
}
