import assert from 'node:assert/strict';
import { hierarchyModels } from './models';
import {
  ATOMIC_OPERATIONS,
  META_FAMILIES,
  type ChoiceOption,
  type HierarchyModel,
  type HierarchyTask,
  type QuestionFormat,
  type TaskLayer,
} from './types';

export const HIERARCHY_VERSION = 'brickatlas-hierarchy-1';
const IDS: ChoiceOption['id'][] = ['A', 'B', 'C', 'D'];

function unique(values: string[]) {
  return [...new Set(values)];
}

function singleChoice(correct: string, distractors: string[], seed: number) {
  const wrong = unique(distractors.filter(value => value !== correct));
  while (wrong.length < 3) wrong.push(`Unsupported alternative ${wrong.length + 1}`);
  const ordered = wrong.slice(0, 3);
  ordered.splice(seed % 4, 0, correct);
  const options = ordered.map((label, index) => ({ id: IDS[index], label }));
  return { options, oracle: { choiceId: options.find(option => option.label === correct)!.id } };
}

function multipleChoice(correct: string[], distractors: string[], seed: number) {
  const values = unique([...correct, ...distractors]).slice(0, 4);
  while (values.length < 4) values.push(`Unsupported alternative ${values.length + 1}`);
  const rotated = values.map((_, index) => values[(index + seed) % values.length]);
  const options = rotated.map((label, index) => ({ id: IDS[index], label }));
  return {
    options,
    oracle: {
      choiceIds: options.filter(option => correct.includes(option.label)).map(option => option.id).sort(),
    },
  };
}

function worldPosition(model: HierarchyModel, moduleId: string) {
  const module = model.modules.find(candidate => candidate.id === moduleId)!;
  const parts = model.parts.filter(part => part.moduleId === moduleId);
  return parts.reduce<[number, number, number]>((sum, part) => [
    sum[0] + (module.position[0] + part.position[0]) / parts.length,
    sum[1] + (module.position[1] + part.position[1]) / parts.length,
    sum[2] + (module.position[2] + part.position[2]) / parts.length,
  ], [0, 0, 0]);
}

function dominantColor(model: HierarchyModel, moduleId: string) {
  const counts = new Map<string, number>();
  for (const part of model.parts.filter(candidate => candidate.moduleId === moduleId)) {
    counts.set(part.color, (counts.get(part.color) ?? 0) + 1);
  }
  return [...counts].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0][0];
}

function incident(model: HierarchyModel, moduleId: string) {
  return model.joints.filter(joint => joint.parent === moduleId || joint.child === moduleId);
}

function descendants(model: HierarchyModel, moduleId: string) {
  const found = new Set<string>(), queue = [moduleId];
  while (queue.length) {
    const parent = queue.shift()!;
    for (const joint of model.joints.filter(candidate => candidate.parent === parent)) {
      if (!found.has(joint.child)) {
        found.add(joint.child);
        queue.push(joint.child);
      }
    }
  }
  return [...found];
}

function feasibleAlternative(model: HierarchyModel) {
  const requirements = model.taskConfig.inventoryRequirements;
  return model.taskConfig.inventoryAlternatives.filter(candidate =>
    candidate.cost <= requirements.maxCost
    && candidate.pieces <= requirements.maxPieces
    && candidate.stiffness >= requirements.minStiffness
    && candidate.jointMode !== 'none')
    .sort((a, b) => a.cost - b.cost || a.mass - b.mass)[0];
}

function paretoAlternatives(model: HierarchyModel) {
  const candidates = model.taskConfig.inventoryAlternatives.filter(candidate => candidate.jointMode !== 'none');
  return candidates.filter(candidate => !candidates.some(other => other.id !== candidate.id
    && other.cost <= candidate.cost
    && other.mass <= candidate.mass
    && other.stiffness >= candidate.stiffness
    && (other.cost < candidate.cost || other.mass < candidate.mass || other.stiffness > candidate.stiffness)));
}

function modelSummary(model: HierarchyModel) {
  return {
    id: model.id,
    name: model.name,
    difficulty: model.difficulty,
    family: model.family,
    description: model.description,
    complexity: model.complexity,
    modules: model.modules.map(module => ({
      id: module.id,
      name: module.name,
      role: module.role,
      anchored: module.anchored,
      visibleParts: model.parts.filter(part => part.moduleId === module.id).length,
    })),
    joints: model.joints.map(joint => ({
      id: joint.id,
      type: joint.type,
      parent: joint.parent,
      child: joint.child,
      axis: joint.axis,
      limits: joint.limits,
    })),
  };
}

function visualization(model: HierarchyModel, suffix: string, highlightModules: string[],
  view: HierarchyTask['visualization']['view'] = 'iso',
  extra: Partial<HierarchyTask['visualization']> = {}): HierarchyTask['visualization'] {
  return {
    modelImage: `images/models/${model.id}-iso.png`,
    detailImage: `images/tasks/${model.id}-${suffix}.png`,
    highlightModules,
    view,
    ...extra,
  };
}

function atomicPrompt(model: HierarchyModel, operation: string, seed: number) {
  const service = model.modules.find(module => module.id === model.taskConfig.serviceModule)!;
  const functional = model.joints.find(joint => joint.id === model.taskConfig.functionalJoint)!;
  const fault = model.joints.find(joint => joint.id === model.taskConfig.faultJoint)!;
  const moduleNames = model.modules.map(module => module.name);
  const targetParts = model.parts.filter(part => part.moduleId === service.id);
  const highest = [...model.modules].sort((a, b) => worldPosition(model, b.id)[1] - worldPosition(model, a.id)[1])[0];
  const anchored = model.modules.find(module => module.anchored)!;
  const parent = model.modules.find(module => module.id ===
    model.joints.find(joint => joint.child === service.id)?.parent) ?? anchored;
  const leaf = [...model.modules].reverse().find(module => !model.joints.some(joint => joint.parent === module.id))!;
  const nextIndex = Math.min(model.assemblyOrder.length - 1,
    Math.max(1, Math.floor(model.assemblyOrder.length / 2)));
  const next = model.modules.find(module => module.id === model.assemblyOrder[nextIndex])!;
  const feasible = feasibleAlternative(model);
  const common = {
    model: modelSummary(model),
    highlightedInterface: service.role,
    instruction: 'Use only the rendered highlight and the supplied structured evidence.',
  };
  const choices = (correct: string, distractors: string[], evidence: Record<string, unknown>,
    question: string, capability: string[]) => ({
    question,
    capability,
    input: { ...common, ...evidence },
    ...singleChoice(correct, distractors, seed),
    highlightModules: [service.id],
  });
  switch (operation) {
    case 'module-identification':
      return choices(service.name, moduleNames, {},
        'Which named module is highlighted?', ['part and module recognition', 'visual grounding']);
    case 'part-count':
      return choices(String(targetParts.length),
        [String(targetParts.length - 1), String(targetParts.length + 1), String(model.parts.length)],
        { target: 'highlighted rigid subassembly' },
        'How many visible pieces belong to the highlighted rigid subassembly?',
        ['counting', 'instance grouping']);
    case 'color-recognition': {
      const color = dominantColor(model, service.id);
      return choices(color, ['#d43a32', '#2878b8', '#f2bf3c', '#edf1f2'],
        { target: 'dominant color of highlighted subassembly' },
        'What is the dominant color of the highlighted subassembly?',
        ['color recognition', 'attribute grounding']);
    }
    case 'spatial-relation':
      return choices(highest.name, moduleNames,
        { relation: 'highest centroid in world Y', candidateModules: moduleNames },
        'Which candidate module has the highest geometric centroid?',
        ['3D spatial relation', 'multi-view correspondence']);
    case 'joint-motion':
      return choices(functional.type,
        ['fixed', 'revolute', 'prismatic', 'spring'],
        { joint: { id: functional.id, axis: functional.axis, limits: functional.limits } },
        'Which motion primitive is assigned to the designated joint?',
        ['joint recognition', 'kinematic semantics']);
    case 'connectivity':
      return choices(parent.name, moduleNames,
        { targetModule: service.name, relation: 'direct parent through one joint' },
        'Which module is the direct structural parent of the highlighted service module?',
        ['connectivity', 'attachment graph']);
    case 'support-anchor':
      return choices(anchored.name, moduleNames,
        { candidateModules: model.modules.map(module => module.name) },
        'Which module is directly anchored to the environment?',
        ['support recognition', 'grounding']);
    case 'contact-count': {
      const count = incident(model, service.id).length;
      return choices(String(count), [String(Math.max(0, count - 1)), String(count + 1), String(model.joints.length)],
        { targetModule: service.name, contactDefinition: 'incident declared joints' },
        'How many declared joints are incident on the highlighted module?',
        ['contact counting', 'topology']);
    }
    case 'recolor':
      return choices(`Recolor only ${service.name} to safety orange`,
        [`Recolor the whole object to safety orange`, `Delete ${service.name}`,
          `Recolor ${parent.name} and preserve ${service.name}`],
        { currentColor: dominantColor(model, service.id), requestedColor: '#e8792e' },
        'Which edit performs the requested local recolor without collateral changes?',
        ['instruction editing', 'recolor', 'change isolation']);
    case 'add':
      return choices(`Add the inspection beacon to ${service.name}'s free service interface`,
        [`Add it inside ${anchored.name}`, `Attach it across ${functional.id}`,
          'Add four copies to every module'],
        { requestedPart: 'inspection beacon', constraints: ['one copy', 'free interface', 'do not block moving joint'] },
        'Which addition obeys the placement and non-interference constraints?',
        ['part addition', 'interface selection', 'collision avoidance']);
    case 'remove':
      return choices(`Remove ${leaf.name} after isolating its direct joint`,
        [`Remove ${anchored.name} first`, `Remove every module`, `Remove ${parent.name} while loaded`],
        { candidateLeaf: leaf.name, dependencyChildren: descendants(model, leaf.id).length },
        'Which removal is locally executable without first dismantling a dependent child?',
        ['part removal', 'dependency reasoning']);
    case 'replace':
      return choices(feasible.label,
        model.taskConfig.inventoryAlternatives.map(candidate => candidate.label),
        { alternatives: model.taskConfig.inventoryAlternatives, requirements: model.taskConfig.inventoryRequirements },
        'Which replacement satisfies the finite inventory and stiffness requirements?',
        ['replacement', 'finite inventory', 'constraint checking']);
    case 'pose-correction':
      return choices('Translate (-1, 0, +1) and rotate -90 degrees about Y',
        ['Translate (+1, 0, -1) and rotate +90 degrees about Y', 'Recolor without moving',
          'Rotate 180 degrees about X'],
        { observedPoseError: { translation: [1, 0, -1], yawDegrees: 90 } },
        'Which local correction exactly inverts the observed pose error?',
        ['pose estimation', 'inverse transform']);
    case 'fault-localization':
      return choices(fault.id,
        model.joints.map(joint => joint.id),
        { symptom: { affectedChild: fault.child, lostConstraint: fault.type }, candidateJoints: model.joints.map(j => j.id) },
        'Which joint best explains the affected child and lost constraint?',
        ['fault localization', 'causal diagnosis']);
    case 'next-step':
      return choices(next.name,
        moduleNames,
        { completedPrefix: model.assemblyOrder.slice(0, nextIndex), candidateModules: moduleNames },
        'Which module is the next valid placement in the certified assembly order?',
        ['next-action prediction', 'assembly order']);
    case 'inventory-check':
      return choices(feasible.id,
        model.taskConfig.inventoryAlternatives.map(candidate => candidate.id),
        { stockCandidates: model.taskConfig.inventoryAlternatives, requirements: model.taskConfig.inventoryRequirements },
        'Which stock item is currently usable under all declared hard constraints?',
        ['inventory checking', 'resource constraints']);
    case 'subassembly-boundary':
      return choices(service.name,
        moduleNames,
        { targetRole: service.role, rigidBoundary: incident(model, service.id).map(joint => joint.id) },
        'Which candidate corresponds to the declared replaceable subassembly boundary?',
        ['subassembly segmentation', 'interface reasoning']);
    default:
      return choices('No operation; verify and preserve the current state',
        [`Recolor ${service.name}`, `Remove ${service.name}`, `Rebuild from empty`],
        { requestedState: { color: dominantColor(model, service.id), poseChange: [0, 0, 0] } },
        'The requested state already matches the current state. What is the minimum valid action?',
        ['no-op detection', 'minimal intervention']);
  }
}

function atomicTask(model: HierarchyModel, operation: string, seed: number, suffix: string): HierarchyTask {
  const generated = atomicPrompt(model, operation, seed);
  return {
    id: `h1-${model.id}-atomic-${suffix}`,
    sourceGroup: model.id,
    difficulty: model.difficulty,
    layer: 'atomic',
    format: 'single-choice',
    family: suffix === 'anchor' ? 'vertical-anchor-operation' : 'atomic-operation-coverage',
    operation,
    capability: generated.capability,
    question: generated.question,
    options: generated.options,
    input: generated.input,
    responseSchema: { choiceId: 'A | B | C | D' },
    oracle: generated.oracle,
    oracleMethod: 'exact authored model-state lookup',
    visualization: visualization(model, `atomic-${suffix}`, generated.highlightModules),
  };
}

function informationUtility(model: HierarchyModel) {
  const worlds = model.taskConfig.hiddenWorlds;
  return model.taskConfig.inspectionQueries.map(query => {
    const groups = new Map<string, number>();
    for (const world of worlds) groups.set(query.returns[world], (groups.get(query.returns[world]) ?? 0) + 1);
    const entropy = Math.log2(worlds.length);
    const residual = [...groups.values()].reduce((sum, count) => {
      const probability = count / worlds.length;
      return sum + probability * Math.log2(count);
    }, 0);
    return { query, gain: entropy - residual, utility: (entropy - residual) / query.cost };
  });
}

function metaPrompt(model: HierarchyModel, family: string, seed: number) {
  const level = Number(model.difficulty.slice(1));
  const root = model.modules.find(module => module.anchored)!;
  const firstChild = model.joints.find(joint => joint.parent === root.id)?.child
    ?? model.modules.find(module => !module.anchored)!.id;
  const functional = model.joints.find(joint => joint.id === model.taskConfig.functionalJoint)!;
  const fault = model.joints.find(joint => joint.id === model.taskConfig.faultJoint)!;
  const summary = modelSummary(model);
  if (family === 'prefix-stability') {
    const valid = model.assemblyOrder.slice(0, Math.min(model.assemblyOrder.length, 3 + level * 2));
    const invalid = [valid.at(-1)!, ...valid.slice(0, -1)];
    const selected = singleChoice('root-to-leaf plan', ['leaf-first plan', 'reverse plan', 'random plan'], seed);
    return {
      format: 'single-choice' as QuestionFormat,
      question: 'Which candidate preserves a supported dependency prefix after every placement?',
      capability: ['prefix stability', 'causal support', 'calibrated physical reasoning'],
      options: selected.options,
      oracle: selected.oracle,
      input: { model: summary, candidates: { 'root-to-leaf plan': valid, 'leaf-first plan': invalid,
        'reverse plan': [...valid].reverse(), 'random plan': [...valid.slice(1), valid[0]] } },
      oracleMethod: 'joint dependency graph enumeration',
      highlight: [firstChild],
    };
  }
  if (family === 'assembly-accessibility') {
    const clearances = [0.6, -0.25, 0.18, -0.1].map(value => Number((value - (level - 1) * 0.02).toFixed(2)));
    const labels = model.taskConfig.accessPaths.map(path => path.label);
    while (labels.length < 4) labels.push(`Alternative service path ${labels.length + 1}`);
    const correct = labels.filter((_, index) => clearances[index] > 0);
    const selected = multipleChoice(correct, labels.filter(label => !correct.includes(label)), seed);
    return {
      format: 'multiple-choice' as QuestionFormat,
      question: 'Select every service path whose minimum swept-volume clearance is strictly positive.',
      capability: ['assembly accessibility', 'continuous collision reasoning', 'set-valued decisions'],
      options: selected.options,
      oracle: selected.oracle,
      input: { model: summary, pathEvidence: labels.map((label, index) => ({ label, minClearance: clearances[index] })),
        convention: 'positive is collision-free; zero or negative collides' },
      oracleMethod: 'swept-volume clearance threshold',
      highlight: [model.taskConfig.serviceModule],
      accessPaths: model.taskConfig.accessPaths.slice(0, 3).map((path, index) => ({
        start: path.end.map((value, axis) =>
          value + (path.start[axis] - value) * 0.35) as [number, number, number],
        end: path.end,
        accessible: clearances[index] > 0,
      })),
    };
  }
  if (family === 'support-counterfactual') {
    const removed = firstChild;
    const affected = [removed, ...descendants(model, removed)];
    const candidates = unique([...affected, ...model.modules.map(module => module.id)]).slice(0, 4);
    const correct = candidates.filter(id => affected.includes(id));
    const selected = multipleChoice(correct, candidates.filter(id => !affected.includes(id)), seed);
    return {
      format: 'multiple-choice' as QuestionFormat,
      question: 'If the declared support interface is removed, which listed modules lose their certified support path?',
      capability: ['counterfactual support', 'dependency closure', 'set-valued prediction'],
      options: selected.options,
      oracle: selected.oracle,
      input: { model: summary, removedModule: removed, supportEdges: model.joints.map(joint => [joint.parent, joint.child]) },
      oracleMethod: 'directed support-graph transitive closure',
      highlight: [removed],
    };
  }
  if (family === 'dynamic-robustness') {
    const impulses = [10, 25, 50, 90].map(value => value * level);
    const transientLimit = Number((1.1 / level).toFixed(3));
    const residualLimit = Number((0.38 / level).toFixed(3));
    const trace = impulses.map((impulse, index) => ({
      impulse,
      maxTransient: Number((transientLimit * [0.32, 0.78, 1.08, 1.9][index]).toFixed(3)),
      residual: Number((residualLimit * [0.25, 0.82, 1.18, 2.1][index]).toFixed(3)),
    }));
    const selected = singleChoice(String(impulses[1]), impulses.map(String), seed);
    return {
      format: 'single-choice' as QuestionFormat,
      question: 'What is the largest tested impulse satisfying both transient and residual motion limits?',
      capability: ['dynamic robustness', 'threshold estimation', 'multi-criterion checking'],
      options: selected.options,
      oracle: selected.oracle,
      input: { model: summary, targetModule: model.taskConfig.loadModule,
        limits: { maxTransient: transientLimit, maxResidual: residualLimit }, responseTrace: trace,
        evidenceClass: 'frozen parameterized load-envelope trace' },
      oracleMethod: 'two-threshold response-table evaluation',
      highlight: [model.taskConfig.loadModule],
      force: { moduleId: model.taskConfig.loadModule, vector: [3 + level, 0.7, 1.2] as [number, number, number] },
    };
  }
  if (family === 'functional-kinematics') {
    const statement = functional.type === 'prismatic'
      ? `translate along ${JSON.stringify(functional.axis)} within ${JSON.stringify(functional.limits)}`
      : `rotate about ${JSON.stringify(functional.axis)} within ${JSON.stringify(functional.limits)}`;
    const selected = singleChoice(statement, [
      'remain fixed under all commands',
      'translate freely along every axis',
      'rotate without a declared axis or limit',
    ], seed);
    return {
      format: 'single-choice' as QuestionFormat,
      question: 'Which motion statement is consistent with the designated functional joint?',
      capability: ['functional kinematics', 'joint semantics', 'axis and limit reasoning'],
      options: selected.options,
      oracle: selected.oracle,
      input: { model: summary, functionalJoint: functional },
      oracleMethod: 'declared joint contract',
      highlight: [functional.child],
    };
  }
  if (family === 'fault-diagnosis') {
    const selected = singleChoice(fault.id, model.joints.map(joint => joint.id), seed);
    return {
      format: 'single-choice' as QuestionFormat,
      question: 'Which joint is the unique causal match for the observed child motion and lost constraint?',
      capability: ['fault diagnosis', 'causal localization', 'mechanism topology'],
      options: selected.options,
      oracle: selected.oracle,
      input: { model: summary, observation: { displacedChild: fault.child, lostMode: fault.type,
        upstreamModulesStable: true }, candidateJoints: model.joints.map(joint => joint.id) },
      oracleMethod: 'joint-to-child causal matching',
      highlight: [fault.child],
    };
  }
  if (family === 'active-inspection') {
    const utilities = informationUtility(model);
    const best = [...utilities].sort((a, b) => b.utility - a.utility || a.query.id.localeCompare(b.query.id))[0];
    const selected = singleChoice(best.query.label,
      model.taskConfig.inspectionQueries.map(query => query.label), seed);
    return {
      format: 'single-choice' as QuestionFormat,
      question: 'Which next inspection maximizes expected information gain per unit cost?',
      capability: ['active inspection', 'information gain', 'cost-aware metacognition'],
      options: selected.options,
      oracle: selected.oracle,
      input: { model: summary, prior: 'uniform', worlds: model.taskConfig.hiddenWorlds,
        queries: model.taskConfig.inspectionQueries },
      oracleMethod: 'finite-world entropy reduction divided by query cost',
      highlight: [model.taskConfig.serviceModule],
    };
  }
  if (family === 'uncertainty-calibration') {
    const selected = singleChoice('Request the discriminating inspection before acting', [
      'Commit to nominal repair with confidence 1.0',
      'Rebuild the complete object immediately',
      'Ignore the unresolved hidden interface',
    ], seed);
    return {
      format: 'single-choice' as QuestionFormat,
      question: 'Two hidden worlds remain action-incompatible under the current observation. What is the calibrated response?',
      capability: ['uncertainty calibration', 'abstention', 'clarification policy'],
      options: selected.options,
      oracle: selected.oracle,
      input: { model: summary, consistentWorlds: ['nominal', 'jammed'],
        actionByWorld: { nominal: 'continue', jammed: 'isolate-and-repair' }, inspectionAvailable: true },
      oracleMethod: 'possible-world action-consistency check',
      highlight: [model.taskConfig.serviceModule],
    };
  }
  const pareto = paretoAlternatives(model);
  const labels = model.taskConfig.inventoryAlternatives.map(candidate => candidate.label);
  const correct = pareto.map(candidate => candidate.label);
  const selected = multipleChoice(correct, labels.filter(label => !correct.includes(label)), seed);
  return {
    format: 'multiple-choice' as QuestionFormat,
    question: 'Select every non-dominated buildable alternative under lower cost, lower mass, and higher stiffness.',
    capability: ['Pareto reasoning', 'multi-objective trade-off', 'engineering metacognition'],
    options: selected.options,
    oracle: selected.oracle,
    input: { model: summary, alternatives: model.taskConfig.inventoryAlternatives,
      objectives: ['minimize cost', 'minimize mass', 'maximize stiffness'] },
    oracleMethod: 'complete Pareto-set enumeration',
    highlight: [model.taskConfig.loadModule],
  };
}

function metaTask(model: HierarchyModel, family: string, seed: number): HierarchyTask {
  const generated = metaPrompt(model, family, seed);
  return {
    id: `h1-${model.id}-meta`,
    sourceGroup: model.id,
    difficulty: model.difficulty,
    layer: 'metacognitive',
    format: generated.format,
    family,
    capability: generated.capability,
    question: generated.question,
    options: generated.options,
    input: generated.input,
    responseSchema: generated.format === 'multiple-choice'
      ? { choiceIds: ['one or more of A | B | C | D'] }
      : { choiceId: 'A | B | C | D' },
    oracle: generated.oracle,
    oracleMethod: generated.oracleMethod,
    visualization: visualization(model, 'meta', generated.highlight, family === 'assembly-accessibility' ? 'side' : 'iso', {
      accessPaths: generated.accessPaths,
      force: generated.force,
    }),
  };
}

function boundedActions(actions: string[], level: number) {
  const target = Math.min(actions.length, 2 + level * 2);
  return actions.slice(0, target);
}

function proceduralTask(model: HierarchyModel, seed: number): HierarchyTask {
  const level = Number(model.difficulty.slice(1));
  const variant = seed % 6;
  const service = model.taskConfig.serviceModule;
  const feasible = feasibleAlternative(model).id;
  let family = '';
  let question = '';
  let actions: string[] = [];
  let input: Record<string, unknown> = {};
  let capability: string[] = [];
  if (variant === 0) {
    family = 'assembly-sequencing';
    actions = boundedActions(model.assemblyOrder.map(id => `place:${id}`), level);
    question = 'Return a complete placement sequence that satisfies every declared dependency in the requested build prefix.';
    input = { requestedPrefixLength: actions.length, availableModules: model.assemblyOrder,
      dependencyEdges: model.joints.map(joint => [joint.parent, joint.child]) };
    capability = ['assembly planning', 'ordering', 'prefix validity'];
  } else if (variant === 1) {
    family = 'safe-disassembly';
    actions = boundedActions([...model.assemblyOrder].reverse().map(id => `remove:${id}`), level);
    question = 'Return a complete safe removal sequence; independent modules may be ordered either way.';
    input = { requestedRemovalCount: actions.length, dependencyEdges: model.joints.map(joint => [joint.parent, joint.child]),
      rule: 'children before parents' };
    capability = ['disassembly planning', 'dependency reversal', 'safe removal'];
  } else if (variant === 2) {
    family = 'edit-then-verify';
    actions = boundedActions([
      `isolate:${service}`,
      `recolor:${service}:safety-orange`,
      `restore:${service}`,
      'verify:no-collateral-change',
      'verify:function',
      'release:service-zone',
    ], level);
    question = 'Return the minimum ordered actions for a local recolor followed by state verification.';
    input = { targetModule: service, requestedColor: 'safety-orange',
      constraints: ['preserve all other modules', 'verify structure and function'] };
    capability = ['instruction execution', 'local editing', 'postcondition verification'];
  } else if (variant === 3) {
    family = 'fault-recovery';
    actions = boundedActions(model.taskConfig.recoveryActions, level);
    question = 'Return the minimum certified recovery sequence for the declared failed joint.';
    input = { failedJoint: model.taskConfig.faultJoint, serviceModule: service,
      actionCatalog: [...model.taskConfig.recoveryActions, 'restart-from-empty', 'replace-unrelated-panel'] };
    capability = ['fault recovery', 'minimal repair', 'action sequencing'];
  } else if (variant === 4) {
    family = 'inventory-replan';
    actions = boundedActions([
      'inspect:stock',
      `select:${feasible}`,
      `isolate:${model.taskConfig.loadModule}`,
      `install:${feasible}`,
      'verify:stiffness',
      'release:load',
    ], level);
    question = 'Return the ordered stockout-recovery actions using the only feasible replacement.';
    input = { unavailable: 'original-brace', alternatives: model.taskConfig.inventoryAlternatives,
      requirements: model.taskConfig.inventoryRequirements };
    capability = ['inventory replanning', 'structural substitution', 'constraint-preserving execution'];
  } else {
    const best = [...informationUtility(model)].sort((a, b) => b.utility - a.utility)[0].query.id;
    family = 'inspect-diagnose-act';
    actions = boundedActions([
      `inspect:${best}`,
      'interpret:observation',
      `isolate:${service}`,
      `repair:${model.taskConfig.faultJoint}`,
      'verify:function',
      'close:service-interface',
    ], level);
    question = 'Return the ordered inspect-diagnose-act sequence; acting before inspection is invalid.';
    input = { hiddenWorlds: model.taskConfig.hiddenWorlds, queries: model.taskConfig.inspectionQueries,
      faultCandidate: model.taskConfig.faultJoint };
    capability = ['active inspection', 'conditional planning', 'execution discipline'];
  }
  const catalog = unique([...actions, 'restart:empty', 'skip:verification', 'modify:unrelated-module']);
  return {
    id: `h1-${model.id}-procedural`,
    sourceGroup: model.id,
    difficulty: model.difficulty,
    layer: 'procedural',
    format: 'ordered-actions',
    family,
    capability,
    question,
    input: { model: modelSummary(model), ...input, actionCatalog: catalog },
    responseSchema: { actionIds: ['string in exact execution order'] },
    oracle: { actionIds: actions },
    oracleMethod: 'state-transition and dependency contract',
    visualization: visualization(model, 'procedural',
      unique([service, model.taskConfig.loadModule]), 'front'),
  };
}

function integrativeTask(model: HierarchyModel, seed: number): HierarchyTask {
  const level = Number(model.difficulty.slice(1));
  const feasible = feasibleAlternative(model);
  const bestQuery = [...informationUtility(model)].sort((a, b) => b.utility - a.utility)[0].query.id;
  const correctPlan = {
    id: `P${seed % 4 + 1}`,
    inspection: bestQuery,
    substitute: feasible.id,
    isolatesLoad: true,
    preservesAccess: true,
    residualRisk: Number((0.08 / level).toFixed(3)),
    steps: 3 + level * 2,
    verification: 'load-and-function-proof',
  };
  const plans = [
    correctPlan,
    { ...correctPlan, id: `P${(seed + 1) % 4 + 1}`, inspection: 'none', residualRisk: 0.45 },
    { ...correctPlan, id: `P${(seed + 2) % 4 + 1}`, substitute: 'fairing', residualRisk: 0.7 },
    { ...correctPlan, id: `P${(seed + 3) % 4 + 1}`, preservesAccess: false, steps: 2 },
  ].sort((a, b) => a.id.localeCompare(b.id));
  const scenarioFamilies = [
    'diagnose-access-repair',
    'inventory-robustness',
    'inspect-plan-execute',
    'multiobjective-maintenance',
    'compound-edit-verification',
    'multi-station-scheduling',
  ];
  const family = scenarioFamilies[seed % scenarioFamilies.length];
  return {
    id: `h1-${model.id}-integrative`,
    sourceGroup: model.id,
    difficulty: model.difficulty,
    layer: 'integrative',
    format: 'structured-plan',
    family,
    capability: [
      'cross-capability integration',
      'resource-aware planning',
      'risk control',
      'verification',
      ...(level >= 3 ? ['long-horizon coordination', 'hidden-state management'] : []),
    ],
    question: 'Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.',
    input: {
      model: modelSummary(model),
      scenario: family,
      constraints: [
        'use the highest information-gain-per-cost inspection',
        `replacement cost <= ${model.taskConfig.inventoryRequirements.maxCost}`,
        `replacement stiffness >= ${model.taskConfig.inventoryRequirements.minStiffness}`,
        'isolate the load before intervention',
        'preserve a service access path',
        `residual risk <= ${Number((0.1 / level).toFixed(3))}`,
        'finish with load and function proof',
      ],
      candidatePlans: plans,
    },
    responseSchema: { planId: 'P1 | P2 | P3 | P4', verificationId: 'string' },
    oracle: { planId: correctPlan.id, verificationId: correctPlan.verification },
    oracleMethod: 'complete hard-constraint plan filtering',
    visualization: visualization(model, 'integrative',
      unique([model.taskConfig.serviceModule, model.taskConfig.loadModule]), 'top', {
        force: { moduleId: model.taskConfig.loadModule, vector: [3 + level, 0.7, 1.2] },
      }),
  };
}

const ANCHOR_OPERATIONS = [
  'module-identification',
  'spatial-relation',
  'recolor',
  'fault-localization',
  'support-anchor',
  'pose-correction',
];

let cache: HierarchyTask[] | undefined;
export function hierarchyTasks() {
  if (cache) return cache;
  const models = hierarchyModels(), tasks: HierarchyTask[] = [];
  for (const [index, model] of models.entries()) {
    const sameLevel = models.filter(candidate => candidate.difficulty === model.difficulty);
    const localIndex = sameLevel.findIndex(candidate => candidate.id === model.id);
    tasks.push(atomicTask(model, ANCHOR_OPERATIONS[localIndex % ANCHOR_OPERATIONS.length],
      index, 'anchor'));
    tasks.push(atomicTask(model, ATOMIC_OPERATIONS[index], index + 1, 'coverage'));
    tasks.push(metaTask(model, META_FAMILIES[index % META_FAMILIES.length], index));
    tasks.push(proceduralTask(model, index));
    tasks.push(integrativeTask(model, index));
  }
  assert.equal(tasks.length, 90);
  assert.equal(new Set(tasks.map(task => task.id)).size, tasks.length);
  assert.equal(new Set(tasks.filter(task => task.family === 'atomic-operation-coverage')
    .map(task => task.operation)).size, ATOMIC_OPERATIONS.length);
  cache = tasks;
  return tasks;
}

export function pilotSelection(tasks = hierarchyTasks()) {
  const selected: HierarchyTask[] = [];
  const difficulties = ['D1', 'D2', 'D3', 'D4'] as const;
  const layers: TaskLayer[] = ['atomic', 'metacognitive', 'procedural', 'integrative'];
  for (const [difficultyIndex, difficulty] of difficulties.entries()) {
    for (const [layerIndex, layer] of layers.entries()) {
      const candidates = tasks.filter(task => task.difficulty === difficulty && task.layer === layer);
      selected.push(candidates[(difficultyIndex + layerIndex) % candidates.length]);
    }
  }
  assert.equal(selected.length, 16);
  return selected;
}
