import assert from 'node:assert/strict';
import {
  IDENTITY_QUAT,
  type MechanismJoint,
  type MechanismModel,
  type MechanismModule,
  type MechanismPart,
  type Quat,
  type ShapeKind,
  type Vec3,
} from './types';

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
  tan: '#c9aa7a',
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

  module(id: string, name: string, role: string, position: Vec3, anchored = false, mass = 1) {
    this.modules.push({ id, name, role, anchored, mass, position, rotation: IDENTITY_QUAT });
    return id;
  }

  part(moduleId: string, shape: ShapeKind, size: Vec3, position: Vec3, color: string, rotation = IDENTITY_QUAT) {
    this.parts.push({ id: `v${String(++this.serial).padStart(4, '0')}`, moduleId, shape,
      size, position, rotation, color });
  }

  brick(moduleId: string, x: number, y: number, z: number, color: string,
    size: Vec3 = [1.9, .58, .9], rotation = IDENTITY_QUAT) {
    this.part(moduleId, 'brick', size, [x, y, z], color, rotation);
  }

  row(moduleId: string, count: number, start: Vec3, step: Vec3, color: string,
    size: Vec3 = [1.9, .58, .9], shape: ShapeKind = 'brick') {
    for (let i = 0; i < count; i++) this.part(moduleId, shape, size,
      [start[0] + step[0] * i, start[1] + step[1] * i, start[2] + step[2] * i], color, IDENTITY_QUAT);
  }

  joint(joint: MechanismJoint) { this.joints.push(joint); }
}

const genericInventory = (variant: number) => [
  { id: 'carbon-beam', label: 'One long carbon beam', pieces: 1,
    cost: variant === 3 ? 5 : 7, mass: variant === 3 ? 1.5 : 1.8,
    stiffness: variant === 3 ? 12 : 9, jointMode: 'fixed' as const },
  { id: 'twin-truss', label: 'Two interlocked short trusses', pieces: 2,
    cost: variant === 4 ? 4 : 6, mass: [1, 4].includes(variant) ? 1.5 : 2.2,
    stiffness: variant === 4 ? 12 : 11, jointMode: 'fixed' as const },
  { id: 'tension-cable', label: 'One tension cable', pieces: 1, cost: 3, mass: .6,
    stiffness: variant === 5 ? 12 : variant === 2 ? 10 : 5, jointMode: 'spring' as const },
  { id: 'decorative-panel', label: 'One fairing panel', pieces: 1, cost: 2, mass: .8, stiffness: 1, jointMode: 'none' as const },
];

function genericInspection(prefix: string, variant: number) {
  const costs = [1 + variant % 3, 1 + (variant + 1) % 3, 1 + (variant + 2) % 3];
  return {
    hiddenWorlds: ['nominal', 'reversed', 'missing-brace', 'jammed'],
    inspectionQueries: [
      { id: `${prefix}-marker`, label: 'Inspect the joint orientation marker', cost: costs[0],
        returns: { nominal: 'forward', reversed: 'reverse', 'missing-brace': 'forward', jammed: 'forward' } },
      { id: `${prefix}-brace`, label: 'Inspect the concealed brace bay', cost: costs[1],
        returns: { nominal: 'present', reversed: 'present', 'missing-brace': 'absent', jammed: 'present' } },
      { id: `${prefix}-probe`, label: 'Apply a low-force actuation probe', cost: costs[2],
        returns: { nominal: 'moves-positive', reversed: 'moves-negative', 'missing-brace': 'moves-positive', jammed: 'no-motion' } },
    ],
  };
}

function rover(): MechanismModel {
  const b = new Builder();
  const base = b.module('chassis', 'Pressurized rover chassis', 'primary-frame', [0, 1.2, 0], true, 18);
  for (const y of [0, .62]) for (const z of [-3.6, -1.8, 0, 1.8, 3.6])
    for (const x of [-2, 0, 2]) b.brick(base, x, y, z, y ? C.white : C.dark);
  for (const z of [-2.7, -.9, .9, 2.7]) {
    b.part(base, 'window', [1.8, 1.1, .18], [-2.95, 1.65, z], C.glass, quatEuler(0, 0, Math.PI / 2));
    b.part(base, 'window', [1.8, 1.1, .18], [2.95, 1.65, z], C.glass, quatEuler(0, 0, Math.PI / 2));
  }
  b.part(base, 'slope', [5.7, 1.2, 2.2], [0, 1.65, -3.55], C.white, quatEuler(-.18, 0, 0));
  b.part(base, 'panel', [5.7, .18, 2.8], [0, 2.75, 1.2], C.white);
  b.row(base, 6, [-2.5, 2.95, 2.7], [1, 0, 0], C.orange, [.9, .18, 1.6], 'plate');
  const battery = b.module('battery', 'Rear battery cartridge', 'service-module', [0, 1.4, 3.5], false, 2);
  b.part(battery, 'panel', [3.4, 1.1, 1.2], [0, 0, 0], C.yellow);
  b.part(battery, 'gear', [.7, .35, .7], [-1.15, 0, .7], C.dark, quatEuler(Math.PI / 2, 0, 0));
  b.joint({ id: 'battery-lock', name: 'Battery locking pins', type: 'fixed', parent: base, child: battery,
    anchorParent: [0, .2, 3.5], anchorChild: [0, 0, 0] });

  const wheelPositions: Array<[string, number, number]> = [
    ['wheel-lf', -3.15, -3], ['wheel-lm', -3.15, 0], ['wheel-lr', -3.15, 3],
    ['wheel-rf', 3.15, -3], ['wheel-rm', 3.15, 0], ['wheel-rr', 3.15, 3],
  ];
  for (const [id, x, z] of wheelPositions) {
    const module = b.module(id, id.replaceAll('-', ' '), 'wheel', [x, 1, z], false, 1.2);
    b.part(module, 'wheel', [1.25, .7, 1.25], [0, 0, 0], C.black, quatEuler(Math.PI / 2, 0, 0));
    b.part(module, 'axle', [.36, 1.1, .36], [0, 0, 0], C.silver, quatEuler(Math.PI / 2, 0, 0));
    b.joint({ id: `${id}-axle`, name: `${id} axle`, type: 'revolute', parent: base, child: module,
      anchorParent: [x, -.2, z], anchorChild: [0, 0, 0], axis: [0, 0, 1] });
  }
  const arm = b.module('sample-arm', 'Articulated sample arm', 'actuator', [2.3, 3.0, -1.5], false, 2.5);
  b.part(arm, 'gear', [.8, .35, .8], [0, 0, 0], C.gray, quatEuler(Math.PI / 2, 0, 0));
  b.row(arm, 5, [0, .65, 0], [0, .75, 0], C.orange, [.65, .68, .65], 'beam');
  b.part(arm, 'beam', [2.8, .5, .5], [1.15, 3.8, 0], C.orange, quatEuler(0, 0, -.35));
  b.part(arm, 'gear', [.65, .3, .65], [2.5, 3.35, 0], C.dark, quatEuler(Math.PI / 2, 0, 0));
  b.joint({ id: 'arm-shoulder', name: 'Arm shoulder hinge', type: 'revolute', parent: base, child: arm,
    anchorParent: [2.3, 1.8, -1.5], anchorChild: [0, 0, 0], axis: [0, 0, 1], limits: [-.2, 1.2] });
  const mast = b.module('sensor-mast', 'Panoramic sensor mast', 'sensor', [-1.3, 3.2, -.8], false, 1.4);
  b.row(mast, 4, [0, .35, 0], [0, .62, 0], C.gray, [.55, .55, .55], 'beam');
  b.part(mast, 'sphere', [1.3, 1.0, 1.3], [0, 2.9, 0], C.glass);
  b.joint({ id: 'mast-turntable', name: 'Mast turntable', type: 'revolute', parent: base, child: mast,
    anchorParent: [-1.3, 2, -.8], anchorChild: [0, 0, 0], axis: [0, 1, 0], limits: [-Math.PI, Math.PI] });
  return {
    id: 'orbital-service-rover', name: 'Orbital Service Rover', nameZh: '轨道检修车',
    domain: 'planetary maintenance',
    description: 'A six-wheel pressurized rover with service battery, panoramic mast and articulated sampling arm.',
    originalDesign: true, modules: b.modules, parts: b.parts, joints: b.joints,
    assemblyOrder: ['chassis', 'battery', ...wheelPositions.map(x => x[0]), 'sensor-mast', 'sample-arm'],
    taskConfig: {
      serviceModule: 'battery',
      accessPaths: [
        { id: 'rear-slide', label: 'Reach the battery latch through the rear service hatch', start: [0, 1.5, 8], end: [0, 1.5, 4.5], halfExtents: [.35, .35, .35] },
        { id: 'roof-drop', label: 'Reach the latch vertically through the cabin roof', start: [0, 8, 3.5], end: [0, 2.2, 3.5], halfExtents: [.35, .35, .35] },
        { id: 'side-insert', label: 'Reach the latch through the left wheel bay', start: [-7, 1.5, 3.5], end: [-1.9, 1.5, 3.5], halfExtents: [.35, .35, .35] },
      ],
      functionalJoint: 'arm-shoulder', functionalTarget: .85,
      loadModule: 'sample-arm', impulseCandidates: [5, 20, 60, 120],
      robustnessLimits: { maxTransientDisplacement: 1.2, maxResidualDisplacement: .45 },
      faultJoint: 'arm-shoulder', recoveryActions: ['stow-arm', 'support-boom', 'replace-shoulder-pin', 'reindex-arm', 'release-boom'],
      inventoryAlternatives: genericInventory(0), inventoryRequirements: { maxCost: 6, maxPieces: 2, minStiffness: 8 },
      ...genericInspection('rover', 0),
    },
  };
}

function crane(): MechanismModel {
  const b = new Builder();
  const base = b.module('dock-base', 'Harbor rail foundation', 'foundation', [0, .5, 0], true, 24);
  for (const z of [-4, -2, 0, 2, 4]) for (const x of [-5, -3, -1, 1, 3, 5])
    b.part(base, 'plate', [1.9, .2, 1.8], [x, 0, z], z % 4 ? C.gray : C.blue);
  b.row(base, 12, [-5.5, .35, -3.6], [1, 0, 0], C.silver, [.9, .22, .25], 'beam');
  b.row(base, 12, [-5.5, .35, 3.6], [1, 0, 0], C.silver, [.9, .22, .25], 'beam');
  const gantry = b.module('gantry', 'Twin-tower crane gantry', 'load-frame', [0, .7, 0], false, 14);
  for (const x of [-4.2, 4.2]) for (const y of [1, 2.1, 3.2, 4.3, 5.4, 6.5])
    for (const z of [-2.4, 2.4]) b.part(gantry, 'beam', [.75, .9, .75], [x, y, z], C.yellow);
  for (const x of [-4.2, 4.2]) for (const y of [2, 4.2, 6.4])
    b.part(gantry, 'beam', [.5, 2.8, 5.4], [x, y, 0], C.dark, quatEuler(0, 0, y % 4 ? .55 : -.55));
  b.row(gantry, 12, [-5.5, 7.25, -2.2], [1, 0, 0], C.yellow, [.9, .5, .65], 'beam');
  b.row(gantry, 12, [-5.5, 7.25, 2.2], [1, 0, 0], C.yellow, [.9, .5, .65], 'beam');
  b.part(gantry, 'window', [2.5, 1.8, 1.8], [4.1, 5.8, -3.2], C.glass);
  b.joint({ id: 'gantry-foot-a', name: 'Left foundation clamp', type: 'fixed', parent: base, child: gantry,
    anchorParent: [-4.2, .2, 0], anchorChild: [-4.2, 0, 0] });
  b.joint({ id: 'gantry-foot-b', name: 'Right foundation clamp', type: 'fixed', parent: base, child: gantry,
    anchorParent: [4.2, .2, 0], anchorChild: [4.2, 0, 0] });
  const trolley = b.module('trolley', 'Traversing trolley', 'actuator', [0, 8.1, 0], false, 3);
  b.part(trolley, 'panel', [2.2, .7, 3.4], [0, 0, 0], C.orange);
  for (const z of [-1.35, 1.35]) for (const x of [-.75, .75])
    b.part(trolley, 'wheel', [.55, .28, .55], [x, -.45, z], C.black, quatEuler(Math.PI / 2, 0, 0));
  b.joint({ id: 'trolley-rail', name: 'Trolley rail', type: 'prismatic', parent: gantry, child: trolley,
    anchorParent: [0, 7.4, 0], anchorChild: [0, 0, 0], axis: [1, 0, 0], limits: [-3.8, 3.8] });
  const hook = b.module('hoist', 'Hoist and hook block', 'service-module', [0, 4.8, 0], false, 2);
  b.part(hook, 'axle', [.25, 3.1, .25], [0, 1.6, 0], C.dark);
  b.part(hook, 'gear', [1.1, .4, 1.1], [0, 0, 0], C.yellow, quatEuler(Math.PI / 2, 0, 0));
  b.part(hook, 'beam', [1.3, .35, .35], [0, -.7, 0], C.dark, quatEuler(0, 0, .8));
  b.joint({ id: 'hoist-slide', name: 'Vertical hoist carriage', type: 'prismatic', parent: trolley, child: hook,
    anchorParent: [0, 0, 0], anchorChild: [0, 3.3, 0], axis: [0, 1, 0], limits: [-4.2, 0] });
  const load = b.module('container', 'Intermodal container', 'payload', [0, 2.15, 0], false, 7);
  for (const z of [-1.4, 0, 1.4]) for (const x of [-1.8, 0, 1.8])
    b.part(load, 'panel', [1.7, 1.4, 1.25], [x, 0, z], C.red);
  b.joint({ id: 'hook-latch', name: 'Container hook latch', type: 'fixed', parent: hook, child: load,
    anchorParent: [0, -1.1, 0], anchorChild: [0, 1.55, 0] });
  return {
    id: 'harbor-container-crane', name: 'Harbor Container Crane', nameZh: '港口集装箱起重机',
    domain: 'load handling',
    description: 'A twin-tower rail crane with traversing trolley, vertical hoist, control cabin and container payload.',
    originalDesign: true, modules: b.modules, parts: b.parts, joints: b.joints,
    assemblyOrder: ['dock-base', 'gantry', 'trolley', 'hoist', 'container'],
    taskConfig: {
      serviceModule: 'trolley',
      accessPaths: [
        { id: 'rail-entry', label: 'Reach the trolley drive from the open rail end', start: [-9, 8.8, 0], end: [-1.5, 8.8, 0], halfExtents: [.4, .3, .4] },
        { id: 'tower-gap', label: 'Lower a service probe through the tower gap', start: [0, 13, 0], end: [0, 8.8, 0], halfExtents: [.4, .3, .4] },
        { id: 'cabin-side', label: 'Reach the trolley through the occupied cabin side', start: [8, 5.8, -3.2], end: [3.2, 5.8, -3.2], halfExtents: [.4, .4, .4] },
      ],
      functionalJoint: 'trolley-rail', functionalTarget: 2.8,
      loadModule: 'container', impulseCandidates: [10, 40, 100, 200],
      robustnessLimits: { maxTransientDisplacement: 1.2, maxResidualDisplacement: .45 },
      faultJoint: 'hook-latch', recoveryActions: ['lower-hoist', 'stabilize-container', 'replace-hook-latch', 'tension-hoist', 'raise-test-load'],
      inventoryAlternatives: genericInventory(1), inventoryRequirements: { maxCost: 7, maxPieces: 1, minStiffness: 8 },
      ...genericInspection('crane', 1),
    },
  };
}

function drawbridge(): MechanismModel {
  const b = new Builder();
  const base = b.module('quay', 'Canal quay and foundations', 'foundation', [0, .4, 0], true, 28);
  for (const x of [-6, -4, -2, 0, 2, 4, 6]) for (const z of [-4.5, -3, 3, 4.5])
    b.part(base, 'plate', [1.9, .25, 1.4], [x, 0, z], z < 0 ? C.tan : C.gray);
  for (const x of [-6, -4, -2, 2, 4, 6]) for (const z of [-1.5, 0, 1.5])
    b.part(base, 'plate', [1.9, .12, 1.4], [x, -.15, z], C.blue);
  for (const side of [-1, 1]) {
    const tower = b.module(`tower-${side < 0 ? 'left' : 'right'}`, `${side < 0 ? 'West' : 'East'} bridge tower`,
      'tower', [side * 5, .7, 0], false, 10);
    for (const y of [.4, 1.3, 2.2, 3.1, 4, 4.9]) for (const z of [-2.2, 2.2])
      for (const x of [-1.2, 1.2]) b.part(tower, 'brick', [1.1, .78, 1.1], [x, y, z], C.white);
    for (const z of [-2.2, 2.2]) b.part(tower, 'arch', [3.5, 1.5, 1.0], [0, 2.2, z], C.gray);
    b.part(tower, 'slope', [3.4, 1.2, 5.4], [0, 5.8, 0], C.navy);
    b.joint({ id: `tower-${side}-foot-a`, name: 'Tower footing A', type: 'fixed', parent: base, child: tower,
      anchorParent: [side * 5, .2, -2], anchorChild: [0, 0, -2] });
    b.joint({ id: `tower-${side}-foot-b`, name: 'Tower footing B', type: 'fixed', parent: base, child: tower,
      anchorParent: [side * 5, .2, 2], anchorChild: [0, 0, 2] });
  }
  for (const side of [-1, 1]) {
    const id = side < 0 ? 'west-deck' : 'east-deck';
    const deck = b.module(id, `${side < 0 ? 'West' : 'East'} bascule deck`, 'moving-deck', [side * 5.2, 1.2, 0], false, 2);
    const centers = side < 0 ? [.85, 2.55, 4.25] : [-.85, -2.55, -4.25];
    for (const x of centers) for (const z of [-1.5, 0, 1.5])
      b.part(deck, 'plate', [1.7, .35, 1.35], [x, 0, z], C.gray);
    for (const z of [-2.2, 2.2]) b.row(deck, 5, [side < 0 ? .45 : -.45, .55, z],
      [side < 0 ? 1.05 : -1.05, 0, 0], C.yellow, [.9, .35, .25], 'beam');
    b.part(deck, 'gear', [1.4, .45, 1.4], [side < 0 ? .4 : -.4, -.3, 0], C.orange, quatEuler(Math.PI / 2, 0, 0));
    const parent = side < 0 ? 'tower-left' : 'tower-right';
    b.joint({ id: `${id}-hinge`, name: `${id} hinge`, type: 'revolute', parent, child: deck,
      anchorParent: [side * .2, .5, 0], anchorChild: [0, 0, 0], axis: [0, 0, 1], limits: [0, 1.25] });
  }
  const gear = b.module('drive-cartridge', 'Bascule drive cartridge', 'service-module', [-5, 2.2, -2.9], false, 2);
  b.part(gear, 'gear', [1.6, .55, 1.6], [0, 0, 0], C.orange, quatEuler(Math.PI / 2, 0, 0));
  b.part(gear, 'axle', [.35, 1.6, .35], [0, 0, 0], C.silver, quatEuler(Math.PI / 2, 0, 0));
  b.joint({ id: 'drive-lock', name: 'Drive cartridge lock', type: 'fixed', parent: 'tower-left', child: gear,
    anchorParent: [0, 1.5, -2.9], anchorChild: [0, 0, 0] });
  return {
    id: 'bascule-canal-gate', name: 'Bascule Canal Gate', nameZh: '双叶运河开启桥',
    domain: 'movable infrastructure',
    description: 'A twin-tower canal crossing with two hinged decks, drive cartridge, counterweight gears and service galleries.',
    originalDesign: true, modules: b.modules, parts: b.parts, joints: b.joints,
    assemblyOrder: ['quay', 'tower-left', 'tower-right', 'drive-cartridge', 'west-deck', 'east-deck'],
    taskConfig: {
      serviceModule: 'drive-cartridge',
      accessPaths: [
        { id: 'gallery-entry', label: 'Reach the drive lock along the west service gallery', start: [-5, 2.2, -8], end: [-5, 2.2, -3.8], halfExtents: [.35, .35, .35] },
        { id: 'tower-drop', label: 'Lower a tool through the tower roof', start: [-5, 10, -2.9], end: [-5, 3.3, -2.9], halfExtents: [.35, .35, .35] },
        { id: 'deck-side', label: 'Reach the drive through the closed deck side', start: [0, 2.2, -7], end: [-4.1, 2.2, -3.2], halfExtents: [.35, .35, .35] },
      ],
      functionalJoint: 'west-deck-hinge', functionalTarget: .95,
      loadModule: 'west-deck', impulseCandidates: [20, 100, 300, 600],
      robustnessLimits: { maxTransientDisplacement: .2, maxResidualDisplacement: .1 },
      faultJoint: 'drive-lock', recoveryActions: ['lock-decks-open', 'open-gallery', 'remove-damaged-drive', 'install-drive-cartridge', 'calibrate-hinge', 'close-gallery'],
      inventoryAlternatives: genericInventory(2), inventoryRequirements: { maxCost: 4, maxPieces: 1, minStiffness: 10 },
      ...genericInspection('bridge', 2),
    },
  };
}

function observatory(): MechanismModel {
  const b = new Builder();
  const base = b.module('foundation', 'Terraced observatory foundation', 'foundation', [0, .4, 0], true, 20);
  for (let ring = 0; ring < 4; ring++) {
    const r = 4.8 - ring * .8;
    for (let i = 0; i < 16; i++) {
      const a = i * Math.PI / 8;
      b.part(base, ring ? 'brick' : 'plate', [1.2, .48, .85], [Math.cos(a) * r, ring * .5, Math.sin(a) * r],
        ring % 2 ? C.white : C.gray, quatEuler(0, -a, 0));
    }
  }
  b.part(base, 'panel', [4.5, 1.2, 2.5], [0, 1.4, 3.6], C.dark);
  const dome = b.module('dome', 'Rotating segmented dome', 'rotating-enclosure', [0, 3.1, 0], false, 9);
  for (let i = 0; i < 20; i++) {
    const a = i * Math.PI / 10;
    b.part(dome, 'slope', [1.35, 1.7, 1.2], [Math.cos(a) * 3.25, .65, Math.sin(a) * 3.25],
      i % 5 === 0 ? C.blue : C.white, quatEuler(.12, -a, 0));
  }
  b.part(dome, 'beam', [1, .5, 6.8], [0, 1.8, 0], C.dark);
  b.joint({ id: 'dome-ring', name: 'Azimuth rotation ring', type: 'revolute', parent: base, child: dome,
    anchorParent: [0, 2.7, 0], anchorChild: [0, 0, 0], axis: [0, 1, 0], limits: [-Math.PI, Math.PI] });
  const telescope = b.module('telescope', 'Elevation telescope', 'instrument', [0, 4.8, 0], false, 4);
  b.part(telescope, 'cylinder', [1.2, 5.2, 1.2], [0, 0, 1.8], C.white, quatEuler(Math.PI / 2, 0, 0));
  b.part(telescope, 'cylinder', [1.65, .8, 1.65], [0, 0, 4.4], C.blue, quatEuler(Math.PI / 2, 0, 0));
  b.part(telescope, 'gear', [1.1, .45, 1.1], [0, 0, -.8], C.orange, quatEuler(Math.PI / 2, 0, 0));
  b.part(telescope, 'beam', [3.6, .45, .45], [0, -1.2, 0], C.dark);
  b.joint({ id: 'elevation-axis', name: 'Telescope elevation axis', type: 'revolute', parent: dome, child: telescope,
    anchorParent: [0, 1.7, 0], anchorChild: [0, 0, 0], axis: [1, 0, 0], limits: [-.15, 1.25] });
  const camera = b.module('camera-pack', 'Cryogenic camera pack', 'service-module', [0, 4.8, 4.9], false, 1.5);
  b.part(camera, 'cylinder', [1.15, 1.1, 1.15], [0, 0, 0], C.silver, quatEuler(Math.PI / 2, 0, 0));
  b.part(camera, 'panel', [1.8, 1.3, .4], [0, 0, .75], C.glass);
  b.joint({ id: 'camera-bayonet', name: 'Camera bayonet', type: 'fixed', parent: telescope, child: camera,
    anchorParent: [0, 0, 4.9], anchorChild: [0, 0, 0] });
  return {
    id: 'adaptive-radio-observatory', name: 'Adaptive Radio Observatory', nameZh: '自适应射电观测站',
    domain: 'scientific instrumentation',
    description: 'A terraced observatory with rotating segmented dome, elevation telescope and removable cryogenic camera.',
    originalDesign: true, modules: b.modules, parts: b.parts, joints: b.joints,
    assemblyOrder: ['foundation', 'dome', 'telescope', 'camera-pack'],
    taskConfig: {
      serviceModule: 'camera-pack',
      accessPaths: [
        { id: 'optical-axis', label: 'Reach the camera bayonet along the optical axis', start: [0, 4.8, 10], end: [0, 4.8, 5.7], halfExtents: [.3, .3, .3] },
        { id: 'dome-slot', label: 'Lower a service probe through the dome slit', start: [0, 11, 4.9], end: [0, 6.2, 4.9], halfExtents: [.3, .3, .3] },
        { id: 'service-door', label: 'Reach the bayonet through the occupied lower service room', start: [0, 2, 8], end: [0, 2, 0], halfExtents: [.3, .3, .3] },
      ],
      functionalJoint: 'elevation-axis', functionalTarget: .7,
      loadModule: 'telescope', impulseCandidates: [20, 100, 500, 2000],
      robustnessLimits: { maxTransientDisplacement: .5, maxResidualDisplacement: .2 },
      faultJoint: 'camera-bayonet', recoveryActions: ['park-telescope', 'open-dome-slit', 'remove-camera', 'clean-bayonet', 'install-camera', 'recalibrate-optics'],
      inventoryAlternatives: genericInventory(3), inventoryRequirements: { maxCost: 5, maxPieces: 1, minStiffness: 11 },
      ...genericInspection('observatory', 3),
    },
  };
}

function tiltrotor(): MechanismModel {
  const b = new Builder();
  const body = b.module('fuselage', 'Firefighting tiltrotor fuselage', 'airframe', [0, 3.2, 0], true, 22);
  for (const z of [-3.5, -2.3, -1.1, .1, 1.3, 2.5]) {
    for (const x of [-1, 1]) b.part(body, 'brick', [1.8, .58, 1.1], [x, 0, z], z < -2 ? C.red : C.white);
    if (z < 1.5) b.part(body, 'slope', [3.7, .7, 1], [0, .75, z], C.red, quatEuler(0, 0, z < -2 ? -.15 : .05));
  }
  b.part(body, 'window', [3.5, 1.2, .3], [0, 1.2, -3.9], C.glass, quatEuler(.2, 0, 0));
  b.part(body, 'panel', [8.8, .38, 1.6], [0, .3, -.2], C.red);
  b.row(body, 6, [-2.5, .2, 3.4], [1, 0, .5], C.white, [.8, .35, .8], 'beam');
  b.part(body, 'panel', [2.8, .3, 4.2], [0, .2, 4.7], C.red);
  for (const side of [-1, 1]) {
    const nacelle = b.module(`nacelle-${side < 0 ? 'left' : 'right'}`, `${side < 0 ? 'Left' : 'Right'} tilting nacelle`,
      'actuator', [side * 4.8, 3.6, -.2], false, 3.2);
    b.part(nacelle, 'cylinder', [1.4, 2.1, 1.4], [0, 0, 0], C.dark, quatEuler(0, 0, Math.PI / 2));
    b.part(nacelle, 'gear', [1.55, .5, 1.55], [0, 0, 0], C.orange, quatEuler(0, 0, Math.PI / 2));
    b.joint({ id: `${nacelle}-tilt`, name: `${nacelle} tilt hinge`, type: 'revolute', parent: body, child: nacelle,
      anchorParent: [side * 4.8, .4, -.2], anchorChild: [0, 0, 0], axis: [0, 0, 1], limits: [0, Math.PI / 2] });
    const rotor = b.module(`rotor-${side < 0 ? 'left' : 'right'}`, `${side < 0 ? 'Left' : 'Right'} rotor`,
      'rotor', [side * 4.8, 5.1, -.2], false, 1.5);
    b.part(rotor, 'axle', [.3, 1.2, .3], [0, 0, 0], C.silver);
    for (const a of [0, Math.PI / 2]) b.part(rotor, 'beam', [7.2, .18, .45], [0, 1, 0], C.black, quatEuler(0, a, 0));
    b.part(rotor, 'gear', [1.0, .35, 1.0], [0, .8, 0], C.yellow);
    b.joint({ id: `${rotor}-shaft`, name: `${rotor} shaft`, type: 'revolute', parent: nacelle, child: rotor,
      anchorParent: [0, 1.5, 0], anchorChild: [0, 0, 0], axis: [0, 1, 0] });
  }
  const tank = b.module('water-tank', 'Removable water tank', 'service-module', [0, 2.2, .8], false, 6);
  b.part(tank, 'panel', [3.2, 1.4, 4], [0, 0, 0], C.blue);
  b.row(tank, 4, [-1.2, .85, -1.2], [.8, 0, 0], C.silver, [.7, .3, .7], 'plate');
  b.joint({ id: 'tank-latch', name: 'Water tank latch', type: 'fixed', parent: body, child: tank,
    anchorParent: [0, -1, .8], anchorChild: [0, 0, 0] });
  return {
    id: 'wildfire-tiltrotor', name: 'Wildfire Tiltrotor', nameZh: '山火救援倾转旋翼机',
    domain: 'aerial emergency response',
    description: 'A twin-rotor firefighting aircraft with tilting nacelles, removable water tank and serviceable drivetrain.',
    originalDesign: true, modules: b.modules, parts: b.parts, joints: b.joints,
    assemblyOrder: ['fuselage', 'water-tank', 'nacelle-left', 'nacelle-right', 'rotor-left', 'rotor-right'],
    taskConfig: {
      serviceModule: 'water-tank',
      accessPaths: [
        { id: 'belly-lift', label: 'Reach the tank latch through the open belly bay', start: [0, .5, .8], end: [0, 1.4, .8], halfExtents: [.35, .35, .35] },
        { id: 'rear-ramp', label: 'Reach the latch through the occupied tail bay', start: [0, 3.2, 8], end: [0, 3.2, 0], halfExtents: [.35, .35, .35] },
        { id: 'side-door', label: 'Reach the latch through the side crew cabin', start: [-7, 3.2, .8], end: [0, 3.2, .8], halfExtents: [.35, .35, .35] },
      ],
      functionalJoint: 'nacelle-left-tilt', functionalTarget: 1.2,
      loadModule: 'rotor-left', impulseCandidates: [2, 8, 20, 40],
      robustnessLimits: { maxTransientDisplacement: 1.2, maxResidualDisplacement: .45 },
      faultJoint: 'tank-latch', recoveryActions: ['secure-airframe', 'open-belly-panel', 'lower-tank', 'replace-latch', 'raise-tank', 'close-belly-panel'],
      inventoryAlternatives: genericInventory(4), inventoryRequirements: { maxCost: 4, maxPieces: 2, minStiffness: 11 },
      ...genericInspection('tiltrotor', 4),
    },
  };
}

function station(): MechanismModel {
  const b = new Builder();
  const base = b.module('station-base', 'Elevated polar station base', 'foundation', [0, 1, 0], true, 20);
  for (const x of [-4, -2, 0, 2, 4]) for (const z of [-3, -1, 1, 3])
    b.part(base, 'plate', [1.9, .28, 1.8], [x, 0, z], C.gray);
  for (const x of [-4, 0, 4]) for (const z of [-3, 3])
    b.part(base, 'beam', [.65, 2.2, .65], [x, -1.1, z], C.dark);
  for (const z of [-2.7, -.9, .9, 2.7]) for (const x of [-3.5, 3.5])
    b.part(base, 'panel', [.35, 1.8, 1.6], [x, 1.15, z], C.white);
  for (const x of [-2.4, -.8, .8, 2.4]) {
    b.part(base, 'window', [1.4, 1.4, .2], [x, 1.25, -3.8], C.glass);
    b.part(base, 'panel', [1.4, 1.4, .2], [x, 1.25, 3.8], C.white);
  }
  for (const side of [-1, 1]) for (const x of [-2.6, 0, 2.6])
    b.part(base, 'slope', [2.4, .8, 3.8], [x, 2.55, side * 2], side < 0 ? C.orange : C.white,
      quatEuler(side * .3, 0, 0));
  const airlock = b.module('airlock-door', 'Pressure airlock door', 'service-module', [-3.8, 2.2, 0], false, 2);
  b.part(airlock, 'panel', [.35, 2.1, 2.1], [0, 0, 0], C.orange);
  b.part(airlock, 'wheel', [.7, .25, .7], [-.25, 0, 0], C.dark, quatEuler(0, 0, Math.PI / 2));
  b.joint({ id: 'airlock-hinge', name: 'Airlock hinge', type: 'revolute', parent: base, child: airlock,
    anchorParent: [-3.8, 1.2, -1], anchorChild: [0, 0, -1], axis: [0, 1, 0], limits: [0, 1.7] });
  const mast = b.module('wind-mast', 'Wind turbine mast', 'energy-system', [5.3, 1.3, 1.8], false, 4);
  b.row(mast, 7, [0, .5, 0], [0, .7, 0], C.gray, [.6, .62, .6], 'beam');
  b.part(mast, 'panel', [2.2, 1.2, 1.2], [0, 5.4, 0], C.white);
  b.joint({ id: 'mast-foot', name: 'Turbine mast foot', type: 'fixed', parent: base, child: mast,
    anchorParent: [5.3, .3, 1.8], anchorChild: [0, 0, 0] });
  const rotor = b.module('wind-rotor', 'Three-blade wind rotor', 'rotor', [5.3, 7.2, 1.8], false, 1.8);
  b.part(rotor, 'gear', [1.2, .45, 1.2], [0, 0, 0], C.yellow, quatEuler(Math.PI / 2, 0, 0));
  for (const a of [0, 2 * Math.PI / 3, 4 * Math.PI / 3])
    b.part(rotor, 'beam', [.45, .22, 4.8], [Math.sin(a) * 2, Math.cos(a) * 2, 0],
      C.white, quatEuler(0, 0, -a));
  b.joint({ id: 'rotor-shaft', name: 'Wind rotor shaft', type: 'revolute', parent: mast, child: rotor,
    anchorParent: [0, 5.9, 0], anchorChild: [0, 0, 0], axis: [0, 0, 1] });
  const solar = b.module('solar-carriage', 'Sliding solar service carriage', 'actuator', [0, 4.1, 4.8], false, 3);
  for (const x of [-2.4, -.8, .8, 2.4])
    b.part(solar, 'panel', [1.45, .16, 3.2], [x, 0, 0], C.navy, quatEuler(.15, 0, 0));
  b.joint({ id: 'solar-rail', name: 'Solar carriage rail', type: 'prismatic', parent: base, child: solar,
    anchorParent: [0, 3.1, 4.8], anchorChild: [0, 0, 0], axis: [1, 0, 0], limits: [-2, 2] });
  return {
    id: 'polar-research-station', name: 'Polar Research Station', nameZh: '极地科研站',
    domain: 'remote infrastructure',
    description: 'An elevated insulated station with pressure airlock, sliding solar array and serviceable wind turbine.',
    originalDesign: true, modules: b.modules, parts: b.parts, joints: b.joints,
    assemblyOrder: ['station-base', 'wind-mast', 'solar-carriage', 'wind-rotor', 'airlock-door'],
    taskConfig: {
      serviceModule: 'airlock-door',
      accessPaths: [
        { id: 'outside-swing', label: 'Reach the airlock hinge from the exterior', start: [-8, 2.2, 0], end: [-4.3, 2.2, 0], halfExtents: [.3, .35, .35] },
        { id: 'roof-drop', label: 'Lower a probe through the sloped roof', start: [-3.8, 10, 0], end: [-3.8, 4, 0], halfExtents: [.3, .35, .35] },
        { id: 'interior-slide', label: 'Reach the hinge through the occupied laboratory', start: [4, 2.2, 0], end: [-3.1, 2.2, 0], halfExtents: [.3, .35, .35] },
      ],
      functionalJoint: 'solar-rail', functionalTarget: 1.5,
      loadModule: 'wind-rotor', impulseCandidates: [2, 10, 30, 60],
      robustnessLimits: { maxTransientDisplacement: 1.2, maxResidualDisplacement: .45 },
      faultJoint: 'mast-foot', recoveryActions: ['feather-rotor', 'lock-mast', 'replace-foot-brace', 'release-mast', 'spin-test'],
      inventoryAlternatives: genericInventory(5), inventoryRequirements: { maxCost: 3, maxPieces: 1, minStiffness: 11 },
      ...genericInspection('station', 5),
    },
  };
}

let cache: MechanismModel[] | undefined;
export function mechanismModels() {
  if (!cache) {
    cache = [rover(), crane(), drawbridge(), observatory(), tiltrotor(), station()];
    for (const model of cache) {
      assert.equal(model.originalDesign, true);
      assert.ok(model.parts.length >= 35, `${model.id}: insufficient visual complexity`);
      assert.equal(new Set(model.parts.map(p => p.id)).size, model.parts.length);
      assert.equal(new Set(model.modules.map(m => m.id)).size, model.modules.length);
      assert.equal(new Set(model.joints.map(j => j.id)).size, model.joints.length);
      assert.ok(model.modules.some(m => m.role === 'service-module'), `${model.id}: service module`);
      assert.ok(model.joints.some(j => ['revolute', 'prismatic'].includes(j.type)), `${model.id}: functional joint`);
    }
  }
  return cache;
}
