/** End-to-end synthetic fixtures. Never submit these as benchmark runs. */
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { root, hash, serializeModelRequest, SYSTEM_PROMPT } from '../ldraw-v2/publish';
import { wireRequest, encodeImage, parseModelOutput } from '../ldraw-v2/adapter';
import { labelPermutation, replaceLabels, alteredGraph } from '../ldraw-v2/conditions';
import { deriveAnswer } from '../ldraw-v2/oracle';
import { verifyRun } from './validate-run';

const read = (p: string) => JSON.parse(readFileSync(resolve(root, p), 'utf8'));
const template = read('benchmark/ldraw-v2/dry-runs/final-24c16a9d44fb-gpt41-standard-canary/manifest.json');
const catalog = read('benchmark/ldraw-v2/catalog.json');
const publicTasks = catalog.flatMap((m: any) => read(`public/benchmark/ldraw-v2/inputs/${m.id}.json`).tasks);
const internalTasks = catalog.flatMap((m: any) => read(`public/benchmark/ldraw-v2/models/${m.id}.json`).tasks);
const renders = read('benchmark/ldraw-v2/paired-renders.json').images;
const temp = mkdtempSync(resolve(tmpdir(), 'brickatlas-synthetic-'));
const write = (p: string, v: any) => writeFileSync(p, JSON.stringify(v, null, 2) + '\n');
const selected = [...new Set(publicTasks.map((t: any) => t.family))]
  .map(f => publicTasks.find((t: any) => t.family === f));
let count = 0;
function fixture(tasks: any[], condition: any, mode = 'correct', transport = 'openai') {
  const dir = resolve(temp, `run-${count++}`); mkdirSync(dir);
  mkdirSync(resolve(dir, 'requests')); mkdirSync(resolve(dir, 'receipts'));
  const m = structuredClone(template);
  Object.assign(m, { mode: 'synthetic-validation', fixtureOnly: true, status: 'complete', condition,
    taskIds: tasks.map(t => t.id), requests: [], calls: tasks.length, results: null });
  m.adapter.transport = transport;
  const submissions = [];
  for (const [i, task] of tasks.entries()) {
    const request = serializeModelRequest(task, condition, SYSTEM_PROMPT,
      path => encodeImage(readFileSync(resolve(root, 'public', path)), m.adapter.imageResolution));
    const text = JSON.stringify(wireRequest(request, m.adapter)) + '\n';
    const file = `requests/${task.id}.json`; writeFileSync(resolve(dir, file), text);
    m.requests.push({ taskId: task.id, file, sha256: hash(text) });
    const original = internalTasks.find((t: any) => t.id === task.id);
    let answer = structuredClone(original.answer);
    if (condition === 'wrong-image' && mode !== 'old') {
      answer = { choiceId: renders.find((r: any) => r.taskId === task.id && r.mode === 'wrong').mismatch.alternateChoiceId };
    }
    if (condition === 'graph-intervention') answer = deriveAnswer(alteredGraph(task), { instances: [] } as any);
    const mapping = condition === 'id-permutation' ? labelPermutation({
      question: task.promptEn, format: task.format, input: task.input, options: task.options,
    }) : {};
    answer = replaceLabels(answer, mapping);
    if (mode === 'missing' && i === 0) continue;
    if (mode === 'timeout') {
      write(resolve(dir, 'receipts', `${task.id}.json`), { ok: false, answer: null, error: 'Request timeout' });
      submissions.push({ id: task.id, answer: null }); continue;
    }
    const output = mode === 'invalid' ? 'not JSON' : JSON.stringify(answer);
    const payload = transport === 'openai'
      ? { model: m.adapter.modelId, choices: [{ message: { content: output } }] }
      : { model: m.adapter.modelId, content: [{ type: 'text', text: output }] };
    write(resolve(dir, 'receipts', `${task.id}.json`), {
      ok: true, httpStatus: 200, raw: JSON.stringify(payload), output, answer: parseModelOutput(output),
    });
    const inverse = Object.fromEntries(Object.entries(mapping).map(([a, b]) => [b, a]));
    submissions.push({ id: task.id, answer: replaceLabels(parseModelOutput(output), inverse) });
  }
  write(resolve(dir, 'submissions.json'), submissions); write(resolve(dir, 'manifest.json'), m);
  return dir;
}
try {
  const visual = selected.filter((t: any) => t.modality === 'visual');
  const graphs = selected.filter((t: any) => ['neighbors', 'graph-removal'].includes(t.family));
  const paths: Record<string, string> = {
    visual_A: fixture(visual, 'operand-only'), visual_B: fixture(visual, 'wrong-image'),
    visual_old: fixture(visual, 'wrong-image', 'old'), visual_invalid: fixture(visual, 'wrong-image', 'invalid'),
    visual_missing: fixture(visual, 'wrong-image', 'missing'), visual_timeout: fixture(visual, 'wrong-image', 'timeout'),
    visual_id: fixture(visual, 'id-permutation'), graph_A: fixture(graphs, 'standard'),
    graph_B: fixture(graphs, 'graph-intervention'), all_families: fixture(selected, 'standard'),
    anthropic_wrong: fixture(visual, 'wrong-image', 'correct', 'anthropic'),
  };
  const outputs: Record<string, any> = {};
  for (const [name, dir] of Object.entries(paths)) outputs[name] = verifyRun(dir, true);
  assert.throws(() => verifyRun(paths.visual_A), /Synthetic/);
  assert.equal(outputs.visual_B.rows.every((r: any) => r.success === 1 && r.original_gold_success === 0), true);
  assert.equal(outputs.visual_old.rows.every((r: any) => r.success === 0 && r.original_gold_success === 1), true);
  assert.equal(outputs.visual_missing.rows[0].failure_reason, 'missing-receipt');
  assert.equal(outputs.visual_timeout.rows[0].failure_reason, 'timeout');
  assert.equal(outputs.all_families.rows.every((r: any) => r.success === 1), true);
  const badDir = paths.visual_A, manifestPath = resolve(badDir, 'manifest.json'), original = read(manifestPath);
  const reject = (change: (m: any) => void) => {
    const m = structuredClone(original); change(m); write(manifestPath, m);
    assert.throws(() => verifyRun(badDir, true)); write(manifestPath, original);
  };
  reject(m => m.requests.push(m.requests[0]));
  reject(m => m.inputs[0].sha256 = 'wrong-dataset');
  reject(m => m.adapter.modelId = 'wrong-revision');
  reject(m => m.systemPromptSha256 = 'wrong-prompt');
  reject(m => m.condition = 'full-scene');
  reject(m => m.codeHashes['adapter.ts'] = 'wrong-adapter');
  const receiptPath = resolve(badDir, 'receipts', `${visual[0].id}.json`);
  const receipt = read(receiptPath);
  write(receiptPath, { ...receipt, answer: { choiceId: 'tampered' } });
  assert.throws(() => verifyRun(badDir, true), /answer\/raw/);
  write(receiptPath, receipt);
  assert.ok(process.argv[2], 'Supply fixture export output path');
  write(resolve(process.argv[2]), { fixture_only: true, outputs,
    assertions: ['strict actual-wire match', 'OpenAI and Anthropic raw parsing', 'alternate visual gold',
      'canonical ID mapping', 'executable actions', 'missing receipt retained', 'timeout classified',
      'duplicate/input/model/prompt/condition/adapter/raw tampering rejected', 'fixtures rejected from real ingestion'] });
  execFileSync('python3', [resolve(root, 'benchmark/suite/ldraw-evidence/test_publication_chain.py'),
    paths.all_families], { cwd: root, stdio: 'inherit' });
  console.log(`PASS: ${Object.keys(outputs).length} receipt fixtures; all tampering rejected`);
} finally { rmSync(temp, { recursive: true, force: true }); }
