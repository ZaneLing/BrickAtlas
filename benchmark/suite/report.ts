import { writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { wilson } from '../core/results';
import { ARTIFACTS, groupResults, type SuiteRun } from './storage';
import { summary } from './data';

export function report(run: SuiteRun) {
  const groups = groupResults(run);
  const percent = (v: number | null | undefined) => typeof v === 'number' ? (v * 100).toFixed(1) + '%' : 'N/A';
  const calls = run.results.flatMap(r => r.calls), cost = calls.reduce((n, c) => n + c.cost, 0);
  const manifest = summary();
  const text = `# BrickAtlas 多任务评测报告

## 运行与费用

- Run: ${run.id}
- 状态: ${run.status}; ${run.error ?? '无运行错误'}
- 协议: ${run.mode}; 输入结构表示: ${run.representation}
- 已处理 ${run.results.length}/${run.selection.length * run.models.length} 例，${calls.length} 次实际 OpenRouter 请求。
- 本次费用 $${cost.toFixed(8)}；campaign 历史累计 $${run.campaignAfter.toFixed(8)}，沿用 $4.50 上限。
- ${run.startedAt} -> ${run.completedAt}
- 错误JSON与错误答案算任务失败，网络/计费失败单列，不筛掉差结果。

## 数据范围

数据版本 ${manifest.version}：${manifest.models} 个程序化结构样本，${manifest.groups} 个去色/平移/yaw规范化几何组，
8 个结构族，${manifest.tasks} 个绝对表示任务。颜色变体不是新结构组；相对表示不是新独立样本。
两类结构整个留出为test_ood。此次模型试验是冻结的小规模分层抽样，不是全数据评测。
没有人工设计资产被伪装为已认证规则砖模型；OMR只读盘点另见数据卡。

## 分任务结果

| 模型 | 任务 | n | 网络错误 | 成功率 | 95% Wilson描述区间 | 格式率 | 状态合法率 | 费用 |
| --- | --- | ---: | ---: | --- | --- | --- | --- | ---: |
${groups.map(g => {
    const success = run.results.filter(r => r.model === g.model && r.kind === g.kind && r.status === 'complete')
      .reduce((n, r) => n + r.verdict.metrics.success, 0);
    return `| ${g.model} | ${g.kind} | ${g.n} | ${g.errors} | ${percent(g.metrics.success)} | ${wilson(success, g.n)?.map(percent).join(' - ') ?? 'N/A'} | ${percent(g.metrics.format)} | ${percent(g.metrics.valid)} | $${g.cost.toFixed(6)} |`;
  }).join('\n')}

宏平均仅用于同协议、同输入信息和同样本集合的描述，不合并one-shot与validator-once。
样本共享生成模板且每单元很少，区间不构成显著性或模型能力排名结论。

## 逐例与细项

| 模型 | taskId | family / split | 成功 | 指标 | 问题 |
| --- | --- | --- | --- | --- | --- |
${run.results.map(r => `| ${r.model} | ${r.taskId} | ${r.family} / ${r.split} | ${r.verdict.metrics.success} | ${Object.entries(r.verdict.metrics).map(([k, v]) => `${k}=${typeof v === 'number' ? v.toFixed(3) : 'N/A'}`).join('; ')} | ${r.error ?? r.verdict.issues.join(', ')} |`).join('\n')}

## 指标解释与不可测范围

- parts/relations: 类型正确的字段准确率，全部字段正确才成功。
- 重建/补全/编辑: 颜色、型号和对称足迹的最优精确多重集匹配；额外零件扣分；状态还须合法。
- Edge F1包括连接节点与实际对接stud数量；不是仅对BOM评分。
- 生成: 当前是受控文字+体积约束；任何合法的目录零件铺砌均可，比较占用IoU及允许颜色，不要求参考拆砖方式。
- 补全/编辑/修复: 独立报告非目标部分保持率。编辑覆盖改色、顶部复制增件、局部删件，尚非任意语义几何改造。
- 修复: 目标复原与故障定位都正确才成功，正常无故障样本报告误报；不是在线机械故障恢复。
- 规划: 检查任一完整顺序的逐步支撑、碰撞与垂直通道，不按唯一作者序列打分。
- 输入图像包含明确披露的逐层视图，不能称为单视图隐藏结构推断；relations/plan等结构任务是符号输入。
- 状态合法不等于承重稳定；不含机械手、机器人、VLA、力学扣合、非网格关节与连续运动。
- Oracle全量通过是裁判自测，不能拿来当学习模型分数。未进行神经网络微调，训练导出不是训练完成。

## 可复现证据

- Dataset hash: ${run.datasetHash}
- Protocol hash: ${run.protocolHash}
- Frozen selection hash: ${run.selectionHash}
- run.json: 输入、原始响应、解析答案、分数、每次generation ID/provider/tokens/cost。
- protocol.json: 请求前冻结的选择与提示词。
- ledger.json: campaign账本快照；frames/: 模型实际看到的PNG。
- 运行 suite:replay 会重新构造任务、解析原始响应、核对图片、计费收据与评分。

## 下一步

先根据分任务失败定位视觉识别、表示解码、关系推理和规划差异，再扩大held-out组数。
研究级发布仍需更广的有许可人工模型、完整连接器、语义生成评价、人工标签审计以及训练对照。
不要从本次小规模工程实验宣称超过BrickNet、BrickGPT或其他已发表基准。
`;
  writeFileSync(resolve(ARTIFACTS, 'runs', run.id, 'REPORT.md'), text);
  return text;
}
