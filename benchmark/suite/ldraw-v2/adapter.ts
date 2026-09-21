import assert from 'node:assert/strict';
import { PNG } from 'pngjs';
import type { ModelRequest } from './types';

export interface Adapter {
  schemaVersion: number; family: string; modelId: string; provider: string; endpoint: string;
  transport: 'openai' | 'anthropic'; apiRevision: string | null; checkpointSha256: string | null;
  providerApiVersion: string; apiKeyEnv: string; systemPrompt: string;
  decoding: { temperature: number; top_p: number; max_tokens: number };
  tools: string[]; imageEncoding: string; imageResolution: { width: number; height: number; resize: string };
  outputParser: string; timeoutMs: number; maxAttempts: number;
  pricingUsdPerMillion: { input: number | null; output: number | null };
}
export function validateAdapter(a: Adapter, live = false) {
  assert.equal(a.schemaVersion, 1); assert.ok(a.modelId && a.provider && a.endpoint);
  assert.ok(['openai', 'anthropic'].includes(a.transport));
  assert.equal(a.tools.length, 0);
  assert.equal(a.maxAttempts, 1, 'No hidden retries; failed calls remain in the denominator');
  assert.equal(a.outputParser, 'strict-json-object; no prose or markdown repair');
  assert.ok(a.imageResolution.width > 0 && a.imageResolution.height > 0);
  const endpoint = new URL(a.endpoint);
  assert.ok(endpoint.protocol === 'https:' || ['localhost', '127.0.0.1'].includes(endpoint.hostname));
  if (live) assert.ok(a.apiRevision || a.checkpointSha256, 'Freeze a real API revision or checkpoint hash before live execution');
}
/** Deterministic bilinear resize with letterboxing; image bytes are snapshotted. */
export function encodeImage(bytes: Buffer, size: Adapter['imageResolution']) {
  const src = PNG.sync.read(bytes);
  const dst = new PNG({ width: size.width, height: size.height });
  dst.data.fill(255);
  const scale = Math.min(size.width / src.width, size.height / src.height);
  const w = Math.max(1, Math.round(src.width * scale)), h = Math.max(1, Math.round(src.height * scale));
  const ox = Math.floor((size.width - w) / 2), oy = Math.floor((size.height - h) / 2);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const sx = Math.max(0, Math.min(src.width - 1, (x + .5) / scale - .5));
    const sy = Math.max(0, Math.min(src.height - 1, (y + .5) / scale - .5));
    const x0 = Math.floor(sx), y0 = Math.floor(sy), x1 = Math.min(x0 + 1, src.width - 1), y1 = Math.min(y0 + 1, src.height - 1);
    const fx = sx - x0, fy = sy - y0;
    for (let c = 0; c < 3; c++) {
      const at = (xx: number, yy: number) => src.data[(yy * src.width + xx) * 4 + c];
      dst.data[((oy + y) * size.width + ox + x) * 4 + c] = Math.round(
        (at(x0, y0) * (1 - fx) + at(x1, y0) * fx) * (1 - fy) +
        (at(x0, y1) * (1 - fx) + at(x1, y1) * fx) * fy);
    }
  }
  return `data:image/png;base64,${PNG.sync.write(dst).toString('base64')}`;
}
export function wireRequest(request: ModelRequest, a: Adapter) {
  if (a.transport === 'openai') return { model: a.modelId, ...a.decoding, messages: request.messages };
  const content = request.messages[1].content;
  assert.ok(Array.isArray(content));
  return { model: a.modelId, ...a.decoding, system: request.messages[0].content,
    messages: [{ role: 'user', content: content.map(c => {
      if (c.type === 'text') return c;
      const [, media_type, data] = c.image_url.url.match(/^data:(image\/png);base64,(.+)$/)!;
      return { type: 'image', source: { type: 'base64', media_type, data } };
    }) }] };
}
export function parseModelOutput(text: string): unknown {
  try {
    const answer = JSON.parse(text);
    return answer && typeof answer === 'object' && !Array.isArray(answer) ? answer : null;
  } catch { return null; }
}
export async function sendRequest(bodyText: string, a: Adapter) {
  const headers: Record<string, string> = { 'content-type': 'application/json' };
  const secret = process.env[a.apiKeyEnv];
  if (a.transport === 'anthropic') {
    if (!secret) throw new Error(`Missing credential environment variable ${a.apiKeyEnv}`);
    headers['x-api-key'] = secret; headers['anthropic-version'] = a.providerApiVersion;
  } else if (secret) headers.authorization = `Bearer ${secret}`;
  else if (!['localhost', '127.0.0.1'].includes(new URL(a.endpoint).hostname))
    throw new Error(`Missing credential environment variable ${a.apiKeyEnv}`);
  const started = performance.now();
  const response = await fetch(a.endpoint, { method: 'POST', headers, body: bodyText, signal: AbortSignal.timeout(a.timeoutMs) });
  const raw = await response.text();
  let payload: any = null;
  try { payload = JSON.parse(raw); } catch { /* Preserve invalid response bytes in receipt. */ }
  const output = a.transport === 'openai' ? payload?.choices?.[0]?.message?.content
    : payload?.content?.filter((c: any) => c.type === 'text').map((c: any) => c.text).join('');
  const usage = payload?.usage ?? null;
  const input = usage?.prompt_tokens ?? usage?.input_tokens, completion = usage?.completion_tokens ?? usage?.output_tokens;
  const price = a.pricingUsdPerMillion;
  const usd = price.input !== null && price.output !== null && Number.isFinite(input) && Number.isFinite(completion)
    ? (input * price.input + completion * price.output) / 1e6 : null;
  return { httpStatus: response.status, ok: response.ok, raw, output: typeof output === 'string' ? output : null,
    answer: response.ok && typeof output === 'string' ? parseModelOutput(output) : null,
    usage, usd, latencyMs: performance.now() - started, providerModel: payload?.model ?? null,
    requestId: response.headers.get('request-id') ?? response.headers.get('x-request-id') };
}
