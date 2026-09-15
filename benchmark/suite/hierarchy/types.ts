import type { MechanismModel, Vec3 } from '../mechanism/types';

export type DifficultyId = 'D1' | 'D2' | 'D3' | 'D4';
export type TaskLayer = 'atomic' | 'metacognitive' | 'procedural' | 'integrative';
export type QuestionFormat =
  | 'single-choice'
  | 'multiple-choice'
  | 'ordered-actions'
  | 'structured-plan';

export interface DifficultySpec {
  id: DifficultyId;
  name: string;
  nameZh: string;
  intent: string;
  typicalParts: [number, number];
  typicalModules: [number, number];
  typicalJoints: [number, number];
  operationHorizon: [number, number];
  observationBurden: string;
  coupledConstraints: number;
}

export interface ComplexityProfile {
  visibleParts: number;
  modules: number;
  joints: number;
  movingJoints: number;
  dependencyDepth: number;
  hiddenInterfaces: number;
  coupledConstraints: number;
  operationHorizon: number;
  complexityIndex: number;
}

export interface HierarchyModel extends MechanismModel {
  difficulty: DifficultyId;
  family: string;
  designNotes: string[];
  complexity: ComplexityProfile;
}

export interface ChoiceOption {
  id: 'A' | 'B' | 'C' | 'D';
  label: string;
}

export interface TaskVisualization {
  modelImage: string;
  detailImage: string;
  highlightModules: string[];
  view: 'iso' | 'front' | 'side' | 'top';
  accessPaths?: Array<{ start: Vec3; end: Vec3; accessible: boolean }>;
  force?: { moduleId: string; vector: Vec3 };
}

export interface HierarchyTask {
  id: string;
  sourceGroup: string;
  difficulty: DifficultyId;
  layer: TaskLayer;
  format: QuestionFormat;
  family: string;
  operation?: string;
  capability: string[];
  question: string;
  options?: ChoiceOption[];
  input: Record<string, unknown>;
  responseSchema: Record<string, unknown>;
  oracle: Record<string, unknown>;
  oracleMethod: string;
  visualization: TaskVisualization;
}

export const DIFFICULTIES: DifficultySpec[] = [
  {
    id: 'D1',
    name: 'Component',
    nameZh: '部件级',
    intent: 'Single interface, local state change, and short dependency chain.',
    typicalParts: [12, 30],
    typicalModules: [2, 5],
    typicalJoints: [1, 4],
    operationHorizon: [1, 4],
    observationBurden: 'one exposed interface',
    coupledConstraints: 1,
  },
  {
    id: 'D2',
    name: 'Assembly',
    nameZh: '装配体级',
    intent: 'Several subassemblies with one primary mechanism and local occlusion.',
    typicalParts: [35, 85],
    typicalModules: [4, 8],
    typicalJoints: [3, 7],
    operationHorizon: [4, 8],
    observationBurden: 'two to three interacting interfaces',
    coupledConstraints: 3,
  },
  {
    id: 'D3',
    name: 'Mechanism',
    nameZh: '机构级',
    intent: 'Articulated whole objects with service access, dynamics, and hidden faults.',
    typicalParts: [40, 150],
    typicalModules: [3, 11],
    typicalJoints: [3, 10],
    operationHorizon: [6, 12],
    observationBurden: 'multi-view articulated object',
    coupledConstraints: 6,
  },
  {
    id: 'D4',
    name: 'System',
    nameZh: '系统级',
    intent: 'Coupled stations, shared resources, long horizons, and cross-zone failures.',
    typicalParts: [160, 320],
    typicalModules: [10, 20],
    typicalJoints: [9, 18],
    operationHorizon: [12, 24],
    observationBurden: 'large scene with hidden and distributed interfaces',
    coupledConstraints: 10,
  },
];

export const TASK_LAYERS: Array<{
  id: TaskLayer;
  name: string;
  nameZh: string;
  intent: string;
}> = [
  {
    id: 'atomic',
    name: 'Atomic operation',
    nameZh: '原子能力单选',
    intent: 'Isolate one perception, relation, edit, or local validation operation.',
  },
  {
    id: 'metacognitive',
    name: 'Metacognitive and physical reasoning',
    nameZh: '元认知与物理推理',
    intent: 'Reason about support, dynamics, uncertainty, information, and trade-offs.',
  },
  {
    id: 'procedural',
    name: 'Executable operation',
    nameZh: '可执行操作题',
    intent: 'Return an ordered, state-valid sequence rather than a final-state guess.',
  },
  {
    id: 'integrative',
    name: 'Integrated system challenge',
    nameZh: '综合复杂题',
    intent: 'Jointly solve diagnosis, inspection, resources, safety, and verification.',
  },
];

export const ATOMIC_OPERATIONS = [
  'module-identification',
  'part-count',
  'color-recognition',
  'spatial-relation',
  'joint-motion',
  'connectivity',
  'support-anchor',
  'contact-count',
  'recolor',
  'add',
  'remove',
  'replace',
  'pose-correction',
  'fault-localization',
  'next-step',
  'inventory-check',
  'subassembly-boundary',
  'no-op-detection',
] as const;

export const META_FAMILIES = [
  'prefix-stability',
  'assembly-accessibility',
  'support-counterfactual',
  'dynamic-robustness',
  'functional-kinematics',
  'fault-diagnosis',
  'active-inspection',
  'uncertainty-calibration',
  'multiobjective-tradeoff',
] as const;
