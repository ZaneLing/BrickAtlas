export type Vec3 = [number, number, number];
export type Bounds = { min: Vec3; max: Vec3 };
export type GroupId = 'body' | 'chassis' | 'wheels' | 'cockpit' | 'front' | 'rear';

export interface PartInstance {
  instanceId: string;
  index: number;
  partNumber: string;
  displayName: string;
  colorCode: string;
  colorName: string;
  colorHex: string;
  sourceFile: string;
  sourceLine: number;
  parentSubmodelId: string;
  path: string[];
  buildStep: number | null;
  originalMatrix: number[];
  bounds: Bounds;
  category: string;
  tags: string[];
  groupId: GroupId;
}

export interface MaterialRecord {
  color: string;
  opacity: number;
  roughness: number;
  metalness: number;
}

export interface GeometryBucket {
  kind: 'mesh' | 'line' | 'conditional';
  material: MaterialRecord;
  attributes: Record<string, { offset: number; count: number; itemSize: number }>;
}

export interface GeometryChunk {
  groupId: GroupId;
  url: string;
  bytes: number;
  sha256: string;
  buckets: GeometryBucket[];
}

export interface AtlasManifest {
  version: 1;
  model: {
    id: string;
    title: string;
    author: string;
    sourceUrl: string;
    license: string;
    year: number;
    notes: string[];
  };
  sourceHash: string;
  instances: PartInstance[];
  submodels: { id: string; name: string; parentId: string | null; sourceFile: string }[];
  groups: { id: GroupId; name: string; color: string; direction: Vec3; instanceIds: string[] }[];
  bounds: Bounds;
  chunks: GeometryChunk[];
  stats: { instances: number; uniqueParts: number; colors: number; triangles: number; compressedBytes: number };
  instructions?: InstructionPlan;
}

export interface AssemblyStep {
  id: string;
  title: string;
  sourceFile: string;
  sourceStep: number | null;
  instanceIds: string[];
}
export interface InstructionPlan {
  provenance: 'source' | 'editorial';
  disclaimer: string;
  steps: AssemblyStep[];
}

export interface ExplorerState {
  hiddenGroups: GroupId[];
  hiddenBrickIds: string[];
  selection: string[];
  highlightedBrickIds: string[];
  isolation: string[] | null;
  explosion: number;
  autoRotate: boolean;
  edges: boolean;
  quality: 'auto' | 'high' | 'ultra' | 'low';
  view: 'perspective' | 'front' | 'side' | 'rear' | 'top';
  revision: number;
  buildStep: number | null;
  highlightStep: boolean;
  grid: boolean;
  background: 'studio' | 'white' | 'dark';
  assemblyRevision: number;
  xray: boolean;
}

export const initialState: ExplorerState = {
  hiddenGroups: [], hiddenBrickIds: [], selection: [], highlightedBrickIds: [], isolation: null, explosion: 0,
  autoRotate: false, edges: true, quality: 'auto', view: 'perspective', revision: 0,
  buildStep: null, highlightStep: true, grid: true, background: 'studio', assemblyRevision: 0, xray: false,
};

export const colorLabels: Record<string, string> = {
  '0': '黑色', '4': '红色', '15': '白色', '19': '棕褐色', '36': '透明红色',
  '47': '透明玻璃', '57': '透明橙色', '71': '浅灰色', '72': '深灰色',
  '73': '中蓝色', '135': '珍珠浅灰色', '256': '黑色橡胶',
};

export function visibleInstances(manifest: AtlasManifest, state: ExplorerState) {
  const isolated = state.isolation ? new Set(state.isolation) : null;
  const built = state.buildStep === null || !manifest.instructions ? null
    : new Set(manifest.instructions.steps.slice(0, state.buildStep).flatMap(s => s.instanceIds));
  const hidden = new Set(state.hiddenBrickIds);
  return manifest.instances.filter(p => !state.hiddenGroups.includes(p.groupId) && !hidden.has(p.instanceId) && (!isolated || isolated.has(p.instanceId)) && (!built || built.has(p.instanceId)));
}

export function searchInstances(manifest: AtlasManifest, query: string) {
  const terms = query.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
  return manifest.instances.filter(p => {
    const group = manifest.groups.find(g => g.id === p.groupId)!;
    const text = [p.partNumber, p.displayName, p.colorName, colorLabels[p.colorCode], p.colorCode, p.category, ...p.path, ...p.tags, group.name].join(' ').toLocaleLowerCase();
    return terms.every(term => text.includes(term));
  });
}
