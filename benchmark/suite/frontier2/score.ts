import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { maintenanceCases, scoreMaintenance, VERSION } from './maintenance';
import { observationCases, admissible, evaluatePolicy } from './observation';
import { schedulingCases, scoreSchedule } from './release';
import { sameSet } from '../frontier/tasks';
import { poseCases, scorePose } from './pose';

export function scoreResponses(raw: unknown) {
  assert.ok(Array.isArray(raw), 'Expected [{id,answer}]');
  const ms = maintenanceCases(), os = observationCases(), ss = schedulingCases();
  const cases: Array<{ id: string; group: string; kind: string; condition: string; score: (a: any) => any }> = [
    ...ms.flatMap(c => ['symbolic', 'layers'].map(condition => ({
      id: c.id + '-' + condition, group: c.sourceGroup, kind: 'maintenance', condition,
      score: (a: any) => scoreMaintenance(c, a),
    }))),
    ...os.flatMap(c => ['admissible-set', 'scan-policy'].map(kind => ({
      id: c.id + '-' + kind, group: c.sourceGroup, kind, condition: 'geometry',
      score: (a: any) => kind === 'scan-policy' ? evaluatePolicy(c.input, a) : {
        success: Number(sameSet(a?.possibleIds, admissible(c.input).map(w => w.id))),
      },
    }))),
    ...ss.map(c => ({ id: c.id, group: c.modelId, kind: 'deadline-schedule', condition: 'symbolic',
      score: (a: any) => scoreSchedule(c, a) })),
    ...poseCases().flatMap(c => ['symbolic', 'layers'].map(condition => ({
      id: c.id + '-' + condition, group: c.sourceGroup, kind: 'pose-patch', condition,
      score: (a: any) => scorePose(c, a),
    }))),
  ];
  const allowed = new Set(cases.map(c => c.id)), predictions = new Map<string, any>();
  for (const row of raw) {
    assert.ok(row && typeof row.id === 'string' && allowed.has(row.id), 'unknown_id');
    assert.ok(!predictions.has(row.id), 'duplicate_id'); predictions.set(row.id, row.answer);
  }
  const rows = cases.map(c => ({ id: c.id, sourceGroup: c.group, kind: c.kind, condition: c.condition,
    present: predictions.has(c.id), result: c.score(predictions.get(c.id)) }));
  const groups = [...new Set(rows.map(r => `${r.kind}:${r.condition}`))];
  return { version: VERSION, expected: cases.length, submitted: predictions.size,
    missing: cases.length - predictions.size, rows,
    strata: Object.fromEntries(groups.map(g => {
      const set = rows.filter(r => `${r.kind}:${r.condition}` === g);
      return [g, { denominator: set.length, success: set.filter(r => r.result.success).length,
        sourceGroups: new Set(set.map(r => r.sourceGroup)).size }];
    })), inference: 'No confidence intervals are inferred from six design sources. Never pool modalities or derived cases as independent trials.' };
}

export function scoreStageResponses(raw: unknown) {
  assert.ok(Array.isArray(raw), 'Expected [{id,stage,answer}]');
  const allowed = new Set(maintenanceCases().flatMap(c => ['symbolic', 'layers'].map(k => c.id + '-' + k)));
  const grouped = new Map<string, Record<string, unknown>>();
  for (const r of raw) {
    assert.ok(r && allowed.has(r.id) && ['diagnosis', 'access', 'repair'].includes(r.stage), 'unknown_stage');
    const old = grouped.get(r.id) ?? {};
    assert.ok(!Object.hasOwn(old, r.stage), 'duplicate_stage');
    old[r.stage] = r.answer; grouped.set(r.id, old);
  }
  return { ...scoreResponses([...grouped].map(([id, answer]) => ({ id, answer }))),
    elicitation: 'independent-stage', expectedStageResponses: 216, submittedStages: raw.length,
    missingStages: 216 - raw.length };
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(import.meta.filename)) {
  const [input, output, mode] = process.argv.slice(2); assert.ok(input && output, 'score.ts predictions.json output.json [--stages]');
  const raw = JSON.parse(readFileSync(input, 'utf8'));
  const result = mode === '--stages' ? scoreStageResponses(raw) : scoreResponses(raw);
  writeFileSync(output, JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify({ expected: result.expected, submitted: result.submitted, missing: result.missing, strata: result.strata }));
}
