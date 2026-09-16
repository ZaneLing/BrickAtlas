import { Quaternion, Vector3 } from 'three';
import type { Task, Action } from '../../../src/benchmark/types';
import { solveActions } from '../../../src/benchmark/engine';
import type { Model } from './models';
import type { physicsEvidence } from './physics';

export const EXTRA_ATOMIC = ['local-frame', 'projection', 'relative-order', 'joint-axis'];
export const EXTRA_META = ['clearance-margin', 'load-moment', 'weighted-posterior', 'expected-loss', 'trace-threshold'];
export const EXTRA_PROCEDURAL = ['guarded-repair', 'rollback'];
export const EXTRA_INTEGRATIVE = ['resource-repair', 'budget-policy'];
export const EXTRA_TITLES: Record<string, string> = {
  'local-frame': '局部坐标变换', projection: '正交视图投影', 'relative-order': '空间相对关系',
  'joint-axis': '约束自由度', 'clearance-margin': '维修间隙预算', 'load-moment': '载荷力矩',
  'weighted-posterior': '非均匀先验更新', 'expected-loss': '风险最小决策', 'trace-threshold': '轨迹阈值判定',
  'guarded-repair': '安全联锁维修', rollback: '失败状态回退', 'resource-repair': '共享工具协同维修',
  'budget-policy': '预算约束检查策略',
};
type Choose = (task: Task, good: any[], bad: any[], multi?: boolean) => Task;
export function advancedTasks(model: Model, physics: Awaited<ReturnType<typeof physicsEvidence>>, seed: number, choose: Choose) {
  const rows: Task[] = [], level = Number(model.difficulty[1]), service = model.taskConfig.serviceModule;
  const make = (family: string, layer: Task['layer'], question: string, input: any, evidence: Task['evidence']): Task => ({
    id: `h3-${model.id}-${family}`, modelId: model.id, difficulty: model.difficulty, family, layer,
    title: EXTRA_TITLES[family], question, input, evidence, targetModule: service,
    capabilities: [EXTRA_TITLES[family]], format: 'single-choice', answer: {},
  });
  const mc = (family: string, layer: Task['layer'], question: string, input: any, good: any, bad: any[],
    evidence: Task['evidence'] = 'model-state') => rows.push(choose(make(family, layer, question, input, evidence), [good], bad));
  const m = model.modules.find(m => m.id === service)!;
  const p = model.parts.find(p => p.moduleId === service)!;
  const turn = new Quaternion().setFromAxisAngle(new Vector3(0, 1, 0), (seed % 4) * Math.PI / 2);
  const round = (point: Vector3) => point.toArray().map(v => Number(v.toFixed(5)));
  const point = new Vector3(...p.position).add(new Vector3(1, 0, 0));
  const transformed = round(point.clone().applyQuaternion(turn).add(new Vector3(...m.position)));
  mc('local-frame', 'atomic', '将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。',
    { localPoint: point.toArray(), rotationXYZW: turn.toArray(), translation: m.position },
    transformed, [round(point), round(point.clone().add(new Vector3(...m.position))), transformed.map(v => v + 1)]);
  const view = ['front', 'side', 'top'][seed % 3];
  const axes = view === 'front' ? [0, 1] : view === 'side' ? [2, 1] : [0, 2];
  const world = [level + 1, 2 * level + 3, -level - 2];
  mc('projection', 'atomic', '按公开视图坐标约定，选择该世界点投影后的二维坐标。',
    { view, point: world, convention: 'front=(x,y), side=(z,y), top=(x,z)' },
    axes.map(i => world[i]), [[world[1], world[0]], [world[0], -world[2]], [0, 0], [world[1], world[2]]]);
  const a = model.modules[0], b = model.modules.at(-1)!, axis = seed % 3;
  const relation = b.position[axis] === a.position[axis] ? 'equal' : b.position[axis] > a.position[axis] ? 'greater' : 'less';
  mc('relative-order', 'atomic', '比较B相对A在指定世界轴上的模块原点坐标。',
    { A: { id: a.id, position: a.position }, B: { id: b.id, position: b.position }, axis: ['x', 'y', 'z'][axis] },
    relation, ['greater', 'less', 'equal']);
  const j = model.joints[seed % model.joints.length];
  const dof = j.type === 'fixed' ? 0 : j.type === 'spring' ? 6 : 1;
  mc('joint-axis', 'atomic', '仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。',
    { joint: j }, dof, [0, 1, 3, 6]);
  const tool = 0.25 + level / 10, margin = (seed % 3) / 20;
  const aperture = tool + 2 * margin + (seed % 2 ? 1 : -1) * (0.03 + (seed % 4) / 100);
  mc('clearance-margin', 'metacognitive', '给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？',
    { module: service, aperture, toolWidth: tool, eachSideMargin: margin },
    aperture + 1e-9 >= tool + 2 * margin ? 'feasible' : 'blocked', ['feasible', 'blocked']);
  const lever = [level, 1 + seed % 3, 0], force = [0, -(2 + seed % 5), 0];
  mc('load-moment', 'metacognitive', '绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。',
    { module: service, lever, force, units: 'scene-length × force' },
    new Vector3(...lever).cross(new Vector3(...force)).toArray(),
    [new Vector3(...force).cross(new Vector3(...lever)).toArray(), [0, 0, 0], [0, -level, 0]]);
  const weights = [1 + seed % 5, 1 + (seed >>> 3) % 7, 1 + level];
  const posterior = weights[1] / (weights[0] + weights[1]);
  mc('weighted-posterior', 'metacognitive', '先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。',
    { module: service, worlds: ['normal', 'jammed', 'loose'], weights, compatible: ['normal', 'jammed'] },
    posterior, [weights[1] / weights.reduce((s, n) => s + n, 0), 0, 1], 'finite-world');
  const risk = (1 + seed % 8) / 10, repairCost = 1 + (seed >>> 4) % 7, failureLoss = 4 + level * 3;
  mc('expected-loss', 'metacognitive', '继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。',
    { faultProbability: risk, repairCost, failureLoss, module: service },
    risk * failureLoss > repairCost ? 'repair' : 'continue', ['repair', 'continue'], 'finite-world');
  const peak = Math.max(...physics.trace.map(t => t.displacement));
  const threshold = peak * (seed % 2 ? 1.2 : 0.8);
  mc('trace-threshold', 'metacognitive', '实际采样轨迹中是否有位移严格超过给定阈值？只评价采样点。',
    { trace: physics.trace, threshold }, peak > threshold ? 'exceeded' : 'within', ['exceeded', 'within'], 'Rapier');
  for (const family of [...EXTRA_PROCEDURAL, 'resource-repair']) {
    const targets = family === 'resource-repair' ? model.modules.filter(m => !m.anchored).slice(-Math.min(level + 1, 4)) : [m];
    const actions: Action[] = [], goalFacts: string[] = [];
    const initialFacts = ['tool:free', ...targets.flatMap(m => [`fault:${m.id}`, ...(family === 'rollback' ? [`misaligned:${m.id}`] : [])])];
    for (const target of targets) {
      const id = target.id;
      const stages = family === 'rollback' ? ['isolate', 'undo', 'align', 'verify', 'resume']
        : ['isolate', 'support', 'unlock', 'replace', 'verify', 'relock', 'release'];
      for (const [i, op] of stages.entries()) actions.push({
        id: `${op}:${id}`, label: `${op} ${id}`, requires: i ? [`done:${stages[i - 1]}:${id}`] : ['tool:free', `fault:${id}`],
        forbids: [`done:${op}:${id}`], adds: [`done:${op}:${id}`, ...(i === stages.length - 1 ? [`ready:${id}`, 'tool:free'] : [])],
        deletes: i === 0 ? ['tool:free'] : op === 'verify' ? [`fault:${id}`, `misaligned:${id}`] : [],
        cost: op === 'replace' ? 2 : 1, visual: { moduleId: id, ...(op === 'undo' ? { visible: false } : op === 'align' ? { visible: true } : {}) },
      });
      goalFacts.push(`ready:${id}`);
    }
    // Unsafe shortcuts exist in the catalog but cannot satisfy verified goals.
    actions.push({ id: 'skip-inspection', label: '跳过检查', requires: ['tool:free'], forbids: [],
      adds: ['unverified'], deletes: ['tool:free'], cost: 0 });
    const t = make(family, family === 'resource-repair' ? 'integrative' : 'procedural',
      '从给定故障状态提交动作序列，满足联锁、独占工具、终态及预算。不要跳过验证。', {
        actions: actions.reverse(), initialFacts, initialModules: model.modules.map(m => m.id),
        goalFacts, absentFacts: ['unverified'], budget: actions.reduce((s, a) => s + a.cost, 0),
      }, 'state-machine');
    t.format = 'actions';
    // Public solver selects productive actions by reachability, excluding trap effects.
    t.answer = solveActions(t); rows.push(t);
  }
  const worlds = [{ id: 'nominal', action: 'continue' }, { id: 'fault', action: seed % 2 ? 'replace' : 'tighten' }];
  const budget = 1 + seed % 3;
  const winner = (seed >>> 5) % 3, signals = seed % 2 ? ['clear', 'alert'] : ['pass', 'fail'];
  const queries = ['visual', 'probe', 'thermal'].map((id, i) => ({
    id, cost: i === winner ? budget : (i + 1) % 3 === winner ? budget + 1 : 0,
    returns: { nominal: signals[0], fault: i === winner || (i + 1) % 3 === winner ? signals[1] : signals[0] },
  }));
  const policy = make('budget-policy', 'integrative', '提交预算内、对所有相容世界均正确的检查决策表。',
    { module: service, worlds, queries, budget }, 'finite-world');
  policy.format = 'policy'; policy.answer = { queryId: queries[winner].id,
    decisions: { [signals[0]]: 'continue', [signals[1]]: worlds[1].action } };
  rows.push(policy);
  return rows;
}
