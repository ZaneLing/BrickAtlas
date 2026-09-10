import type { AtlasManifest } from '../model/types';
import { Matrix4 } from 'three';
import { modelCatalog } from '../../atlas.config';
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
  originalMatrix?: number[];
  shape?: ImageBrick['shape'];
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
): ComposerBrick => ({
  partId, width, depth, height, x, y, z, colorCode, colorHex,
  shape: partId === '3069b' ? 'tile' : partId === '3062b' ? 'round' : partId === '3039' || partId === '54200' ? 'slope' : 'box',
});

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
    const sizeX = part.bounds.max[0] - part.bounds.min[0];
    const sizeY = part.bounds.max[1] - part.bounds.min[1];
    const sizeZ = part.bounds.max[2] - part.bounds.min[2];
    const normalization = new Matrix4().makeTranslation(-centerX, -min[1] + 3.2, -centerZ);
    return {
      partId: part.partNumber,
      width: Math.max(0.01, sizeX / 8),
      depth: Math.max(0.01, sizeZ / 8),
      height: Math.max(0.01, sizeY / 8),
      x: ((part.bounds.min[0] + part.bounds.max[0]) / 2 - centerX) / 8,
      y: ((part.bounds.min[1] + part.bounds.max[1]) / 2 - min[1]) / 8 + 0.4,
      z: ((part.bounds.min[2] + part.bounds.max[2]) / 2 - centerZ) / 8,
      colorCode: Number(part.colorCode) || 0,
      colorHex: part.colorHex,
      originalMatrix: normalization.multiply(new Matrix4().fromArray(part.originalMatrix)).toArray(),
    };
  });
}

export function rotatedFootprint(item: Pick<ComposerItem, 'footprint' | 'rotation'>) {
  return item.rotation % 2
    ? [item.footprint[1], item.footprint[0]] as [number, number]
    : item.footprint;
}

function rectanglesOverlap(a: ComposerItem, b: ComposerItem) {
  const vertical = (item: ComposerItem) => {
    const bottom = Math.min(...item.bricks.map(brick => brick.y - brick.height / 2));
    const top = Math.max(...item.bricks.map(brick => brick.y + brick.height / 2));
    return [bottom + item.level * 0.4, top + item.level * 0.4];
  };
  if (a.bricks.length && b.bricks.length) {
    const [amin, amax] = vertical(a), [bmin, bmax] = vertical(b);
    if (amax <= bmin + 0.01 || bmax <= amin + 0.01) return false;
  }
  const [aw, ad] = rotatedFootprint(a);
  const [bw, bd] = rotatedFootprint(b);
  return Math.abs(a.x - b.x) < (aw + bw) / 2
    && Math.abs(a.z - b.z) < (ad + bd) / 2;
}

export function canPlaceItem(project: CompositionProject, candidate: ComposerItem, ignoreId?: string) {
  if (![candidate.x, candidate.z, candidate.level].every(Number.isFinite)
    || !Number.isInteger(candidate.level) || candidate.level < 0 || candidate.level > 60
    || ![0, 1, 2, 3].includes(candidate.rotation)) return false;
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
  const footprint: [number, number] = asset.modelId && bricks.length
    ? [
      Math.ceil(2 * Math.max(...bricks.map(brick => Math.abs(brick.x) + brick.width / 2))),
      Math.ceil(2 * Math.max(...bricks.map(brick => Math.abs(brick.z) + brick.depth / 2))),
    ] : asset.footprint;
  const placement = findOpenPlacement(project, footprint);
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
    footprint,
    bricks: asset.kind === 'part' ? bricks.map(source => {
      const height = /^(3023|3020|3069b)$/.test(source.partId) ? 0.4 : 1.2;
      return { ...source, height, y: 0.4 + height / 2 };
    }) : bricks,
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
        partId: '3031',
        width,
        depth,
        height: 0.4,
        x: x + width / 2 - base.width / 2,
        y: 0.2,
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

export function createCompositionBuild(
  project: CompositionProject,
  manifests: ReadonlyMap<string, AtlasManifest> = new Map(),
): ImageBrickBuild {
  const base = baseplateCatalog.find(item => item.id === project.baseplateId) ?? baseplateCatalog[0];
  const bricks = baseplateBricks(base);
  const sourceGroups: NonNullable<ImageBrickBuild['sourceGroups']> = [];
  project.items.forEach((item, itemIndex) => {
    const placement = new Matrix4().makeTranslation(item.x * 8, item.level * 3.2, item.z * 8)
      .multiply(new Matrix4().makeRotationY(item.rotation * Math.PI / 2));
    const ids: string[] = [];
    item.bricks.forEach((source, brickIndex) => {
      const [localX, localZ] = rotatePoint(source.x, source.z, item.rotation);
      const id = `${item.id}_${String(brickIndex + 1).padStart(4, '0')}`;
      ids.push(id);
      bricks.push({
        id,
        partId: source.partId,
        width: source.width,
        depth: source.depth,
        height: source.height,
        rotation: item.rotation,
        x: item.x + localX,
        y: source.y + item.level * 0.4,
        z: item.z + localZ,
        colorId: `ldraw-${source.colorCode}`,
        colorCode: source.colorCode,
        colorHex: source.colorHex,
        step: itemIndex + 2,
        shape: source.shape,
        ldrawMatrix: source.originalMatrix
          ? new Matrix4().makeScale(2.5, -2.5, -2.5).multiply(placement)
            .multiply(new Matrix4().fromArray(source.originalMatrix)).toArray()
          : undefined,
      });
    });
    const manifest = item.sourceModelId ? manifests.get(item.sourceModelId) : undefined;
    if (manifest) {
      const { min, max } = manifest.bounds;
      const normalization = new Matrix4().makeTranslation(-(min[0] + max[0]) / 2, -min[1] + 3.2, -(min[2] + max[2]) / 2);
      sourceGroups.push({
        modelId: item.sourceModelId!,
        matrix: new Matrix4().makeScale(1.5, 1.5, 1.5).multiply(placement).multiply(normalization).toArray(),
        brickIds: ids,
      });
    }
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
    reconstruction: 'mesh-ai',
    bricks,
    sourceGroups,
    credits: [...new Set(project.items.map(item => item.sourceModelId))].flatMap(id => {
      const source = modelCatalog.find(model => model.id === id);
      return source ? [`${source.title}; ${source.author}; ${source.license}; ${source.sourceUrl}; transformed into a composition`] : [];
    }),
    steps,
    bom: [...bom.values()].sort((a, b) => b.quantity - a.quantity || a.key.localeCompare(b.key)),
  };
}

export function parseCompositionProject(value: string | null): CompositionProject {
  if (!value) return createCompositionProject();
  try {
    const parsed = JSON.parse(value) as CompositionProject;
    if (parsed.version !== 1 || !Array.isArray(parsed.items) || parsed.items.length > 200
      || typeof parsed.name !== 'string' || typeof parsed.id !== 'string'
      || !baseplateCatalog.some(base => base.id === parsed.baseplateId)
      || new Set(parsed.items.map(item => item?.id)).size !== parsed.items.length
      || !parsed.items.every(item =>
        item && typeof item.id === 'string' && typeof item.nameZh === 'string' && typeof item.nameEn === 'string'
        && composerAssets.some(asset => asset.id === item.assetId)
        && [item.x, item.z, item.level].every(Number.isFinite)
        && [0, 1, 2, 3].includes(item.rotation)
        && Array.isArray(item.footprint) && item.footprint.length === 2 && item.footprint.every(n => Number.isFinite(n) && n > 0)
        && Array.isArray(item.bricks) && item.bricks.length > 0 && item.bricks.length <= 5000
        && item.bricks.every(brick =>
          brick && /^[\w-]+$/.test(brick.partId) && /^#[0-9a-f]{6}$/i.test(brick.colorHex)
          && [brick.width, brick.depth, brick.height].every(n => Number.isFinite(n) && n > 0)
          && [brick.x, brick.y, brick.z, brick.colorCode].every(Number.isFinite)
          && (!brick.originalMatrix || brick.originalMatrix.length === 16 && brick.originalMatrix.every(Number.isFinite)),
        ),
      )) return createCompositionProject();
    return parsed;
  } catch {
    return createCompositionProject();
  }
}

export function changeBaseplate(project: CompositionProject, baseplateId: string): CompositionProject | null {
  if (!baseplateCatalog.some(base => base.id === baseplateId)) return null;
  const next = { ...project, baseplateId, updatedAt: Date.now() };
  // Never relocate, rotate or delete an assembly as a side effect of changing its base.
  return next.items.every(item => canPlaceItem(next, item, item.id)) ? next : null;
}
