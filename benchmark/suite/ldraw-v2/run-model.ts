import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync } from 'node:fs';
import { resolve, relative } from 'node:path';
import { execFileSync } from 'node:child_process';
import { parseArgs } from 'node:util';
import { root, site, hash, loadPublicBundle, serializeModelRequest, SYSTEM_PROMPT, assertNoPrivateFields } from './publish';
import { conditions, eligible, labelPermutation, replaceLabels } from './conditions';
import { validateAdapter, wireRequest, encodeImage, sendRequest, type Adapter } from './adapter';
import type { Condition } from './types';
import { scoreLDrawBatch } from './score';

const { values } = parseArgs({ options: {
  help: { type: 'boolean' }, adapter: { type: 'string' }, out: { type: 'string' },
  condition: { type: 'string', default: 'standard' }, input: { type: 'string' },
  tasks: { type: 'string' }, limit: { type: 'string' }, execute: { type: 'boolean', default: false },
}});
if (values.help) {
  console.log(`Usage: tsx run-model.ts --adapter model-adapters/gpt41.json --out DIR
  [--condition ${conditions.join('|')}]
  [--input PATH_TO_V2_INPUT_JSON] [--tasks TASK_ID_ARRAY_JSON] [--limit N] [--execute]
Default: offline dry run; writes the exact wire bodies and hashes, no API calls.
Output directory must be new. --execute sends one call per item, without retries.
Internal models/*.json paths are rejected. Missing/failed outputs remain failures.`);
  process.exit(0);
}
assert.ok(values.adapter && values.out, '--adapter and --out required; use --help');
const condition = values.condition as Condition;
assert.ok(conditions.includes(condition));
const adapter: Adapter = JSON.parse(readFileSync(resolve(values.adapter), 'utf8'));
validateAdapter(adapter, values.execute);
assert.equal(adapter.systemPrompt, 'SYSTEM_PROMPT in publish.ts (validated and hashed at run time)');
const files = values.input ? [resolve(values.input)] : readdirSync(resolve(site, 'inputs')).filter(f => f.endsWith('.json'))
  .sort().map(f => resolve(site, 'inputs', f));
let tasks = files.flatMap(f => loadPublicBundle(f).tasks).filter(t => eligible(t, condition));
if (values.tasks) {
  const ids: unknown = JSON.parse(readFileSync(resolve(values.tasks), 'utf8'));
  assert.ok(Array.isArray(ids) && ids.every(id => typeof id === 'string') && new Set(ids).size === ids.length);
  assert.ok(ids.every(id => tasks.some(t => t.id === id)), 'Task list contains ineligible/unknown IDs');
  tasks = tasks.filter(t => ids.includes(t.id));
}
tasks.sort((a, b) => a.id.localeCompare(b.id));
if (values.limit) {
  const n = Number(values.limit); assert.ok(Number.isSafeInteger(n) && n > 0);
  tasks = tasks.slice(0, n);
}
assert.ok(tasks.length, 'No eligible tasks');
const out = resolve(values.out);
assert.ok(!existsSync(out), 'Choose a new run directory; never overwrite a run');
mkdirSync(resolve(out, 'requests'), { recursive: true });
mkdirSync(resolve(out, 'receipts'));
const write = (file: string, value: unknown) => writeFileSync(resolve(out, file), JSON.stringify(value, null, 2) + '\n');
const sourceCode = ['publish.ts', 'adapter.ts', 'conditions.ts', 'score.ts', 'oracle.ts', 'run-model.ts',
  '../../../src/benchmark-v2/scoring.ts', '../../../src/benchmark/engine.ts'];
const manifest: any = {
  release: 'brickatlas-ldraw-2', mode: values.execute ? 'live-inference' : 'offline-dry-run',
  status: 'preparing', startedAt: new Date().toISOString(), condition, adapter,
  gitCommit: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim(),
  nodeVersion: process.version, packageLockSha256: hash(readFileSync(resolve(root, 'package-lock.json'))),
  codeHashes: Object.fromEntries(sourceCode.map(f => [f, hash(readFileSync(resolve(import.meta.dirname, f)))])),
  systemPromptSha256: hash(SYSTEM_PROMPT), taskIds: tasks.map(t => t.id),
  inputs: files.map(f => ({ file: relative(root, f), sha256: hash(readFileSync(f)) })),
  requests: [], calls: 0, results: null,
};
write('manifest.json', manifest);
const requests: { id: string; body: string; inverse: Record<string, string> }[] = [];
const imageCache = new Map<string, string>();
// Prepare every request before the first network call. No scoring bundle reads.
for (const task of tasks) {
  const request = serializeModelRequest(task, condition, SYSTEM_PROMPT, path => {
    if (!imageCache.has(path)) imageCache.set(path, encodeImage(readFileSync(resolve(root, 'public', path)), adapter.imageResolution));
    return imageCache.get(path)!;
  });
  const body = wireRequest(request, adapter);
  assertNoPrivateFields(body);
  const text = JSON.stringify(body) + '\n';
  writeFileSync(resolve(out, 'requests', `${task.id}.json`), text);
  const map = condition === 'id-permutation' ? labelPermutation({
    question: task.promptEn, format: task.format, input: task.input, options: task.options,
  }) : {};
  requests.push({ id: task.id, body: text, inverse: Object.fromEntries(Object.entries(map).map(([a, b]) => [b, a])) });
  manifest.requests.push({ taskId: task.id, file: `requests/${task.id}.json`, sha256: hash(text) });
}
manifest.status = values.execute ? 'running' : 'dry-run-complete';
write('manifest.json', manifest);
if (values.execute) {
  const submissions = [];
  for (const request of requests) {
    manifest.calls++;
    let receipt: any;
    try { receipt = await sendRequest(request.body, adapter); }
    catch (error) { receipt = { ok: false, error: error instanceof Error ? error.message : String(error), answer: null }; }
    write(`receipts/${request.id}.json`, receipt);
    submissions.push({ id: request.id, answer: receipt.answer ? replaceLabels(receipt.answer, request.inverse) : null });
    write('submissions.json', submissions);
    write('manifest.json', manifest);
    console.log(`${submissions.length}/${requests.length}: ${request.id}, response=${receipt.ok ? 'received' : 'failed'}`);
  }
  // Scoring occurs only after all actual model requests have been saved/sent.
  const result = scoreLDrawBatch(submissions, tasks.map(t => t.id), condition === 'graph-intervention');
  write('scores.json', result);
  manifest.status = 'complete'; manifest.results = { success: result.success, total: result.expected };
  manifest.completedAt = new Date().toISOString(); write('manifest.json', manifest);
}
console.log(JSON.stringify({ status: manifest.status, tasks: tasks.length, calls: manifest.calls, out }, null, 2));
