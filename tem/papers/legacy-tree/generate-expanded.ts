import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { digest } from '../suite/data';
import { validationCases } from '../suite/study/model-validation';
import { PAPER_MODELS } from '../suite/study/paper-models';
import { getSpec, taskForV2 } from '../suite/v2/cases';
import { publicAlgorithm } from '../suite/v2/baseline';
import { heightPlan, trainRetrieval } from '../suite/study/algorithms';
import { copyInputAnswer } from '../suite/study/paper-audit';
import { evaluateStrict } from '../suite/study/strict-evaluate';
import type { PublicTask } from '../suite/shared';

const here = dirname(fileURLToPath(import.meta.url)), study = resolve(here, '../suite/artifacts/study');
const read = (p: string) => JSON.parse(readFileSync(resolve(study, p), 'utf8'));
const analysis = read('paper-models/analysis.json'), ambiguity = read('ambiguity/audit.json');
const render = read('ambiguity/render-verification.json');
assert.equal(analysis.status, 'complete'); assert.equal(analysis.newResponses, 156);
assert.equal(analysis.sourceGroups, 3); assert.equal(analysis.summary.length, 8);
const labels: Record<string, string> = { 'openai/gpt-4.1-mini': 'GPT-4.1 mini', 'openai/gpt-4.1': 'GPT-4.1',
  'google/gemini-2.5-flash': 'Gemini 2.5 Flash', 'qwen/qwen3-vl-32b-instruct': 'Qwen3-VL-32B',
  ...Object.fromEntries(PAPER_MODELS.map(m => [m.id, m.label])) };
const families = ['relations', 'reconstruct', 'generate', 'complete', 'edit', 'plan', 'repair'];
const write = (name: string, rows: string[]) => writeFileSync(resolve(here, 'tables', name + '.tex'),
  '% Generated from expanded measured evidence; not projected performance.\n' + rows.join('\n') + '\n');
const fraction = (r: any) => r.returned === 0 ? '\\unmeasured' : `${r.successes}/${r.planned}`;
const neural = analysis.summary.map((m: any) => `${labels[m.model]}${m.cohort === 'new' ? '$^{+}$' : ''} & ${
  families.map(k => fraction(m.families[k])).join(' & ')} & ${m.formatAccepted}/39 & ${m.cost.toFixed(3)} \\\\`);
const selection = validationCases().rows.filter(r => r.arm === 'ordinary');
const methods = [
  { label: 'Copy current', supports: ['complete', 'edit', 'repair'], predict: copyInputAnswer },
  { label: 'BOM / extent retrieval', supports: ['reconstruct', 'generate', 'complete', 'repair'], predict: (p: PublicTask) => trainRetrieval(p)?.answer },
  { label: 'Symbolic rules', supports: ['relations', 'edit'], predict: publicAlgorithm },
  { label: 'Greedy legal action', supports: ['plan'], predict: publicAlgorithm },
  { label: 'Height-sorted plan', supports: ['plan'], predict: heightPlan },
];
const baselineRows = methods.map(method => {
  const rows = selection.filter(r => method.supports.includes(getSpec(r.caseId).kind)).map(row => {
    const task = taskForV2(getSpec(row.caseId)), answer = method.predict(task.public);
    return { caseId: row.caseId, kind: task.spec.kind, variant: task.spec.variant,
      group: task.spec.group, answer, verdict: evaluateStrict(task, answer) };
  });
  return { method: method.label, supports: method.supports, rows };
});
write('expanded-main', [
  '\\rowcolor{tableband}\\multicolumn{10}{l}{\\textit{Vision--language models: same three source objects}} \\\\',
  ...neural, '\\midrule',
  '\\rowcolor{tableband}\\multicolumn{10}{l}{\\textit{Public-input algorithmic controls: supported tasks only}} \\\\',
  ...baselineRows.map(b => `${b.method} & ${
  families.map(kind => {
    const rows = b.rows.filter(r => r.kind === kind);
    return rows.length ? `${rows.reduce((n, r) => n + r.verdict.metrics.success, 0)}/${rows.length}` : '--';
  }).join(' & ')} & -- & -- \\\\`)]);
const pct = (v: number | null | undefined) => v == null ? '--' : (v * 100).toFixed(1);
write('expanded-diagnostics', analysis.summary.map((m: any) => {
  const f = m.families, vals = [
    f.reconstruct.metrics.partF1?.value, f.reconstruct.metrics.surfaceF1?.value,
    f.complete.metrics.additionF1?.value, f.complete.metrics.preservation?.value,
    f.plan.metrics.legalPrefix?.value,
    analysis.rows.filter((r: any) => r.model === m.model && getSpec(r.caseId).kind === 'repair'
      && getSpec(r.caseId).variant !== 'none').reduce((n: number, r: any) => n + r.diagnosis.verdict.metrics.localizationF1, 0) / 6,
  ];
  return `${labels[m.model]} & ${vals.map(pct).join(' & ')} & ${m.truncated}/39 \\\\`;
}));
const variants = [...new Set(selection.map(r => { const s = getSpec(r.caseId); return `${s.kind}/${s.variant}`; }))];
const variantOutcomes = variants.map(variant => analysis.rows.filter((r: any) =>
  `${getSpec(r.caseId).kind}/${getSpec(r.caseId).variant}` === variant).map((r: any) => r.diagnosis.verdict.metrics.success));
const floors = variantOutcomes.filter(v => v.every((x: number) => x === 0)).length;
const ceilings = variantOutcomes.filter(v => v.every((x: number) => x === 1)).length;
const reconstruction = analysis.summary.map((m: any) => m.families.reconstruct.successes);
const added = analysis.summary.map((m: any) => m.families.complete.metrics.additionF1.value * 100);
write('expanded-findings', [
  `In this shared sample, ${floors} of 13 variants have zero exact success across all eight models and ${ceilings} are saturated.`,
  `Reconstruction successes range from ${Math.min(...reconstruction)}/3 to ${Math.max(...reconstruction)}/3;
mean added-part F1 ranges from ${Math.min(...added).toFixed(1)}\\% to ${Math.max(...added).toFixed(1)}\\%.`,
  'These are descriptive ranges, not evidence of a stable population ranking. Floor/ceiling patterns motivate calibrated difficulty and local metrics before a larger comparison.',
]);
write('expanded-variants', variants.map(variant => `${variant.replaceAll('_', '\\_')} & ${
  analysis.summary.map((m: any) => {
    const rows = analysis.rows.filter((r: any) => r.model === m.model && `${getSpec(r.caseId).kind}/${getSpec(r.caseId).variant}` === variant);
    assert.equal(rows.length, 3);
    return `${rows.reduce((n: number, r: any) => n + r.diagnosis.verdict.metrics.success, 0)}/3`;
  }).join(' & ')} \\\\`));
write('ambiguity-audit', ambiguity.conditions.flatMap((c: any) => Object.entries(c.baselines).map(([method, v]: [string, any]) => {
  const name: Record<string, string> = { oracle: 'Set-valued oracle', enumeration: 'Public-input enumeration',
    alwaysNo: 'Always no', alwaysUnknown: 'Always undetermined', firstWitness: 'Single-witness answer' };
  return `${c.condition === 'exterior' ? 'Exterior' : 'Disclosed'} & ${name[method]} & ${v.correct}/${v.total} & ${pct(v.balancedAccuracy)} & ${pct(v.sourceMacro)} \\\\`;
})));
write('ambiguity-counts', ambiguity.conditions.map((c: any) =>
  `${c.condition === 'exterior' ? 'Exterior' : 'Support disclosed'} & ${c.groups} & ${c.cases} & ${c.counts.yes} & ${c.counts.no} & ${c.counts.undetermined} \\\\`));
write('expanded-resources', [`The four new models cost \\$${analysis.newCost.toFixed(9)} across 156 settled requests.
The cumulative campaign is 1,765 calls and \\$${analysis.campaignAfter.toFixed(9)}, below the unchanged \\$4.50 cap.
The new model allocation was capped at \\$0.75; geometry audits and paper renders made no model calls.`]);
const artifacts = ['paper-models/protocol.json', 'paper-models/run.json', 'paper-models/analysis.json', 'ambiguity/audit.json',
  'ambiguity/render-verification.json'];
writeFileSync(resolve(here, 'expanded-evidence.json'), JSON.stringify({
  scope: 'Eight-model descriptive pilot, same-source algorithmic controls, finite-grammar extension; no confirmatory claims.',
  models: 8, sharedSources: 3, newCalls: 156, historicalCalls: 156, newCost: analysis.newCost,
  campaignAfter: analysis.campaignAfter, ambiguityCases: ambiguity.cases, ambiguityFamilies: ambiguity.sourceGroups,
  pixelComparisons: render.comparisons, allPixelIdentical: render.allPixelIdentical,
  sourceHashes: Object.fromEntries(artifacts.map(p => [p, digest(readFileSync(resolve(study, p), 'utf8'))])),
  generatorHash: digest(readFileSync(fileURLToPath(import.meta.url), 'utf8')), baselineRows,
}, null, 2) + '\n');
console.log(JSON.stringify({ models: 8, sharedSources: 3, newCalls: 156, newCost: analysis.newCost }));
