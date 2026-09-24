import { Box3, Matrix4, Vector3 } from 'three';
import type { AtlasManifest, PartInstance, Vec3 } from '../model/types';

export const smoothstep = (t: number) => { const x = Math.min(1, Math.max(0, t)); return x * x * (3 - 2 * x); };
export const inventoryRotation = new Matrix4().makeRotationY(-0.65).premultiply(new Matrix4().makeRotationX(0.4));

export function groupOffset(part: PartInstance, manifest: AtlasManifest): Vec3 {
  const direction = manifest.groups.find(g => g.id === part.groupId)!.direction;
  const v: Vec3 = [...direction];
  if (part.groupId === 'wheels' || /door/.test(part.path.join(' '))) {
    v[2] = Math.sign((part.bounds.min[2] + part.bounds.max[2]) / 2 || 1) * 60;
  }
  return v;
}

export interface Cell { id: string; x: number; y: number; width: number; height: number }
export interface InventoryLayout { offsets: Map<string, Vec3>; cells: Cell[]; width: number; height: number }

export function inventoryLayout(parts: PartInstance[], aspect: number): InventoryLayout {
  const rotationInverse = inventoryRotation.clone().invert();
  const padding = 7;
  const items = parts.map(part => {
    const box = new Box3(new Vector3(...part.bounds.min), new Vector3(...part.bounds.max)).applyMatrix4(inventoryRotation);
    const size = box.getSize(new Vector3());
    return { part, box, width: Math.max(size.x, 9) + padding, height: Math.max(size.y, 9) + padding };
  }).sort((a, b) => b.height - a.height || a.part.instanceId.localeCompare(b.part.instanceId));
  const area = items.reduce((sum, item) => sum + item.width * item.height, 0);
  const width = Math.max(...items.map(i => i.width), Math.sqrt(area * Math.max(0.4, aspect)) * 1.08, 1);
  const cells: Cell[] = [];
  let x = 0, y = 0, rowHeight = 0, usedWidth = 0;
  for (const item of items) {
    if (x + item.width > width && x > 0) { y += rowHeight; x = 0; rowHeight = 0; }
    cells.push({ id: item.part.instanceId, x, y, width: item.width, height: item.height });
    x += item.width;
    usedWidth = Math.max(usedWidth, x);
    rowHeight = Math.max(rowHeight, item.height);
  }
  const height = y + rowHeight;
  const offsets = new Map<string, Vec3>();
  items.forEach((item, i) => {
    const cell = cells[i];
    const center = item.box.getCenter(new Vector3());
    const target = new Vector3(cell.x + cell.width / 2 - usedWidth / 2, height / 2 - cell.y - cell.height / 2, 0);
    const offset = target.sub(center).applyMatrix4(rotationInverse);
    offsets.set(item.part.instanceId, offset.toArray() as Vec3);
  });
  return { offsets, cells, width: usedWidth, height };
}

export function explosionOffset(part: PartInstance, e: number, manifest: AtlasManifest, inventory: InventoryLayout): Vec3 {
  if (e <= 0) return [0, 0, 0];
  const group = groupOffset(part, manifest);
  if (e <= 0.45) {
    const t = smoothstep(e / 0.45);
    return group.map(v => v * t) as Vec3;
  }
  const target = inventory.offsets.get(part.instanceId) ?? group;
  const t = smoothstep((e - 0.45) / 0.55);
  return group.map((v, i) => v + (target[i] - v) * t) as Vec3;
}
