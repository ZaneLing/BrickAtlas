import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { BENCHMARK } from '../storage';

export function localStatus() {
  const root = resolve(BENCHMARK, '.runtime/vlm-training');
  const jobs = ['base-seed17', ...['single', 'multi', 'leave-edit'].flatMap(c => [17, 29, 43].map(seed => `${c}-seed${seed}`))];
  return jobs.map(name => {
    const live = resolve(root, name), published = resolve(BENCHMARK, 'suite/artifacts/study/local', name);
    const dir = existsSync(resolve(live, 'manifest.json')) ? live : published;
    const file = resolve(dir, 'manifest.json');
    if (!existsSync(file)) return { name, status: 'pending', steps: 0, targetSteps: name.startsWith('base') ? 0 : 120,
      supervisedTokens: 0, predictions: 0, inputTokens: 0, outputTokens: 0, inferenceSeconds: 0,
      before: null, after: null, history: [] };
    const done = existsSync(resolve(dir, 'result.json'));
    const manifest = JSON.parse(readFileSync(done ? resolve(dir, 'result.json') : file, 'utf8'));
    const steps = existsSync(resolve(dir, 'steps.json')) ? JSON.parse(readFileSync(resolve(dir, 'steps.json'), 'utf8')) : [];
    const predictions = existsSync(resolve(dir, 'predictions.json')) ? JSON.parse(readFileSync(resolve(dir, 'predictions.json'), 'utf8')) : [];
    return { name, status: done || manifest.status === 'complete' ? 'complete' : 'in-progress-or-interrupted', steps: steps.length,
      targetSteps: manifest.condition === 'base' ? 0 : manifest.config.steps,
      supervisedTokens: steps.reduce((n: number, s: any) => n + s.supervised_tokens, 0),
      predictions: predictions.length, inputTokens: predictions.reduce((n: number, p: any) => n + p.input_tokens, 0),
      outputTokens: predictions.reduce((n: number, p: any) => n + p.output_tokens, 0),
      inferenceSeconds: predictions.reduce((n: number, p: any) => n + p.seconds, 0),
      before: manifest.validation_before ?? null, after: manifest.validation_after ?? null, history: steps.map((s: any) => ({ step: s.step, loss: s.loss })) };
  });
}
