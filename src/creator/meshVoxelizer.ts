export interface MeshVoxelVolume {
  width: number;
  height: number;
  depth: number;
  occupied: Uint8Array;
  triangleCount: number;
  surfaceVoxelCount: number;
  solidVoxelCount: number;
}

export interface MeshVoxelizeOptions {
  resolution: number;
  hollow: boolean;
}

type Point = [number, number, number];

const clamp = (value: number, min: number, max: number) =>
  Math.max(min, Math.min(max, value));

function voxelIndex(
  x: number,
  y: number,
  z: number,
  width: number,
  depth: number,
) {
  return (y * depth + z) * width + x;
}

function distance(a: Point, b: Point) {
  return Math.hypot(
    a[0] - b[0],
    a[1] - b[1],
    a[2] - b[2],
  );
}

function projectedIntersectionX(
  pointY: number,
  pointZ: number,
  a: Point,
  b: Point,
  c: Point,
) {
  const denominator =
    (b[2] - c[2]) * (a[1] - c[1])
    + (c[1] - b[1]) * (a[2] - c[2]);
  if (Math.abs(denominator) < 1e-8) return null;
  const u = (
    (b[2] - c[2]) * (pointY - c[1])
    + (c[1] - b[1]) * (pointZ - c[2])
  ) / denominator;
  const v = (
    (c[2] - a[2]) * (pointY - c[1])
    + (a[1] - c[1]) * (pointZ - c[2])
  ) / denominator;
  const w = 1 - u - v;
  const epsilon = -1e-6;
  return u >= epsilon && v >= epsilon && w >= epsilon
    ? u * a[0] + v * b[0] + w * c[0]
    : null;
}

function countOccupied(values: Uint8Array) {
  let count = 0;
  for (const value of values) count += Number(Boolean(value));
  return count;
}

export function voxelizeMeshTriangles(
  positions: Float32Array,
  options: MeshVoxelizeOptions,
): MeshVoxelVolume {
  if (!positions.length || positions.length % 9 !== 0) {
    throw new Error('Mesh triangle data is empty or malformed');
  }
  const resolution = clamp(Math.round(options.resolution), 12, 48);
  const min: Point = [Infinity, Infinity, Infinity];
  const max: Point = [-Infinity, -Infinity, -Infinity];
  for (let index = 0; index < positions.length; index += 3) {
    for (let axis = 0; axis < 3; axis++) {
      const value = positions[index + axis];
      if (!Number.isFinite(value)) throw new Error('Mesh contains non-finite coordinates');
      min[axis] = Math.min(min[axis], value);
      max[axis] = Math.max(max[axis], value);
    }
  }
  const extent: Point = [
    max[0] - min[0],
    max[1] - min[1],
    max[2] - min[2],
  ];
  const maximumExtent = Math.max(...extent);
  if (maximumExtent <= 1e-8) throw new Error('Mesh has no measurable volume');
  const scale = (resolution - 3) / maximumExtent;
  const width = Math.max(3, Math.ceil(extent[0] * scale) + 2);
  const height = Math.max(3, Math.ceil(extent[1] * scale) + 2);
  const depth = Math.max(3, Math.ceil(extent[2] * scale) + 2);
  const vertices = new Float32Array(positions.length);
  for (let index = 0; index < positions.length; index += 3) {
    vertices[index] = 1 + (positions[index] - min[0]) * scale;
    vertices[index + 1] = 1 + (positions[index + 1] - min[1]) * scale;
    vertices[index + 2] = 1 + (positions[index + 2] - min[2]) * scale;
  }

  const surface = new Uint8Array(width * height * depth);
  const rayBins = Array.from(
    { length: height * depth },
    () => [] as number[],
  );
  const triangleCount = vertices.length / 9;
  for (let triangle = 0; triangle < triangleCount; triangle++) {
    const offset = triangle * 9;
    const a: Point = [
      vertices[offset],
      vertices[offset + 1],
      vertices[offset + 2],
    ];
    const b: Point = [
      vertices[offset + 3],
      vertices[offset + 4],
      vertices[offset + 5],
    ];
    const c: Point = [
      vertices[offset + 6],
      vertices[offset + 7],
      vertices[offset + 8],
    ];
    const steps = clamp(
      Math.ceil(Math.max(distance(a, b), distance(b, c), distance(c, a)) * 2),
      1,
      72,
    );
    for (let row = 0; row <= steps; row++) {
      for (let column = 0; column <= steps - row; column++) {
        const u = row / steps;
        const v = column / steps;
        const w = 1 - u - v;
        const x = clamp(Math.floor(a[0] * w + b[0] * u + c[0] * v), 0, width - 1);
        const y = clamp(Math.floor(a[1] * w + b[1] * u + c[1] * v), 0, height - 1);
        const z = clamp(Math.floor(a[2] * w + b[2] * u + c[2] * v), 0, depth - 1);
        surface[voxelIndex(x, y, z, width, depth)] = 1;
      }
    }
    const minY = clamp(Math.floor(Math.min(a[1], b[1], c[1])), 0, height - 1);
    const maxY = clamp(Math.ceil(Math.max(a[1], b[1], c[1])), 0, height - 1);
    const minZ = clamp(Math.floor(Math.min(a[2], b[2], c[2])), 0, depth - 1);
    const maxZ = clamp(Math.ceil(Math.max(a[2], b[2], c[2])), 0, depth - 1);
    for (let y = minY; y <= maxY; y++) {
      for (let z = minZ; z <= maxZ; z++) {
        rayBins[y * depth + z].push(triangle);
      }
    }
  }

  const solid = surface.slice();
  for (let y = 0; y < height; y++) {
    for (let z = 0; z < depth; z++) {
      const intersections: number[] = [];
      for (const triangle of rayBins[y * depth + z]) {
        const offset = triangle * 9;
        const point = projectedIntersectionX(
          y + 0.5,
          z + 0.5,
          [vertices[offset], vertices[offset + 1], vertices[offset + 2]],
          [vertices[offset + 3], vertices[offset + 4], vertices[offset + 5]],
          [vertices[offset + 6], vertices[offset + 7], vertices[offset + 8]],
        );
        if (point !== null) intersections.push(point);
      }
      intersections.sort((a, b) => a - b);
      const unique = intersections.filter(
        (value, index) => index === 0 || Math.abs(value - intersections[index - 1]) > 1e-3,
      );
      for (let pair = 0; pair + 1 < unique.length; pair += 2) {
        const start = clamp(Math.ceil(unique[pair] - 0.5), 0, width - 1);
        const end = clamp(Math.floor(unique[pair + 1] - 0.5), 0, width - 1);
        for (let x = start; x <= end; x++) {
          solid[voxelIndex(x, y, z, width, depth)] = 1;
        }
      }
    }
  }

  const occupied = options.hollow ? new Uint8Array(solid.length) : solid;
  if (options.hollow) {
    for (let y = 0; y < height; y++) {
      for (let z = 0; z < depth; z++) {
        for (let x = 0; x < width; x++) {
          const index = voxelIndex(x, y, z, width, depth);
          if (!solid[index]) continue;
          const boundary = x === 0 || x === width - 1
            || y === 0 || y === height - 1
            || z === 0 || z === depth - 1
            || !solid[voxelIndex(x - 1, y, z, width, depth)]
            || !solid[voxelIndex(x + 1, y, z, width, depth)]
            || !solid[voxelIndex(x, y - 1, z, width, depth)]
            || !solid[voxelIndex(x, y + 1, z, width, depth)]
            || !solid[voxelIndex(x, y, z - 1, width, depth)]
            || !solid[voxelIndex(x, y, z + 1, width, depth)];
          if (boundary || surface[index]) occupied[index] = 1;
        }
      }
    }
  }
  const solidVoxelCount = countOccupied(solid);
  if (!solidVoxelCount) throw new Error('Mesh voxelization produced no occupied cells');
  return {
    width,
    height,
    depth,
    occupied,
    triangleCount,
    surfaceVoxelCount: countOccupied(surface),
    solidVoxelCount,
  };
}
