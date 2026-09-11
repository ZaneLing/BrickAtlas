import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { atomicJson, type Ledger } from '../core/budget';
import { models, digest, summary } from './data';
import { ARTIFACTS, BENCHMARK, SUITE, SYSTEM, auditOMR, buildData, defaultSelection, exportSFT, listRuns, runBaselines, sourceHashes } from './storage';
import { taskFor } from './tasks';
import { parseJSON, score } from './score';
import { runSuite } from './runner';
import { SuiteRenderer } from './render';
import { report } from './report';
import { TASKS, type Kind, type Mode } from './shared';

const [command, ...args] = process.argv.slice(2);
const option = (name: string, fallback: string) => args.find(a => a.startsWith(`--${name}=`))?.slice(name.length + 3) ?? fallback;
if (command === 'prepare') {
  console.log(JSON.stringify({ dataset: buildData(), baselines: Object.keys(runBaselines()).length,
    sft: exportSFT(), auditedOMR: auditOMR() }, null, 2));
} else if (command === 'run') {
  if (!args.includes('--paid')) throw new Error('Pass --paid to explicitly authorize this bounded paid run');
  const info = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
  const renderer = new SuiteRenderer(info.url);
  try {
    const representation = option('representation', 'absolute') as 'absolute' | 'relative';
    const selection = defaultSelection(representation);
    const kindFilter = option('tasks', '').split(',').filter(Boolean);
    if (kindFilter.some(k => !TASKS.includes(k as Kind))) throw new Error('Unknown task kind');
    const run = await runSuite(renderer, {
      models: option('models', 'openai/gpt-4.1-mini,google/gemini-2.5-flash').split(','),
      mode: option('mode', 'one-shot') as Mode, representation,
      selection: kindFilter.length ? selection.filter(s => kindFilter.includes(s.kind)) : selection,
    }, progress => console.log(JSON.stringify(progress)));
    console.log(JSON.stringify({ id: run.id, status: run.status, cost: run.campaignAfter - run.campaignBefore }));
    if (run.status === 'error') process.exitCode = 1;
  } finally { await renderer.close(); }
} else if (command === 'replay') {
  const evidence = [];
  for (const run of listRuns()) {
    assert.equal(run.datasetHash, summary().digest); assert.equal(run.protocolHash, digest(SYSTEM));
    assert.equal(run.selectionHash, digest(run.selection));
    assert.deepEqual(sourceHashes(), run.sourceFiles);
    const dir = resolve(ARTIFACTS, 'runs', run.id), ids = new Set<string>();
    const ledger = JSON.parse(readFileSync(resolve(dir, 'ledger.json'), 'utf8')) as Ledger;
    let cost = 0, complete = 0;
    for (const row of run.results) {
      const m = models().find(m => m.id === row.modelId)!;
      const task = taskFor(m, row.kind, row.representation);
      assert.deepEqual(task.public, row.input);
      for (const [i, call] of row.calls.entries()) {
        assert.deepEqual(parseJSON(call.content), row.answers[i]);
        assert.ok(!ids.has(call.id)); ids.add(call.id);
        const charge = ledger.charges.find(c => c.generationId === call.id);
        assert.ok(charge); assert.equal(charge.actual, call.cost); assert.equal(charge.status, 'settled');
        cost += call.cost;
      }
      if (row.status === 'complete') {
        assert.equal(row.calls.length, run.mode === 'one-shot' ? 1 : 2);
        assert.deepEqual(score(task, row.answers.at(-1)), row.verdict); complete++;
      }
      for (const path of row.frames) {
        assert.match(path, /^frames\/[a-f0-9]{64}\.png$/);
        assert.equal(digest(readFileSync(resolve(dir, path)).toString('base64')), path.slice(7, -4));
      }
    }
    assert.ok(Math.abs(cost - (run.campaignAfter - run.campaignBefore)) < 1e-8);
    assert.ok(run.campaignAfter <= 4.5);
    if (run.status === 'complete') assert.equal(complete, run.selection.length * run.models.length);
    report(run);
    evidence.push({ run: run.id, complete, requests: ids.size, cost, sourceMatches: true, scoresReproduced: true });
  }
  atomicJson(resolve(ARTIFACTS, 'replay.json'), evidence);
  console.log(JSON.stringify(evidence, null, 2));
} else if (command === 'score') {
  const path = option('predictions', '');
  if (!path) throw new Error('Provide --predictions=/absolute/path.jsonl');
  const representation = option('representation', 'absolute') as 'absolute' | 'relative';
  if (!['absolute', 'relative'].includes(representation)) throw new Error('Invalid representation');
  const selection = defaultSelection(representation);
  const lines = readFileSync(resolve(path), 'utf8').split('\n').filter(Boolean).map(l => JSON.parse(l));
  if (new Set(lines.map(l => l.taskId)).size !== lines.length) throw new Error('Duplicate task ID');
  if (lines.some(l => !selection.some(s => s.taskId === l.taskId))) throw new Error('Unknown task ID');
  const output = selection.map(s => {
    const task = taskFor(models().find(m => m.id === s.modelId)!, s.kind, representation);
    const row = lines.find(l => l.taskId === s.taskId);
    return { taskId: s.taskId, missing: !row, verdict: score(task, row?.answer ?? null) };
  });
  atomicJson(resolve(ARTIFACTS, 'external-scores.json'), output);
  console.log(JSON.stringify(output, null, 2));
} else if (command === 'export-inputs') {
  const output = resolve(BENCHMARK, '.runtime/suite-exports/inputs.jsonl');
  const imageDir = resolve(BENCHMARK, '.runtime/suite-exports/images');
  mkdirSync(imageDir, { recursive: true });
  const info = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
  const renderer = new SuiteRenderer(info.url);
  const rows = [];
  try {
    for (const s of defaultSelection()) {
      const t = taskFor(models().find(m => m.id === s.modelId)!, s.kind), images = [];
      for (const f of t.frames) {
        const frame = await renderer.render(f);
        writeFileSync(resolve(imageDir, `${frame.hash}.png`), frame.buffer);
        images.push(`images/${frame.hash}.png`);
      }
      rows.push({ taskId: t.public.id, system: SYSTEM, input: t.public,
        images, modality: t.frames.length ? 'RGB+text' : 'text/structure' });
    }
  } finally { await renderer.close(); }
  writeFileSync(output, rows.map(r => JSON.stringify(r)).join('\n') + '\n');
  console.log(output);
} else {
  console.log('Commands: prepare | run --paid [--models=...] [--mode=validator-once] [--representation=relative] [--tasks=...] | replay | score --predictions=... | export-inputs');
}
