import { createHash, randomUUID } from 'node:crypto';
import { existsSync, mkdirSync, openSync, closeSync, readFileSync, readdirSync, unlinkSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { Budget, HARD_CAP_USD, atomicJson } from './core/budget';
import { Environment } from './core/environment';
import { MODELS, completion, modelPricing, type Message } from './core/openrouter';
import { BUILDER_PROMPT, SYSTEM_PROMPT } from './core/prompts';
import { RenderService, type Frame } from './core/render-service';
import type { EpisodeResult, RunResult } from './core/results';
import { PILOT_SPEC, pilotTasks } from './core/tasks';
import type { Action, Observation, Protocol } from './shared/types';
import { writeReport } from './report';

export const ROOT = dirname(fileURLToPath(import.meta.url));
export function loadKey() {
  if (!process.env.OPENROUTER_API_KEY && existsSync(resolve(ROOT, '../.env'))) {
    process.loadEnvFile(resolve(ROOT, '../.env'));
  }
  return process.env.OPENROUTER_API_KEY ?? '';
}
export function hash(value: string | Buffer) { return createHash('sha256').update(value).digest('hex'); }

export function parseAction(text: string): Action | null {
  try {
    const trimmed = text.trim().replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '');
    const value = JSON.parse(trimmed);
    if (!value || typeof value !== 'object' || Array.isArray(value) || typeof value.type !== 'string') return null;
    return value as Action;
  } catch { return null; }
}

function fingerprints() {
  const files: Record<string, string> = {};
  for (const dir of ['core', 'shared', 'web']) for (const entry of readdirSync(resolve(ROOT, dir))) {
    if (/\.(ts|tsx|html|css)$/.test(entry)) {
      const name = `${dir}/${entry}`;
      files[name] = hash(readFileSync(resolve(ROOT, name)));
    }
  }
  for (const file of ['run.ts', 'server.ts', 'vite.config.ts']) files[file] = hash(readFileSync(resolve(ROOT, file)));
  return files;
}

export interface PilotProgress { status: string; runId?: string; completed: number; total: number; model?: string; error?: string }

export async function runPilot(
  renderer: RenderService,
  selected: string[] = MODELS.map(m => m.id),
  progress: (p: PilotProgress) => void = () => {},
): Promise<RunResult> {
  if (!selected.length || selected.length > MODELS.length || new Set(selected).size !== selected.length
    || selected.some(id => !MODELS.some(m => m.id === id))) throw new Error('Invalid model selection');
  const key = loadKey();
  if (!key) throw new Error('OPENROUTER_API_KEY is missing');
  mkdirSync(resolve(ROOT, '.runtime'), { recursive: true });
  const lock = resolve(ROOT, '.runtime/pilot.lock');
  const fd = openSync(lock, 'wx', 0o600);
  writeFileSync(fd, `${process.pid}\n`);
  closeSync(fd);
  let run: RunResult | undefined;
  try {
    const budget = new Budget(resolve(ROOT, '.runtime/campaign-ledger.json'), HARD_CAP_USD);
    if (budget.blocked) throw new Error('Campaign has an unsettled charge; reconcile first');
    const id = `${new Date().toISOString().replace(/[:.]/g, '-')}-${randomUUID().slice(0, 8)}`;
    const output = resolve(ROOT, 'results', id);
    mkdirSync(resolve(output, 'observations'), { recursive: true });
    const sourceFiles = fingerprints();
    run = {
      version: 'care-mini-v1', id, startedAt: new Date().toISOString(), completedAt: null,
      status: 'running', split: 'public-pilot',
      observation: 'RGB+visible-part-identities', actionSpace: 'grid-edits+ordered-batches',
      models: selected, plannedEpisodes: selected.length * 6, pricing: await modelPricing(),
      protocolHash: hash(SYSTEM_PROMPT + BUILDER_PROMPT), taskHash: hash(JSON.stringify(PILOT_SPEC)),
      sourceHash: hash(JSON.stringify(sourceFiles)), sourceFiles, episodes: [], ledger: budget.ledger,
    };
    atomicJson(resolve(output, 'protocol.json'), { inspector: SYSTEM_PROMPT, builder: BUILDER_PROMPT,
      maxDecisions: 14, maxPrimitives: 48, maxOutputTokens: 2200, temperature: 0 });
    const persist = () => {
      run!.ledger = structuredClone(budget.ledger);
      atomicJson(resolve(output, 'run.json'), run);
    };
    const storeFrame = (frame: Frame) => {
      const relative = `observations/${frame.hash}.png`;
      const path = resolve(output, relative);
      if (!existsSync(path)) writeFileSync(path, frame.buffer);
      return relative;
    };
    persist();
    try {
      for (const model of selected) for (const protocol of ['active', 'passive'] as Protocol[]) {
        const tasks = protocol === 'active' ? pilotTasks() : pilotTasks().slice(0, 2);
        for (const task of tasks) {
          progress({ status: 'running', runId: id, completed: run.episodes.length, total: run.plannedEpisodes, model });
          const env = new Environment(task, protocol);
          const result: EpisodeResult = {
            id: `${model.replaceAll('/', '_')}-${protocol}-${task.id}`,
            model, protocol, taskId: task.id, seed: task.seed, variant: task.variant, fault: task.fault,
            status: 'complete', score: env.score(), trace: [], finalImage: '',
          };
          run.episodes.push(result);
          let context: 'inspector' | 'builder' = 'inspector';
          let messages: Message[] = [{ role: 'system', content: SYSTEM_PROMPT }];
          try {
            while (env.phase !== 'done') {
              if (env.phase === 'build' && context === 'inspector') {
                context = 'builder';
                messages = [{ role: 'system', content: BUILDER_PROMPT }];
              }
              const observation: Observation = env.observe();
              const frame = await renderer.render(env.sceneParts(), env.view, env.visibleParts().map(p => p.id));
              const image = storeFrame(frame);
              messages.push({ role: 'user', content: [
                { type: 'text', text: JSON.stringify(observation) },
                { type: 'image_url', image_url: { url: `data:image/png;base64,${frame.buffer.toString('base64')}` } },
              ] });
              const response = await completion(key, model, messages, budget);
              const action = parseAction(response.content);
              env.step(action);
              result.trace.push({ index: result.trace.length, context, observation, image,
                action, response, feedback: env.feedback });
              messages.push({ role: 'assistant', content: response.content || '{}' });
              result.score = env.score();
              persist();
            }
          } catch (error) {
            result.status = 'error';
            result.error = error instanceof Error ? error.message : 'Unknown run error';
            throw error;
          } finally {
            result.score = env.score();
            result.finalImage = storeFrame(await renderer.render(env.built, env.view, env.built.map(p => p.id)));
            persist();
          }
        }
      }
      run.status = 'complete';
    } catch (error) {
      run.status = 'error';
      run.error = error instanceof Error ? error.message : 'Unknown run error';
    }
    run.completedAt = new Date().toISOString();
    persist();
    writeReport(run);
    atomicJson(resolve(ROOT, 'results/latest.json'), { id: run.id });
    progress({ status: run.status, runId: run.id, completed: run.episodes.length,
      total: run.plannedEpisodes, error: run.error });
    return run;
  } finally {
    unlinkSync(lock);
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const url = process.env.BENCHMARK_URL ?? 'http://127.0.0.1:5174';
  const renderer = new RenderService(url);
  try {
    const selected = process.argv.filter(a => a.startsWith('--model=')).map(a => a.slice(8));
    const run = await runPilot(renderer, selected.length ? selected : undefined, p => console.log(JSON.stringify(p)));
    console.log(JSON.stringify({ status: run.status, runId: run.id,
      actualUsd: run.ledger.charges.reduce((s, c) => s + (c.actual ?? 0), 0) }));
    if (run.status === 'error') process.exitCode = 1;
  } finally { await renderer.close(); }
}
