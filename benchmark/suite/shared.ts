export const VERSION = 'brickatlas-multitask-1.0';
export const TASKS = ['parts', 'relations', 'reconstruct', 'generate', 'complete', 'edit', 'plan', 'repair'] as const;
export type Kind = typeof TASKS[number];
export const LABELS: Record<Kind, string> = {
  parts: '零件与接口', relations: '空间与连接', reconstruct: '多视图重建',
  generate: '条件生成', complete: '结构补全', edit: '指令编辑', plan: '装拆规划', repair: '错误修复',
};
export type Split = 'train' | 'validation' | 'test_id' | 'test_ood';
export type Mode = 'one-shot' | 'validator-once';
export type View = 'iso' | 'top' | 'front' | 'side';
export type Color = 'red' | 'blue' | 'green' | 'yellow' | 'gray' | 'white';
export const COLORS: Record<Color, string> = {
  red: '#bd3028', blue: '#176cb3', green: '#368061', yellow: '#e8bc31', gray: '#95a2ac', white: '#eef0ef',
};
export const CATALOG: Record<string, { name: string; w: number; d: number; h: number }> = {
  '3005': { name: 'Brick 1x1', w: 1, d: 1, h: 3 },
  '3004': { name: 'Brick 1x2', w: 2, d: 1, h: 3 },
  '3622': { name: 'Brick 1x3', w: 3, d: 1, h: 3 },
  '3010': { name: 'Brick 1x4', w: 4, d: 1, h: 3 },
  '3009': { name: 'Brick 1x6', w: 6, d: 1, h: 3 },
  '3008': { name: 'Brick 1x8', w: 8, d: 1, h: 3 },
  '3003': { name: 'Brick 2x2', w: 2, d: 2, h: 3 },
  '3002': { name: 'Brick 2x3', w: 3, d: 2, h: 3 },
  '3001': { name: 'Brick 2x4', w: 4, d: 2, h: 3 },
  '2456': { name: 'Brick 2x6', w: 6, d: 2, h: 3 },
  '3007': { name: 'Brick 2x8', w: 8, d: 2, h: 3 },
  '3024': { name: 'Plate 1x1', w: 1, d: 1, h: 1 },
  '3023': { name: 'Plate 1x2', w: 2, d: 1, h: 1 },
  '3623': { name: 'Plate 1x3', w: 3, d: 1, h: 1 },
  '3710': { name: 'Plate 1x4', w: 4, d: 1, h: 1 },
  '3666': { name: 'Plate 1x6', w: 6, d: 1, h: 1 },
  '3460': { name: 'Plate 1x8', w: 8, d: 1, h: 1 },
  '3022': { name: 'Plate 2x2', w: 2, d: 2, h: 1 },
  '3021': { name: 'Plate 2x3', w: 3, d: 2, h: 1 },
  '3020': { name: 'Plate 2x4', w: 4, d: 2, h: 1 },
  '3795': { name: 'Plate 2x6', w: 6, d: 2, h: 1 },
  '3034': { name: 'Plate 2x8', w: 8, d: 2, h: 1 },
  '3031': { name: 'Plate 4x4', w: 4, d: 4, h: 1 },
  '3032': { name: 'Plate 4x6', w: 6, d: 4, h: 1 },
  '3035': { name: 'Plate 4x8', w: 8, d: 4, h: 1 },
};
export interface Part { id: string; partId: string; color: Color; x: number; y: number; z: number; turn: number }
export interface Structure { version: 1; parts: Part[] }
export interface RelativeNode {
  id: string; partId: string; color: Color; parent: string | null;
  offset: [number, number, number]; turn: number;
}
export interface Edge { a: string; b: string; studs: number }
export interface FrameSpec { parts: Part[]; view: View; layer: number | null; title: string }
export interface PublicTask {
  id: string; kind: Kind; split: Split; family: string;
  prompt: string; input: Record<string, unknown>; responseSchema: Record<string, unknown>;
  imageTitles: string[]; images?: string[];
}
export interface Metrics {
  format: number; success: number; valid: number;
  [key: string]: number | null;
}
export interface Verdict { metrics: Metrics; issues: string[] }
export interface SampleSummary { id: string; group: string; family: string; split: Split; parts: number; description: string }
export interface DatasetSummary {
  version: string; digest: string; models: number; groups: number; tasks: number;
  families: Record<string, number>; splits: Record<string, number>; catalogParts: number;
}
export const RULES = `BrickAtlas grid-v1: x,z use studs (8 mm), y uses plate heights (3.2 mm).
Part position is the MINIMUM x,z corner and BOTTOM y. turn is 0,1,2,3 quarter-turns:
odd turns swap catalog w,d; 180-degree symmetric bricks have equal footprints.
All bricks/plates are opaque rectangular bodies with top studs and bottom sockets.
Only integer coordinates 0..24 and at most 64 pieces; bodies must fit within [0,32]^3.
No overlap. Every elevated part needs at least one directly supporting stud below it.
Only vertical +Y removal and -Y insertion are allowed in plan tasks; overhead overlap blocks passage.
This is discrete geometry/connectivity, NOT force, stability or robot-control simulation.
Program output: {"version":1,"parts":[{"id":"p1","partId":"3005","color":"red","x":0,"y":0,"z":0,"turn":0}]}.
Alternative reversible output: {"version":1,"nodes":[{"id":"p1","partId":"3005","color":"red",
"parent":null,"offset":[0,0,0],"turn":0}, ...]}.
Relative offsets are in GLOBAL grid axes from parent's minimum corner; turn remains absolute.
Parents must occur earlier. This relative program is not a guarantee of a stud attachment.
Return exactly one JSON object; no markdown or chain of thought.`;
