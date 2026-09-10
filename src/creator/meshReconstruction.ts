import { Mesh, Vector3 } from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import type { Client as GradioClient } from '@gradio/client';

export type CloudMeshProvider = 'triposr-cpu' | 'stable-fast-3d' | 'triposr';
export type CloudMeshPhase =
  | 'connecting'
  | 'uploading'
  | 'queued'
  | 'generating'
  | 'downloading';

export interface CloudMeshResult {
  blob: Blob;
  provider: CloudMeshProvider;
  providerName: string;
  sourceUrl: string;
}

export interface ExtractedMesh {
  positions: Float32Array;
  triangleCount: number;
  sampledTriangleCount: number;
}

type GradioFile = {
  url?: string;
  path?: string;
  name?: string;
  orig_name?: string;
};

function fileUrl(value: unknown): string | null {
  if (typeof value === 'string' && /^https?:\/\//.test(value)) return value;
  if (!value || typeof value !== 'object') return null;
  const file = value as GradioFile;
  return file.url && /^https?:\/\//.test(file.url)
    ? file.url
    : file.path && /^https?:\/\//.test(file.path)
      ? file.path
      : null;
}

async function runJob(
  client: GradioClient,
  endpoint: string,
  input: unknown[],
  signal: AbortSignal,
  onPhase: (phase: CloudMeshPhase, detail?: string) => void,
) {
  signal.throwIfAborted();
  const job = client.submit(endpoint, input);
  const abort = () => {
    void job.cancel();
    job.close_stream();
  };
  signal.addEventListener('abort', abort, { once: true });
  let result: unknown[] | null = null;
  try {
    for await (const message of job) {
      signal.throwIfAborted();
      if (message.type === 'status') {
        if (message.stage === 'error') {
          throw new Error(typeof message.message === 'string'
            ? message.message
            : 'The public image-to-3D service rejected this job');
        }
        if (message.stage === 'pending') {
          const queue = typeof message.position === 'number'
            ? `Queue position ${message.position + 1}`
            : undefined;
          onPhase('queued', queue);
        } else if (message.stage === 'generating' || message.stage === 'streaming') {
          onPhase('generating');
        }
      } else if (message.type === 'data') {
        result = message.data as unknown[];
      }
    }
  } finally {
    signal.removeEventListener('abort', abort);
  }
  if (!result) throw new Error('The public image-to-3D service returned no model');
  return result;
}

export async function reconstructPhotoMesh(
  file: File | Blob,
  provider: CloudMeshProvider,
  signal: AbortSignal,
  onPhase: (phase: CloudMeshPhase, detail?: string) => void,
  token = '',
): Promise<CloudMeshResult> {
  onPhase('connecting');
  const { Client, handle_file } = await import('@gradio/client');
  const options = token.trim().startsWith('hf_')
    ? { token: token.trim() as `hf_${string}` }
    : undefined;
  const space = provider === 'stable-fast-3d'
    ? 'stabilityai/stable-fast-3d'
    : provider === 'triposr-cpu'
      ? 'WeReCooking2/Dust3R-TripoSR'
      : 'stabilityai/TripoSR';
  const client = await Client.connect(space, options);
  try {
    onPhase('uploading');
    let output: unknown[];
    if (provider === 'stable-fast-3d') {
      output = await runJob(
        client,
        '/run_button',
        [handle_file(file), 0.85, null, 'Triangle', 20_000, 1024],
        signal,
        onPhase,
      );
    } else {
      const preprocessed = await runJob(
        client,
        '/preprocess',
        [handle_file(file), true, 0.85],
        signal,
        onPhase,
      );
      output = await runJob(
        client,
        '/generate',
        [preprocessed[0], provider === 'triposr-cpu' ? 96 : 128],
        signal,
        onPhase,
      );
    }
    const sourceUrl = provider === 'stable-fast-3d'
      ? fileUrl(output[1])
      : fileUrl(output[1]) ?? fileUrl(output[0]);
    if (!sourceUrl) throw new Error('The provider response did not contain a GLB file');
    onPhase('downloading');
    const response = await fetch(sourceUrl, { signal });
    if (!response.ok) throw new Error(`Could not download generated GLB (HTTP ${response.status})`);
    const length = Number(response.headers.get('content-length') ?? 0);
    if (length > 120 * 1024 * 1024) throw new Error('Generated GLB exceeds the 120 MB safety limit');
    const blob = await response.blob();
    if (!blob.size || blob.size > 120 * 1024 * 1024) {
      throw new Error('Generated GLB is empty or exceeds the 120 MB safety limit');
    }
    return {
      blob,
      provider,
      providerName: provider === 'stable-fast-3d'
        ? 'Stable Fast 3D'
        : provider === 'triposr-cpu'
          ? 'TripoSR Public CPU'
          : 'TripoSR Official',
      sourceUrl,
    };
  } finally {
    client.close();
  }
}

export async function extractMeshTriangles(
  blob: Blob,
  maximumTriangles = 250_000,
): Promise<ExtractedMesh> {
  const gltf = await new GLTFLoader().parseAsync(await blob.arrayBuffer(), '');
  gltf.scene.updateMatrixWorld(true);
  const meshes: Mesh[] = [];
  let triangleCount = 0;
  gltf.scene.traverse(object => {
    if (!(object instanceof Mesh)) return;
    const position = object.geometry.getAttribute('position');
    if (!position) return;
    meshes.push(object);
    triangleCount += object.geometry.index
      ? Math.floor(object.geometry.index.count / 3)
      : Math.floor(position.count / 3);
  });
  if (!triangleCount) throw new Error('Generated GLB contains no triangle mesh');
  const stride = Math.max(1, Math.ceil(triangleCount / maximumTriangles));
  const values: number[] = [];
  const point = new Vector3();
  let triangleCursor = 0;
  for (const mesh of meshes) {
    const geometry = mesh.geometry;
    const position = geometry.getAttribute('position');
    const index = geometry.index;
    const count = index ? Math.floor(index.count / 3) : Math.floor(position.count / 3);
    for (let triangle = 0; triangle < count; triangle++, triangleCursor++) {
      if (triangleCursor % stride) continue;
      for (let corner = 0; corner < 3; corner++) {
        const vertex = index
          ? index.getX(triangle * 3 + corner)
          : triangle * 3 + corner;
        point.fromBufferAttribute(position, vertex).applyMatrix4(mesh.matrixWorld);
        values.push(point.x, point.y, point.z);
      }
    }
  }
  return {
    positions: Float32Array.from(values),
    triangleCount,
    sampledTriangleCount: values.length / 9,
  };
}
