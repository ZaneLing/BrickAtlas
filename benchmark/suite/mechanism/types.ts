export type Vec3 = [number, number, number];
export type Quat = [number, number, number, number];
export type ShapeKind =
  | 'brick'
  | 'plate'
  | 'beam'
  | 'panel'
  | 'slope'
  | 'arch'
  | 'window'
  | 'cylinder'
  | 'wheel'
  | 'axle'
  | 'gear'
  | 'sphere';

export interface MechanismPart {
  id: string;
  moduleId: string;
  shape: ShapeKind;
  size: Vec3;
  position: Vec3;
  rotation: Quat;
  color: string;
}

export interface MechanismModule {
  id: string;
  name: string;
  role: string;
  anchored: boolean;
  mass: number;
  position: Vec3;
  rotation: Quat;
}

export interface MechanismJoint {
  id: string;
  name: string;
  type: 'fixed' | 'revolute' | 'prismatic' | 'spring';
  parent: string;
  child: string;
  anchorParent: Vec3;
  anchorChild: Vec3;
  axis?: Vec3;
  limits?: [number, number];
  restLength?: number;
  stiffness?: number;
  damping?: number;
}

export interface AccessPath {
  id: string;
  label: string;
  start: Vec3;
  end: Vec3;
  halfExtents: Vec3;
}

export interface InventoryAlternative {
  id: string;
  label: string;
  pieces: number;
  cost: number;
  mass: number;
  stiffness: number;
  jointMode: 'fixed' | 'spring' | 'none';
}

export interface InspectionQuery {
  id: string;
  label: string;
  cost: number;
  returns: Record<string, string>;
}

export interface MechanismModel {
  id: string;
  name: string;
  nameZh: string;
  domain: string;
  description: string;
  originalDesign: true;
  modules: MechanismModule[];
  parts: MechanismPart[];
  joints: MechanismJoint[];
  assemblyOrder: string[];
  taskConfig: {
    serviceModule: string;
    accessPaths: AccessPath[];
    functionalJoint: string;
    functionalTarget: number;
    loadModule: string;
    impulseCandidates: number[];
    robustnessLimits: { maxTransientDisplacement: number; maxResidualDisplacement: number };
    faultJoint: string;
    recoveryActions: string[];
    inventoryAlternatives: InventoryAlternative[];
    inventoryRequirements: { maxCost: number; maxPieces: number; minStiffness: number };
    hiddenWorlds: string[];
    inspectionQueries: InspectionQuery[];
  };
}

export type MechanismTaskKind =
  | 'prefix-dynamics'
  | 'insertion-access'
  | 'fault-recovery'
  | 'inventory-substitution'
  | 'dynamic-robustness'
  | 'functional-kinematics'
  | 'active-inspection'
  | 'multiobjective-design';

export interface MechanismTask {
  id: string;
  sourceGroup: string;
  kind: MechanismTaskKind;
  capability: string[];
  question: string;
  input: Record<string, unknown>;
  oracle: Record<string, unknown>;
  visualization: {
    modelImage: string;
    detailImage: string;
    highlightModules: string[];
    view: 'iso' | 'front' | 'side' | 'top';
  };
}

export const IDENTITY_QUAT: Quat = [0, 0, 0, 1];
