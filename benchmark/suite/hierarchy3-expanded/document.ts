import { copyFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { BASE, OUT, ROOT, read, write, sha } from './release';
import type { Task } from '../../../src/benchmark/types';
import { FAMILIES } from './models';

const audit = read(resolve(OUT, 'audit.json')), catalog = read(resolve(OUT, 'catalog.json')) as any[];
const bundles = catalog.map(m => read(resolve(OUT, 'models', `${m.id}.json`)));
const tasks: Task[] = bundles.flatMap(b => b.tasks), controls = read(resolve(OUT, 'controls.json'));
const paper = resolve(ROOT, 'benchmark/paper');
const tex = (value: unknown) => String(value).replace(/[&%_$#{}]/g, c => `\\${c}`);
const layers = { atomic: '原子能力', metacognitive: '元认知与物理', procedural: '操作执行', integrative: '综合任务' };
const body = [
  '# Hierarchy-3 扩容版：144 模型与 6,912 道题', '',
  `在原48模型基础上新增96个原创数字布局，四级各36个模型，每模型完整覆盖48类任务，共6,912题。`,
  `总计${audit.parts.toLocaleString('en-US')}个可视部件、${audit.modules}个刚体模块、${audit.joints}个声明关节。`,
  '',
  '| 指标 | 原版 | 扩容版 |', '|---|---:|---:|',
  '| 模型数 | 48 | 144 |', '| 每级模型数 | 12 | 36 |',
  '| 题目数 | 2,304 | 6,912 |', '| 每级题目 | 576 | 1,728 |',
  '| 可视部件 | 6,339 | 42,617 |', '| 配套视图 | 192 | 576 |',
  '| 动作题 | 384 | 1,152 |', '',
  '## 新增模型的组织', '',
  '新增12类构造族，每族有2种设计配置，在4个结构等级中逐级加入载体、工位、仓储和共享检查模块，共12×2×4=96个布局。',
  'D1为独立装置；D2加入移动载体与控制台；D3组合两个不同工位并加入仓储；D4组合3或4个工位并设置共享检查架。',
  '它们共享可复用构件，不是96个独立采样的机械家族，也没有把换色或单纯重命名算作新模型。',
  '',
  '| 构造族 | 配置一 | 配置二 | 新布局数 |', '|---|---|---|---:|',
  ...FAMILIES.map(f => `| ${f.kind} | ${f.zh[0]} | ${f.zh[1]} | 8 |`), '',
  '## 各级规模', '',
  '| 难度 | 模型 | 本次新增 | 部件范围 | 问题 |', '|---|---:|---:|---|---:|',
  ...audit.levels.map((l: any) => `| ${l.id} | ${l.models} | ${l.newModels} | ${l.minParts}–${l.maxParts} | ${l.tasks} |`), '',
  '难度是结构范围分层，尚未经过人类或模型准确率校准。各层部件数量存在交叉；同一构造族内可比较增加载体和工位后的任务负担。',
  '',
  '## 题库同步', '',
  '| 能力层 | 每模型题族数 | 每级题数 | 总题数 |', '|---|---:|---:|---:|',
  ...Object.entries(layers).map(([key, title]) => `| ${title} | ${audit.byLayer[key] / 144} | ${audit.byLayer[key] / 4} | ${audit.byLayer[key]} |`), '',
  '48个任务族全部覆盖144个模型，包括识别、计数、位姿、改色、补件、依赖装配、维修、支撑反事实、实际物理记录、信息增益、贝叶斯后验、风险、调度和预算策略。新增4,608题的输入和答案均由对应模型生成。',
  '本轮沿用已校正的题型合同，没有把相同题目反复复制作为新增题量。条件字段和模型结构决定答案；基础读数题仍可能简单。',
  '',
  '## 质量验证', '',
  '- 所有ID、正尺寸、有限位姿、单位四元数和装配依赖顺序验证通过。',
  '- 逐顶点核对显示几何被含凸点的包围体包含；所有模块对（包括直接相连者）初始窄相穿透≤0.005。',
  `- ${audit.nominalWithinTolerance}/144满足几何代表点位移<0.35、转角<0.15rad、非弹簧关节残差<0.02；旋转与滑动限位经运行时回读。`,
  '- 沿用Rapier 0.20.0、120Hz、64次迭代、有限力位置伺服60000/1500/20000；未放宽旧门槛。',
  '- 新增96个布局几何指纹互异，去除名称、颜色和平移后也不重复。总库143种几何，旧版indexed-toggle-latch/orthogonal-probe-stage同外形、关节配置不同，保持原样并公开标注。',
  '- 6,912个参考答案均被接受；1,152个动作题由公开规则求解器完成。回归验证错误选项、错误多选集合、缺步与超预算均不能通过。',
  '- 模块内部仍是复合刚体；这些验证不认证商业积木扣合、被动稳定、齿轮传动耦合或机器人连续操作路径。',
  '',
  '## 审核记录与历史结果兼容', '',
  '原48模型JSON及其2,304题保持逐字节不变，见retained-compatibility.json。原来的通过/不通过判定、理由和导入批次继续使用同一taskId。',
  '审核总览分母自动读取最新目录，变为6,912；新增题默认待审核。人工意见只在用户提交时写入，扩容程序不创建人工通过记录。',
  '原16题廉价试跑7/16、$0.013621保持在hierarchy-v3/pilot/run.json。本次新增模型没有付费模型结果，不能将旧试跑视为144模型库准确率。',
  '',
  '## 网页与文件', '',
  '- /benchmark：全部144个模型，按难度/名称检索，可3D旋转、缩放、展开、隔离、三视图与动作回放。',
  '- /benchmark/review：6,912题审核总览；原模型和新模型反馈汇总到同一批次。',
  '- QUESTION_BANK.zh-CN.md：完整题目、选项、公开输入和参考答案；questions/*.md可按模型单独阅读。',
  '- public.json与answers.json：公开任务与答案分开；models/*.json包含对应几何和实际模拟证据。',
  '- 论文更新144模型规模；附录逐模型收录全部144个对象和48类任务索引。保留192张原视图、新生成384张，共576张。',
  '',
  '## 全部模型', '', '| 难度 | 名称 / ID | 部件 | 模块 | 关节 | 状态 |', '|---|---|---:|---:|---:|---|',
  ...catalog.map(m => `| ${m.difficulty} | ${m.nameZh} (${m.id}) | ${m.parts} | ${m.modules} | ${m.joints} | ${m.retained ? '保留' : '新增'} |`), '',
].join('\n');
writeFileSync(resolve(OUT, 'REPORT.zh-CN.md'), body.trimEnd() + '\n');
mkdirSync(resolve(OUT, 'questions'), { recursive: true });
const bank = ['# Hierarchy-3 扩容版全部6,912题', '', '原48模型2,304题保持不变，新增96模型4,608题。', ''];
for (const b of bundles) {
  const lines = [`## ${b.model.difficulty} ${b.model.nameZh}`, ''];
  for (const t of b.tasks as Task[]) lines.push(`### ${t.title}（${t.id}）`, '', t.question, '',
    `能力：${t.capabilities.join('、')}；形式：${t.format}；证据：${t.evidence}。`, '',
    ...(t.options ? t.options.map(o => `- ${o.id}：${o.label}`) : []), '',
    '```json', JSON.stringify({ input: t.input, answer: t.answer }, null, 2), '```', '');
  const contents = lines.join('\n');
  writeFileSync(resolve(OUT, 'questions', `${b.model.id}.md`), contents);
  bank.push(contents);
}
writeFileSync(resolve(OUT, 'QUESTION_BANK.zh-CN.md'), bank.join('\n'));
writeFileSync(resolve(paper, 'tables/hierarchy-expanded-scale.tex'), audit.levels.map((l: any) =>
  `${l.id} & ${l.models} & ${l.minParts}--${l.maxParts} & ${l.tasks} \\\\`).join('\n') + '\n');
writeFileSync(resolve(paper, 'hierarchy-expanded-results.tex'), [
  `\\newcommand{\\PilotN}{16}`, `\\newcommand{\\PilotSuccess}{7}`, `\\newcommand{\\PilotCost}{0.013621}`,
  `\\newcommand{\\ControlSuccess}{${controls.reduce((s: number, r: any) => s + r.constantOrEmpty.success, 0)}}`,
].join('\n') + '\n');
const cases = ['\\onecolumn', '\\section{Complete Expanded Object and Question Index}'];
mkdirSync(resolve(paper, 'figures/hierarchy-expanded'), { recursive: true });
for (const [index, b] of bundles.entries()) {
  const m = b.model;
  cases.push(index ? '\\clearpage' : '', `\\subsection{${index + 1}. ${tex(m.name)} (${m.difficulty})}`,
    `${m.parts.length} visible parts; ${m.modules.length} modules; ${m.joints.length} joints. `
      + `Representative-point motion ${b.physics.nominalPointDrift.toFixed(4)}; rotation ${b.physics.nominalAngularDrift.toFixed(4)} rad.`,
    '\\begin{center}', ...['iso', 'front', 'side', 'top'].map(view =>
      `\\includegraphics[width=.24\\textwidth]{figures/hierarchy-expanded/${m.id}-${view}.png}`),
    '\\end{center}', '\\noindent All 48 families share this source. Full inputs and answers appear in the companion question bank.',
    '\\begin{center}\\tiny\\begin{tabular}{rllll}\\toprule No. & Family & Layer & Output & Evidence\\\\\\midrule',
    ...b.tasks.map((t: Task, i: number) => `${i + 1} & ${tex(t.family)} & ${tex(t.layer)} & ${tex(t.format)} & ${tex(t.evidence)} \\\\`),
    '\\bottomrule\\end{tabular}\\end{center}');
  for (const view of ['iso', 'front', 'side', 'top'])
    copyFileSync(resolve(OUT, 'images', `${m.id}-${view}.png`), resolve(paper, 'figures/hierarchy-expanded', `${m.id}-${view}.png`));
}
writeFileSync(resolve(paper, 'hierarchy-expanded-cases.tex'), cases.join('\n') + '\n');
write(resolve(paper, 'hierarchy-expanded-evidence.json'), { ...audit,
  hashes: Object.fromEntries(['audit.json', 'catalog.json', 'public.json', 'answers.json', 'quality.json',
    'controls.json', 'retained-compatibility.json', 'render-audit.json'].map(p => [p, sha(resolve(OUT, p))])),
  historicalPilot: { path: 'benchmark/hierarchy-v3/pilot/run.json', sha256: sha(resolve(BASE, 'pilot/run.json')), n: 16, success: 7 },
});
console.log(JSON.stringify({ modelPages: bundles.length, questions: tasks.length, added: audit.newLayouts }));
