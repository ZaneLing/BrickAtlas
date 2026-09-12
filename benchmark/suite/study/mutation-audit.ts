import assert from 'node:assert/strict';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { caseSpecs, taskForV2 } from '../v2/cases';
import { evaluateStrict } from './strict-evaluate';
import { independentPlanCheck, heightPlan } from './algorithms';
import { relative } from '../geometry';
import { STUDY } from './protocol';

export function mutationAudit() {
  let checks = 0, plans = 0, edits = 0, repairs = 0, structures = 0;
  for (const spec of caseSpecs()) {
    if (!['default', 'symbolic'].includes(spec.condition)) continue;
    const task = taskForV2(spec);
    if (spec.kind === 'plan') {
      const correct = (heightPlan(task.public) as { order: string[] }).order;
      for (const order of [correct.slice(1), [...correct, correct[0]], ['missing-id', ...correct],
        [...correct].reverse()]) {
        const accepted = evaluateStrict(task, { order }).metrics.success === 1;
        assert.equal(accepted, independentPlanCheck(task.public, order)); checks++;
      }
      assert.equal(evaluateStrict(task, { order: correct.slice(0, -1) }).metrics.success, 0); checks++; plans++;
    } else if (spec.kind === 'edit') {
      assert.equal(evaluateStrict(task, task.source).metrics.success, 0, 'No-op cannot solve a nonempty edit'); checks++; edits++;
    } else if (spec.kind === 'repair') {
      const answer = structuredClone(task.oracle) as any;
      answer.faultIds = task.changedIds.length ? [] : [task.target.parts[0].id];
      assert.equal(evaluateStrict(task, answer).metrics.success, 0); checks++;
      if (task.changedIds.length) {
        answer.faultIds = [...task.changedIds, ...task.changedIds];
        assert.equal(evaluateStrict(task, answer).metrics.format, 0); checks++;
      }
      repairs++;
    } else if (spec.kind === 'reconstruct') {
      const renamed = { version: 1 as const, parts: task.target.parts.map((p, i) => ({ ...p, id: `renamed-${i}`, turn: (p.turn + 2) % 4 })).reverse() };
      assert.equal(evaluateStrict(task, renamed).metrics.success, 1); checks++;
      assert.equal(evaluateStrict(task, relative(renamed)).metrics.success, 1); checks++;
      const duplicate = structuredClone(task.target);
      duplicate.parts[1].id = duplicate.parts[0].id;
      assert.equal(evaluateStrict(task, duplicate).metrics.format, 0); checks++; structures++;
    }
  }
  const result = { checks, plans, edits, repairs, structures, differences: [],
    scope: 'All v2 objects: plan omissions/duplicates/unknown IDs/reversal; edit no-op; repair false localization; structure ID/yaw/order invariance and duplicate IDs.',
    apiRequests: 0 };
  atomicJson(resolve(STUDY, 'mutation-audit.json'), result); return result;
}
