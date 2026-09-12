import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { ARTIFACTS, BENCHMARK } from '../storage';

export function trainingStatus() {
  const runtime = resolve(BENCHMARK, '.runtime/local-training'), bundles = resolve(ARTIFACTS, 'runs');
  const names = new Set([
    ...(existsSync(runtime) ? readdirSync(runtime) : []),
    ...readdirSync(bundles).filter(n => n.startsWith('local-qwen3-')).map(n => n.slice('local-qwen3-'.length)),
  ]);
  return [...names].filter(n => /^(base|single|multi)-seed\d+$/.test(n)).sort().flatMap(name => {
    const live = resolve(runtime, name), bundle = resolve(bundles, 'local-qwen3-' + name);
    const dir = existsSync(resolve(live, 'manifest.json')) ? live : bundle;
    const result = resolve(dir, dir === live ? 'result.json' : 'training-manifest.json');
    const file = existsSync(result) ? result : resolve(dir, 'manifest.json');
    if (!existsSync(file)) return [];
    const manifest = JSON.parse(readFileSync(file, 'utf8'));
    let history: { step: number; loss: number; task: string }[] = [];
    if (existsSync(resolve(dir, 'training-steps.json'))) history = JSON.parse(readFileSync(resolve(dir, 'training-steps.json'), 'utf8'));
    else if (existsSync(resolve(dir, 'training.jsonl'))) history = readFileSync(resolve(dir, 'training.jsonl'), 'utf8')
      .split('\n').filter(Boolean).flatMap(line => { try { return [JSON.parse(line)]; } catch { return []; } });
    return [{ name, condition: manifest.condition, seed: manifest.seed, status: manifest.status === 'complete' ? 'complete' : 'not-finished',
      device: manifest.device, steps: manifest.optimization_steps ?? history.at(-1)?.step ?? 0,
      targetSteps: manifest.condition === 'base' ? 0 : manifest.config.steps,
      trainedParameters: manifest.trained_parameters ?? 0, tokens: manifest.processed_tokens ?? 0,
      before: manifest.validation_loss_before ?? null, after: manifest.validation_loss_after ?? null, history }];
  });
}
