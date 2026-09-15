import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { mechanismModels } from './models';
import { mechanismTasks } from './tasks';
import { OUTPUT } from './release';

const LABELS = {
  'prefix-dynamics': ['全过程前缀动力学', '逐步装配时是否出现坠落、失稳或错误依赖'],
  'insertion-access': ['连续路径可达性', '工具或零件的扫掠体能否无碰撞到达维修界面'],
  'fault-recovery': ['故障诊断与最小返工', '从动力学后果定位故障关节并给出最小维修'],
  'inventory-substitution': ['有限库存替代', '缺件时满足成本、数量和刚度约束的替代'],
  'dynamic-robustness': ['动态扰动鲁棒性', '冲击下的最大瞬态位移和残余位移'],
  'functional-kinematics': ['功能与运动学正确性', '铰链、滑轨、转台或旋翼能否完成目标运动'],
  'active-inspection': ['主动检查与澄清', '选择单位成本信息增益最高的下一次检查'],
  'multiobjective-design': ['多目标工程权衡', '识别成本、质量、刚度之间的 Pareto 解'],
} as const;

const CAPABILITY_ZH: Record<string, string> = {
  'long-horizon planning': '长程规划',
  'prefix dynamics': '前缀动力学',
  'causal support': '因果支撑',
  'continuous collision checking': '连续碰撞检测',
  'assembly accessibility': '装配可达性',
  'service planning': '维修规划',
  'fault localization': '故障定位',
  'causal diagnosis': '因果诊断',
  'minimum repair': '最小返工',
  'finite inventory': '有限库存',
  'structural substitution': '结构替代',
  'constraint satisfaction': '约束满足',
  'dynamic physical reasoning': '动态物理推理',
  'impulse robustness': '冲击鲁棒性',
  'failure threshold estimation': '失效阈值估计',
  'joint semantics': '关节语义',
  'functional prediction': '功能预测',
  'kinematic reasoning': '运动学推理',
  'active perception': '主动感知',
  'information gain': '信息增益',
  'cost-aware clarification': '成本敏感澄清',
  'Pareto reasoning': 'Pareto 推理',
  'cost-mass-stiffness trade-off': '成本-质量-刚度权衡',
  'engineering design': '工程设计',
};

const escape = (value: unknown) => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const pretty = (value: unknown) => JSON.stringify(value, null, 2);

export async function composeMechanism() {
  const models = mechanismModels(), tasks = await mechanismTasks();
  const resultRows: Array<{ taskId: string; model: string; answer: unknown; success: number }> = [];
  const localRawPath = resolve(OUTPUT, 'results/local-qwen3-0.6b.json');
  const localScorePath = resolve(OUTPUT, 'results/local-qwen3-0.6b.scores.json');
  if (existsSync(localRawPath) && existsSync(localScorePath)) {
    const raw = JSON.parse(readFileSync(localRawPath, 'utf8'));
    const scores = JSON.parse(readFileSync(localScorePath, 'utf8'));
    for (const row of raw) resultRows.push({ taskId: row.id, model: 'Qwen3-0.6B 本地文本',
      answer: row.answer, success: scores.rows.find((score: any) => score.id === row.id)?.result.success ?? 0 });
  }
  const latestPath = resolve(OUTPUT, 'results/latest.json');
  if (existsSync(latestPath)) {
    const latest = JSON.parse(readFileSync(latestPath, 'utf8'));
    const run = JSON.parse(readFileSync(resolve(OUTPUT, 'results', latest.path), 'utf8'));
    for (const row of run.results) resultRows.push({ taskId: row.taskId,
      model: row.model === 'openai/gpt-4.1-mini' ? 'GPT-4.1 mini' : 'Gemini 2.5 Flash',
      answer: row.answer, success: row.verdict.success });
  }
  const modelNames = [...new Set(resultRows.map(row => row.model))];
  const summaryRows = modelNames.map(model => {
    const selected = resultRows.filter(row => row.model === model);
    return { model, success: selected.filter(row => row.success).length, total: selected.length };
  });
  const summaryHtml = summaryRows.length ? `<section class="results-summary"><h2>模型实测总览</h2>
    <table><thead><tr><th>模型</th><th>Exact Success</th><th>说明</th></tr></thead><tbody>
    ${summaryRows.map(row => `<tr><td>${row.model}</td><td>${row.success} / ${row.total}</td>
      <td>${row.model.includes('本地') ? '纯文本小模型基线' : '单图 + 结构输入，固定最小 Harness'}</td></tr>`).join('')}
    </tbody></table></section>` : '';
  const taskNav = Object.entries(LABELS).map(([kind, [label]]) =>
    `<button data-filter="${kind}">${label}</button>`).join('');
  const sections = models.map(model => {
    const rows = tasks.filter(task => task.sourceGroup === model.id).map(task => {
      const [label, purpose] = LABELS[task.kind];
      const displayInput = { ...task.input };
      delete (displayInput as any).model;
      const taskResults = resultRows.filter(row => row.taskId === task.id);
      return `<article class="task-row" data-kind="${task.kind}">
        <figure><img loading="lazy" src="${task.visualization.detailImage}" alt="${escape(model.nameZh)} ${label}"></figure>
        <div class="task-copy">
          <header><span class="task-index">${escape(task.id)}</span><h3>${label}</h3></header>
          <p class="purpose">${purpose}</p>
          <p class="question">${escape(task.question)}</p>
          <dl><dt>对应能力</dt><dd>${task.capability.map(c => CAPABILITY_ZH[c] ?? c).join(' · ')}</dd>
          <dt>验证器</dt><dd>${['prefix-dynamics', 'insertion-access', 'dynamic-robustness', 'functional-kinematics'].includes(task.kind)
            ? 'Rapier 3D 刚体/关节/Shape Cast' : task.kind === 'active-inspection' ? '有限世界信息增益'
              : '结构约束与最小动作评分器'}</dd></dl>
          <details><summary>模型实际输入</summary><pre>${escape(pretty(displayInput))}</pre></details>
          <details class="oracle"><summary>Oracle / 正确答案</summary><pre>${escape(pretty(task.oracle))}</pre></details>
          ${taskResults.length ? `<details><summary>模型回答与得分</summary>
            <table class="answer-table"><thead><tr><th>模型</th><th>结果</th><th>回答</th></tr></thead><tbody>
            ${taskResults.map(row => `<tr><td>${row.model}</td><td class="${row.success ? 'pass' : 'fail'}">${row.success ? '通过' : '失败'}</td>
              <td><code>${escape(JSON.stringify(row.answer))}</code></td></tr>`).join('')}</tbody></table></details>` : ''}
        </div>
      </article>`;
    }).join('');
    return `<section class="model-section" data-model="${model.id}">
      <div class="model-overview">
        <img src="images/models/${model.id}-iso.png" alt="${escape(model.nameZh)}">
        <div><span class="eyebrow">原创机构型对象 · ${model.domain}</span>
        <h2>${model.nameZh}<small>${model.name}</small></h2>
        <p>${model.description}</p>
        <dl><dt>可视零件</dt><dd>${model.parts.length}</dd><dt>刚体模块</dt><dd>${model.modules.length}</dd>
        <dt>物理关节</dt><dd>${model.joints.length}</dd><dt>任务</dt><dd>8 类</dd></dl></div>
      </div>${rows}</section>`;
  }).join('');
  const html = `<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,">
  <title>BrickAtlas Mechanism-1 Case Browser</title>
  <style>
  *{box-sizing:border-box}body{margin:0;font:14px/1.55 Inter,Arial,sans-serif;color:#172027;background:#f5f7f8}
  .top{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid #d9e0e3;padding:14px 24px}
  .top h1{font-size:21px;margin:0 0 8px}.top p{margin:0;color:#59666f}.filters{display:flex;gap:6px;overflow:auto;margin-top:12px}
  button{border:1px solid #cbd4d9;background:#fff;padding:7px 10px;border-radius:5px;white-space:nowrap;cursor:pointer}
  button.active{background:#172027;color:#fff;border-color:#172027}main{max-width:1260px;margin:auto;background:#fff}
  .notice{padding:14px 24px;background:#fff4d8;border-bottom:1px solid #ecd491}
  .model-section{border-bottom:8px solid #eef2f4}.model-overview{display:grid;grid-template-columns:minmax(380px,55%) 1fr;gap:28px;padding:28px}
  .model-overview>img{width:100%;aspect-ratio:4/3;object-fit:cover;border:1px solid #d7dfe3;border-radius:6px}
  .eyebrow,.task-index{font-size:11px;text-transform:uppercase;color:#687780}.model-overview h2{font-size:26px;margin:8px 0}
  .model-overview h2 small{display:block;font-size:14px;font-weight:400;color:#67747c}.model-overview dl{display:grid;grid-template-columns:auto 1fr auto 1fr;gap:8px 16px}
  dt{font-weight:700}dd{margin:0}.task-row{display:grid;grid-template-columns:minmax(340px,42%) 1fr;border-top:1px solid #dfe5e8;padding:24px 28px;gap:26px}
  figure{margin:0}figure img{width:100%;aspect-ratio:4/3;object-fit:cover;border:1px solid #d7dfe3;border-radius:6px}
  .task-copy h3{font-size:19px;margin:3px 0}.purpose{color:#53616a;margin:0 0 10px}.question{font-size:16px;font-weight:650}
  .task-copy dl{display:grid;grid-template-columns:76px 1fr;gap:6px 12px;padding:10px 0;border-top:1px solid #e2e7e9}
  details{border-top:1px solid #e2e7e9;padding:8px 0}summary{cursor:pointer;font-weight:650}pre{overflow:auto;background:#f3f5f6;padding:12px;font-size:12px}
  .oracle summary{color:#176b49}.results-summary{padding:20px 28px;border-bottom:8px solid #eef2f4}.results-summary table,.answer-table{width:100%;border-collapse:collapse}
  th,td{text-align:left;padding:7px 9px;border-bottom:1px solid #dfe5e8}.pass{color:#176b49;font-weight:700}.fail{color:#b02c25;font-weight:700}
  code{font-size:11px;word-break:break-all}.hidden{display:none}@media(max-width:760px){.model-overview,.task-row{grid-template-columns:1fr;padding:18px}.top{padding:12px}.model-overview dl{grid-template-columns:auto 1fr}}
  </style>
  <header class="top"><h1>BrickAtlas Mechanism-1 · 全部 Case 可视化</h1>
  <p>6 个原创整体机构，48 道题。OMR/LDraw 仅作为复杂度参考，不是本数据集 case。</p>
  <nav class="filters"><button class="active" data-filter="all">全部</button>${taskNav}</nav></header>
  <div class="notice"><strong>读图方式：</strong>每题同时显示对象、问题、对应能力、模型实际输入、确定性 Oracle 和验证器。红/深色高亮表示本题关注模块；路径题绿色为可行路径、红色为碰撞路径。</div>
  <main>${summaryHtml}${sections}</main>
  <script>document.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-filter]').forEach(x=>x.classList.remove('active'));b.classList.add('active');const f=b.dataset.filter;document.querySelectorAll('.task-row').forEach(r=>r.classList.toggle('hidden',f!=='all'&&r.dataset.kind!==f));});</script>`;
  writeFileSync(resolve(OUTPUT, 'index.html'), html);

  const md = [`# BrickAtlas Mechanism-1 全部题目`, '',
    '> OMR/LDraw 只用于设计复杂度参考，不是本套件 case。以下 48 道题全部来自 6 个原创机构对象。', ''];
  if (summaryRows.length) {
    md.push('## 模型实测总览', '', '| 模型 | Exact Success |', '|---|---:|',
      ...summaryRows.map(row => `| ${row.model} | ${row.success}/${row.total} |`), '');
  }
  for (const model of models) {
    md.push(`## ${model.nameZh} / ${model.name}`, '', model.description, '',
      `- 可视零件：${model.parts.length}`,
      `- 刚体模块：${model.modules.length}`,
      `- 物理关节：${model.joints.length}`, '');
    for (const task of tasks.filter(t => t.sourceGroup === model.id)) {
      const [label, purpose] = LABELS[task.kind];
      md.push(`### ${label}`, '', `- **题目**：${task.question}`,
        `- **考察目标**：${purpose}`,
        `- **对应能力**：${task.capability.map(c => CAPABILITY_ZH[c] ?? c).join('、')}`,
        `- **可视化**：[查看图片](${task.visualization.detailImage})`,
        `- **Oracle**：\`${JSON.stringify(task.oracle)}\``,
        ...resultRows.filter(row => row.taskId === task.id)
          .map(row => `- **${row.model}**：${row.success ? '通过' : '失败'}，\`${JSON.stringify(row.answer)}\``), '');
    }
  }
  writeFileSync(resolve(OUTPUT, 'CASEBOOK.zh-CN.md'), md.join('\n'));
  if (summaryRows.length) {
    writeFileSync(resolve(OUTPUT, 'MODEL_REPORT.zh-CN.md'), [
      '# Mechanism-1 模型实测汇总', '',
      '| 模型 | Exact Success |', '|---|---:|',
      ...summaryRows.map(row => `| ${row.model} | ${row.success}/${row.total} |`), '',
      '逐题回答、Oracle 和可视化见 `index.html` 与 `CASEBOOK.zh-CN.md`。', '',
    ].join('\n'));
  }
  console.log(JSON.stringify({ html: 'index.html', markdown: 'CASEBOOK.zh-CN.md', tasks: tasks.length }));
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(import.meta.filename)) {
  await composeMechanism();
}
