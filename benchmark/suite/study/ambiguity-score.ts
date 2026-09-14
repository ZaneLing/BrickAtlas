import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { AMBIGUITY_DIR, scoreSetAnswer, type SetAnswer } from './ambiguity';

export interface AmbiguityPrediction { caseId: string; answer: unknown }
export function scoreAmbiguityBatch(
  cases: Array<{ id: string; group: string; condition: string; expected: SetAnswer }>,
  predictions: AmbiguityPrediction[],
) {
  assert.ok(cases.length > 0);
  const ids = new Set(cases.map(c => c.id)), found = new Map<string, unknown>();
  assert.equal(ids.size, cases.length, 'Duplicate selected case');
  for (const p of predictions) {
    assert.ok(ids.has(p.caseId), 'Unknown prediction case');
    assert.ok(!found.has(p.caseId), 'Duplicate prediction case');
    found.set(p.caseId, p.answer);
  }
  const rows = cases.map(c => ({ ...c, returned: found.has(c.id), ...scoreSetAnswer(c.expected, found.get(c.id)) }));
  const conditions = [...new Set(cases.map(c => c.condition))].map(condition => {
    const selected = rows.filter(c => c.condition === condition);
    const conditional = (metric: 'falseCertainty' | 'unnecessaryAbstention') => {
      const values = selected.map(r => r[metric]).filter((v): v is number => v !== null);
      return { numerator: values.reduce((a, b) => a + b, 0), denominator: values.length,
        rate: values.length ? values.reduce((a, b) => a + b, 0) / values.length : null };
    };
    const classes = [...new Set(selected.map(c => c.expected))].map(label => {
      const group = selected.filter(c => c.expected === label);
      return { label, correct: group.reduce((n, r) => n + r.success, 0), n: group.length };
    });
    const groups = [...new Set(selected.map(c => c.group))].map(group => {
      const values = selected.filter(c => c.group === group);
      return values.reduce((n, r) => n + r.success, 0) / values.length;
    });
    return { condition, planned: selected.length, sourceGroups: groups.length,
      returned: selected.filter(c => c.returned).length, missing: selected.filter(c => !c.returned).length,
      format: selected.reduce((n, r) => n + r.format, 0), successes: selected.reduce((n, r) => n + r.success, 0),
      classes, balancedAccuracy: classes.reduce((n, r) => n + r.correct / r.n, 0) / classes.length,
      sourceMacroAccuracy: groups.reduce((a, b) => a + b, 0) / groups.length,
      falseCertainty: conditional('falseCertainty'), unnecessaryAbstention: conditional('unnecessaryAbstention') };
  });
  return { rows, conditions, scope: 'All selected cases stay in denominators. Missing/malformed outputs fail success; conditional error rates must be read with response/format coverage, since missing outputs make neither definite claims nor explicit abstentions.' };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const [input, output] = process.argv.slice(2);
  assert.ok(input && output, 'Usage: ambiguity-score.ts predictions.jsonl report.json');
  assert.notEqual(resolve(input), resolve(output), 'Do not overwrite submitted predictions');
  const audit = JSON.parse(readFileSync(resolve(AMBIGUITY_DIR, 'audit.json'), 'utf8'));
  const raw = readFileSync(resolve(input), 'utf8');
  const predictions = raw.trim() ? raw.trim().split('\n').map(line => JSON.parse(line)) : [];
  const result = { version: 'ambiguity-score-1', auditHash: digest(audit), predictionHash: digest(raw),
    ...scoreAmbiguityBatch(audit.rows, predictions), apiRequests: 0 };
  atomicJson(resolve(output), result);
  console.log(JSON.stringify({ cases: result.rows.length, conditions: result.conditions }));
}
