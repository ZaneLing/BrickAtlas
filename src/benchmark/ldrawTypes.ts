import type { Task } from './types';
import type { AtlasManifest, PartInstance } from '../model/types';

export interface NumberedPart {
  id: string;
  label: string;
  partNumber: string;
  name: string;
  color: string;
  colorCode: string;
  sourceFile: string;
  sourceLine: number;
  submodelId: string;
}
export interface LDrawTask extends Task {
  references: Array<Pick<NumberedPart, 'id' | 'label'>>;
  promptEn: string;
  evidenceDetail: string;
  modality: 'visual' | 'source-data' | 'connector-graph' | 'scene-edit';
  visualInput?: { numberedView: string; isolationAllowed: true };
}
export interface LDrawEntry {
  id: string;
  sourceModelId: string;
  name: string;
  nameZh: string;
  difficulty: string;
  parts: number;
  modules: number;
  tasks: number;
  sourceUrl: string;
  author: string;
  license: string;
  sourceHash: string;
  setNumber: string;
  connectorCoverage: number;
  intersectionCandidates: number;
  sourceSteps: number;
}
export interface ConnectorEdge {
  a: string; b: string; family: string; aConnector: number; bConnector: number;
  yawOrSlide: number; flip: boolean; rotation: number[];
}
export interface LDrawAudit {
  manifestSha256: string;
  connectorCoverage: number;
  unsupported: Array<{ instanceId: string; partNumber: string }>;
  edges: ConnectorEdge[];
  components: string[][];
  componentSizes: number[];
  duplicatePlacements: number;
  collisionStatus: string;
  collisionPairs: string[][];
  nonFixedCollisionPairs: string[][];
  nonMatingCollisionPairs: string[][];
  graphPoseNormalizationMax: number;
  sourceGeometryModified: false;
  scope: string;
}
export interface LDrawBundle {
  version: 'brickatlas-ldraw-1';
  entry: LDrawEntry;
  tasks: LDrawTask[];
  parts: NumberedPart[];
  audit: LDrawAudit;
  instructions: AtlasManifest['instructions'];
}
export type PublicLDrawTask = Omit<LDrawTask, 'answer' | 'evidenceDetail'>;
export function publicTask(task: LDrawTask): PublicLDrawTask {
  const { answer: _answer, evidenceDetail: _detail, ...input } = task;
  return input;
}
export function numberedPart(part: PartInstance): NumberedPart {
  return { id: part.instanceId, label: `B${String(part.index + 1).padStart(4, '0')}`,
    partNumber: part.partNumber, name: part.displayName, color: part.colorName,
    colorCode: part.colorCode, sourceFile: part.sourceFile, sourceLine: part.sourceLine,
    submodelId: part.parentSubmodelId };
}
