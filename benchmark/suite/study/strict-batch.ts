import { createWriteStream, mkdirSync, readFileSync } from 'node:fs';
import { createGzip } from 'node:zlib';
import { once } from 'node:events';
import { pipeline } from 'node:stream/promises';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS, SUITE } from '../storage';
import { digest } from '../data';
import { verifySelection, clusterBootstrap, evaluationHashes, type Selection } from '../v2/batch';
import { sourceHashes, DIRECTORY } from '../v2/build';
import { taskForV2, type CaseSpec } from '../v2/cases';
import { evaluateStrict, EVALUATOR_VERSION } from './strict-evaluate';

export function strictStrata(spec: CaseSpec) {
  return [
    `task|${spec.kind}|${spec.variant}|${spec.condition}|${spec.split}`,
    `policy|${spec.policy}|${spec.kind}|${spec.condition}|${spec.split}`,
    `difficulty|${spec.difficulty}|${spec.kind}|${spec.condition}|${spec.split}`,
  ];
}
export function strictAggregator() {
  const groups = new Map<string, { n: number; missing: number; sums: Record<string, number>;
    denominators: Record<string, number>; objects: Map<string, { n: number; sum: number }> }>();
  return {
    append(spec: CaseSpec, verdict: ReturnType<typeof evaluateStrict>, missing: boolean) {
      for (const k of strictStrata(spec)) {
        if (!groups.has(k)) groups.set(k, { n: 0, missing: 0, sums: {}, denominators: {}, objects: new Map() });
        const g = groups.get(k)!; g.n++; g.missing += Number(missing);
        for (const [key, value] of Object.entries(verdict.metrics)) if (value !== null) {
          if (typeof value !== 'number' || !Number.isFinite(value)) throw new Error('Nonfinite metric');
          g.sums[key] = (g.sums[key] ?? 0) + value; g.denominators[key] = (g.denominators[key] ?? 0) + 1;
        }
        const object = g.objects.get(spec.group) ?? { n: 0, sum: 0 }; object.n++; object.sum += verdict.metrics.success;
        g.objects.set(spec.group, object);
      }
    },
    rows() {
      return [...groups].map(([stratum, g]) => ({ stratum, n: g.n, missing: g.missing, sourceGroups: g.objects.size,
        metrics: Object.fromEntries(Object.entries(g.sums).map(([k, v]) => [k, { value: v / g.denominators[k], denominator: g.denominators[k] }])),
        objectSuccess: clusterBootstrap([...g.objects.values()].map(o => o.sum / o.n)) }));
    },
  };
}
export async function strictBatch(selection: Selection, predictions: Map<string, unknown>, model: string) {
  const specs = verifySelection(selection), known = new Set(specs.map(s => s.id));
  if ([...predictions.keys()].some(id => !known.has(id))) throw new Error('Unknown prediction');
  const manifest = JSON.parse(readFileSync(resolve(DIRECTORY, 'manifest.json'), 'utf8'));
  if (digest(sourceHashes()) !== digest(manifest.sourceHashes)) throw new Error('Source drift');
  const id = new Date().toISOString().replace(/[:.]/g, '-') + '-strict-' + digest(model).slice(0, 8);
  const dir = resolve(ARTIFACTS, 'evaluations-v2', id); mkdirSync(dir);
  const gzip = createGzip(), stream = createWriteStream(resolve(dir, 'cases.jsonl.gz'));
  const done = pipeline(gzip, stream);
  void done.catch(() => {});
  const aggregate = strictAggregator();
  try {
    for (const spec of specs) {
      const task = taskForV2(spec), missing = !predictions.has(spec.id), answer = predictions.get(spec.id) ?? null;
      const verdict = evaluateStrict(task, answer);
      aggregate.append(spec, verdict, missing);
      if (!gzip.write(JSON.stringify({ spec, inputHash: digest(task.public), answer, missing, verdict }) + '\n')) await once(gzip, 'drain');
    }
    gzip.end(); await done;
  } catch (error) {
    gzip.destroy(); stream.destroy();
    await done.catch(() => {});
    throw error;
  }
  const rows = aggregate.rows();
  atomicJson(resolve(dir, 'selection.json'), selection);
  atomicJson(resolve(dir, 'summary.json'), { id, model, baseline: false, cases: specs.length, version: manifest.version,
    evaluatorVersion: EVALUATOR_VERSION, strictSourceHashes: strictSourceHashes(), evaluationHashes: evaluationHashes(),
    sourceHashes: sourceHashes(), rows, selectionHash: selection.hash, apiRequests: 0,
    note: 'Strict primitive-type input validation; original submissions retained. Historical v2 metrics are not rewritten.' });
  return { id, cases: specs.length, evaluatorVersion: EVALUATOR_VERSION };
}
export function strictSourceHashes() {
  return Object.fromEntries(['strict-evaluate.ts', 'strict-batch.ts', 'strict-trace.ts', 'strict-replay.ts'].map(file =>
    [file, digest(readFileSync(resolve(SUITE, 'study', file), 'utf8'))]));
}
