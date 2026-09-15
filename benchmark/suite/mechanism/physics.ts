import RAPIER from '@dimforge/rapier3d-compat';
import { type MechanismJoint, type MechanismModel, type Quat, type Vec3 } from './types';

let ready: Promise<void> | undefined;
export function initPhysics() {
  return ready ??= RAPIER.init();
}

const vector = ([x, y, z]: Vec3) => ({ x, y, z });
const rotation = ([x, y, z, w]: Quat) => ({ x, y, z, w });
const distance = (a: { x: number; y: number; z: number }, b: Vec3) =>
  Math.hypot(a.x - b[0], a.y - b[1], a.z - b[2]);

function colliderFor(part: MechanismModel['parts'][number]) {
  const [sx, sy, sz] = part.size;
  if (part.shape === 'sphere') return RAPIER.ColliderDesc.ball(Math.max(sx, sy, sz) / 2);
  if (['cylinder', 'wheel', 'axle', 'gear'].includes(part.shape)) {
    return RAPIER.ColliderDesc.cylinder(sy / 2, Math.max(sx, sz) / 2);
  }
  // Slopes and arches use conservative convex envelopes in the physics track.
  return RAPIER.ColliderDesc.cuboid(sx / 2, sy / 2, sz / 2);
}

function jointData(joint: MechanismJoint) {
  if (joint.type === 'fixed') {
    return RAPIER.JointData.fixed(vector(joint.anchorParent), rotation([0, 0, 0, 1]),
      vector(joint.anchorChild), rotation([0, 0, 0, 1]));
  }
  if (joint.type === 'revolute') {
    const data = RAPIER.JointData.revolute(vector(joint.anchorParent), vector(joint.anchorChild),
      vector(joint.axis ?? [0, 1, 0]));
    if (joint.limits) { data.limitsEnabled = true; data.limits = [...joint.limits]; }
    return data;
  }
  if (joint.type === 'prismatic') {
    const data = RAPIER.JointData.prismatic(vector(joint.anchorParent), vector(joint.anchorChild),
      vector(joint.axis ?? [1, 0, 0]));
    if (joint.limits) { data.limitsEnabled = true; data.limits = [...joint.limits]; }
    return data;
  }
  return RAPIER.JointData.spring(joint.restLength ?? 0, joint.stiffness ?? 20,
    joint.damping ?? 4, vector(joint.anchorParent), vector(joint.anchorChild));
}

interface BuiltWorld {
  world: RAPIER.World;
  bodies: Map<string, RAPIER.RigidBody>;
  joints: Map<string, RAPIER.ImpulseJoint>;
}

async function buildWorld(model: MechanismModel, options: {
  moduleIds?: Set<string>;
  omitJointIds?: Set<string>;
  staticOnly?: boolean;
  gravity?: Vec3;
} = {}): Promise<BuiltWorld> {
  await initPhysics();
  const world = new RAPIER.World(vector(options.gravity ?? [0, -9.81, 0]));
  world.timestep = 1 / 120;
  world.numSolverIterations = 12;
  world.numInternalPgsIterations = 2;
  const ground = world.createRigidBody(RAPIER.RigidBodyDesc.fixed().setTranslation(0, -.3, 0));
  world.createCollider(RAPIER.ColliderDesc.cuboid(30, .3, 30).setFriction(.9), ground);
  const bodies = new Map<string, RAPIER.RigidBody>();
  for (const module of model.modules.filter(m => !options.moduleIds || options.moduleIds.has(m.id))) {
    const desc = options.staticOnly || module.anchored
      ? RAPIER.RigidBodyDesc.fixed()
      : RAPIER.RigidBodyDesc.dynamic().setLinearDamping(.35).setAngularDamping(.45);
    desc.setTranslation(...module.position).setRotation(rotation(module.rotation));
    const body = world.createRigidBody(desc);
    bodies.set(module.id, body);
    const parts = model.parts.filter(p => p.moduleId === module.id);
    for (const part of parts) {
      const collider = colliderFor(part)
        .setTranslation(...part.position)
        .setRotation(rotation(part.rotation))
        .setFriction(.8)
        .setRestitution(0)
        .setMass(module.mass / Math.max(1, parts.length));
      world.createCollider(collider, body);
    }
  }
  const joints = new Map<string, RAPIER.ImpulseJoint>();
  for (const joint of model.joints) {
    if (options.omitJointIds?.has(joint.id)) continue;
    const parent = bodies.get(joint.parent), child = bodies.get(joint.child);
    if (!parent || !child) continue;
    const created = world.createImpulseJoint(jointData(joint), parent, child, true);
    created.setContactsEnabled(false);
    joints.set(joint.id, created);
  }
  return { world, bodies, joints };
}

function configureHoldingMotors(model: MechanismModel, built: BuiltWorld, except?: string,
  mode: 'rigid' | 'compliant' = 'rigid') {
  for (const spec of model.joints) {
    if (spec.id === except || !['revolute', 'prismatic'].includes(spec.type)) continue;
    const joint = built.joints.get(spec.id) as RAPIER.RevoluteImpulseJoint | RAPIER.PrismaticImpulseJoint | undefined;
    if (!joint) continue;
    joint.configureMotorPosition(0, mode === 'rigid' ? 1200 : 120, mode === 'rigid' ? 100 : 20);
    joint.setMotorMaxForce(mode === 'rigid' ? 5000 : 80);
  }
}

function step(world: RAPIER.World, count: number) {
  for (let i = 0; i < count; i++) world.step();
}

function quaternionAngle(a: RAPIER.Rotation, b: Quat) {
  const dot = Math.min(1, Math.abs(a.x * b[0] + a.y * b[1] + a.z * b[2] + a.w * b[3]));
  return 2 * Math.acos(dot);
}

export async function simulatePrefix(model: MechanismModel, order: string[]) {
  const builtIds = new Set<string>();
  const traces: Array<{ step: number; moduleId: string; stable: boolean; maxDisplacement: number }> = [];
  let firstUnstableStep: number | null = null;
  for (let index = 0; index < order.length; index++) {
    builtIds.add(order[index]);
    const built = await buildWorld(model, { moduleIds: builtIds });
    configureHoldingMotors(model, built);
    step(built.world, 120);
    const displacement = Math.max(...[...builtIds].map(id => {
      const body = built.bodies.get(id)!;
      return distance(body.translation(), model.modules.find(m => m.id === id)!.position);
    }));
    const stable = displacement < .35;
    traces.push({ step: index, moduleId: order[index], stable, maxDisplacement: displacement });
    built.world.free();
    if (!stable) { firstUnstableStep = index; break; }
  }
  return { success: Number(firstUnstableStep === null && builtIds.size === model.modules.length),
    firstUnstableStep, traces };
}

export async function evaluateAccessPaths(model: MechanismModel) {
  const service = model.modules.find(m => m.id === model.taskConfig.serviceModule)!;
  const included = new Set(model.modules.filter(m => m.id !== service.id).map(m => m.id));
  const built = await buildWorld(model, { moduleIds: included, staticOnly: true, gravity: [0, 0, 0] });
  built.world.step();
  const results = model.taskConfig.accessPaths.map(path => {
    const velocity = {
      x: path.end[0] - path.start[0],
      y: path.end[1] - path.start[1],
      z: path.end[2] - path.start[2],
    };
    const shape = new RAPIER.Cuboid(...path.halfExtents);
    const hit = built.world.castShape(vector(path.start), rotation([0, 0, 0, 1]), velocity,
      shape, 0, 1, true);
    return {
      pathId: path.id,
      accessible: !hit,
      timeOfImpact: hit?.time_of_impact ?? null,
      blockingModule: hit ? [...built.bodies].find(([, body]) => body.handle === hit.collider.parent()?.handle)?.[0] ?? null : null,
    };
  });
  built.world.free();
  return results;
}

export async function simulateFunctionalMotion(model: MechanismModel) {
  const spec = model.joints.find(j => j.id === model.taskConfig.functionalJoint)!;
  const childModule = model.modules.find(m => m.id === spec.child)!;
  const built = await buildWorld(model);
  configureHoldingMotors(model, built, spec.id);
  const joint = built.joints.get(spec.id) as RAPIER.RevoluteImpulseJoint | RAPIER.PrismaticImpulseJoint;
  joint.configureMotorPosition(model.taskConfig.functionalTarget, 120, 24);
  joint.setMotorMaxForce(120);
  step(built.world, 300);
  const child = built.bodies.get(spec.child)!;
  const motion = spec.type === 'prismatic'
    ? distance(child.translation(), childModule.position)
    : quaternionAngle(child.rotation(), childModule.rotation);
  const result = {
    jointId: spec.id,
    jointType: spec.type,
    target: model.taskConfig.functionalTarget,
    measuredMotion: motion,
    reachesTarget: motion >= Math.abs(model.taskConfig.functionalTarget) * .55,
  };
  built.world.free();
  return result;
}

export async function simulateImpulseLadder(model: MechanismModel) {
  const target = model.modules.find(m => m.id === model.taskConfig.loadModule)!;
  const rows = [];
  for (const impulse of model.taskConfig.impulseCandidates) {
    const built = await buildWorld(model);
    configureHoldingMotors(model, built, undefined, 'compliant');
    step(built.world, 240);
    const body = built.bodies.get(target.id)!;
    const start = body.translation();
    const origin: Vec3 = [start.x, start.y, start.z];
    const originRotation = body.rotation();
    const originQuat: Quat = [originRotation.x, originRotation.y, originRotation.z, originRotation.w];
    const radius = Math.max(1, ...model.parts.filter(p => p.moduleId === target.id).map(p =>
      Math.hypot(...p.position) + Math.max(...p.size) / 2));
    body.applyImpulseAtPoint({ x: impulse, y: impulse * .18, z: impulse * .35 },
      { x: start.x, y: start.y + 1, z: start.z }, true);
    let maxDisplacement = 0;
    for (let i = 0; i < 240; i++) {
      built.world.step();
      const equivalentMotion = Math.max(distance(body.translation(), origin),
        quaternionAngle(body.rotation(), originQuat) * radius);
      maxDisplacement = Math.max(maxDisplacement, equivalentMotion);
    }
    const finalDisplacement = Math.max(distance(body.translation(), origin),
      quaternionAngle(body.rotation(), originQuat) * radius);
    rows.push({ impulse, maxDisplacement, finalDisplacement,
      safe: maxDisplacement < model.taskConfig.robustnessLimits.maxTransientDisplacement
        && finalDisplacement < model.taskConfig.robustnessLimits.maxResidualDisplacement });
    built.world.free();
  }
  return rows;
}

export async function simulateJointFault(model: MechanismModel, jointId: string) {
  const spec = model.joints.find(j => j.id === jointId)!;
  const child = model.modules.find(m => m.id === spec.child)!;
  const built = await buildWorld(model, { omitJointIds: new Set([jointId]) });
  configureHoldingMotors(model, built);
  const body = built.bodies.get(child.id)!;
  step(built.world, 240);
  const displacement = distance(body.translation(), child.position);
  const tilt = quaternionAngle(body.rotation(), child.rotation);
  built.world.free();
  return { jointId, childModule: child.id, displacement, tilt, failed: displacement > .5 || tilt > .35 };
}

export function paretoAlternatives(model: MechanismModel) {
  const candidates = model.taskConfig.inventoryAlternatives.filter(c =>
    c.cost <= model.taskConfig.inventoryRequirements.maxCost
    && c.pieces <= model.taskConfig.inventoryRequirements.maxPieces
    && c.stiffness >= model.taskConfig.inventoryRequirements.minStiffness
    && c.jointMode !== 'none');
  return candidates.filter(a => !candidates.some(b => b.id !== a.id
    && b.cost <= a.cost && b.mass <= a.mass && b.stiffness >= a.stiffness
    && (b.cost < a.cost || b.mass < a.mass || b.stiffness > a.stiffness)));
}
