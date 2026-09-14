import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { gunzipSync, gzipSync } from 'node:zlib';
import { CATALOG, type PublicTask } from '../shared';
import { digest } from '../data';
import { dims } from '../geometry';
import { DIRECTORY, sourceHashes } from '../v2/build';
import { caseSpecs, taskForV2 } from '../v2/cases';
import type { RecordV2 } from '../v2/dataset';
import { EVALUATOR_VERSION, evaluateStrict } from './strict-evaluate';

export function copyInputAnswer(task: PublicTask): unknown {
  if (!['complete', 'edit', 'repair'].includes(task.kind)) throw new Error('Copy baseline requires a current structure');
  if (!task.input.current) throw new Error('Missing public current structure');
  const structure = structuredClone(task.input.current);
  return task.kind === 'repair' ? { structure, faultIds: [] } : structure;
}

export function inventory(records: RecordV2[]) {
  assert.ok(records.length, 'Nonempty source population required');
  assert.equal(new Set(records.map(r => r.group)).size, records.length, 'Duplicate source group');
  const partTypes = Object.entries(CATALOG).map(([partId, type]) => ({
    partId, ...type, instances: 0, objects: 0, bySplit: {} as Record<string, number>,
  }));
  const rows = records.map(record => {
    const parts = record.structure.parts;
    for (const id of new Set(parts.map(p => p.partId))) {
      const entry = partTypes.find(t => t.partId === id);
      assert.ok(entry, 'Unknown catalog part');
      const n = parts.filter(p => p.partId === id).length;
      entry.instances += n; entry.objects++;
      entry.bySplit[record.split] = (entry.bySplit[record.split] ?? 0) + n;
    }
    return { id: record.id, group: record.group, policy: record.policy, split: record.split,
      pieces: parts.length, height: Math.max(...parts.map(p => p.y + dims(p).h)),
      colors: new Set(parts.map(p => p.color)).size, types: new Set(parts.map(p => p.partId)).size,
      edges: record.connections.length, difficulty: record.difficulty };
  });
  return { sourceGroups: rows.length, instances: rows.reduce((n, r) => n + r.pieces, 0),
    catalogTypes: partTypes.length, assembledTypes: partTypes.filter(t => t.instances).length,
    absentTypes: partTypes.filter(t => !t.instances).map(t => t.partId), partTypes, rows };
}

export interface ControlRow {
  caseId: string; group: string; kind: string; variant: string; condition: string; split: string; policy: string;
  metrics: Record<string, number | null>;
}
export function summarizeControls(rows: ControlRow[]) {
  assert.equal(new Set(rows.map(r => r.caseId)).size, rows.length, 'Duplicate case');
  const keys = [...new Set(rows.map(r => `${r.kind}/${r.variant}`))];
  return keys.map(key => {
    const selected = rows.filter(r => `${r.kind}/${r.variant}` === key);
    // One variant/condition per source: its mean has an unambiguous object denominator.
    assert.equal(new Set(selected.map(r => r.group)).size, selected.length, 'Repeated source within endpoint');
    const metrics = [...new Set(selected.flatMap(r => Object.keys(r.metrics)))];
    return { key, cases: selected.length, sourceGroups: selected.length,
      metrics: Object.fromEntries(metrics.map(metric => {
        const values = selected.map(r => r.metrics[metric]).filter((v): v is number => typeof v === 'number');
        assert.ok(values.every(Number.isFinite), 'Nonfinite metric');
        return [metric, { mean: values.length ? values.reduce((a, b) => a + b, 0) / values.length : null,
          denominator: values.length }];
      })) };
  });
}

export function paperAudit(verifyOnly = false) {
  const manifest = JSON.parse(readFileSync(resolve(DIRECTORY, 'manifest.json'), 'utf8'));
  assert.deepEqual(sourceHashes(), manifest.sourceHashes, 'Frozen casebank implementation changed');
  const compressed = readFileSync(resolve(DIRECTORY, 'structures.jsonl.gz'));
  assert.equal(createHash('sha256').update(compressed).digest('hex'),
    manifest.shards.find((s: { filename: string }) => s.filename === 'structures.jsonl.gz').compressedSha256);
  const records: RecordV2[] = gunzipSync(compressed).toString('utf8').trim().split('\n').map(line => JSON.parse(line));
  const coverage = inventory(records);
  assert.equal(coverage.sourceGroups, manifest.structures);
  const specs = caseSpecs();
  const taskCounts = [...new Set(specs.map(s => s.kind))].map(kind => {
    const selected = specs.filter(s => s.kind === kind);
    return { kind, cases: selected.length, groups: new Set(selected.map(s => s.group)).size,
      variants: [...new Set(selected.map(s => s.variant))],
      conditions: [...new Set(selected.map(s => s.condition))] };
  });
  assert.equal(taskCounts.reduce((n, r) => n + r.cases, 0), manifest.cases);
  const selection = specs.filter(s => s.kind === 'edit'
    || (s.kind === 'complete' || s.kind === 'repair') && s.condition === 'ordinary');
  const controls: ControlRow[] = [];
  for (const spec of selection) {
    const task = taskForV2(spec), answer = copyInputAnswer(task.public);
    controls.push({ caseId: spec.id, group: spec.group, kind: spec.kind, variant: spec.variant,
      condition: spec.condition, split: spec.split, policy: spec.policy,
      metrics: evaluateStrict(task, answer).metrics });
    if (controls.length % 5120 === 0) console.log(JSON.stringify({ copyCases: controls.length, total: selection.length }));
  }
  const summary = summarizeControls(controls);
  const output = resolve(DIRECTORY, '../study/paper-audit');
  const raw = controls.map(r => JSON.stringify(r)).join('\n') + '\n';
  const controlBytes = gzipSync(raw, { level: 9 });
  const report = { version: 'paper-audit-1', evaluator: EVALUATOR_VERSION, apiRequests: 0,
    population: 'Full released procedural casebank, including training; descriptive census, not held-out neural performance.',
    sourceHashes: { ...sourceHashes(), 'study/paper-audit.ts': digest(readFileSync(fileURLToPath(import.meta.url), 'utf8')),
      'study/strict-evaluate.ts': digest(readFileSync(resolve(DIRECTORY, '../../study/strict-evaluate.ts'), 'utf8')) },
    structuresSha256: manifest.shards.find((s: { filename: string }) => s.filename === 'structures.jsonl.gz').compressedSha256,
    controlsSha256: createHash('sha256').update(controlBytes).digest('hex'),
    selectionHash: digest(selection.map(s => s.id)), cases: manifest.cases, taskCounts, coverage,
    copyControls: { cases: controls.length, sourceGroups: records.length, summary,
      contract: 'Return public current unchanged; repair reports no fault. No target, oracle, image, retrieval or corrective operation is read by the predictor.' } };
  if (verifyOnly) {
    assert.deepEqual(controlBytes, readFileSync(resolve(output, 'copy-controls.jsonl.gz')), 'Control replay differs');
    assert.deepEqual(report, JSON.parse(readFileSync(resolve(output, 'audit.json'), 'utf8')), 'Inventory replay differs');
  } else {
    mkdirSync(output, { recursive: true });
    writeFileSync(resolve(output, 'copy-controls.jsonl.gz'), controlBytes);
    writeFileSync(resolve(output, 'audit.json'), JSON.stringify(report, null, 2) + '\n');
  }
  console.log(JSON.stringify({ objects: records.length, types: coverage.assembledTypes, cases: controls.length, summary }));
  return report;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) paperAudit(process.argv.includes('--verify'));
