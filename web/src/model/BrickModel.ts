import { Euler, Matrix4, Quaternion, Vector3 } from 'three';
import type { AtlasManifest, Bounds, PartInstance, Vec3 } from './types';

export interface Brick {
  id: string;
  partId: string;
  name: string;
  position: Vec3;
  rotation: Vec3;
  color: { code: string; name: string; hex: string };
  dimensions: Vec3;
  bounds: Bounds;
  assemblyId: string;
  source: { file: string; line: number };
  instance: PartInstance;
}

export class BrickModel {
  readonly bricks: readonly Brick[];
  private readonly byId: ReadonlyMap<string, Brick>;

  constructor(readonly manifest: AtlasManifest) {
    this.bricks = manifest.instances.map(instance => {
      const matrix = new Matrix4().fromArray(instance.originalMatrix);
      const position = new Vector3();
      const quaternion = new Quaternion();
      matrix.decompose(position, quaternion, new Vector3());
      const rotation = new Euler().setFromQuaternion(quaternion);
      const dimensions = new Vector3(...instance.bounds.max).sub(new Vector3(...instance.bounds.min));
      const angle = (value: number) => Math.abs(value) < 1e-12 ? 0 : value;
      return {
        id: instance.instanceId,
        partId: instance.partNumber,
        name: instance.displayName,
        position: position.toArray() as Vec3,
        rotation: [angle(rotation.x), angle(rotation.y), angle(rotation.z)],
        color: { code: instance.colorCode, name: instance.colorName, hex: instance.colorHex },
        dimensions: dimensions.toArray() as Vec3,
        bounds: instance.bounds,
        assemblyId: instance.parentSubmodelId,
        source: { file: instance.sourceFile, line: instance.sourceLine },
        instance,
      };
    });
    this.byId = new Map(this.bricks.map(brick => [brick.id, brick]));
  }

  get id() { return this.manifest.model.id; }
  getBrick(id: string) { return this.byId.get(id); }
  findByPartId(partId: string) { return this.bricks.filter(brick => brick.partId === partId); }
}
