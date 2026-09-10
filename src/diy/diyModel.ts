import { brickPalette } from '../creator/imageBrickModel';

export type Turn = 0 | 1 | 2 | 3;
export type DiyTool = 'place' | 'orbit' | 'pan' | 'erase' | 'paint';
export interface DiyPart {
  id: string;
  nameZh: string;
  nameEn: string;
  width: number;
  depth: number;
  height: number;
  shape: 'brick' | 'plate' | 'tile' | 'round' | 'slope';
}
// X/Z are stud cells; Y is a plate layer (3.2 mm). No board-edge constraint.
export interface DiyBrick {
  id: string;
  partId: string;
  color: string;
  x: number;
  y: number;
  z: number;
  turn: Turn;
  stampId: string;
}
export interface DiyProject {
  version: 1;
  name: string;
  bricks: DiyBrick[];
}
export interface DiyRecipe {
  id: string;
  nameZh: string;
  nameEn: string;
  parts: { partId: string; x: number; y: number; z: number; turn?: Turn }[];
}
export interface DiyBrush { recipeId: string; color: string; turn: Turn }
export type PlacementIssue = 'overlap' | 'unsupported' | 'limit' | null;
export const DIY_LIMIT = 5000;
export const PLATE_HEIGHT = 0.4;
export const diyParts: DiyPart[] = [
  { id: '3005', nameZh: '基础砖 1×1', nameEn: 'Brick 1×1', width: 1, depth: 1, height: 3, shape: 'brick' },
  { id: '3004', nameZh: '基础砖 1×2', nameEn: 'Brick 1×2', width: 2, depth: 1, height: 3, shape: 'brick' },
  { id: '3622', nameZh: '基础砖 1×3', nameEn: 'Brick 1×3', width: 3, depth: 1, height: 3, shape: 'brick' },
  { id: '3010', nameZh: '基础砖 1×4', nameEn: 'Brick 1×4', width: 4, depth: 1, height: 3, shape: 'brick' },
  { id: '3003', nameZh: '基础砖 2×2', nameEn: 'Brick 2×2', width: 2, depth: 2, height: 3, shape: 'brick' },
  { id: '3001', nameZh: '基础砖 2×4', nameEn: 'Brick 2×4', width: 4, depth: 2, height: 3, shape: 'brick' },
  { id: '2456', nameZh: '基础砖 2×6', nameEn: 'Brick 2×6', width: 6, depth: 2, height: 3, shape: 'brick' },
  { id: '3024', nameZh: '薄板 1×1', nameEn: 'Plate 1×1', width: 1, depth: 1, height: 1, shape: 'plate' },
  { id: '3023', nameZh: '薄板 1×2', nameEn: 'Plate 1×2', width: 2, depth: 1, height: 1, shape: 'plate' },
  { id: '3022', nameZh: '薄板 2×2', nameEn: 'Plate 2×2', width: 2, depth: 2, height: 1, shape: 'plate' },
  { id: '3020', nameZh: '薄板 2×4', nameEn: 'Plate 2×4', width: 4, depth: 2, height: 1, shape: 'plate' },
  { id: '3031', nameZh: '薄板 4×4', nameEn: 'Plate 4×4', width: 4, depth: 4, height: 1, shape: 'plate' },
  { id: '3069b', nameZh: '光面砖 1×2', nameEn: 'Tile 1×2', width: 2, depth: 1, height: 1, shape: 'tile' },
  { id: '3068b', nameZh: '光面砖 2×2', nameEn: 'Tile 2×2', width: 2, depth: 2, height: 1, shape: 'tile' },
  { id: '3062b', nameZh: '圆砖 1×1', nameEn: 'Round brick 1×1', width: 1, depth: 1, height: 3, shape: 'round' },
  { id: '3039', nameZh: '斜坡砖 2×2', nameEn: 'Slope 2×2', width: 2, depth: 2, height: 3, shape: 'slope' },
];
export const partById = new Map(diyParts.map(part => [part.id, part]));
export const diyRecipes: DiyRecipe[] = [
  ...diyParts.map(part => ({ id: part.id, nameZh: part.nameZh, nameEn: part.nameEn, parts: [{ partId: part.id, x: 0, y: 0, z: 0 }] })),
  { id: 'table', nameZh: '小桌子', nameEn: 'Table', parts: [
    { partId: '3005', x: 0, y: 0, z: 0 }, { partId: '3005', x: 3, y: 0, z: 0 },
    { partId: '3005', x: 0, y: 0, z: 3 }, { partId: '3005', x: 3, y: 0, z: 3 },
    { partId: '3031', x: 0, y: 3, z: 0 },
  ] },
  { id: 'gateway', nameZh: '小门廊', nameEn: 'Gateway', parts: [
    { partId: '3003', x: 0, y: 0, z: 0 }, { partId: '3003', x: 4, y: 0, z: 0 },
    { partId: '3003', x: 0, y: 3, z: 0 }, { partId: '3003', x: 4, y: 3, z: 0 },
    { partId: '2456', x: 0, y: 6, z: 0 },
  ] },
  { id: 'steps', nameZh: '小台阶', nameEn: 'Staircase', parts: [
    { partId: '2456', x: 0, y: 0, z: 0 },
    { partId: '3001', x: 2, y: 3, z: 0 },
    { partId: '3003', x: 4, y: 6, z: 0 },
  ] },
  { id: 'bench', nameZh: '长椅', nameEn: 'Bench', parts: [
    { partId: '3003', x: 0, y: 0, z: 0 }, { partId: '3003', x: 4, y: 0, z: 0 },
    { partId: '2456', x: 0, y: 3, z: 0 },
    { partId: '3010', x: 1, y: 6, z: 0 },
  ] },
];
export const recipeById = new Map(diyRecipes.map(recipe => [recipe.id, recipe]));

export function footprint(brick: Pick<DiyBrick, 'partId' | 'turn'>) {
  const part = partById.get(brick.partId)!;
  return brick.turn % 2 ? { width: part.depth, depth: part.width } : { width: part.width, depth: part.depth };
}

export function stamp(brush: DiyBrush, x: number, y: number, z: number, stampId = 'preview'): DiyBrick[] {
  const recipe = recipeById.get(brush.recipeId)!;
  const rotated = recipe.parts.map((part, index) => {
    const turn = part.turn ?? 0;
    const size = footprint({ partId: part.partId, turn });
    let px = part.x, pz = part.z, w = size.width, d = size.depth;
    for (let i = 0; i < brush.turn; i++) {
      [px, pz, w, d] = [pz, -px - w, d, w];
    }
    return { id: `${stampId}_${index}`, stampId, partId: part.partId, color: brush.color, x: px, y: part.y, z: pz, turn: ((turn + brush.turn) % 4) as Turn };
  });
  const minX = Math.min(...rotated.map(part => part.x)), minZ = Math.min(...rotated.map(part => part.z));
  return rotated.map(part => ({ ...part, x: part.x - minX + x, y: part.y + y, z: part.z - minZ + z }));
}

export function stampSize(brush: DiyBrush) {
  const parts = stamp(brush, 0, 0, 0);
  return {
    width: Math.max(...parts.map(part => part.x + footprint(part).width)),
    depth: Math.max(...parts.map(part => part.z + footprint(part).depth)),
    height: Math.max(...parts.map(part => part.y + partById.get(part.partId)!.height)),
  };
}

function cells(brick: DiyBrick, visit: (x: number, z: number) => void) {
  const size = footprint(brick);
  for (let x = brick.x; x < brick.x + size.width; x++) for (let z = brick.z; z < brick.z + size.depth; z++) visit(x, z);
}

function topStudAt(brick: DiyBrick, x: number, z: number) {
  const part = partById.get(brick.partId)!;
  if (part.shape === 'tile') return false;
  if (part.shape !== 'slope') return true;
  const size = footprint(brick);
  const dx = x - brick.x, dz = z - brick.z;
  return [dz === 0, dx === 0, dz === size.depth - 1, dx === size.width - 1][brick.turn];
}

export class DiyIndex {
  private readonly columns = new Map<string, DiyBrick[]>();
  constructor(bricks: readonly DiyBrick[]) { bricks.forEach(brick => this.add(brick)); }
  add(brick: DiyBrick) {
    cells(brick, (x, z) => {
      const key = `${x}:${z}`;
      const column = this.columns.get(key) ?? [];
      column.push(brick);
      this.columns.set(key, column);
    });
  }
  validate(candidates: DiyBrick[], count: number): PlacementIssue {
    if (count + candidates.length > DIY_LIMIT) return 'limit';
    const added = new DiyIndex([]);
    for (const brick of [...candidates].sort((a, b) => a.y - b.y)) {
      if (!validBrick(brick)) return 'limit';
      let overlap = false, supported = brick.y === 0;
      const top = brick.y + partById.get(brick.partId)!.height;
      cells(brick, (x, z) => {
        const nearby = [...(this.columns.get(`${x}:${z}`) ?? []), ...(added.columns.get(`${x}:${z}`) ?? [])];
        for (const below of nearby) {
          const belowTop = below.y + partById.get(below.partId)!.height;
          if (brick.y < belowTop && top > below.y) overlap = true;
          if (belowTop === brick.y && topStudAt(below, x, z)) supported = true;
        }
      });
      if (overlap) return 'overlap';
      if (!supported) return 'unsupported';
      added.add(brick);
    }
    return null;
  }
}

export function canRemove(bricks: DiyBrick[], id: string) {
  const remaining = bricks.filter(brick => brick.id !== id);
  return !new DiyIndex([]).validate(remaining, 0);
}

function validBrick(brick: DiyBrick) {
  return brick && typeof brick.id === 'string' && brick.id.length <= 100
    && typeof brick.stampId === 'string' && brick.stampId.length <= 100
    && partById.has(brick.partId) && brickPalette.some(color => color.id === brick.color)
    && [0, 1, 2, 3].includes(brick.turn)
    && [brick.x, brick.z].every(n => Number.isInteger(n) && Math.abs(n) <= 1_000_000)
    && Number.isInteger(brick.y) && brick.y >= 0 && brick.y <= 3000;
}
export function emptyDiyProject(): DiyProject { return { version: 1, name: 'My DIY Studio', bricks: [] }; }

export function parseDiyProject(text: string): DiyProject {
  if (text.length > 4_000_000) throw new Error('Project file is too large');
  const value = JSON.parse(text) as DiyProject;
  if (!value || value.version !== 1 || typeof value.name !== 'string' || value.name.length > 100
    || !Array.isArray(value.bricks) || value.bricks.length > DIY_LIMIT
    || !value.bricks.every(validBrick)
    || new Set(value.bricks.map(brick => brick.id)).size !== value.bricks.length
    || new DiyIndex([]).validate(value.bricks, 0)) throw new Error('Invalid DIY project');
  return value;
}

export interface DiyHistory { past: DiyProject[]; present: DiyProject; future: DiyProject[] }
export function commitDiy(history: DiyHistory, project: DiyProject): DiyHistory {
  return { past: [...history.past.slice(-49), history.present], present: project, future: [] };
}
export function undoDiy(history: DiyHistory): DiyHistory {
  const previous = history.past.at(-1);
  return previous ? { past: history.past.slice(0, -1), present: previous, future: [history.present, ...history.future] } : history;
}
export function redoDiy(history: DiyHistory): DiyHistory {
  const next = history.future[0];
  return next ? { past: [...history.past, history.present], present: next, future: history.future.slice(1) } : history;
}

export function diyBom(project: DiyProject) {
  const result = new Map<string, { partId: string; color: string; count: number }>();
  for (const brick of project.bricks) {
    const key = `${brick.partId}:${brick.color}`;
    const row = result.get(key) ?? { partId: brick.partId, color: brick.color, count: 0 };
    row.count++;
    result.set(key, row);
  }
  return [...result.values()].sort((a, b) => b.count - a.count);
}

export function diyToLdraw(project: DiyProject) {
  const rotation = ['1 0 0 0 1 0 0 0 1', '0 0 -1 0 1 0 1 0 0', '-1 0 0 0 1 0 0 0 -1', '0 0 1 0 1 0 -1 0 0'];
  const lines = [`0 ${project.name.replace(/[\r\n]/g, ' ')}`, '0 Brick Atlas DIY', '0 Virtual ground is not included in the inventory'];
  let previous = '';
  for (const brick of project.bricks) {
    const part = partById.get(brick.partId)!;
    const size = footprint(brick);
    if (previous && previous !== brick.stampId) lines.push('0 STEP');
    previous = brick.stampId;
    lines.push(`1 ${brickPalette.find(color => color.id === brick.color)!.code} ${(brick.x + size.width / 2) * 20} ${-(brick.y + part.height) * 8} ${-(brick.z + size.depth / 2) * 20} ${rotation[brick.turn]} ${part.id}.dat`);
  }
  return `${lines.join('\n')}\n`;
}
