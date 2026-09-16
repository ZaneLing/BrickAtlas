import { createHash } from 'node:crypto';
import type { Task, Action } from '../../../src/benchmark/types';
import { solveActions, score } from '../../../src/benchmark/engine';
import type { Model } from './models';
import { geometry, physicsEvidence } from './physics';
import { advancedTasks, EXTRA_ATOMIC, EXTRA_META, EXTRA_TITLES } from './advanced';

export const VERSION = 'brickatlas-hierarchy-3';
export const ATOMIC = ['identify', 'count', 'color', 'position', 'joint-type', 'parent', 'anchor',
  'degree', 'recolor', 'add', 'remove', 'replace', 'translate', 'rotate', 'next-module', 'inventory',
  'boundary', 'no-op', ...EXTRA_ATOMIC];
export const META = ['prefix', 'access', 'counterfactual', 'dynamic', 'kinematic', 'diagnosis',
  'information-gain', 'abstention', 'posterior', 'pareto', ...EXTRA_META];
export const TITLES: Record<string, string> = {
  ...EXTRA_TITLES,
  identify: '模块识别', count: '部件计数', color: '颜色识别', position: '三维位置',
  'joint-type': '关节类型', parent: '直接连接', anchor: '基座识别', degree: '接口计数',
  recolor: '局部改色', add: '补装部件', remove: '安全拆除', replace: '替换选择',
  translate: '平移纠偏', rotate: '姿态纠偏', 'next-module': '下一步放置',
  inventory: '库存核算', boundary: '子装配边界', 'no-op': '最小干预',
  prefix: '全过程依赖', access: '连续维修路径', counterfactual: '支撑反事实',
  dynamic: '冲击响应读数', kinematic: '关节限位推理', diagnosis: '约束故障诊断',
  'information-gain': '主动检查收益', abstention: '不确定性与弃答', posterior: '观测后信念更新',
  pareto: '多目标工程权衡', assembly: '依赖装配', disassembly: '依赖拆解',
  'service-repair': '承载维修', 'compound-edit': '复合编辑验证',
  'multi-fault': '跨区域联合维修', scheduling: '多工位资源调度', policy: '检查后条件策略',
};
const labels = ['A', 'B', 'C', 'D'];
const seedOf = (id: string) => createHash('sha256').update(id).digest().readUInt32LE(0);
const encoded = (v: any) => JSON.stringify(v);

const SET_FAMILIES = new Set(['parent', 'anchor', 'remove', 'next-module', 'boundary', 'counterfactual']);
export function semanticKey(task: Pick<Task, 'family'>, value: any): string {
  if (SET_FAMILIES.has(task.family) && Array.isArray(value)) return encoded([...new Set(value)].sort());
  if (value && typeof value === 'object' && !Array.isArray(value))
    return encoded(Object.fromEntries(Object.keys(value).sort().map(k => [k, value[k]])));
  return encoded(value);
}
export function choice(task: Task, correct: any[], wrong: any[], multi = false) {
  const key = (v: any) => semanticKey(task, v);
  const entries = [...correct, ...wrong].filter((v, i, a) => a.findIndex(x => key(x) === key(v)) === i);
  if (!multi && entries.length < 2) throw new Error(`No contrast: ${task.id}`);
  // Keep the complete correct set; at most four choices for numeric/local questions.
  const values = multi ? entries : entries.slice(0, 4);
  const offset = seedOf(task.id) % values.length;
  const rotated = values.map((_, i) => values[(i + offset) % values.length]);
  task.options = rotated.map((value, i) => ({ id: labels[i] ?? `O${i + 1}`, value,
    label: typeof value === 'string' ? value : encoded(value) }));
  const ids = task.options.filter(o => correct.some(v => key(v) === key(o.value))).map(o => o.id);
  if (!multi && ids.length !== 1) throw new Error(`Ambiguous single-choice: ${task.id}`);
  task.format = multi ? 'multiple-choice' : 'single-choice';
  task.answer = multi ? { choiceIds: ids } : { choiceId: ids[0] };
  return task;
}

function rootConnected(model: Model, removed = new Set<string>()) {
  const found = new Set(model.modules.filter(m => m.anchored && !removed.has(m.id)).map(m => m.id));
  for (let i = 0; i < model.modules.length; i++) for (const j of model.joints) {
    if (removed.has(j.parent) || removed.has(j.child)) continue;
    if (found.has(j.parent)) found.add(j.child);
    if (found.has(j.child)) found.add(j.parent);
  }
  return [...found].sort();
}

function contract(model: Model, kind: string): Pick<Task, 'input' | 'answer'> {
  const ids = model.modules.map(m => m.id), actions: Action[] = [];
  const initialFacts: string[] = [], goalFacts: string[] = [], initialModules: string[] = [];
  const add = (a: Action) => actions.push(a);
  if (kind === 'assembly' || kind === 'disassembly') {
    if (kind === 'disassembly') { initialModules.push(...ids); initialFacts.push(...ids.map(id => `present:${id}`)); }
    for (const id of kind === 'assembly' ? model.assemblyOrder : [...model.assemblyOrder].reverse()) {
      const predecessors = model.joints.filter(j => kind === 'assembly' ? j.child === id : j.parent === id)
        .map(j => kind === 'assembly' ? j.parent : j.child);
      if (kind === 'assembly') {
        add({ id: `place:${id}`, label: `安装 ${id}`, requires: predecessors.map(p => `present:${p}`),
          forbids: [`present:${id}`], adds: [`present:${id}`], deletes: [], cost: 1,
          visual: { moduleId: id, visible: true } });
        goalFacts.push(`present:${id}`);
      } else {
        add({ id: `remove:${id}`, label: `拆除 ${id}`, requires: [`present:${id}`],
          forbids: predecessors.map(p => `present:${p}`), adds: [`removed:${id}`], deletes: [`present:${id}`],
          cost: 1, visual: { moduleId: id, visible: false } });
        goalFacts.push(`removed:${id}`);
      }
    }
  } else {
    initialModules.push(...ids);
    const targets = kind === 'multi-fault'
      ? model.modules.filter(m => !m.anchored).slice(-Number(model.difficulty[1]))
      : [model.modules.find(m => m.id === model.taskConfig.serviceModule)!];
    for (const m of targets) {
      const id = m.id; initialFacts.push(`fault:${id}`, `closed:${id}`);
      const stages = kind === 'compound-edit'
        ? ['support', 'open', 'recolor', 'verify', 'close', 'release']
        : ['support', 'open', 'remove', 'replace', 'verify', 'close', 'release'];
      for (const [i, op] of stages.entries()) {
        const name = `${op}:${id}`;
        add({ id: name, label: `${op} ${id}`,
          requires: i ? [`done:${stages[i - 1]}:${id}`] : [`fault:${id}`],
          forbids: [`done:${op}:${id}`],
          adds: [`done:${op}:${id}`, ...(op === 'release' ? [`repaired:${id}`] : [])],
          deletes: op === 'verify' ? [`fault:${id}`] : [],
          cost: 1, visual: { moduleId: id, ...(op === 'remove' ? { visible: false } : {}),
            ...(op === 'replace' ? { visible: true } : {}),
            ...(op === 'recolor' ? { color: '#ea7635' } : {}) } });
      }
      goalFacts.push(`repaired:${id}`);
    }
  }
  // Randomized catalog order prevents copying the displayed action list.
  actions.sort((a, b) => seedOf(`${model.id}:${a.id}`) - seedOf(`${model.id}:${b.id}`));
  const input = { initialFacts, initialModules, actions, goalFacts, budget: actions.length,
    semantics: 'requires must hold; forbids must be absent; effects apply in order; unit action cost' };
  const provisional = { format: 'actions', input } as unknown as Task;
  const answer = solveActions(provisional);
  if (!score(provisional, answer).success) throw new Error(`Unsolvable contract ${model.id} ${kind}`);
  return { input, answer };
}

export async function modelTasks(model: Model) {
  const evidence = await physicsEvidence(model);
  const geo = geometry(model), moduleIds = model.modules.map(m => m.id);
  const service = model.taskConfig.serviceModule, parts = model.parts.filter(p => p.moduleId === service);
  const joint = model.joints.find(j => j.id === model.taskConfig.functionalJoint)!;
  const parents = (id: string) => [...new Set(model.joints.filter(j => j.child === id).map(j => j.parent))].sort();
  const summary = { modules: model.modules, joints: model.joints,
    parts: model.parts.map(p => ({ id: p.id, moduleId: p.moduleId, shape: p.shape, color: p.color })),
    centers: geo.centers };
  const task = (layer: Task['layer'], family: string, question: string, evidenceType: Task['evidence'] = 'model-state'): Task => ({
    id: `h3-${model.id}-${family}`, modelId: model.id, difficulty: model.difficulty, layer, family,
    title: TITLES[family], question, capabilities: [TITLES[family]], format: 'single-choice',
    input: {}, answer: {}, targetModule: service, evidence: evidenceType,
  });
  const rows: Task[] = [];
  const atom = (family: string, question: string, correct: any, wrong: any[], input: any = {}) => {
    const t = task('atomic', family, question); t.input = input;
    rows.push(choice(t, [correct], wrong));
  };
  atom('identify', '高亮的维修模块对应哪个 ID？', service, moduleIds, { moduleNames: model.modules.map(m => ({ id: m.id, name: m.name })) });
  atom('count', `模块 ${service} 有多少个可视零件？`, parts.length, [parts.length + 1, Math.max(0, parts.length - 1), parts.length + 3], { parts: summary.parts });
  atom('color', `零件 ${parts[0].id} 的颜色值是什么？`, parts[0].color, ['#2878b8', '#d43a32', '#f2bf3c', '#26323b'], { part: parts[0] });
  atom('position', `模块 ${service} 的世界包围盒中心是什么？`, geo.centers[service],
    moduleIds.filter(id => id !== service).map(id => geo.centers[id]).concat([[999, 999, 999]]), { centers: geo.centers });
  atom('joint-type', `${joint.id} 采用什么约束类型？`, joint.type, ['fixed', 'revolute', 'prismatic', 'spring'], { joint });
  atom('parent', `${service} 的直接父模块集合是什么？`, parents(service), [[service], [], moduleIds], { joints: summary.joints });
  const roots = model.modules.filter(m => m.anchored).map(m => m.id).sort();
  atom('anchor', '哪些模块被声明为固定基座？', roots, [[], moduleIds, [service]], { modules: summary.modules });
  const degree = model.joints.filter(j => j.parent === service || j.child === service).length;
  atom('degree', `${service} 连接几个声明关节？平行关节分别计数。`, degree, [degree + 1, Math.max(0, degree - 1), degree + 2], { joints: summary.joints });
  atom('recolor', `仅将 ${parts[0].id} 改成 #e8792e，其他零件不变。选择正确补丁。`,
    { id: parts[0].id, color: '#e8792e' }, [{ id: parts[1]?.id ?? service, color: '#e8792e' },
      { id: parts[0].id, color: '#2878b8' }, { id: '*', color: '#e8792e' }], { part: parts[0] });
  atom('add', `模块 ${service} 缺失零件 ${parts[0].id}。选择与目标清单一致的补装描述。`, parts[0],
    [{ ...parts[0], moduleId: moduleIds.find(id => id !== service) }, { ...parts[0], size: [3, 3, 3] },
      { ...parts[0], color: '#000000' }], { targetPart: parts[0], existingIds: model.parts.filter(p => p.id !== parts[0].id).map(p => p.id) });
  const leaves = moduleIds.filter(id => !model.joints.some(j => j.parent === id)).sort();
  atom('remove', '按声明依赖图，当前可以先拆哪些叶模块？', leaves, [roots, [], moduleIds], { joints: summary.joints, modules: moduleIds });
  const seed = seedOf(model.id);
  const alternatives = [0, 1, 2, 3].map(i => ({ id: `stock-${i}`, cost: 2 + (seedOf(`${model.id}:cost:${i}`) % 7),
    stiffness: 3 + (seedOf(`${model.id}:stiff:${i}`) % 9), mass: 0.5 + (seedOf(`${model.id}:mass:${i}`) % 15) / 10 }));
  const limit = 6 + seed % 3;
  const feasible = alternatives.filter(a => a.cost <= limit);
  if (!feasible.length) alternatives[0].cost = 2;
  const selected = alternatives.filter(a => a.cost <= limit).sort((a, b) => b.stiffness - a.stiffness
    || a.cost - b.cost || a.id.localeCompare(b.id))[0];
  atom('replace', '在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。', selected.id, alternatives.map(a => a.id), { alternatives, maxCost: limit });
  const delta = [Number(model.difficulty[1]), 0, -2];
  atom('translate', '观察到相对目标的平移误差 delta，选择补偿平移。', delta.map(n => n ? -n : 0),
    [delta, [0, 0, 0], [0, 2, 0]], { delta, target: service });
  const currentYaw = (seed % 8) * 45, targetYaw = ((seed >>> 4) % 8) * 45;
  const yawDelta = ((targetYaw - currentYaw + 540) % 360) - 180;
  atom('rotate', '选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。', yawDelta,
    [-yawDelta, 0, 90, -90, -180], { module: service, currentYaw, targetYaw });
  const prefix = model.assemblyOrder.slice(0, Math.ceil(moduleIds.length / 2));
  const next = moduleIds.filter(id => !prefix.includes(id) && parents(id).every(p => prefix.includes(p))).sort();
  atom('next-module', '已完成给定前缀，选择所有前置依赖已满足的下一模块集合。', next,
    [[], prefix, moduleIds.filter(id => !prefix.includes(id))].concat([[roots[0]]]),
    { prefix, joints: summary.joints, modules: moduleIds });
  const surplus = seed % 9;
  atom('inventory', `备件库有 ${parts.length + surplus} 件，替换模块需 ${parts.length} 件，还剩多少？`, surplus,
    [surplus + 1, Math.max(0, surplus - 1), surplus + 3], { available: parts.length + surplus, required: parts.length });
  const boundary = model.joints.filter(j => j.parent === service || j.child === service).map(j => j.id).sort();
  atom('boundary', `隔离 ${service} 需要断开哪些边界关节？`, boundary, [[], model.joints.map(j => j.id), [joint.id]],
    { joints: summary.joints, target: service });
  atom('no-op', '当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？', 0, [1, 2, parts.length], { module: service });

  const meta = (family: string, question: string, good: any[], bad: any[], input: any,
    type: Task['evidence'], multi = false) => {
    const t = task('metacognitive', family, question, type); t.input = input;
    rows.push(choice(t, good, bad, multi));
  };
  const badOrder = [...model.assemblyOrder];
  if (seed % 5) {
    const target = model.assemblyOrder.filter(id => parents(id).length)[seed % (moduleIds.length - roots.length)];
    const parentIndex = badOrder.findIndex(id => parents(target).includes(id));
    badOrder.splice(badOrder.indexOf(target), 1); badOrder.splice(parentIndex, 0, target);
  }
  const invalidAt = badOrder.findIndex((id, i) => parents(id).some(p => !badOrder.slice(0, i).includes(p)));
  meta('prefix', '给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。', [invalidAt],
    [-1, invalidAt + 1, badOrder.length - 1], { order: badOrder, joints: summary.joints }, 'support-graph');
  meta('access', '根据实际 Rapier shape cast 记录，选择全部无碰撞路径。', evidence.paths.filter(p => p.clear).map(p => p.id),
    evidence.paths.filter(p => !p.clear).map(p => p.id), { paths: evidence.paths, simulator: evidence.scope }, 'Rapier', true);
  const removed = moduleIds.find(id => parents(id).length && model.joints.some(j => j.parent === id)) ?? service;
  const connected = rootConnected(model, new Set([removed]));
  const lost = moduleIds.filter(id => id !== removed && !connected.includes(id));
  meta('counterfactual', '移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。',
    [lost.sort()], [[removed], [], moduleIds], { removed, roots, joints: summary.joints, modules: moduleIds }, 'support-graph');
  const peak = Math.max(...evidence.trace.map(t => t.displacement));
  meta('dynamic', 'Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。', [Number(peak.toFixed(4))],
    [Number((peak + 0.2).toFixed(4)), 0, Number((peak + 1).toFixed(4))], { trace: evidence.trace, impulse: evidence.impulse,
      nominalDrift: evidence.nominalDrift, scope: '采样轨迹极值，非连续时间极值；不代表实物安全阈值' }, 'Rapier');
  const limits = joint.limits ?? [-Math.PI, Math.PI];
  meta('kinematic', '下列目标位置/角度中哪些在关节声明限位内（含边界）？',
    [limits[0], (limits[0] + limits[1]) / 2], [limits[0] - 0.5, limits[1] + 0.5],
    { joint: joint.id, limits, units: joint.type === 'prismatic' ? 'scene units' : 'radians' }, 'model-state', true);
  const fault = model.joints.find(j => j.id === model.taskConfig.faultJoint)!;
  meta('diagnosis', '已检测到端点和约束类型如下，选择匹配的全部关节。', model.joints.filter(j =>
    j.parent === fault.parent && j.child === fault.child && j.type === fault.type).map(j => j.id),
    model.joints.filter(j => j.parent !== fault.parent || j.child !== fault.child || j.type !== fault.type).slice(0, 3).map(j => j.id),
    { endpoints: [fault.parent, fault.child], type: fault.type, joints: summary.joints }, 'model-state', true);
  const queries = [0, 1, 2].map(i => ({ id: `query-${i}`, cost: 1 + (i + seedOf(model.id)) % 3,
    returns: i === 0 ? [0, 0, 1, 1] : i === 1 ? [0, 1, 2, 3] : [0, 0, 0, 1] }));
  const utilities = queries.map(query => {
    const sizes = [...new Set(query.returns)].map(v => query.returns.filter(x => x === v).length);
    const information = -sizes.reduce((s, n) => s + n / 4 * Math.log2(n / 4), 0);
    return { ...query, information, utility: information / query.cost };
  });
  const best = Math.max(...utilities.map(q => q.utility));
  meta('information-gain', '均匀先验四个世界，选择信息增益/成本最大的全部检查。',
    utilities.filter(q => Math.abs(q.utility - best) < 1e-9).map(q => q.id),
    utilities.filter(q => Math.abs(q.utility - best) >= 1e-9).map(q => q.id),
    { queries, module: service, worlds: ['normal', 'jammed', 'reversed', 'loose'] }, 'finite-world', true);
  const ambiguous = seedOf(model.id) % 2 === 0;
  meta('abstention', '所有相容世界是否允许同一个后续动作？选择继续执行或请求检查。',
    [ambiguous ? 'inspect' : 'commit'], [ambiguous ? 'commit' : 'inspect'],
    { worlds: [{ id: 'w0', action: 'continue' }, { id: 'w1', action: ambiguous ? 'repair' : 'continue' }] }, 'finite-world');
  const observationByWorld = [0, 1, 2, 3].map(i => (seed >>> i) & 1 ? 'positive' : 'negative');
  const observed = observationByWorld[seed % 4];
  const probability = observationByWorld[1] === observed ? 1 / observationByWorld.filter(o => o === observed).length : 0;
  meta('posterior', '均匀先验，得到给定观测后，jammed 世界的后验概率是多少？',
    [probability], [0, 1 / 4, 1 / 3, 1 / 2, 1], { module: service, worlds: ['normal', 'jammed', 'reversed', 'loose'],
      observationByWorld, observed }, 'finite-world');
  const frontier = alternatives.filter(a => !alternatives.some(b => b.id !== a.id && b.cost <= a.cost && b.mass <= a.mass
    && b.stiffness >= a.stiffness && (b.cost < a.cost || b.mass < a.mass || b.stiffness > a.stiffness)));
  meta('pareto', '最小成本、最小质量、最大刚度，选择完整非支配集合。', frontier.map(a => a.id),
    alternatives.filter(a => !frontier.includes(a)).map(a => a.id), { alternatives }, 'model-state', true);

  for (const kind of ['assembly', 'disassembly', 'service-repair', 'compound-edit', 'multi-fault']) {
    const t = task(kind === 'multi-fault' ? 'integrative' : 'procedural', kind,
      '提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。', 'state-machine');
    t.format = 'actions'; Object.assign(t, contract(model, kind)); rows.push(t);
  }
  const schedule = task('integrative', 'scheduling', '为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。', 'resource-schedule');
  schedule.format = 'schedule';
  const count = Math.min(moduleIds.length, Number(model.difficulty[1]) * 2 + 2);
  const jobs = moduleIds.slice(0, count).map((module, i) => ({ id: `job-${i}`, module,
    duration: 1 + seedOf(module) % 3, resource: i % 2 ? 'technician' : 'test-bench',
    after: i >= 2 ? [`job-${i - 2}`] : [] }));
  const starts: Record<string, number> = {}, free = { technician: 0, 'test-bench': 0 };
  for (const job of jobs) { starts[job.id] = free[job.resource as keyof typeof free]; free[job.resource as keyof typeof free] += job.duration; }
  schedule.input = { jobs, deadline: Math.max(...Object.values(free)) };
  schedule.answer = { starts }; rows.push(schedule);
  const policy = task('integrative', 'policy', '提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。', 'finite-world');
  policy.format = 'policy';
  const worldActions = ['continue', 'tighten', 'replace'];
  const worlds = ['normal', 'loose', 'jammed'].map((id, i) => ({ id, action: worldActions[(i + seed % 3) % 3] }));
  const policyQueries = ['visual', 'probe', 'thermal'].map((id, i) => ({ id, cost: 1 + i,
    returns: Object.fromEntries(worlds.map((w, n) => [w.id, i === seed % 3 ? `signal-${n}` : n < 2 ? 'same' : 'other'])) }));
  const selectedQuery = policyQueries[seed % 3];
  policy.input = { module: service, worlds, budget: selectedQuery.cost, queries: policyQueries };
  policy.answer = { queryId: selectedQuery.id, decisions: Object.fromEntries(worlds.map(w => [selectedQuery.returns[w.id], w.action])) }; rows.push(policy);
  rows.push(...advancedTasks(model, evidence, seed, choice));
  if (rows.length !== 48 || rows.some(t => !score(t, t.answer).success))
    throw new Error(`Oracle failed: ${model.id}: ${rows.filter(t => !score(t, t.answer).success).map(t => t.family)}`);
  return { tasks: rows, physics: evidence, geometry: geo };
}
