import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const release = resolve(here, '../mechanism-v1');
const read = path => JSON.parse(readFileSync(path, 'utf8'));
const sha = path => createHash('sha256').update(readFileSync(path)).digest('hex');
const models = read(resolve(release, 'models.json'));
const audit = read(resolve(release, 'audit.json'));
const local = read(resolve(release, 'results/local-qwen3-0.6b.scores.json'));
const latest = read(resolve(release, 'results/latest.json'));
const api = read(resolve(release, 'results', latest.path));
assert.equal(audit.originalDesigns, 6);
assert.equal(audit.tasks, 48);
assert.equal(api.status, 'complete');

const labels = {
  'prefix-dynamics': 'Prefix',
  'insertion-access': 'Access',
  'fault-recovery': 'Repair',
  'inventory-substitution': 'Stock',
  'dynamic-robustness': 'Dynamics',
  'functional-kinematics': 'Function',
  'active-inspection': 'Inspect',
  'multiobjective-design': 'Pareto',
};
const kinds = Object.keys(labels);
const modelRows = [
  { id: 'local', label: 'Qwen3-0.6B (text)', rows: local.rows.map(row => ({
    kind: row.kind, success: row.result.success,
  })) },
  ...['openai/gpt-4.1-mini', 'google/gemini-2.5-flash'].map(id => ({
    id, label: id.startsWith('openai') ? 'GPT-4.1 mini' : 'Gemini 2.5 Flash',
    rows: api.results.filter(row => row.model === id).map(row => ({ kind: row.kind, success: row.verdict.success })),
  })),
];
const table = modelRows.map(model => {
  const scores = kinds.map(kind => `${model.rows.filter(row => row.kind === kind && row.success).length}/6`);
  return `${model.label} & ${scores.join(' & ')} \\\\`;
}).join('\n') + '\n';
writeFileSync(resolve(here, 'tables/mechanism-results.tex'), table);
writeFileSync(resolve(here, 'tables/mechanism-models.tex'), models.map(model =>
  `${model.name} & ${model.parts.length} & ${model.modules.length} & ${model.joints.length} \\\\`
).join('\n') + '\n');

const evidence = {
  version: audit.version,
  models: models.length,
  tasks: audit.tasks,
  byKind: audit.byKind,
  physicsEngine: audit.physicsEngine,
  apiRun: {
    id: api.id,
    requests: api.results.length,
    cost: api.campaignAfter - api.campaignBefore,
    campaignAfter: api.campaignAfter,
  },
  modelTotals: Object.fromEntries(modelRows.map(model =>
    [model.label, model.rows.reduce((sum, row) => sum + row.success, 0)])),
  hashes: {
    audit: sha(resolve(release, 'audit.json')),
    models: sha(resolve(release, 'models.json')),
    public: sha(resolve(release, 'public.json')),
    localScores: sha(resolve(release, 'results/local-qwen3-0.6b.scores.json')),
    apiRun: sha(resolve(release, 'results', latest.path)),
    modelFigure: sha(resolve(here, 'figures/mechanism-models.pdf')),
    taskFigure: sha(resolve(here, 'figures/mechanism-tasks.pdf')),
    generator: sha(fileURLToPath(import.meta.url)),
  },
};
writeFileSync(resolve(here, 'mechanism-evidence.json'), JSON.stringify(evidence, null, 2) + '\n');
console.log(JSON.stringify(evidence));
