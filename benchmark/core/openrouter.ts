import { Budget } from './budget';

export const MODELS = [
  { id: 'openai/gpt-4.1-mini', label: 'GPT-4.1 mini', promptCap: 0.5, completionCap: 2 },
  { id: 'google/gemini-2.5-flash', label: 'Gemini 2.5 Flash', promptCap: 0.4, completionCap: 3 },
] as const;
export interface Message {
  role: 'system' | 'user' | 'assistant';
  content: string | ({ type: 'text'; text: string } | { type: 'image_url'; image_url: { url: string } })[];
}
export interface CallResult {
  id: string;
  provider: string;
  content: string;
  cost: number;
  promptTokens: number;
  completionTokens: number;
  reasoningTokens: number;
  latencyMs: number;
  finishReason: string;
}
export const MAX_OUTPUT = 2200;
export function requestCeiling(modelId: string, messages: Message[]) {
  const model = MODELS.find(m => m.id === modelId);
  if (!model) throw new Error('Model is not in pilot allowlist');
  let text = 2048, images = 0;
  for (const message of messages) {
    if (typeof message.content === 'string') text += Buffer.byteLength(message.content);
    else for (const item of message.content) {
      if (item.type === 'text') text += Buffer.byteLength(item.text);
      else images++;
    }
  }
  if (text > 50_000 || images > 16) throw new Error('Prompt exceeds pilot request limit');
  // Byte count bounds text tokens conservatively; each 640x480 image reserves 16K tokens.
  const ceiling = ((text + images * 16384) * model.promptCap + MAX_OUTPUT * model.completionCap) / 1e6
    + images * 0.005;
  return { ceiling, model };
}

export async function modelPricing() {
  const response = await fetch('https://openrouter.ai/api/v1/models', { signal: AbortSignal.timeout(20_000) });
  if (!response.ok) throw new Error(`Model catalog HTTP ${response.status}`);
  const json = await response.json() as { data: {
    id: string; pricing: Record<string, string>;
    architecture: { input_modalities: string[] };
  }[] };
  return MODELS.map(model => {
    const entry = json.data.find(m => m.id === model.id);
    if (!entry || !entry.architecture.input_modalities.includes('image')
      || !Number.isFinite(Number(entry.pricing.prompt))
      || !Number.isFinite(Number(entry.pricing.completion))
      || Number(entry.pricing.prompt) * 1e6 > model.promptCap
      || Number(entry.pricing.completion) * 1e6 > model.completionCap) {
      throw new Error(`Model unavailable or exceeds price cap: ${model.id}`);
    }
    return { id: model.id, pricing: entry.pricing,
      maxPromptPerMillion: model.promptCap, maxCompletionPerMillion: model.completionCap };
  });
}

export async function completion(key: string, modelId: string, messages: Message[], budget: Budget): Promise<CallResult> {
  if (!key) throw new Error('OPENROUTER_API_KEY is not configured');
  const { ceiling, model } = requestCeiling(modelId, messages);
  const chargeId = budget.reserve(modelId, ceiling);
  const start = performance.now();
  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      signal: AbortSignal.timeout(90_000),
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json',
        'X-OpenRouter-Title': 'Brick Atlas CARE-mini pilot' },
      body: JSON.stringify({
        model: modelId, messages, stream: false, temperature: 0,
        max_tokens: MAX_OUTPUT, response_format: { type: 'json_object' },
        ...(modelId.startsWith('google/') ? { reasoning: { enabled: false } } : {}),
        provider: { sort: 'price', allow_fallbacks: false, require_parameters: true,
          data_collection: 'deny',
          max_price: { prompt: model.promptCap, completion: model.completionCap, image: 0.005 } },
      }),
    });
    // Raw HTTP errors are deliberately not logged: upstream errors may echo request data.
    if (!response.ok) throw new Error(`OpenRouter HTTP ${response.status}; no automatic retry`);
    const data = await response.json() as {
      id: string; provider?: string;
      choices?: { message: { content: string }; finish_reason: string }[];
      usage?: { cost: number; prompt_tokens: number; completion_tokens: number;
        completion_tokens_details?: { reasoning_tokens?: number } };
    };
    if (!data.usage || typeof data.usage.cost !== 'number' || !data.id) {
      throw new Error('Missing usage cost; stopped for reconciliation');
    }
    budget.settle(chargeId, data.usage.cost, data.id);
    return {
      id: data.id, provider: data.provider ?? 'unknown',
      content: data.choices?.[0]?.message.content ?? '',
      cost: data.usage.cost, promptTokens: data.usage.prompt_tokens,
      completionTokens: data.usage.completion_tokens,
      reasoningTokens: data.usage.completion_tokens_details?.reasoning_tokens ?? 0,
      latencyMs: Math.round(performance.now() - start),
      finishReason: data.choices?.[0]?.finish_reason ?? 'unknown',
    };
  } catch (error) {
    budget.uncertain(chargeId);
    throw error;
  }
}
