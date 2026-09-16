import { Quaternion, Vector3 } from 'three';
import type { Model } from '../hierarchy3/models';
import type { MechanismJoint, MechanismModule, MechanismPart, Vec3, Quat } from '../mechanism/types';
import { geometry } from '../hierarchy3/physics';

const Q: Quat = [0, 0, 0, 1];
const C = { dark: '#273e50', white: '#dfebed', blue: '#387bb3', orange: '#dc6040', gold: '#e9ad37', green: '#45a080' };
type Kind = 'arm' | 'gripper' | 'carousel' | 'slide' | 'cradle' | 'drum'
  | 'gantry' | 'wings' | 'suspension' | 'gate' | 'probe' | 'turntable';
type Spec = { kind: Kind; zh: [string, string]; en: [string, string] };
export const FAMILIES: Spec[] = [
  { kind: 'arm', zh: ['折肘检修臂', '双段取样臂'], en: ['Elbow Service Arm', 'Two-link Sampling Arm'] },
  { kind: 'gripper', zh: ['对向夹持器', '三指夹持器'], en: ['Opposed Gripper', 'Three-finger Gripper'] },
  { kind: 'carousel', zh: ['四槽样品转盘', '六槽试管转盘'], en: ['Four-slot Sample Carousel', 'Six-slot Tube Carousel'] },
  { kind: 'slide', zh: ['十字进给台', '双导轨升降台'], en: ['Cross-feed Stage', 'Twin-rail Elevator'] },
  { kind: 'cradle', zh: ['弧架倾转托座', '双轴光学托座'], en: ['Tilting Cradle', 'Two-axis Optical Cradle'] },
  { kind: 'drum', zh: ['横轴卷筒座', '双卷筒索引器'], en: ['Horizontal Drum Stand', 'Twin-drum Indexer'] },
  { kind: 'gantry', zh: ['龙门巡检滑台', '双滑车检修架'], en: ['Gantry Inspection Stage', 'Twin-trolley Service Frame'] },
  { kind: 'wings', zh: ['折叠双翼板组', '四瓣展开板组'], en: ['Folding Twin Wings', 'Four-petal Panel Array'] },
  { kind: 'suspension', zh: ['三点弹性托盘', '四点弹性仪器台'], en: ['Three-point Elastic Tray', 'Four-point Instrument Suspension'] },
  { kind: 'gate', zh: ['旋转扇形闸门', '双叶联锁门架'], en: ['Rotary Sector Gate', 'Twin-leaf Interlock Frame'] },
  { kind: 'probe', zh: ['倾斜探针架', '三向探针架'], en: ['Inclined Probe Stand', 'Three-direction Probe Stand'] },
  { kind: 'turntable', zh: ['偏心载荷回转台', '双层维修回转台'], en: ['Offset-load Turntable', 'Two-tier Service Turntable'] },
];

// Authored digital modules; every joint anchor is computed from one world point.
// Module poses are initially identity; tilted individual parts use quaternions.
class Builder {
  modules: MechanismModule[] = [];
  parts: MechanismPart[] = [];
  joints: MechanismJoint[] = [];
  active: string[] = [];
  add(id: string, pos: Vec3, parent?: string, type: MechanismJoint['type'] = 'fixed',
    axis: Vec3 = [0, 1, 0], mass = 1.2, anchor: Vec3 = pos) {
    this.modules.push({ id, name: id.replaceAll('-', ' '), role: parent ? type === 'fixed' ? 'structure' : 'actuator' : 'foundation',
      anchored: !parent, mass: parent ? mass : 30, position: pos, rotation: Q });
    if (parent) {
      const p = this.modules.find(m => m.id === parent)!;
      this.joints.push({ id: `${id}-joint`, name: `${id} interface`, parent, child: id, type,
        anchorParent: anchor.map((v, i) => v - p.position[i]) as Vec3,
        anchorChild: anchor.map((v, i) => v - pos[i]) as Vec3, axis,
        ...(type === 'revolute' ? { limits: [-0.6, 0.6] as [number, number] }
          : type === 'prismatic' ? { limits: [-0.45, 0.45] as [number, number] } : {}) });
      if (type === 'revolute' || type === 'prismatic') this.active.push(`${id}-joint`);
    }
    return id;
  }
  part(moduleId: string, shape: MechanismPart['shape'], p: Vec3, size: Vec3, color = C.white, rotation = Q) {
    this.parts.push({ id: `${moduleId}-p${this.parts.length}`, moduleId, shape, position: p, size, color, rotation });
  }
  deck(id: string, nx: number, nz: number, p: Vec3 = [0, 0, 0], color = C.blue) {
    for (let x = 0; x < nx; x++) for (let z = 0; z < nz; z++)
      this.part(id, 'plate', [p[0] + x - (nx - 1) / 2, p[1], p[2] + z - (nz - 1) / 2],
        [0.96, 0.24, 0.96], color);
  }
  rod(id: string, start: Vec3, end: Vec3, color = C.gold, thickness = 0.3) {
    const a = new Vector3(...start), delta = new Vector3(...end).sub(a);
    const count = Math.max(1, Math.ceil(delta.length()));
    const q = new Quaternion().setFromUnitVectors(new Vector3(0, 1, 0), delta.clone().normalize()).toArray() as Quat;
    for (let i = 0; i < count; i++) this.part(id, 'beam',
      a.clone().addScaledVector(delta, (i + 0.5) / count).toArray() as Vec3,
      [thickness, delta.length() / count, thickness], color, q);
  }
  spring(parent: string, child: string, world: Vec3, n: number) {
    const local = (id: string) => world.map((v, i) => v - this.modules.find(m => m.id === id)!.position[i]) as Vec3;
    this.joints.push({ id: `${child}-elastic-${n}`, name: 'Separated elastic support', type: 'spring', parent, child,
      anchorParent: local(parent), anchorChild: local(child), restLength: 0, stiffness: 4000, damping: 160 });
  }
}

function device(b: Builder, kind: Kind, variant: number, prefix: string, center: Vec3, parent: string) {
  const world = (x: number, y: number, z: number): Vec3 => [center[0] + x, center[1] + y, center[2] + z];
  const partCount = b.parts.length;
  const mount = b.add(`${prefix}-mount`, world(0, 0, 0), parent);
  b.deck(mount, 6 + variant, 5, [0, 0, 0], C.dark);
  const mod = (name: string, x: number, y: number, z: number, type: MechanismJoint['type'] = 'fixed',
    axis: Vec3 = [0, 1, 0], owner = mount, mass = 1.2) => b.add(`${prefix}-${name}`, world(x, y, z), owner, type, axis, mass);
  let target = '', moving = '';
  if (kind === 'arm') {
    const shoulder = mod('shoulder', -1.7, 0.7, 0, 'revolute');
    b.part(shoulder, 'cylinder', [0, 0, 0], [0.9, 0.6, 0.9], C.blue);
    const elbow = mod('elbow', -1.7, 1.35, 0, 'revolute', [0, 0, 1], shoulder);
    b.rod(elbow, [0, 0, 0], [1.5, 2.4 + variant * 0.5, 0]);
    const wrist = mod('wrist', -0.2, 3.75 + variant * 0.5, 0.7, 'revolute', [0, 0, 1], elbow);
    b.rod(wrist, [0, 0, 0], [2 + variant * 0.7, -0.7, 0], C.orange);
    target = mod('tool', 1.9 + variant * 0.7, 3 + variant * 0.5, 1.3, 'prismatic', [0, 1, 0], wrist);
    b.part(target, 'arch', [0, 0, 0], [0.65, 0.65, 0.65], C.green);
    b.part(target, 'axle', [0, -0.6, 0], [0.2, 0.5, 0.2], C.white);
    moving = `${elbow}-joint`;
  } else if (kind === 'gripper') {
    const hub = mod('hub', 0, 1, 0, 'revolute');
    b.part(hub, 'cylinder', [0, 0, 0], [1.2, 1.2, 1.2], C.blue);
    for (let i = 0; i < 2 + variant; i++) {
      const a = i * Math.PI * 2 / (2 + variant), x = Math.cos(a), z = Math.sin(a);
      const finger = mod(`finger-${i}`, x * 1.25, 1.8, z * 1.25, 'revolute', [-z, 0, x], hub);
      b.rod(finger, [0, 0, 0], [x * 0.5, 1.8, z * 0.5], C.gold);
      b.part(finger, 'panel', [x * 0.5, 2, z * 0.5], [0.45, 0.3, 0.45], C.green);
      target = finger;
    }
    moving = `${hub}-joint`;
  } else if (kind === 'carousel') {
    const shaft = mod('shaft', 0, 0.8, 0);
    b.part(shaft, 'cylinder', [0, 0, 0], [0.7, 1, 0.7], C.white);
    const rotor = mod('rotor', 0, 1.65, 0, 'revolute', [0, 1, 0], shaft);
    b.part(rotor, 'gear', [0, 0, 0], [4.8, 0.3, 4.8], C.blue);
    for (let i = 0; i < 4 + 2 * variant; i++) {
      const a = i * Math.PI * 2 / (4 + 2 * variant), x = 1.8 * Math.cos(a), z = 1.8 * Math.sin(a);
      target = mod(`cup-${i}`, x, 2.3, z, 'fixed', [0, 1, 0], rotor, 0.25);
      b.part(target, 'cylinder', [0, 0, 0], [0.6, 0.6 + variant * 0.2, 0.6], C.gold);
      b.part(target, 'sphere', [0, 0.55, 0], [0.35, 0.3, 0.35], C.green);
    }
    moving = `${rotor}-joint`;
  } else if (kind === 'slide') {
    for (const x of [-1.7, 1.7]) b.rod(mount, [x, 0.5, -2], [x, 0.5, 2], C.white, 0.25);
    const carriage = mod('carriage', 0, 1, 0, 'prismatic', [0, 0, 1]);
    b.deck(carriage, 3, 2, [0, 0, 0], C.blue);
    target = mod('cross-feed', 0, 1.6, 0, 'prismatic', variant ? [0, 1, 0] : [1, 0, 0], carriage);
    b.deck(target, 2, 2, [0, 0, 0], C.orange);
    if (variant) for (const x of [-1, 1]) b.rod(carriage, [x, 0.6, -1.5], [x, 2.5, -1.5], C.gold);
    else b.rod(carriage, [-2, 0.4, -1.5], [2, 0.4, -1.5], C.gold);
    moving = `${target}-joint`;
  } else if (kind === 'cradle') {
    const yoke = mod('yoke', 0, 0.6, 0);
    for (const x of [-2.2, 2.2]) b.rod(yoke, [x, 0, 0], [x, 3, 0], C.gold, 0.4);
    b.rod(yoke, [-2.2, 0, 0], [2.2, 0, 0], C.white);
    const cradle = mod('cradle', 0, 3.3, 0, 'revolute', [1, 0, 0], yoke);
    b.part(cradle, 'cylinder', [0, 0, 0], [2.5, 1.6, 2.5], C.blue);
    target = mod('optic', 0, 4.55, 0, variant ? 'revolute' : 'fixed', [0, 1, 0], cradle, 0.5);
    b.part(target, 'cylinder', [0, 0, 0], [1.2, 0.5, 1.2], C.green);
    b.part(target, 'window', [0, 0.4, 0], [1, 0.1, 1], '#79c7d8');
    moving = `${cradle}-joint`;
  } else if (kind === 'drum') {
    for (const x of [-2.6, 2.6]) b.rod(mount, [x, 0.5, 0], [x, 2.8, 0], C.gold, 0.35);
    for (let i = 0; i < 1 + variant; i++) {
      target = mod(`drum-${i}`, variant ? (i ? 1 : -1) : 0, 2.5, 0, 'revolute', [1, 0, 0]);
      const q: Quat = [0, 0, Math.SQRT1_2, Math.SQRT1_2], width = variant ? 1.3 : 3.6;
      b.part(target, 'cylinder', [0, 0, 0], [2.4, width, 2.4], C.blue, q);
      for (const sign of [-1, 1]) b.part(target, 'gear', [sign * (width / 2 + 0.13), 0, 0], [2.7, 0.2, 2.7], C.orange, q);
    }
    moving = `${target}-joint`;
  } else if (kind === 'gantry') {
    const rail = mod('overhead', 0, 0.5, 0);
    for (const x of [-3, 3]) b.rod(rail, [x, 0, 0], [x, 4.2, 0], C.gold, 0.4);
    b.rod(rail, [-3, 4.2, 0], [3, 4.2, 0], C.gold, 0.35);
    for (let i = 0; i < 1 + variant; i++) {
      const trolley = mod(`trolley-${i}`, variant ? (i ? 1.3 : -1.3) : 0, 5.2, 0, 'prismatic', [1, 0, 0], rail);
      b.deck(trolley, 2, 2, [0, 0, 0], C.orange);
      target = mod(`probe-${i}`, variant ? (i ? 1.3 : -1.3) : 0, 3.6, 0.9, 'prismatic', [0, 1, 0], trolley, 0.3);
      b.rod(target, [0, -1.3, 0], [0, 0.8, 0], C.white, 0.18);
      b.part(target, 'sphere', [0, -1.6, 0], [0.6, 0.5, 0.6], C.green);
      moving = `${trolley}-joint`;
    }
  } else if (kind === 'wings') {
    const hub = mod('hub', 0, 1.5, 0);
    b.part(hub, 'cylinder', [0, 0, 0], [1.6, 2, 1.6], C.white);
    for (let i = 0; i < (variant ? 4 : 2); i++) {
      const a = i * Math.PI * 2 / (variant ? 4 : 2), x = Math.cos(a), z = Math.sin(a);
      target = mod(`wing-${i}`, x * 2.5, 3.1 + i * 0.12, z * 2.5, 'revolute', [-z, 0, x], hub, 0.65);
      b.deck(target, 2, 2 + variant, [0, 0, 0], C.blue);
      b.rod(target, [-0.7, -0.3, 0], [0.7, -0.3, 0], C.gold, 0.15);
    }
    moving = `${target}-joint`;
  } else if (kind === 'suspension') {
    const support = mod('support', 0, 0.65, 0);
    for (const x of [-2.5, 2.5]) {
      b.rod(support, [x, 0, -1.5], [x, 3.5, -1.5], C.gold);
      b.rod(support, [x, 3.5, -1.5], [x, 3.5, 1.5], C.white);
    }
    target = b.add(`${prefix}-elastic-tray`, world(0, 2.3, 0), support, 'spring');
    const joint = b.joints.at(-1)!; joint.stiffness = 4000; joint.damping = 160; joint.restLength = 0;
    b.deck(target, 3, 3, [0, 0, 0], C.green);
    b.spring(support, target, world(-1, 2.3, -1), 1);
    b.spring(support, target, world(1, 2.3, -1), 2);
    if (variant) b.spring(support, target, world(-1, 2.3, 1), 3);
    const sensor = mod('instrument', 0, 3.1, 0, 'revolute', [0, 1, 0], target, 0.25);
    b.part(sensor, 'cylinder', [0, 0, 0], [0.8, 0.8, 0.8], C.blue);
    b.part(sensor, 'sphere', [0, 0.7, 0], [0.6, 0.4, 0.6], C.orange);
    moving = `${sensor}-joint`;
  } else if (kind === 'gate') {
    for (const x of [-2.8, 2.8]) b.rod(mount, [x, 0.5, 0], [x, 3.8, 0], C.white, 0.35);
    for (let i = 0; i < 1 + variant; i++) {
      target = mod(`leaf-${i}`, variant ? (i ? 1.15 : -1.15) : 0, 2.2, 0.7,
        'revolute', [0, 1, 0]);
      const w = variant ? 1.9 : 4.5;
      for (let n = 0; n < 4; n++) b.part(target, 'panel', [(n - 1.5) * w / 4, 0, 0], [w / 4, 2.3, 0.25], C.orange);
      b.rod(target, [-w / 2, 0.6, -0.3], [w / 2, -0.6, -0.3], C.gold, 0.18);
    }
    moving = `${target}-joint`;
  } else if (kind === 'probe') {
    const hub = mod('hub', 0, 1, 0, 'revolute');
    b.part(hub, 'cylinder', [0, 0, 0], [1, 1.2, 1], C.blue);
    for (let i = 0; i < (variant ? 3 : 1); i++) {
      const a = i * Math.PI * 2 / 3, x = Math.cos(a), z = Math.sin(a);
      target = mod(`probe-${i}`, x, 2.2, z, 'prismatic', [x * 0.6, 0.8, z * 0.6], hub, 0.5);
      b.rod(target, [0, 0, 0], [x * 1.4, 2, z * 1.4], C.gold, 0.25);
      b.part(target, 'sphere', [x * 1.5, 2.2, z * 1.5], [0.55, 0.55, 0.55], C.green);
    }
    moving = `${target}-joint`;
  } else {
    const pedestal = mod('pedestal', 0, 0.9, 0);
    b.part(pedestal, 'cylinder', [0, 0, 0], [1.7, 1.2, 1.7], C.white);
    const rotor = mod('rotor', 0, 1.9, 0, 'revolute', [0, 1, 0], pedestal);
    b.deck(rotor, 4, 4, [0, 0, 0], C.blue);
    target = mod('offset-load', 1, 2.7, 0.6, 'fixed', [0, 1, 0], rotor, 0.8);
    b.part(target, 'cylinder', [0, 0, 0], [1.3, 1.1, 1.3], C.orange);
    b.part(target, 'gear', [0, 0.75, 0], [1.4, 0.25, 1.4], C.gold);
    if (variant) {
      const tier = mod('upper-stage', -1, 3, -1, 'prismatic', [0, 1, 0], rotor, 0.8);
      b.deck(tier, 2, 2, [0, 0, 0], C.green);
    }
    moving = `${rotor}-joint`;
  }
  return { target, moving, parts: b.parts.length - partCount };
}

export function expansionModels(): Model[] {
  return [1, 2, 3, 4].flatMap(level => FAMILIES.flatMap((spec, familyIndex) => [0, 1].map(variant => {
    const b = new Builder(), difficulty = `D${level}` as Model['difficulty'];
    const id = `exp-${difficulty.toLowerCase()}-${spec.kind}-${variant + 1}`;
    const prefixZh = ['', '', '装配单元·', '复合机构·', '协同系统·'][level];
    const names = ['', '', ' Assembly', ' Compound Mechanism', ' Service System'];
    const base = b.add('foundation', [0, 0.15, 0]);
    // Stage count and serial dependency grow with level; distinct constructors
    // are deliberately shared across levels for matched-family comparisons.
    const stationCount = level < 3 ? 1 : level === 3 ? 2 : 3 + variant;
    const spacing = 13;
    for (let i = 0; i < stationCount; i++) {
      const x = (i - (stationCount - 1) / 2) * spacing;
      b.deck(base, 8, 7, [x, 0, 0], C.dark);
      if (i) b.rod(base, [x - spacing + 3.5, 0, -2.8], [x - 3.5, 0, -2.8], C.dark, 0.2);
    }
    let selected: ReturnType<typeof device> | undefined;
    for (let i = 0; i < stationCount; i++) {
      const x = (i - (stationCount - 1) / 2) * spacing;
      let owner = base, elevation = 0.65;
      if (level >= 2) {
        const shuttle = b.add(`cell-${i}-shuttle`, [x, 0.7, 0], base, 'prismatic', variant ? [0, 0, 1] : [1, 0, 0], 3);
        b.deck(shuttle, 8, 6, [0, 0, 0], C.white);
        owner = shuttle; elevation = 1.3;
      }
      const kind = i === 0 ? spec.kind : FAMILIES[(familyIndex + i * 3 + variant) % FAMILIES.length].kind;
      const built = device(b, kind, (variant + i) % 2, `cell-${i}`, [x, elevation, 0], owner);
      selected ??= built;
      if (level >= 2) {
        const console = b.add(`cell-${i}-console`, [x, 1.3, 6], base);
        b.deck(console, 3, 2, [0, 0, 0], C.orange);
        b.part(console, 'window', [0, 0.6, -0.3], [1.8, 0.75, 0.15], '#79c7d8');
        b.part(console, 'slope', [0, 1.1, 0], [2, 0.35, 1.8], C.white);
      }
      if (level >= 3) {
        const magazine = b.add(`cell-${i}-magazine`, [x, 0.8, -6], base);
        for (let row = 0; row < level; row++) b.deck(magazine, 4, 3, [0, row * 1.2, 0], C.white);
        for (const sx of [-1.8, 1.8]) b.rod(magazine, [sx, 0, -1.2], [sx, level * 1.2, -1.2], C.gold, 0.2);
        const drawer = b.add(`cell-${i}-drawer`, [x, 1.5, -6], magazine, 'prismatic', [0, 0, 1], 0.7);
        b.deck(drawer, 3, 2, [0, 0, 0], C.green);
      }
    }
    if (level === 4) {
      const scanner = b.add('shared-inspection-mast', [0, 1, 11], base);
      for (const x of [-1.5, 1.5]) b.rod(scanner, [x, 0, 0], [x, 5, 0], C.white, 0.4);
      b.rod(scanner, [-1.5, 5, 0], [1.5, 5, 0], C.gold, 0.35);
      const head = b.add('shared-scanner', [0, 6.8, 11], scanner, 'revolute', [0, 1, 0]);
      b.part(head, 'cylinder', [0, 0, 0], [1.3, 0.6, 1.3], C.orange);
      b.part(head, 'window', [0, 0.6, 0], [1.1, 0.25, 1.1], '#79c7d8');
    }
    const model: Model = { id, name: spec.en[variant] + names[level], nameZh: prefixZh + spec.zh[variant],
      family: spec.kind, lineage: `expanded-${spec.kind}`, domain: 'authored service mechanisms',
      difficulty, originalDesign: true, modules: b.modules, parts: b.parts, joints: b.joints,
      description: `${stationCount} service station(s), ${level >= 2 ? 'movable carrier' : 'fixed fixture'}, ${spec.en[variant]}. `
        + 'Independent joint actuators; no inferred gear coupling or commercial connector claim.',
      assemblyOrder: b.modules.map(m => m.id),
      taskConfig: { serviceModule: selected!.target, functionalJoint: selected!.moving, loadModule: selected!.target,
        functionalTarget: 0.3, faultJoint: b.joints.find(j => j.child === selected!.target)!.id,
        accessPaths: [], recoveryActions: [], impulseCandidates: [1, 5, 20],
        robustnessLimits: { maxTransientDisplacement: 0.5, maxResidualDisplacement: 0.2 },
        inventoryAlternatives: [], inventoryRequirements: { maxCost: 6, maxPieces: 2, minStiffness: 8 },
        hiddenWorlds: [], inspectionQueries: [] } };
    // Same geometry-center convention as the existing protocol, without applying
    // legacy model-specific relocation patches.
    const centers = geometry(model).centers;
    for (const m of model.modules) {
      const shift = new Vector3(...centers[m.id]).sub(new Vector3(...m.position));
      m.position = centers[m.id] as Vec3;
      for (const p of model.parts.filter(p => p.moduleId === m.id)) p.position = new Vector3(...p.position).sub(shift).toArray() as Vec3;
      for (const j of model.joints) {
        if (j.parent === m.id) j.anchorParent = new Vector3(...j.anchorParent).sub(shift).toArray() as Vec3;
        if (j.child === m.id) j.anchorChild = new Vector3(...j.anchorChild).sub(shift).toArray() as Vec3;
      }
    }
    return model;
  })));
}
