import * as ort from 'onnxruntime-web/wasm';

type DepthRequest = {
  image: {
    data: Uint8ClampedArray;
    width: number;
    height: number;
  };
};

const DEPTH_MODEL_URL =
  'https://huggingface.co/onnx-community/depth-anything-v2-small/resolve/4472b7362082ad9968fee890ca0f1e5aca36b93d/onnx/model_q4f16.onnx';
const DEPTH_MODEL_SHA256 = 'eca72971aea64216d767c70c534160de53b5435b588d362bac6dbd5a73f9bf1e';

ort.env.wasm.numThreads = 1;
ort.env.wasm.proxy = false;
ort.env.wasm.wasmPaths = {
  wasm: new URL(
    '../../node_modules/onnxruntime-web/dist/ort-wasm-simd-threaded.wasm',
    import.meta.url,
  ).href,
};

let sessionPromise: Promise<ort.InferenceSession> | null = null;
const post = (message: unknown, transfer?: Transferable[]) => (
  self as unknown as { postMessage: (value: unknown, transfer?: Transferable[]) => void }
).postMessage(message, transfer);

async function createSession(url: string) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Depth model download failed (${response.status})`);
  const model = await response.arrayBuffer();
  const hash = [...new Uint8Array(await crypto.subtle.digest('SHA-256', model))]
    .map(value => value.toString(16).padStart(2, '0'))
    .join('');
  if (hash !== DEPTH_MODEL_SHA256) throw new Error('Depth model checksum mismatch');
  return ort.InferenceSession.create(model, { executionProviders: ['wasm'] });
}

function inputTensor(
  image: DepthRequest['image'],
  size: number,
  mean: readonly number[],
  deviation: readonly number[],
) {
  const plane = size * size;
  const tensor = new Float32Array(plane * 3);
  for (let y = 0; y < size; y++) {
    const sourceY = Math.min(image.height - 1, Math.floor((y + 0.5) / size * image.height));
    for (let x = 0; x < size; x++) {
      const sourceX = Math.min(image.width - 1, Math.floor((x + 0.5) / size * image.width));
      const target = y * size + x;
      const source = (sourceY * image.width + sourceX) * 4;
      const alpha = image.data[source + 3] / 255;
      for (let channel = 0; channel < 3; channel++) {
        const composited = image.data[source + channel] * alpha + 255 * (1 - alpha);
        tensor[channel * plane + target] =
          (composited / 255 - mean[channel]) / deviation[channel];
      }
    }
  }
  return new ort.Tensor('float32', tensor, [1, 3, size, size]);
}

self.onmessage = async (event: MessageEvent<DepthRequest>) => {
  try {
    post({ type: 'progress', phase: 'model' });
    sessionPromise ??= createSession(DEPTH_MODEL_URL);
    const session = await sessionPromise;
    post({ type: 'progress', phase: 'depth' });
    const depthOutput = await session.run({
      pixel_values: inputTensor(
        event.data.image,
        518,
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225],
      ),
    });
    const depth = depthOutput.predicted_depth;
    if (!depth || depth.type !== 'float32' || depth.dims.length < 2) {
      throw new Error('Depth model returned an unexpected tensor');
    }
    const depthData = new Float32Array(depth.data as Float32Array);
    post({
      type: 'result',
      depth: {
        data: depthData,
        width: depth.dims.at(-1)!,
        height: depth.dims.at(-2)!,
      },
    }, [depthData.buffer]);
  } catch (error) {
    post({
      type: 'error',
      error: error instanceof Error ? error.message : String(error),
    });
  }
};
