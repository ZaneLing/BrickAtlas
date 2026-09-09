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
export interface ImageBrickViews {
  front: SampledImage;
  top?: SampledImage;
  side?: SampledImage;
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

const partByWidth: Record<1 | 2 | 3 | 4, string> = {
  1: '3005',
  2: '3004',
  3: '3622',
  4: '3010',
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
  const points = [
    [0, 0], [width - 1, 0], [0, height - 1], [width - 1, height - 1],
    [Math.min(1, width - 1), Math.min(1, height - 1)],
    [Math.max(0, width - 2), Math.min(1, height - 1)],
    [Math.min(1, width - 1), Math.max(0, height - 2)],
    [Math.max(0, width - 2), Math.max(0, height - 2)],
  ];
  const total = points.reduce((sum, [x, y]) => {
    const offset = (y * width + x) * 4;
    return [sum[0] + data[offset], sum[1] + data[offset + 1], sum[2] + data[offset + 2]];
  }, [0, 0, 0]);
  return total.map(value => Math.round(value / points.length)) as [number, number, number];
}

function partitionRun(start: number, end: number, reverse: boolean, maxWidth = 4) {
  const widths: (1 | 2 | 3 | 4)[] = [];
  let remaining = end - start;
  if (reverse && remaining > 1) {
    const width = Math.min(2, remaining - 1) as 1 | 2;
    widths.push(width);
    remaining -= width;
  }
  while (remaining > 0) {
    const width = Math.min(maxWidth, remaining) as 1 | 2 | 3 | 4;
    widths.push(width);
    remaining -= width;
  }
  const segments: { start: number; width: 1 | 2 | 3 | 4 }[] = [];
  let cursor = start;
  for (const width of widths) {
    segments.push({ start: cursor, width });
    cursor += width;
  }
  return segments;
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
): { cells: (ImageCell | null)[]; background: [number, number, number] } {
  if (width < 1 || height < 1 || data.length !== width * height * 4) {
    throw new Error('Invalid image pixel data');
  }
  const maxDepth = clamp(Math.round(options.maxDepth), 1, 6);
  const maxColors = clamp(Math.round(options.maxColors), 2, brickPalette.length);
  const background = estimateBackground(data, width, height);
  const backgroundLab = rgbToLab(background);
  const pixels = Array.from({ length: width * height }, (_, index) => {
    const offset = index * 4;
    const rgb = [data[offset], data[offset + 1], data[offset + 2]] as const;
    const alpha = data[offset + 3];
    const backgroundDistance = distance(rgbToLab(rgb), backgroundLab);
    return {
      rgb,
      alpha,
      backgroundDistance,
      occupied: alpha > 24 && (!options.removeBackground || backgroundDistance >= options.backgroundThreshold),
    };
  });
  if (pixels.filter(pixel => pixel.occupied).length < Math.max(4, pixels.length * 0.025)) {
    for (const pixel of pixels) pixel.occupied = pixel.alpha > 24;
  }
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
    cells: pixels.map(pixel => {
    if (!pixel.occupied) return null;
    const color = nearestColor(pixel.rgb, selectedPalette.length ? selectedPalette : paletteLab);
    const lightness = rgbToLab(pixel.rgb)[0] / 100;
    const relief = clamp(pixel.backgroundDistance / 65, 0, 1) * 0.45 + (1 - lightness) * 0.55;
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
) {
  const bandSize = 3;
  const depthBands = Math.ceil(depth / bandSize);
  const bricks: ImageBrick[] = [];
  let brickIndex = 0;
  for (let level = 0; level < height; level++) {
    for (let row = 0; row < depth; row++) {
      let column = 0;
      while (column < width) {
        const color = voxels.get(`${column}:${level}:${row}`);
        if (!color) {
          column++;
          continue;
        }
        let end = column + 1;
        while (end < width) {
          const next = voxels.get(`${end}:${level}:${row}`);
          if (!next || next.id !== color.id) break;
          end++;
        }
        const reverse = options.bond === 'running'
          ? (level + row) % 2 === 1
          : options.bond === 'reinforced' && level % 2 === 1;
        const maxWidth = options.bond === 'reinforced' && (level + row) % 3 === 0 ? 2 : 4;
        for (const segment of partitionRun(column, end, reverse, maxWidth)) {
          brickIndex++;
          const step = level * depthBands + Math.floor(row / bandSize) + 1;
          bricks.push({
            id: `image_brick_${String(brickIndex).padStart(5, '0')}`,
            partId: partByWidth[segment.width],
            width: segment.width,
            x: segment.start + segment.width / 2 - width / 2,
            y: level * 1.2 + 0.6,
            z: row - depth / 2 + 0.5,
            colorId: color.id,
            colorCode: color.code,
            colorHex: color.hex,
            step,
          });
        }
        column = end;
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
    bricks,
    steps,
    bom: [...bomMap.values()].sort((a, b) => b.quantity - a.quantity || a.key.localeCompare(b.key)),
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
  const requestedDepth = options.method === 'relief'
    ? clamp(Math.round(options.maxDepth), 1, 6)
    : width;
  const top = views.top ? analyzeImage(views.top.data, views.top.width, views.top.height, options) : null;
  const side = views.side ? analyzeImage(views.side.data, views.side.width, views.side.height, options) : null;
  const depth = Math.max(1, Math.min(requestedDepth, views.top?.height ?? width, views.side?.width ?? width));
  const voxels = new Map<string, BrickPaletteColor>();

  for (let sourceRow = 0; sourceRow < height; sourceRow++) {
    const level = height - sourceRow - 1;
    for (let x = 0; x < width; x++) {
      const frontCell = frontAnalysis.cells[sourceRow * width + x];
      if (!frontCell) continue;
      for (let z = 0; z < depth; z++) {
        let occupied = z < frontCell.depth;
        const colors: (readonly number[])[] = [frontCell.rgb];
        if (options.method !== 'relief') {
          const topCell = top?.cells[z * views.top!.width + x];
          const sideCell = side?.cells[sourceRow * views.side!.width + z];
          occupied = Boolean(frontCell && (!top || topCell) && (!side || sideCell));
          if (topCell) colors.push(topCell.rgb);
          if (sideCell) colors.push(sideCell.rgb);
        }
        if (!occupied) continue;
        const rgb = [0, 1, 2].map(channel =>
          Math.round(colors.reduce((sum, color) => sum + color[channel], 0) / colors.length),
        );
        voxels.set(`${x}:${level}:${z}`, nearestColor(rgb));
      }
    }
  }

  // Apply a single shared palette after view fusion, not a separate palette per photo.
  const frequency = new Map<string, number>();
  for (const color of voxels.values()) frequency.set(color.id, (frequency.get(color.id) ?? 0) + 1);
  const selected = new Set([...frequency].sort((a, b) => b[1] - a[1]).slice(0, options.maxColors).map(([id]) => id));
  const palette = paletteLab.filter(item => selected.has(item.color.id));
  for (const [key, color] of voxels) {
    if (!selected.has(color.id)) voxels.set(key, nearestColor(hexToRgb(color.hex), palette));
  }

  if (options.method === 'hollow' && voxels.size) {
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

  let modelVoxels = voxels;
  let modelWidth = width;
  let modelHeight = height;
  let modelDepth = depth;
  if (voxels.size) {
    const coordinates = [...voxels.keys()].map(key => key.split(':').map(Number));
    const min = [0, 1, 2].map(axis => Math.min(...coordinates.map(point => point[axis])));
    const max = [0, 1, 2].map(axis => Math.max(...coordinates.map(point => point[axis])));
    modelWidth = max[0] - min[0] + 1;
    modelHeight = max[1] - min[1] + 1;
    modelDepth = max[2] - min[2] + 1;
    modelVoxels = new Map([...voxels].map(([key, color]) => {
      const [x, y, z] = key.split(':').map(Number);
      return [`${x - min[0]}:${y - min[1]}:${z - min[2]}`, color];
    }));
  }

  return buildFromVoxels(
    modelVoxels,
    modelWidth,
    modelHeight,
    modelDepth,
    options,
    name,
    frontAnalysis.background,
    1 + Number(Boolean(top)) + Number(Boolean(side)),
    front.width,
    front.height,
  );
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

export function createDemoBrickBuild() {
  const pattern = [
    '.......YYYY.........',
    '......YYYYYY........',
    '..RRRRBBBBBBBBRR....',
    '.RRRRRWWBBBBWWRRR...',
    'RRRRRRBBBBBBBBRRRR..',
    'RRRRRRRRRRRRRRRRRR..',
    '...KKK......KKK.....',
    '..KKKKK....KKKKK....',
  ];
  const colors: Record<string, readonly [number, number, number]> = {
    '.': [245, 246, 248],
    R: [201, 26, 9],
    B: [0, 85, 191],
    Y: [242, 205, 55],
    W: [244, 244, 244],
    K: [5, 19, 29],
  };
  const data = new Uint8ClampedArray(pattern.length * pattern[0].length * 4);
  pattern.forEach((row, y) => [...row].forEach((token, x) => {
    const offset = (y * row.length + x) * 4;
    data.set([...colors[token], token === '.' ? 0 : 255], offset);
  }));
  return createBrickRelief(data, pattern[0].length, pattern.length, {
    width: pattern[0].length,
    maxDepth: 3,
    maxColors: 6,
    removeBackground: true,
    backgroundThreshold: 12,
    method: 'relief',
    bond: 'running',
    brickBudget: 1200,
  }, 'Brick Atlas demo');
}
