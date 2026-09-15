import { type MechanismTask } from './types';

const object = (value: unknown): value is Record<string, any> =>
  Boolean(value) && typeof value === 'object' && !Array.isArray(value);
const stringArray = (value: unknown): value is string[] =>
  Array.isArray(value) && value.every(x => typeof x === 'string') && new Set(value).size === value.length;
const sameSet = (a: unknown, b: unknown) =>
  stringArray(a) && stringArray(b) && a.length === b.length && a.every(x => b.includes(x));

export function evaluateMechanismTask(task: MechanismTask, raw: unknown) {
  const answer = object(raw) ? raw : {};
  let fields: Record<string, number> = {};
  if (task.kind === 'prefix-dynamics') {
    fields = {
      validPlan: Number(answer.validPlanId === task.oracle.validPlanId),
      failureStep: Number(answer.invalidPlanFirstFailure === task.oracle.invalidPlanFirstFailure),
    };
  } else if (task.kind === 'insertion-access') {
    fields = { accessiblePaths: Number(sameSet(answer.accessiblePathIds, task.oracle.accessiblePathIds)) };
  } else if (task.kind === 'fault-recovery') {
    fields = {
      faultJoint: Number(answer.faultJointId === task.oracle.faultJointId),
      recoveryActions: Number(Array.isArray(answer.actions)
        && JSON.stringify(answer.actions) === JSON.stringify(task.oracle.actions)),
    };
  } else if (task.kind === 'inventory-substitution') {
    fields = { alternative: Number(answer.alternativeId === task.oracle.alternativeId) };
  } else if (task.kind === 'dynamic-robustness') {
    fields = { threshold: Number(answer.maxSafeImpulse === task.oracle.maxSafeImpulse) };
  } else if (task.kind === 'functional-kinematics') {
    fields = {
      joint: Number(answer.jointId === task.oracle.jointId),
      outcome: Number(answer.reachesTarget === task.oracle.reachesTarget),
    };
  } else if (task.kind === 'active-inspection') {
    fields = { query: Number(typeof answer.queryId === 'string'
      && (task.oracle.queryIds as string[]).includes(answer.queryId)) };
  } else {
    fields = { paretoSet: Number(sameSet(answer.paretoIds, task.oracle.paretoIds)) };
  }
  return {
    success: Number(Object.values(fields).length > 0 && Object.values(fields).every(Boolean)),
    format: Number(object(raw)),
    fields,
  };
}
