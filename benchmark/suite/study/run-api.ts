import { closeSync, mkdirSync, openSync, readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { isDeepStrictEqual } from 'node:util';
import { Budget, atomicJson } from '../../core/budget';
import { completion, modelPricing, type Message } from '../../core/openrouter';
import { BENCHMARK, SYSTEM } from '../storage';
import { parseJSON } from '../score';
import { digest } from '../data';
import { sourceHashes } from '../v2/build';
import { getSpec, taskForV2 } from '../v2/cases';
import { evaluate } from '../v2/evaluate';
import { STUDY, type Prepared } from './protocol';

export async function runAPI() {
  const protocol = JSON.parse(readFileSync(resolve(STUDY, 'protocol.json'), 'utf8'));
  if (!isDeepStrictEqual(protocol.sourceHashes, sourceHashes())) throw new Error('Dataset source drift');
  const prepared = JSON.parse(readFileSync(resolve(STUDY, 'inputs/prepared.json'), 'utf8')) as Prepared[];
  if (digest(prepared.map(p => p.spec)) !== protocol.hash) throw new Error('Selection drift');
  if (!process.env.OPENROUTER_API_KEY) process.loadEnvFile(resolve(BENCHMARK, '../.env'));
  const key = process.env.OPENROUTER_API_KEY;
  if (!key) throw new Error('Missing API key');
  const lock = resolve(BENCHMARK, '.runtime/pilot.lock'), fd = openSync(lock, 'wx', 0o600);
  writeFileSync(fd, `${process.pid}\n`); closeSync(fd);
  try {
    const budget = new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json'));
    if (budget.blocked) throw new Error('Unsettled prior charge');
    const pricing = await modelPricing(), id = new Date().toISOString().replace(/[:.]/g, '-') + '-api';
    const dir = resolve(STUDY, 'runs', id); mkdirSync(dir, { recursive: true });
    const rows: unknown[] = [];
    const run = { id, version: 'study-v1', protocol, pricing, status: 'running', error: null as string | null,
      campaignBefore: budget.spent, campaignAfter: budget.spent, rows,
      runnerHash: digest(readFileSync(resolve(BENCHMARK, 'suite/study/run-api.ts'), 'utf8')) };
    const persist = () => { run.campaignAfter = budget.spent; atomicJson(resolve(dir, 'run.json'), run); atomicJson(resolve(dir, 'ledger.json'), budget.ledger); };
    persist();
    try {
      // Interleave models by case, preserving exactly the same scene information.
      for (const [i, p] of prepared.entries()) for (const model of protocol.settings.models) {
        const task = taskForV2(getSpec(p.spec.id));
        if (!isDeepStrictEqual(p.input, task.public)) throw new Error('Input changed');
        const content: Exclude<Message['content'], string> = [{ type: 'text', text: JSON.stringify(p.input) }];
        for (const [j, path] of p.images.entries()) {
          const buffer = readFileSync(resolve(STUDY, 'inputs', path));
          if (digest(buffer.toString('base64')) !== path.slice(7, -4)) throw new Error('Image hash changed');
          content.push({ type: 'text', text: p.input.imageTitles[j] },
            { type: 'image_url', image_url: { url: 'data:image/png;base64,' + buffer.toString('base64') } });
        }
        // Preserve at least $0.50 of the original cap for fixed controls.
        if (budget.spent > 3.7) throw new Error('Study allocation reached; remaining uncalled cases are not complete');
        const call = await completion(key, model, [{ role: 'system', content: SYSTEM }, { role: 'user', content }], budget);
        const answer = parseJSON(call.content);
        rows.push({ caseId: p.spec.id, spec: p.spec, model, input: p.input, images: p.images, call, answer, verdict: evaluate(task, answer) });
        persist();
        console.log(JSON.stringify({ completed: rows.length, total: prepared.length * 2, spent: budget.spent, case: i + 1 }));
      }
      run.status = 'complete';
    } catch (e) { run.status = 'error'; run.error = (e as Error).message; }
    persist(); return { id, status: run.status, completed: rows.length, error: run.error, spent: budget.spent };
  } finally { unlinkSync(lock); }
}
