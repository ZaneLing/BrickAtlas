import { readFileSync, existsSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { STUDY } from './protocol';
import { statistics } from './statistics';
import { replayStudy } from './results';
import { localStatus } from './local-status';
import { importVLM } from './import-local';
import { localStatistics } from './local-statistics';

export function writeStudyReport() {
  const replay = replayStudy(); statistics();
  const data = JSON.parse(readFileSync(resolve(STUDY, 'statistics.json'), 'utf8'));
  const local = importVLM(), state = localStatus(); localStatistics();
  const aggregate = new Map<string, { n: number; success: number }>();
  for (const r of data.groups) {
    const k = r.stratum.split('|').slice(0, 3).join(' / ');
    const value = aggregate.get(k) ?? { n: 0, success: 0 };
    value.n += r.n; value.success += Math.round(r.metrics.success.value * r.n); aggregate.set(k, value);
  }
  const audit = JSON.parse(readFileSync(resolve(STUDY, 'independent-audit.json'), 'utf8'));
  const body = `# v2 非人工研究补强：实际进展报告

本报告只列当前有产物支持的结果。完整目标未因本轮进展被缩小。
总体文字说明见 [OVERVIEW.zh-CN.md](OVERVIEW.zh-CN.md)。

## 已完成的新证据

- 两API模型674次主实验，24个共同留出对象、8策略各3对象及25个已知目录题。
- 固定对照56次：无图、错配图、符号参考、重复、同首答反思/反馈、相对表示。
- 两个run共${replay.reduce((n, r) => n + r.cases, 0)}次新增请求，新增费用$${replay.reduce((n, r) => n + r.newCost, 0).toFixed(8)}，全部收据已结算、分数可复算。
- ${audit.geometryCases}个正确/扰动结构，${audit.metricComparisons}项独立指标比对，没有差异。
- ${audit.relationCases}道关系独立算法一致；高度规划器全${audit.plans}道装拆通过。
- train-only检索覆盖${audit.retrievalCases}个非训练对象的重建题，无测试对象检索进训练索引。
- 严格schema版本拒绝数组冒充字符串；全117910真值与118640条既有记录的指标保持不变，5120个畸形答案被拒绝。
- 337道测试题的Torch/MLX输入token、像素与mask哈希全部一致；840行训练/验证数据及480张PNG已打包并核对。
- 全107520项错误答案/等价性检查通过：规划缺步、重复、未知ID和反序，编辑无操作，修复误报，结构ID与等价旋转。
- 1177条训练/验证/测试输入共1970图像使用、626独立渲染，全部重新渲染后与原题图片一致。

高度规划全通过意味着当前竖直插拔域不需要复杂搜索；不能再用贪心失败作为该域很难的证据。
独立checker只验证名义网格，不代表任意CAD、力学或语义真值正确。

## 主实验

| 模型 / 任务 / 变体 | n | 成功 |
| --- | ---: | ---: |
${[...aggregate].map(([k, v]) => `| ${k} | ${v.n} | ${v.success} |`).join('\n')}

变体不能当独立对象。当前对象仅24个，不能宣称具有充分统计功效。
更完整的格式/几何/表面/定位指标、分母、延迟、tokens及截断数见artifacts/study/statistics.json。

## 固定对照

| 条件 | n | 原始成功 | 对照成功 | 增益 / 退化 |
| --- | ---: | ---: | ---: | --- |
${data.paired.map((r: any) => `| ${r.arm} | ${r.n} | ${r.before} | ${r.after} | ${r.gains} / ${r.losses} |`).join('\n')}

每策略选首个已冻结对象，不按分数筛选。符号参考是额外真值信息；相对表示不等于连接器程序。
全零成功造成地板效应，不能根据无图与正常图都0分断言模型没有利用图像。
跨任务相关性按24个对象计算，常量边际返回null，不强行编造相关系数或显著性。

## 多模态训练状态

固定SmolVLM-256M、真实四视图、96训练对象/24验证对象、七装配任务。
每优化步512个监督答案tokens；单任务/多任务/留编辑任务各三个seed。
所有条件的正式推理统一MLX、无量化、完整337题和2200-token输出上限。
PyTorch未完成的测速样本已归档，不作为训练/模型对照成绩。
输入一致性测试核对token、像素及mask；不同数值kernel仍可能改变输出。

| job | 状态 | 优化步 | 监督tokens | 测试预测 |
| --- | --- | ---: | ---: | ---: |
${state.map(s => `| ${s.name} | ${s.status} | ${s.steps}/${s.targetSteps} | ${s.supervisedTokens} | ${s.predictions}/337 |`).join('\n')}

已完成并导入的训练run：${local.length}/10。未完成的run不计算训练收益。
匹配监督量和步数不代表相同输入/图像token、耗时或计算量。
验证NLL仅使用每任务固定两例，不代表全部168条验证样本。
840条训练/验证样本的题面token前缀与监督边界已逐条核对，最大完整序列5176。
337条测试oracle在SmolVLM tokenizer下最长1793 token，均未超过2200输出上限；
oracle仅用于离线长度诊断，没有附加到模型输入。
逐任务、变体、信息条件、split、seed的结果、配对变化及真实预算见local-statistics.json。

## 评分版本与复现

新提交的v2:score与网页评价默认采用v2-strict-schema-1；
score-legacy仅用于明确的历史复现。已有付费run不改写。
严格批量run同时保存缺答、原始坏答案、源码哈希与对象级统计；
replay按版本复算所有指标、所有分层与完整状态链。
旧解码器的类型转换漏洞曾真实存在，不因新增测试就声称历史软件绝对无错。

## 未完成目标

- 全部训练及对照输出完成前，不能报告多模态迁移结论。
- 目前仍缺充分规模多模型确认性实验、丰富真实外部结构和自由语义评价。
- 通用CAD连接/力学不在现有验证范围；需要新域协议，不能对网格结果外推。
- 独立人审按要求单列，当前没有完成的真实审核。
- 每环提供有范围的证据；不能承诺绝对无错或录用。
`;
  writeFileSync(resolve(STUDY, '../../study/REPORT.zh-CN.md'), body);
  return { apiRequests: replay.reduce((n, r) => n + r.cases, 0), completedTraining: local.length };
}
