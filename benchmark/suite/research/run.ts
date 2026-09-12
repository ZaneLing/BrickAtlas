import { closeSync, existsSync, mkdirSync, openSync, readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { isDeepStrictEqual } from 'node:util';
import { Budget, atomicJson } from '../../core/budget';
import { completion, MODELS, modelPricing, type Message } from '../../core/openrouter';
import { TASKS, type Kind } from '../shared';
import { ARTIFACTS, BENCHMARK, SUITE, SYSTEM, type ResultRow, type SuiteRun } from '../storage';
import { digest } from '../data';
import { parseJSON } from '../score';
import { SuiteRenderer } from '../render';
import { RESEARCH_VERSION, researchModels } from './dataset';
import { type Condition, researchTaskFor, researchScore } from './tasks';

export interface ResearchRun extends SuiteRun {
  research: true;
  cases: { modelId: string; kind: Kind; condition: Condition; taskId: string }[];
}
export function researchSelection() {
  const selected = (['test_id', 'test_ood'] as const).flatMap(split => {
    const seen = new Set<string>();
    return researchModels().filter(m => m.split === split && new Set(m.structure.parts.map(p => p.y)).size <= 13)
      .sort((a, b) => digest(a.group + 'paired-v1').localeCompare(digest(b.group + 'paired-v1')))
      .filter(m => { if (seen.has(m.family)) return false; seen.add(m.family); return true; }).slice(0, 2);
  });
  return selected.flatMap(m => TASKS.flatMap(kind => {
    const conditions: Condition[] = ['reconstruct', 'complete', 'repair'].includes(kind)
      ? ['ordinary', 'layers', 'symbolic'] : ['ordinary'];
    return conditions.map(condition => ({ modelId: m.id, kind, condition,
      taskId: researchTaskFor(m, kind, condition).public.id }));
  }));
}
function fingerprints() {
  return Object.fromEntries(['research/dataset.ts', 'research/tasks.ts', 'research/run.ts',
    'research/independent-check.ts', 'shared.ts', 'geometry.ts', 'score.ts', 'tasks.ts', 'web/viewer.ts',
    '../core/openrouter.ts', '../core/budget.ts']
    .map(file => [file, digest(readFileSync(resolve(SUITE, file), 'utf8'))]));
}
export async function runResearch(renderer: SuiteRenderer, onProgress: (p: { completed: number; total: number; runId: string }) => void = () => {},
  selectedModels: string[] = MODELS.map(m => m.id)) {
  if (!selectedModels.length || new Set(selectedModels).size !== selectedModels.length
    || selectedModels.some(id => !MODELS.some(m => m.id === id))) throw new Error('Invalid research model allowlist');
  if (!process.env.OPENROUTER_API_KEY) process.loadEnvFile(resolve(BENCHMARK, '../.env'));
  const key = process.env.OPENROUTER_API_KEY;
  if (!key) throw new Error('No API key');
  const lock = resolve(BENCHMARK, '.runtime/pilot.lock'), fd = openSync(lock, 'wx', 0o600);
  writeFileSync(fd, `${process.pid}\n`); closeSync(fd);
  try {
    const budget = new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json'));
    if (budget.blocked) throw new Error('Unsettled charge');
    const id = new Date().toISOString().replace(/[:.]/g, '-') + '-research';
    const dir = resolve(ARTIFACTS, 'runs', id); mkdirSync(resolve(dir, 'frames'), { recursive: true });
    const cases = researchSelection();
    const run: ResearchRun = {
      version: RESEARCH_VERSION, research: true, id, status: 'running', startedAt: new Date().toISOString(), completedAt: null,
      datasetHash: digest(researchModels()), protocolHash: digest(SYSTEM), sourceFiles: fingerprints(),
      cases, selection: cases.map(c => ({ ...c, split: researchModels().find(m => m.id === c.modelId)!.split })),
      selectionHash: digest(cases), models: selectedModels, mode: 'one-shot', representation: 'absolute',
      pricing: await modelPricing(), results: [], campaignBefore: budget.spent, campaignAfter: budget.spent,
    };
    const persist = () => { run.campaignAfter = budget.spent; atomicJson(resolve(dir, 'run.json'), run); atomicJson(resolve(dir, 'ledger.json'), budget.ledger); };
    atomicJson(resolve(dir, 'protocol.json'), { system: SYSTEM, cases,
      settings: { temperature: 0, maxOutputTokens: 2200, retries: 0 },
      note: 'Same heldout objects across tasks; visual conditions share surface and full-structure diagnostics. Cases sampled before requests.' });
    persist();
    try {
      for (const modelName of run.models) for (const entry of cases) {
        onProgress({ completed: run.results.length, total: cases.length * run.models.length, runId: id });
        const m = researchModels().find(m => m.id === entry.modelId)!;
        const t = researchTaskFor(m, entry.kind, entry.condition);
        const row: ResultRow = { taskId: t.public.id, modelId: m.id, group: m.group, family: m.family,
          split: m.split, kind: entry.kind, model: modelName, mode: 'one-shot', representation: 'absolute',
          input: t.public, frames: [], answers: [], calls: [], verdict: researchScore(t, null), status: 'complete' };
        run.results.push(row);
        try {
          const content: Exclude<Message['content'], string> = [{ type: 'text', text: JSON.stringify(t.public) }];
          for (const f of t.frames) {
            const frame = await renderer.render(f), path = `frames/${frame.hash}.png`;
            if (!existsSync(resolve(dir, path))) writeFileSync(resolve(dir, path), frame.buffer);
            row.frames.push(path);
            content.push({ type: 'text', text: f.title }, { type: 'image_url', image_url: { url: `data:image/png;base64,${frame.buffer.toString('base64')}` } });
          }
          const response = await completion(key, modelName, [{ role: 'system', content: SYSTEM }, { role: 'user', content }], budget);
          row.calls.push(response); row.answers.push(parseJSON(response.content));
          row.verdict = researchScore(t, row.answers[0]);
        } catch (e) {
          row.status = 'error'; row.error = (e as Error).message; throw e;
        } finally { persist(); }
      }
      run.status = 'complete';
    } catch (e) { run.status = 'error'; run.error = (e as Error).message; }
    run.completedAt = new Date().toISOString(); persist();
    writeResearchReport(run);
    return run;
  } finally { unlinkSync(lock); }
}
export function replayResearch(run: ResearchRun) {
  if (run.datasetHash !== digest(researchModels()) || !isDeepStrictEqual(run.sourceFiles, fingerprints())) throw new Error('Research source version changed');
  if (run.selectionHash !== digest(run.cases)) throw new Error('Selection changed');
  if (run.protocolHash !== digest(SYSTEM)) throw new Error('System prompt changed');
  let calls = 0, cost = 0;
  const caseKeys = new Set<string>(), callIds = new Set<string>();
  const dir = resolve(ARTIFACTS, 'runs', run.id);
  const ledger = JSON.parse(readFileSync(resolve(dir, 'ledger.json'), 'utf8'));
  for (const row of run.results) {
    const caseKey = `${row.model}:${row.taskId}`;
    if (caseKeys.has(caseKey) || !run.models.includes(row.model)) throw new Error('Duplicate or unknown case');
    caseKeys.add(caseKey);
    const c = run.cases.find(c => c.taskId === row.taskId)!;
    const t = researchTaskFor(researchModels().find(m => m.id === row.modelId)!, row.kind, c.condition);
    if (!isDeepStrictEqual(t.public, row.input)) throw new Error('Input drift');
    if (row.status === 'complete' && !isDeepStrictEqual(researchScore(t, row.answers[0]), row.verdict)) throw new Error('Score drift');
    for (const call of row.calls) {
      if (callIds.has(call.id)) throw new Error('Duplicate generation receipt');
      callIds.add(call.id);
      if (!isDeepStrictEqual(parseJSON(call.content), row.answers[0])) throw new Error('Response drift');
      const receipt = ledger.charges.find((c: { generationId: string }) => c.generationId === call.id);
      if (!receipt || receipt.actual !== call.cost || receipt.status !== 'settled') throw new Error('Receipt drift');
      cost += call.cost; calls++;
    }
    for (const path of row.frames) {
      if (!/^frames\/[a-f0-9]{64}\.png$/.test(path)
        || digest(readFileSync(resolve(dir, path)).toString('base64')) !== path.slice(7, -4)) throw new Error('Frame drift');
    }
  }
  if (Math.abs(cost - (run.campaignAfter - run.campaignBefore)) > 1e-8 || run.campaignAfter > 4.5) throw new Error('Campaign cost mismatch');
  if (run.status === 'complete' && run.results.length !== run.cases.length * run.models.length) throw new Error('Missing cases');
  return { run: run.id, cases: run.results.length, calls, cost, scoresReproduced: true };
}

export function groupResearch(run: ResearchRun) {
  const keys = [...new Set(run.results.map(r => `${r.model}|${r.kind}|${run.cases.find(c => c.taskId === r.taskId)!.condition}`))];
  return keys.map(key => {
    const [model, kind, condition] = key.split('|');
    const rows = run.results.filter(r => r.model === model && r.kind === kind
      && run.cases.find(c => c.taskId === r.taskId)?.condition === condition);
    const done = rows.filter(r => r.status === 'complete');
    const metricKeys = [...new Set(done.flatMap(r => Object.keys(r.verdict.metrics)))];
    const metrics = Object.fromEntries(metricKeys.map(k => {
      const values = done.map(r => r.verdict.metrics[k]).filter((n): n is number => typeof n === 'number');
      return [k, values.length ? values.reduce((a, b) => a + b, 0) / values.length : null];
    }));
    return { model, kind, condition, n: done.length, errors: rows.length - done.length, metrics,
      cost: rows.flatMap(r => r.calls).reduce((n, c) => n + c.cost, 0) };
  });
}
export function writeResearchReport(run: ResearchRun) {
  const groups = groupResearch(run), calls = run.results.flatMap(r => r.calls);
  const text = `# Composition grammar controlled evaluation

Status: ${run.status}; ${run.error ?? 'no infrastructure error'}.
Version: ${run.version}; ${run.results.length} cases; ${calls.length} calls.
Actual API cost: $${calls.reduce((n, c) => n + c.cost, 0).toFixed(8)}.
Campaign cumulative: $${run.campaignAfter.toFixed(8)} / $4.50.

The SAME four heldout objects are used across eight tasks. Visual reconstruction,
completion and repair have ordinary RGB+BOM, layer-revealed, and privileged symbolic
conditions. Other tasks have their task-default symbolic or isolated-part input.
This is a small paired development study, not a statistically powered leaderboard.

| Model | Task | Condition | n | Errors | Success | Full structure | Surface F1 | Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
${groups.map(g => `| ${g.model} | ${g.kind} | ${g.condition} | ${g.n} | ${g.errors} | ${g.metrics.success ?? 'N/A'} | ${g.metrics.fullStructureSuccess ?? 'N/A'} | ${g.metrics.surfaceF1 ?? 'N/A'} | $${g.cost.toFixed(6)} |`).join('\n')}

## Interpretation

- Primary visual score uses colored first-hit grid surfaces along positive X/Y/Z,
  legal geometry, BOM and preservation; hidden-layout alternatives are not forced
  to match one private reference. Full-structure correctness is separate.
- Generation uses envelope, anchoring, branching, connectivity and color-count
  constraints, not a supplied target voxel mask. It is not aesthetic text-to-3D.
- Editing is a whole-assembly spatial rotation; this is not arbitrary semantic editing.
- Geometry uses supported grid parts. Imported BrickNet catalog coverage is not
  equivalent to validated general connector or force simulation.
- No model receives a prior task's answer. Cases and source hashes were frozen before calls.
- Model, visibility condition and task remain separate; do not average conditions
  into one alleged visual-intelligence score.
- Human audit and broad external-data transfer have not been completed.

Dataset hash: ${run.datasetHash}
Selection hash: ${run.selectionHash}
Source hashes and full responses: run.json. Actual receipts: ledger.json.
`;
  writeFileSync(resolve(ARTIFACTS, 'runs', run.id, 'REPORT.md'), text);
}
