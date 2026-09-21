import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { parseArgs } from 'node:util';
import { hash } from './publish';
const { values } = parseArgs({ options: {
  help: { type: 'boolean' }, manifest: { type: 'string' }, out: { type: 'string' },
}});
if (values.help || !values.manifest) {
  console.log(`Usage: tsx legacy-replay.ts --manifest authentic-v1-run.json --out NEW_DIR
Manifest: {release:"brickatlas-ldraw-1", requests:[{taskId,file,sha256,receiptFile,receiptSha256}]}.
Requires saved wire bodies and receipts; validates every hash. Produces field-stripped
request pairs only when references really appeared in the saved request.
Numerical-format changes require separate preregistration. Does not call any API.
Without a genuine manifest the historical comparison is ineligible.`);
  process.exit(0);
}
assert.ok(values.out);
const base = dirname(resolve(values.manifest));
const manifest = JSON.parse(readFileSync(resolve(values.manifest), 'utf8'));
assert.equal(manifest.release, 'brickatlas-ldraw-1');
mkdirSync(resolve(values.out)); // Refuse to overwrite an existing experiment.
function strip(value: any): any {
  if (Array.isArray(value)) return value.map(strip);
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value)
    .filter(([k]) => !['references', 'targetModule', 'capabilities', 'evidence'].includes(k))
    .map(([k, v]) => [k, strip(v)]));
  if (typeof value === 'string' && /^[{[]/.test(value.trim())) {
    try { return JSON.stringify(strip(JSON.parse(value))); } catch { return value; }
  }
  return value;
}
const rows = [];
for (const row of manifest.requests) {
  assert.ok(/^ld1-[\w-]+$/.test(row.taskId));
  const original = readFileSync(resolve(base, row.file));
  const receipt = readFileSync(resolve(base, row.receiptFile));
  assert.equal(hash(original), row.sha256); assert.equal(hash(receipt), row.receiptSha256);
  const wire = JSON.parse(original.toString());
  const serialized = JSON.stringify(wire).replaceAll('\\"', '"');
  const eligible = /"references"\s*:/.test(serialized);
  if (eligible) {
    writeFileSync(resolve(values.out, `${row.taskId}-original.json`), original);
    writeFileSync(resolve(values.out, `${row.taskId}-stripped.json`), JSON.stringify(strip(wire), null, 2) + '\n');
  }
  rows.push({ taskId: row.taskId, originalSha256: row.sha256, receiptSha256: row.receiptSha256, eligible,
    reason: eligible ? 'References observed in authentic saved body' : 'No references field in saved body' });
}
writeFileSync(resolve(values.out, 'eligibility.json'), JSON.stringify({
  status: 'audited-not-replayed', results: null, provenance: 'Caller-supplied historical manifest; hashes checked',
  interpretation: 'A future paired drop measures sensitivity, not by itself shortcut use.', rows,
}, null, 2) + '\n');
