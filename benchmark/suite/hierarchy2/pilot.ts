import { readFileSync, writeFileSync, mkdirSync, openSync, closeSync, unlinkSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { Budget } from '../../core/budget';
import { completion, modelPricing, requestCeiling, type Message } from '../../core/openrouter';
import { score } from '../../../src/benchmark/engine';
import { OUT, sha } from './release';
import type { Task } from '../../../src/benchmark/types';

const benchmark = resolve(import.meta.dirname, '../..');
const root = resolve(benchmark, '..');
if (existsSync(resolve(OUT, 'pilot/run.json'))) throw new Error('Pilot already archived; use offline replay, not a new billed run');
if (!process.env.OPENROUTER_API_KEY) process.loadEnvFile(resolve(root, '.env'));
const catalog = JSON.parse(readFileSync(resolve(OUT, 'catalog.json'), 'utf8'));
const families = ['boundary', 'information-gain', 'service-repair', 'scheduling'];
const tasks: Task[] = ['D1', 'D2', 'D3', 'D4'].flatMap(d => families.map((family, i) => {
  const m = catalog.filter((m: any) => m.difficulty === d)[i * 2];
  const bundle = JSON.parse(readFileSync(resolve(OUT, 'models', `${m.id}.json`), 'utf8'));
  return bundle.tasks.find((t: Task) => t.family === family);
}));
const model = 'openai/gpt-4.1-mini', allocation = 0.10;
const lock = resolve(benchmark, '.runtime/pilot.lock');
const fd = openSync(lock, 'wx', 0o600); closeSync(fd);
const budget = new Budget(resolve(benchmark, '.runtime/campaign-ledger.json'));
const before = budget.spent, results: any[] = [];
mkdirSync(resolve(OUT, 'pilot'), { recursive: true });
const run: any = { version: 'brickatlas-hierarchy-2', model, cases: tasks.map(t => t.id), status: 'running',
  before, after: before, allocation, publicHash: sha(resolve(OUT, 'public.json')), results, error: null };
const save = () => {
  run.after = budget.spent;
  writeFileSync(resolve(OUT, 'pilot/run.json'), JSON.stringify(run, null, 2) + '\n');
};
try {
  if (budget.blocked) throw new Error('Unsettled campaign charge');
  run.pricing = (await modelPricing()).filter(p => p.id === model);
  save();
  for (const t of tasks) {
    const { answer, ...pub } = t;
    const imagePath = resolve(OUT, 'images', `${t.modelId}-iso.png`);
    const messages: Message[] = [
      { role: 'system', content: 'Solve the public benchmark contract. Output JSON only. MCQ uses choiceId or choiceIds. Actions use actionIds. Schedules use starts: {jobId: integer}. Do not explain.' },
      { role: 'user', content: [{ type: 'text', text: JSON.stringify(pub) },
        { type: 'image_url', image_url: { url: `data:image/png;base64,${readFileSync(imagePath).toString('base64')}` } }] },
    ];
    const { ceiling } = requestCeiling(model, messages);
    if (budget.spent - before + ceiling > allocation) throw new Error('Pilot ceiling reached before request');
    const call = await completion(process.env.OPENROUTER_API_KEY!, model, messages, budget);
    let prediction: unknown = null;
    try { prediction = JSON.parse(call.content); } catch { /* invalid remains a failed response */ }
    results.push({ id: t.id, difficulty: t.difficulty, layer: t.layer, family: t.family,
      imageHash: sha(imagePath), prediction, verdict: score(t, prediction), call });
    save(); console.log(`${results.length}/16 ${t.difficulty} ${t.family}: ${results.at(-1).verdict.success}`);
  }
  run.status = 'complete';
} catch (e) { run.status = 'error'; run.error = String(e); }
finally { save(); unlinkSync(lock); }
console.log(JSON.stringify({ status: run.status, n: results.length, cost: run.after - before, error: run.error }));
