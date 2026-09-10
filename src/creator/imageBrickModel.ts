export interface BrickPaletteColor {
  id: string;
  code: number;
  nameZh: string;
  nameEn: string;
  hex: string;
}

export interface ImageBrick {
  id: string;
  partId: string;
  width: number;
  depth?: number;
  height?: number;
  rotation?: 0 | 1 | 2 | 3;
  ldrawMatrix?: number[];
  shape?: 'box' | 'round' | 'slope' | 'tile';
  x: number;
  y: number;
  z: number;
  colorId: string;
  colorCode: number;
  colorHex: string;
  step: number;
}

export interface ImageBrickBomItem {
  key: string;
  partId: string;
  width: number;
  depth?: number;
  height?: number;
  colorId: string;
  colorCode: number;
  colorHex: string;
  colorNameZh: string;
  colorNameEn: string;
  quantity: number;
}

export interface ImageBrickStep {
  id: number;
  layer: number;
  rowStart: number;
  rowEnd: number;
  brickIds: string[];
}

export interface ImageBrickBuild {
  name: string;
  width: number;
  height: number;
  maxDepth: number;
  method: ImageBrickMethod;
  bond: ImageBrickBond;
  viewCount: number;
  brickBudget: number;
  sourceWidth: number;
  sourceHeight: number;
  backgroundHex: string;
  reconstruction: 'empty' | 'relief' | 'shape-inflation' | 'depth-ai' | 'multi-view' | 'mesh-ai';
  bricks: ImageBrick[];
  bom: ImageBrickBomItem[];
  steps: ImageBrickStep[];
  sourceGroups?: { modelId: string; matrix: number[]; brickIds: string[] }[];
  credits?: string[];
}

export interface ImageBrickOptions {
  width: number;
  maxDepth: number;
  maxColors: number;
  removeBackground: boolean;
  backgroundThreshold: number;
  method: ImageBrickMethod;
  bond: ImageBrickBond;
  brickBudget: number;
}

export type ImageBrickMethod = 'relief' | 'hollow' | 'solid';
export type ImageBrickBond = 'running' | 'stacked' | 'reinforced';
export interface SampledImage {
  data: Uint8ClampedArray;
  width: number;
  height: number;
}
export interface SampledDepth {
  data: Float32Array;
  width: number;
  height: number;
}
export interface SampledMeshVolume {
  width: number;
  height: number;
  depth: number;
  occupied: Uint8Array;
  triangleCount: number;
  surfaceVoxelCount: number;
  solidVoxelCount: number;
}
export interface ImageBrickViews {
  front: SampledImage;
  left?: SampledImage;
  back?: SampledImage;
  right?: SampledImage;
  frontDepth?: SampledDepth;
}

export const brickPalette: BrickPaletteColor[] = [
  { id: 'black', code: 0, nameZh: '黑色', nameEn: 'Black', hex: '#05131d' },
  { id: 'blue', code: 1, nameZh: '亮蓝色', nameEn: 'Bright blue', hex: '#0055bf' },
  { id: 'green', code: 2, nameZh: '深绿色', nameEn: 'Dark green', hex: '#237841' },
  { id: 'red', code: 4, nameZh: '亮红色', nameEn: 'Bright red', hex: '#c91a09' },
  { id: 'dark-pink', code: 5, nameZh: '深粉色', nameEn: 'Dark pink', hex: '#c870a0' },
  { id: 'brown', code: 6, nameZh: '棕色', nameEn: 'Brown', hex: '#583927' },
  { id: 'light-gray', code: 71, nameZh: '浅灰色', nameEn: 'Light bluish gray', hex: '#a0a5a9' },
  { id: 'dark-gray', code: 72, nameZh: '深灰色', nameEn: 'Dark bluish gray', hex: '#6c6e68' },
  { id: 'yellow', code: 14, nameZh: '亮黄色', nameEn: 'Bright yellow', hex: '#f2cd37' },
  { id: 'white', code: 15, nameZh: '白色', nameEn: 'White', hex: '#f4f4f4' },
  { id: 'tan', code: 19, nameZh: '沙黄色', nameEn: 'Tan', hex: '#e4cd9e' },
  { id: 'purple', code: 22, nameZh: '紫色', nameEn: 'Purple', hex: '#81007b' },
  { id: 'orange', code: 25, nameZh: '亮橙色', nameEn: 'Bright orange', hex: '#fe8a18' },
  { id: 'lime', code: 27, nameZh: '青柠色', nameEn: 'Lime', hex: '#bbe90b' },
  { id: 'lavender', code: 31, nameZh: '薰衣草色', nameEn: 'Lavender', hex: '#e1d5ed' },
  { id: 'dark-red', code: 320, nameZh: '暗红色', nameEn: 'Dark red', hex: '#720e0f' },
  { id: 'azure', code: 322, nameZh: '中天蓝色', nameEn: 'Medium azure', hex: '#68c3e2' },
  { id: 'pink', code: 221, nameZh: '亮粉色', nameEn: 'Bright pink', hex: '#e4adc8' },
];

const partByFootprint: Record<string, string> = {
  '1x1': '3005',
  '2x1': '3004',
  '3x1': '3622',
  '4x1': '3010',
  '2x2': '3003',
  '3x2': '3002',
  '4x2': '3001',
};

const clamp = (value: number, min: number, max: number) => Math.max(min, Math.min(max, value));

function hexToRgb(hex: string) {
  const value = Number.parseInt(hex.slice(1), 16);
  return [(value >> 16) & 255, (value >> 8) & 255, value & 255] as const;
}

function linear(value: number) {
  const channel = value / 255;
  return channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4;
}

function rgbToLab(rgb: readonly number[]) {
  const [r, g, b] = rgb.map(linear);
  const x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047;
  const y = r * 0.2126 + g * 0.7152 + b * 0.0722;
  const z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883;
  const pivot = (value: number) => value > 0.008856 ? value ** (1 / 3) : 7.787 * value + 16 / 116;
  const [fx, fy, fz] = [pivot(x), pivot(y), pivot(z)];
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)] as const;
}

const paletteLab = brickPalette.map(color => ({ color, lab: rgbToLab(hexToRgb(color.hex)) }));

function distance(a: readonly number[], b: readonly number[]) {
  return Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
}

function nearestColor(rgb: readonly number[], palette = paletteLab) {
  const lab = rgbToLab(rgb);
  return palette.reduce((best, candidate) =>
    distance(lab, candidate.lab) < distance(lab, best.lab) ? candidate : best,
  ).color;
}

function estimateBackground(data: Uint8ClampedArray, width: number, height: number) {
  let minX = width;
  let minY = height;
  let maxX = -1;
  let maxY = -1;
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      if (data[(y * width + x) * 4 + 3] <= 24) continue;
      minX = Math.min(minX, x);
      minY = Math.min(minY, y);
      maxX = Math.max(maxX, x);
      maxY = Math.max(maxY, y);
    }
  }
  if (maxX < minX || maxY < minY) return [255, 255, 255] as [number, number, number];
  const points: [number, number][] = [];
  const stride = Math.max(1, Math.floor(Math.min(maxX - minX + 1, maxY - minY + 1) / 8));
  for (let x = minX; x <= maxX; x += stride) {
    points.push([x, minY], [x, maxY]);
  }
  for (let y = minY + stride; y < maxY - stride; y += stride) {
    points.push([minX, y], [maxX, y]);
  }
  const channels = [0, 1, 2].map(channel => points.map(([x, y]) =>
    data[(y * width + x) * 4 + channel],
  ).sort((a, b) => a - b));
  return channels.map(values => values[Math.floor(values.length / 2)] ?? 255) as [number, number, number];
}

function foregroundMask(
  data: Uint8ClampedArray,
  width: number,
  height: number,
  background: [number, number, number],
  threshold: number,
) {
  const backgroundLab = rgbToLab(background);
  const pixelDistance = new Float32Array(width * height);
  const alpha = new Uint8Array(width * height);
  for (let index = 0; index < width * height; index++) {
    const offset = index * 4;
    alpha[index] = data[offset + 3];
    pixelDistance[index] = distance(
      rgbToLab([data[offset], data[offset + 1], data[offset + 2]]),
      backgroundLab,
    );
  }
  const exterior = new Uint8Array(width * height);
  const queue = new Int32Array(width * height);
  let head = 0;
  let tail = 0;
  const seed = (x: number, y: number) => {
    const index = y * width + x;
    if (exterior[index] || (alpha[index] > 24 && pixelDistance[index] > threshold * 1.55)) return;
    exterior[index] = 1;
    queue[tail++] = index;
  };
  for (let x = 0; x < width; x++) {
    seed(x, 0);
    seed(x, height - 1);
  }
  for (let y = 1; y < height - 1; y++) {
    seed(0, y);
    seed(width - 1, y);
  }
  while (head < tail) {
    const index = queue[head++];
    const x = index % width;
    const y = Math.floor(index / width);
    const neighbors = [
      x > 0 ? index - 1 : -1,
      x + 1 < width ? index + 1 : -1,
      y > 0 ? index - width : -1,
      y + 1 < height ? index + width : -1,
    ];
    for (const next of neighbors) {
      if (next < 0 || exterior[next]) continue;
      if (alpha[next] <= 24 || pixelDistance[next] <= threshold * 1.2) {
        exterior[next] = 1;
        queue[tail++] = next;
      }
    }
  }
  const mask = new Uint8Array(width * height);
  for (let index = 0; index < mask.length; index++) {
    mask[index] = alpha[index] > 24
      && !exterior[index]
      && pixelDistance[index] >= threshold * 0.85
      ? 1
      : 0;
  }
  const occupied = mask.reduce((sum, value) => sum + value, 0);
  if (occupied < Math.max(4, mask.length * 0.025)) {
    for (let index = 0; index < mask.length; index++) mask[index] = alpha[index] > 24 ? 1 : 0;
  }
  return { mask, pixelDistance };
}

function distanceField(mask: Uint8Array, width: number, height: number) {
  const result = new Float32Array(mask.length);
  result.fill(Number.POSITIVE_INFINITY);
  for (let index = 0; index < mask.length; index++) {
    if (!mask[index]) result[index] = 0;
  }
  const diagonal = Math.SQRT2;
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const index = y * width + x;
      if (!mask[index]) continue;
      if (x > 0) result[index] = Math.min(result[index], result[index - 1] + 1);
      if (y > 0) result[index] = Math.min(result[index], result[index - width] + 1);
      if (x > 0 && y > 0) result[index] = Math.min(result[index], result[index - width - 1] + diagonal);
      if (x + 1 < width && y > 0) result[index] = Math.min(result[index], result[index - width + 1] + diagonal);
    }
  }
  for (let y = height - 1; y >= 0; y--) {
    for (let x = width - 1; x >= 0; x--) {
      const index = y * width + x;
      if (!mask[index]) continue;
      if (x + 1 < width) result[index] = Math.min(result[index], result[index + 1] + 1);
      if (y + 1 < height) result[index] = Math.min(result[index], result[index + width] + 1);
      if (x + 1 < width && y + 1 < height) result[index] = Math.min(result[index], result[index + width + 1] + diagonal);
      if (x > 0 && y + 1 < height) result[index] = Math.min(result[index], result[index + width - 1] + diagonal);
    }
  }
  return result;
}

function sampleScalar(source: SampledDepth, x: number, y: number, width: number, height: number) {
  const sx = clamp(Math.round((x + 0.5) / width * source.width - 0.5), 0, source.width - 1);
  const sy = clamp(Math.round((y + 0.5) / height * source.height - 0.5), 0, source.height - 1);
  return source.data[sy * source.width + sx];
}

function normalizedDepth(source: SampledDepth | undefined, mask: Uint8Array, width: number, height: number) {
  if (!source) return null;
  const sampled = new Float32Array(width * height);
  const values: number[] = [];
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const index = y * width + x;
      sampled[index] = sampleScalar(source, x, y, width, height);
      if (mask[index] && Number.isFinite(sampled[index])) values.push(sampled[index]);
    }
  }
  if (!values.length) return null;
  values.sort((a, b) => a - b);
  const low = values[Math.floor(values.length * 0.05)];
  const high = values[Math.floor(values.length * 0.95)];
  const range = Math.max(1e-5, high - low);
  for (let index = 0; index < sampled.length; index++) {
    sampled[index] = clamp((sampled[index] - low) / range, 0, 1);
  }
  return sampled;
}

type ImageCell = {
  color: BrickPaletteColor;
  depth: number;
  rgb: readonly [number, number, number];
};

function analyzeImage(
  data: Uint8ClampedArray,
  width: number,
  height: number,
  options: ImageBrickOptions,
): { cells: (ImageCell | null)[]; mask: Uint8Array; background: [number, number, number] } {
  if (width < 1 || height < 1 || data.length !== width * height * 4) {
    throw new Error('Invalid image pixel data');
  }
  const maxDepth = clamp(Math.round(options.maxDepth), 1, 32);
  const maxColors = clamp(Math.round(options.maxColors), 2, brickPalette.length);
  const background = estimateBackground(data, width, height);
  const foreground = options.removeBackground
    ? foregroundMask(data, width, height, background, options.backgroundThreshold)
    : {
        mask: Uint8Array.from({ length: width * height }, (_, index) => data[index * 4 + 3] > 24 ? 1 : 0),
        pixelDistance: new Float32Array(width * height),
      };
  const pixels = Array.from({ length: width * height }, (_, index) => {
    const offset = index * 4;
    const rgb = [data[offset], data[offset + 1], data[offset + 2]] as const;
    return {
      rgb,
      backgroundDistance: foreground.pixelDistance[index],
      occupied: Boolean(foreground.mask[index]),
    };
  });
  const frequency = new Map<string, number>();
  for (const pixel of pixels) {
    if (!pixel.occupied) continue;
    const match = nearestColor(pixel.rgb);
    frequency.set(match.id, (frequency.get(match.id) ?? 0) + 1);
  }
  const selectedIds = [...frequency.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, maxColors)
    .map(([id]) => id);
  const selectedPalette = paletteLab.filter(item => selectedIds.includes(item.color.id));
  return {
    background,
    mask: foreground.mask,
    cells: pixels.map(pixel => {
      if (!pixel.occupied) return null;
      const color = nearestColor(pixel.rgb, selectedPalette.length ? selectedPalette : paletteLab);
      const lightness = rgbToLab(pixel.rgb)[0] / 100;
      const relief = clamp(pixel.backgroundDistance / 65, 0, 1) * 0.35 + (1 - lightness) * 0.65;
      return { color, depth: 1 + Math.round(relief * (maxDepth - 1)), rgb: pixel.rgb };
    }),
  };
}

function buildFromVoxels(
  voxels: Map<string, BrickPaletteColor>,
  width: number,
  height: number,
  depth: number,
  options: ImageBrickOptions,
  name: string,
  background: [number, number, number],
  viewCount: number,
  sourceWidth = width,
  sourceHeight = height,
  reconstruction: ImageBrickBuild['reconstruction'] = 'shape-inflation',
): ImageBrickBuild {
  const bandSize = 3;
  const depthBands = Math.ceil(depth / bandSize);
  const bricks: ImageBrick[] = [];
  const visited = new Set<string>();
  let brickIndex = 0;
  for (let level = 0; level < height; level++) {
    for (let row = 0; row < depth; row++) {
      for (let column = 0; column < width; column++) {
        const originKey = `${column}:${level}:${row}`;
        if (visited.has(originKey)) continue;
        const color = voxels.get(`${column}:${level}:${row}`);
        if (!color) continue;
        const reverse = options.bond === 'running'
          ? (level + row) % 2 === 1
          : options.bond === 'reinforced' && level % 2 === 1;
        const candidates: [number, number][] = reverse
          ? [[2, 2], [4, 2], [3, 2], [2, 1], [4, 1], [3, 1], [1, 1]]
          : [[4, 2], [3, 2], [2, 2], [4, 1], [3, 1], [2, 1], [1, 1]];
        const allowed = options.bond === 'reinforced' && (level + row) % 3 === 0
          ? candidates.filter(([candidateWidth]) => candidateWidth <= 2)
          : candidates;
        const footprint = allowed.find(([candidateWidth, candidateDepth]) => {
          if (column + candidateWidth > width || row + candidateDepth > depth) return false;
          for (let dz = 0; dz < candidateDepth; dz++) {
            for (let dx = 0; dx < candidateWidth; dx++) {
              const key = `${column + dx}:${level}:${row + dz}`;
              if (visited.has(key) || voxels.get(key)?.id !== color.id) return false;
            }
          }
          return true;
        }) ?? [1, 1];
        const [brickWidth, brickDepth] = footprint;
        for (let dz = 0; dz < brickDepth; dz++) {
          for (let dx = 0; dx < brickWidth; dx++) {
            visited.add(`${column + dx}:${level}:${row + dz}`);
          }
        }
        brickIndex++;
        const step = level * depthBands + Math.floor(row / bandSize) + 1;
        bricks.push({
          id: `image_brick_${String(brickIndex).padStart(5, '0')}`,
          partId: partByFootprint[`${brickWidth}x${brickDepth}`],
          width: brickWidth,
          depth: brickDepth,
          x: column + brickWidth / 2 - width / 2,
          y: level * 1.2 + 0.6,
          z: row + brickDepth / 2 - depth / 2,
          colorId: color.id,
          colorCode: color.code,
          colorHex: color.hex,
          step,
        });
      }
    }
  }
  const rawStepIds = [...new Set(bricks.map(brick => brick.step))].sort((a, b) => a - b);
  const steps = rawStepIds.map((rawId, index) => {
    const layer = Math.floor((rawId - 1) / depthBands);
    const band = (rawId - 1) % depthBands;
    return {
      id: index + 1,
      layer,
      rowStart: band * bandSize,
      rowEnd: Math.min(depth, (band + 1) * bandSize) - 1,
      brickIds: bricks.filter(brick => brick.step === rawId).map(brick => brick.id),
    };
  });
  const stepIds = new Map(rawStepIds.map((id, index) => [id, index + 1]));
  for (const brick of bricks) brick.step = stepIds.get(brick.step)!;
  const bomMap = new Map<string, ImageBrickBomItem>();
  for (const brick of bricks) {
    const key = `${brick.partId}:${brick.colorId}`;
    const color = brickPalette.find(item => item.id === brick.colorId)!;
    const item = bomMap.get(key);
    if (item) item.quantity++;
    else bomMap.set(key, {
      key,
      partId: brick.partId,
      width: brick.width,
      depth: brick.depth,
      colorId: brick.colorId,
      colorCode: brick.colorCode,
      colorHex: brick.colorHex,
      colorNameZh: color.nameZh,
      colorNameEn: color.nameEn,
      quantity: 1,
    });
  }
  const backgroundHex = `#${background.map(value => value.toString(16).padStart(2, '0')).join('')}`;
  return {
    name,
    width,
    height,
    maxDepth: depth,
    method: options.method,
    bond: options.bond,
    viewCount,
    brickBudget: options.brickBudget,
    sourceWidth,
    sourceHeight,
    backgroundHex,
    reconstruction,
    bricks,
    steps,
    bom: [...bomMap.values()].sort((a, b) => b.quantity - a.quantity || a.key.localeCompare(b.key)),
  };
}

function cellAt(
  analysis: ReturnType<typeof analyzeImage>,
  image: SampledImage,
  x: number,
  y: number,
  targetWidth: number,
  targetHeight: number,
  flipX = false,
) {
  let sourceX = clamp(Math.floor((x + 0.5) / targetWidth * image.width), 0, image.width - 1);
  if (flipX) sourceX = image.width - sourceX - 1;
  const sourceY = clamp(Math.floor((y + 0.5) / targetHeight * image.height), 0, image.height - 1);
  return analysis.cells[sourceY * image.width + sourceX];
}

function applySharedPalette(voxels: Map<string, BrickPaletteColor>, maxColors: number) {
  const frequency = new Map<string, number>();
  for (const color of voxels.values()) frequency.set(color.id, (frequency.get(color.id) ?? 0) + 1);
  const selected = new Set(
    [...frequency]
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, clamp(Math.round(maxColors), 2, brickPalette.length))
      .map(([id]) => id),
  );
  const palette = paletteLab.filter(item => selected.has(item.color.id));
  for (const [key, color] of voxels) {
    if (!selected.has(color.id)) voxels.set(key, nearestColor(hexToRgb(color.hex), palette));
  }
}

function hollowVolume(voxels: Map<string, BrickPaletteColor>) {
  if (!voxels.size) return;
  const solid = new Set(voxels.keys());
  for (const key of [...voxels.keys()]) {
    const [x, y, z] = key.split(':').map(Number);
    const enclosed = [
      `${x - 1}:${y}:${z}`, `${x + 1}:${y}:${z}`,
      `${x}:${y - 1}:${z}`, `${x}:${y + 1}:${z}`,
      `${x}:${y}:${z - 1}`, `${x}:${y}:${z + 1}`,
    ].every(neighbor => solid.has(neighbor));
    if (enclosed) voxels.delete(key);
  }
}

function trimVoxels(voxels: Map<string, BrickPaletteColor>, fallback: [number, number, number]) {
  if (!voxels.size) {
    return { voxels, width: fallback[0], height: fallback[1], depth: fallback[2] };
  }
  const coordinates = [...voxels.keys()].map(key => key.split(':').map(Number));
  const min = [0, 1, 2].map(axis => Math.min(...coordinates.map(point => point[axis])));
  const max = [0, 1, 2].map(axis => Math.max(...coordinates.map(point => point[axis])));
  return {
    width: max[0] - min[0] + 1,
    height: max[1] - min[1] + 1,
    depth: max[2] - min[2] + 1,
    voxels: new Map([...voxels].map(([key, color]) => {
      const [x, y, z] = key.split(':').map(Number);
      return [`${x - min[0]}:${y - min[1]}:${z - min[2]}`, color];
    })),
  };
}

export function createBrickModelFromViews(
  views: ImageBrickViews,
  options: ImageBrickOptions,
  name = 'Image sculpture',
): ImageBrickBuild {
  const { front } = views;
  const width = clamp(Math.round(options.width), 12, 48);
  if (front.width !== width || front.height < 1) {
    throw new Error(`Front view must already be sampled to ${width}px wide`);
  }
  const frontAnalysis = analyzeImage(front.data, front.width, front.height, options);
  const height = front.height;
  const depth = options.method === 'relief'
    ? clamp(Math.round(options.maxDepth), 1, 8)
    : clamp(Math.round(options.maxDepth), 4, width);
  const left = views.left ? analyzeImage(views.left.data, views.left.width, views.left.height, options) : null;
  const back = views.back ? analyzeImage(views.back.data, views.back.width, views.back.height, options) : null;
  const right = views.right ? analyzeImage(views.right.data, views.right.width, views.right.height, options) : null;
  const viewCount = 1 + Number(Boolean(left)) + Number(Boolean(back)) + Number(Boolean(right));
  const voxels = new Map<string, BrickPaletteColor>();
  const shapeDistance = distanceField(frontAnalysis.mask, width, height);
  const maximumDistance = Math.max(1, ...shapeDistance.filter(Number.isFinite));
  const aiDepth = normalizedDepth(views.frontDepth, frontAnalysis.mask, width, height);
  if (aiDepth) {
    for (let pass = 0; pass < 2; pass++) {
      const source = aiDepth.slice();
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          const index = y * width + x;
          if (!frontAnalysis.mask[index]) continue;
          let total = 0;
          let count = 0;
          for (let dy = -1; dy <= 1; dy++) {
            for (let dx = -1; dx <= 1; dx++) {
              const nx = x + dx;
              const ny = y + dy;
              if (nx < 0 || nx >= width || ny < 0 || ny >= height) continue;
              const neighbor = ny * width + nx;
              if (!frontAnalysis.mask[neighbor]) continue;
              total += source[neighbor];
              count++;
            }
          }
          if (count) aiDepth[index] = total / count;
        }
      }
    }
  }

  for (let sourceRow = 0; sourceRow < height; sourceRow++) {
    const level = height - sourceRow - 1;
    for (let x = 0; x < width; x++) {
      const index = sourceRow * width + x;
      const frontCell = frontAnalysis.cells[index];
      if (!frontCell) continue;
      const shapeRadius = Math.pow(clamp(shapeDistance[index] / maximumDistance, 0, 1), 0.68);
      const estimatedDepth = aiDepth?.[index] ?? 0.5;
      for (let z = 0; z < depth; z++) {
        let occupied: boolean;
        const colors: (readonly number[])[] = [frontCell.rgb];
        if (options.method === 'relief') {
          occupied = z < Math.min(depth, frontCell.depth);
        } else if (viewCount > 1) {
          const leftCell = left && cellAt(left, views.left!, depth - z - 1, sourceRow, depth, height);
          const rightCell = right && cellAt(right, views.right!, z, sourceRow, depth, height);
          const backCell = back && cellAt(back, views.back!, width - x - 1, sourceRow, width, height);
          occupied = Boolean((!left || leftCell) && (!right || rightCell) && (!back || backCell));
          if (leftCell) colors.push(leftCell.rgb);
          if (rightCell) colors.push(rightCell.rgb);
          if (backCell) colors.push(backCell.rgb);
        } else if (aiDepth && options.method === 'hollow') {
          const surface = Math.round((1 - estimatedDepth) * Math.max(1, depth - 3));
          const thickness = shapeRadius > 0.58 ? 3 : 2;
          occupied = z >= surface && z < Math.min(depth, surface + thickness);
        } else {
          const halfDepth = Math.max(
            1,
            Math.round((0.12 + shapeRadius * 0.88) * (depth / 2) * (0.78 + estimatedDepth * 0.44)),
          );
          const center = (depth - 1) / 2 + Math.round((estimatedDepth - 0.5) * depth * 0.22);
          occupied = z >= Math.floor(center - halfDepth) && z <= Math.ceil(center + halfDepth);
        }
        if (!occupied) continue;
        const rgb = [0, 1, 2].map(channel =>
          Math.round(colors.reduce((sum, color) => sum + color[channel], 0) / colors.length),
        );
        voxels.set(`${x}:${level}:${z}`, nearestColor(rgb));
      }
    }
  }

  applySharedPalette(voxels, options.maxColors);
  if (options.method === 'hollow' && !(aiDepth && viewCount === 1)) hollowVolume(voxels);
  const trimmed = trimVoxels(voxels, [width, height, depth]);

  const build = buildFromVoxels(
    trimmed.voxels,
    trimmed.width,
    trimmed.height,
    trimmed.depth,
    options,
    name,
    frontAnalysis.background,
    viewCount,
    front.width,
    front.height,
    options.method === 'relief'
      ? 'relief'
      : viewCount > 1
        ? 'multi-view'
        : views.frontDepth
          ? 'depth-ai'
          : 'shape-inflation',
  );
  if (views.frontDepth) {
    build.credits = [
      'Depth Anything V2 Small ONNX, Apache-2.0, revision 4472b7362082ad9968fee890ca0f1e5aca36b93d',
    ];
  }
  return build;
}

export function createBrickModelFromMeshVolume(
  volume: SampledMeshVolume,
  front: SampledImage,
  options: ImageBrickOptions,
  name = 'AI mesh sculpture',
  credit = 'Public image-to-3D mesh',
): ImageBrickBuild {
  if (
    volume.width < 1
    || volume.height < 1
    || volume.depth < 1
    || volume.occupied.length !== volume.width * volume.height * volume.depth
  ) {
    throw new Error('Invalid mesh voxel volume');
  }
  const analysis = analyzeImage(front.data, front.width, front.height, {
    ...options,
    removeBackground: false,
  });
  const fallback = analysis.cells.find((cell): cell is ImageCell => Boolean(cell))?.color
    ?? brickPalette.find(color => color.id === 'light-gray')!;
  const voxels = new Map<string, BrickPaletteColor>();
  for (let y = 0; y < volume.height; y++) {
    for (let z = 0; z < volume.depth; z++) {
      for (let x = 0; x < volume.width; x++) {
        const index = (y * volume.depth + z) * volume.width + x;
        if (!volume.occupied[index]) continue;
        const sourceX = clamp(
          Math.floor((x + 0.5) / volume.width * front.width),
          0,
          front.width - 1,
        );
        const sourceY = clamp(
          Math.floor((1 - (y + 0.5) / volume.height) * front.height),
          0,
          front.height - 1,
        );
        voxels.set(
          `${x}:${y}:${z}`,
          analysis.cells[sourceY * front.width + sourceX]?.color ?? fallback,
        );
      }
    }
  }
  applySharedPalette(voxels, options.maxColors);
  const trimmed = trimVoxels(voxels, [
    volume.width,
    volume.height,
    volume.depth,
  ]);
  const build = buildFromVoxels(
    trimmed.voxels,
    trimmed.width,
    trimmed.height,
    trimmed.depth,
    options,
    name,
    analysis.background,
    1,
    Math.max(volume.width, volume.height, volume.depth),
    front.height,
    'mesh-ai',
  );
  build.credits = [
    credit,
    `${volume.triangleCount.toLocaleString('en-US')} source triangles; ${volume.solidVoxelCount.toLocaleString('en-US')} solid voxels`,
  ];
  return build;
}

export function createEmptyBrickBuild(): ImageBrickBuild {
  return {
    name: '',
    width: 0,
    height: 0,
    maxDepth: 0,
    method: 'hollow',
    bond: 'running',
    viewCount: 0,
    brickBudget: 0,
    sourceWidth: 0,
    sourceHeight: 0,
    backgroundHex: '#f2f4f8',
    reconstruction: 'empty',
    bricks: [],
    bom: [],
    steps: [],
  };
}

export function createBrickRelief(
  data: Uint8ClampedArray,
  sourceWidth: number,
  sourceHeight: number,
  options: ImageBrickOptions,
  name = 'Image sculpture',
): ImageBrickBuild {
  return createBrickModelFromViews({
    front: { data, width: sourceWidth, height: sourceHeight },
  }, { ...options, method: 'relief' }, name);
}

export function imageBrickBuildToLdraw(build: ImageBrickBuild) {
  const lines = [
    `0 ${build.name.replace(/[\r\n]/g, ' ')}`,
    '0 Generated by Brick Atlas Image Studio',
    '0 !LICENSE Redistributable under CC BY 4.0',
    ...(build.credits ?? []).map(credit => `0 Source attribution: ${credit.replace(/[\r\n]/g, ' ')}`),
  ];
  let previousStep = 0;
  for (const brick of [...build.bricks].sort((a, b) => a.step - b.step || a.z - b.z || a.x - b.x)) {
    if (previousStep && brick.step !== previousStep) lines.push('0 STEP');
    previousStep = brick.step;
    const matrices = [
      '1 0 0 0 1 0 0 0 1',
      '0 0 1 0 1 0 -1 0 0',
      '-1 0 0 0 1 0 0 0 -1',
      '0 0 -1 0 1 0 1 0 0',
    ];
    // LDraw origins are on the top face. A stud is 20 LDU, a brick is 24 LDU.
    const matrix = brick.ldrawMatrix;
    const n = (value: number) => Number(value.toFixed(6));
    if (matrix) {
      lines.push(`1 ${brick.colorCode} ${[matrix[12], matrix[13], matrix[14], matrix[0], matrix[4], matrix[8], matrix[1], matrix[5], matrix[9], matrix[2], matrix[6], matrix[10]].map(n).join(' ')} ${brick.partId}.dat`);
    } else {
      const turn = (4 - (brick.rotation ?? 0)) % 4;
      lines.push(`1 ${brick.colorCode} ${n(brick.x * 20)} ${n(-(brick.y + (brick.height ?? 1.2) / 2) * 20)} ${n(-brick.z * 20)} ${matrices[turn]} ${brick.partId}.dat`);
    }
  }
  return `${lines.join('\n')}\n`;
}
