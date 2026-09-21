import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { createServer } from 'node:http';
import { PNG } from 'pngjs';
import { root, data, site, hash, loadPublicBundle, serializeModelRequest, assertNoPrivateFields } from './publish';
import { conditions, eligible, alteredGraph, labelPermutation, replaceLabels } from './conditions';
import { deriveAnswer } from './oracle';
import { validateAdapter, wireRequest, parseModelOutput, sendRequest, type Adapter } from './adapter';
import type { AtlasManifest } from '../../../src/model/types';
if (process.argv.includes('--help')) {
  console.log('Usage: tsx verify-experiments.ts\nCheck every condition, paired render, exact dry-run body and local mock transport. No model API calls.');
  process.exit(0);
}
const read = (path: string) => JSON.parse(readFileSync(path, 'utf8'));
const tasks = readdirSync(resolve(site, 'inputs')).filter(f => f.endsWith('.json'))
  .flatMap(f => loadPublicBundle(resolve(site, 'inputs', f)).tasks);
const plan = read(resolve(root, 'benchmark/paper/ldraw-v2-experiments.json'));
const renders = read(resolve(data, 'paired-renders.json'));
const dry = read(resolve(data, 'dry-runs/gpt41-standard/manifest.json'));
assert.equal(dry.status, 'dry-run-complete'); assert.equal(dry.calls, 0); assert.equal(dry.results, null);
assert.equal(renders.images.length, 907);
assert.equal(new Set(renders.images.map((r: any) => `${r.taskId}/${r.mode}`)).size, 907);
let requests = 0, graphChanges = 0, labelRoundTrips = 0;
const examples: any[] = [];
for (const condition of conditions) {
  const actual = tasks.filter(t => eligible(t, condition));
  const prereg = plan.conditions.find((c: any) => c.id === condition);
  assert.equal(actual.length, prereg.n);
  assert.deepEqual(actual.map(t => t.id).sort(), prereg.taskIds);
  for (const task of actual) {
    const request = serializeModelRequest(task, condition);
    assertNoPrivateFields(request);
    const content = request.messages[1].content;
    assert.ok(Array.isArray(content));
    const payload = JSON.parse((content[0] as { text: string }).text);
    assertNoPrivateFields(payload);
    assert.ok(!('references' in payload));
    const images = content.filter(c => c.type === 'image_url');
    assert.equal(images.length, task.modality === 'visual' && condition !== 'text-without-image'
      ? condition === 'multi-view' ? 2 : 1 : 0);
    for (const image of images) {
      const bytes = readFileSync(resolve(root, 'public', image.image_url.url));
      const png = PNG.sync.read(bytes);
      assert.ok(png.width > 0 && png.height > 0);
    }
    if (condition === 'graph-intervention') {
      const emptyManifest = { instances: [] } as unknown as AtlasManifest;
      const a = deriveAnswer(task, emptyManifest), b = deriveAnswer(alteredGraph(task), emptyManifest);
      assert.notDeepEqual(a, b, `Intervention did not change answer: ${task.id}`);
      graphChanges++;
    }
    if (condition === 'id-permutation') {
      const original = JSON.parse((serializeModelRequest(task).messages[1].content as any)[0].text);
      const map = labelPermutation(original), inverse = Object.fromEntries(Object.entries(map).map(([a, b]) => [b, a]));
      assert.deepEqual(replaceLabels(payload, inverse), original); labelRoundTrips++;
      if (task.modality === 'visual') {
        const render = renders.images.find((r: any) => r.taskId === task.id && r.mode === 'id');
        assert.deepEqual(Object.values(render.labels).sort(), Object.values(map).sort());
      }
    }
    if (actual[0].id === task.id) examples.push({ taskId: task.id, condition, request });
    requests++;
  }
}
for (const row of renders.images) {
  assert.equal(hash(readFileSync(resolve(root, 'public', row.file))), row.sha256);
  assert.equal(row.sourcePosesPreserved, true);
  assert.ok(Object.keys(row.labels).length <= 12);
  if (row.mode === 'mask') {
    const full = renders.images.find((r: any) => r.taskId === row.taskId && r.mode === 'full');
    assert.deepEqual(full.camera, row.camera); assert.deepEqual(full.projections, row.projections);
  }
  if (row.mode === 'wrong') {
    const internal = read(resolve(site, 'models', `${row.modelId}.json`)).tasks.find((t: any) => t.id === row.taskId);
    assert.notEqual(row.mismatch.alternateChoiceId, internal.answer.choiceId);
  }
}
for (const row of dry.requests) {
  const bytes = readFileSync(resolve(data, 'dry-runs/gpt41-standard', row.file));
  assert.equal(hash(bytes), row.sha256);
  const wire = JSON.parse(bytes.toString()); assertNoPrivateFields(wire);
  for (const block of wire.messages[1].content) if (block.type === 'image_url') {
    const png = PNG.sync.read(Buffer.from(block.image_url.url.split(',')[1], 'base64'));
    assert.equal(png.width, 1280); assert.equal(png.height, 800);
  }
}
const adapterDir = resolve(import.meta.dirname, 'model-adapters');
for (const file of readdirSync(adapterDir).filter(f => f.endsWith('.json')))
  validateAdapter(read(resolve(adapterDir, file)));
assert.equal(parseModelOutput('```json\n{"choiceId":"A"}\n```'), null);
assert.equal(parseModelOutput('Answer: {"choiceId":"A"}'), null);
assert.equal(parseModelOutput('[]'), null);
assert.deepEqual(parseModelOutput('{"value":4}'), { value: 4 });
// Exercise actual serialization/receipt handling against a local fixture only.
let received = '';
const server = createServer((req, res) => {
  req.setEncoding('utf8'); let raw = '';
  req.on('data', chunk => { raw += chunk; });
  req.on('end', () => {
    received = raw;
    const body = JSON.parse(raw), anthropic = !!body.system;
    res.writeHead(200, { 'content-type': 'application/json', 'request-id': 'local-test-only' });
    res.end(JSON.stringify(anthropic ? { content: [{ type: 'text', text: '{"choiceId":"A"}' }], usage: { input_tokens: 3, output_tokens: 2 } }
      : { choices: [{ message: { content: '{"choiceId":"A"}' } }], usage: { prompt_tokens: 3, completion_tokens: 2 } }));
  });
});
await new Promise<void>(ready => server.listen(0, '127.0.0.1', ready));
try {
  const address = server.address() as { port: number };
  for (const transport of ['openai', 'anthropic'] as const) {
    const adapter: Adapter = { ...read(resolve(adapterDir, 'gpt41.json')), transport,
      endpoint: `http://127.0.0.1:${address.port}`, apiKeyEnv: 'LDRAW_V2_TEST_CREDENTIAL' };
    process.env.LDRAW_V2_TEST_CREDENTIAL = 'nonsecret-fixture';
    const request = serializeModelRequest(tasks.find(t => t.modality !== 'visual')!);
    const body = JSON.stringify(wireRequest(request, adapter)) + '\n';
    const receipt = await sendRequest(body, adapter);
    assert.equal(received, body); assert.deepEqual(receipt.answer, { choiceId: 'A' });
    assert.equal(receipt.usd, null); assert.equal(receipt.requestId, 'local-test-only');
  }
} finally { delete process.env.LDRAW_V2_TEST_CREDENTIAL; server.close(); }
const result = { status: 'passed', conditionRequests: requests, graphChangedAnswers: graphChanges,
  labelPermutationRoundTrips: labelRoundTrips, pairedImages: renders.images.length,
  realWireDryRunSnapshots: dry.requests.length, adapters: 6, localTransportFixtures: 2,
  modelApiCalls: 0, humanReview: 'pending' };
writeFileSync(resolve(data, 'phase-4-checks.json'), JSON.stringify(result, null, 2) + '\n');
writeFileSync(resolve(data, 'condition-request-examples.json'), JSON.stringify(examples, null, 2) + '\n');
console.log(JSON.stringify(result, null, 2));
