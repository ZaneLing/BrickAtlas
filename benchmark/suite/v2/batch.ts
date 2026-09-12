import { createReadStream, createWriteStream, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createInterface } from 'node:readline';
import { once } from 'node:events';
import { finished } from 'node:stream/promises';
import { createGzip } from 'node:zlib';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { ARTIFACTS, SUITE } from '../storage';
import { caseSpecs, taskForV2, type CaseSpec } from './cases';
import { evaluate, type Evaluation } from './evaluate';
import { sourceHashes, DIRECTORY } from './build';
import { VERSION, random } from './dataset';
import { publicAlgorithm } from './baseline';

export interface Selection {
  version: string; id: string; caseIds: string[]; hash: string;
  filters: { split: string; condition: string; limitObjects?: number };
}
export function evaluationHashes() {
  return Object.fromEntries(['v2/batch.ts', 'v2/baseline.ts', 'v2/trace.ts'].map(p =>
    [p, digest(readFileSync(resolve(SUITE, p), 'utf8'))]));
}
export function selectCases(split = 'test_id', condition = 'all', limitObjects?: number): Selection {
  if (!['train', 'validation', 'test_id', 'test_ood', 'all'].includes(split)) throw new Error('Invalid split');
  if (!['default', 'ordinary', 'layers', 'symbolic', 'all'].includes(condition)) throw new Error('Invalid condition');
  if (limitObjects !== undefined && (!Number.isInteger(limitObjects) || limitObjects < 1)) throw new Error('Invalid object limit');
  let candidates = caseSpecs().filter(s => (split === 'all' || s.split === split)
    && (condition === 'all' || s.condition === condition));
  if (limitObjects !== undefined) {
    const groups = [...new Set(candidates.map(s => s.group))].sort((a, b) => digest('selection-v2:' + a).localeCompare(digest('selection-v2:' + b)));
    const keep = new Set(groups.slice(0, limitObjects)); candidates = candidates.filter(s => keep.has(s.group));
  }
  const caseIds = candidates.map(s => s.id), filters = { split, condition, limitObjects };
  const hash = digest({ version: VERSION, caseIds, filters });
  return { version: VERSION, id: 'selection-' + hash.slice(0, 16), caseIds, hash, filters };
}
export function verifySelection(s: Selection) {
  if (s.version !== VERSION || !Array.isArray(s.caseIds) || !s.caseIds.length
    || new Set(s.caseIds).size !== s.caseIds.length
    || s.hash !== digest({ version: s.version, caseIds: s.caseIds, filters: s.filters })) throw new Error('Invalid selection manifest');
  const known = new Map(caseSpecs().map(c => [c.id, c]));
  if (s.caseIds.some(id => !known.has(id))) throw new Error('Selection contains unknown case');
  const expected = selectCases(s.filters.split, s.filters.condition, s.filters.limitObjects);
  if (expected.hash !== s.hash) throw new Error('Selection does not match declared filters');
  return s.caseIds.map(id => known.get(id)!);
}
export async function readPredictions(path: string) {
  const predictions = new Map<string, unknown>();
  for await (const line of createInterface({ input: createReadStream(path), crlfDelay: Infinity })) {
    if (!line.trim()) continue;
    if (line.length > 1_000_000) throw new Error('Prediction line too large');
    const row = JSON.parse(line);
    if (!row || typeof row.caseId !== 'string' || !Object.hasOwn(row, 'answer')) throw new Error('Expected {caseId,answer}');
    if (predictions.has(row.caseId)) throw new Error('Duplicate prediction');
    predictions.set(row.caseId, row.answer);
  }
  return predictions;
}
export function clusterBootstrap(values: number[], seed = 731, samples = 1000) {
  if (!values.length) return null;
  const rng = random(seed), boot = [];
  for (let b = 0; b < samples; b++) {
    let sum = 0;
    for (let i = 0; i < values.length; i++) sum += values[Math.floor(rng() * values.length)];
    boot.push(sum / values.length);
  }
  boot.sort((a, b) => a - b);
  return { mean: values.reduce((a, b) => a + b, 0) / values.length,
    low: boot[Math.floor(samples * 0.025)], high: boot[Math.min(samples - 1, Math.ceil(samples * 0.975))],
    groups: values.length, resamples: samples, seed };
}
type Aggregate = { n: number; missing: number; sums: Record<string, number>; counts: Record<string, number>;
  clusters: Map<string, { sum: number; n: number }> };
export async function scoreBatch(selection: Selection, predictions: Map<string, unknown>,
  model: string, baseline = false) {
  const specs = verifySelection(selection), known = new Set(selection.caseIds);
  if ([...predictions.keys()].some(id => !known.has(id))) throw new Error('Unknown or out-of-selection prediction');
  const manifest = JSON.parse(readFileSync(resolve(DIRECTORY, 'manifest.json'), 'utf8'));
  if (digest(sourceHashes()) !== digest(manifest.sourceHashes)) throw new Error('Casebank source changed; rebuild and audit first');
  const id = new Date().toISOString().replace(/[:.]/g, '-') + '-v2-' + digest(model).slice(0, 8);
  const dir = resolve(ARTIFACTS, 'evaluations-v2', id);
  if (existsSync(dir)) throw new Error('Run already exists');
  mkdirSync(dir, { recursive: true });
  const stream = createGzip({ level: 6 }), output = createWriteStream(resolve(dir, 'cases.jsonl.gz'));
  stream.pipe(output);
  const done = finished(output);
  const groups = new Map<string, Aggregate>();
  const appendGroup = (key: string, spec: CaseSpec, verdict: Evaluation, missing: boolean) => {
    const g: Aggregate = groups.get(key) ?? { n: 0, missing: 0, sums: {}, counts: {}, clusters: new Map() };
    g.n++; g.missing += Number(missing);
    for (const [k, value] of Object.entries(verdict.metrics)) if (value !== null) {
      if (!Number.isFinite(value)) throw new Error('Non-finite metric');
      g.sums[k] = (g.sums[k] ?? 0) + value; g.counts[k] = (g.counts[k] ?? 0) + 1;
    }
    const c = g.clusters.get(spec.group) ?? { sum: 0, n: 0 };
    c.sum += verdict.metrics.success; c.n++; g.clusters.set(spec.group, c);
    groups.set(key, g);
  };
  try {
    for (const spec of specs) {
      const task = taskForV2(spec), missing = !baseline && !predictions.has(spec.id);
      const answer = baseline ? publicAlgorithm(task.public) : predictions.get(spec.id) ?? null;
      const verdict = evaluate(task, answer);
      for (const key of [
        `task|${spec.kind}|${spec.variant}|${spec.condition}|${spec.split}`,
        `policy|${spec.policy}|${spec.kind}|${spec.condition}|${spec.split}`,
        `difficulty|${spec.difficulty}|${spec.kind}|${spec.condition}|${spec.split}`,
      ]) appendGroup(key, spec, verdict, missing);
      const line = JSON.stringify({ spec, inputHash: digest(task.public), answer, missing, verdict }) + '\n';
      if (!stream.write(line)) await once(stream, 'drain');
    }
    stream.end(); await done;
  } catch (e) { stream.destroy(); void done.catch(() => {}); throw e; }
  const rows = [...groups].map(([stratum, g]) => ({
    stratum, n: g.n, missing: g.missing, sourceGroups: g.clusters.size,
    metrics: Object.fromEntries(Object.entries(g.sums).map(([k, sum]) => [k, { value: sum / g.counts[k], denominator: g.counts[k] }])),
    objectSuccess: clusterBootstrap([...g.clusters.values()].map(c => c.sum / c.n)),
  }));
  const report = { id, version: VERSION, model, baseline, cases: specs.length, selectionHash: selection.hash,
    rows, sourceHashes: sourceHashes(), evaluationHashes: evaluationHashes(), apiRequests: 0,
    note: 'All selected cases counted. Missing answers receive zero applicable metrics; malformed QA may retain per-field partial credit but cannot succeed. Null is only task-inapplicable. Bootstrap clusters source objects. No aggregate mixes information conditions.' };
  atomicJson(resolve(dir, 'selection.json'), selection); atomicJson(resolve(dir, 'summary.json'), report);
  return { id, cases: specs.length, strata: rows.length, baseline, apiRequests: 0 };
}
