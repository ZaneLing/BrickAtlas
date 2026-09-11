import { closeSync, existsSync, mkdirSync, openSync, readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { Budget, atomicJson } from '../core/budget';
import { completion, modelPricing, MODELS, type Message } from '../core/openrouter';
import { digest, models, summary } from './data';
import { MODELS as ALLOWED } from '../core/openrouter';
import { type Mode, VERSION } from './shared';
import { taskFor } from './tasks';
import { legalityFeedback, parseJSON, score } from './score';
import { SuiteRenderer } from './render';
import { ARTIFACTS, BENCHMARK, SYSTEM, defaultSelection, sourceHashes, type ResultRow, type Selection, type SuiteRun } from './storage';
import { report } from './report';

export interface Options {
  models?: string[]; mode?: Mode; representation?: 'absolute' | 'relative'; selection?: Selection[];
}
export interface Progress { running: boolean; completed: number; total: number; runId?: string; error?: string }
export async function runSuite(renderer: SuiteRenderer, options: Options = {}, onProgress: (p: Progress) => void = () => {}) {
  const selected = options.models ?? MODELS.map(m => m.id);
  const mode = options.mode ?? 'one-shot', representation = options.representation ?? 'absolute';
  if (!selected.length || selected.length > 2 || new Set(selected).size !== selected.length
    || selected.some(m => !ALLOWED.some(x => x.id === m))
    || !['one-shot', 'validator-once'].includes(mode)
    || !['absolute', 'relative'].includes(representation)) throw new Error('Unsupported run configuration');
  const selection = options.selection ?? defaultSelection(representation);
  if (!selection.length || selection.length > 32 || new Set(selection.map(s => s.taskId)).size !== selection.length) throw new Error('Invalid smoke selection');
  for (const s of selection) {
    const m = models().find(m => m.id === s.modelId);
    if (!m || m.split !== s.split || !['test_id', 'test_ood'].includes(s.split)
      || taskFor(m, s.kind, representation).public.id !== s.taskId) throw new Error('Selection differs from dataset/protocol');
  }
  if (!process.env.OPENROUTER_API_KEY && existsSync(resolve(BENCHMARK, '../.env'))) process.loadEnvFile(resolve(BENCHMARK, '../.env'));
  const key = process.env.OPENROUTER_API_KEY;
  if (!key) throw new Error('OPENROUTER_API_KEY missing');
  mkdirSync(resolve(BENCHMARK, '.runtime'), { recursive: true });
  const lock = resolve(BENCHMARK, '.runtime/pilot.lock');
  const fd = openSync(lock, 'wx', 0o600); writeFileSync(fd, `${process.pid}\n`); closeSync(fd);
  try {
    const budget = new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json'));
    if (budget.blocked) throw new Error('Unsettled campaign charge; reconcile first');
    const id = new Date().toISOString().replace(/[:.]/g, '-') + '-' + mode;
    const dir = resolve(ARTIFACTS, 'runs', id);
    mkdirSync(resolve(dir, 'frames'), { recursive: true });
    const run: SuiteRun = {
      version: VERSION, id, status: 'running', startedAt: new Date().toISOString(), completedAt: null,
      datasetHash: summary().digest, protocolHash: digest(SYSTEM), sourceFiles: sourceHashes(),
      selection, selectionHash: digest(selection), models: selected, mode, representation,
      pricing: await modelPricing(), results: [], campaignBefore: budget.spent, campaignAfter: budget.spent,
    };
    const persist = () => {
      run.campaignAfter = budget.spent;
      atomicJson(resolve(dir, 'run.json'), run);
      atomicJson(resolve(dir, 'ledger.json'), budget.ledger);
    };
    atomicJson(resolve(dir, 'protocol.json'), { system: SYSTEM, selection, mode, representation,
      maxOutputTokens: 2200, temperature: 0, imageProtocol: 'assembled RGB plus disclosed top-down layer inspections',
      failedOutputsCountAsFailures: true, retries: 0 });
    persist();
    try {
      for (const model of selected) for (const entry of selection) {
        onProgress({ running: true, completed: run.results.length, total: selected.length * selection.length, runId: id });
        const m = models().find(m => m.id === entry.modelId)!;
        const task = taskFor(m, entry.kind, representation);
        const row: ResultRow = {
          taskId: task.public.id, modelId: m.id, group: m.group, family: m.family, split: m.split, kind: entry.kind,
          model, mode, representation, input: task.public, frames: [], answers: [], calls: [],
          verdict: score(task, null), status: 'complete',
        };
        run.results.push(row);
        try {
          const content: Exclude<Message['content'], string> = [
            { type: 'text', text: JSON.stringify({ prompt: task.public.prompt, input: task.public.input,
              responseSchema: task.public.responseSchema, imageTitles: task.public.imageTitles }) },
          ];
          for (const frameSpec of task.frames) {
            const frame = await renderer.render(frameSpec);
            const path = `frames/${frame.hash}.png`;
            if (!existsSync(resolve(dir, path))) writeFileSync(resolve(dir, path), frame.buffer);
            row.frames.push(path);
            content.push({ type: 'text', text: frameSpec.title },
              { type: 'image_url', image_url: { url: `data:image/png;base64,${frame.buffer.toString('base64')}` } });
          }
          const messages: Message[] = [{ role: 'system', content: SYSTEM }, { role: 'user', content }];
          const first = await completion(key, model, messages, budget);
          row.calls.push(first);
          row.answers.push(parseJSON(first.content));
          row.verdict = score(task, row.answers[0]);
          persist();
          if (mode === 'validator-once') {
            // Always give exactly one target-blind check; never use target score as a retry trigger.
            messages.push({ role: 'assistant', content: first.content || '{}' }, { role: 'user',
              content: `One target-blind validation report: ${JSON.stringify(legalityFeedback(row.answers[0]))}. Submit your final answer once more; no further checks.` });
            const second = await completion(key, model, messages, budget);
            row.calls.push(second); row.answers.push(parseJSON(second.content));
            row.verdict = score(task, row.answers[1]);
          }
        } catch (error) {
          row.status = 'error'; row.error = (error as Error).message;
          throw error;
        } finally { persist(); }
      }
      run.status = 'complete';
    } catch (error) {
      run.status = 'error'; run.error = (error as Error).message;
    }
    run.completedAt = new Date().toISOString();
    persist(); report(run);
    onProgress({ running: false, completed: run.results.length, total: selected.length * selection.length, runId: id, error: run.error });
    return run;
  } finally { unlinkSync(lock); }
}
