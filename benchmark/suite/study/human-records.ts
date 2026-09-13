import assert from 'node:assert/strict';
import { closeSync, existsSync, mkdirSync, openSync, readFileSync, readdirSync, unlinkSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import type { AuditLabel } from './human-audit';
import type { Adjudication } from './human-calibration';

export type AuditRecordKind = 'labels' | 'adjudications';
export interface AuditRecords { labels: AuditLabel[]; adjudications: Adjudication[]; batches: string[] }

function parseRows(raw: string): unknown[] {
  const rows: unknown[] = [];
  for (const [index, line] of raw.split(/\r?\n/).entries()) {
    const content = index === 0 ? line.replace(/^\uFEFF/, '') : line;
    if (!content.trim()) continue;
    try { rows.push(JSON.parse(content)); }
    catch { throw new Error(`Invalid JSON in review input at line ${index + 1}`); }
  }
  return rows;
}

export function readAuditRecords(directory: string): AuditRecords {
  const result: AuditRecords = { labels: [], adjudications: [], batches: [] };
  const legacy = resolve(directory, 'labels.jsonl');
  if (existsSync(legacy)) {
    const raw = readFileSync(legacy, 'utf8');
    result.labels.push(...parseRows(raw) as AuditLabel[]);
    result.batches.push(`legacy:${digest(raw)}`);
  }
  const batches = resolve(directory, 'batches');
  if (existsSync(batches)) for (const filename of readdirSync(batches).sort()) {
    if (!filename.endsWith('.json')) continue;
    assert.match(filename, /^[a-f0-9]{64}\.json$/, 'Invalid review batch filename');
    const batch = JSON.parse(readFileSync(resolve(batches, filename), 'utf8'));
    assert.equal(batch.version, 'human-review-batch-1');
    assert.ok(batch.kind === 'labels' || batch.kind === 'adjudications');
    assert.equal(typeof batch.raw, 'string');
    assert.equal(digest({ kind: batch.kind, raw: batch.raw }), filename.slice(0, -5), 'Review batch integrity mismatch');
    const rows = parseRows(batch.raw);
    assert.ok(rows.length > 0, 'Empty review batch');
    if (batch.kind === 'labels') result.labels.push(...rows as AuditLabel[]);
    else result.adjudications.push(...rows as Adjudication[]);
    result.batches.push(filename.slice(0, -5));
  }
  return result;
}

export function importAuditRecords(directory: string, kind: AuditRecordKind, raw: string,
  validate: (records: AuditRecords) => void) {
  assert.ok(kind === 'labels' || kind === 'adjudications');
  const rows = parseRows(raw); assert.ok(rows.length > 0, 'Empty review batch');
  mkdirSync(directory, { recursive: true, mode: 0o700 });
  const lock = resolve(directory, 'import.lock'), fd = openSync(lock, 'wx', 0o600);
  closeSync(fd);
  try {
    const current = readAuditRecords(directory);
    validate(current);
    const hash = digest({ kind, raw }), file = resolve(directory, 'batches', `${hash}.json`);
    if (existsSync(file)) return { batchHash: hash, records: rows.length, imported: false };
    const next: AuditRecords = { labels: [...current.labels], adjudications: [...current.adjudications], batches: [...current.batches, hash] };
    if (kind === 'labels') next.labels.push(...rows as AuditLabel[]);
    else next.adjudications.push(...rows as Adjudication[]);
    validate(next);
    // Only fully validated batches become visible; originals are never edited or concatenated in place.
    atomicJson(file, { version: 'human-review-batch-1', kind, raw });
    return { batchHash: hash, records: rows.length, imported: true };
  } finally { unlinkSync(lock); }
}
