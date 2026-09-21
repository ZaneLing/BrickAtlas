import type { LDrawBundle, LDrawTask } from '../../../src/benchmark/ldrawTypes';

export type V2Task = Omit<LDrawTask, 'format' | 'layer'> & {
  format: LDrawTask['format'] | 'integer';
  layer: Exclude<LDrawTask['layer'], 'integrative'> | 'graph-internal';
  numericDomain?: { min: number; max: number };
};
export type InternalBundle = Omit<LDrawBundle, 'version' | 'tasks'> & {
  version: 'brickatlas-ldraw-2';
  role: 'internal-scoring-review';
  tasks: V2Task[];
};
export type PublicTask = Pick<V2Task, 'id' | 'modelId' | 'family' | 'modality' | 'format' | 'promptEn'> & {
  input: Record<string, any>;
  options?: { id: string; label: string }[];
  visualInput?: { numberedView: string; isolationAllowed: true };
};
export interface PublicBundle {
  version: 'brickatlas-ldraw-2';
  role: 'model-input';
  modelId: string;
  sourceHash: string;
  tasks: PublicTask[];
}
export type Condition = 'standard' | 'text-without-image' | 'graph-edges-withheld'
  | 'full-scene' | 'background-mask' | 'operand-only' | 'choice-order' | 'edge-order' | 'id-permutation'
  | 'wrong-image' | 'camera-perturbation' | 'color-nuisance' | 'multi-view' | 'graph-intervention';
export interface ModelRequest {
  messages: Array<{ role: 'system' | 'user'; content: string | Array<
    { type: 'text'; text: string } | { type: 'image_url'; image_url: { url: string } }
  > }>;
}
