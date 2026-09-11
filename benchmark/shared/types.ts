export type Turn = 0 | 1 | 2 | 3;
export type View = 'iso' | 'top' | 'front' | 'back';
export type Phase = 'inspect' | 'build' | 'done';
export type Protocol = 'active' | 'passive';
export type Fault = 'none' | 'missing' | 'offset';
export interface Brick {
  id: string;
  partId: string;
  color: string;
  x: number;
  y: number;
  z: number;
  turn: Turn;
}
export interface Blueprint {
  version: 1;
  parts: Brick[];
}
export interface InventoryItem {
  partId: string;
  color: string;
  count: number;
}
export interface Scene {
  parts: Brick[];
  view: View;
}
export interface VisibleHandle {
  id: string;
  partId: string;
  color: string;
}
export interface Observation {
  phase: Phase;
  protocol: Protocol;
  view: View;
  visible: VisibleHandle[];
  inventory: InventoryItem[];
  blueprint: Blueprint | null;
  feedback: string;
  remainingActions: number;
  imageUrl?: string;
}
export type Action =
  | { type: 'look'; view: View }
  | { type: 'detach'; id: string; predict?: { newlyVisible: number; components: number } }
  | { type: 'blueprint'; blueprint: Blueprint }
  | { type: 'place'; part: Omit<Brick, 'id'> }
  | { type: 'build'; parts: Omit<Brick, 'id'>[] }
  | { type: 'finish' };
export interface Score {
  exact: boolean;
  partF1: number;
  edgeF1: number;
  matched: number;
  expected: number;
  extra: number;
  missing: number;
  valid: boolean;
}
export interface EpisodeScore {
  anatomy: Score;
  construction: Score;
  blueprintExecutable: boolean;
  lifecycleSuccess: boolean;
  causalAccuracy: number | null;
  causalAttempts: number;
  actions: number;
  primitiveActions: number;
  invalidActions: number;
  inspectionRemovals: number;
  recoverySuccess: boolean | null;
  faultTriggered: boolean;
  faultEligible: boolean;
  postFaultActions: number;
}
export interface TaskSummary {
  id: string;
  title: string;
  family: string;
  parts: number;
  split: 'public-pilot';
}
