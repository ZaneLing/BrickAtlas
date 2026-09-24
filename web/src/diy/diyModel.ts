import { brickPalette } from '../creator/imageBrickModel';

export type Turn = 0 | 1 | 2 | 3;
export type DiyTool = 'place' | 'orbit' | 'pan' | 'erase' | 'paint';
export type DiyCategory = 'basic' | 'plate' | 'tile' | 'slope' | 'round' | 'modified' | 'technic' | 'connector' | 'architecture' | 'motion';
export type DiyShape = 'brick' | 'plate' | 'tile' | 'round' | 'slope' | 'inverted-slope' | 'curved'
  | 'grille' | 'jumper' | 'side-stud' | 'technic' | 'beam' | 'pin' | 'axle'
  | 'clip' | 'bar' | 'cone' | 'panel' | 'arch' | 'fence' | 'wheel' | 'dish' | 'propeller' | 'turntable';
export interface DiyPart {
  id: string;
  nameZh: string;
  nameEn: string;
  category: DiyCategory;
  width: number;
  depth: number;
  height: number;
  shape: DiyShape;
  top: 'all' | 'none' | 'center' | 'rear';
  tags?: string[];
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
  parts: { partId: string; x: number; y: number; z: number; turn?: Turn; color?: string }[];
}
export interface DiyBrush { recipeId: string; color: string; turn: Turn }
export type PlacementIssue = 'overlap' | 'unsupported' | 'limit' | null;
export const DIY_LIMIT = 5000;
export const PLATE_HEIGHT = 0.4;
const part = (
  id: string, nameZh: string, nameEn: string, category: DiyCategory,
  width: number, depth: number, height: number, shape: DiyShape,
  top: DiyPart['top'] = 'all', tags?: string[],
): DiyPart => ({ id, nameZh, nameEn, category, width, depth, height, shape, top, tags });
export const diyParts: DiyPart[] = [
  part('3005', '基础砖 1×1', 'Brick 1×1', 'basic', 1, 1, 3, 'brick'),
  part('3004', '基础砖 1×2', 'Brick 1×2', 'basic', 2, 1, 3, 'brick'),
  part('3622', '基础砖 1×3', 'Brick 1×3', 'basic', 3, 1, 3, 'brick'),
  part('3010', '基础砖 1×4', 'Brick 1×4', 'basic', 4, 1, 3, 'brick'),
  part('3009', '基础砖 1×6', 'Brick 1×6', 'basic', 6, 1, 3, 'brick'),
  part('3008', '基础砖 1×8', 'Brick 1×8', 'basic', 8, 1, 3, 'brick'),
  part('3003', '基础砖 2×2', 'Brick 2×2', 'basic', 2, 2, 3, 'brick'),
  part('3002', '基础砖 2×3', 'Brick 2×3', 'basic', 3, 2, 3, 'brick'),
  part('3001', '基础砖 2×4', 'Brick 2×4', 'basic', 4, 2, 3, 'brick'),
  part('2456', '基础砖 2×6', 'Brick 2×6', 'basic', 6, 2, 3, 'brick'),
  part('3006', '基础砖 2×10', 'Brick 2×10', 'basic', 10, 2, 3, 'brick'),

  part('3024', '薄板 1×1', 'Plate 1×1', 'plate', 1, 1, 1, 'plate'),
  part('3023', '薄板 1×2', 'Plate 1×2', 'plate', 2, 1, 1, 'plate'),
  part('3710', '薄板 1×4', 'Plate 1×4', 'plate', 4, 1, 1, 'plate'),
  part('3666', '薄板 1×6', 'Plate 1×6', 'plate', 6, 1, 1, 'plate'),
  part('60479', '薄板 1×12', 'Plate 1×12', 'plate', 12, 1, 1, 'plate'),
  part('3022', '薄板 2×2', 'Plate 2×2', 'plate', 2, 2, 1, 'plate'),
  part('3021', '薄板 2×3', 'Plate 2×3', 'plate', 3, 2, 1, 'plate'),
  part('3020', '薄板 2×4', 'Plate 2×4', 'plate', 4, 2, 1, 'plate'),
  part('3795', '薄板 2×6', 'Plate 2×6', 'plate', 6, 2, 1, 'plate'),
  part('3031', '薄板 4×4', 'Plate 4×4', 'plate', 4, 4, 1, 'plate'),

  part('3070b', '光面砖 1×1', 'Tile 1×1', 'tile', 1, 1, 1, 'tile', 'none'),
  part('3069b', '光面砖 1×2', 'Tile 1×2', 'tile', 2, 1, 1, 'tile', 'none'),
  part('2431', '光面砖 1×4', 'Tile 1×4', 'tile', 4, 1, 1, 'tile', 'none'),
  part('6636', '光面砖 1×6', 'Tile 1×6', 'tile', 6, 1, 1, 'tile', 'none'),
  part('3068b', '光面砖 2×2', 'Tile 2×2', 'tile', 2, 2, 1, 'tile', 'none'),
  part('2412b', '格栅光面砖 1×2', 'Grille tile 1×2', 'tile', 2, 1, 1, 'grille', 'none', ['grille']),
  part('2877', '格栅砖 1×2', 'Grille brick 1×2', 'tile', 2, 1, 3, 'grille', 'none', ['vent']),

  part('3039', '45° 斜坡 2×2', 'Slope 45 2×2', 'slope', 2, 2, 3, 'slope', 'rear'),
  part('3040b', '45° 斜坡 1×2', 'Slope 45 1×2', 'slope', 2, 1, 3, 'slope', 'rear'),
  part('3665a', '倒斜坡 1×2', 'Inverted slope 1×2', 'slope', 2, 1, 3, 'inverted-slope'),
  part('3298', '33° 斜坡 2×3', 'Slope 33 2×3', 'slope', 3, 2, 3, 'slope', 'rear'),
  part('3037', '45° 斜坡 2×4', 'Slope 45 2×4', 'slope', 4, 2, 3, 'slope', 'rear'),
  part('4286', '33° 斜坡 1×3', 'Slope 33 1×3', 'slope', 3, 1, 3, 'slope', 'rear'),
  part('60477', '18° 低斜坡 1×4', 'Low slope 18 1×4', 'slope', 4, 1, 1, 'slope', 'rear'),
  part('11477', '曲面斜坡 1×2', 'Curved slope 1×2', 'slope', 2, 1, 2, 'curved', 'rear'),
  part('30165', '曲面顶砖 2×2', 'Curved top 2×2', 'slope', 2, 2, 3, 'curved', 'rear'),

  part('3062b', '圆砖 1×1', 'Round brick 1×1', 'round', 1, 1, 3, 'round'),
  part('3941', '圆砖 2×2', 'Round brick 2×2', 'round', 2, 2, 3, 'round'),
  part('3942c', '圆锥 2×2×2', 'Cone 2×2×2', 'round', 2, 2, 6, 'cone', 'center'),
  part('2654a', '圆盘 2×2', 'Dish 2×2', 'round', 2, 2, 1, 'dish', 'center'),

  part('3794b', '跳线板 1×2', 'Jumper plate 1×2', 'modified', 2, 1, 1, 'jumper', 'center'),
  part('87580', '跳线板 2×2', 'Jumper plate 2×2', 'modified', 2, 2, 1, 'jumper', 'center'),
  part('87087', '侧凸点砖 1×1', 'Side-stud brick 1×1', 'modified', 1, 1, 3, 'side-stud'),
  part('30414', '侧凸点砖 1×4', 'Side-stud brick 1×4', 'modified', 4, 1, 3, 'side-stud'),
  part('60478', '末端把手板 1×2', 'Handle plate 1×2', 'modified', 2, 1, 1, 'clip', 'all', ['handle']),
  part('4215b', '墙板 1×4×3', 'Panel 1×4×3', 'modified', 4, 1, 9, 'panel'),

  part('3700', 'Technic 孔砖 1×2', 'Technic brick 1×2', 'technic', 2, 1, 3, 'technic'),
  part('3701', 'Technic 孔砖 1×4', 'Technic brick 1×4', 'technic', 4, 1, 3, 'technic'),
  part('3702', 'Technic 孔砖 1×8', 'Technic brick 1×8', 'technic', 8, 1, 3, 'technic'),
  part('3703', 'Technic 孔砖 1×16', 'Technic brick 1×16', 'technic', 16, 1, 3, 'technic'),
  part('32000', 'Technic 双孔砖 1×2', 'Technic brick 1×2 two holes', 'technic', 2, 1, 3, 'technic'),
  part('32064b', 'Technic 轴孔砖 1×2', 'Technic axle-hole brick 1×2', 'technic', 2, 1, 3, 'technic'),
  part('60483', 'Technic 梁 2L', 'Technic liftarm 2L', 'technic', 2, 1, 1, 'beam', 'none'),
  part('32140', 'Technic 直角梁 2×4', 'Technic bent liftarm 2×4', 'technic', 4, 2, 1, 'beam', 'none'),
  part('32291', 'Technic 十字连接块', 'Technic cross block', 'technic', 2, 2, 2, 'technic', 'none'),

  part('2780', 'Technic 摩擦销', 'Technic friction pin', 'connector', 2, 1, 1, 'pin', 'none'),
  part('4274', 'Technic 半销', 'Technic half pin', 'connector', 1, 1, 1, 'pin', 'none'),
  part('3673', 'Technic 连接销', 'Technic pin', 'connector', 2, 1, 1, 'pin', 'none'),
  part('32062', 'Technic 轴 2L', 'Technic axle 2L', 'connector', 2, 1, 1, 'axle', 'none'),
  part('32123b', 'Technic 半衬套', 'Technic half bush', 'connector', 1, 1, 1, 'round', 'none'),
  part('60470b', '水平双夹板 1×2', 'Plate 1×2 with clips', 'connector', 2, 1, 1, 'clip', 'all'),
  part('2555', '带夹光面砖 1×1', 'Tile 1×1 with clip', 'connector', 1, 1, 1, 'clip', 'none'),
  part('11090', '管夹杆', 'Bar tube with clip', 'connector', 2, 1, 1, 'clip', 'none'),
  part('48729b', '短杆带夹', 'Short bar with clip', 'connector', 2, 1, 1, 'clip', 'none'),
  part('63868', '末端夹板 1×2', 'End clip plate 1×2', 'connector', 2, 1, 1, 'clip', 'all'),
  part('30374', '直杆 4L', 'Bar 4L', 'connector', 4, 1, 1, 'bar', 'none'),

  part('3659', '拱门 1×4', 'Arch 1×4', 'architecture', 4, 1, 6, 'arch'),
  part('2339', '拱门 1×5×4', 'Arch 1×5×4', 'architecture', 5, 1, 12, 'arch'),
  part('3455', '拱门 1×6', 'Arch 1×6', 'architecture', 6, 1, 6, 'arch'),
  part('3633', '矮栅栏 1×4', 'Low fence 1×4', 'architecture', 4, 1, 3, 'fence', 'none'),
  part('3185', '格子栅栏 1×4×2', 'Lattice fence 1×4×2', 'architecture', 4, 1, 6, 'fence', 'none'),
  part('2377', '窗框 1×2×2', 'Window frame 1×2×2', 'architecture', 2, 1, 6, 'panel'),

  part('3679', '转盘上片 2×2', 'Turntable top 2×2', 'motion', 2, 2, 1, 'turntable', 'center'),
  part('3680', '转盘底座 2×2', 'Turntable base 2×2', 'motion', 2, 2, 1, 'turntable', 'center'),
  part('2421', '三叶螺旋桨', 'Three-blade propeller', 'motion', 4, 4, 1, 'propeller', 'none'),
  part('32020', 'Technic 轮毂', 'Technic wheel rim', 'motion', 3, 1, 3, 'wheel', 'none'),
  part('2496', '小车轮组', 'Trolley wheel', 'motion', 2, 1, 2, 'wheel', 'none'),
];
export const diyCategories: { id: DiyCategory; nameZh: string; nameEn: string }[] = [
  { id: 'basic', nameZh: '基础砖', nameEn: 'Bricks' },
  { id: 'plate', nameZh: '薄板', nameEn: 'Plates' },
  { id: 'tile', nameZh: '光面/格栅', nameEn: 'Tiles' },
  { id: 'slope', nameZh: '斜坡/曲面', nameEn: 'Slopes' },
  { id: 'round', nameZh: '圆件', nameEn: 'Round' },
  { id: 'modified', nameZh: '改装砖', nameEn: 'Modified' },
  { id: 'technic', nameZh: 'Technic', nameEn: 'Technic' },
  { id: 'connector', nameZh: '连接件', nameEn: 'Connectors' },
  { id: 'architecture', nameZh: '建筑件', nameEn: 'Architecture' },
  { id: 'motion', nameZh: '运动件', nameEn: 'Motion' },
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
  { id: 'chair', nameZh: '靠背椅', nameEn: 'Chair', parts: [
    { partId: '3003', x: 0, y: 0, z: 0 }, { partId: '3022', x: 0, y: 3, z: 0 },
    { partId: '3004', x: 0, y: 4, z: 1 },
  ] },
  { id: 'tree', nameZh: '小树', nameEn: 'Tree', parts: [
    { partId: '3005', x: 1, y: 0, z: 1, color: 'brown' },
    { partId: '3941', x: 0, y: 3, z: 0, color: 'green' },
    { partId: '3942c', x: 0, y: 6, z: 0, color: 'green' },
  ] },
  { id: 'lamp', nameZh: '路灯', nameEn: 'Street lamp', parts: [
    { partId: '3005', x: 0, y: 0, z: 0, color: 'dark-gray' },
    { partId: '3005', x: 0, y: 3, z: 0, color: 'dark-gray' },
    { partId: '3942c', x: 0, y: 6, z: 0, color: 'yellow' },
  ] },
  { id: 'traffic-light', nameZh: '信号灯', nameEn: 'Traffic light', parts: [
    { partId: '3005', x: 0, y: 0, z: 0, color: 'dark-gray' },
    { partId: '3005', x: 0, y: 3, z: 0, color: 'black' },
    { partId: '87087', x: 0, y: 6, z: 0, color: 'red' },
    { partId: '87087', x: 0, y: 9, z: 0, color: 'yellow' },
    { partId: '87087', x: 0, y: 12, z: 0, color: 'green' },
  ] },
  { id: 'flower-bed', nameZh: '花坛', nameEn: 'Flower bed', parts: [
    { partId: '3031', x: 0, y: 0, z: 0, color: 'brown' },
    { partId: '3062b', x: 0, y: 1, z: 0, color: 'pink' },
    { partId: '3062b', x: 3, y: 1, z: 0, color: 'yellow' },
    { partId: '3062b', x: 0, y: 1, z: 3, color: 'purple' },
    { partId: '3062b', x: 3, y: 1, z: 3, color: 'red' },
  ] },
  { id: 'rocket', nameZh: '小火箭', nameEn: 'Mini rocket', parts: [
    { partId: '3941', x: 0, y: 0, z: 0, color: 'white' },
    { partId: '3941', x: 0, y: 3, z: 0, color: 'red' },
    { partId: '3942c', x: 0, y: 6, z: 0, color: 'red' },
  ] },
  { id: 'tower', nameZh: '彩色塔', nameEn: 'Color tower', parts: [
    { partId: '3003', x: 0, y: 0, z: 0, color: 'blue' },
    { partId: '3003', x: 0, y: 3, z: 0, color: 'yellow' },
    { partId: '3003', x: 0, y: 6, z: 0, color: 'red' },
    { partId: '3942c', x: 0, y: 9, z: 0, color: 'white' },
  ] },
  { id: 'signpost', nameZh: '指示牌', nameEn: 'Signpost', parts: [
    { partId: '3005', x: 0, y: 0, z: 0, color: 'dark-gray' },
    { partId: '3005', x: 0, y: 3, z: 0, color: 'dark-gray' },
    { partId: '30414', x: 0, y: 6, z: 0, color: 'blue' },
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
    return { id: `${stampId}_${index}`, stampId, partId: part.partId, color: part.color ?? brush.color, x: px, y: part.y, z: pz, turn: ((turn + brush.turn) % 4) as Turn };
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
  const size = footprint(brick);
  const dx = x - brick.x, dz = z - brick.z;
  if (part.top === 'none') return false;
  if (part.top === 'center') return dx === Math.floor((size.width - 1) / 2) && dz === Math.floor((size.depth - 1) / 2);
  if (part.top === 'rear') return [dz === 0, dx === 0, dz === size.depth - 1, dx === size.width - 1][brick.turn];
  return true;
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

export function rotateDiyBrick(
  project: DiyProject,
  id: string,
): { project: DiyProject; issue: PlacementIssue } {
  const current = project.bricks.find(brick => brick.id === id);
  if (!current) return { project, issue: null };
  return moveDiyBrick(project, id, { turn: ((current.turn + 1) % 4) as Turn });
}

export function moveDiyBrick(project: DiyProject, id: string, update: Partial<Pick<DiyBrick, 'x' | 'y' | 'z' | 'turn'>>) {
  const current = project.bricks.find(brick => brick.id === id);
  if (!current) return { project, issue: null };
  const replacement = { ...current, ...update };
  const bricks = project.bricks.map(brick => brick.id === id ? replacement : brick);
  const issue = new DiyIndex([]).validate(bricks, 0);
  return issue ? { project, issue } : { project: { ...project, bricks }, issue: null };
}

export function duplicateDiyBrick(project: DiyProject, id: string): { project: DiyProject; issue: PlacementIssue; id?: string } {
  const source = project.bricks.find(brick => brick.id === id);
  if (!source) return { project, issue: null };
  if (project.bricks.length >= DIY_LIMIT) return { project, issue: 'limit' };
  const index = new DiyIndex(project.bricks);
  const copyId = crypto.randomUUID();
  for (let radius = 1; radius <= 32; radius++) {
    for (let dz = -radius; dz <= radius; dz++) for (let dx = -radius; dx <= radius; dx++) {
      if (Math.max(Math.abs(dx), Math.abs(dz)) !== radius) continue;
      const candidate = { ...source, id: copyId, stampId: copyId, x: source.x + dx, z: source.z + dz };
      if (!index.validate([candidate], project.bricks.length)) {
        return { project: { ...project, bricks: [...project.bricks, candidate] }, issue: null, id: copyId };
      }
    }
  }
  return { project, issue: 'unsupported' };
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
