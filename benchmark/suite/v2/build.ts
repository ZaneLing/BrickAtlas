import { createWriteStream, existsSync, mkdirSync, readFileSync, renameSync, rmSync } from 'node:fs';
import { resolve } from 'node:path';
import { createGzip } from 'node:zlib';
import { once } from 'node:events';
import { finished } from 'node:stream/promises';
import { createHash } from 'node:crypto';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS, SUITE } from '../storage';
import { digest } from '../data';
import { dataset, POLICIES, VERSION } from './dataset';
import { caseSpecs, taskForV2 } from './cases';
import { groundTruth } from './ground-truth';
import { evaluate } from './evaluate';

export const DIRECTORY = resolve(ARTIFACTS, 'casebank-v2');
export function sourceHashes() {
  return Object.fromEntries(['v2/dataset.ts', 'v2/cases.ts', 'v2/evaluate.ts', 'v2/ground-truth.ts', 'v2/build.ts',
    'geometry.ts', 'data.ts', 'shared.ts', 'research/dataset.ts', 'research/independent-check.ts', 'research/tasks.ts',
    'tasks.ts', 'score.ts'].map(p => [p, digest(readFileSync(resolve(SUITE, p), 'utf8'))]));
}
export async function buildCasebank() {
  mkdirSync(DIRECTORY, { recursive: true });
  const temporary = resolve(DIRECTORY, '.building');
  if (existsSync(temporary)) throw new Error('Incomplete build exists; inspect .building before removing it');
  mkdirSync(temporary);
  const streams = new Map<string, { gzip: ReturnType<typeof createGzip>; done: Promise<void>;
    hash: ReturnType<typeof createHash>; count: number }>();
  const append = async (name: string, value: unknown) => {
    let stream = streams.get(name);
    if (!stream) {
      const gzip = createGzip({ level: 6 }), output = createWriteStream(resolve(temporary, name + '.jsonl.gz'));
      gzip.pipe(output); stream = { gzip, done: finished(output), hash: createHash('sha256'), count: 0 }; streams.set(name, stream);
    }
    const line = JSON.stringify(value) + '\n'; stream.hash.update(line); stream.count++;
    if (!stream.gzip.write(line)) await once(stream.gzip, 'drain');
  };
  const specs = caseSpecs(), records = dataset(), metrics = new Map<string, { n: number; oracle: number; empty: number; copy: number }>();
  const failures: string[] = [];
  try {
    for (const m of records) await append('structures', m);
    for (const [i, spec] of specs.entries()) {
      const t = taskForV2(spec), gt = groundTruth(t);
      const empty = evaluate(t, null), copy = evaluate(t, spec.kind === 'repair'
        ? { structure: t.source ?? { version: 1, parts: [] }, faultIds: [] }
        : t.source ?? t.public.input.structure ?? { version: 1, parts: [] });
      if (gt.oracleEvaluation.metrics.success !== 1 || empty.metrics.success !== 0) failures.push(spec.id);
      const k = [spec.kind, spec.variant, spec.condition, spec.split].join('|');
      const row = metrics.get(k) ?? { n: 0, oracle: 0, empty: 0, copy: 0 };
      row.n++; row.oracle += gt.oracleEvaluation.metrics.success; row.empty += empty.metrics.success; row.copy += copy.metrics.success; metrics.set(k, row);
      await append(`inputs-${spec.split}`, { caseId: spec.id, input: t.public });
      await append(`ground-truth-${spec.split}`, gt);
      await append(`render-private-${spec.split}`, { caseId: spec.id, frames: t.frames });
      await append('case-index', { ...spec, inputHash: gt.inputHash, groundTruthHash: digest(gt), frames: t.frames.length });
      if ((i + 1) % 5000 === 0) console.log(JSON.stringify({ built: i + 1, total: specs.length }));
    }
    if (failures.length) throw new Error(`${failures.length} oracle/empty audit failures: ${failures.slice(0, 10)}`);
    for (const s of streams.values()) s.gzip.end();
    for (const s of streams.values()) await s.done;
    const shards = [...streams].map(([name, stream]) => {
      const filename = name + '.jsonl.gz', compressed = readFileSync(resolve(temporary, filename));
      return { filename, rows: stream.count, jsonlSha256: stream.hash.digest('hex'),
        compressedSha256: createHash('sha256').update(compressed).digest('hex'), bytes: compressed.length };
    });
    const manifest = { version: VERSION, structures: records.length, geometricGroups: new Set(records.map(m => m.group)).size,
      catalogQuestions: specs.filter(s => s.kind === 'parts').length, cases: specs.length,
      splits: Object.fromEntries(['train', 'validation', 'test_id', 'test_ood'].map(split => [split, {
        structures: records.filter(m => m.split === split).length, cases: specs.filter(s => s.split === split).length }])),
      policies: POLICIES.map(policy => ({ policy, n: records.filter(m => m.policy === policy).length,
        splits: [...new Set(records.filter(m => m.policy === policy).map(m => m.split))] })),
      difficulty: Object.fromEntries(['small', 'medium', 'large'].map(d => [d, records.filter(m => m.difficulty === d).length])),
      parts: { min: Math.min(...records.map(m => m.structure.parts.length)), max: Math.max(...records.map(m => m.structure.parts.length)) },
      sourceHashes: sourceHashes(), datasetHash: digest(records), caseSpecHash: digest(specs), shards,
      audit: { everyCaseOraclePassed: true, everyCaseEmptyFailed: true, independentGeometryChecks: specs.length,
        annotationOrigin: 'procedural', realHumanReviews: 0, excludesExactGeometriesFromOldReleases: true },
      limitations: ['Public procedural casebank; not a private test or independent human-designed dataset.',
        'Policy-disjoint bridge/shell generation is not a proof of disjoint semantic support or absence of near duplicates.',
        'Catalog identification uses known types; colors share a catalog group and are not independent unseen parts.',
        'Ground-truth and private render recipes are evaluator-only and MUST NOT be fed to visual models.'] };
    for (const shard of shards) renameSync(resolve(temporary, shard.filename), resolve(DIRECTORY, shard.filename));
    atomicJson(resolve(DIRECTORY, 'baseline-audit.json'), [...metrics].map(([stratum, row]) => ({ stratum, ...row })));
    atomicJson(resolve(DIRECTORY, 'manifest.json'), manifest);
    rmSync(temporary, { recursive: true });
    return manifest;
  } catch (error) {
    for (const s of streams.values()) { s.gzip.destroy(); void s.done.catch(() => {}); }
    throw error;
  }
}
