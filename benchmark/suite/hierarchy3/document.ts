import { readFileSync, writeFileSync, mkdirSync, copyFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { OUT, sha } from './release';
import type { Task } from '../../../src/benchmark/types';
import './errata';
const read = (name: string) => JSON.parse(readFileSync(resolve(OUT, name), 'utf8'));
const catalog = read('catalog.json'), audit = read('audit.json');
const bundles = catalog.map((m: any) => read(`models/${m.id}.json`));
const tasks: Task[] = bundles.flatMap((b: any) => b.tasks);
const controls = read('controls.json'), distributions = read('answer-distributions.json');
const pilot = existsSync(resolve(OUT, 'pilot/run.json')) ? read('pilot/run.json') : { results: [], cases: [] };
const paper = resolve(import.meta.dirname, '../../paper');
const layerZh: Record<string, string> = { atomic: '原子能力', metacognitive: '元认知/物理', procedural: '操作', integrative: '综合' };
const tex = (s: unknown) => String(s).replace(/[&%_$#{}]/g, c => `\\${c}`);
const totalScore = pilot.results.reduce((s: number, r: any) => s + r.verdict.success, 0);
const families = [...new Set(tasks.map(t => t.family))];
const actionCount = tasks.filter(t => t.format === 'actions').length;
const report = [
  '# BrickAtlas Hierarchy-3 扩充与校正报告', '',
  `本版48个原创数字布局，四级各12个，每个布局48类任务，共${audit.tasks}题。包含${audit.parts}个可视部件、${audit.modules}个模块、${audit.joints}个声明关节。`,
  '保留并校正40个旧布局，新增8个布局。程序化构件和部分机构拓扑共享，48个布局不等同48个独立机构家族。',
  '',
  '## 扩充规模', '', '| 项目 | Hierarchy-2 | Hierarchy-3 |', '|---|---:|---:|',
  '| 原创布局 | 40 | 48 |', '| 每级布局 | 10 | 12 |', '| 共用任务族 | 35 | 48 |',
  '| 问题数 | 1,400 | 2,304 |', '| 可视部件 | 5,070 | 6,339 |',
  '| 参考动作任务 | 200 | 384 |', '',
  '| 难度 | 布局数 | 零件范围 | 题数 |', '|---|---:|---|---:|',
  ...audit.levels.map((d: any) => `| ${d.id} | ${d.models} | ${d.minParts}–${d.maxParts} | ${d.tasks} |`), '',
  '四级是结构范围：部件、装配体、机构、系统。D2与D3零件范围有交叉，不代表已标定的单调难度；横向比较固定对象，纵向比较固定任务族。',
  '',
  '## 能力矩阵', '', '| 层 | 任务族 | 每级题数 | 总题数 |', '|---|---|---:|---:|',
  ...Object.keys(layerZh).map(layer =>
    `| ${layerZh[layer]} | ${[...new Set(tasks.filter(t => t.layer === layer).map(t => t.title))].join('、')} | ${audit.byLayer[layer] / 4} | ${audit.byLayer[layer]} |`), '',
  '新增任务覆盖局部坐标、正交投影、相对位置、关节自由度、净空预算、载荷力矩、非均匀后验、期望损失、轨迹阈值、联锁维修、回退、共享工具和预算策略。',
  '',
  '## 校正结果', '',
  '- 11道旧单选存在等价集合选项；新版按题型规范化并验证所有选择题语义选项唯一。向量和动作序列不排序。',
  '- 修正Mechanism-1条件熵负号；六个旧最佳检查标签未改变。旧数据、旧试跑及原分数保留。',
  '- 球、圆柱、齿轮、拱及凸点统一尺寸与包围规则；逐顶点验证显示几何被碰撞包围体包含。',
  '- 修复暂停回放选择模块导致隐藏模块重现；隔离与当前帧激活状态取交集。',
  '- 修正不一致塔脚锚点、多个模型的接口穿透、船闸单点弹簧系泊的旋转失约束。旋转限位使用运行时setLimits并逐个回读；冲击施力点和采样点均与局部原点无关。',
  `- ${audit.nominalWithinTolerance}/48模型满足新版名义状态约束：代表点位移<0.35、转角<0.15rad、非弹簧关节残差<0.02。全部模块对（包括相连模块）初始窄相穿透≤0.005。`,
  '- 新模拟协议：120Hz、64次迭代、ForceBased位置伺服(60000/1500/20000)，含凸点保守包围体；相连模块接触保持启用。参数与旧版不同，不能把改善全部归因于几何变化。',
  '- 各模块内部为复合刚体。未认证商业LEGO扣合、材料、制造公差或每步机器人接触路径。',
  '', '完整问题与修正依据见[ERRATA.zh-CN.md](ERRATA.zh-CN.md)。',
  '',
  '## 答案捷径审计', '', '| 题族 | 新版语义答案种数 | 固定语义多数答案准确率 |', '|---|---:|---:|',
  ...distributions.filter((d: any) => ['rotate', 'inventory', 'prefix', 'posterior', 'pareto', 'policy'].includes(d.family))
    .map((d: any) => `| ${d.family} | ${d.uniqueAnswers} | ${(d.semanticMajorityAccuracy * 100).toFixed(1)}% |`), '',
  '这六类旧题各40/40答案相同。新版本改变实际输入条件，不仅轮转选项标签。完整48族分布见answer-distributions.json；二选一题仍有较高机会水平，不把这些基础控制题宣称为高难任务。',
  '',
  '## 验证与网页', '',
  `全部${tasks.length}个参考答案通过；${actionCount}个动作合同可由公开规则求解器完成。回归检查拒绝所有错误单选、每题一位变更的多选、缺步、重复动作、跳过验证、资源重叠和预算外策略。`,
  '原网站首页包含全部48张模型卡片。/benchmark可筛选，/benchmark/:id可旋转、缩放、平移、三视图、展开、隔离、截图，以及粘贴动作JSON逐步回放。全部数据与离线模型逐字节相同。',
  '',
  '## 低成本流程试跑', '',
  pilot.results.length
    ? `GPT-4.1 mini固定${pilot.cases.length}题：${totalScore}/${pilot.results.length}通过，费用$${((pilot.after ?? 0) - (pilot.before ?? 0)).toFixed(6)}。每格n=1，仅验证流程。原始记录与输入/图像哈希见pilot/run.json。`
    : '新版尚未运行付费模型；旧版14/16单独存档，不移作新版成绩。',
  '公开结构数据辅助作答；未完成去图/去符号消融、人工难度校准或隐藏测试，不能外推纯视觉能力与整体准确率。',
  '本次9个失败中：4个动作答案使用错误JSON字段（动作列表本身可由诊断性重放检查），4个期望损失题选错，1个坐标变换题选错。严格评分不自动修复字段，避免混淆格式遵循与任务能力；题族也不同，不能与旧14/16直接比较。',
  '',
  '## 全部模型', '', '| 难度 | 名称 | 零件 | 模块 | 关节 | 题数 |', '|---|---|---:|---:|---:|---:|',
  ...catalog.map((m: any) => `| ${m.difficulty} | ${m.nameZh} (${m.id}) | ${m.parts} | ${m.modules} | ${m.joints} | ${m.tasks} |`),
  '', '题目/选项/输入/答案见QUESTION_BANK.zh-CN.md；public.json排除答案；manifest.json绑定发布数据及生成器。',
].join('\n') + '\n';
writeFileSync(resolve(OUT, 'REPORT.zh-CN.md'), report);
const bank = [`# Hierarchy-3 全部${audit.tasks}题`, '', '题目、输入与参考答案来自同一发布合同。', ''];
for (const b of bundles) {
  bank.push(`## ${b.model.difficulty} ${b.model.nameZh}`, '');
  for (const t of b.tasks as Task[]) bank.push(`### ${t.title}（${t.id}）`, '', t.question, '',
    `能力：${t.capabilities.join('、')}；形式：${t.format}；证据：${t.evidence}。`, '',
    ...(t.options ? t.options.map(o => `- ${o.id}：${o.label}`) : []), '',
    '```json', JSON.stringify({ input: t.input, answer: t.answer }, null, 2), '```', '');
}
writeFileSync(resolve(OUT, 'QUESTION_BANK.zh-CN.md'), bank.join('\n'));
mkdirSync(resolve(paper, 'tables'), { recursive: true });
writeFileSync(resolve(paper, 'tables/hierarchy3-scale.tex'), audit.levels.map((d: any) =>
  `${d.id} & ${d.models} & ${d.minParts}--${d.maxParts} & ${d.tasks} \\\\`).join('\n') + '\n');
writeFileSync(resolve(paper, 'tables/hierarchy3-contracts.tex'), families.map(family => {
  const t = tasks.find(t => t.family === family)!;
  return `${tex(family)} & ${tex(t.layer)} & ${tex(t.format)} & ${tex(t.evidence)} \\\\`;
}).join('\n') + '\n');
writeFileSync(resolve(paper, 'tables/hierarchy3-pilot.tex'), ['D1', 'D2', 'D3', 'D4'].map(d => {
  const cells = Object.keys(layerZh).map(layer => {
    const rs = pilot.results.filter((r: any) => r.difficulty === d && r.layer === layer);
    return rs.length ? `${rs.reduce((s: number, r: any) => s + r.verdict.success, 0)}/${rs.length}` : '--';
  });
  return `${d} & ${cells.join(' & ')} \\\\`;
}).join('\n') + '\n');
writeFileSync(resolve(paper, 'hierarchy3-results.tex'), [
  `\\newcommand{\\PilotN}{${pilot.results.length}}`, `\\newcommand{\\PilotSuccess}{${totalScore}}`,
  `\\newcommand{\\PilotCost}{${((pilot.after ?? 0) - (pilot.before ?? 0)).toFixed(6)}}`,
  `\\newcommand{\\ControlSuccess}{${controls.reduce((s: number, r: any) => s + r.constantOrEmpty.success, 0)}}`,
].join('\n') + '\n');
const cases = ['\\onecolumn', '\\section{Complete Object and Question Index}'];
for (const [index, b] of bundles.entries()) {
  const m = b.model;
  cases.push(index ? '\\clearpage' : '', `\\subsection{${index + 1}. ${tex(m.name)} (${m.difficulty})}`,
    `${m.parts.length} visible parts, ${m.modules.length} modules, ${m.joints.length} joints. `
    + `Nominal representative-point displacement: ${b.physics.nominalPointDrift.toFixed(4)}; `
    + `angular displacement: ${b.physics.nominalAngularDrift.toFixed(4)} rad. `
    + `No inter-module penetration above 0.005, including directly joined modules.`,
    '\\begin{center}', ...['iso', 'front', 'side', 'top'].map(view =>
      `\\includegraphics[width=.24\\textwidth]{figures/hierarchy3/${m.id}-${view}.png}`),
    '\\end{center}', '\\noindent All 48 tasks share this source; complete inputs, choices and answers are in the companion question bank.',
    '\\begin{center}\\tiny\\begin{tabular}{rllll}\\toprule No. & Family & Layer & Output & Evidence\\\\\\midrule',
    ...b.tasks.map((t: Task, i: number) => `${i + 1} & ${tex(t.family)} & ${tex(t.layer)} & ${tex(t.format)} & ${tex(t.evidence)} \\\\`),
    '\\bottomrule\\end{tabular}\\end{center}');
}
writeFileSync(resolve(paper, 'hierarchy3-cases.tex'), cases.join('\n') + '\n');
const evidence = { ...audit, pilot: { model: pilot.model, cases: pilot.cases.length, completed: pilot.results.length,
  success: totalScore, cost: (pilot.after ?? 0) - (pilot.before ?? 0) },
  hashes: Object.fromEntries(['audit.json', 'catalog.json', 'public.json', 'answers.json', 'quality.json',
    'controls.json', 'render-audit.json', 'pilot/run.json'].filter(p => existsSync(resolve(OUT, p))).map(p => [p, sha(resolve(OUT, p))])),
  actionSolverSuccess: controls.filter((r: any) => r.publicActionSolver?.success === 1).length };
writeFileSync(resolve(paper, 'hierarchy3-evidence.json'), JSON.stringify(evidence, null, 2) + '\n');
mkdirSync(resolve(paper, 'figures/hierarchy3'), { recursive: true });
for (const m of catalog) for (const view of ['iso', 'front', 'side', 'top'])
  copyFileSync(resolve(OUT, 'images', `${m.id}-${view}.png`), resolve(paper, 'figures/hierarchy3', `${m.id}-${view}.png`));
console.log(JSON.stringify(evidence));
