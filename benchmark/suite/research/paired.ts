import { closeSync, copyFileSync, mkdirSync, openSync, readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { isDeepStrictEqual } from 'node:util';
import { atomicJson, Budget } from '../../core/budget';
import { completion, type Message } from '../../core/openrouter';
import { ARTIFACTS, BENCHMARK, SUITE, SYSTEM, listRuns, type ResultRow, type SuiteRun } from '../storage';
import { digest } from '../data';
import { legalityFeedback, parseJSON } from '../score';
import { researchModels, RESEARCH_VERSION } from './dataset';
import { researchTaskFor, researchScore } from './tasks';
import { replayResearch, type ResearchRun } from './run';

export const PAIRED_VERSION = 'composition-feedback-v1';
export type PairedRun = Omit<ResearchRun, 'mode' | 'results'> & {
  mode: 'paired-reflection' | 'paired-validation';
  results: (Omit<ResultRow, 'mode'> & { mode: string; refinementPrompt: string })[];
  paired: { parentRun: string; arm: 'reflection' | 'validation'; reusedFirstResponse: true };
};
function fingerprint() { return digest(readFileSync(resolve(SUITE, 'research/paired.ts'), 'utf8')); }
export async function runPaired() {
  const parent = listRuns().find(r => r.version === RESEARCH_VERSION && r.status === 'complete') as ResearchRun | undefined;
  if (!parent) throw new Error('Complete the main research experiment first');
  replayResearch(parent);
  if (!process.env.OPENROUTER_API_KEY) process.loadEnvFile(resolve(BENCHMARK, '../.env'));
  const key = process.env.OPENROUTER_API_KEY;
  if (!key) throw new Error('Missing API key');
  const model = 'google/gemini-2.5-flash';
  // Selection is by task and condition, never by model success/failure.
  const sources = parent.results.filter(r => r.model === model && ['generate', 'reconstruct', 'repair'].includes(r.kind)
    && parent.cases.find(c => c.taskId === r.taskId)?.condition === 'ordinary');
  if (sources.length !== 12) throw new Error('Expected twelve predeclared paired cases');
  const lock = resolve(BENCHMARK, '.runtime/pilot.lock'), fd = openSync(lock, 'wx', 0o600);
  writeFileSync(fd, `${process.pid}\n`); closeSync(fd);
  const output = [];
  try {
    const budget = new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json'));
    if (budget.blocked) throw new Error('Unsettled charge');
    for (const arm of ['reflection', 'validation'] as const) {
      const id = new Date().toISOString().replace(/[:.]/g, '-') + '-paired-' + arm;
      const dir = resolve(ARTIFACTS, 'runs', id); mkdirSync(resolve(dir, 'frames'), { recursive: true });
      const cases = parent.cases.filter(c => sources.some(r => r.taskId === c.taskId));
      const run: PairedRun = {
        ...parent, version: PAIRED_VERSION, id, mode: `paired-${arm}`, models: [model],
        startedAt: new Date().toISOString(), completedAt: null, status: 'running', error: undefined,
        cases, selection: parent.selection.filter(s => cases.some(c => c.taskId === s.taskId)),
        selectionHash: digest(cases), sourceFiles: { ...parent.sourceFiles, 'paired-extension': fingerprint() },
        results: [], campaignBefore: budget.spent, campaignAfter: budget.spent,
        paired: { parentRun: parent.id, arm, reusedFirstResponse: true },
      };
      const persist = () => { run.campaignAfter = budget.spent; atomicJson(resolve(dir, 'run.json'), run); atomicJson(resolve(dir, 'ledger.json'), budget.ledger); };
      atomicJson(resolve(dir, 'protocol.json'), { cases, parent: parent.id, arm,
        design: 'Identical first responses and images reused. Only one additional call per arm/case. No goal feedback.' });
      persist();
      try {
        for (const source of sources) {
          const refinementPrompt = arm === 'reflection'
            ? 'Review your previous answer once and submit a final JSON answer. No new scene information is provided.'
            : `Review your previous answer using this target-blind legality report: ${JSON.stringify(legalityFeedback(source.answers[0]))}. Submit a final JSON answer. No target error locations or target score are provided.`;
          const row = { ...structuredClone(source), mode: `paired-${arm}`, refinementPrompt };
          run.results.push(row);
          const content: Exclude<Message['content'], string> = [{ type: 'text', text: JSON.stringify(source.input) }];
          for (let i = 0; i < source.frames.length; i++) {
            const file = source.frames[i], image = readFileSync(resolve(ARTIFACTS, 'runs', parent.id, file));
            copyFileSync(resolve(ARTIFACTS, 'runs', parent.id, file), resolve(dir, file));
            content.push({ type: 'text', text: source.input.imageTitles[i] },
              { type: 'image_url', image_url: { url: `data:image/png;base64,${image.toString('base64')}` } });
          }
          try {
            const response = await completion(key, model, [
              { role: 'system', content: SYSTEM }, { role: 'user', content },
              { role: 'assistant', content: source.calls[0].content || '{}' },
              { role: 'user', content: refinementPrompt },
            ], budget);
            row.calls.push(response); row.answers.push(parseJSON(response.content));
            const c = cases.find(c => c.taskId === row.taskId)!;
            row.verdict = researchScore(researchTaskFor(researchModels().find(m => m.id === row.modelId)!, row.kind, c.condition), row.answers[1]);
          } catch (error) { row.status = 'error'; row.error = (error as Error).message; throw error; }
          finally { persist(); }
          console.log(JSON.stringify({ arm, completed: run.results.length, total: sources.length }));
        }
        run.status = 'complete';
      } catch (e) { run.status = 'error'; run.error = (e as Error).message; }
      run.completedAt = new Date().toISOString(); persist();
      const success = run.results.filter(r => r.verdict.metrics.success === 1).length;
      writeFileSync(resolve(dir, 'REPORT.md'), `# Paired ${arm} control

Parent: ${parent.id}. Status: ${run.status}.
The EXACT original first model responses are reused. The model gets one additional
${arm === 'reflection' ? 'reflection request without new information' : 'target-blind geometry validation report'}.
This is a fixed Harness experiment, not autonomous tool use.

Cases: ${run.results.length}/${sources.length}; final successes: ${success}.
New API charges: $${(run.campaignAfter - run.campaignBefore).toFixed(8)}.
The first call stored in each row is a reused historical receipt and must not be charged twice.
This small post-pilot paired control is exploratory, not a preregistered confirmation.
`);
      output.push(run);
      if (run.status === 'error') break;
    }
    return output;
  } finally { unlinkSync(lock); }
}
export function replayPaired(run: PairedRun) {
  if (run.sourceFiles['paired-extension'] !== fingerprint()) throw new Error('Paired implementation changed');
  const parent = listRuns().find(r => r.id === run.paired.parentRun) as ResearchRun;
  replayResearch(parent);
  if (run.selectionHash !== digest(run.cases) || run.protocolHash !== parent.protocolHash
    || run.datasetHash !== parent.datasetHash) throw new Error('Paired protocol changed');
  const ledger = JSON.parse(readFileSync(resolve(ARTIFACTS, 'runs', run.id, 'ledger.json'), 'utf8'));
  let cost = 0;
  const seen = new Set<string>();
  for (const row of run.results) {
    const source = parent.results.find(r => r.model === row.model && r.taskId === row.taskId)!;
    if (!source || seen.has(row.taskId)) throw new Error('Unknown or duplicate paired case');
    seen.add(row.taskId);
    if (row.status === 'complete' && row.calls.length !== 2) throw new Error('Missing refinement');
    if (!isDeepStrictEqual(row.calls[0], source.calls[0]) || !isDeepStrictEqual(row.input, source.input)) throw new Error('Initial-response pairing broken');
    const expectedPrompt = run.paired.arm === 'reflection'
      ? 'Review your previous answer once and submit a final JSON answer. No new scene information is provided.'
      : `Review your previous answer using this target-blind legality report: ${JSON.stringify(legalityFeedback(source.answers[0]))}. Submit a final JSON answer. No target error locations or target score are provided.`;
    if (row.refinementPrompt !== expectedPrompt) throw new Error('Refinement prompt changed');
    if (!isDeepStrictEqual(row.frames, source.frames)) throw new Error('Paired frames changed');
    for (const file of row.frames) {
      if (!/^frames\/[a-f0-9]{64}\.png$/.test(file)
        || digest(readFileSync(resolve(ARTIFACTS, 'runs', run.id, file)).toString('base64')) !== file.slice(7, -4)) throw new Error('Frame drift');
    }
    for (const [i, call] of row.calls.entries()) {
      if (!isDeepStrictEqual(parseJSON(call.content), row.answers[i])) throw new Error('Answer differs');
      if (i > 0) {
        const receipt = ledger.charges.find((c: { generationId: string }) => c.generationId === call.id);
        if (!receipt || receipt.actual !== call.cost || receipt.status !== 'settled') throw new Error('New charge mismatch');
        cost += call.cost;
      }
    }
    const c = run.cases.find(c => c.taskId === row.taskId)!;
    const expected = researchScore(researchTaskFor(researchModels().find(m => m.id === row.modelId)!, row.kind, c.condition), row.answers.at(-1));
    if (!isDeepStrictEqual(expected, row.verdict)) throw new Error('Paired score mismatch');
  }
  if (Math.abs(cost - (run.campaignAfter - run.campaignBefore)) > 1e-8) throw new Error('New charge total differs');
  if (run.status === 'complete' && run.results.length !== 12) throw new Error('Missing paired cases');
  return { run: run.id, cases: run.results.length, calls: run.results.reduce((n, r) => n + Math.max(0, r.calls.length - 1), 0),
    cost, pairedFirstResponsesVerified: true, scoresReproduced: true };
}
