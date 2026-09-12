import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url)), study = resolve(here, '../suite/artifacts/study');
const files = ['statistics.json', 'replay.json', 'independent-audit.json', 'exact-near-duplicates.json',
  'connector-audit.json', 'strict-audit.json', 'backend-corpus-check.json', 'local-summary.json',
  'mutation-audit.json', 'render-verification.json', 'training-bundle-verification.json'];
const data = Object.fromEntries(files.map(name => [name, JSON.parse(readFileSync(resolve(study, name), 'utf8'))]));
assert.equal(data['replay.json'].reduce((n, r) => n + r.cases, 0), 730);
assert.equal(data['independent-audit.json'].differences.length, 0);
assert.equal(data['strict-audit.json'].differences.length, 0);
assert.equal(data['backend-corpus-check.json'].allTokenAndPixelDigestsMatch, true);
const tex = s => String(s).replaceAll('_', '\\_');
const write = (name, rows) => writeFileSync(resolve(here, 'tables', name + '.tex'),
  '% Generated from study evidence; do not edit.\n' + rows.join('\n') + '\n');
const tasks = [['parts', null], ['relations', 'contact'], ['relations', 'separated'],
  ['reconstruct', 'full'], ['generate', 'constraints'], ['complete', 'suffix'],
  ['edit', 'rotate'], ['edit', 'recolor'], ['edit', 'remove'],
  ['plan', 'assemble'], ['plan', 'disassemble'], ['repair', 'none'], ['repair', 'color'], ['repair', 'shift']];
write('study-main', tasks.map(([kind, variant]) => {
  const cells = ['openai/gpt-4.1-mini', 'google/gemini-2.5-flash'].map(model => {
    const rows = data['statistics.json'].groups.filter(r => {
      const [m, k, v] = r.stratum.split('|');
      return m === model && k === kind && (variant === null || v === variant);
    });
    const n = rows.reduce((n, r) => n + r.n, 0); assert.equal(n, kind === 'parts' ? 25 : 24);
    return `${rows.reduce((n, r) => n + Math.round(r.n * r.metrics.success.value), 0)}/${n}`;
  });
  return `${tex(kind + (variant ? '/' + variant : ''))} & ${cells.join(' & ')} \\\\`;
}));
write('study-controls', data['statistics.json'].paired.map(r =>
  `${tex(r.arm)} & ${r.before}/${r.n} & ${r.after}/${r.n} \\\\`));
write('study-training', data['local-summary.json'].map(r => {
  const success = Object.values(r.byTask).reduce((n, t) => n + t.successes, 0);
  return `${tex(r.condition)} & ${r.seed} & ${r.steps} & ${r.supervisedTokens.toLocaleString('en-US')} & ${success}/${r.predictions} \\\\`;
}));
writeFileSync(resolve(here, 'study-evidence.json'), JSON.stringify({
  scope: 'Completed v2 API study and completed local jobs only; small-sample exploratory evidence.',
  localJobsComplete: data['local-summary.json'].length, plannedLocalJobs: 10,
  provenance: Object.fromEntries(files.map(name => [name, {
    path: '../suite/artifacts/study/' + name,
    sha256: createHash('sha256').update(readFileSync(resolve(study, name))).digest('hex'),
  }])),
}, null, 2) + '\n');
console.log(JSON.stringify({ tables: 3, localJobsComplete: data['local-summary.json'].length }));
