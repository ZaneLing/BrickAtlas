import { existsSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { hierarchyModels } from './models';
import { OUTPUT } from './release';
import { hierarchyTasks } from './tasks';
import { DIFFICULTIES, TASK_LAYERS, type TaskLayer } from './types';

const escape = (value: unknown) => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;');
const pretty = (value: unknown) => JSON.stringify(value, null, 2);

const MODEL_LABELS: Record<string, string> = {
  'openai/gpt-4.1-mini': 'GPT-4.1 mini',
  'google/gemini-2.5-flash': 'Gemini 2.5 Flash',
};

const LAYER_CAPABILITIES: Record<TaskLayer, string> = {
  atomic: '识别、计数、颜色、位姿、连接、支撑、增删改换、局部修复',
  metacognitive: '前缀稳定、可达性、反事实、动力学、运动学、不确定性、信息增益、Pareto',
  procedural: '装配、拆卸、编辑后验证、故障恢复、库存重规划、先检查后执行',
  integrative: '诊断 + 可达 + 维修 + 库存 + 风险 + 验证的联合决策',
};

const DIFFICULTY_INTENT_ZH = {
  D1: '单一接口、局部状态变化和短依赖链。',
  D2: '多个子装配、一个主要机构和局部遮挡。',
  D3: '完整多关节对象，包含维修可达、动力学与隐藏故障。',
  D4: '跨工位耦合、共享资源、长操作链和跨区域故障。',
} as const;

interface ResultRow {
  taskId: string;
  model: string;
  answer: unknown;
  success: number;
}

function readResults(): ResultRow[] {
  const latestPath = resolve(OUTPUT, 'results/latest.json');
  if (!existsSync(latestPath)) return [];
  const latest = JSON.parse(readFileSync(latestPath, 'utf8'));
  const run = JSON.parse(readFileSync(resolve(OUTPUT, 'results', latest.path), 'utf8'));
  return run.results.map((row: any) => ({
    taskId: row.taskId,
    model: MODEL_LABELS[row.model] ?? row.model,
    answer: row.answer,
    success: row.verdict.success,
  }));
}

function matrixRows(results: ResultRow[]) {
  return DIFFICULTIES.flatMap(difficulty => TASK_LAYERS.map(layer => {
    const selected = results.filter(result => {
      const task = hierarchyTasks().find(candidate => candidate.id === result.taskId);
      return task?.difficulty === difficulty.id && task.layer === layer.id;
    });
    return {
      difficulty: difficulty.id,
      layer: layer.id,
      n: selected.length,
      success: selected.filter(result => result.success).length,
    };
  }));
}

export function composeHierarchy() {
  const models = hierarchyModels(), tasks = hierarchyTasks(), results = readResults();
  const resultsRoot = resolve(OUTPUT, 'results');
  const excludedRuns = existsSync(resultsRoot)
    ? readdirSync(resultsRoot, { withFileTypes: true }).filter(entry => entry.isDirectory())
      .map(entry => {
        const path = resolve(resultsRoot, entry.name, 'run.json');
        return existsSync(path) ? JSON.parse(readFileSync(path, 'utf8')) : null;
      }).filter(run => run && run.status !== 'complete')
    : [];
  const modelNames = [...new Set(results.map(row => row.model))];
  const summaries = modelNames.map(model => {
    const selected = results.filter(row => row.model === model);
    return { model, n: selected.length, success: selected.filter(row => row.success).length };
  });
  const difficultyNav = DIFFICULTIES.map(level =>
    `<button data-difficulty="${level.id}">${level.id} ${level.nameZh}</button>`).join('');
  const layerNav = TASK_LAYERS.map(layer =>
    `<button data-layer="${layer.id}">${layer.nameZh}</button>`).join('');
  const resultSummary = summaries.length
    ? `<section class="results"><h2>低成本流程试跑</h2><table><thead><tr><th>模型</th><th>样本</th><th>Exact Success</th></tr></thead>
      <tbody>${summaries.map(row => `<tr><td>${escape(row.model)}</td><td>${row.n}</td><td>${row.success}/${row.n}</td></tr>`).join('')}</tbody></table></section>`
    : '<section class="results"><h2>低成本流程试跑</h2><p>尚未运行；当前页面只展示数据和 Oracle。</p></section>';
  const sections = DIFFICULTIES.map(difficulty => {
    const selectedModels = models.filter(model => model.difficulty === difficulty.id);
    const modelHtml = selectedModels.map(model => {
      const modelTasks = tasks.filter(task => task.sourceGroup === model.id);
      const taskHtml = modelTasks.map(task => {
        const taskResults = results.filter(row => row.taskId === task.id);
        const actionTrace = task.layer === 'procedural'
          ? `<details class="trace"><summary>逐步 Oracle 执行轨迹</summary><ol>${(task.oracle.actionIds as string[])
            .map((action, index) => `<li><b>Step ${index + 1}</b><code>${escape(action)}</code></li>`).join('')}</ol></details>`
          : '';
        const options = task.options?.length
          ? `<ol class="options">${task.options.map(option => `<li><b>${option.id}</b> ${escape(option.label)}</li>`).join('')}</ol>`
          : '';
        return `<article class="task" data-task-difficulty="${task.difficulty}" data-task-layer="${task.layer}">
          <figure><img loading="lazy" src="${task.visualization.detailImage}" alt="${escape(model.nameZh)} ${escape(task.family)}"></figure>
          <div class="task-copy">
            <span class="task-id">${task.id}</span>
            <div class="task-tags"><span>${task.difficulty}</span><span>${TASK_LAYERS.find(layer => layer.id === task.layer)!.nameZh}</span><span>${task.format}</span></div>
            <h4>${escape(task.family)}</h4>
            <p class="question">${escape(task.question)}</p>
            ${options}
            <dl><dt>能力</dt><dd>${task.capability.join(' · ')}</dd><dt>Oracle</dt><dd>${escape(task.oracleMethod)}</dd></dl>
            <details><summary>模型输入</summary><pre>${escape(pretty(task.input))}</pre></details>
            ${actionTrace}
            <details class="oracle"><summary>正确答案</summary><pre>${escape(pretty(task.oracle))}</pre></details>
            ${taskResults.length ? `<details><summary>低成本模型回答</summary><table><thead><tr><th>模型</th><th>结果</th><th>回答</th></tr></thead>
              <tbody>${taskResults.map(row => `<tr><td>${escape(row.model)}</td><td class="${row.success ? 'pass' : 'fail'}">${row.success ? '通过' : '失败'}</td>
              <td><code>${escape(JSON.stringify(row.answer))}</code></td></tr>`).join('')}</tbody></table></details>` : ''}
          </div>
        </article>`;
      }).join('');
      return `<section class="model" data-model-difficulty="${model.difficulty}">
        <div class="model-head">
          <div class="model-gallery"><img class="primary-view" src="images/models/${model.id}-iso.png" alt="${escape(model.nameZh)} 等轴视图">
          <div class="view-strip"><img src="images/models/${model.id}-front.png" alt="${escape(model.nameZh)} 正视图">
          <img src="images/models/${model.id}-side.png" alt="${escape(model.nameZh)} 侧视图">
          <img src="images/models/${model.id}-top.png" alt="${escape(model.nameZh)} 俯视图"></div></div>
          <div><span class="eyebrow">${model.difficulty} · ${escape(model.family)}</span>
          <h3>${escape(model.nameZh)}<small>${escape(model.name)}</small></h3>
          <p>${escape(model.description)}</p>
          <dl><dt>零件</dt><dd>${model.parts.length}</dd><dt>模块</dt><dd>${model.modules.length}</dd>
          <dt>关节</dt><dd>${model.joints.length}</dd><dt>复杂度指数</dt><dd>${model.complexity.complexityIndex}</dd></dl>
          <p class="notes">${model.designNotes.map(note => escape(note)).join(' · ')}</p></div>
        </div>${taskHtml}
      </section>`;
    }).join('');
    return `<section class="difficulty-band" data-difficulty-band="${difficulty.id}">
      <header class="difficulty-head"><span>${difficulty.id}</span><h2>${difficulty.nameZh} / ${difficulty.name}</h2>
      <p>${DIFFICULTY_INTENT_ZH[difficulty.id]}</p><dl><dt>典型零件</dt><dd>${difficulty.typicalParts.join('–')}</dd>
      <dt>操作步长</dt><dd>${difficulty.operationHorizon.join('–')}</dd><dt>耦合约束</dt><dd>${difficulty.coupledConstraints}</dd></dl></header>
      ${modelHtml}</section>`;
  }).join('');
  const html = `<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="icon" href="data:,"><title>BrickAtlas Hierarchy-1</title><style>
  *{box-sizing:border-box}body{margin:0;font:14px/1.55 Inter,"PingFang SC",Arial,sans-serif;color:#182128;background:#f2f5f6}
  .top{position:sticky;top:0;z-index:10;background:#fff;border-bottom:1px solid #ccd5d9;padding:14px 22px}.top h1{font-size:22px;margin:0}
  .top p{margin:3px 0 8px;color:#596770}.filters{display:flex;gap:7px;overflow:auto;padding:3px 0}.filters+ .filters{border-top:1px solid #e5eaec;margin-top:5px;padding-top:8px}
  button{border:1px solid #c7d1d6;background:#fff;padding:6px 10px;border-radius:5px;white-space:nowrap;cursor:pointer}
  button.active{background:#17242d;color:#fff;border-color:#17242d}.intro{background:#fff;padding:20px max(22px,calc((100% - 1280px)/2));border-bottom:1px solid #d9e0e3}
  .matrix-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:1280px;margin:18px auto}.matrix-grid figure{margin:0}.matrix-grid img{width:100%;border:1px solid #ccd5d9;border-radius:6px}
  main{max-width:1280px;margin:auto;background:#fff}.results{padding:20px 28px;border-bottom:8px solid #e7edef}.results table,details table{width:100%;border-collapse:collapse}
  th,td{text-align:left;padding:7px 9px;border-bottom:1px solid #dce3e6}.difficulty-band{border-bottom:12px solid #dce4e7}
  .difficulty-head{padding:26px 28px;background:#18242d;color:#fff}.difficulty-head>span{font-size:28px;font-weight:800;color:#f2bf3c}.difficulty-head h2{display:inline;margin:0 0 0 12px;font-size:23px}
  .difficulty-head p{max-width:820px;color:#dce4e7}.difficulty-head dl{display:flex;gap:10px 24px;flex-wrap:wrap}.difficulty-head dd{margin:0;color:#fff}
  .model{border-top:1px solid #dce3e6}.model-head{display:grid;grid-template-columns:minmax(380px,52%) 1fr;gap:28px;padding:28px}
  .model-gallery .primary-view,.task figure img{width:100%;aspect-ratio:4/3;object-fit:cover;border:1px solid #d2dade;border-radius:6px}
  .view-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:6px}.view-strip img{width:100%;aspect-ratio:4/3;object-fit:cover;border:1px solid #d2dade;border-radius:4px}
  .eyebrow,.task-id{font-size:11px;color:#687781;text-transform:uppercase}.model-head h3{font-size:25px;margin:7px 0}.model-head h3 small{display:block;font-size:14px;font-weight:400;color:#66757e}
  dl{display:grid;grid-template-columns:auto 1fr auto 1fr;gap:7px 14px}dt{font-weight:700}dd{margin:0}.notes{color:#52626b}
  .task{display:grid;grid-template-columns:minmax(330px,40%) 1fr;gap:24px;padding:24px 28px;border-top:1px solid #dce3e6}.task figure{margin:0}
  .task h4{font-size:19px;margin:5px 0}.task-tags{display:flex;gap:6px;flex-wrap:wrap}.task-tags span{padding:2px 6px;border:1px solid #c9d3d8;border-radius:4px;font-size:11px}
  .question{font-size:16px;font-weight:650}.options{padding-left:28px}.options li{padding:3px 0}.task dl{grid-template-columns:70px 1fr}
  details{border-top:1px solid #dce3e6;padding:8px 0}summary{cursor:pointer;font-weight:650}.oracle summary{color:#176b49}
  .trace ol{display:grid;gap:6px;padding-left:24px}.trace li{padding:6px 8px;background:#f1f5f3;border-left:3px solid #27865e}.trace li b{display:inline-block;width:62px}.trace li code{font-size:12px}
  pre{overflow:auto;background:#f1f4f5;padding:12px;font-size:12px}code{word-break:break-all;font-size:11px}.pass{color:#176b49;font-weight:700}.fail{color:#b02c25;font-weight:700}
  .hidden{display:none}@media(max-width:760px){.top{padding:11px}.top h1{font-size:20px}.intro{padding:16px}.matrix-grid{grid-template-columns:1fr;margin:12px 0}
  .model-head,.task{grid-template-columns:1fr;padding:18px}.difficulty-head{padding:20px 18px}.model-head dl{grid-template-columns:auto 1fr}.task dl{grid-template-columns:62px 1fr}
  .results{padding:18px;overflow:auto}th,td{padding:6px}.difficulty-head dl{display:grid;grid-template-columns:auto 1fr}}
  </style></head><body><header class="top"><h1>BrickAtlas Hierarchy-1 · 分层积木能力基准</h1>
  <p>18 个原创对象 · 4 个难度 · 90 道核心题 · 48 道 D3 Mechanism 扩展题</p>
  <nav class="filters difficulty-filters"><button class="active" data-difficulty="all">全部难度</button>${difficultyNav}</nav>
  <nav class="filters layer-filters"><button class="active" data-layer="all">全部题型</button>${layerNav}</nav></header>
  <section class="intro"><h2>横向看题型，纵向看难度</h2><p>每个对象固定包含两道原子单选，以及元认知/物理、可执行操作和综合约束题各一道。所有题目都从同层积木库派生。</p>
  <div class="matrix-grid"><figure><img src="LIBRARY_OVERVIEW.png" alt="四级积木库总览"></figure>
  <figure><img src="TASK_ABILITY_MATRIX.png" alt="难度与能力矩阵"></figure>
  <figure><img src="PILOT_HEATMAP.png" alt="低成本模型准确率热力图"></figure></div></section>
  <main>${resultSummary}${sections}</main><script>
  let difficulty='all',layer='all';
  function apply(){document.querySelectorAll('.difficulty-band').forEach(b=>b.classList.toggle('hidden',difficulty!=='all'&&b.dataset.difficultyBand!==difficulty));
  document.querySelectorAll('.task').forEach(t=>t.classList.toggle('hidden',(difficulty!=='all'&&t.dataset.taskDifficulty!==difficulty)||(layer!=='all'&&t.dataset.taskLayer!==layer)));}
  document.querySelectorAll('[data-difficulty]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-difficulty]').forEach(x=>x.classList.remove('active'));b.classList.add('active');difficulty=b.dataset.difficulty;apply();});
  document.querySelectorAll('[data-layer]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-layer]').forEach(x=>x.classList.remove('active'));b.classList.add('active');layer=b.dataset.layer;apply();});
  </script></body></html>`;
  writeFileSync(resolve(OUTPUT, 'index.html'), html.replace(/[ \t]+$/gm, '') + '\n');

  const questionBook = [
    '# BrickAtlas Hierarchy-1 问答库',
    '',
    '> 90 道核心题全部由 18 个原创对象派生；OMR/LDraw 不进入模型、题目或分数。',
    '',
  ];
  for (const difficulty of DIFFICULTIES) {
    questionBook.push(`## ${difficulty.id} ${difficulty.nameZh}`, '');
    for (const model of models.filter(candidate => candidate.difficulty === difficulty.id)) {
      questionBook.push(`### ${model.nameZh} / ${model.name}`, '');
      for (const task of tasks.filter(candidate => candidate.sourceGroup === model.id)) {
        questionBook.push(`#### ${task.layer} · ${task.family}`, '',
          `- 题目：${task.question}`,
          `- 形式：${task.format}`,
          `- 能力：${task.capability.join('、')}`,
          `- Oracle 方法：${task.oracleMethod}`,
          `- 答案：\`${JSON.stringify(task.oracle)}\``,
          `- 图片：[${task.id}](${task.visualization.detailImage})`, '');
      }
    }
  }
  writeFileSync(resolve(OUTPUT, 'QUESTION_BANK.zh-CN.md'), questionBook.join('\n'));

  const matrix = matrixRows(results);
  const report = [
    '# BrickAtlas Hierarchy-1 分层基准报告',
    '',
    '## 设计结论',
    '',
    'Mechanism-1 被保留为 D3 机构级，不再承担全部难度。Hierarchy-1 在其上下补充部件级、装配体级和系统级原创对象。',
    '难度不是只按零件数划分，还同时考虑模块数、运动关节、依赖深度、隐藏接口、耦合约束和操作步长。',
    '',
    '## 数据规模',
    '',
    `- 原创对象：${models.length}`,
    `- 可视零件：${models.reduce((sum, model) => sum + model.parts.length, 0)}`,
    `- 核心题：${tasks.length}`,
    '- D3 Mechanism-1 扩展题：48',
    `- 总问题数：${tasks.length + 48}`,
    '- 每个对象：2 道原子单选 + 1 道元认知/物理题 + 1 道操作题 + 1 道综合题',
    '',
    '## 难度层级',
    '',
    '| 难度 | 对象数 | 核心题 | 定义 |',
    '|---|---:|---:|---|',
    ...DIFFICULTIES.map(difficulty => `| ${difficulty.id} ${difficulty.nameZh} | ${models.filter(model => model.difficulty === difficulty.id).length} | ${tasks.filter(task => task.difficulty === difficulty.id).length} | ${DIFFICULTY_INTENT_ZH[difficulty.id]} |`),
    '',
    '## 四级原创积木库',
    '',
    '| 难度 | 对象 | 零件 | 模块 | 关节 | 复杂度指数 |',
    '|---|---|---:|---:|---:|---:|',
    ...models.map(model => `| ${model.difficulty} | ${model.nameZh} / ${model.name} | ${model.parts.length} | ${model.modules.length} | ${model.joints.length} | ${model.complexity.complexityIndex} |`),
    '',
    '## 任务层与能力',
    '',
    '| 任务层 | 题量 | 主要能力 |',
    '|---|---:|---|',
    ...TASK_LAYERS.map(layer => `| ${layer.nameZh} | ${tasks.filter(task => task.layer === layer.id).length} | ${LAYER_CAPABILITIES[layer.id]} |`),
    '',
    '## 横向与纵向对照',
    '',
    '- 四个难度都重复测量：模块识别、三维空间关系、局部改色和故障定位，形成纵向锚点。',
    '- D3 额外加入支撑锚点和位姿纠正；18 道 coverage 原子题共同覆盖全部 18 种原子操作。',
    '- 同一任务层的观察负担从 D1 单接口上升到 D4 跨工位、共享资源和 12–24 步操作链。',
    '- 每个对象的操作题都在网页中展示编号 Oracle 动作轨迹；每个对象提供等轴、正、侧、俯四视图。',
    '',
    '### 原子操作全集',
    '',
    `${tasks.filter(task => task.family === 'atomic-operation-coverage').map(task => task.operation).join('、')}。`,
    '',
    '### 元认知/物理题族',
    '',
    `${[...new Set(tasks.filter(task => task.layer === 'metacognitive').map(task => task.family))].join('、')}。`,
    '',
    '## 低成本流程试跑',
    '',
    summaries.length
      ? summaries.map(row => `- ${row.model}：${row.success}/${row.n}`).join('\n')
      : '- 尚未运行。',
    excludedRuns.length
      ? `- 未计分/已淘汰尝试：${excludedRuns.length} 次；均保留 run、ledger 与 reconciliation 证据。`
      : '- 未发生未计分或已淘汰尝试。',
    '',
    '| 难度 | 任务层 | 样本 | 正确 |',
    '|---|---|---:|---:|',
    ...matrix.map(row => `| ${row.difficulty} | ${row.layer} | ${row.n} | ${row.success} |`),
    '',
    '该试跑只覆盖固定的 4×4 分层样本，用于验证请求、解析、评分、汇总和热力图链路，不用于模型排名。',
    '',
    '## 科学边界',
    '',
    '- 四个难度目前是工程定义的开发层级，尚未经过真人作答时间、通过率和 IRT 难度标定。',
    '- D3 的物理任务有 Rapier 刚体、关节和 Shape Cast 证据；其他层的核心题同时包含符号约束与冻结响应表。',
    '- 当前 18 个对象都是公开开发对象；正式论文仍需新增隐藏、来源隔离的确认集。',
    '- 物理结果不是 LEGO 扣合力、ABS 形变、公差或机器人抓取实验的替代品。',
    '',
  ];
  writeFileSync(resolve(OUTPUT, 'HIERARCHY_REPORT.zh-CN.md'), report.join('\n'));
  console.log(JSON.stringify({
    models: models.length,
    tasks: tasks.length,
    results: results.length,
    html: 'index.html',
    report: 'HIERARCHY_REPORT.zh-CN.md',
  }));
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(import.meta.filename)) {
  composeHierarchy();
}
