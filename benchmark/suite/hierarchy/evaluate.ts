import type { HierarchyTask } from './types';

const object = (value: unknown): value is Record<string, unknown> =>
  Boolean(value) && typeof value === 'object' && !Array.isArray(value);

const stringArray = (value: unknown): value is string[] =>
  Array.isArray(value) && value.every(item => typeof item === 'string')
  && new Set(value).size === value.length;

const sameSet = (left: unknown, right: unknown) =>
  stringArray(left) && stringArray(right)
  && left.length === right.length && left.every(item => right.includes(item));

const sameOrder = (left: unknown, right: unknown) =>
  stringArray(left) && stringArray(right) && JSON.stringify(left) === JSON.stringify(right);

function dependencyOrder(task: HierarchyTask, value: unknown) {
  if (!stringArray(value) || !sameSet(value, task.oracle.actionIds)) {
    return { actionSet: 0, dependencies: 0 };
  }
  const positions = new Map(value.map((action, index) => [action.split(':').slice(1).join(':'), index]));
  const edges = Array.isArray(task.input.dependencyEdges)
    ? task.input.dependencyEdges as Array<[string, string]>
    : [];
  const dependencies = edges.every(([parent, child]) => {
    if (!positions.has(parent) || !positions.has(child)) return true;
    return task.family === 'assembly-sequencing'
      ? positions.get(parent)! < positions.get(child)!
      : positions.get(child)! < positions.get(parent)!;
  });
  return { actionSet: 1, dependencies: Number(dependencies) };
}

export function evaluateHierarchyTask(task: HierarchyTask, raw: unknown) {
  const answer = object(raw) ? raw : {};
  let fields: Record<string, number>;
  if (task.format === 'single-choice') {
    fields = { choice: Number(answer.choiceId === task.oracle.choiceId) };
  } else if (task.format === 'multiple-choice') {
    fields = { choices: Number(sameSet(answer.choiceIds, task.oracle.choiceIds)) };
  } else if (task.format === 'ordered-actions') {
    fields = ['assembly-sequencing', 'safe-disassembly'].includes(task.family)
      ? dependencyOrder(task, answer.actionIds)
      : { actionOrder: Number(sameOrder(answer.actionIds, task.oracle.actionIds)) };
  } else {
    fields = {
      plan: Number(answer.planId === task.oracle.planId),
      verification: Number(answer.verificationId === task.oracle.verificationId),
    };
  }
  return {
    success: Number(Object.values(fields).every(Boolean)),
    format: Number(object(raw)),
    fields,
  };
}
