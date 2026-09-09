import { describe, expect, it } from 'vitest';
import { Matrix4 } from 'three';
import {
  baseplateCatalog,
  canPlaceItem,
  composerAssets,
  createComposerItem,
  createCompositionBuild,
  createCompositionProject,
  rotatedFootprint,
  sourceBricksFromManifest,
  changeBaseplate, parseCompositionProject,
  type ComposerItem,
} from '../../src/composer/compositionModel';
import type { AtlasManifest } from '../../src/model/types';

function item(overrides: Partial<ComposerItem> = {}): ComposerItem {
  return {
    id: 'item_a',
    assetId: 'brick-2x4',
    nameZh: '基础砖',
    nameEn: 'Brick',
    kind: 'part',
    x: 0,
    z: 0,
    level: 0,
    rotation: 0,
    footprint: [4, 2],
    bricks: [{
      partId: '3001',
      width: 4,
      depth: 2,
      height: 1.16,
      x: 0,
      y: 0.9,
      z: 0,
      colorCode: 1,
      colorHex: '#0055bf',
    }],
    ...overrides,
  };
}

describe('composition model', () => {
  it('rotates footprints and rejects overlaps or out-of-bounds placement', () => {
    const project = { ...createCompositionProject(), items: [item()] };
    expect(rotatedFootprint(item({ rotation: 1 }))).toEqual([2, 4]);
    expect(canPlaceItem(project, item({ id: 'item_b', x: 2, z: 0 }))).toBe(false);
    expect(canPlaceItem(project, item({ id: 'item_b', x: 10, z: 10 }))).toBe(true);
    expect(canPlaceItem(project, item({ id: 'item_b', x: baseplateCatalog[0].width }))).toBe(false);
  });

  it('finds an open snapped location for a library asset', () => {
    const project = createCompositionProject();
    const asset = composerAssets.find(value => value.id === 'cat')!;
    const first = createComposerItem(project, asset);
    expect(first).not.toBeNull();
    const second = createComposerItem({ ...project, items: [first!] }, asset);
    expect(second).not.toBeNull();
    expect([second!.x, second!.z]).not.toEqual([first!.x, first!.z]);
  });

  it('creates a base-first build, BOM and stable component steps', () => {
    const project = { ...createCompositionProject(), items: [item()] };
    const build = createCompositionBuild(project);
    expect(build.steps).toHaveLength(2);
    expect(build.steps[0].brickIds.every(id => id.startsWith('base_'))).toBe(true);
    expect(build.steps[1].brickIds).toEqual(['item_a_0001']);
    expect(build.bricks.find(brick => brick.id === 'item_a_0001')).toMatchObject({
      partId: '3001',
      step: 2,
    });
    expect(build.bom.reduce((sum, entry) => sum + entry.quantity, 0)).toBe(build.bricks.length);
  });

  it('preserves source millimetres and matrices in stud coordinates', () => {
    const manifest = {
      bounds: { min: [-20, 0, -10], max: [20, 24, 10] },
      instances: [{
        partNumber: '3001',
        colorCode: '4',
        colorHex: '#c91a09',
        originalMatrix: new Matrix4().makeScale(0.4, -0.4, -0.4).toArray(),
        bounds: { min: [-20, 0, -10], max: [20, 24, 10] },
      }],
    } as unknown as AtlasManifest;
    expect(sourceBricksFromManifest(manifest)[0]).toMatchObject({
      partId: '3001',
      width: 5,
      depth: 2.5,
      height: 3,
      x: 0,
      y: 1.9,
      z: 0,
      colorCode: 4,
      colorHex: '#c91a09',
    });
    const source = sourceBricksFromManifest(manifest)[0];
    expect(source.originalMatrix?.[13]).toBe(3.2);
    const build = createCompositionBuild({ ...createCompositionProject(), items: [item({ bricks: [source] })] });
    const matrix = build.bricks.at(-1)!.ldrawMatrix!;
    expect(matrix[0]).toBeCloseTo(1);
    expect(matrix[5]).toBeCloseTo(1);
    expect(matrix[13]).toBeCloseTo(-8);
  });

  it('rejects a shrinking base without changing IDs, placement or item count', () => {
    const project = { ...createCompositionProject(), baseplateId: '64-sand', items: [item({ x: 25, rotation: 1 })] };
    expect(changeBaseplate(project, '32-gray')).toBeNull();
    expect(project.items).toEqual([item({ x: 25, rotation: 1 })]);
    const larger = changeBaseplate({ ...project, items: [item()] }, '48-blue')!;
    expect(larger.items).toEqual([item()]);
  });

  it('rejects invalid numbers and vertical interpenetration', () => {
    const project = { ...createCompositionProject(), items: [item()] };
    expect(canPlaceItem(project, item({ id: 'b', level: 1 }))).toBe(false);
    expect(canPlaceItem(project, item({ id: 'b', level: 3 }))).toBe(true);
    expect(canPlaceItem(project, item({ x: NaN }))).toBe(false);
    expect(canPlaceItem(project, item({ level: 1000 }))).toBe(false);
  });

  it('recovers malformed saved projects without passing unsafe data to the renderer', () => {
    for (const payload of ['null', '{"version":1,"items":[{}]}', '{invalid']) {
      expect(parseCompositionProject(payload).items).toEqual([]);
    }
    const project = { ...createCompositionProject(), items: [item()] };
    expect(parseCompositionProject(JSON.stringify(project))).toEqual(project);
  });

  it('uses 4x4 plate part IDs instead of 32x32 baseplate IDs', () => {
    expect(createCompositionBuild(createCompositionProject()).bricks.every(brick => brick.partId === '3031')).toBe(true);
  });
});
