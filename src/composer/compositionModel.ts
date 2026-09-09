import type { AtlasManifest } from '../model/types';
import {
  brickPalette,
  type ImageBrick,
  type ImageBrickBomItem,
  type ImageBrickBuild,
} from '../creator/imageBrickModel';

export type ComposerAssetKind = 'model' | 'character' | 'animal' | 'part';
export type QuarterTurn = 0 | 1 | 2 | 3;

export interface ComposerAsset {
  id: string;
  nameZh: string;
  nameEn: string;
  categoryZh: string;
  categoryEn: string;
  kind: ComposerAssetKind;
  modelId?: string;
  preview?: string;
  footprint: [number, number];
  original?: boolean;
  bricks?: ComposerBrick[];
}

export interface ComposerBrick {
  partId: string;
  width: number;
  depth: number;
  height: number;
  x: number;
  y: number;
  z: number;
  colorCode: number;
  colorHex: string;
}

export interface ComposerItem {
  id: string;
  assetId: string;
  nameZh: string;
  nameEn: string;
  kind: ComposerAssetKind;
  sourceModelId?: string;
  sourceUrl?: string;
  x: number;
  z: number;
  level: number;
  rotation: QuarterTurn;
  footprint: [number, number];
  bricks: ComposerBrick[];
}

export interface BaseplatePreset {
  id: string;
  nameZh: string;
  nameEn: string;
  width: number;
  depth: number;
  colorCode: number;
  colorHex: string;
}

export interface CompositionProject {
  version: 1;
  id: string;
  name: string;
  baseplateId: string;
  items: ComposerItem[];
  updatedAt: number;
}

const brick = (
  partId: string,
  width: number,
  depth: number,
  height: number,
  x: number,
  y: number,
  z: number,
  colorCode: number,
  colorHex: string,
): ComposerBrick => ({ partId, width, depth, height, x, y, z, colorCode, colorHex });

const miniFigure = [
  brick('970c00', 2, 1, 1.2, 0, 2.7, 0, 1, '#0055bf'),
  brick('973c00', 2, 1, 1.7, 0, 1.25, 0, 4, '#c91a09'),
  brick('3626c', 1, 1, 1, 0, 3.8, 0, 14, '#f2cd37'),
  brick('3901', 1.3, 1.3, 0.35, 0, 4.45, 0, 1, '#0055bf'),
];

const cat = [
  brick('3004', 2, 1, 1.16, 0, 1.48, 0, 72, '#6c6e68'),
  brick('3005', 1, 1, 1.16, 0.5, 2.62, 0, 72, '#6c6e68'),
  brick('54200', 1, 1, 0.65, 0.5, 3.52, 0, 72, '#6c6e68'),
  brick('3005', 1, 1, 1.16, -1.2, 1.65, 0, 72, '#6c6e68'),
];

const dog = [
  brick('3010', 4, 1, 1.16, 0, 1.48, 0, 6, '#583927'),
  brick('3004', 2, 1, 1.16, 1.25, 2.62, 0, 6, '#583927'),
  brick('3005', 1, 1, 1.16, -1.9, 1.85, 0, 6, '#583927'),
  brick('3005', 1, 1, 1.16, -1.1, 0.62, 0, 6, '#583927'),
  brick('3005', 1, 1, 1.16, 1.1, 0.62, 0, 6, '#583927'),
];

export const baseplateCatalog: BaseplatePreset[] = [
  { id: '32-gray', nameZh: '城市底板', nameEn: 'City baseplate', width: 32, depth: 32, colorCode: 71, colorHex: '#a0a5a9' },
  { id: '48-green', nameZh: '公园底板', nameEn: 'Park baseplate', width: 48, depth: 32, colorCode: 2, colorHex: '#4b9f4a' },
  { id: '48-blue', nameZh: '海港底板', nameEn: 'Harbor baseplate', width: 48, depth: 32, colorCode: 1, colorHex: '#4a90cf' },
  { id: '64-sand', nameZh: '大型场景底板', nameEn: 'Large scene base', width: 64, depth: 48, colorCode: 19, colorHex: '#d7c58c' },
];

export const composerAssets: ComposerAsset[] = [
  { id: 'sea-plane', nameZh: '水上飞机', nameEn: 'Sea plane', categoryZh: '飞行器', categoryEn: 'Aircraft', kind: 'model', modelId: '31028', preview: 'models/31028/preview.png', footprint: [18, 18] },
  { id: 'sailboat', nameZh: '帆船', nameEn: 'Sailboat', categoryZh: '船舶', categoryEn: 'Marine', kind: 'model', modelId: '31028-sailboat', preview: 'models/31028-sailboat/preview.png', footprint: [14, 18] },
  { id: 'blue-racer', nameZh: '蓝色赛车', nameEn: 'Blue racer', categoryZh: '车辆', categoryEn: 'Vehicles', kind: 'model', modelId: '31027', preview: 'models/31027/preview.png', footprint: [16, 10] },
  { id: 'kart', nameZh: '卡丁车', nameEn: 'Kart', categoryZh: '车辆', categoryEn: 'Vehicles', kind: 'model', modelId: '31027-kart', preview: 'models/31027-kart/preview.png', footprint: [12, 10] },
  { id: 'cottage', nameZh: '田园小屋', nameEn: 'Small cottage', categoryZh: '建筑', categoryEn: 'Buildings', kind: 'model', modelId: '31009', preview: 'models/31009/preview.png', footprint: [24, 20] },
  { id: 'caboose', nameZh: '铁路守车', nameEn: 'Caboose', categoryZh: '铁路', categoryEn: 'Rail', kind: 'model', modelId: '10014', preview: 'models/10014/preview.png', footprint: [22, 10] },
  { id: 'minifigure', nameZh: '城市小人', nameEn: 'City minifigure', categoryZh: '角色', categoryEn: 'Characters', kind: 'character', footprint: [3, 3], original: true, bricks: miniFigure },
  { id: 'cat', nameZh: '积木小猫', nameEn: 'Brick cat', categoryZh: '动物', categoryEn: 'Animals', kind: 'animal', footprint: [4, 3], original: true, bricks: cat },
  { id: 'dog', nameZh: '积木小狗', nameEn: 'Brick dog', categoryZh: '动物', categoryEn: 'Animals', kind: 'animal', footprint: [6, 3], original: true, bricks: dog },
  { id: 'brick-1x1', nameZh: '基础砖 1×1', nameEn: 'Brick 1×1', categoryZh: '单个零件', categoryEn: 'Loose parts', kind: 'part', footprint: [1, 1], original: true, bricks: [brick('3005', 1, 1, 1.16, 0, 0.9, 0, 4, '#c91a09')] },
  { id: 'brick-1x2', nameZh: '基础砖 1×2', nameEn: 'Brick 1×2', categoryZh: '单个零件', categoryEn: 'Loose parts', kind: 'part', footprint: [2, 1], original: true, bricks: [brick('3004', 2, 1, 1.16, 0, 0.9, 0, 14, '#f2cd37')] },
  { id: 'brick-1x3', nameZh: '基础砖 1×3', nameEn: 'Brick 1×3', categoryZh: '单个零件', categoryEn: 'Loose parts', kind: 'part', footprint: [3, 1], original: true, bricks: [brick('3622', 3, 1, 1.16, 0, 0.9, 0, 4, '#c91a09')] },
  { id: 'brick-2x2', nameZh: '基础砖 2×2', nameEn: 'Brick 2×2', categoryZh: '单个零件', categoryEn: 'Loose parts', kind: 'part', footprint: [2, 2], original: true, bricks: [brick('3003', 2, 2, 1.16, 0, 0.9, 0, 15, '#f4f4f4')] },
  { id: 'brick-2x4', nameZh: '基础砖 2×4', nameEn: 'Brick 2×4', categoryZh: '单个零件', categoryEn: 'Loose parts', kind: 'part', footprint: [4, 2], original: true, bricks: [brick('3001', 4, 2, 1.16, 0, 0.9, 0, 1, '#0055bf')] },
  { id: 'plate-1x2', nameZh: '薄板 1×2', nameEn: 'Plate 1×2', categoryZh: '单个零件', categoryEn: 'Loose parts', kind: 'part', footprint: [2, 1], original: true, bricks: [brick('3023', 2, 1, 0.38, 0, 0.51, 0, 72, '#6c6e68')] },
  { id: 'plate-2x4', nameZh: '薄板 2×4', nameEn: 'Plate 2×4', categoryZh: '单个零件', categoryEn: 'Loose parts', kind: 'part', footprint: [4, 2], original: true, bricks: [brick('3020', 4, 2, 0.38, 0, 0.51, 0, 15, '#f4f4f4')] },
  { id: 'tile-1x2', nameZh: '光面砖 1×2', nameEn: 'Tile 1×2', categoryZh: '单个零件', categoryEn: 'Loose parts', kind: 'part', footprint: [2, 1], original: true, bricks: [brick('3069b', 2, 1, 0.28, 0, 0.46, 0, 0, '#05131d')] },
  { id: 'round-1x1', nameZh: '圆砖 1×1', nameEn: 'Round brick 1×1', categoryZh: '单个零件', categoryEn: 'Loose parts', kind: 'part', footprint: [1, 1], original: true, bricks: [brick('3062b', 1, 1, 1.16, 0, 0.9, 0, 27, '#bbe90b')] },
  { id: 'slope-2x2', nameZh: '斜坡砖 2×2', nameEn: 'Slope brick 2×2', categoryZh: '单个零件', categoryEn: 'Loose parts', kind: 'part', footprint: [2, 2], original: true, bricks: [brick('3039', 2, 2, 1.16, 0, 0.9, 0, 25, '#fe8a18')] },
];

export function createCompositionProject(): CompositionProject {
  return {
    version: 1,
    id: `composition_${Date.now().toString(36)}`,
    name: 'My Brick World',
    baseplateId: baseplateCatalog[0].id,
    items: [],
    updatedAt: Date.now(),
  };
}

export function sourceBricksFromManifest(manifest: AtlasManifest): ComposerBrick[] {
  const min = manifest.bounds.min;
  const max = manifest.bounds.max;
  const centerX = (min[0] + max[0]) / 2;
  const centerZ = (min[2] + max[2]) / 2;
  return manifest.instances.map(part => {
    const sizeX = Math.max(1, part.bounds.max[0] - part.bounds.min[0]);
    const sizeY = Math.max(3.2, part.bounds.max[1] - part.bounds.min[1]);
    const sizeZ = Math.max(1, part.bounds.max[2] - part.bounds.min[2]);
    return {
      partId: part.partNumber,
      width: Math.max(1, Math.min(4, Math.round(sizeX / 20))),
      depth: Math.max(1, Math.min(4, Math.round(sizeZ / 20))),
      height: Math.max(0.35, Math.min(3.5, sizeY / 12)),
      x: ((part.bounds.min[0] + part.bounds.max[0]) / 2 - centerX) / 20,
      y: ((part.bounds.min[1] + part.bounds.max[1]) / 2 - min[1]) / 12 + 0.34,
      z: ((part.bounds.min[2] + part.bounds.max[2]) / 2 - centerZ) / 20,
      colorCode: Number(part.colorCode) || 0,
      colorHex: part.colorHex,
    };
  });
}

export function rotatedFootprint(item: Pick<ComposerItem, 'footprint' | 'rotation'>) {
  return item.rotation % 2
    ? [item.footprint[1], item.footprint[0]] as [number, number]
    : item.footprint;
}

function rectanglesOverlap(a: ComposerItem, b: ComposerItem) {
  if ((a.kind === 'part' || b.kind === 'part') && a.level !== b.level) return false;
  const [aw, ad] = rotatedFootprint(a);
  const [bw, bd] = rotatedFootprint(b);
  return Math.abs(a.x - b.x) < (aw + bw) / 2
    && Math.abs(a.z - b.z) < (ad + bd) / 2;
}

export function canPlaceItem(project: CompositionProject, candidate: ComposerItem, ignoreId?: string) {
  const base = baseplateCatalog.find(item => item.id === project.baseplateId) ?? baseplateCatalog[0];
  const [width, depth] = rotatedFootprint(candidate);
  if (
    candidate.x - width / 2 < -base.width / 2
    || candidate.x + width / 2 > base.width / 2
    || candidate.z - depth / 2 < -base.depth / 2
    || candidate.z + depth / 2 > base.depth / 2
  ) return false;
  return project.items.every(item => item.id === ignoreId || !rectanglesOverlap(item, candidate));
}

export function findOpenPlacement(
  project: CompositionProject,
  footprint: [number, number],
): { x: number; z: number } | null {
  const base = baseplateCatalog.find(item => item.id === project.baseplateId) ?? baseplateCatalog[0];
  for (let ring = 0; ring <= Math.max(base.width, base.depth); ring += 2) {
    for (let z = -ring; z <= ring; z += 2) {
      for (let x = -ring; x <= ring; x += 2) {
        if (Math.max(Math.abs(x), Math.abs(z)) !== ring) continue;
        const candidate: ComposerItem = {
          id: '__candidate__',
          assetId: '',
          nameZh: '',
          nameEn: '',
          kind: 'part',
          x,
          z,
          level: 0,
          rotation: 0,
          footprint,
          bricks: [],
        };
        if (canPlaceItem(project, candidate)) return { x, z };
      }
    }
  }
  return null;
}

export function createComposerItem(
  project: CompositionProject,
  asset: ComposerAsset,
  bricks = asset.bricks ?? [],
  sourceUrl?: string,
): ComposerItem | null {
  const placement = findOpenPlacement(project, asset.footprint);
  if (!placement) return null;
  return {
    id: `item_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 7)}`,
    assetId: asset.id,
    nameZh: asset.nameZh,
    nameEn: asset.nameEn,
    kind: asset.kind,
    sourceModelId: asset.modelId,
    sourceUrl,
    x: placement.x,
    z: placement.z,
    level: 0,
    rotation: 0,
    footprint: asset.footprint,
    bricks,
  };
}

function rotatePoint(x: number, z: number, rotation: QuarterTurn): [number, number] {
  if (rotation === 1) return [z, -x];
  if (rotation === 2) return [-x, -z];
  if (rotation === 3) return [-z, x];
  return [x, z];
}

function baseplateBricks(base: BaseplatePreset): ImageBrick[] {
  const result: ImageBrick[] = [];
  for (let z = 0; z < base.depth; z += 4) {
    for (let x = 0; x < base.width; x += 4) {
      const width = Math.min(4, base.width - x);
      const depth = Math.min(4, base.depth - z);
      result.push({
        id: `base_${x}_${z}`,
        partId: '3811',
        width,
        depth,
        height: 0.28,
        x: x + width / 2 - base.width / 2,
        y: 0.14,
        z: z + depth / 2 - base.depth / 2,
        colorId: `base-${base.colorCode}`,
        colorCode: base.colorCode,
        colorHex: base.colorHex,
        step: 1,
      });
    }
  }
  return result;
}

export function createCompositionBuild(project: CompositionProject): ImageBrickBuild {
  const base = baseplateCatalog.find(item => item.id === project.baseplateId) ?? baseplateCatalog[0];
  const bricks = baseplateBricks(base);
  project.items.forEach((item, itemIndex) => {
    item.bricks.forEach((source, brickIndex) => {
      const [localX, localZ] = rotatePoint(source.x, source.z, item.rotation);
      bricks.push({
        id: `${item.id}_${String(brickIndex + 1).padStart(4, '0')}`,
        partId: source.partId,
        width: source.width,
        depth: source.depth,
        height: source.height,
        rotation: item.rotation,
        x: item.x + localX,
        y: source.y + item.level * 1.16,
        z: item.z + localZ,
        colorId: `ldraw-${source.colorCode}`,
        colorCode: source.colorCode,
        colorHex: source.colorHex,
        step: itemIndex + 2,
      });
    });
  });
  const steps = [
    { id: 1, layer: 0, rowStart: 0, rowEnd: base.depth - 1, brickIds: bricks.filter(item => item.step === 1).map(item => item.id) },
    ...project.items.map((_, index) => ({
      id: index + 2,
      layer: index + 1,
      rowStart: 0,
      rowEnd: 0,
      brickIds: bricks.filter(brickItem => brickItem.step === index + 2).map(brickItem => brickItem.id),
    })),
  ];
  const bom = new Map<string, ImageBrickBomItem>();
  for (const item of bricks) {
    const key = `${item.partId}:${item.colorCode}`;
    const palette = brickPalette.find(color => color.code === item.colorCode);
    const current = bom.get(key);
    if (current) current.quantity++;
    else bom.set(key, {
      key,
      partId: item.partId,
      width: item.width,
      depth: item.depth,
      height: item.height,
      colorId: item.colorId,
      colorCode: item.colorCode,
      colorHex: item.colorHex,
      colorNameZh: palette?.nameZh ?? `LDraw ${item.colorCode}`,
      colorNameEn: palette?.nameEn ?? `LDraw ${item.colorCode}`,
      quantity: 1,
    });
  }
  return {
    name: project.name,
    width: base.width,
    height: Math.max(1, Math.ceil(Math.max(...bricks.map(item => item.y + (item.height ?? 1) / 2)))),
    maxDepth: base.depth,
    method: 'solid',
    bond: 'running',
    viewCount: 0,
    brickBudget: bricks.length,
    sourceWidth: base.width,
    sourceHeight: base.depth,
    backgroundHex: base.colorHex,
    bricks,
    steps,
    bom: [...bom.values()].sort((a, b) => b.quantity - a.quantity || a.key.localeCompare(b.key)),
  };
}

export function parseCompositionProject(value: string | null): CompositionProject {
  if (!value) return createCompositionProject();
  try {
    const parsed = JSON.parse(value) as CompositionProject;
    if (parsed.version !== 1 || !Array.isArray(parsed.items)) return createCompositionProject();
    return parsed;
  } catch {
    return createCompositionProject();
  }
}
