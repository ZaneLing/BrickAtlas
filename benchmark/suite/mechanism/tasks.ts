import assert from 'node:assert/strict';
import { mechanismModels } from './models';
import {
  evaluateAccessPaths,
  initPhysics,
  paretoAlternatives,
  simulateFunctionalMotion,
  simulateImpulseLadder,
  simulateJointFault,
  simulatePrefix,
} from './physics';
import { type InspectionQuery, type MechanismModel, type MechanismTask } from './types';

export const MECHANISM_VERSION = 'brickatlas-mechanism-1';

function modelSummary(model: MechanismModel) {
  return {
    id: model.id,
    name: model.name,
    domain: model.domain,
    description: model.description,
    modules: model.modules.map(m => ({ id: m.id, name: m.name, role: m.role, anchored: m.anchored, mass: m.mass })),
    joints: model.joints.map(j => ({ id: j.id, name: j.name, type: j.type,
      parent: j.parent, child: j.child, axis: j.axis, limits: j.limits })),
  };
}

export function infoGain(worlds: string[], query: InspectionQuery) {
  const groups = new Map<string, number>();
  for (const world of worlds) groups.set(query.returns[world], (groups.get(query.returns[world]) ?? 0) + 1);
  const h = Math.log2(worlds.length);
  const conditional = [...groups.values()].reduce((sum, n) => {
    const p = n / worlds.length;
    return sum + p * Math.log2(n);
  }, 0);
  return { queryId: query.id, informationGain: h - conditional, efficiency: (h - conditional) / query.cost };
}

function paretoAll(model: MechanismModel) {
  const candidates = model.taskConfig.inventoryAlternatives.filter(c => c.jointMode !== 'none');
  return candidates.filter(a => !candidates.some(b => b.id !== a.id
    && b.cost <= a.cost && b.mass <= a.mass && b.stiffness >= a.stiffness
    && (b.cost < a.cost || b.mass < a.mass || b.stiffness > a.stiffness)));
}

function visual(model: MechanismModel, kind: MechanismTask['kind'], highlightModules: string[],
  view: MechanismTask['visualization']['view'] = 'iso') {
  return {
    modelImage: `images/models/${model.id}-iso.png`,
    detailImage: `images/tasks/${model.id}-${kind}.png`,
    highlightModules,
    view,
  };
}

let cache: Promise<MechanismTask[]> | undefined;
export function mechanismTasks() {
  return cache ??= buildTasks();
}

async function buildTasks() {
  await initPhysics();
  const tasks: MechanismTask[] = [];
  for (const model of mechanismModels()) {
    const summary = modelSummary(model);

    const validOrder = [...model.assemblyOrder];
    const invalidFirst = [...model.modules].filter(m => !m.anchored)
      .sort((a, b) => b.position[1] - a.position[1])[0].id;
    const invalidOrder = [invalidFirst, ...validOrder.filter(id => id !== invalidFirst)];
    const valid = await simulatePrefix(model, validOrder);
    const invalid = await simulatePrefix(model, invalidOrder);
    assert.equal(valid.success, 1, `${model.id}: valid prefix`);
    assert.equal(invalid.firstUnstableStep, 0, `${model.id}: invalid prefix`);
    tasks.push({
      id: `m1-${model.id}-prefix-dynamics`, sourceGroup: model.id, kind: 'prefix-dynamics',
      capability: ['long-horizon planning', 'prefix dynamics', 'causal support'],
      question: 'Which candidate module order remains dynamically supported at every prefix, and where does the other first fail?',
      input: { model: summary, candidates: [{ id: 'plan-a', order: validOrder }, { id: 'plan-b', order: invalidOrder }],
        protocol: { gravity: 9.81, horizonSecondsPerPrefix: 1, unstableDisplacement: .35 } },
      oracle: { validPlanId: 'plan-a', invalidPlanFirstFailure: invalid.firstUnstableStep },
      visualization: visual(model, 'prefix-dynamics', [invalidOrder[0]]),
    });

    const access = await evaluateAccessPaths(model);
    const accessiblePathIds = access.filter(row => row.accessible).map(row => row.pathId);
    assert.ok(accessiblePathIds.length > 0 && accessiblePathIds.length < access.length, `${model.id}: access contrast`);
    tasks.push({
      id: `m1-${model.id}-insertion-access`, sourceGroup: model.id, kind: 'insertion-access',
      capability: ['continuous collision checking', 'assembly accessibility', 'service planning'],
      question: 'Which proposed swept-volume paths let the declared service tool reach the target interface without collision?',
      input: { model: summary, serviceModule: model.taskConfig.serviceModule, paths: model.taskConfig.accessPaths,
        protocol: 'Rapier 3D cuboid shape cast; serviced module excluded so the query measures tool access to its interface.' },
      oracle: { accessiblePathIds },
      visualization: visual(model, 'insertion-access', [model.taskConfig.serviceModule], 'side'),
    });

    const fault = await simulateJointFault(model, model.taskConfig.faultJoint);
    assert.equal(fault.failed, true, `${model.id}: fault must be observable`);
    const candidateJoints = [model.taskConfig.faultJoint,
      ...model.joints.filter(j => j.id !== model.taskConfig.faultJoint).slice(0, 2).map(j => j.id)];
    tasks.push({
      id: `m1-${model.id}-fault-recovery`, sourceGroup: model.id, kind: 'fault-recovery',
      capability: ['fault localization', 'causal diagnosis', 'minimum repair'],
      question: 'Identify the failed joint from the measured displacement and return the minimum certified recovery action sequence.',
      input: { model: summary, candidateJointIds: candidateJoints,
        observation: { childModule: fault.childModule, displacement: fault.displacement, tilt: fault.tilt },
        actionCatalog: [...model.taskConfig.recoveryActions, 'replace-unrelated-panel', 'restart-from-empty'] },
      oracle: { faultJointId: model.taskConfig.faultJoint, actions: model.taskConfig.recoveryActions },
      visualization: visual(model, 'fault-recovery', [fault.childModule]),
    });

    const feasible = paretoAlternatives(model);
    assert.equal(feasible.length, 1, `${model.id}: inventory answer`);
    tasks.push({
      id: `m1-${model.id}-inventory-substitution`, sourceGroup: model.id, kind: 'inventory-substitution',
      capability: ['finite inventory', 'structural substitution', 'constraint satisfaction'],
      question: 'A required brace is unavailable. Which listed replacement satisfies cost, piece-count and minimum-stiffness constraints?',
      input: { model: summary, alternatives: model.taskConfig.inventoryAlternatives,
        requirements: model.taskConfig.inventoryRequirements },
      oracle: { alternativeId: feasible[0].id },
      visualization: visual(model, 'inventory-substitution', [model.taskConfig.loadModule]),
    });

    const ladder = await simulateImpulseLadder(model);
    const safe = ladder.filter(row => row.safe);
    tasks.push({
      id: `m1-${model.id}-dynamic-robustness`, sourceGroup: model.id, kind: 'dynamic-robustness',
      capability: ['dynamic physical reasoning', 'impulse robustness', 'failure threshold estimation'],
      question: 'What is the largest tested impulse that stays within the declared transient and residual displacement limits?',
      input: { model: summary, targetModule: model.taskConfig.loadModule,
        impulseCandidates: model.taskConfig.impulseCandidates,
        limits: model.taskConfig.robustnessLimits,
        simulator: 'Rapier 3D, 120 Hz, 12 solver iterations, 2 internal PGS iterations' },
      oracle: { maxSafeImpulse: safe.at(-1)?.impulse ?? 0 },
      visualization: visual(model, 'dynamic-robustness', [model.taskConfig.loadModule]),
    });

    const functional = await simulateFunctionalMotion(model);
    tasks.push({
      id: `m1-${model.id}-functional-kinematics`, sourceGroup: model.id, kind: 'functional-kinematics',
      capability: ['joint semantics', 'functional prediction', 'kinematic reasoning'],
      question: 'Under motor actuation, does the designated revolute or prismatic mechanism achieve the required motion?',
      input: { model: summary, jointId: functional.jointId, jointType: functional.jointType,
        targetMotion: functional.target, passFraction: .55 },
      oracle: { jointId: functional.jointId, reachesTarget: functional.reachesTarget },
      visualization: visual(model, 'functional-kinematics',
        [model.joints.find(j => j.id === model.taskConfig.functionalJoint)!.child]),
    });

    const utilities = model.taskConfig.inspectionQueries.map(q => infoGain(model.taskConfig.hiddenWorlds, q));
    const best = Math.max(...utilities.map(row => row.efficiency));
    const bestQueries = utilities.filter(row => Math.abs(row.efficiency - best) < 1e-12).map(row => row.queryId);
    tasks.push({
      id: `m1-${model.id}-active-inspection`, sourceGroup: model.id, kind: 'active-inspection',
      capability: ['active perception', 'information gain', 'cost-aware clarification'],
      question: 'Which inspection should be requested next to maximize expected information gain per unit cost?',
      input: { model: summary, prior: 'uniform', hiddenWorlds: model.taskConfig.hiddenWorlds,
        queries: model.taskConfig.inspectionQueries },
      oracle: { queryIds: bestQueries },
      visualization: visual(model, 'active-inspection', [model.taskConfig.serviceModule], 'front'),
    });

    const pareto = paretoAll(model);
    tasks.push({
      id: `m1-${model.id}-multiobjective-design`, sourceGroup: model.id, kind: 'multiobjective-design',
      capability: ['Pareto reasoning', 'cost-mass-stiffness trade-off', 'engineering design'],
      question: 'Return every non-dominated buildable alternative under lower cost, lower mass and higher stiffness.',
      input: { model: summary, objectives: ['minimize cost', 'minimize mass', 'maximize stiffness'],
        alternatives: model.taskConfig.inventoryAlternatives },
      oracle: { paretoIds: pareto.map(c => c.id).sort() },
      visualization: visual(model, 'multiobjective-design', [model.taskConfig.loadModule], 'top'),
    });
  }
  assert.equal(tasks.length, 48);
  return tasks;
}
