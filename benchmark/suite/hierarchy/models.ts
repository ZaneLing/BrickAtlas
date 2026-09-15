import assert from 'node:assert/strict';
import { mechanismModels } from '../mechanism/models';
import {
  IDENTITY_QUAT,
  type InventoryAlternative,
  type MechanismJoint,
  type MechanismModule,
  type MechanismPart,
  type Quat,
  type ShapeKind,
  type Vec3,
} from '../mechanism/types';
import { DIFFICULTIES, type DifficultyId, type HierarchyModel } from './types';

const C = {
  red: '#d43a32',
  blue: '#2878b8',
  navy: '#173b63',
  yellow: '#f2bf3c',
  orange: '#e8792e',
  white: '#edf1f2',
  gray: '#8c99a3',
  dark: '#26323b',
  black: '#101820',
  glass: '#79c7d8',
  green: '#3f8a61',
  lime: '#8ebf45',
  silver: '#c6cdd2',
  magenta: '#a94872',
};

function quatEuler(x = 0, y = 0, z = 0): Quat {
  const cx = Math.cos(x / 2), sx = Math.sin(x / 2);
  const cy = Math.cos(y / 2), sy = Math.sin(y / 2);
  const cz = Math.cos(z / 2), sz = Math.sin(z / 2);
  return [
    sx * cy * cz - cx * sy * sz,
    cx * sy * cz + sx * cy * sz,
    cx * cy * sz - sx * sy * cz,
    cx * cy * cz + sx * sy * sz,
  ];
}

class Builder {
  modules: MechanismModule[] = [];
  parts: MechanismPart[] = [];
  joints: MechanismJoint[] = [];
  private serial = 0;

  module(id: string, name: string, role: string, anchored = false, mass = 1) {
    this.modules.push({ id, name, role, anchored, mass, position: [0, 0, 0], rotation: IDENTITY_QUAT });
    return id;
  }

  part(moduleId: string, shape: ShapeKind, size: Vec3, position: Vec3, color: string,
    rotation: Quat = IDENTITY_QUAT) {
    this.parts.push({
      id: `h${String(++this.serial).padStart(4, '0')}`,
      moduleId,
      shape,
      size,
      position,
      rotation,
      color,
    });
  }

  line(moduleId: string, count: number, start: Vec3, step: Vec3, color: string,
    size: Vec3 = [0.9, 0.45, 0.9], shape: ShapeKind = 'brick') {
    for (let index = 0; index < count; index++) {
      this.part(moduleId, shape, size, [
        start[0] + step[0] * index,
        start[1] + step[1] * index,
        start[2] + step[2] * index,
      ], color);
    }
  }

  grid(moduleId: string, nx: number, nz: number, origin: Vec3, color: string,
    size: Vec3 = [0.92, 0.25, 0.92], gap = 1) {
    for (let x = 0; x < nx; x++) for (let z = 0; z < nz; z++) {
      this.part(moduleId, 'plate', size, [origin[0] + x * gap, origin[1], origin[2] + z * gap], color);
    }
  }

  ring(moduleId: string, count: number, center: Vec3, radius: number, color: string,
    shape: ShapeKind = 'brick') {
    for (let index = 0; index < count; index++) {
      const angle = index * Math.PI * 2 / count;
      this.part(moduleId, shape, [1.15, 0.55, 0.8], [
        center[0] + Math.cos(angle) * radius,
        center[1],
        center[2] + Math.sin(angle) * radius,
      ], color, quatEuler(0, -angle, 0));
    }
  }

  connect(id: string, parent: string, child: string, type: MechanismJoint['type'],
    anchor: Vec3, axis: Vec3 = [0, 1, 0], limits?: [number, number]) {
    this.joints.push({
      id,
      name: id.replaceAll('-', ' '),
      type,
      parent,
      child,
      anchorParent: anchor,
      anchorChild: anchor,
      axis,
      limits,
    });
  }
}

function inventory(seed: number): {
  alternatives: InventoryAlternative[];
  requirements: { maxCost: number; maxPieces: number; minStiffness: number };
} {
  const alternatives: InventoryAlternative[] = [
    { id: 'long-beam', label: 'One rigid long beam', pieces: 1, cost: 6, mass: 1.8,
      stiffness: 9, jointMode: 'fixed' },
    { id: 'paired-truss', label: 'Two interlocked short trusses', pieces: 2, cost: 5, mass: 2.2,
      stiffness: 11, jointMode: 'fixed' },
    { id: 'cable-stay', label: 'One light tension stay', pieces: 1, cost: 3, mass: 0.6,
      stiffness: 7, jointMode: 'spring' },
    { id: 'fairing', label: 'One cosmetic fairing', pieces: 1, cost: 2, mass: 0.8,
      stiffness: 1, jointMode: 'none' },
  ];
  const requirements = [
    { maxCost: 5, maxPieces: 2, minStiffness: 10 },
    { maxCost: 6, maxPieces: 1, minStiffness: 8 },
    { maxCost: 4, maxPieces: 1, minStiffness: 6 },
  ][seed % 3];
  return { alternatives, requirements };
}

function inspections(prefix: string, seed: number) {
  const costs = [1 + seed % 3, 1 + (seed + 1) % 3, 1 + (seed + 2) % 3];
  return {
    hiddenWorlds: ['nominal', 'reversed', 'missing-brace', 'jammed'],
    inspectionQueries: [
      {
        id: `${prefix}-marker`,
        label: 'Inspect orientation marker',
        cost: costs[0],
        returns: { nominal: 'forward', reversed: 'reverse', 'missing-brace': 'forward', jammed: 'forward' },
      },
      {
        id: `${prefix}-brace`,
        label: 'Inspect concealed brace interface',
        cost: costs[1],
        returns: { nominal: 'present', reversed: 'present', 'missing-brace': 'absent', jammed: 'present' },
      },
      {
        id: `${prefix}-probe`,
        label: 'Apply low-force motion probe',
        cost: costs[2],
        returns: { nominal: 'positive', reversed: 'negative', 'missing-brace': 'positive', jammed: 'none' },
      },
    ],
  };
}

function dependencyDepth(modules: MechanismModule[], joints: MechanismJoint[]) {
  const depth = new Map(modules.filter(module => module.anchored).map(module => [module.id, 0]));
  for (let pass = 0; pass < modules.length; pass++) {
    for (const joint of joints) {
      const parent = depth.get(joint.parent);
      if (parent !== undefined && !depth.has(joint.child)) depth.set(joint.child, parent + 1);
    }
  }
  return Math.max(0, ...depth.values());
}

function withComplexity(model: Omit<HierarchyModel, 'complexity'>, operationHorizon?: number): HierarchyModel {
  const difficulty = DIFFICULTIES.find(level => level.id === model.difficulty)!;
  const movingJoints = model.joints.filter(joint => joint.type === 'revolute' || joint.type === 'prismatic').length;
  const depth = dependencyDepth(model.modules, model.joints);
  const horizon = operationHorizon ?? Math.min(difficulty.operationHorizon[1],
    Math.max(difficulty.operationHorizon[0], model.assemblyOrder.length + 2));
  return {
    ...model,
    complexity: {
      visibleParts: model.parts.length,
      modules: model.modules.length,
      joints: model.joints.length,
      movingJoints,
      dependencyDepth: depth,
      hiddenInterfaces: model.taskConfig.hiddenWorlds.length,
      coupledConstraints: difficulty.coupledConstraints,
      operationHorizon: horizon,
      complexityIndex: model.parts.length + model.modules.length * 7 + model.joints.length * 10
        + movingJoints * 8 + depth * 6 + difficulty.coupledConstraints * 10,
    },
  };
}

function finish(args: {
  builder: Builder;
  id: string;
  name: string;
  nameZh: string;
  domain: string;
  description: string;
  difficulty: Exclude<DifficultyId, 'D3'>;
  family: string;
  designNotes: string[];
  assemblyOrder: string[];
  serviceModule: string;
  functionalJoint: string;
  loadModule: string;
  faultJoint: string;
  seed: number;
  operationHorizon?: number;
}) {
  const { alternatives, requirements } = inventory(args.seed);
  const modules = args.builder.modules;
  const serviceParts = args.builder.parts.filter(part => part.moduleId === args.serviceModule);
  const serviceCenter: Vec3 = serviceParts.length
    ? serviceParts.reduce<Vec3>((sum, part) => [
      sum[0] + part.position[0] / serviceParts.length,
      sum[1] + part.position[1] / serviceParts.length,
      sum[2] + part.position[2] / serviceParts.length,
    ], [0, 0, 0])
    : [0, 2, 0];
  const model = withComplexity({
    id: args.id,
    name: args.name,
    nameZh: args.nameZh,
    domain: args.domain,
    description: args.description,
    originalDesign: true,
    difficulty: args.difficulty,
    family: args.family,
    designNotes: args.designNotes,
    modules,
    parts: args.builder.parts,
    joints: args.builder.joints,
    assemblyOrder: args.assemblyOrder,
    taskConfig: {
      serviceModule: args.serviceModule,
      accessPaths: [
        {
          id: `${args.id}-front`,
          label: 'Direct front service approach',
          start: [serviceCenter[0], serviceCenter[1], serviceCenter[2] + 12],
          end: [serviceCenter[0], serviceCenter[1], serviceCenter[2] + 1.4],
          halfExtents: [0.3, 0.3, 0.3],
        },
        {
          id: `${args.id}-top`,
          label: 'Vertical service approach',
          start: [serviceCenter[0], serviceCenter[1] + 12, serviceCenter[2]],
          end: [serviceCenter[0], serviceCenter[1] + 1.4, serviceCenter[2]],
          halfExtents: [0.35, 0.35, 0.35],
        },
        {
          id: `${args.id}-core`,
          label: 'Blocked approach through the structural core',
          start: [serviceCenter[0] - 12, serviceCenter[1], serviceCenter[2]],
          end: [serviceCenter[0] + 1.4, serviceCenter[1], serviceCenter[2]],
          halfExtents: [0.45, 0.45, 0.45],
        },
      ],
      functionalJoint: args.functionalJoint,
      functionalTarget: args.functionalJoint.includes('slide') ? 1.8 : 0.8,
      loadModule: args.loadModule,
      impulseCandidates: [5, 20, 60, 140].map(value => value * Number(args.difficulty.slice(1))),
      robustnessLimits: {
        maxTransientDisplacement: 1.4 / Number(args.difficulty.slice(1)),
        maxResidualDisplacement: 0.5 / Number(args.difficulty.slice(1)),
      },
      faultJoint: args.faultJoint,
      recoveryActions: [
        'isolate-load',
        `access-${args.serviceModule}`,
        `replace-${args.faultJoint}`,
        'reindex-mechanism',
        'proof-test',
      ],
      inventoryAlternatives: alternatives,
      inventoryRequirements: requirements,
      ...inspections(args.id, args.seed),
    },
  }, args.operationHorizon);
  assert.equal(new Set(model.assemblyOrder).size, modules.length, `${model.id}: assembly order`);
  assert.ok(modules.every(module => model.assemblyOrder.includes(module.id)), `${model.id}: module coverage`);
  assert.ok(model.joints.some(joint => ['revolute', 'prismatic'].includes(joint.type)), `${model.id}: moving joint`);
  return model;
}

function signalSwitchStand() {
  const b = new Builder();
  const base = b.module('base', 'Weighted signal base', 'foundation', true, 8);
  b.grid(base, 3, 3, [-1, 0.15, -1], C.dark);
  const post = b.module('post', 'Signal mast', 'support', false, 2);
  b.line(post, 6, [0, 0.75, 0], [0, 0.62, 0], C.gray, [0.65, 0.55, 0.65], 'beam');
  const arm = b.module('signal-arm', 'Pivoting signal arm', 'actuator', false, 1);
  b.line(arm, 5, [0.45, 4.1, 0], [0.8, 0, 0], C.red, [0.72, 0.35, 0.42], 'beam');
  const lamp = b.module('lamp', 'Inspection lamp', 'service-module', false, 0.5);
  b.part(lamp, 'cylinder', [0.9, 0.45, 0.9], [4.4, 4.1, 0], C.yellow, quatEuler(Math.PI / 2, 0, 0));
  b.part(lamp, 'panel', [0.25, 1.1, 1.1], [4.78, 4.1, 0], C.black);
  b.connect('post-foot', base, post, 'fixed', [0, 0.35, 0]);
  b.connect('arm-pivot', post, arm, 'revolute', [0, 4.1, 0], [0, 0, 1], [-0.8, 0.8]);
  b.connect('lamp-lock', arm, lamp, 'fixed', [4.4, 4.1, 0]);
  return finish({
    builder: b, id: 'signal-switch-stand', name: 'Signal Switch Stand', nameZh: '检修信号转臂',
    domain: 'local signaling', description: 'A weighted mast with one pivoting signal arm and removable inspection lamp.',
    difficulty: 'D1', family: 'single-interface actuator',
    designNotes: ['one exposed hinge', 'one removable lamp', 'short support chain'],
    assemblyOrder: [base, post, arm, lamp], serviceModule: lamp, functionalJoint: 'arm-pivot',
    loadModule: arm, faultJoint: 'lamp-lock', seed: 0,
  });
}

function maintenanceTrolley() {
  const b = new Builder();
  const chassis = b.module('chassis', 'Maintenance trolley chassis', 'foundation', true, 7);
  b.grid(chassis, 3, 3, [-1, 0.6, -1], C.blue);
  const front = b.module('front-axle', 'Front wheel axle', 'wheel-pair', false, 1);
  const rear = b.module('rear-axle', 'Rear wheel axle', 'wheel-pair', false, 1);
  for (const [module, z] of [[front, -1], [rear, 1]] as const) {
    for (const x of [-1.8, 1.8]) b.part(module, 'wheel', [1.0, 0.45, 1.0], [x, 0.45, z], C.black,
      quatEuler(Math.PI / 2, 0, 0));
    b.part(module, 'axle', [0.3, 3.5, 0.3], [0, 0.45, z], C.silver, quatEuler(0, 0, Math.PI / 2));
  }
  const tray = b.module('tool-tray', 'Removable tool tray', 'service-module', false, 1);
  b.grid(tray, 2, 2, [-0.5, 1.1, -0.5], C.orange);
  const handle = b.module('handle', 'Foldable pull handle', 'actuator', false, 0.7);
  b.part(handle, 'beam', [0.4, 3.2, 0.4], [0, 2.2, 1.9], C.gray);
  b.part(handle, 'beam', [2.4, 0.35, 0.35], [0, 3.75, 1.9], C.gray);
  b.connect('front-axle-pin', chassis, front, 'revolute', [0, 0.45, -1], [1, 0, 0]);
  b.connect('rear-axle-pin', chassis, rear, 'revolute', [0, 0.45, 1], [1, 0, 0]);
  b.connect('tray-clips', chassis, tray, 'fixed', [0, 1, 0]);
  b.connect('handle-pivot', chassis, handle, 'revolute', [0, 0.8, 1.9], [1, 0, 0], [0, 1.2]);
  return finish({
    builder: b, id: 'maintenance-trolley', name: 'Maintenance Trolley', nameZh: '维修工具小车',
    domain: 'shop-floor transport', description: 'A compact four-wheel trolley with a removable tray and folding handle.',
    difficulty: 'D1', family: 'small mobile assembly',
    designNotes: ['paired wheel modules', 'removable tray', 'folding handle'],
    assemblyOrder: [chassis, front, rear, tray, handle], serviceModule: tray, functionalJoint: 'handle-pivot',
    loadModule: tray, faultJoint: 'tray-clips', seed: 1,
  });
}

function safetyHatch() {
  const b = new Builder();
  const frame = b.module('frame', 'Safety hatch frame', 'foundation', true, 6);
  for (const x of [-2, -1, 0, 1, 2]) {
    b.part(frame, 'brick', [0.9, 0.55, 0.9], [x, 0.5, -1.6], C.yellow);
    b.part(frame, 'brick', [0.9, 0.55, 0.9], [x, 0.5, 1.6], C.yellow);
  }
  for (const z of [-0.6, 0.6]) {
    b.part(frame, 'brick', [0.9, 0.55, 0.9], [-2, 0.5, z], C.yellow);
    b.part(frame, 'brick', [0.9, 0.55, 0.9], [2, 0.5, z], C.yellow);
  }
  const lid = b.module('lid', 'Hinged safety lid', 'actuator', false, 2);
  b.grid(lid, 4, 3, [-1.5, 0.85, -1], C.red);
  const latch = b.module('latch', 'Sliding latch cartridge', 'service-module', false, 0.5);
  b.part(latch, 'beam', [2.0, 0.35, 0.45], [0, 1.2, 1.45], C.silver);
  b.part(latch, 'gear', [0.75, 0.3, 0.75], [1.25, 1.2, 1.45], C.black, quatEuler(Math.PI / 2, 0, 0));
  b.connect('lid-hinge', frame, lid, 'revolute', [-2, 0.8, 0], [0, 0, 1], [0, 1.35]);
  b.connect('latch-slide', lid, latch, 'prismatic', [0, 1.2, 1.45], [1, 0, 0], [-0.6, 0.6]);
  return finish({
    builder: b, id: 'hinged-safety-hatch', name: 'Hinged Safety Hatch', nameZh: '铰接安全舱盖',
    domain: 'protective access', description: 'A framed service hatch with a hinged lid and sliding lock cartridge.',
    difficulty: 'D1', family: 'two-stage closure',
    designNotes: ['clear frame boundary', 'hinge plus latch', 'single service interface'],
    assemblyOrder: [frame, lid, latch], serviceModule: latch, functionalJoint: 'lid-hinge',
    loadModule: lid, faultJoint: 'latch-slide', seed: 2,
  });
}

function valveStand() {
  const b = new Builder();
  const base = b.module('pipe-base', 'Pipe and pedestal', 'foundation', true, 8);
  b.grid(base, 3, 3, [-1, 0.15, -1], C.gray);
  b.line(base, 5, [0, 0.8, 0], [0, 0.7, 0], C.blue, [0.85, 0.62, 0.85], 'cylinder');
  const wheel = b.module('valve-wheel', 'Rotary valve wheel', 'actuator', false, 1);
  b.ring(wheel, 8, [0, 4.3, 0], 1.25, C.red, 'beam');
  b.part(wheel, 'axle', [0.35, 0.8, 0.35], [0, 4.3, 0], C.silver, quatEuler(Math.PI / 2, 0, 0));
  const indicator = b.module('indicator', 'Position indicator', 'service-module', false, 0.4);
  b.part(indicator, 'panel', [1.4, 0.2, 0.7], [0, 5.8, 0], C.white);
  b.part(indicator, 'beam', [0.2, 1.2, 0.2], [0, 5.2, 0], C.orange);
  b.connect('wheel-shaft', base, wheel, 'revolute', [0, 4.3, 0], [0, 0, 1], [-Math.PI, Math.PI]);
  b.connect('indicator-coupler', wheel, indicator, 'fixed', [0, 5.1, 0]);
  return finish({
    builder: b, id: 'valve-control-stand', name: 'Valve Control Stand', nameZh: '阀门控制台',
    domain: 'fluid control', description: 'A pedestal valve with a rotary handwheel and coupled position indicator.',
    difficulty: 'D1', family: 'rotary control',
    designNotes: ['single rotary degree of freedom', 'visible indicator', 'local replacement task'],
    assemblyOrder: [base, wheel, indicator], serviceModule: indicator, functionalJoint: 'wheel-shaft',
    loadModule: wheel, faultJoint: 'indicator-coupler', seed: 3,
  });
}

function warehouseSorter() {
  const b = new Builder();
  const floor = b.module('floor', 'Sorter foundation', 'foundation', true, 18);
  b.grid(floor, 6, 4, [-2.5, 0.15, -1.5], C.gray);
  const belt = b.module('belt', 'Transfer conveyor', 'transport', false, 5);
  b.line(belt, 12, [-4.4, 0.75, 0], [0.8, 0, 0], C.blue, [0.72, 0.2, 2.2], 'plate');
  const gate = b.module('diverter-gate', 'Pivoting diverter', 'actuator', false, 2);
  b.line(gate, 6, [0, 1.15, 0], [0.55, 0, 0], C.orange, [0.5, 0.5, 0.35], 'beam');
  const sensor = b.module('scanner', 'Overhead scanner', 'sensor', false, 1);
  for (const x of [-1.5, 1.5]) b.line(sensor, 4, [x, 0.8, -1.4], [0, 0.7, 0], C.dark);
  b.part(sensor, 'beam', [4, 0.35, 0.45], [0, 3.3, -1.4], C.dark);
  b.part(sensor, 'window', [1.2, 0.2, 0.8], [0, 3.0, -1.1], C.glass);
  const left = b.module('left-bin', 'Left destination bin', 'payload-zone', false, 3);
  const right = b.module('right-bin', 'Right destination bin', 'payload-zone', false, 3);
  for (const [module, z, color] of [[left, -3, C.green], [right, 3, C.yellow]] as const) {
    b.grid(module, 2, 2, [2.5, 0.7, z - 0.5], color);
  }
  b.connect('belt-drive', floor, belt, 'prismatic', [0, 0.7, 0], [1, 0, 0], [-0.5, 0.5]);
  b.connect('gate-pivot', belt, gate, 'revolute', [0, 1.15, 0], [0, 1, 0], [-0.7, 0.7]);
  b.connect('scanner-frame', floor, sensor, 'fixed', [0, 0.5, -1.4]);
  b.connect('left-bin-lock', floor, left, 'fixed', [3, 0.6, -3]);
  b.connect('right-bin-lock', floor, right, 'fixed', [3, 0.6, 3]);
  return finish({
    builder: b, id: 'warehouse-sorter', name: 'Warehouse Sorter', nameZh: '仓储分流机',
    domain: 'material sorting', description: 'A scanned conveyor with a pivoting diverter and two destination bins.',
    difficulty: 'D2', family: 'sensor-actuator assembly',
    designNotes: ['scanner-to-gate dependency', 'two destinations', 'local belt access'],
    assemblyOrder: [floor, belt, sensor, left, right, gate], serviceModule: gate, functionalJoint: 'gate-pivot',
    loadModule: belt, faultJoint: 'gate-pivot', seed: 4,
  });
}

function rescueWinchTower() {
  const b = new Builder();
  const base = b.module('base', 'Rescue tower footing', 'foundation', true, 24);
  b.grid(base, 4, 4, [-1.5, 0.15, -1.5], C.dark);
  const tower = b.module('tower', 'Braced rescue tower', 'support', false, 10);
  for (const x of [-2, 2]) for (const z of [-2, 2]) b.line(tower, 6, [x, 0.8, z], [0, 0.8, 0],
    C.yellow, [0.55, 0.7, 0.55], 'beam');
  for (const y of [2, 4, 6]) {
    b.part(tower, 'beam', [4.8, 0.35, 0.35], [0, y, -2], C.navy);
    b.part(tower, 'beam', [4.8, 0.35, 0.35], [0, y, 2], C.navy);
  }
  const boom = b.module('boom', 'Tilting rescue boom', 'actuator', false, 4);
  b.line(boom, 8, [0.4, 7.2, 0], [0.75, 0, 0], C.orange, [0.68, 0.45, 0.45], 'beam');
  const drum = b.module('winch-drum', 'Cable drum', 'service-module', false, 2);
  b.part(drum, 'cylinder', [1.6, 1.1, 1.6], [-1.2, 6.8, 0], C.red, quatEuler(0, 0, Math.PI / 2));
  b.part(drum, 'axle', [0.4, 2.2, 0.4], [-1.2, 6.8, 0], C.silver, quatEuler(0, 0, Math.PI / 2));
  const hook = b.module('hook', 'Lowering hook block', 'payload-interface', false, 1);
  b.part(hook, 'axle', [0.2, 5.0, 0.2], [5.2, 4.4, 0], C.dark);
  b.part(hook, 'gear', [1.0, 0.35, 1.0], [5.2, 1.9, 0], C.yellow);
  const cage = b.module('rescue-cage', 'Rescue cage', 'payload', false, 5);
  b.grid(cage, 3, 2, [4.2, 0.7, -0.5], C.red);
  b.line(cage, 2, [4.2, 1.3, -0.5], [2, 0, 0], C.white);
  b.line(cage, 2, [4.2, 1.3, 0.5], [2, 0, 0], C.white);
  b.connect('tower-feet', base, tower, 'fixed', [0, 0.4, 0]);
  b.connect('boom-hinge', tower, boom, 'revolute', [0, 7.2, 0], [0, 0, 1], [-0.2, 1.0]);
  b.connect('drum-shaft', tower, drum, 'revolute', [-1.2, 6.8, 0], [1, 0, 0], [-Math.PI, Math.PI]);
  b.connect('hook-slide', boom, hook, 'prismatic', [5.2, 4.4, 0], [0, 1, 0], [-3, 1]);
  b.connect('cage-latch', hook, cage, 'fixed', [5.2, 1.4, 0]);
  return finish({
    builder: b, id: 'rescue-winch-tower', name: 'Rescue Winch Tower', nameZh: '救援绞盘塔',
    domain: 'vertical rescue', description: 'A braced tower with tilting boom, winch drum, lowering hook, and rescue cage.',
    difficulty: 'D2', family: 'load-handling assembly',
    designNotes: ['three moving interfaces', 'suspended payload', 'braced support frame'],
    assemblyOrder: [base, tower, boom, drum, hook, cage], serviceModule: drum, functionalJoint: 'hook-slide',
    loadModule: cage, faultJoint: 'cage-latch', seed: 5,
  });
}

function inspectionSkiff() {
  const b = new Builder();
  const hull = b.module('hull', 'Catamaran inspection hull', 'foundation', true, 16);
  for (const z of [-1.7, 1.7]) {
    b.line(hull, 8, [-3.5, 0.45, z], [1, 0, 0], C.blue, [0.9, 0.5, 0.85], 'slope');
    b.line(hull, 4, [-1.5, 0.95, z], [1, 0, 0], C.white, [0.9, 0.35, 0.8], 'plate');
  }
  const cabin = b.module('cabin', 'Inspection cabin', 'control', false, 4);
  b.grid(cabin, 3, 2, [-1, 1.3, -0.5], C.white);
  for (const x of [-1, 0, 1]) b.part(cabin, 'window', [0.8, 0.8, 0.15], [x, 2.0, -0.85], C.glass);
  const rudder = b.module('rudder', 'Steering rudder', 'actuator', false, 1);
  b.part(rudder, 'panel', [0.25, 1.5, 1.0], [3.7, 0.2, 0], C.orange);
  const propeller = b.module('propeller', 'Inspection propeller', 'service-module', false, 1);
  b.part(propeller, 'axle', [0.25, 1.2, 0.25], [3.2, 0.5, 0], C.silver, quatEuler(0, 0, Math.PI / 2));
  b.ring(propeller, 5, [3.9, 0.5, 0], 0.75, C.yellow, 'beam');
  const mast = b.module('sensor-mast', 'Survey mast', 'sensor', false, 1);
  b.line(mast, 4, [0, 2.0, 0], [0, 0.65, 0], C.dark, [0.45, 0.55, 0.45], 'beam');
  b.part(mast, 'sphere', [1.0, 0.8, 1.0], [0, 4.4, 0], C.glass);
  b.connect('cabin-mount', hull, cabin, 'fixed', [0, 1.2, 0]);
  b.connect('rudder-pivot', hull, rudder, 'revolute', [3.7, 0.5, 0], [0, 1, 0], [-0.6, 0.6]);
  b.connect('propeller-shaft', hull, propeller, 'revolute', [3.2, 0.5, 0], [1, 0, 0], [-Math.PI, Math.PI]);
  b.connect('mast-turntable', cabin, mast, 'revolute', [0, 2.0, 0], [0, 1, 0], [-Math.PI, Math.PI]);
  return finish({
    builder: b, id: 'canal-inspection-skiff', name: 'Canal Inspection Skiff', nameZh: '运河巡检艇',
    domain: 'water inspection', description: 'A twin-hull survey craft with steering rudder, propeller, cabin, and sensor mast.',
    difficulty: 'D2', family: 'compact mobile mechanism',
    designNotes: ['three kinematic axes', 'paired hulls', 'rear service zone'],
    assemblyOrder: [hull, cabin, rudder, propeller, mast], serviceModule: propeller,
    functionalJoint: 'rudder-pivot', loadModule: cabin, faultJoint: 'propeller-shaft', seed: 6,
  });
}

function solarTracker() {
  const b = new Builder();
  const base = b.module('foundation', 'Tracker foundation', 'foundation', true, 18);
  b.grid(base, 4, 4, [-1.5, 0.15, -1.5], C.gray);
  const mast = b.module('mast', 'Rotating support mast', 'support', false, 5);
  for (const x of [-0.7, 0.7]) b.line(mast, 6, [x, 0.8, 0], [0, 0.75, 0], C.white,
    [0.55, 0.65, 0.55], 'beam');
  const yoke = b.module('yoke', 'Azimuth yoke', 'actuator', false, 3);
  b.part(yoke, 'beam', [5.2, 0.55, 0.55], [0, 5.2, 0], C.orange);
  b.part(yoke, 'gear', [1.2, 0.45, 1.2], [0, 4.8, 0], C.dark);
  const left = b.module('panel-left', 'Left solar wing', 'energy-surface', false, 3);
  const right = b.module('panel-right', 'Right solar wing', 'energy-surface', false, 3);
  for (const [module, offset] of [[left, -4.2], [right, 4.2]] as const) {
    for (let x = 0; x < 4; x++) for (let z = 0; z < 4; z++) {
      b.part(module, 'panel', [0.9, 0.18, 0.9], [offset + (x - 1.5), 5.2, z - 1.5], C.blue);
    }
  }
  const battery = b.module('battery', 'Tracker battery pack', 'service-module', false, 2);
  b.grid(battery, 2, 2, [-0.5, 0.8, 2.0], C.yellow);
  b.connect('mast-base', base, mast, 'revolute', [0, 0.5, 0], [0, 1, 0], [-Math.PI, Math.PI]);
  b.connect('yoke-tilt', mast, yoke, 'revolute', [0, 5.2, 0], [0, 0, 1], [-0.8, 0.8]);
  b.connect('left-panel-hinge', yoke, left, 'revolute', [-2.6, 5.2, 0], [1, 0, 0], [-0.3, 0.3]);
  b.connect('right-panel-hinge', yoke, right, 'revolute', [2.6, 5.2, 0], [1, 0, 0], [-0.3, 0.3]);
  b.connect('battery-lock', base, battery, 'fixed', [0, 0.8, 2.0]);
  return finish({
    builder: b, id: 'solar-tracker-array', name: 'Solar Tracker Array', nameZh: '双轴太阳能跟踪阵列',
    domain: 'renewable energy', description: 'A dual-axis tracker with two panel wings, azimuth mast, tilt yoke, and battery pack.',
    difficulty: 'D2', family: 'coupled orientation assembly',
    designNotes: ['dual-axis tracking', 'symmetric panel wings', 'service battery'],
    assemblyOrder: [base, mast, yoke, left, right, battery], serviceModule: battery,
    functionalJoint: 'yoke-tilt', loadModule: left, faultJoint: 'left-panel-hinge', seed: 7,
  });
}

function dockingYard() {
  const b = new Builder();
  const platform = b.module('platform', 'Orbital service platform', 'foundation', true, 50);
  b.grid(platform, 10, 8, [-4.5, 0.15, -3.5], C.gray);
  const hub = b.module('hub', 'Pressurized docking hub', 'central-control', false, 20);
  b.ring(hub, 24, [0, 2.1, 0], 3.4, C.white, 'slope');
  b.ring(hub, 16, [0, 3.1, 0], 2.6, C.blue, 'window');
  b.part(hub, 'cylinder', [4.2, 2.8, 4.2], [0, 2.2, 0], C.white);
  const airlock = b.module('airlock', 'Service airlock', 'service-module', false, 4);
  b.grid(airlock, 3, 3, [-1, 0.8, 4.2], C.orange);
  const westArm = b.module('dock-arm-west', 'West articulated docking arm', 'actuator', false, 6);
  const eastArm = b.module('dock-arm-east', 'East articulated docking arm', 'actuator', false, 6);
  for (const [module, sign] of [[westArm, -1], [eastArm, 1]] as const) {
    b.line(module, 10, [sign * 3.8, 2.3, 0], [sign * 0.75, 0.08, 0], C.yellow,
      [0.65, 0.45, 0.65], 'beam');
    b.part(module, 'gear', [1.4, 0.45, 1.4], [sign * 3.6, 2.3, 0], C.dark);
  }
  const solarWest = b.module('solar-west', 'West solar wing', 'power', false, 5);
  const solarEast = b.module('solar-east', 'East solar wing', 'power', false, 5);
  for (const [module, z] of [[solarWest, -6], [solarEast, 6]] as const) {
    for (let x = 0; x < 5; x++) for (let row = 0; row < 4; row++) {
      b.part(module, 'panel', [1.1, 0.16, 1.1], [x - 2, 3.2, z + row - 1.5], C.navy);
    }
  }
  const shuttle = b.module('shuttle', 'Docked transfer shuttle', 'payload', false, 9);
  b.line(shuttle, 12, [-2.75, 1.2, -7.5], [0.5, 0, 0], C.white, [0.46, 0.65, 1.4], 'slope');
  for (const x of [-2.5, 2.5]) b.part(shuttle, 'wheel', [1.1, 0.45, 1.1], [x, 1.0, -7.5], C.black);
  const craneBase = b.module('crane-base', 'Cargo crane pedestal', 'support', false, 8);
  b.line(craneBase, 8, [4.2, 0.8, 3.5], [0, 0.7, 0], C.orange, [0.65, 0.6, 0.65], 'beam');
  const craneBoom = b.module('crane-boom', 'Cargo crane boom', 'actuator', false, 4);
  b.line(craneBoom, 10, [4.2, 6.0, 3.5], [-0.6, 0.15, 0], C.orange, [0.55, 0.42, 0.55], 'beam');
  const cargo = b.module('cargo-pod', 'Transfer cargo pod', 'payload', false, 5);
  b.grid(cargo, 3, 3, [-1, 1.0, 7.0], C.red);
  b.connect('hub-clamp', platform, hub, 'fixed', [0, 0.5, 0]);
  b.connect('airlock-slide', hub, airlock, 'prismatic', [0, 1.0, 4.2], [0, 0, 1], [-0.4, 0.8]);
  b.connect('west-arm-pivot', hub, westArm, 'revolute', [-3.5, 2.3, 0], [0, 1, 0], [-1.2, 1.2]);
  b.connect('east-arm-pivot', hub, eastArm, 'revolute', [3.5, 2.3, 0], [0, 1, 0], [-1.2, 1.2]);
  b.connect('west-solar-hinge', hub, solarWest, 'revolute', [0, 3.2, -3.5], [1, 0, 0], [-0.5, 0.5]);
  b.connect('east-solar-hinge', hub, solarEast, 'revolute', [0, 3.2, 3.5], [1, 0, 0], [-0.5, 0.5]);
  b.connect('shuttle-dock', platform, shuttle, 'fixed', [0, 0.8, -7.5]);
  b.connect('crane-pedestal', platform, craneBase, 'revolute', [4.2, 0.5, 3.5], [0, 1, 0], [-Math.PI, Math.PI]);
  b.connect('crane-boom-hinge', craneBase, craneBoom, 'revolute', [4.2, 6.0, 3.5], [0, 0, 1], [-0.5, 1.0]);
  b.connect('cargo-lock', platform, cargo, 'fixed', [0, 0.8, 7.0]);
  return finish({
    builder: b, id: 'orbital-docking-yard', name: 'Orbital Docking Yard', nameZh: '轨道综合对接场',
    domain: 'orbital logistics', description: 'A coupled orbital yard with docking arms, solar wings, shuttle, crane, cargo pod, and service airlock.',
    difficulty: 'D4', family: 'distributed orbital system',
    designNotes: ['shared hub resources', 'two docking workcells', 'cross-zone crane and airlock dependencies'],
    assemblyOrder: [platform, hub, airlock, solarWest, solarEast, westArm, eastArm, shuttle, craneBase, craneBoom, cargo],
    serviceModule: airlock, functionalJoint: 'west-arm-pivot', loadModule: craneBoom,
    faultJoint: 'crane-boom-hinge', seed: 8, operationHorizon: 18,
  });
}

function floodResponseLock() {
  const b = new Builder();
  const basin = b.module('basin', 'Flood lock basin', 'foundation', true, 60);
  for (const z of [-5, 5]) b.grid(basin, 12, 2, [-5.5, 0.15, z], C.gray);
  for (const x of [-5.5, 5.5]) b.grid(basin, 2, 9, [x, 0.15, -4], C.gray);
  const gateNorth = b.module('gate-north', 'North sector gate', 'barrier', false, 14);
  const gateSouth = b.module('gate-south', 'South sector gate', 'barrier', false, 14);
  for (const [module, z] of [[gateNorth, -3], [gateSouth, 3]] as const) {
    for (let x = 0; x < 6; x++) for (let y = 0; y < 3; y++) {
      b.part(module, 'panel', [1.0, 0.8, 0.28], [x - 2.5, 0.8 + y * 0.8, z], C.blue);
    }
  }
  const tower = b.module('control-tower', 'Flood control tower', 'control', false, 12);
  for (const x of [-4.5, -2.5]) for (const z of [-4, -2]) b.line(tower, 5, [x, 0.8, z], [0, 0.75, 0], C.white);
  b.part(tower, 'window', [3.0, 1.3, 0.2], [-3.5, 4.6, -4.5], C.glass);
  const pumpA = b.module('pump-a', 'West emergency pump', 'service-module', false, 5);
  const pumpB = b.module('pump-b', 'East emergency pump', 'service-module', false, 5);
  for (const [module, x] of [[pumpA, -4], [pumpB, 4]] as const) {
    b.part(module, 'cylinder', [2.2, 1.8, 2.2], [x, 1.2, 0], C.orange);
    b.ring(module, 8, [x, 2.3, 0], 1.0, C.dark, 'gear');
  }
  const gantry = b.module('gantry', 'Emergency service gantry', 'support', false, 10);
  for (const x of [-5, 5]) b.line(gantry, 7, [x, 0.8, 0], [0, 0.75, 0], C.yellow);
  b.line(gantry, 12, [-5.5, 6.0, 0], [1, 0, 0], C.yellow, [0.9, 0.45, 0.5], 'beam');
  const trolley = b.module('gantry-trolley', 'Gantry maintenance trolley', 'actuator', false, 3);
  b.grid(trolley, 3, 2, [-1, 6.35, -0.5], C.red);
  const sensorA = b.module('sensor-north', 'North level sensor', 'sensor', false, 1);
  const sensorB = b.module('sensor-south', 'South level sensor', 'sensor', false, 1);
  for (const [module, z] of [[sensorA, -4], [sensorB, 4]] as const) {
    b.line(module, 3, [0, 0.8, z], [0, 0.7, 0], C.dark);
    b.part(module, 'sphere', [0.9, 0.7, 0.9], [0, 3.0, z], C.glass);
  }
  const barge = b.module('service-barge', 'Emergency service barge', 'payload', false, 8);
  b.grid(barge, 5, 3, [-2, 0.6, -0.8], C.green);
  b.connect('north-gate-hinge', basin, gateNorth, 'revolute', [-3, 1.0, -3], [0, 1, 0], [0, 1.2]);
  b.connect('south-gate-hinge', basin, gateSouth, 'revolute', [3, 1.0, 3], [0, 1, 0], [-1.2, 0]);
  b.connect('tower-foundation', basin, tower, 'fixed', [-3.5, 0.5, -3.5]);
  b.connect('pump-a-lock', basin, pumpA, 'fixed', [-4, 0.5, 0]);
  b.connect('pump-b-lock', basin, pumpB, 'fixed', [4, 0.5, 0]);
  b.connect('gantry-feet', basin, gantry, 'fixed', [0, 0.5, 0]);
  b.connect('gantry-slide', gantry, trolley, 'prismatic', [0, 6.2, 0], [1, 0, 0], [-4, 4]);
  b.connect('north-sensor-link', tower, sensorA, 'fixed', [0, 2, -4]);
  b.connect('south-sensor-link', tower, sensorB, 'fixed', [0, 2, 4]);
  b.connect('barge-mooring', basin, barge, 'spring', [0, 0.6, 0]);
  return finish({
    builder: b, id: 'flood-response-lock', name: 'Flood Response Lock', nameZh: '洪水应急船闸系统',
    domain: 'flood infrastructure', description: 'A twin-gate lock with redundant pumps, level sensors, service gantry, control tower, and emergency barge.',
    difficulty: 'D4', family: 'redundant civil system',
    designNotes: ['redundant pumps and sensors', 'coupled gates', 'shared maintenance gantry'],
    assemblyOrder: [basin, tower, gantry, trolley, pumpA, pumpB, sensorA, sensorB, gateNorth, gateSouth, barge],
    serviceModule: pumpA, functionalJoint: 'gantry-slide', loadModule: gateNorth,
    faultJoint: 'north-gate-hinge', seed: 9, operationHorizon: 20,
  });
}

function cargoTerminal() {
  const b = new Builder();
  const floor = b.module('floor', 'Automated terminal floor', 'foundation', true, 70);
  b.grid(floor, 12, 6, [-5.5, 0.15, -2.5], C.gray);
  const rackA = b.module('rack-a', 'West storage rack', 'storage', false, 14);
  const rackB = b.module('rack-b', 'East storage rack', 'storage', false, 14);
  for (const [module, x] of [[rackA, -4.5], [rackB, 4.5]] as const) {
    for (const z of [-2, 0, 2]) for (const y of [1, 2.5, 4]) {
      b.part(module, 'beam', [2.0, 0.35, 0.55], [x, y, z], C.navy);
      b.part(module, 'panel', [1.7, 0.7, 0.9], [x, y + 0.5, z], y === 2.5 ? C.orange : C.yellow);
    }
  }
  const conveyorA = b.module('conveyor-a', 'Inbound conveyor', 'transport', false, 6);
  const conveyorB = b.module('conveyor-b', 'Outbound conveyor', 'transport', false, 6);
  for (const [module, z, color] of [[conveyorA, -1.2, C.blue], [conveyorB, 1.2, C.green]] as const) {
    b.line(module, 18, [-4.25, 0.7, z], [0.5, 0, 0], color, [0.46, 0.2, 0.8], 'plate');
  }
  const gantry = b.module('gantry', 'Overhead transfer gantry', 'support', false, 14);
  for (const x of [-5, 5]) b.line(gantry, 8, [x, 0.8, 0], [0, 0.75, 0], C.yellow);
  b.line(gantry, 14, [-4.8, 6.3, 0], [0.75, 0, 0], C.yellow, [0.68, 0.45, 0.55], 'beam');
  const shuttle = b.module('shuttle', 'Gantry shuttle', 'actuator', false, 3);
  b.grid(shuttle, 3, 2, [-1, 6.6, -0.5], C.red);
  const lift = b.module('lift', 'Vertical transfer lift', 'service-module', false, 4);
  b.grid(lift, 3, 3, [-1, 1.0, -1], C.white);
  b.line(lift, 4, [-1.3, 1.6, -1.3], [0, 0.8, 0], C.dark);
  const robotA = b.module('robot-a', 'West sorting robot', 'actuator', false, 2);
  const robotB = b.module('robot-b', 'East sorting robot', 'actuator', false, 2);
  for (const [module, x] of [[robotA, -2.5], [robotB, 2.5]] as const) {
    b.part(module, 'gear', [1.2, 0.4, 1.2], [x, 1.0, 0], C.dark);
    b.line(module, 5, [x, 1.5, 0], [0, 0.7, 0], C.orange, [0.5, 0.6, 0.5], 'beam');
    b.part(module, 'beam', [2.0, 0.4, 0.4], [x + (x < 0 ? 0.8 : -0.8), 4.5, 0], C.orange);
  }
  const containers = ['container-red', 'container-blue', 'container-yellow'].map((id, index) => {
    const module = b.module(id, id.replaceAll('-', ' '), 'payload', false, 3);
    b.grid(module, 4, 2, [-1.5 + index * 3, 1.0, 3.5], [C.red, C.blue, C.yellow][index]);
    return module;
  });
  b.connect('rack-a-feet', floor, rackA, 'fixed', [-4.5, 0.5, 0]);
  b.connect('rack-b-feet', floor, rackB, 'fixed', [4.5, 0.5, 0]);
  b.connect('inbound-drive', floor, conveyorA, 'prismatic', [0, 0.7, -1.2], [1, 0, 0], [-0.4, 0.4]);
  b.connect('outbound-drive', floor, conveyorB, 'prismatic', [0, 0.7, 1.2], [1, 0, 0], [-0.4, 0.4]);
  b.connect('gantry-feet', floor, gantry, 'fixed', [0, 0.5, 0]);
  b.connect('shuttle-slide', gantry, shuttle, 'prismatic', [0, 6.4, 0], [1, 0, 0], [-4.5, 4.5]);
  b.connect('lift-slide', shuttle, lift, 'prismatic', [0, 4.5, 0], [0, 1, 0], [-4, 0]);
  b.connect('robot-a-base', floor, robotA, 'revolute', [-2.5, 1, 0], [0, 1, 0], [-Math.PI, Math.PI]);
  b.connect('robot-b-base', floor, robotB, 'revolute', [2.5, 1, 0], [0, 1, 0], [-Math.PI, Math.PI]);
  containers.forEach((module, index) => b.connect(`container-${index}-lock`, floor, module, 'fixed',
    [-1.5 + index * 3, 0.7, 3.5]));
  return finish({
    builder: b, id: 'automated-cargo-terminal', name: 'Automated Cargo Terminal', nameZh: '自动化货运终端',
    domain: 'warehouse orchestration', description: 'A dual-flow terminal with storage racks, conveyors, robots, gantry shuttle, lift, and distributed payloads.',
    difficulty: 'D4', family: 'multi-workcell logistics',
    designNotes: ['two material flows', 'shared gantry and lift', 'multiple robots and payloads'],
    assemblyOrder: [floor, rackA, rackB, conveyorA, conveyorB, gantry, shuttle, lift, robotA, robotB, ...containers],
    serviceModule: lift, functionalJoint: 'shuttle-slide', loadModule: lift,
    faultJoint: 'lift-slide', seed: 10, operationHorizon: 22,
  });
}

function sampleRefinery() {
  const b = new Builder();
  const pad = b.module('pad', 'Lunar refinery pad', 'foundation', true, 55);
  b.grid(pad, 10, 7, [-4.5, 0.15, -3], C.gray);
  const habitat = b.module('habitat', 'Pressurized control habitat', 'control', false, 16);
  b.ring(habitat, 20, [-3.2, 1.8, 0], 2.1, C.white, 'slope');
  b.part(habitat, 'cylinder', [3.0, 2.2, 3.0], [-3.2, 1.7, 0], C.white);
  for (const z of [-1.2, 0, 1.2]) b.part(habitat, 'window', [0.2, 0.8, 0.8], [-5.0, 2.0, z], C.glass);
  const crusher = b.module('crusher', 'Sample crusher', 'processor', false, 8);
  b.grid(crusher, 3, 3, [-1, 0.8, -3.0], C.orange);
  b.ring(crusher, 8, [0, 2.0, -3.0], 1.0, C.dark, 'gear');
  const conveyor = b.module('conveyor', 'Sealed transfer conveyor', 'transport', false, 5);
  b.line(conveyor, 18, [-3.5, 1.0, -1.8], [0.45, 0.02, 0.1], C.blue, [0.42, 0.2, 0.65], 'plate');
  const centrifuge = b.module('centrifuge', 'Rotary separator', 'actuator', false, 7);
  b.ring(centrifuge, 12, [3.0, 2.0, 0], 1.6, C.red, 'panel');
  b.part(centrifuge, 'cylinder', [2.0, 2.4, 2.0], [3.0, 2.0, 0], C.silver);
  const solarA = b.module('solar-a', 'North solar wing', 'power', false, 4);
  const solarB = b.module('solar-b', 'South solar wing', 'power', false, 4);
  for (const [module, z] of [[solarA, -5], [solarB, 5]] as const) {
    for (let x = 0; x < 6; x++) for (let row = 0; row < 3; row++) {
      b.part(module, 'panel', [0.9, 0.16, 0.9], [x - 2.5, 1.2, z + row - 1], C.navy);
    }
  }
  const tankA = b.module('tank-a', 'Feedstock tank', 'storage', false, 5);
  const tankB = b.module('tank-b', 'Product tank', 'storage', false, 5);
  for (const [module, x, color] of [[tankA, 5.0, C.yellow], [tankB, 6.7, C.green]] as const) {
    b.line(module, 5, [x, 0.8, 2.8], [0, 0.7, 0], color, [1.2, 0.65, 1.2], 'cylinder');
  }
  const rover = b.module('sample-rover', 'Sample transfer rover', 'payload', false, 5);
  b.grid(rover, 4, 3, [-1.5, 0.7, 3.0], C.white);
  for (const x of [-1.8, 1.8]) for (const z of [2.2, 3.8]) {
    b.part(rover, 'wheel', [0.9, 0.4, 0.9], [x, 0.45, z], C.black);
  }
  const arm = b.module('loading-arm', 'Refinery loading arm', 'service-module', false, 3);
  b.line(arm, 7, [1.5, 1.3, -1.5], [0, 0.7, 0], C.orange, [0.5, 0.6, 0.5], 'beam');
  b.part(arm, 'beam', [3.5, 0.45, 0.45], [2.8, 5.4, -1.5], C.orange, quatEuler(0, 0, -0.25));
  const silo = b.module('silo', 'Processed sample silo', 'storage', false, 5);
  b.line(silo, 6, [5.8, 0.8, -3], [0, 0.7, 0], C.magenta, [1.4, 0.65, 1.4], 'cylinder');
  b.connect('habitat-mount', pad, habitat, 'fixed', [-3.2, 0.5, 0]);
  b.connect('crusher-mount', pad, crusher, 'fixed', [0, 0.5, -3]);
  b.connect('conveyor-drive', crusher, conveyor, 'prismatic', [0, 1.0, -2], [1, 0, 0], [-0.4, 0.4]);
  b.connect('centrifuge-shaft', conveyor, centrifuge, 'revolute', [3, 2, 0], [0, 1, 0], [-Math.PI, Math.PI]);
  b.connect('solar-a-hinge', pad, solarA, 'revolute', [0, 1.2, -5], [1, 0, 0], [-0.5, 0.5]);
  b.connect('solar-b-hinge', pad, solarB, 'revolute', [0, 1.2, 5], [1, 0, 0], [-0.5, 0.5]);
  b.connect('tank-a-lock', pad, tankA, 'fixed', [5, 0.5, 2.8]);
  b.connect('tank-b-lock', pad, tankB, 'fixed', [6.7, 0.5, 2.8]);
  b.connect('rover-dock', pad, rover, 'fixed', [0, 0.5, 3]);
  b.connect('arm-shoulder', crusher, arm, 'revolute', [1.5, 1.3, -1.5], [0, 0, 1], [-0.2, 1.1]);
  b.connect('silo-lock', pad, silo, 'fixed', [5.8, 0.5, -3]);
  return finish({
    builder: b, id: 'lunar-sample-refinery', name: 'Lunar Sample Refinery', nameZh: '月面样品精炼站',
    domain: 'in-situ resource processing', description: 'A coupled lunar facility with habitat, crusher, conveyor, separator, tanks, solar wings, rover, loading arm, and silo.',
    difficulty: 'D4', family: 'resource-processing system',
    designNotes: ['material and power chains', 'mobile transfer interface', 'distributed storage and processing'],
    assemblyOrder: [pad, habitat, crusher, conveyor, centrifuge, solarA, solarB, tankA, tankB, rover, arm, silo],
    serviceModule: arm, functionalJoint: 'centrifuge-shaft', loadModule: centrifuge,
    faultJoint: 'conveyor-drive', seed: 11, operationHorizon: 24,
  });
}

function decorateMechanism(model: ReturnType<typeof mechanismModels>[number], index: number): HierarchyModel {
  return withComplexity({
    ...model,
    difficulty: 'D3',
    family: [
      'mobile service mechanism',
      'load-handling mechanism',
      'movable infrastructure',
      'scientific instrument',
      'aerial rescue vehicle',
      'modular research habitat',
    ][index],
    designNotes: [
      'retained from the frozen Mechanism-1 development suite',
      'full rigid-body, joint, shape-cast, and repair evidence',
      'eight additional Mechanism-1 tasks remain linked as a D3 extension',
    ],
  });
}

let cache: HierarchyModel[] | undefined;
export function hierarchyModels(): HierarchyModel[] {
  if (cache) return cache;
  const models = [
    signalSwitchStand(),
    maintenanceTrolley(),
    safetyHatch(),
    valveStand(),
    warehouseSorter(),
    rescueWinchTower(),
    inspectionSkiff(),
    solarTracker(),
    ...mechanismModels().map(decorateMechanism),
    dockingYard(),
    floodResponseLock(),
    cargoTerminal(),
    sampleRefinery(),
  ];
  assert.equal(models.length, 18);
  assert.equal(new Set(models.map(model => model.id)).size, models.length);
  cache = models;
  return models;
}
