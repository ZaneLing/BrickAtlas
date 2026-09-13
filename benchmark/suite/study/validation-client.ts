import { Budget } from '../../core/budget';
import type { Message, CallResult } from '../../core/openrouter';

export const VALIDATION_MODELS = [
  { id: 'openai/gpt-4.1-mini', prompt: 0.5, completion: 2 },
  { id: 'openai/gpt-4.1', prompt: 2.1, completion: 8.5 },
  { id: 'google/gemini-2.5-flash', prompt: 0.4, completion: 3 },
  { id: 'qwen/qwen3-vl-32b-instruct', prompt: 0.3, completion: 1 },
];
export const VALIDATION_TOKENS = 2200;

export function validationCeiling(modelId: string, messages: Message[]) {
  const model = VALIDATION_MODELS.find(m => m.id === modelId);
  if (!model) throw new Error('Unknown validation model');
  let bytes = 2048, images = 0;
  for (const m of messages) {
    if (typeof m.content === 'string') bytes += Buffer.byteLength(m.content);
    else for (const item of m.content) {
      if (item.type === 'text') bytes += Buffer.byteLength(item.text);
      else images++;
    }
  }
  if (bytes > 50_000 || images > 4) throw new Error('Validation input exceeds limit');
  return ((bytes + images * 16384) * model.prompt + VALIDATION_TOKENS * model.completion) / 1e6 + images * 0.005;
}

export async function validationPricing() {
  const response = await fetch('https://openrouter.ai/api/v1/models', { signal: AbortSignal.timeout(20000) });
  if (!response.ok) throw new Error(`Catalog HTTP ${response.status}`);
  const data = (await response.json()).data;
  return VALIDATION_MODELS.map(model => {
    const entry = data.find((e: any) => e.id === model.id);
    if (!entry?.architecture.input_modalities.includes('image')
      || !entry.supported_parameters.includes('response_format')
      || !Number.isFinite(Number(entry.pricing.prompt)) || !Number.isFinite(Number(entry.pricing.completion))
      || Number(entry.pricing.prompt) * 1e6 > model.prompt
      || Number(entry.pricing.completion) * 1e6 > model.completion) throw new Error(`Pricing/capability mismatch: ${model.id}`);
    return { id: model.id, pricing: entry.pricing, parameters: entry.supported_parameters, caps: model };
  });
}

export async function validationCompletion(key: string, modelId: string, messages: Message[], budget: Budget,
  transport: typeof fetch = fetch): Promise<CallResult> {
  if (!key) throw new Error('Missing OpenRouter credential');
  const model = VALIDATION_MODELS.find(m => m.id === modelId)!;
  const ceiling = validationCeiling(modelId, messages), charge = budget.reserve(modelId, ceiling);
  const start = performance.now();
  try {
    const response = await transport('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST', signal: AbortSignal.timeout(120000),
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json', 'X-OpenRouter-Title': 'BrickAtlas validation' },
      body: JSON.stringify({ model: modelId, messages, temperature: 0, stream: false,
        max_tokens: VALIDATION_TOKENS, response_format: { type: 'json_object' },
        ...(modelId.startsWith('google/') ? { reasoning: { enabled: false } } : {}),
        provider: { sort: 'price', allow_fallbacks: false, require_parameters: true, data_collection: 'deny',
          max_price: { prompt: model.prompt, completion: model.completion, image: 0.005 } } }),
    });
    if (!response.ok) throw new Error(`OpenRouter HTTP ${response.status}; automatic retry disabled`);
    const data = await response.json();
    if (!data.id || !Number.isFinite(data.usage?.cost)) throw new Error('Missing billing evidence');
    budget.settle(charge, data.usage.cost, data.id);
    const choice = data.choices?.[0];
    if (typeof choice?.message?.content !== 'string') throw new Error('Missing model response');
    return { id: data.id, provider: data.provider ?? 'unknown', content: choice.message.content,
      cost: data.usage.cost, promptTokens: data.usage.prompt_tokens, completionTokens: data.usage.completion_tokens,
      reasoningTokens: data.usage.completion_tokens_details?.reasoning_tokens ?? 0,
      latencyMs: Math.round(performance.now() - start), finishReason: choice.finish_reason ?? 'unknown' };
  } catch (error) { budget.uncertain(charge); throw error; }
}
