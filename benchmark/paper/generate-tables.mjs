import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url)), artifacts = resolve(here, '../suite/artifacts');
const paths = {
  manifest: 'casebank-v2/manifest.json',
  quality: 'casebank-v2/quality-audit.json',
  baseline: 'evaluations-v2/2026-09-12T09-24-23-743Z-v2-b187752b/summary.json',
  verification: 'casebank-v2/verification.json',
  replay: 'casebank-v2/replay-evaluations.json',
  clean: 'casebank-v2/clean-verification.json',
  engineering: 'casebank-v2/engineering-verification.json',
  pilot: 'research/statistics.json',
};
const data = Object.fromEntries(Object.entries(paths).map(([k, p]) => [k, JSON.parse(readFileSync(resolve(artifacts, p), 'utf8'))]));
assert.equal(data.manifest.cases, 117910);
assert.equal(data.manifest.structures, 5120);
assert.equal(data.verification.groundTruthsRegenerated, data.manifest.cases);
assert.equal(data.replay.runs[0].cases, data.manifest.cases);
assert.equal(data.clean.fullCasebankVerified, true);
assert.ok(data.engineering.checks.every(c => c.passed));
assert.equal(data.baseline.baseline, true);
const tex = value => String(value).replaceAll('_', '\\_').replaceAll('%', '\\%');
const num = n => n.toLocaleString('en-US');
mkdirSync(resolve(here, 'tables'), { recursive: true });
const write = (name, rows) => writeFileSync(resolve(here, 'tables', name + '.tex'), '% Generated from committed evidence; do not edit.\n' + rows.join('\n') + '\n');
write('splits', Object.entries(data.manifest.splits).map(([k, s]) => `${tex(k)} & ${num(s.structures)} & ${num(s.cases)} \\\\`));
const planning = [];
for (const p of data.quality.policyRows) {
  const rows = data.baseline.rows.filter(r => r.stratum.startsWith(`policy|${p.policy}|plan|`));
  // Policy-level plan aggregates mix assemble/disassemble; use task cases below for exact direction.
  assert.ok(rows.length);
}
// Exact direction-by-policy totals are reconstructed from per-case records separately;
// the paper's direction table uses task strata, never the mixed policy aggregates.
for (const direction of ['assemble', 'disassemble']) {
  for (const split of ['train', 'validation', 'test_id', 'test_ood']) {
    const row = data.baseline.rows.find(r => r.stratum === `task|plan|${direction}|default|${split}`);
    planning.push(`${direction} & ${tex(split)} & ${num(row.n)} & ${num(Math.round(row.n * row.metrics.success.value))} & ${(row.metrics.success.value * 100).toFixed(1)} \\\\`);
  }
}
write('planning', planning);
write('policy', data.quality.policyRows.map(r => `${tex(r.policy)} & ${r.objects} & ${r.mean.pieces.toFixed(1)} & ${r.mean.height.toFixed(1)} & ${r.mean.multiSupported.toFixed(2)} \\\\`));
write('pilot', ['reconstruct', 'complete', 'repair'].flatMap(kind =>
  ['openai/gpt-4.1-mini', 'google/gemini-2.5-flash'].map(model => {
    const values = ['ordinary', 'layers', 'symbolic'].map(condition => {
      const r = data.pilot.taskRows.find(r => r.kind === kind && r.model === model && r.condition === condition);
      return `${Math.round(r.metrics.success * r.n)}/${r.n}`;
    });
    return `${kind} & ${model.startsWith('openai') ? 'GPT-4.1 mini' : 'Gemini Flash'} & ${values.join(' & ')} \\\\`;
  })));
const training = data.pilot.localTraining.rows;
write('training', ['base', 'single', 'multi'].flatMap(condition => training.filter(r => r.condition === condition).map(r =>
  `${condition} & ${r.seed} & ${r.steps} & ${num(r.processedTokens)} & ${r.successes}/${r.cases} \\\\`)));
const provenance = Object.fromEntries(Object.entries(paths).map(([name, path]) => [name, {
  path: '../suite/artifacts/' + path, sha256: createHash('sha256').update(readFileSync(resolve(artifacts, path))).digest('hex'),
}]));
writeFileSync(resolve(here, 'evidence.json'), JSON.stringify({
  provenance, scope: 'V2 full deterministic baseline; neural results from older releases only.',
  template: { source: 'https://github.com/cvpr-org/author-kit', revision: '291758547e923160eb4d37079b7b9f0dfce82355',
    files: Object.fromEntries(['cvpr.sty', 'ieeenat_fullname.bst'].map(p => [p, createHash('sha256').update(readFileSync(resolve(here, p))).digest('hex')])) },
}, null, 2) + '\n');
console.log(JSON.stringify({ tables: 5, verifiedCaseCount: data.manifest.cases, evidence: 'paper/evidence.json' }));
