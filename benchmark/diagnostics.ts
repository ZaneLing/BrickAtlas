import { closeSync, existsSync, mkdirSync, openSync, readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { Budget, atomicJson } from './core/budget';
import { Environment } from './core/environment';
import { BUILDER_PROMPT } from './core/prompts';
import { MODELS, completion, modelPricing, type Message } from './core/openrouter';
import { RenderService } from './core/render-service';
import { makeTask } from './core/tasks';
import type { TraceStep } from './core/results';
import { ROOT, hash, loadKey, parseAction } from './run';

const latest = JSON.parse(readFileSync(resolve(ROOT, 'results/latest.json'), 'utf8')) as { id: string };
if (!/^[\w.-]{1,100}$/.test(latest.id)) throw new Error('Invalid run ID');
const output = resolve(ROOT, 'results', latest.id);
const resultPath = resolve(output, 'diagnostics.json');
if (existsSync(resultPath)) throw new Error('Diagnostic results already exist; refusing an accidental paid repeat');
const info = JSON.parse(readFileSync(resolve(ROOT, '.runtime/server.json'), 'utf8')) as { url: string };
const key = loadKey();
if (!key) throw new Error('OPENROUTER_API_KEY missing');
const lock = resolve(ROOT, '.runtime/pilot.lock');
const fd = openSync(lock, 'wx', 0o600);
writeFileSync(fd, `${process.pid}\n`);
closeSync(fd);
const renderer = new RenderService(info.url);
try {
  const budget = new Budget(resolve(ROOT, '.runtime/campaign-ledger.json'));
  const result = {
    protocol: 'oracle-blueprint-conditioned-builder-v1',
    parentRun: latest.id,
    startedAt: new Date().toISOString(), completedAt: null as string | null,
    status: 'running', error: null as string | null,
    blueprintSource: 'oracle (not model generated)',
    promptHash: hash(BUILDER_PROMPT),
    scriptHash: hash(readFileSync(resolve(ROOT, 'diagnostics.ts'))),
    pricing: await modelPricing(),
    cases: [] as {
      model: string; fault: string; status: string; error?: string;
      finalExact: boolean; faultTriggered: boolean; recoveryEligible: boolean;
      recoverySuccess: boolean | null; finalF1: number; actions: number;
      cost: number; trace: TraceStep[]; finalImage: string;
    }[],
    ledger: budget.ledger,
  };
  const persist = () => {
    result.ledger = structuredClone(budget.ledger);
    atomicJson(resultPath, result);
  };
  const frameFor = async (env: Environment) => {
    const frame = await renderer.render(env.sceneParts(), env.view, env.visibleParts().map(p => p.id));
    const relative = `observations/${frame.hash}.png`;
    mkdirSync(resolve(output, 'observations'), { recursive: true });
    if (!existsSync(resolve(output, relative))) writeFileSync(resolve(output, relative), frame.buffer);
    return { frame, relative };
  };
  persist();
  try {
    for (const model of MODELS) for (const fault of ['none', 'missing', 'offset'] as const) {
      console.log(JSON.stringify({ model: model.id, fault, completed: result.cases.length, total: 6 }));
      const env = new Environment(makeTask(41, 0, fault));
      env.step({ type: 'blueprint', blueprint: { version: 1, parts: env.task.target } });
      const item = { model: model.id, fault, status: 'running', finalExact: false,
        faultTriggered: false, recoveryEligible: false, recoverySuccess: null as boolean | null,
        finalF1: 0, actions: 0, cost: 0, trace: [] as TraceStep[], finalImage: '' };
      result.cases.push(item);
      const messages: Message[] = [{ role: 'system', content: BUILDER_PROMPT }];
      while (env.phase !== 'done') {
        const observation = env.observe();
        const { frame, relative } = await frameFor(env);
        messages.push({ role: 'user', content: [
          { type: 'text', text: JSON.stringify(observation) },
          { type: 'image_url', image_url: { url: `data:image/png;base64,${frame.buffer.toString('base64')}` } },
        ] });
        const response = await completion(key, model.id, messages, budget);
        const action = parseAction(response.content);
        env.step(action);
        item.trace.push({ index: item.trace.length, context: 'builder', observation, image: relative,
          action, response, feedback: env.feedback });
        item.cost += response.cost;
        messages.push({ role: 'assistant', content: response.content || '{}' });
        persist();
      }
      const score = env.score();
      Object.assign(item, {
        status: 'complete', finalExact: score.construction.exact,
        faultTriggered: score.faultTriggered, recoveryEligible: score.faultEligible,
        recoverySuccess: score.recoverySuccess, finalF1: score.construction.partF1,
        actions: score.actions - 1, finalImage: (await frameFor(env)).relative,
      });
      persist();
    }
    result.status = 'complete';
  } catch (e) {
    result.status = 'error';
    result.error = (e as Error).message;
    const last = result.cases.at(-1);
    if (last?.status === 'running') { last.status = 'error'; last.error = result.error; }
  }
  result.completedAt = new Date().toISOString();
  persist();
  console.log(JSON.stringify({ status: result.status, cases: result.cases.length,
    diagnosticsUsd: result.cases.reduce((s, c) => s + c.cost, 0), campaign: budget.summary() }));
  if (result.status === 'error') process.exitCode = 1;
} finally {
  await renderer.close();
  unlinkSync(lock);
}
