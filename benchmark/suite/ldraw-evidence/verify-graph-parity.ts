import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { alteredGraph } from '../ldraw-v2/conditions';
import type { PublicTask } from '../ldraw-v2/types';

if (process.argv.includes('--help')) {
  console.log('Usage: tsx verify-graph-parity.ts\nRead-only comparison of the new independent audit against frozen v2 graph interventions.');
  process.exit(0);
}
const root = resolve(import.meta.dirname, '../../..');
const data = resolve(root, 'benchmark/ldraw-evidence-v1');
const audit = JSON.parse(readFileSync(resolve(data, 'node-prior-audit.json'), 'utf8'));
const catalog = JSON.parse(readFileSync(resolve(root, 'benchmark/ldraw-v2/catalog.json'), 'utf8'));
const tasks: PublicTask[] = catalog.flatMap((m: any) =>
  JSON.parse(readFileSync(resolve(root, 'public/benchmark/ldraw-v2/inputs', m.id + '.json'), 'utf8')).tasks);
for (const row of audit.rows) {
  const task = tasks.find(t => t.id === row.task_id)!;
  const changed = alteredGraph(task);
  assert.deepEqual(changed.input.edges, row.intervention.edges);
  assert.deepEqual(changed.input.nodes, task.input.nodes);
}
const report = { status: 'passed', exactExistingInterventionMatches: audit.rows.length,
  scope: 'Independent Python intervention and frozen TypeScript generation agree; not model inference.' };
writeFileSync(resolve(data, 'graph-parity-verification.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report));
