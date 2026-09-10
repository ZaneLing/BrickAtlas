import type { SampledDepth, SampledImage } from './imageBrickModel';

export type DepthPhase = 'model' | 'depth';

export function estimatePhotoDepth(
  image: SampledImage,
  signal: AbortSignal,
  onProgress?: (phase: DepthPhase) => void,
) {
  return new Promise<SampledDepth>((resolve, reject) => {
    const worker = new Worker(new URL('../workers/depth.worker.ts', import.meta.url), { type: 'module' });
    const cleanup = () => {
      worker.terminate();
      signal.removeEventListener('abort', abort);
    };
    const abort = () => {
      cleanup();
      reject(new DOMException('Cancelled', 'AbortError'));
    };
    signal.addEventListener('abort', abort, { once: true });
    worker.onerror = event => {
      cleanup();
      reject(new Error(event.message || 'Depth worker failed'));
    };
    worker.onmessage = (event: MessageEvent<
      | { type: 'progress'; phase: DepthPhase }
      | { type: 'result'; depth: SampledDepth }
      | { type: 'error'; error: string }
    >) => {
      if (event.data.type === 'progress') {
        onProgress?.(event.data.phase);
        return;
      }
      cleanup();
      if (event.data.type === 'error') reject(new Error(event.data.error));
      else resolve(event.data.depth);
    };
    worker.postMessage({ image }, [image.data.buffer]);
  });
}
