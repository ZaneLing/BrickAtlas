import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { parseArgs } from 'node:util';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
import { validateAdapter, wireRequest, sendRequest, type Adapter } from '../ldraw-v2/adapter';
import { SYSTEM_PROMPT } from '../ldraw-v2/publish';

const { values } = parseArgs({ options: {
  help: { type: 'boolean' }, adapter: { type: 'string' }, out: { type: 'string' },
  execute: { type: 'boolean', default: false },
} });
if (values.help) {
  console.log('Usage: tsx run-matched-graphs.ts --adapter FILE --out NEW_DIR [--execute]\nDefault is an offline snapshot. All observations are separate requests in the frozen shuffled order. No parent IDs, transformation types or answer directions enter prompts.');
  process.exit(0);
}
assert.ok(values.adapter && values.out, 'Adapter and fresh output directory required');
const root = resolve(import.meta.dirname, '../../..');
const data = resolve(root, 'benchmark/ldraw-evidence-v1/matched-graphs-v1');
const hash = (s: string | Buffer) => createHash('sha256').update(s).digest('hex');
const inputBytes = readFileSync(resolve(data, 'inputs.json'));
const inputs = JSON.parse(inputBytes.toString());
assert.equal(inputs.extension_version, 'ldraw2-matched-graphs-v1');
assert.equal(inputs.role, 'model-input');
const adapterBytes = readFileSync(resolve(values.adapter));
const adapter: Adapter = JSON.parse(adapterBytes.toString());
validateAdapter(adapter, values.execute);
const out = resolve(values.out);
assert.ok(!existsSync(out), 'Never overwrite a run');
mkdirSync(resolve(out, 'requests'), { recursive: true });
mkdirSync(resolve(out, 'receipts'));
const write = (name: string, value: unknown) => writeFileSync(resolve(out, name), JSON.stringify(value, null, 2) + '\n');
const manifest: any = { release: 'ldraw2-matched-graphs-v1', analysis_version: 'ldraw2-evidence-v1',
  mode: values.execute ? 'live-inference' : 'offline-dry-run', status: 'preparing',
  condition: 'shuffled-independent-hypothetical-graphs', adapter, adapter_hash: hash(adapterBytes),
  dataset_hash: hash(inputBytes), systemPromptSha256: hash(SYSTEM_PROMPT),
  code_hashes: Object.fromEntries(['run-matched-graphs.ts', '../ldraw-v2/adapter.ts', '../ldraw-v2/publish.ts']
    .map(f => [f, hash(readFileSync(resolve(import.meta.dirname, f)))])),
  taskIds: inputs.observations.map((o: any) => o.id), requests: [], calls: 0, results: null };
const requests = [];
for (const o of inputs.observations) {
  assert.deepEqual(Object.keys(o.payload).sort(), ['format', 'input', 'question']);
  const request = wireRequest({ messages: [{ role: 'system', content: SYSTEM_PROMPT },
    { role: 'user', content: [{ type: 'text', text: JSON.stringify(o.payload) }] }] }, adapter);
  const body = JSON.stringify(request) + '\n';
  const filename = `requests/${o.id}.json`;
  writeFileSync(resolve(out, filename), body);
  manifest.requests.push({ taskId: o.id, file: filename, sha256: hash(body) });
  requests.push({ id: o.id, body });
}
manifest.status = values.execute ? 'running' : 'dry-run-complete';
write('manifest.json', manifest);
if (values.execute) {
  const submissions = [];
  for (const r of requests) {
    const started = performance.now();
    manifest.calls++;
    let receipt;
    try { receipt = await sendRequest(r.body, adapter); }
    catch (error) { receipt = { ok: false, error: String(error), answer: null, latencyMs: performance.now() - started }; }
    write(`receipts/${r.id}.json`, receipt);
    submissions.push({ id: r.id, answer: receipt.answer });
    write('submissions.json', submissions); write('manifest.json', manifest);
  }
  // Gold is read only after every request is sent.
  const internal = JSON.parse(readFileSync(resolve(data, 'manifest.json'), 'utf8'));
  const rows = submissions.map(s => {
    const gold = internal.observations.find((o: any) => o.id === s.id).gold;
    const value = (s.answer as any)?.value;
    return { id: s.id, success: Number(Number.isSafeInteger(value) && value === gold.value) };
  });
  write('scores.json', { release: manifest.release, rows });
  manifest.status = 'complete'; manifest.results = { success: rows.filter(r => r.success).length, total: rows.length };
  write('manifest.json', manifest);
}
console.log(JSON.stringify({ mode: manifest.mode, requests: requests.length, calls: manifest.calls, out }));
