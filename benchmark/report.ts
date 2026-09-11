import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { summaries, type RunResult } from './core/results';
import type { Ledger } from './core/budget';

const root = dirname(fileURLToPath(import.meta.url));
const percent = (n: number | null) => n === null ? 'N/A' : `${(n * 100).toFixed(1)}%`;

export function writeReport(run: RunResult) {
  const diagnosticPath = resolve(root, 'results', run.id, 'diagnostics.json');
  const diagnostics = existsSync(diagnosticPath)
    ? JSON.parse(readFileSync(diagnosticPath, 'utf8')) as {
      status: string; ledger: Ledger;
      cases: { model: string; fault: string; status: string; finalExact: boolean;
        finalF1: number; faultTriggered: boolean; recoveryEligible: boolean; recoverySuccess: boolean | null;
        actions: number; cost: number; trace: unknown[] }[];
    } : null;
  const rows = summaries(run);
  const calls = run.episodes.flatMap(e => e.trace.map(t => t.response));
  const total = calls.reduce((s, c) => s + c.cost, 0);
  const finalLedger = diagnostics?.ledger ?? run.ledger;
  const campaign = finalLedger.charges.reduce((s, c) => s + (c.actual ?? 0), 0);
  const uncertain = finalLedger.charges.filter(c => c.status !== 'settled');
  const committed = finalLedger.charges.reduce((s, c) => s + (c.actual ?? c.reserved), 0);
  const diagnosticCost = diagnostics?.cases.reduce((s, c) => s + c.cost, 0) ?? 0;
  const diagnosticSection = diagnostics ? `## 条件化 Builder / 恢复诊断

主试验后追加 ${diagnostics.cases.length} 个小诊断，费用 $${diagnosticCost.toFixed(6)}，
${diagnostics.cases.reduce((s, c) => s + c.trace.length, 0)} 次真实推理。状态: ${diagnostics.status}。
**正确蓝图由 oracle 提供，模型仍需自己操作世界；这些成绩不计入主试验全流程成功率。**
所有诊断使用 seed=41、同一个横向内部结构，仅改变故障条件。每种条件只有一次运行。

| 模型 | 条件 | 最终 exact | 最终 F1 | 故障触发 | 可评恢复 | 恢复成功 | 模型决策 | API 费用 |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: |
${diagnostics.cases.map(c => `| ${c.model} | ${c.fault} | ${c.finalExact} | ${percent(c.finalF1)} | ${c.faultTriggered} | ${c.recoveryEligible} | ${c.recoverySuccess === null ? 'N/A' : c.recoverySuccess} | ${c.actions} | $${c.cost.toFixed(6)} |`).join('\n')}

诊断允许区分“结构理解/蓝图错误”和“执行/监控错误”，但不能用正确蓝图条件下的成功，
替代主动发现隐藏结构的证据。提前 finish、合法但错位的放置、漏检偏移均保留在原始记录中。
详见同目录 \`diagnostics.json\`；里面明确标注 \`blueprintSource: oracle\`。

` : '';
  const p95 = (values: number[]) => values.length
    ? [...values].sort((a, b) => a - b)[Math.ceil(values.length * 0.95) - 1] : 0;
  const paired = run.models.map(model => {
    const values = ['active', 'passive'].map(protocol => {
      const eps = run.episodes.filter(e => e.status === 'complete' && e.model === model
        && e.protocol === protocol && e.seed === 41 && e.fault === 'none');
      return `${eps.filter(e => e.score.anatomy.exact).length}/${eps.length}`;
    });
    return `| ${model} | ${values[0]} | ${values[1]} |`;
  });
  const failures = run.episodes.filter(e => !e.score.lifecycleSuccess).map(e => {
    const invalid = e.trace.filter(t => !['accepted', 'submitted', 'handoff'].includes(t.feedback))
      .map(t => t.feedback);
    return `| ${e.model} | ${e.protocol} / ${e.taskId} | ${e.status} | ${e.score.anatomy.missing} | ${e.score.construction.missing} | ${[...new Set(invalid)].join(', ') || 'final state mismatch'} |`;
  });
  const content = `# Brick Atlas CARE-mini v1 Benchmark 报告

## 结论与范围

- 运行 ID: \`${run.id}\`
- 开始: ${run.startedAt}; 结束: ${run.completedAt}; 状态: **${run.status}**
- 已执行 ${run.episodes.length}/${run.plannedEpisodes} 个 episode，${calls.length} 次真实 OpenRouter 推理请求。
- 本轮已核账推理费用 **$${total.toFixed(6)}**；本地 campaign 累计已核账 **$${campaign.toFixed(6)}**。
- 追加条件化诊断 ${diagnostics?.cases.length ?? 0} 例，费用 **$${diagnosticCost.toFixed(6)}**；本次交付合计 **$${(total + diagnosticCost).toFixed(6)}**。
- 含未核账预留的 campaign 占用 **$${committed.toFixed(6)}**；硬预算 $${run.ledger.cap.toFixed(2)}，相对用户 $5 上限保留 $0.50 缓冲。
- 未结账请求: ${uncertain.length}。费用来自响应的 \`usage.cost\`，不是价格乘 token 的估算；不含充值手续费、汇率或本地算力成本。
- 这是工程 pilot，不是 SOTA 排行榜、不证明优于既有 benchmark，不作显著性或通用因果智能结论。
${run.error ? `- 运行停止原因: ${run.error}\n` : ''}
## 实现的评测

v1 为独立的 \`benchmark/\` 模块，没有改动原项目的 src、模型资产、根 package 或路由。
复用既有 React、Three.js、Playwright 和 TypeScript 依赖。原有 15 个 OMR 模型没有被全量测试。

| 项目 | v1 实际实现 |
| --- | --- |
| 任务 | 4 个配置，来自一个 8 块密封盒结构族；2 个颜色/ID 种子；水平/纵向内部排列 |
| 主协议 | RGB + 可见零件身份；离散网格编辑与有序批量放置 |
| Active | 可以拆除外部覆盖件，再提交蓝图 |
| Passive | 同样的视角和库存，但检查阶段禁止拆解 |
| Handoff | 同型号模型的新上下文，只收到蓝图与当前库存，不含探索历史 |
| 故障 | 无故障、顶盖缺失、顶盖合法偏移；环境不通知故障位置 |
| 蓝图 | 有序零件/颜色/绝对网格位姿数组，确定性执行并派生 stud 接触图 |
| 预算 | 每 episode 最多 14 次决策、48 次 primitive 编辑，每批最多 12 块 |
| 物理 | 仅矩形砖体无重叠、整数 stud 对接、下方至少一个支撑 stud、向上拆卸通道 |

**未实现**: 承重/重心/扣合力、真实机器人、非标准连接器、完整连续 SE(3)、
跨型号 Builder 泛化、步骤 DAG、任意 OMR 解剖、最优修复 regret 和真实世界实物验证。
这不是完整 CARE 旗舰版；不把连接分量变化等同于力学因果预测。

## 数据与条件

- 一共仅两种隐藏几何布局，样本规模刻意保持小，符合本次成本控制要求。两者的粗粒度砖间连接图同构，v1 不声称测出了不同的力学因果拓扑。
- 每个配对使用相同外壳、BOM、可见句柄、背景和镜头；模型不会收到任务 seed、variant、fault 或私有目标位姿。
- 初始可见身份采用本结构族的闭壳遮挡规则，不宣称通用像素检测器或 RGB-only 感知。
- 已观察零件的身份/颜色免费提供；几何坐标需要从图像和目录推断。
- 三维图像由 Three.js 生成；视觉几何为标准砖的程序化近似，不是完整 LDraw 管/底面。
- 两个低成本视觉模型为可运行性抽样，不代表当前最强模型或全系列模型。
- public-pilot 的程序、结果、观测图像和最终蓝图均公开，用于复现而不是隐藏测试集。
- 配对像素一致性由独立 renderer 测试检查；只有对固定允许视角、无额外侧信道的条件才适用不可区分性论证。
- 故障在足够多的成功放置后触发，若未达到条件或没有可操作顶盖则记未触发，绝不记为恢复成功。

## 结果

表中 n 只统计正常结束的 episode；基础设施/API 失败单列为 errors。
Active 含 2 个干净任务和 2 个故障任务；Passive 仅含相同的 2 个干净配对。
**两者总平均不可直接解释为主动干预提升。**

| 模型 | 协议 | n | errors | 全流程成功 | 95% Wilson 区间 | 蓝图 Part F1 | 最终 Part F1 | 最终 Edge F1 | 蓝图可执行 | API 费用 |
| --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- | ---: |
${rows.map(r => `| ${r.model} | ${r.protocol} | ${r.n} | ${r.errors} | ${r.successes}/${r.n} | ${r.ci95 ? r.ci95.map(percent).join(' - ') : 'N/A'} | ${percent(r.anatomyF1)} | ${percent(r.finalF1)} | ${percent(r.edgeF1)} | ${percent(r.blueprintExecutable)} | $${r.cost.toFixed(6)} |`).join('\n')}

### 干净配对的主动/被动对照

仅比较 seed=41、无故障的同一对目标，分子为蓝图精确复原数。

| 模型 | Active exact anatomy | Passive exact anatomy |
| --- | --- | --- |
${paired.join('\n')}

每种协议仅两例，置信区间很宽；两个配对目标不是独立模型族，Wilson 区间仅作描述，
不能代替按结构族聚类的统计分析。禁止据此宣称因果效应大小或可靠模型排名。

### 恢复与行为

| 模型 | 协议 | 有效恢复成功/可评恢复 | 非法动作 | 平均决策 | 付费请求 |
| --- | --- | --- | ---: | ---: | ---: |
${rows.map(r => `| ${r.model} | ${r.protocol} | ${r.recoverySuccesses}/${r.recoveryEligible} | ${r.invalidActions} | ${r.averageActions?.toFixed(1) ?? 'N/A'} | ${r.calls} |`).join('\n')}

恢复指标仅统计**故障发生前已经精确建成**的 episode；其余是建造失败或混合错误，不当成独立恢复测量。
分母为 0 表示 N/A，而不是 0% 或 100%。没有 oracle 提供故障位置，也没有自动纠正模型输出。

${diagnosticSection}
## 逐 episode

| 模型 | 协议 | task | 故障 | 解剖 exact | 最终 exact | 故障触发 | 恢复可评 | 全流程成功 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
${run.episodes.map(e => `| ${e.model} | ${e.protocol} | ${e.taskId} | ${e.fault} | ${e.score.anatomy.exact} | ${e.score.construction.exact} | ${e.score.faultTriggered} | ${e.score.faultEligible} | ${e.score.lifecycleSuccess} |`).join('\n')}

### 失败证据

此表按确定性日志归类，不用另一个 LLM 代替裁判。missing 是在型号、颜色、网格位姿均匹配意义下缺失的目标实例数。

| 模型 | episode | 状态 | 蓝图未匹配目标 | 最终未匹配目标 | 环境反馈 |
| --- | --- | --- | ---: | ---: | --- |
${failures.length ? failures.join('\n') : '| All | All | complete | 0 | 0 | No failures observed in this small pilot |'}

## 评分定义

1. \`Part F1 = 2 * matched / (targetCount + outputCount)\`。同型号、颜色、网格位姿的实例按多重集匹配，忽略 ID。
2. 正方形砖 yaw 对称；长方形 180 度对称。使用最小 X/Z 锚点和实际 footprint 判等，重复砖不会重复得分。
3. Edge F1 比较匹配节点间的连接边；这里是砖间 stud 接触，不是任意连接器端口类型图。
4. exact 要求全部实例匹配、没有多余零件、世界状态在上述离散规则内合法。
5. Blueprint executable 独立检查蓝图顺序在库存和放置规则下可执行；能执行不等于目标正确。
6. Lifecycle success 要求有效蓝图、解剖 exact、最终 exact、episode 结束；故障任务还必须实际触发故障。
7. 拆解前预测评估 newlyVisible 和移除后 components 的联合准确率；不输出预测计错误，无拆解计 N/A。
8. 错误但合法的放置会保留；没有 ghost、参考目标吸附、目标匹配奖励或人工补答案。
9. v1 的 place 是离散位姿放置，不检查从空中到目标位置的连续插入扫掠路径。故不能根据它认证“无阻挡装配顺序”；detach 单独检查上方通道。

## 成本与可复现性

- 本轮 prompt tokens: ${calls.reduce((s, c) => s + c.promptTokens, 0)}
- 本轮 completion tokens: ${calls.reduce((s, c) => s + c.completionTokens, 0)}
- 本轮 reasoning tokens: ${calls.reduce((s, c) => s + c.reasoningTokens, 0)}
- 请求延迟 P95: ${(p95(calls.map(c => c.latencyMs)) / 1000).toFixed(2)} s
- 模型 temperature=0，max_tokens=2200；Gemini 显式关闭可选 reasoning；供应商路由按价格、不允许 fallback。
- 每次调用发送前按文本字节上界、图像保守 token 额度、输出上限与 provider max_price 预留费用。
- campaign ledger 在 \`.runtime/\` 持久化；CLI 和网页共用排他锁。超时/未知账单保留预留并停止整个运行。
- API key 仅在服务端进程读取既有忽略的 .env，不进入浏览器、Git、请求日志或结果。
- 本地管理员可信；模型只能看到 runner 传入的图文，不能读本机文件。v1 不是抵抗恶意本地用户的远程执行沙箱。
- protocol SHA256: \`${run.protocolHash}\`
- task spec SHA256: \`${run.taskHash}\`
- source SHA256: \`${run.sourceHash}\`
- \`run.json\` 保留逐请求 generation ID、provider、原始模型输出、动作、环境反馈、cost 与 token；\`observations/\` 保留内容寻址 PNG。

## 验证与下一步

运行 \`npm test\` 验证评分对称性、重复件、合法/非法顺序、遮挡、故障和预算；
运行 \`npm run test:ui\` 验证隔离的页面、四个视角下双胞胎像素一致性、交互与响应式布局。
这些是实现验证，不是人类或模型 benchmark 的替代成绩，具体本轮验证结果见 \`verification.json\`（若存在）。

下一版应先增加非同构结构族、真正隐藏的服务端生成任务和更稳健的视觉坐标呈现，
再扩大模型集合。补齐物理连接器和独立稳定性求解之前，不把 v1 结果包装为真实物理装配能力。

## 相关工作与边界

- LTRON / Break and Make: https://arxiv.org/abs/2207.13738
- InstructioNet: https://arxiv.org/abs/2410.01111
- BC-Bench / Brick-Composer: https://arxiv.org/abs/2606.05445
- BrickNet: https://arxiv.org/abs/2604.22984
- BrickSim: https://arxiv.org/abs/2603.16853
- OpenRouter usage.cost: https://openrouter.ai/docs/guides/guides/usage-accounting

本轮只建立可运行的主动/被动配对、隔离蓝图交接和故障恢复测试链路；
它没有证明任何一项能力在所有既有工作中都未被测过。
`;
  writeFileSync(resolve(root, 'results', run.id, 'REPORT.zh-CN.md'), content);
  return content;
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const latest = JSON.parse(readFileSync(resolve(root, 'results/latest.json'), 'utf8')) as { id: string };
  const run = JSON.parse(readFileSync(resolve(root, 'results', latest.id, 'run.json'), 'utf8')) as RunResult;
  writeReport(run);
  console.log(`Report written: results/${run.id}/REPORT.zh-CN.md`);
}
