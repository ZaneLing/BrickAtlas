import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { constructibilityCases } from './cases';
import { evaluateConstructibility } from './evaluate';
import { VERSION } from './geometry';

export function scoreConstructibility(raw: unknown) {
  assert.ok(Array.isArray(raw), 'Expected [{id,answer}]');
  const cases = constructibilityCases();
  const allowed = new Set(cases.map(c => c.id));
  const predictions = new Map<string, unknown>();
  for (const row of raw) {
    assert.ok(row && typeof row.id === 'string' && allowed.has(row.id), 'unknown_id');
    assert.ok(!predictions.has(row.id), 'duplicate_id');
    predictions.set(row.id, row.answer);
  }
  const rows = cases.map(c => ({
    id: c.id,
    sourceGroup: c.sourceGroup,
    kind: c.kind,
    present: predictions.has(c.id),
    result: evaluateConstructibility(c, predictions.get(c.id)),
  }));
  const kinds = [...new Set(rows.map(row => row.kind))];
  return {
    version: VERSION,
    expected: cases.length,
    submitted: predictions.size,
    missing: cases.length - predictions.size,
    rows,
    byKind: Object.fromEntries(kinds.map(kind => {
      const selected = rows.filter(row => row.kind === kind);
      return [kind, {
        cases: selected.length,
        successes: selected.filter(row => row.result.success).length,
        sourceGroups: new Set(selected.map(row => row.sourceGroup)).size,
      }];
    })),
    aggregation: 'Report each family separately. Do not treat 78 conditions from six sources as independent trials.',
  };
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(import.meta.filename)) {
  const [input, output] = process.argv.slice(2);
  assert.ok(input && output, 'score.ts predictions.json output.json');
  const result = scoreConstructibility(JSON.parse(readFileSync(input, 'utf8')));
  writeFileSync(output, JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify({
    expected: result.expected,
    submitted: result.submitted,
    missing: result.missing,
    byKind: result.byKind,
  }));
}
