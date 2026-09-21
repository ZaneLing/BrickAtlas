/** Read-only verification of frozen-v2 wire requests and authentic response semantics.
 * Synthetic receipts are accepted ONLY by an explicit test flag and remain labelled.
 */
import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { resolve, relative, sep } from 'node:path';
import { pathToFileURL } from 'node:url';
import { PNG } from 'pngjs';
import { root, hash, serializeModelRequest, SYSTEM_PROMPT } from '../ldraw-v2/publish';
import { validateAdapter, encodeImage, wireRequest, parseModelOutput } from '../ldraw-v2/adapter';
import { eligible, labelPermutation, replaceLabels, alteredGraph } from '../ldraw-v2/conditions';
import { deriveAnswer } from '../ldraw-v2/oracle';
import { score } from '../../../src/benchmark-v2/scoring';
import { replay } from '../../../src/benchmark/engine';

const version = 'ldraw2-evidence-v1';
const analysisDir = resolve(root, 'benchmark/ldraw-evidence-v1');
const read = (p: string) => JSON.parse(readFileSync(p, 'utf8'));
const canonical = (v: any): string => JSON.stringify(v && typeof v === 'object'
  ? Array.isArray(v) ? v.map(x => JSON.parse(canonical(x)))
    : Object.fromEntries(Object.keys(v).sort().filter(k => v[k] !== undefined).map(k => [k, JSON.parse(canonical(v[k]))]))
  : v);
const objectHash = (v: any) => hash(canonical(v));
const unique = (ids: string[]) => assert.equal(new Set(ids).size, ids.length, 'Duplicate ID');

export function verifyRun(directory: string, allowSynthetic = false) {
  const dir = resolve(directory), manifestPath = resolve(dir, 'manifest.json'), m = read(manifestPath);
  const fixture = m.mode === 'synthetic-validation';
  assert.ok(!fixture || (allowSynthetic && m.fixtureOnly === true), 'Synthetic receipts forbidden in real results');
  assert.ok(['offline-dry-run', 'live-inference', ...(allowSynthetic ? ['synthetic-validation'] : [])].includes(m.mode));
  assert.ok(['dry-run-complete', 'complete', 'running'].includes(m.status));
  if (m.mode !== 'offline-dry-run') assert.ok(['complete', 'running'].includes(m.status));
  assert.equal(m.release, 'brickatlas-ldraw-2');
  const lock = read(resolve(analysisDir, 'baseline-lock.json'));
  const locked = new Map<string, any>(lock.files.map((f: any) => [f.path, f]));
  const readset = new Map<string, string>();
  function checked(path: string, frozen = false) {
    const bytes = readFileSync(path), rel = relative(root, path), sha256 = hash(bytes);
    if (frozen) assert.equal(sha256, locked.get(rel)?.sha256, `Frozen file changed/absent: ${rel}`);
    readset.set(rel, sha256); return bytes;
  }
  function frozenJSON(path: string) { return JSON.parse(checked(resolve(root, path), true).toString()); }
  checked(manifestPath);
  const adapter = m.adapter;
  validateAdapter(adapter, m.mode !== 'offline-dry-run');
  assert.equal(adapter.imageEncoding, 'base64-png');
  assert.equal(adapter.imageResolution.resize, 'contain on white, never crop');
  assert.equal(adapter.systemPrompt, 'SYSTEM_PROMPT in publish.ts (validated and hashed at run time)');
  assert.equal(m.systemPromptSha256, hash(SYSTEM_PROMPT), 'Prompt mismatch');
  assert.equal(m.packageLockSha256, hash(checked(resolve(root, 'package-lock.json'), true)));
  const codeNames = ['publish.ts', 'adapter.ts', 'conditions.ts', 'score.ts', 'oracle.ts', 'run-model.ts',
    '../../../src/benchmark-v2/scoring.ts', '../../../src/benchmark/engine.ts'];
  assert.deepEqual(Object.keys(m.codeHashes).sort(), codeNames.sort());
  for (const name of codeNames) assert.equal(m.codeHashes[name],
    hash(checked(resolve(root, 'benchmark/suite/ldraw-v2', name), true)), `Code mismatch: ${name}`);
  unique(m.taskIds); unique(m.requests.map((r: any) => r.taskId)); unique(m.inputs.map((r: any) => r.file));
  assert.deepEqual(m.requests.map((r: any) => r.taskId).sort(), [...m.taskIds].sort());
  const catalog = frozenJSON('benchmark/ldraw-v2/catalog.json');
  const publicTasks = new Map<string, any>(), privateTasks = new Map<string, any>(), parts = new Map<string, any>();
  const dataset: any[] = [];
  for (const source of catalog) {
    const pubPath = `public/benchmark/ldraw-v2/inputs/${source.id}.json`;
    const intPath = `public/benchmark/ldraw-v2/models/${source.id}.json`;
    const pub = frozenJSON(pubPath), internal = frozenJSON(intPath);
    assert.equal(pub.role, 'model-input'); assert.equal(internal.role, 'internal-scoring-review');
    dataset.push({ id: source.id, source_hash: pub.sourceHash,
      input_sha256: readset.get(pubPath), internal_sha256: readset.get(intPath) });
    pub.tasks.forEach((t: any) => publicTasks.set(t.id, t));
    internal.tasks.forEach((t: any) => privateTasks.set(t.id, t));
    parts.set(source.id, internal.parts);
  }
  for (const input of m.inputs) {
    assert.ok(/^public\/benchmark\/ldraw-v2\/inputs\/[\w-]+\.json$/.test(input.file), 'Non-public input');
    assert.equal(input.sha256, readset.get(input.file), 'Dataset mismatch');
  }
  for (const id of m.taskIds) {
    const task = publicTasks.get(id);
    assert.ok(task && eligible(task, m.condition), `Unknown/ineligible task: ${id}`);
    assert.ok(m.inputs.some((r: any) => r.file === `public/benchmark/ldraw-v2/inputs/${task.modelId}.json`));
  }
  const renders = frozenJSON('benchmark/ldraw-v2/paired-renders.json');
  const renderMap = new Map<string, any>(renders.images.map((r: any) => [r.file, r]));
  const submissionFile = resolve(dir, 'submissions.json');
  const submissions = existsSync(submissionFile) ? JSON.parse(checked(submissionFile).toString()) : [];
  assert.ok(Array.isArray(submissions)); unique(submissions.map((r: any) => r.id));
  assert.ok(submissions.every((r: any) => m.taskIds.includes(r.id)), 'Unknown submission');
  const bySubmission = new Map<string, any>(submissions.map((r: any) => [r.id, r]));
  const receiptDir = resolve(dir, 'receipts');
  const receiptNames = existsSync(receiptDir) ? readdirSync(receiptDir).filter(f => f.endsWith('.json')) : [];
  assert.ok(receiptNames.every(f => m.taskIds.includes(f.slice(0, -5))), 'Unknown receipt');
  if (m.mode === 'offline-dry-run') {
    assert.equal(m.status, 'dry-run-complete'); assert.equal(m.calls, 0);
    assert.equal(submissions.length, 0); assert.equal(receiptNames.length, 0);
  } else {
    assert.ok(Number.isInteger(m.calls) && m.calls >= receiptNames.length && m.calls <= m.taskIds.length);
    if (m.status === 'complete') assert.equal(m.calls, m.taskIds.length, 'Incomplete call count');
  }
  const rows: any[] = [];
  for (const request of m.requests) {
    const task = publicTasks.get(request.taskId), internal = privateTasks.get(request.taskId);
    const requestPath = resolve(dir, request.file);
    assert.ok(requestPath.startsWith(dir + sep), 'Request outside run');
    const actual = checked(requestPath);
    assert.equal(hash(actual), request.sha256, 'Request hash mismatch');
    const images: any[] = [];
    const expected = serializeModelRequest(task, m.condition, SYSTEM_PROMPT, path => {
      const bytes = checked(resolve(root, 'public', path), true), url = encodeImage(bytes, adapter.imageResolution);
      const wireBytes = Buffer.from(url.split(',')[1], 'base64'), png = PNG.sync.read(wireBytes);
      const metadata = renderMap.get(path);
      if (metadata) {
        assert.equal(metadata.sha256, hash(bytes)); assert.equal(metadata.taskId, task.id);
        assert.equal(metadata.sourceHash, dataset.find(s => s.id === task.modelId).source_hash);
      }
      images.push({ file: path, source_sha256: hash(bytes), wire_sha256: hash(wireBytes),
        width: png.width, height: png.height, render_metadata: metadata ?? null,
        qa_status: 'unreviewed-at-exact-wire-bytes' });
      return url;
    });
    assert.equal(actual.toString(), JSON.stringify(wireRequest(expected, adapter)) + '\n',
      'Actual wire differs from declared condition/adapter/input');
    const payload = JSON.parse((expected.messages[1].content as any[])[0].text);
    const mapping = m.condition === 'id-permutation' ? labelPermutation({
      question: task.promptEn, format: task.format, input: task.input, options: task.options,
    }) : {};
    const inverse = Object.fromEntries(Object.entries(mapping).map(([a, b]) => [b, a]));
    const canonicalPayload = replaceLabels(payload, inverse);
    assert.deepEqual(canonicalPayload.options, task.options ? (m.condition === 'choice-order'
      ? [...task.options].reverse() : task.options) : undefined, 'Option semantic mapping mismatch');
    let gold = internal.answer, goldKind = 'frozen-internal-answer';
    if (m.condition === 'graph-intervention') {
      gold = deriveAnswer(alteredGraph(task), { instances: [] } as any); goldKind = 'graph-oracle-on-wire-evidence';
    }
    if (m.condition === 'wrong-image') {
      const meta = images[0]?.render_metadata, alt = meta?.mismatch?.alternateChoiceId;
      assert.ok(alt && alt !== gold.choiceId && task.options.some((o: any) => o.id === alt));
      if (task.family === 'color') {
        const donor = parts.get(task.modelId).find((p: any) => p.id === meta.mismatch.donor);
        assert.ok(donor); assert.equal(task.options.find((o: any) => o.id === alt).label, donor.color);
        assert.equal(meta.labels[donor.id], internal.references[0].label);
        assert.deepEqual(meta.renderOperands, [donor.id]);
        assert.equal(meta.mismatch.original, internal.references[0].id);
      } else {
        const oldLabel = task.options.find((o: any) => o.id === gold.choiceId).label;
        const newLabel = task.options.find((o: any) => o.id === alt).label;
        const correctInstance = internal.references.find((r: any) => r.label === oldLabel).id;
        const otherInstance = internal.references.find((r: any) => r.label === newLabel).id;
        assert.equal(meta.labels[correctInstance], newLabel); assert.equal(meta.labels[otherInstance], oldLabel);
        assert.deepEqual([...meta.mismatch.swappedLabels].sort(), [oldLabel, newLabel].sort());
      }
      gold = { choiceId: alt }; goldKind = 'paired-render-alternate-label-verified';
    }
    let answer: any = null, failure = 'missing-receipt', receiptHash: string | null = null;
    const receiptPath = resolve(receiptDir, `${task.id}.json`);
    if (existsSync(receiptPath)) {
      const receiptBytes = checked(receiptPath), r = JSON.parse(receiptBytes.toString());
      receiptHash = hash(receiptBytes);
      if (r.error !== undefined) {
        assert.equal(r.ok, false); assert.equal(r.answer, null);
        failure = /timeout|timed out|abort/i.test(r.error) ? 'timeout' : 'api-error';
      } else {
        let raw: any = null;
        try { raw = JSON.parse(r.raw); } catch { /* Invalid provider payload is retained. */ }
        if (raw?.model) assert.equal(raw.model, adapter.modelId, 'Served model revision differs from declared revision');
        assert.equal(r.ok, r.httpStatus >= 200 && r.httpStatus < 300, 'HTTP status mismatch');
        const output = adapter.transport === 'openai' ? raw?.choices?.[0]?.message?.content
          : raw?.content?.filter((c: any) => c.type === 'text').map((c: any) => c.text).join('');
        assert.equal(r.output, typeof output === 'string' ? output : null, 'Receipt output/raw mismatch');
        const parsed = r.ok && typeof output === 'string' ? parseModelOutput(output) : null;
        assert.deepEqual(r.answer, parsed, 'Receipt answer/raw mismatch');
        answer = parsed ? replaceLabels(parsed, inverse) : null;
        failure = !r.ok ? 'api-error' : raw?.choices?.[0]?.message?.refusal || raw?.stop_reason === 'refusal'
          ? 'refusal' : typeof output !== 'string' ? 'missing-output' : parsed === null ? 'invalid-json' : '';
        if (failure === 'refusal') answer = null;
      }
      const submitted = bySubmission.get(task.id);
      if (submitted) assert.deepEqual(submitted.answer, answer, 'Submission differs from raw response/mapping');
      else { failure = 'missing-submission'; answer = null; }
    } else assert.ok(!bySubmission.has(task.id), 'Submission without receipt');
    const verdict = score({ ...internal, answer: gold }, answer);
    const original = score(internal, answer);
    if (!failure && !verdict.validFormat) failure = 'invalid-format';
    if (!failure && !verdict.success) failure = 'incorrect';
    let execution = null;
    if (internal.format === 'actions') {
      const r = replay(internal, answer?.actionIds);
      execution = { issue: r.issue, final_facts: r.frames.at(-1)?.facts ?? [], success: r.success };
    }
    rows.push({ task_id: task.id, parent_task_id: task.id, source_id: task.modelId, family: task.family,
      request_sha256: request.sha256, receipt_sha256: receiptHash, answer, failure_reason: failure || null,
      payload: canonicalPayload, format: task.format, gold, original_gold: internal.answer,
      gold_source: { kind: goldKind, scoring_file: `public/benchmark/ldraw-v2/models/${task.modelId}.json`,
        scoring_sha256: readset.get(`public/benchmark/ldraw-v2/models/${task.modelId}.json`),
        renders_sha256: goldKind.includes('render') ? readset.get('benchmark/ldraw-v2/paired-renders.json') : null,
        oracle_sha256: m.codeHashes['oracle.ts'] },
      success: m.mode === 'offline-dry-run' ? null : verdict.success,
      original_gold_success: m.mode === 'offline-dry-run' ? null : original.success,
      valid_format: m.mode === 'offline-dry-run' ? null : verdict.validFormat, execution, images });
  }
  return { analysis_version: version, evidence_kind: fixture ? 'synthetic-fixture-not-benchmark' : m.mode,
    status: m.mode === 'offline-dry-run' ? 'not-run' : m.status === 'complete' ? 'complete' : 'incomplete',
    manifest: relative(root, manifestPath), manifest_sha256: hash(readFileSync(manifestPath)),
    model_revision: { model_id: adapter.modelId, api_revision: adapter.apiRevision,
      checkpoint_sha256: adapter.checkpointSha256, provider: adapter.provider },
    adapter_hash: objectHash(adapter), prompt_hash: m.systemPromptSha256,
    dataset_hash: objectHash({ release: m.release, sources: dataset }),
    condition: m.condition, task_ids: [...m.taskIds].sort(), calls: m.calls,
    code_hashes: m.codeHashes, validator_sha256: hash(readFileSync(fileURLToPath())),
    readset: [...readset].map(([file, sha256]) => ({ file, sha256 })), rows };
}
function fileURLToPath() { return resolve(root, 'benchmark/suite/ldraw-evidence/validate-run.ts'); }
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  assert.ok(process.argv[2] && process.argv[3], 'Usage: tsx validate-run.ts RUN_DIRECTORY NEW_OUTPUT_JSON');
  const out = resolve(process.argv[3]);
  assert.ok(!existsSync(out), 'Never overwrite a validation receipt');
  const result = verifyRun(process.argv[2], process.argv.includes('--synthetic-fixture'));
  writeFileSync(out, JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify({ status: result.status, tasks: result.rows.length, output: out }));
}
