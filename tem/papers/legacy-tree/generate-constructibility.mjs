import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const read = path => JSON.parse(readFileSync(resolve(here, path), 'utf8'));
const sha = path => createHash('sha256').update(readFileSync(resolve(here, path))).digest('hex');
const audit = read('../constructibility-v1/audit.json');
const algorithms = read('../constructibility-v1/algorithm-results.json');
assert.equal(audit.version, 'brickatlas-constructibility-1');
assert.equal(audit.records, 78);
assert.equal(algorithms.length, 78);
assert.ok(algorithms.every(row => row.result.success === 1));

const labels = {
  'sequence-audit': 'Sequence audit',
  'blocked-recovery': 'Blocked recovery',
  'stockout-replan': 'Stockout replan',
  'clarify-or-commit': 'Clarify / commit',
};
const shortcut = {
  'sequence-audit': audit.shortcuts.sequenceAlwaysValid,
  'blocked-recovery': audit.shortcuts.recoveryNoOperation,
  'stockout-replan': audit.shortcuts.stockoutUseUnavailable,
  'clarify-or-commit': audit.shortcuts.clarificationAlwaysCommitH0,
};
const rows = Object.entries(audit.byKind).map(([kind, count]) =>
  `${labels[kind]} & ${count} & ${count} & ${shortcut[kind]} \\\\`).join('\n') + '\n';
writeFileSync(resolve(here, 'tables/constructibility-v1.tex'), rows);
writeFileSync(resolve(here, 'constructibility-evidence.json'), JSON.stringify({
  version: audit.version,
  sourceGroups: audit.sourceGroups,
  records: audit.records,
  byKind: audit.byKind,
  shortcuts: audit.shortcuts,
  publicSha256: sha('../constructibility-v1/public.json'),
  auditSha256: sha('../constructibility-v1/audit.json'),
  protocolSha256: sha('../constructibility-v1/frozen-protocol.json'),
  algorithmResultsSha256: sha('../constructibility-v1/algorithm-results.json'),
  generatorSha256: sha('generate-constructibility.mjs'),
}, null, 2) + '\n');
console.log(JSON.stringify({ version: audit.version, records: audit.records, tableRows: 4 }));
