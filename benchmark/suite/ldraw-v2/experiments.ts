import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { root, data, site, loadPublicBundle } from './publish';
import { conditions, eligible } from './conditions';
if (process.argv.includes('--help')) {
  console.log('Usage: tsx experiments.ts\nRegenerate the proposed v2 experiment plan. Does not call APIs or overwrite adapter configs.');
  process.exit(0);
}
const tasks = readdirSync(resolve(site, 'inputs')).filter(f => f.endsWith('.json'))
  .flatMap(f => loadPublicBundle(resolve(site, 'inputs', f)).tasks);
const names: Record<string, string> = {
  standard: 'Frozen operand-isolation image / structured public input',
  'text-without-image': 'Question and options without image',
  'full-scene': 'Full original assembly with operand labels',
  'background-mask': 'Only operands visible; same full-scene camera',
  'operand-only': 'Only operands visible; camera refitted to operands',
  'wrong-image': 'Semantically mismatched image with the same operand labels',
  'graph-edges-withheld': 'Edge list withheld (interface records excluded)',
  'graph-intervention': 'One logical edge removal/addition changes the answer',
  'choice-order': 'Reverse option presentation; retain anonymous option IDs',
  'edge-order': 'Reverse equivalent edge serialization',
  'id-permutation': 'Bijective B-number renaming in text and pixels',
  'camera-perturbation': 'Fixed alternative camera with original operand identities',
  'color-nuisance': 'Desaturated operand image; type only',
  'multi-view': 'Two fixed views (not adaptive tool interaction)',
};
const pairs = [
  ['visual-information', 'standard', 'text-without-image'],
  ['visual-mismatch', 'operand-only', 'wrong-image'],
  ['background-only', 'full-scene', 'background-mask'],
  ['crop-access', 'full-scene', 'operand-only'],
  ['large-scene-versus-text', 'full-scene', 'text-without-image'],
  ['edge-information', 'standard', 'graph-edges-withheld'],
  ['edge-causal-control', 'standard', 'graph-intervention'],
  ['label-binding', 'operand-only', 'id-permutation'],
  ['label-binding-structured', 'standard', 'id-permutation'],
  ['choice-position', 'standard', 'choice-order'],
  ['edge-equivalence', 'standard', 'edge-order'],
  ['camera', 'operand-only', 'camera-perturbation'],
  ['color-nuisance', 'operand-only', 'color-nuisance'],
  ['view-access', 'operand-only', 'multi-view'],
];
const old = JSON.parse(readFileSync(resolve(root, 'benchmark/paper/ldraw-experiments.json'), 'utf8'));
const plan = {
  version: 'ldraw-2-experiment-plan-v1', release: 'brickatlas-ldraw-2', status: 'proposed-not-run',
  crossModule: 'Not measured; Phase 3 skipped. No score-product or integration-residual analysis.',
  missingPolicy: 'Unrun numeric results remain null and blank in tables.',
  primaryEstimand: 'Per-family paired accuracy difference A minus B; source-macro primary, item-micro secondary.',
  bootstrap: { resamples: 10000, seed: 20260918, cluster: 'source assembly', interval: 'percentile 95%' },
  equivalence: { margin: null, status: 'Not preregistered; no equivalence claim allowed.' },
  algorithmicControls: [
    { id: 'public-action-solver', n: 75, scope: 'actions', evidence: 'benchmark/ldraw-v2/verification.json',
      role: 'Executable contract ceiling; not model inference or mechanical planning.' },
    { id: 'semantic-majority', scope: 'each family', evidence: 'benchmark/ldraw-v2/descriptive-analysis/analysis.json',
      role: 'In-corpus answer prior; not held-out generalization.' },
  ],
  conditions: conditions.map(id => ({ id, description: names[id],
    taskIds: tasks.filter(t => eligible(t, id)).map(t => t.id).sort(),
    n: tasks.filter(t => eligible(t, id)).length, result: null })),
  pairedComparisons: pairs.map(([id, a, b]) => ({ id, a, b,
    taskIds: tasks.filter(t => eligible(t, a as any) && eligible(t, b as any) &&
      (id !== 'label-binding-structured' || t.modality !== 'visual')).map(t => t.id).sort(),
    scoring: b === 'graph-intervention' ? 'Recompute the answer from the intervened public graph; report response adaptation.' : 'Original semantic answer',
    results: { deltaMacro: null, deltaMicro: null, ci95: null, correctToWrong: null, wrongToCorrect: null } })),
  tables: old.tables.map((table: any) => table.id === 'ablations' || table.id === 'robustness'
    ? { ...table, rows: conditions.filter(c => (table.id === 'robustness') ===
      ['choice-order', 'edge-order', 'id-permutation', 'camera-perturbation', 'color-nuisance', 'graph-intervention'].includes(c))
      .map(id => ({ condition: [names[id], tasks.filter(t => eligible(t, id)).length],
        results: Object.fromEntries(table.metrics.map((m: string) => [m, null])) })) }
    : table),
  changesFromV1: [
    '140 full/masked/cropped pairs are new renders; v1 standard images were already operand-isolated.',
    'Edge withholding and reordering: 146 applicable items, excluding 87 interface items with no edge list.',
    'Choice-order: 469 applicable items, because 73 graph-removal questions now use integer response.',
    'ID permutation: 576 applicable items; 24 evidence-limit and 17 source-sequence items have no B-labels.',
    'Fixed two-view access replaces unspecified interactive rotate/zoom; adaptive tool use is not implemented or claimed.',
    'Legacy replay requires authentic historical wire requests; absent snapshots imply ineligibility.',
  ],
  v1Replay: { status: 'ineligible-until-authentic-request-manifest-provided', eligibleRequests: null, results: null,
    policy: 'Never reconstruct a leaky request and describe it as a historical experiment.' },
};
writeFileSync(resolve(root, 'benchmark/paper/ldraw-v2-experiments.json'), JSON.stringify(plan, null, 2) + '\n');
writeFileSync(resolve(data, 'experiment-task-lists.json'), JSON.stringify(plan.conditions, null, 2) + '\n');
console.log(JSON.stringify({ status: plan.status, conditions: plan.conditions.map(({ id, n }) => ({ id, n })) }, null, 2));
