import { BufferAttribute, BufferGeometry } from 'three';
import type { AtlasManifest, GeometryBucket } from '../model/types';
import { modelCatalog } from '../../atlas.config';

export interface SourceGeometry {
  manifest: AtlasManifest;
  buckets: { definition: GeometryBucket; geometry: BufferGeometry }[];
}

// One decoded copy per source model, shared by all composition instances.
const sources = new Map<string, Promise<SourceGeometry>>();

export function loadSourceGeometry(modelId: string): Promise<SourceGeometry> {
  const cached = sources.get(modelId);
  if (cached) return cached;
  if (!modelCatalog.some(model => model.id === modelId)) return Promise.reject(new Error('Unknown source model'));
  const promise = (async () => {
    const base = new URL(`${import.meta.env.BASE_URL}models/${modelId}/`, location.href).href;
    const response = await fetch(`${base}manifest.json`);
    if (!response.ok) throw new Error(`manifest.json: HTTP ${response.status}`);
    const manifest = await response.json() as AtlasManifest;
    return new Promise<SourceGeometry>((resolve, reject) => {
      const worker = new Worker(new URL('../workers/geometry.worker.ts', import.meta.url), { type: 'module' });
      const buckets: SourceGeometry['buckets'] = [];
      const fail = (error: Error) => {
        worker.terminate();
        buckets.forEach(bucket => bucket.geometry.dispose());
        reject(error);
      };
      worker.onerror = event => fail(new Error(event.message));
      worker.onmessage = ({ data }) => {
        try {
          if (data.type === 'error') { fail(new Error(data.message)); return; }
          if (data.type === 'chunk') {
            const chunk = manifest.chunks.find(item => item.groupId === data.groupId)!;
            for (const definition of chunk.buckets) {
              const geometry = new BufferGeometry();
              for (const [name, attr] of Object.entries(definition.attributes)) {
                geometry.setAttribute(name, new BufferAttribute(new Float32Array(data.buffer, attr.offset, attr.count), attr.itemSize));
              }
              buckets.push({ definition, geometry });
            }
          }
          if (data.type === 'complete') {
            worker.terminate();
            resolve({ manifest, buckets });
          }
        } catch (error) { fail(error instanceof Error ? error : new Error(String(error))); }
      };
      worker.postMessage({ base, chunks: manifest.chunks });
    });
  })();
  sources.set(modelId, promise);
  promise.catch(() => sources.delete(modelId));
  return promise;
}
