import { hierarchyModels } from '../hierarchy/models';
import type { MechanismModel, MechanismPart, MechanismModule, MechanismJoint, Vec3, Quat } from '../mechanism/types';
import type { DifficultyId } from '../hierarchy/types';

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
    const mount = d.add('mount', [0, 1, 0], 'support', base);
    d.part(mount, 'cylinder', [0, 0, 0], [1, 1.2, 1], colors[4]);
    if (family === 'gripper') {
      addArm('finger-left', [-0.4, 1.7, 0], mount, 0.65, 3);
      addArm('finger-right', [0.4, 1.7, 0], mount, 2.49, 3);
    } else if (family === 'carousel' || family === 'vane') {
      const rotor = d.add('rotor', [0, 1.8, 0], 'actuator', mount, 'revolute');
      functional = 'rotor-joint';
      for (let i = 0; i < (family === 'carousel' ? 4 : 3); i++)
        d.part(rotor, 'beam', [Math.cos(i * 2.1), 0, Math.sin(i * 2.1)], [2.5, 0.3, 0.4], colors[i]);
    } else if (family === 'drawer') {
      const slide = d.add('drawer', [0, 1.7, 0], 'actuator', mount, 'prismatic', [1, 0, 0]);
      d.deck(slide, 3, 2, colors[1]); functional = 'drawer-joint';
    } else {
      const arm = addArm('yoke', [0, 1.6, 0], mount, family === 'hoist' ? 0.9 : 0.3, 3);
      d.part(arm, family === 'hoist' ? 'gear' : 'sphere', [2, 0.5, 0], [1, 1, 1], colors[1]);
    }
    service = d.add('service-cartridge', [0, 0.75, 1.2], 'service', base);
    d.deck(service, 2, 2, colors[2]);
  } else {
    const mast = d.add('mast', [-1.6, 0.7, -0.6], 'frame', base);
    d.tower(mast, level * 3);
    const pivotY = level * 1.8 + 0.7;
    const rotation = family === 'dock' || family === 'cable' ? 0.1 : family === 'drill' ? -1.1 : 0.65;
    const boom = addArm('primary-boom', [-1.6, pivotY, -0.6], mast, rotation, level + 3);
    const tip: Vec3 = [-1.6 + Math.cos(rotation) * (level + 3), pivotY + Math.sin(rotation) * (level + 3), -0.6];
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
    const cab = d.add('control-cab', [2, 1.2, 1.3], 'control', base);
    d.deck(cab, 2, 3, colors[4]);
    d.part(cab, 'window', [0, 1, -1.2], [2, 1.5, 0.15], '#79c7d8');
    d.part(cab, 'slope', [0, 1.8, 0], [2.5, 0.5, 3], colors[1]);
    service = d.add('service-cartridge', [2, 0.8, -2], 'service', base);
    d.deck(service, 2, 2, colors[2]);
    if (level >= 3) {
      const second = addArm('secondary-boom', [2.8, 2, 0], cab, 2.0, level + 1);
      const clamp = d.add('clamp', [1, 5, 0], 'tool', second, 'revolute', [0, 0, 1]);
      d.part(clamp, 'arch', [0, 0, 0], [1.8, 1, 1], colors[0]);
      const tray = d.add('sliding-tray', [0, 0.9, 2.5], 'payload', base, 'prismatic', [0, 0, 1]);
      d.deck(tray, 4, 2, colors[3]);
    }
    if (['loader', 'drill', 'excavator'].includes(family)) {
      for (const side of [-1, 1]) {
        const track = d.add(`track-${side}`, [0, 0.6, side * 3.1], 'traction', base, 'revolute', [0, 0, 1]);
        for (const x of [-2, 0, 2]) d.part(track, 'wheel', [x, 0, 0], [1.3, 0.7, 1.3], colors[5]);
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
        const scissor = d.add(`scissor-${side}`, [0, 1, side * 1.5], 'linkage', base, 'revolute', [0, 0, 1]);
        d.beam(scissor, 5, side > 0 ? 0.9 : 2.2, colors[3]);
      }
    }
    if (family === 'weather') {
      const vane = d.add('weather-head', [0, 7, 0], 'sensor', boom, 'revolute');
      for (let i = 0; i < 3; i++) {
        d.part(vane, 'beam', [Math.cos(i * 2.1), 0, Math.sin(i * 2.1)], [2, 0.2, 0.4], colors[1]);
        d.part(vane, 'sphere', [2 * Math.cos(i * 2.1), 0, 2 * Math.sin(i * 2.1)], [0.7, 0.7, 0.7], colors[2]);
      }
      d.part(vane, 'panel', [0, 1, 0], [0.1, 1.5, 2], colors[4]);
    }
    if (family === 'dock') {
      const ramp = d.add('loading-ramp', [4, 1, 0], 'ramp', base, 'revolute', [0, 0, 1]);
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
      for (const z of [-3, 3]) {
        const tank = d.add(`buoyancy-${z}`, [0, 2, z], 'buoyancy', base);
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
          [Math.cos(angle) * 4, 1, Math.sin(angle) * 4], 'transport', station, 'prismatic', [1, 0, 0]);
        d.deck(conveyor, 4, 2, colors[5]);
      }
      if (family === 'hangar') {
        const roof = d.add('hangar-roof', [0, 11, 0], 'enclosure', mast);
        d.deck(roof, 12, 6, colors[4]);
      }
      if (family === 'launch') {
        const launcher = d.add('launch-rail', [-5, 2, 0], 'launch-structure', base, 'revolute', [0, 0, 1]);
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
  const all = [...retained, ...SPECS.map(author)];
  return all.sort((a, b) => a.difficulty.localeCompare(b.difficulty) || a.id.localeCompare(b.id));
}
