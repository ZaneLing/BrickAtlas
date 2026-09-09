import { describe, expect, it } from 'vitest';
import { BrickModel } from '../../src/model/BrickModel';
import type { AtlasManifest } from '../../src/model/types';

const manifest = {
  version: 1,
  model: { id: 'test', title: 'Test', author: 'A', sourceUrl: '', license: '', year: 2026, notes: [] },
  sourceHash: '',
  instances: [{
    instanceId: 'brick_000001', index: 0, partNumber: '3001', displayName: 'Brick 2 x 4',
    colorCode: '4', colorName: 'Red', colorHex: '#c91a09', sourceFile: 'main.ldr', sourceLine: 8,
    parentSubmodelId: 'body', path: ['main.ldr'], buildStep: 1,
    originalMatrix: [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 10, 20, 30, 1],
    bounds: { min: [0, 0, 0], max: [32, 9.6, 16] }, category: 'Brick', tags: [], groupId: 'body',
  }],
  submodels: [], groups: [{ id: 'body', name: 'Body', color: '#f00', direction: [0, 1, 0], instanceIds: ['brick_000001'] }],
  bounds: { min: [0, 0, 0], max: [32, 9.6, 16] }, chunks: [],
  stats: { instances: 1, uniqueParts: 1, colors: 1, triangles: 0, compressedBytes: 0 },
} satisfies AtlasManifest;

describe('BrickModel', () => {
  it('owns brick identity, transform, color and dimensions outside the viewer', () => {
    const model = new BrickModel(manifest);
    const brick = model.getBrick('brick_000001')!;
    expect(model.id).toBe('test');
    expect(brick.partId).toBe('3001');
    expect(brick.position).toEqual([10, 20, 30]);
    expect(brick.rotation).toEqual([0, 0, 0]);
    expect(brick.color.code).toBe('4');
    expect(brick.dimensions).toEqual([32, 9.6, 16]);
    expect(model.findByPartId('3001')).toEqual([brick]);
  });
});
