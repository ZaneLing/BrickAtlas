import { describe, expect, it } from 'vitest';
import {
  createBrickModelFromMeshVolume,
  type ImageBrickOptions,
} from '../../src/creator/imageBrickModel';
import { voxelizeMeshTriangles } from '../../src/creator/meshVoxelizer';

const cube = Float32Array.from([
  0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0,
  0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1,
  0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0,
  1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1,
  0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1,
  0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0,
]);

const options: ImageBrickOptions = {
  width: 16,
  maxDepth: 16,
  maxColors: 4,
  removeBackground: false,
  backgroundThreshold: 18,
  method: 'solid',
  bond: 'running',
  brickBudget: 5000,
};

describe('mesh voxelization', () => {
  it('fills a closed triangle mesh and can retain only its shell', () => {
    const solid = voxelizeMeshTriangles(cube, { resolution: 16, hollow: false });
    const hollow = voxelizeMeshTriangles(cube, { resolution: 16, hollow: true });
    expect(solid.triangleCount).toBe(12);
    expect(solid.solidVoxelCount).toBeGreaterThan(solid.surfaceVoxelCount);
    expect(hollow.occupied.reduce((sum, value) => sum + value, 0))
      .toBeLessThan(solid.solidVoxelCount);
  });

  it('packs mesh voxels into a mesh-attributed brick build', () => {
    const volume = voxelizeMeshTriangles(cube, { resolution: 16, hollow: true });
    const image = {
      width: 2,
      height: 2,
      data: new Uint8ClampedArray([
        201, 26, 9, 255, 201, 26, 9, 255,
        201, 26, 9, 255, 201, 26, 9, 255,
      ]),
    };
    const build = createBrickModelFromMeshVolume(
      volume,
      image,
      { ...options, method: 'hollow' },
      'Cube',
      'Test mesh',
    );
    expect(build.reconstruction).toBe('mesh-ai');
    expect(build.bricks.length).toBeGreaterThan(0);
    expect(build.credits?.[0]).toBe('Test mesh');
  });
});
