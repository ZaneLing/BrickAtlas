import { voxelizeMeshTriangles } from '../creator/meshVoxelizer';

const worker = self as unknown as {
  onmessage: ((event: MessageEvent) => void) | null;
  postMessage: (message: unknown, transfer?: Transferable[]) => void;
};

worker.onmessage = ({
  data,
}: MessageEvent<{
  positions: Float32Array;
  resolution: number;
  hollow: boolean;
}>) => {
  try {
    const volume = voxelizeMeshTriangles(data.positions, {
      resolution: data.resolution,
      hollow: data.hollow,
    });
    worker.postMessage({ volume }, [volume.occupied.buffer as ArrayBuffer]);
  } catch (cause) {
    worker.postMessage({
      error: cause instanceof Error ? cause.message : String(cause),
    });
  }
};
