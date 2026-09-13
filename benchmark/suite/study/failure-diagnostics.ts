import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { decode, validate } from '../geometry';
import { parseJSON } from '../score';
import { getSpec, taskForV2, type CaseTask } from '../v2/cases';
import { EVALUATOR_VERSION, evaluateStrict, structureSchemaValid } from './strict-evaluate';
import { localEvidenceRuns } from './local-evidence';
import { STUDY } from './protocol';
import { studyRuns, type StudyRow } from './results';

export const FAILURE_STAGES = ['json', 'response-schema', 'structure-domain', 'geometry',
  'plan-execution', 'answer-mismatch', 'preservation', 'localization', 'target-or-constraints', 'success'] as const;

export function diagnoseResponse(task: CaseTask, raw: string, finishReason: string) {
  const text = raw.trim().replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '');
  let jsonParsed = true;
  try { JSON.parse(text); } catch { jsonParsed = false; }
  const answer = parseJSON(raw), verdict = evaluateStrict(task, answer);
  const object = answer && typeof answer === 'object' && !Array.isArray(answer) ? answer as Record<string, unknown> : null;
  const kind = task.spec.kind, structured = !['parts', 'relations', 'plan'].includes(kind);
  const structure = structured ? (kind === 'repair' ? object?.structure : answer) : null;
  const schema = structured ? structureSchemaValid(structure) : verdict.metrics.format === 1;
  const decoded = structured && schema ? decode(structure) : null;
  const geometryIssues = decoded ? validate(decoded.parts) : [];
  // This is the earliest observable rejection, not an inferred cognitive cause.
  let stage: typeof FAILURE_STAGES[number];
  if (!jsonParsed) stage = 'json';
  else if (!object || !schema) stage = 'response-schema';
  else if (structured && !decoded) stage = 'structure-domain';
  else if (verdict.metrics.format !== 1) stage = 'response-schema';
  else if (verdict.metrics.success === 1) stage = 'success';
  else if (kind === 'plan') stage = 'plan-execution';
  else if (kind === 'relations' || kind === 'parts') stage = 'answer-mismatch';
  else if (geometryIssues.length) stage = 'geometry';
  else if (verdict.metrics.preservation !== undefined && verdict.metrics.preservation !== 1) stage = 'preservation';
  else if (kind === 'repair' && verdict.metrics.localizationF1 !== 1) stage = 'localization';
  else stage = 'target-or-constraints';
  const envelopeFields = object ? ['prompt', 'input', 'responseSchema', 'imageTitles'].filter(k => Object.hasOwn(object, k)) : [];
  const nestedStructure = object && kind !== 'repair' && structureSchemaValid(object.structure);
  return { stage, jsonParsed, schemaValid: schema, formatAccepted: verdict.metrics.format === 1,
    geometryChecked: !!decoded, geometryIssues, envelopeFields, nestedStructure: !!nestedStructure,
    tokenLimitReached: finishReason === 'length', verdict };
}

export function diagnosticSummary(rows: Array<ReturnType<typeof diagnoseResponse>>) {
  const stages = Object.fromEntries(FAILURE_STAGES.map(stage => [stage, rows.filter(r => r.stage === stage).length]));
  const metrics = [...new Set(rows.flatMap(r => Object.keys(r.verdict.metrics)))];
  const summarize = (selected: typeof rows) => Object.fromEntries(metrics.map(key => {
    const values = selected.map(r => r.verdict.metrics[key]).filter((v): v is number => typeof v === 'number');
    return [key, { value: values.length ? values.reduce((n, v) => n + v, 0) / values.length : null, denominator: values.length }];
  }));
  assert.equal(Object.values(stages).reduce((n, v) => n + v, 0), rows.length);
  return { n: rows.length, stages, jsonParsed: rows.filter(r => r.jsonParsed).length,
    formatAccepted: rows.filter(r => r.formatAccepted).length,
    tokenLimitReached: rows.filter(r => r.tokenLimitReached).length,
    envelopeLike: rows.filter(r => r.envelopeFields.length >= 3).length,
    nestedStructure: rows.filter(r => r.nestedStructure).length,
    allResponses: summarize(rows), formatAcceptedOnly: summarize(rows.filter(r => r.formatAccepted)) };
}

export function failureDiagnostics() {
  const api = studyRuns(), locals = localEvidenceRuns();
  const rows = [...api, ...locals].flatMap(run => (run.rows as StudyRow[]).map(row => {
    const spec = getSpec(row.caseId), diagnosis = diagnoseResponse(taskForV2(spec), row.call.content, row.call.finishReason);
    // Strict diagnostics may only be attached to historical evidence if scores agree.
    assert.deepEqual(diagnosis.verdict.metrics, row.verdict.metrics, `Scorer drift: ${run.id}/${row.caseId}`);
    return { runId: run.id, model: row.model ?? run.model, caseId: spec.id, group: spec.group,
      kind: spec.kind, variant: spec.variant, condition: spec.condition, split: spec.split,
      arm: row.arm ?? 'one-shot', rawHash: digest(row.call.content), ...diagnosis };
  }));
  const keys = [...new Set(rows.map(r => [r.runId, r.model, r.kind, r.variant, r.condition, r.split, r.arm].join('|')))];
  const groups = keys.map(stratum => {
    const selected = rows.filter(r => [r.runId, r.model, r.kind, r.variant, r.condition, r.split, r.arm].join('|') === stratum);
    return { stratum, sourceGroups: new Set(selected.map(r => r.group)).size, ...diagnosticSummary(selected) };
  });
  const byModel = [...new Set(rows.filter(r => r.arm === 'one-shot').map(r => r.model))].map(model => ({
    model, ...diagnosticSummary(rows.filter(r => r.model === model && r.arm === 'one-shot')),
  }));
  const sourcePaths = [
    ...api.map(run => `runs/${run.id}/run.json`),
    ...locals.flatMap(run => [`local/${run.id.slice(6)}/manifest.json`, `local/${run.id.slice(6)}/predictions.json`]),
  ];
  const result = { version: 'failure-diagnostics-1', evaluator: EVALUATOR_VERSION, apiRequests: 0,
    sourceHashes: Object.fromEntries(sourcePaths.map(path => [path, digest(readFileSync(resolve(STUDY, path), 'utf8'))])),
    rows, groups, byModel,
    caveats: ['Post-hoc development diagnostics on already observed data, not a new held-out experiment.',
      'Stages are ordered observable rejection gates, not causal perception/reasoning labels.',
      'Token-limit flags can overlap every stage; envelope-like means three prompt metadata fields, not proven verbatim copying.',
      'Format-conditional metrics are diagnostic only; the main denominator includes every response.',
      'Ordinary reconstruction includes RGB and BOM; control arms retain their actual additional or missing information.'] };
  atomicJson(resolve(STUDY, 'failure-diagnostics.json'), result);
  return { responses: rows.length, groups: groups.length, models: byModel.map(({ model, n, stages, tokenLimitReached, envelopeLike }) =>
    ({ model, n, stages, tokenLimitReached, envelopeLike })) };
}
