import { closeSync, mkdirSync, openSync, readFileSync, readdirSync, unlinkSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { Budget, atomicJson } from '../../core/budget';
import { completion, type Message } from '../../core/openrouter';
import { BENCHMARK, SYSTEM } from '../storage';
import { relative, decode } from '../geometry';
import { legalityFeedback, parseJSON } from '../score';
import { getSpec, taskForV2 } from '../v2/cases';
import { evaluate } from '../v2/evaluate';
import { STUDY } from './protocol';
import { digest } from '../data';

export async function runControls() {
  const parentId = readdirSync(resolve(STUDY, 'runs')).filter(p => p.endsWith('-api')).sort().at(-1)!;
  const parent = JSON.parse(readFileSync(resolve(STUDY, 'runs', parentId, 'run.json'), 'utf8'));
  if (parent.status !== 'complete') throw new Error('Primary API run must complete first');
  if (!process.env.OPENROUTER_API_KEY) process.loadEnvFile(resolve(BENCHMARK, '../.env'));
  const key = process.env.OPENROUTER_API_KEY!;
  const lock = resolve(BENCHMARK, '.runtime/pilot.lock'), fd = openSync(lock, 'wx', 0o600);
  writeFileSync(fd, `${process.pid}\n`); closeSync(fd);
  try {
    const budget = new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json'));
    const model = 'google/gemini-2.5-flash';
    // Every policy contributes its first selected object. Never inspect outcomes.
    const selected = new Map<string, string>();
    for (const row of parent.rows) if (row.spec.kind !== 'parts' && !selected.has(row.spec.policy)) selected.set(row.spec.policy, row.spec.modelId);
    const rows = parent.rows.filter((r: any) => r.model === model && selected.get(r.spec.policy) === r.spec.modelId);
    const controls = rows.filter((r: any) => r.spec.kind === 'reconstruct').flatMap((row: any) =>
      ['no-image', 'mismatched-images', 'symbolic-reference', 'reflection', 'validation', 'repeat'].map(arm => ({ row, arm })));
    controls.push(...rows.filter((r: any) => r.spec.kind === 'plan' && r.spec.variant === 'assemble')
      .map((row: any) => ({ row, arm: 'relative' })));
    const id = new Date().toISOString().replace(/[:.]/g, '-') + '-controls', dir = resolve(STUDY, 'runs', id);
    mkdirSync(dir, { recursive: true });
    const run = { id, parentId, model, selection: controls.map((c: any) => ({ caseId: c.row.caseId, arm: c.arm })),
      rows: [] as unknown[], status: 'running', error: null as string | null, campaignBefore: budget.spent, campaignAfter: budget.spent,
      scriptHash: digest(readFileSync(resolve(BENCHMARK, 'suite/study/control.ts'), 'utf8')),
      note: 'Eight source objects, interleaved by case. Same-first-answer reflection/validation; fresh no-image, relative and repeat conditions. Exploratory fixed controls.' };
    const persist = () => { run.campaignAfter = budget.spent; atomicJson(resolve(dir, 'run.json'), run); atomicJson(resolve(dir, 'ledger.json'), budget.ledger); };
    persist();
    try {
      for (const { row, arm } of controls) {
        const input = structuredClone(row.input);
        if (arm === 'no-image') {
          input.imageTitles = []; input.prompt += ' Control condition: images are withheld. Use only the remaining public information.';
        }
        if (arm === 'relative') input.input.target = relative(decode(input.input.target)!);
        if (arm === 'symbolic-reference') {
          input.imageTitles = []; input.input.reference = taskForV2(getSpec(row.caseId)).target;
          input.prompt += ' Privileged diagnostic: use the supplied full symbolic reference; images are omitted.';
        }
        const other = rows.find((r: any) => r.spec.kind === 'reconstruct' && r.spec.modelId !== row.spec.modelId);
        const images = ['no-image', 'symbolic-reference'].includes(arm) ? []
          : arm === 'mismatched-images' ? other.images : row.images;
        const content: Exclude<Message['content'], string> = [{ type: 'text', text: JSON.stringify(input) }];
        for (const [i, path] of images.entries()) {
          const image = readFileSync(resolve(STUDY, 'inputs', path));
          content.push({ type: 'text', text: input.imageTitles[i] },
            { type: 'image_url', image_url: { url: 'data:image/png;base64,' + image.toString('base64') } });
        }
        const messages: Message[] = [{ role: 'system', content: SYSTEM }, { role: 'user', content }];
        let feedback: string | null = null;
        if (['reflection', 'validation'].includes(arm)) {
          feedback = arm === 'reflection' ? 'Review the previous answer once. No new scene information is supplied. Return final JSON.'
            : `Review the previous answer with this target-blind legality report: ${JSON.stringify(legalityFeedback(row.answer))}. Return final JSON.`;
          messages.push({ role: 'assistant', content: row.call.content || '{}' }, { role: 'user', content: feedback });
        }
        const call = await completion(key, model, messages, budget), answer = parseJSON(call.content);
        run.rows.push({ caseId: row.caseId, model, arm, input, images,
          imageDonor: arm === 'mismatched-images' ? other.caseId : null,
          feedback, reusedFirstCall: feedback ? row.call : null,
          call, answer, verdict: evaluate(taskForV2(getSpec(row.caseId)), answer) });
        persist(); console.log(JSON.stringify({ controls: run.rows.length, total: controls.length, spent: budget.spent }));
      }
      run.status = 'complete';
    } catch (e) { run.status = 'error'; run.error = (e as Error).message; }
    persist(); return { id, status: run.status, cases: run.rows.length, error: run.error };
  } finally { unlinkSync(lock); }
}
