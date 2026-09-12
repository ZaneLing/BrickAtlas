import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { digest } from '../data';
import { sourceHashes } from '../v2/build';
import { evaluationHashes, verifySelection, type Selection } from '../v2/batch';
import { getSpec, taskForV2 } from '../v2/cases';
import { jsonLines } from '../v2/verify';
import { EVALUATOR_VERSION, evaluateStrict } from './strict-evaluate';
import { strictAggregator, strictSourceHashes } from './strict-batch';
import { strictTrace } from './strict-trace';

export async function replayStrictRun(dir: string) {
  const summary = JSON.parse(readFileSync(resolve(dir, 'summary.json'), 'utf8'));
  const selection: Selection = JSON.parse(readFileSync(resolve(dir, 'selection.json'), 'utf8'));
  assert.equal(summary.evaluatorVersion, EVALUATOR_VERSION);
  assert.equal(summary.baseline, false);
  assert.equal(summary.selectionHash, selection.hash);
  assert.deepEqual(summary.sourceHashes, sourceHashes());
  assert.deepEqual(summary.evaluationHashes, evaluationHashes());
  assert.deepEqual(summary.strictSourceHashes, strictSourceHashes());
  const specs = verifySelection(selection), seen = new Set<string>(), aggregate = strictAggregator();
  for await (const row of jsonLines(resolve(dir, 'cases.jsonl.gz'))) {
    assert.equal(row.spec.id, specs[seen.size]?.id, 'Frozen case order or membership changed');
    assert.ok(!seen.has(row.spec.id)); seen.add(row.spec.id);
    const spec = getSpec(row.spec.id), task = taskForV2(spec);
    assert.deepEqual(row.spec, spec); assert.equal(row.inputHash, digest(task.public));
    assert.equal(typeof row.missing, 'boolean');
    assert.ok(Object.hasOwn(row, 'answer'));
    if (row.missing) assert.equal(row.answer, null);
    const verdict = evaluateStrict(task, row.answer);
    assert.deepEqual(row.verdict, verdict);
    aggregate.append(spec, verdict, row.missing);
    const trace = strictTrace(summary.id, summary.model, row, []);
    assert.deepEqual(trace.verdict, verdict);
    assert.deepEqual(trace.events.find(e => e.kind === 'response')!.payload, {
      answer: row.answer, missing: row.missing, evaluatorVersion: EVALUATOR_VERSION,
    });
    for (const [i, event] of trace.events.entries()) {
      assert.equal(digest(trace.states[event.before]), event.before);
      assert.equal(digest(trace.states[event.after]), event.after);
      if (i) assert.equal(event.before, trace.events[i - 1].after);
    }
  }
  assert.equal(seen.size, specs.length); assert.equal(summary.cases, seen.size);
  assert.deepEqual(summary.rows, aggregate.rows());
  return {
    id: summary.id, cases: seen.size, traceCases: seen.size, evaluatorVersion: EVALUATOR_VERSION,
    scoresReproduced: true, aggregatesReproduced: true, publicBaselineRecomputed: false,
    compressedSha256: createHash('sha256').update(readFileSync(resolve(dir, 'cases.jsonl.gz'))).digest('hex'),
  };
}
