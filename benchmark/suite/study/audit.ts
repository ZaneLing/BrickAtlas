import assert from 'node:assert/strict';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS } from '../storage';
import { dataset } from '../v2/dataset';
import { caseSpecs, taskForV2 } from '../v2/cases';
import { evaluate } from '../v2/evaluate';
import { independentMetrics } from './independent';
import { heightPlan, independentQA, independentPlanCheck, trainRetrieval } from './algorithms';

export async function audit() {
  let metricComparisons = 0, geometryCases = 0, relationCases = 0, plans = 0, retrievalCases = 0;
  const differences: unknown[] = [], retrieval: unknown[] = [];
  const first = new Set(dataset().map(m => m.id));
  for (const spec of caseSpecs()) {
    if (spec.kind === 'reconstruct' && spec.condition === 'symbolic') {
      const task = taskForV2(spec), parts = task.target.parts;
      const variants = [
        [...parts].reverse().map(p => ({ ...p, turn: (p.turn + 2) % 4 })),
        parts.slice(0, -1),
        parts.map((p, i) => i === parts.length - 1 ? { ...p, color: p.color === 'red' ? 'blue' as const : 'red' as const } : p),
      ];
      for (const actual of variants) {
        const expected = independentMetrics(parts, actual), scored = evaluate(task, { version: 1, parts: actual });
        for (const [k, value] of Object.entries(expected)) {
          if (Math.abs(value - (scored.metrics[k] ?? -1)) > 1e-9) differences.push({ caseId: spec.id, metric: k, expected: value, actual: scored.metrics[k] });
          metricComparisons++;
        }
        geometryCases++;
      }
    } else if (spec.kind === 'relations') {
      const task = taskForV2(spec); assert.deepEqual(independentQA(task.public), task.oracle); relationCases++;
    } else if (spec.kind === 'plan') {
      const task = taskForV2(spec), answer = heightPlan(task.public) as { order: string[] };
      assert.equal(evaluate(task, answer).metrics.success, 1);
      assert.equal(independentPlanCheck(task.public, answer.order), true); plans++;
    } else if (spec.kind === 'reconstruct' && spec.condition === 'ordinary' && spec.split !== 'train') {
      const task = taskForV2(spec), retrieved = trainRetrieval(task.public)!;
      assert.notEqual(retrieved.retrieved.group, spec.group);
      assert.equal(dataset().find(m => m.id === retrieved.retrieved.id)!.split, 'train');
      retrieval.push({ caseId: spec.id, retrieved: retrieved.retrieved,
        verdict: evaluate(task, retrieved.answer) }); retrievalCases++;
    }
  }
  const report = { geometryCases, metricComparisons, relationCases, plans, retrievalCases, differences,
    heightSortedPlannerAllPass: plans === first.size * 2, independentGeometryMethod: 'unordered cell maps and face intersections',
    scope: 'All source objects: ID/yaw symmetry, piece deletion, recolor. Does not prove all arbitrary malformed inputs or physical mechanics.',
    apiRequests: 0 };
  atomicJson(resolve(ARTIFACTS, 'study/independent-audit.json'), report);
  atomicJson(resolve(ARTIFACTS, 'study/train-retrieval.json'), retrieval);
  assert.equal(differences.length, 0, JSON.stringify(differences.slice(0, 5)));
  return report;
}
