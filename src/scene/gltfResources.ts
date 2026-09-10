import { LoadingManager, Mesh, type Object3D, type Texture } from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

export const GLB_SIZE_LIMIT = 120 * 1024 * 1024;

export function validateGlbBuffer(buffer: ArrayBuffer) {
  if (buffer.byteLength < 20 || buffer.byteLength > GLB_SIZE_LIMIT) throw new Error('GLB must be between 20 bytes and 120 MB');
  const header = new DataView(buffer);
  if (header.getUint32(0, true) !== 0x46546c67 || header.getUint32(4, true) !== 2
    || header.getUint32(8, true) !== buffer.byteLength) throw new Error('Invalid GLB 2.0 header');
  const length = header.getUint32(12, true);
  if (header.getUint32(16, true) !== 0x4e4f534a || length > 8_000_000 || length + 20 > buffer.byteLength) throw new Error('Invalid GLB JSON chunk');
  const json = JSON.parse(new TextDecoder().decode(new Uint8Array(buffer, 20, length))) as {
    asset?: { version?: string };
    buffers?: { uri?: string; byteLength?: number }[]; images?: { uri?: string }[];
    accessors?: { count?: number; type?: string; componentType?: number }[];
  };
  if (!json || json.asset?.version !== '2.0') throw new Error('Invalid GLB asset version');
  if (json.buffers && (!Array.isArray(json.buffers) || json.buffers.some(buffer => !Number.isSafeInteger(buffer.byteLength) || buffer.byteLength! < 0))
    || json.images && !Array.isArray(json.images)
    || json.accessors && (!Array.isArray(json.accessors) || json.accessors.some(accessor =>
      !Number.isSafeInteger(accessor.count) || accessor.count! < 0 || accessor.count! > 10_000_000))) throw new Error('Invalid or oversized GLB resources');
  if ((json.buffers ?? []).reduce((sum, buffer) => sum + buffer.byteLength!, 0) > GLB_SIZE_LIMIT) throw new Error('GLB buffers exceed 120 MB');
  if ([...(json.buffers ?? []), ...(json.images ?? [])].some(item => item.uri && !item.uri.startsWith('data:'))) {
    throw new Error('GLB must embed all buffers and textures; external resources are not allowed');
  }
}

export async function loadEmbeddedGlb(blob: Blob) {
  if (blob.size > GLB_SIZE_LIMIT) throw new Error('GLB exceeds 120 MB');
  const buffer = await blob.arrayBuffer();
  validateGlbBuffer(buffer);
  const manager = new LoadingManager();
  manager.setURLModifier(url => {
    if (!/^(data:|blob:)/.test(url)) throw new Error('External GLB resources are not allowed');
    return url;
  });
  return new GLTFLoader(manager).parseAsync(buffer, '');
}

export function disposeObject(root: Object3D) {
  const textures = new Set<Texture>();
  const images = new Set<ImageBitmap>();
  root.traverse(object => {
    if (!(object instanceof Mesh)) return;
    object.geometry.dispose();
    const materials = Array.isArray(object.material) ? object.material : [object.material];
    for (const material of materials) {
      if (!material) continue;
      for (const value of Object.values(material)) {
        if (value && typeof value === 'object' && 'isTexture' in value) textures.add(value as Texture);
      }
      material.dispose();
    }
  });
  for (const texture of textures) {
    if (texture.image && typeof texture.image.close === 'function') images.add(texture.image);
    texture.dispose();
  }
  for (const image of images) image.close();
}
