import { readFileSync, writeFileSync, mkdirSync, copyFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { OUT, WEB, sha } from './release';
import type { Task } from '../../../src/benchmark/types';
const read = (name: string) => JSON.parse(readFileSync(resolve(OUT, name), 'utf8'));
const catalog = read('catalog.json'), audit = read('audit.json');
const bundles = catalog.map((m: any) => read(`models/${m.id}.json`));
const tasks: Task[] = bundles.flatMap((b: any) => b.tasks);
const controls = read('controls.json');
const pilot = existsSync(resolve(OUT, 'pilot/run.json')) ? read('pilot/run.json') : { results: [], cases: [] };
const paper = resolve(import.meta.dirname, '../../paper');
const layerZh: Record<string, string> = { atomic: '原子能力', metacognitive: '元认知/物理', procedural: '操作', integrative: '综合' };
const tex = (s: unknown) => String(s).replace(/[&%_$#{}]/g, c => `\\${c}`);
const ordinal = (id: string) => catalog.findIndex((m: any) => m.id === id) + 1;
const totalScore = pilot.results.reduce((s: number, r: any) => s + r.verdict.success, 0);
const families = [...new Set(tasks.map(t => t.family))];
const report = [
  '# BrickAtlas Hierarchy-2 扩容与质量报告', '',
  '## 当前交付', '',
  `40 个布局（保留18个，新增22个），四级各10个对象，每个对象35题，共${audit.tasks}题。`,
  `总计${audit.parts}个可视部件、${audit.modules}个刚体模块、${audit.joints}个声明关节。`,
  '这些是由程序化组件组合的原创开发布局，不是40位独立设计师或40种完全不同的机制；共享构件族需要在未来划分中一起隔离。',
  '',
  '## 与上一版相比', '',
  '| 项目 | Hierarchy-1 | Hierarchy-2 |', '|---|---:|---:|',
  '| 对象布局 | 18 | 40 |', '| 新版本核心问题 | 90 | 1,400 |',
  '| 可视部件 | 1,773 | 5,070 |', '| 每级共同覆盖任务族 | 部分 | 35 |',
  '| 网页操作回放 | 静态动作列表 | 可执行状态转换 |',
  '| 动力学题证据 | 部分手写响应表 | Rapier 实际采样轨迹 |', '',
  '## 四级库', '', '| 难度 | 对象数 | 零件范围 | 题数 |', '|---|---:|---|---:|',
  ...audit.levels.map((d: any) => `| ${d.id} | ${d.models} | ${d.minParts}–${d.maxParts} | ${d.tasks} |`), '',
  'D2与D3零件范围有交叉。层级是按部件/装配体/机构/系统的设计范围指定，尚不是测得的单调难度等级。',
  '不应把零件增加直接解释为同一能力的因果难度提升；跨层比较应固定任务族和输入条件。',
  '',
  '## 任务与能力', '', '| 层 | 任务族 | 每级题数 | 全部题数 |', '|---|---|---:|---:|',
  ...['atomic', 'metacognitive', 'procedural', 'integrative'].map(layer =>
    `| ${layerZh[layer]} | ${[...new Set(tasks.filter(t => t.layer === layer).map(t => t.title))].join('、')} | ${audit.byLayer[layer] / 4} | ${audit.byLayer[layer]} |`), '',
  '## 质量与物理审计', '',
  '- 每个源对象：实例与模块 ID 唯一、有限位姿、正尺寸、声明依赖顺序检查；同一任务族在40个对象上都存在。',
  '- 不含仅换色或改名的几何重复。22个新布局共享设计组件，不作为独立机制族计数。',
  '- 1,400个参考答案逐个验证；200个动作任务由读取公开前置条件的求解器执行。',
  '- 装配/拆卸/维修/复合编辑通过状态事实验证，允许交换独立动作；拒绝漏步、重复、超预算。',
  '- 调度验证先后依赖、独占资源、时长与截止；条件策略在所有可能世界中检查。',
  `- 40个对象均执行了Rapier轨迹和Shape Cast；其中${audit.nominalWithinTolerance}/40在当前模拟参数下名义漂移<0.35，其余不能标记为稳定结构。`,
  '- quality.json逐例公开包围盒重叠数与名义漂移。包围盒重叠可能对应合理的关节界面；也可能暴露设计干涉，不能等同精确碰撞或扣合检查。',
  '- 动力学题测量读懂实际采样轨迹的能力，未声称仅靠单图预测动力学；碰撞题亦提供模拟观测。',
  '- 持续接触、材料形变、LEGO连接器扣合、制造公差、机械手执行仍未标定。',
  '',
  '## 原网页接入', '',
  '- 原网站首页包含全部40张基准模型卡片。',
  '- /benchmark 提供难度与名称筛选；/benchmark/:id 加载完整真实几何。',
  '- 鼠标旋转、滚轮缩放、右键平移；三视图、自由视角、3D展开、模块选择与隔离、截图导出。',
  '- 任务面板包含全部35题、题目、输入、参考答案与评分。粘贴模型动作JSON可以播放和拖动到任一步。',
  '- 回放显示真实部件显隐与颜色变化及状态事实；展开是可视化操作，不是物理拆解认证。',
  '- 网页中模型文件与离线发布文件逐字节一致；使用原网页同一渲染器生成160张模型视图。',
  '',
  '## 模型流程验证', '',
  `GPT-4.1 mini 本版固定16题：${totalScore}/${pilot.cases.length || 16}。本轮费用$${((pilot.after ?? 0) - (pilot.before ?? 0)).toFixed(6)}。`,
  '四个难度分别抽取边界识别、信息增益、承载维修和资源调度各一题。n=1/单元格；不能外推各层全部题目的准确率。',
  '选择先于调用固定。原始回答、usage成本、generation ID和public.json哈希保存在pilot/run.json。',
  '大量结构信息已公开，因此原子题主要是结构读数/编辑合同检查；视觉依赖性消融尚未完成。小样本高分也说明仍需后续难度校准。',
  '',
  '## 全部模型', '', '| 编号 | 难度 | 名称 | 零件 | 模块 | 关节 | 题数 |', '|---|---|---|---:|---:|---:|---:|',
  ...catalog.map((m: any, i: number) => `| ${i + 1} | ${m.difficulty} | ${m.nameZh} (${m.id}) | ${m.parts} | ${m.modules} | ${m.joints} | ${m.tasks} |`), '',
  '完整问答见QUESTION_BANK.zh-CN.md；模型、任务、真实物理证据见models/*.json；public.json排除答案。',
].join('\n') + '\n';
writeFileSync(resolve(OUT, 'REPORT.zh-CN.md'), report);
const bank = ['# Hierarchy-2 全部1,400题', '', '题目、输入与参考答案来自同一发布合同。', ''];
for (const b of bundles) {
  bank.push(`## ${b.model.difficulty} ${b.model.nameZh}`, '');
  for (const t of b.tasks as Task[]) bank.push(`### ${t.title}（${t.id}）`, '', t.question, '',
    `能力：${t.capabilities.join('、')}；形式：${t.format}；证据：${t.evidence}。`, '',
    ...(t.options ? t.options.map(o => `- ${o.id}：${o.label}`) : []), '',
    '```json', JSON.stringify({ input: t.input, answer: t.answer }, null, 2), '```', '');
}
writeFileSync(resolve(OUT, 'QUESTION_BANK.zh-CN.md'), bank.join('\n'));
mkdirSync(resolve(paper, 'tables'), { recursive: true });
writeFileSync(resolve(paper, 'tables/hierarchy2-scale.tex'), audit.levels.map((d: any) =>
  `${d.id} & ${d.models} & ${d.minParts}--${d.maxParts} & ${d.tasks} \\\\`).join('\n') + '\n');
const contracts = families.map(family => {
  const t = tasks.find(t => t.family === family)!;
  return `${tex(family)} & ${tex(t.layer)} & ${tex(t.format)} & ${tex(t.evidence)} \\\\`;
}).join('\n') + '\n';
writeFileSync(resolve(paper, 'tables/hierarchy2-contracts.tex'), contracts);
const pilotTable = ['D1', 'D2', 'D3', 'D4'].map(d => {
  const cells = ['atomic', 'metacognitive', 'procedural', 'integrative'].map(layer => {
    const rs = pilot.results.filter((r: any) => r.difficulty === d && r.layer === layer);
    return rs.length ? `${rs.reduce((s: number, r: any) => s + r.verdict.success, 0)}/${rs.length}` : '--';
  });
  return `${d} & ${cells.join(' & ')} \\\\`;
}).join('\n') + '\n';
writeFileSync(resolve(paper, 'tables/hierarchy2-pilot.tex'), pilotTable);

const cases = ['\\onecolumn', '\\section{Complete Object and Question Index}'];
for (const b of bundles) {
  const m = b.model;
  cases.push(ordinal(m.id) > 1 ? '\\clearpage' : '', `\\subsection{${ordinal(m.id)}. ${tex(m.name)} (${m.difficulty})}`,
    `${m.parts.length} visible parts, ${m.modules.length} modules, ${m.joints.length} joints. `
    + `Nominal drift: ${b.physics.nominalDrift.toFixed(4)}; tolerance outcome: ${b.physics.nominalWithinTolerance ? 'within' : 'outside'}. `
    + `Inter-module envelope overlaps: ${b.geometry.interModuleEnvelopeOverlaps}. These counts do not certify connector legality.`,
    '\\begin{center}',
    ...['iso', 'front', 'side', 'top'].map(view => `\\includegraphics[width=.24\\textwidth]{figures/hierarchy2/${m.id}-${view}.png}`),
    '\\end{center}', '\\noindent The following 35 tasks share this source object. Full inputs, choices and answers are in the companion question bank.',
    '\\begin{center}\\scriptsize\\begin{tabular}{rllll}\\toprule No. & Family & Layer & Output & Evidence\\\\\\midrule',
    ...b.tasks.map((t: Task, i: number) => `${i + 1} & ${tex(t.family)} & ${tex(t.layer)} & ${tex(t.format)} & ${tex(t.evidence)} \\\\`),
    '\\bottomrule\\end{tabular}\\end{center}');
}
writeFileSync(resolve(paper, 'hierarchy2-cases.tex'), cases.join('\n') + '\n');
const evidence = { ...audit, pilot: { model: pilot.model, cases: pilot.cases.length, completed: pilot.results.length,
  success: totalScore, cost: (pilot.after ?? 0) - (pilot.before ?? 0) },
  hashes: Object.fromEntries(['audit.json', 'catalog.json', 'public.json', 'answers.json', 'quality.json',
    'controls.json', 'render-audit.json', 'pilot/run.json'].filter(p => existsSync(resolve(OUT, p))).map(p => [p, sha(resolve(OUT, p))])),
  actionSolverSuccess: controls.filter((r: any) => r.publicActionSolver?.success === 1).length,
  constantSuccess: controls.reduce((s: number, r: any) => s + r.constantOrEmpty.success, 0) };
writeFileSync(resolve(paper, 'hierarchy2-evidence.json'), JSON.stringify(evidence, null, 2) + '\n');
mkdirSync(resolve(paper, 'figures/hierarchy2'), { recursive: true });
for (const m of catalog) for (const view of ['iso', 'front', 'side', 'top'])
  copyFileSync(resolve(OUT, 'images', `${m.id}-${view}.png`), resolve(paper, 'figures/hierarchy2', `${m.id}-${view}.png`));
mkdirSync(resolve(WEB, 'docs'), { recursive: true });
copyFileSync(resolve(OUT, 'REPORT.zh-CN.md'), resolve(WEB, 'docs/REPORT.zh-CN.md'));
console.log(JSON.stringify(evidence));
