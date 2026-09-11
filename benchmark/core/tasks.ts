import { createHash } from 'node:crypto';
import type { Brick, Fault, InventoryItem, TaskSummary } from '../shared/types';
import { bom, compileBlueprint, validateWorld } from './world';

export interface Task {
  id: string;
  seed: number;
  variant: 0 | 1;
  fault: Fault;
  target: Brick[];
  hiddenIds: string[];
  coverId: string;
  inventory: InventoryItem[];
}
export function makeTask(seed: number, variant: 0 | 1, fault: Fault): Task {
  const hash = createHash('sha256').update(`care-mini-1:${seed}:${variant}:${fault}`).digest('hex');
  const labels = Array.from({ length: 8 }, (_, i) => `p${(i * 3 + seed % 8) % 8 + 1}`);
  const wall = seed % 2 ? 'red' : 'green';
  const lid = seed % 2 ? 'yellow' : 'white';
  const specs: Omit<Brick, 'id'>[] = [
    { partId: '3958', color: 'gray', x: 0, y: 0, z: 0, turn: 0 },
    { partId: '3009', color: wall, x: 0, y: 1, z: 0, turn: 0 },
    { partId: '3009', color: wall, x: 0, y: 1, z: 5, turn: 0 },
    { partId: '3010', color: wall, x: 0, y: 1, z: 1, turn: 1 },
    { partId: '3010', color: wall, x: 5, y: 1, z: 1, turn: 1 },
    { partId: '3010', color: 'blue', x: 1, y: 1, z: 1, turn: variant },
    { partId: '3010', color: 'blue', x: variant ? 3 : 1, y: 1, z: variant ? 1 : 3, turn: variant },
    { partId: '3958', color: lid, x: 0, y: 4, z: 0, turn: 0 },
  ];
  const target = specs.map((p, i) => ({ ...p, id: labels[i] }));
  const inventory = bom([...target,
    { ...target[5], id: 'distractor-1', partId: '3004' },
    { ...target[5], id: 'distractor-2', partId: '3005', color: 'yellow' },
  ]);
  if (validateWorld(target) || !compileBlueprint({ version: 1, parts: target }, inventory).ok) {
    throw new Error('Task certification failed');
  }
  return {
    id: hash.slice(0, 16), seed, variant, fault, target,
    hiddenIds: [labels[5], labels[6]], coverId: labels[7], inventory,
  };
}

export const PILOT_SPEC = [
  { seed: 41, variant: 0 as const, fault: 'none' as const },
  { seed: 41, variant: 1 as const, fault: 'none' as const },
  { seed: 42, variant: 0 as const, fault: 'missing' as const },
  { seed: 42, variant: 1 as const, fault: 'offset' as const },
];

export function pilotTasks() {
  return PILOT_SPEC.map(s => makeTask(s.seed, s.variant, s.fault));
}

export function taskSummary(task: Task, index: number): TaskSummary {
  return { id: task.id, title: `密封结构 ${String(index + 1).padStart(2, '0')}`,
    family: 'sealed-box', parts: task.target.length, split: 'public-pilot' };
}
