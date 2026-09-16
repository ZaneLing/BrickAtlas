import { hierarchyModels } from '../hierarchy/models';
import type { MechanismModel, MechanismPart, MechanismModule, MechanismJoint, Vec3, Quat } from '../mechanism/types';
import type { DifficultyId } from '../hierarchy/types';
import { Box3, Quaternion, Vector3 } from 'three';
import { partEnvelope, partMatrix } from '../../../src/benchmark/geometry';

export type Model = MechanismModel & { difficulty: DifficultyId; family: string; lineage: string };
const Q: Quat = [0, 0, 0, 1];
const colors = ['#e9ad37', '#387bb3', '#dc6040', '#45a080', '#dfebed', '#273e50'];
const qz = (a: number): Quat => [0, 0, Math.sin(a / 2), Math.cos(a / 2)];

// Authored module layouts. Coordinates are scene units, not commercial part specifications.
class Design {
  parts: MechanismPart[] = [];
  modules: MechanismModule[] = [];
  joints: MechanismJoint[] = [];
  add(id: string, position: Vec3, role: string, parent?: string, type: MechanismJoint['type'] = 'fixed',
    axis: Vec3 = [0, 1, 0]) {
    this.modules.push({ id, name: id.replaceAll('-', ' '), role, position, rotation: Q, anchored: !parent, mass: role === 'frame' ? 10 : 2 });
    if (parent) {
      const p = this.modules.find(m => m.id === parent)!;
      this.joints.push({ id: `${id}-joint`, name: `${id} interface`, parent, child: id, type,
        anchorParent: position.map((v, i) => v - p.position[i]) as Vec3, anchorChild: [0, 0, 0],
        axis, ...(type !== 'fixed' ? { limits: [-0.8, 0.8] as [number, number] } : {}) });
    }
    return id;
  }
  part(moduleId: string, shape: MechanismPart['shape'], position: Vec3, size: Vec3,
    color = colors[0], rotation = Q) {
    this.parts.push({ id: `${moduleId}-p${this.parts.length + 1}`, moduleId, shape, position, size, color, rotation });
  }
  deck(id: string, nx: number, nz: number, color = colors[4], y = 0) {
    for (let x = 0; x < nx; x++) for (let z = 0; z < nz; z++)
      this.part(id, 'plate', [x - (nx - 1) / 2, y, z - (nz - 1) / 2], [0.98, 0.28, 0.98], color);
  }
  beam(id: string, length: number, angle = 0, color = colors[0]) {
    for (let n = 0; n < length; n++)
      this.part(id, 'beam', [Math.cos(angle) * (n + 0.5), Math.sin(angle) * (n + 0.5), 0],
        [0.99, 0.48, 0.5], color, qz(angle));
    this.part(id, 'gear', [0, 0, 0], [0.85, 0.3, 0.85], colors[5]);
  }
  tower(id: string, height: number) {
    for (const x of [-1.5, 1.5]) for (const z of [-1, 1])
      for (let y = 0; y < height; y++) this.part(id, 'brick', [x, y * 0.6, z], [0.7, 0.6, 0.7], colors[4]);
    for (let y = 0; y < height; y += 3)
      this.part(id, 'beam', [0, y * 0.6, -1], [3.7, 0.25, 0.4], colors[1]);
  }
}

type Spec = [string, string, string, DifficultyId, string];
const SPECS: Spec[] = [
  ['camera-gimbal', '相机稳定云台', 'Camera Gimbal', 'D1', 'gimbal'],
  ['folding-gripper', '折叠夹持器', 'Folding Gripper', 'D1', 'gripper'],
  ['ratchet-hoist', '棘轮微型提升器', 'Ratchet Hoist', 'D1', 'hoist'],
  ['sample-carousel', '样品转盘', 'Sample Carousel', 'D1', 'carousel'],
  ['sliding-drawer', '导轨工具抽屉', 'Rail Tool Drawer', 'D1', 'drawer'],
  ['wind-vane', '风向测量仪', 'Wind Vane', 'D1', 'vane'],
  ['scissor-service-lift', '剪式检修升降台', 'Scissor Service Lift', 'D2', 'lift'],
  ['tracked-drill', '履带取芯钻机', 'Tracked Core Drill', 'D2', 'drill'],
  ['swing-dock', '旋转装卸码头', 'Swing Loading Dock', 'D2', 'dock'],
  ['telescope-cart', '伸缩光学巡检车', 'Telescopic Optics Cart', 'D2', 'optics'],
  ['articulated-loader', '铰接装载机', 'Articulated Loader', 'D2', 'loader'],
  ['folding-weather-mast', '折叠气象桅杆', 'Folding Weather Mast', 'D2', 'weather'],
  ['cable-inspection-robot', '缆索巡检机器人', 'Cable Inspection Robot', 'D3', 'cable'],
  ['subsea-manipulator', '深海双臂作业器', 'Subsea Manipulator', 'D3', 'subsea'],
  ['rotary-excavator', '回转斗轮挖掘机', 'Rotary Bucket Excavator', 'D3', 'excavator'],
  ['retractable-radar', '收展式相控阵雷达', 'Retractable Array Radar', 'D3', 'radar'],
  ['polar-drilling-complex', '极地钻探综合站', 'Polar Drilling Complex', 'D4', 'drill'],
  ['aircraft-service-hangar', '航空器协同检修库', 'Aircraft Service Hangar', 'D4', 'hangar'],
  ['tidal-energy-station', '潮汐能维护站', 'Tidal Energy Station', 'D4', 'turbine'],
  ['orbital-telescope-yard', '轨道望远镜装配场', 'Orbital Telescope Yard', 'D4', 'optics'],
  ['automated-recycling-plant', '自动分拣回收厂', 'Automated Recycling Plant', 'D4', 'recycling'],
  ['rescue-launch-complex', '应急救援发射基地', 'Rescue Launch Complex', 'D4', 'launch'],
];

function author([id, nameZh, name, difficulty, family]: Spec): Model {
  const d = new Design(), level = Number(difficulty[1]);
  const base = d.add('foundation', [0, 0.3, 0], 'frame');
  d.deck(base, level === 1 ? 3 : level === 4 ? 12 : 6, level === 1 ? 2 : level === 4 ? 10 : 5, colors[5]);
  let functional = '', service = '';
  const addArm = (prefix: string, p: Vec3, parent: string, angle: number, length: number) => {
    const a = d.add(prefix, p, 'actuator', parent, 'revolute', [0, 0, 1]);
    d.beam(a, length, angle);
    functional ||= `${a}-joint`;
    return a;
  };
  if (level === 1) {
    const mount = d.add('mount', [0, 1.2, 0], 'support', base);
    d.part(mount, 'cylinder', [0, 0, 0], [1, 1.2, 1], colors[4]);
    if (family === 'gripper') {
      addArm('finger-left', [-0.4, 2.1, -0.45], mount, 0.65, 3);
      addArm('finger-right', [0.4, 2.1, 0.45], mount, 2.49, 3);
    } else if (family === 'carousel' || family === 'vane') {
      const rotor = d.add('rotor', [0, 2.1, 0], 'actuator', mount, 'revolute');
      functional = 'rotor-joint';
      for (let i = 0; i < (family === 'carousel' ? 4 : 3); i++)
        d.part(rotor, 'beam', [Math.cos(i * 2.1), 0, Math.sin(i * 2.1)], [2.5, 0.3, 0.4], colors[i]);
    } else if (family === 'drawer') {
      const slide = d.add('drawer', [0, 2.1, 0], 'actuator', mount, 'prismatic', [1, 0, 0]);
      d.deck(slide, 3, 2, colors[1]); functional = 'drawer-joint';
    } else {
      const arm = addArm('yoke', [0, 2.1, 0], mount, family === 'hoist' ? 0.9 : 0.3, 3);
      d.part(arm, family === 'hoist' ? 'gear' : 'sphere', [2, 0.5, 0], [1, 1, 1], colors[1]);
    }
    service = d.add('service-cartridge', [0, 0.75, 2.2], 'service', base);
    d.deck(service, 2, 2, colors[2]);
  } else {
    const mast = d.add('mast', [-1.6, 0.9, -0.6], 'frame', base);
    d.tower(mast, level * 3);
    const pivotY = level * 1.8 + 0.7;
    const rotation = family === 'dock' || family === 'cable' ? 0.1 : family === 'drill' ? -0.15 : 0.65;
    const boom = addArm('primary-boom', [-1.6, pivotY, -0.6], mast, rotation, level + 3);
    const tip: Vec3 = [-1.6 + Math.cos(rotation) * (level + 3), pivotY + Math.sin(rotation) * (level + 3),
      ['loader', 'excavator'].includes(family) ? 1.4 : 0.6];
    const tool = d.add('tool-head', tip, 'tool', boom, family === 'drill' ? 'prismatic' : 'revolute',
      family === 'drill' ? [0, 1, 0] : [0, 0, 1]);
    if (['optics', 'radar'].includes(family)) {
      for (let n = 0; n < 12; n++) {
        const a = n * Math.PI / 6;
        d.part(tool, 'slope', [Math.cos(a) * 1.7, Math.sin(a) * 1.7, 0],
          [0.8, 0.8, 0.5], colors[1], qz(a));
      }
      d.part(tool, 'cylinder', [0, 0, 0], [1.5, 1.8, 1.5], colors[4]);
    } else if (family === 'loader' || family === 'excavator') {
      d.deck(tool, 4, 3, colors[2]);
      for (const z of [-1, 1]) d.part(tool, 'panel', [0, 0.7, z], [4, 1.4, 0.2], colors[2]);
    } else {
      d.part(tool, 'gear', [0, 0, 0], [1.7, 0.8, 1.7], colors[2]);
      d.part(tool, 'axle', [0, -1, 0], [0.4, 2, 0.4], colors[4]);
    }
    const cab = d.add('control-cab', [2, 1.2, 1.8], 'control', base);
    d.deck(cab, 2, 3, colors[4]);
    d.part(cab, 'window', [0, 1, -1.2], [2, 1.5, 0.15], '#79c7d8');
    d.part(cab, 'slope', [0, 1.8, 0], [2.5, 0.5, 3], colors[1]);
    service = d.add('service-cartridge', [2, 0.8, -2], 'service', base);
    d.deck(service, 2, 2, colors[2]);
    if (level >= 3) {
      const second = addArm('secondary-boom', [2.8, 2, 4], cab, 2.0, level + 1);
      const clamp = d.add('clamp', [2.8 + Math.cos(2) * (level + 1), 2 + Math.sin(2) * (level + 1), 4.8],
        'tool', second, 'revolute', [0, 0, 1]);
      d.part(clamp, 'arch', [0, 0, 0], [1.8, 1, 1], colors[0]);
      const tray = d.add('sliding-tray', [0, 1.8, 3.9], 'payload', base, 'prismatic', [0, 0, 1]);
      d.deck(tray, 4, 2, colors[3]);
    }
    if (['loader', 'drill', 'excavator'].includes(family)) {
      for (const side of [-1, 1]) {
        const track = d.add(`track-${side}`, [0, 0.6, side * 4], 'traction', base, 'revolute', [0, 0, 1]);
        for (const x of [-2, 0, 2]) d.part(track, 'wheel', [x, 0, 0], [1.3, 0.7, 1.3], colors[5],
          [Math.SQRT1_2, 0, 0, Math.SQRT1_2]);
        for (let i = 0; i < 8; i++) {
          d.part(track, 'beam', [-2.5 + i * 0.7, 0.8, 0], [0.68, 0.25, 0.8], '#405267');
          d.part(track, 'beam', [-2.5 + i * 0.7, -0.6, 0], [0.68, 0.25, 0.8], '#405267');
        }
      }
    }
    if (family === 'lift') {
      const platform = d.add('elevating-platform', [0, 5, 2], 'payload', base, 'prismatic', [0, 1, 0]);
      d.deck(platform, 5, 4, colors[2]);
      for (const side of [-1, 1]) {
        const scissor = d.add(`scissor-${side}`, [0, 1, side * 3.8], 'linkage', base, 'revolute', [0, 0, 1]);
        d.beam(scissor, 5, side > 0 ? 0.9 : 2.2, colors[3]);
      }
    }
    if (family === 'weather') {
      const vane = d.add('weather-head', [-1.6, pivotY + 3, -0.6], 'sensor', mast, 'revolute');
      for (let i = 0; i < 3; i++) {
        d.part(vane, 'beam', [Math.cos(i * 2.1), 0, Math.sin(i * 2.1)], [2, 0.2, 0.4], colors[1]);
        d.part(vane, 'sphere', [2 * Math.cos(i * 2.1), 0, 2 * Math.sin(i * 2.1)], [0.7, 0.7, 0.7], colors[2]);
      }
      d.part(vane, 'panel', [0, 1, 0], [0.1, 1.5, 2], colors[4]);
    }
    if (family === 'dock') {
      const ramp = d.add('loading-ramp', [6.8, 1, 0], 'ramp', base, 'revolute', [0, 0, 1]);
      d.deck(ramp, 6, 4, colors[3]);
      d.part(ramp, 'beam', [0, 0.6, 2], [6, 0.4, 0.4], colors[0]);
    }
    if (family === 'cable') {
      for (const z of [-2.5, 2.5]) {
        const wheel = d.add(`cable-roller-${z}`, [0, 7, z], 'traction', mast, 'revolute', [0, 0, 1]);
        d.part(wheel, 'wheel', [0, 0, 0], [2, 1, 2], colors[2]);
        d.part(wheel, 'axle', [0, 0, 0], [0.3, 3, 0.3], colors[5]);
      }
    }
    if (family === 'subsea') {
      for (const z of [-4.5, 4.5]) {
        const tank = d.add(`buoyancy-${z}`, [0, 3, z], 'buoyancy', base);
        for (let n = 0; n < 6; n++) d.part(tank, 'cylinder', [n - 2.5, 0, 0],
          [1, 1.4, 1], colors[0]);
      }
    }
    if (family === 'radar') {
      const dish = d.add('folding-array', [0, 7, -2], 'sensor', boom, 'revolute', [1, 0, 0]);
      d.deck(dish, 5, 5, colors[1]);
    }
    if (level === 4) {
      // Six distinct system layouts: processing, energy, hangar, launch, drilling and optics.
      const stations = family === 'hangar' ? 4 : family === 'recycling' ? 5 : 3;
      for (let i = 0; i < stations; i++) {
        const angle = (i + 0.4) * Math.PI * 2 / stations;
        const station = d.add(`station-${i}`, [Math.cos(angle) * 7, 0.7, Math.sin(angle) * 7],
          'workcell', base);
        d.deck(station, 4, 3, colors[(i + 1) % colors.length]);
        const machine = d.add(`station-${i}-machine`,
          [Math.cos(angle) * 7, 1.5, Math.sin(angle) * 7], 'processor', station, 'revolute');
        if (family === 'launch' || family === 'drill') {
          for (let h = 0; h < 7; h++) d.part(machine, 'cylinder', [0, h * 0.7, 0],
            [1.1, 0.7, 1.1], colors[(i + 2) % colors.length]);
          d.part(machine, 'slope', [0, 5.2, 0], [1.5, 1.1, 1.5], colors[4]);
        } else if (family === 'optics' || family === 'turbine') {
          for (let blade = 0; blade < 6; blade++)
            d.part(machine, 'beam', [Math.cos(blade) * 1.4, 0, Math.sin(blade) * 1.4],
              [2.1, 0.3, 0.6], colors[i % 3]);
        } else {
          d.tower(machine, 4);
          d.part(machine, 'window', [0, 1.8, 1], [2.6, 1.2, 0.2], '#79c7d8');
        }
        const conveyor = d.add(`station-${i}-transfer`,
          [Math.cos(angle) * 12, 1, Math.sin(angle) * 12], 'transport', station, 'prismatic', [Math.cos(angle), 0, Math.sin(angle)]);
        d.deck(conveyor, 4, 2, colors[5]);
      }
      if (family === 'hangar') {
        const roof = d.add('hangar-roof', [0, 14, 0], 'enclosure', mast);
        d.deck(roof, 12, 6, colors[4]);
      }
      if (family === 'launch') {
        const launcher = d.add('launch-rail', [-7, 2, -3], 'launch-structure', base, 'revolute', [0, 0, 1]);
        d.beam(launcher, 12, 1.25, colors[3]);
      }
    }
  }
  const serviceJoint = d.joints.find(j => j.child === service)!;
  const load = d.joints.find(j => j.id === functional)!.child;
  return {
    id, name, nameZh, domain: family, family, difficulty, lineage: id, originalDesign: true,
    description: `${name}: an authored ${difficulty} articulated system with ${d.modules.length} modules.`,
    parts: d.parts, modules: d.modules, joints: d.joints, assemblyOrder: d.modules.map(m => m.id),
    taskConfig: { serviceModule: service, functionalJoint: functional, functionalTarget: 0.5,
      loadModule: load, faultJoint: serviceJoint.id, recoveryActions: [], accessPaths: [],
      impulseCandidates: [1, 5, 20, 80], robustnessLimits: { maxTransientDisplacement: 0.5, maxResidualDisplacement: 0.2 },
      inventoryAlternatives: [], inventoryRequirements: { maxCost: 6, maxPieces: 2, minStiffness: 8 },
      hiddenWorlds: [], inspectionQueries: [] },
  };
}

export function models(): Model[] {
  const retained = hierarchyModels().map(m => ({ ...structuredClone(m), lineage: m.id }));
  const all = [...retained, ...SPECS.map(author), ...expandedModels()];
  return all.map(correctedModel).sort((a, b) => a.difficulty.localeCompare(b.difficulty) || a.id.localeCompare(b.id));
}

function expandedModels(): Model[] {
  const specs: Spec[] = [
    ['indexed-toggle-latch', '双轴索引锁扣', 'Indexed Toggle Latch', 'D1', 'serial-latch'],
    ['orthogonal-probe-stage', '正交探针微调台', 'Orthogonal Probe Stage', 'D1', 'orthogonal-stage'],
    ['parallel-pallet-handler', '双臂托盘转运器', 'Parallel Pallet Handler', 'D2', 'dual-arm-transfer'],
    ['articulated-camera-dolly', '多轴相机检修滑台', 'Articulated Camera Dolly', 'D2', 'serial-camera-stage'],
    ['tri-arm-sample-handler', '三臂样品操作器', 'Tri-arm Sample Handler', 'D3', 'parallel-handoff'],
    ['segmented-petal-observatory', '分瓣展开观测仪', 'Segmented Petal Observatory', 'D3', 'petal-deployment'],
    ['distributed-battery-exchange', '多工位电池交换站', 'Distributed Battery Exchange', 'D4', 'battery-workcells'],
    ['segmented-antenna-yard', '分段天线协作装配场', 'Segmented Antenna Yard', 'D4', 'antenna-workcells'],
  ];
  return specs.map(([id, nameZh, name, difficulty, family]) => {
    const d = new Design(), level = Number(difficulty[1]);
    const base = d.add('frame', [0, 0.3, 0], 'frame');
    d.deck(base, level * 2 + 2, level * 2 + 2, colors[5]);
    let service = '', functional = '', load = '';
    const branches = family === 'petal-deployment' ? 6 : family === 'antenna-workcells' ? 5
      : level === 1 ? 1 : level === 2 ? 2 : level === 3 ? 3 : 4;
    for (let b = 0; b < branches; b++) {
      const offset = (b - (branches - 1) / 2) * (level === 4 ? 7 : 4);
      const rail = d.add(`rail-${b}`, [offset, 1, 0], 'guide', base);
      d.part(rail, 'beam', [0, 0, 0], [0.6, 0.4, level * 2 + 2], colors[4]);
      const slide = d.add(`carriage-${b}`, [offset, 1.5, 0], 'linear-stage', rail, 'prismatic', [0, 0, 1]);
      d.deck(slide, 2, 2, colors[1]);
      const pivot = d.add(`turret-${b}`, [offset, 2.2, 0], 'rotary-stage', slide, 'revolute', [0, 1, 0]);
      d.part(pivot, 'cylinder', [0, 0, 0], [1.2, 0.8, 1.2], colors[0]);
      const arm = d.add(`elbow-${b}`, [offset, 2.65, 0], 'linkage', pivot, 'revolute', [1, 0, 0]);
      d.part(arm, 'beam', [0, 0.5 + level * 0.3, 0], [0.55, 1 + level * 0.6, 0.5], colors[2]);
      const head = d.add(`head-${b}`, [offset, 4.1 + level * 0.6, 0], 'service-tool', arm,
        family === 'orthogonal-stage' ? 'prismatic' : 'revolute', family === 'orthogonal-stage' ? [1, 0, 0] : [0, 0, 1]);
      d.part(head, family.includes('camera') ? 'cylinder' : 'arch', [0, 0, 0], [1.6, 0.7, 1], colors[3]);
      d.part(head, 'panel', [0, 0.45, 0], [1.8, 0.15, 1.2], colors[4]);
      if (b === 0) { service = head; functional = `${slide}-joint`; load = head; }
      if (level >= 3) {
        const petal = d.add(`petal-${b}`, [offset, 5.4 + level * 0.6, 0], 'deployable-surface', head, 'revolute', [0, 0, 1]);
        d.deck(petal, 3, level + 1, colors[1]);
        const sensor = d.add(`sensor-${b}`, [offset, 5.95 + level * 0.6, 0], 'instrument', petal);
        d.part(sensor, 'sphere', [0, 0, 0], [0.8, 0.6, 0.8], '#79c7d8');
      }
      if (level === 4) {
        const rack = d.add(`rack-${b}`, [offset, 1, -7], 'storage', base);
        for (let shelf = 0; shelf < 3; shelf++) {
          d.deck(rack, 4, 3, colors[4], shelf * 1.4);
        }
        for (const x of [-1.8, 1.8]) d.part(rack, 'beam', [x, 1.4, 0], [0.25, 3.4, 0.25], colors[5]);
        const pack = d.add(`exchange-pack-${b}`, [offset, 3, -7], 'payload', rack, 'prismatic', [0, 0, 1]);
        d.part(pack, 'panel', [0, 0, 0], [2.4, 0.6, 1.8], colors[b % 3]);
        const gate = d.add(`gate-${b}`, [offset, 1.5, 6], 'interlock', base, 'revolute', [0, 1, 0]);
        d.part(gate, 'panel', [0, 0.5, 0], [3, 1.8, 0.25], colors[0]);
      }
    }
    return { id, name, nameZh, difficulty, family, domain: family, lineage: id, originalDesign: true,
      description: `${name}: ${branches} independently constrained serial workcell chains with service and exchange interfaces.`,
      modules: d.modules, parts: d.parts, joints: d.joints, assemblyOrder: d.modules.map(m => m.id),
      taskConfig: { serviceModule: service, loadModule: load, functionalJoint: functional,
        functionalTarget: 0.5, faultJoint: `${service}-joint`, accessPaths: [], recoveryActions: [],
        impulseCandidates: [1, 5, 20], robustnessLimits: { maxTransientDisplacement: 0.5, maxResidualDisplacement: 0.2 },
        inventoryAlternatives: [], inventoryRequirements: { maxCost: 6, maxPieces: 2, minStiffness: 8 },
        hiddenWorlds: [], inspectionQueries: [] } };
  });
}

export function correctedModel(source: Model): Model {
  const model = structuredClone(source);
  const relocations: Record<string, Record<string, Vec3>> = {
    'canal-inspection-skiff': { rudder: [1.8, 0, 0], propeller: [0.1, 0, 0] },
    'bascule-canal-gate': { 'west-deck': [0, 0.3, 0], 'east-deck': [0, 0.3, 0],
      'tower-left': [-2.4, 0, 0], 'tower-right': [2.4, 0, 0], 'drive-cartridge': [-2.4, 0.6, -0.7] },
    'hinged-safety-hatch': { lid: [0, 0.2, 0], latch: [0, 0.5, 0] },
    'warehouse-sorter': { scanner: [0, 0, -0.3], 'diverter-gate': [0, 0.1, 0] },
    'maintenance-trolley': { 'front-axle': [0, -0.55, 0], 'rear-axle': [0, -0.55, 0] },
    'signal-switch-stand': { 'signal-arm': [0, 0, 0.55], lamp: [0.2, 0, 0.55] },
    'solar-tracker-array': { yoke: [0, 0.3, 0], 'panel-left': [-0.4, 0.3, 0], 'panel-right': [0.4, 0.3, 0] },
    'adaptive-radio-observatory': { telescope: [0, 1.8, 0], 'camera-pack': [0, 1.7, 0.5] },
    'harbor-container-crane': { hoist: [0.3, -0.2, 0] },
    'swing-dock': { 'control-cab': [-0.1, 0, 0] },
    'tracked-drill': { 'tool-head': [0.9, 0, 0] },
    'subsea-manipulator': { 'buoyancy-4.5': [0, 0, 0.3] },
    'orbital-service-rover': { battery: [0, 0, 1.8],
      'wheel-lf': [-0.6, 0, 0], 'wheel-lm': [-0.6, 0, 0], 'wheel-lr': [-0.6, 0, 0],
      'wheel-rf': [0.6, 0, 0], 'wheel-rm': [0.6, 0, 0], 'wheel-rr': [0.6, 0, 0] },
    'polar-research-station': { 'airlock-door': [-1.4, 0, 0.3], 'wind-rotor': [0, 0.9, 0] },
    'wildfire-tiltrotor': { 'nacelle-left': [-0.9, 0, 0], 'nacelle-right': [0.9, 0, 0], 'water-tank': [0, -0.5, 0] },
    'retractable-radar': { 'folding-array': [0, 0, -1.4], 'tool-head': [0, 0, 0.4] },
    'polar-drilling-complex': { 'track--1': [0, 0, -1.5], 'track-1': [0, 0, 1.5], 'station-2': [0, 0, -0.7] },
    'automated-cargo-terminal': { 'rack-a': [-2.2, 0, 0], 'rack-b': [2.2, 0, 0],
      lift: [0, 0.2, 0], shuttle: [0, 0.1, 0], 'container-blue': [1, 0, 0], 'container-yellow': [2, 0, 0] },
    'flood-response-lock': { 'pump-a': [-1.1, 0.15, 2.8], 'pump-b': [1.1, 0.15, 2.8] },
    'lunar-sample-refinery': { conveyor: [0, 0.1, -0.7], 'loading-arm': [0.3, 0, -0.8],
      'sample-rover': [0, 0.2, 0], centrifuge: [0, 0.9, 0] },
    'orbital-docking-yard': { 'cargo-pod': [0, 0, 0.3], 'dock-arm-west': [-0.5, 0.3, 0],
      'dock-arm-east': [0.5, 0.3, 0], 'crane-boom': [0, 0.3, 0] },
  };
  const shifts = relocations[model.id] ?? {};
  if (model.id === 'flood-response-lock') for (const [index, anchor] of ([[2, 0.6, 0], [-2, 0.6, 1]] as Vec3[]).entries())
    model.joints.push({ id: `barge-mooring-${index + 2}`, name: 'Separated elastic mooring', type: 'spring',
      parent: 'basin', child: 'service-barge', anchorParent: anchor, anchorChild: anchor,
      restLength: 0, stiffness: 4000, damping: 160 });
  for (const m of model.modules) if (shifts[m.id])
    m.position = new Vector3(...m.position).add(new Vector3(...shifts[m.id])).toArray() as Vec3;
  for (const j of model.joints) {
    const delta = new Vector3(...(shifts[j.child] ?? [0, 0, 0])).sub(new Vector3(...(shifts[j.parent] ?? [0, 0, 0])));
    const parent = model.modules.find(m => m.id === j.parent)!;
    j.anchorParent = new Vector3(...j.anchorParent).add(delta.applyQuaternion(new Quaternion(...parent.rotation).invert())).toArray() as Vec3;
    if (j.type === 'spring' && !j.stiffness) { j.stiffness = 4000; j.damping = 160; }
  }
  // The gate tower footing used y=.1 on only one side of four fixed joints.
  if (model.id === 'bascule-canal-gate') for (const j of model.joints.filter(j => /tower.*foot/.test(j.id))) {
    const parent = model.modules.find(m => m.id === j.parent)!, child = model.modules.find(m => m.id === j.child)!;
    j.anchorChild = new Vector3(...j.anchorParent).applyQuaternion(new Quaternion(...parent.rotation))
      .add(new Vector3(...parent.position)).sub(new Vector3(...child.position))
      .applyQuaternion(new Quaternion(...child.rotation).invert()).toArray() as Vec3;
  }
  // Recenter local frames while preserving every world-space vertex and joint.
  // This removes the distant-origin convention of the 12 legacy Builder objects.
  for (const m of model.modules) {
    const bounds = new Box3();
    const parts = model.parts.filter(p => p.moduleId === m.id);
    for (const p of parts) {
      const { center, half } = partEnvelope(p);
      bounds.union(new Box3(center.clone().sub(half), center.clone().add(half))
        .applyMatrix4(partMatrix(p.position, p.rotation)));
    }
    const shift = bounds.getCenter(new Vector3());
    m.position = new Vector3(...m.position).add(shift.clone().applyQuaternion(new Quaternion(...m.rotation))).toArray() as Vec3;
    for (const p of parts) p.position = new Vector3(...p.position).sub(shift).toArray() as Vec3;
    for (const j of model.joints) {
      if (j.parent === m.id) j.anchorParent = new Vector3(...j.anchorParent).sub(shift).toArray() as Vec3;
      if (j.child === m.id) j.anchorChild = new Vector3(...j.anchorChild).sub(shift).toArray() as Vec3;
    }
  }
  return model;
}
