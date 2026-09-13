import { writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { POSE_DIR, POSE_ARMS } from './pose-probes';
import { replayPoseProbes } from './pose-run';
import { VALIDATION_MODELS } from './validation-client';

export function poseReport() {
  const data = replayPoseProbes();
  const names: Record<string, string> = {
    'full-rgb': '完整结构/RGB', 'pose-rgb': '局部位姿/RGB', 'choice-rgb': '四选一/RGB',
    'choice-permuted': '四选一/置换', 'choice-no-image': '四选一/无图', 'pose-symbolic': '局部位姿/符号',
  };
  const label = (s: string) => s.split('/').slice(1).join('/');
  const frac = (arm: string, model: string) => {
    const row = data.summary.find(r => r.arm === arm && r.model === model)!;
    return `${row.successes}/${row.n}`;
  };
  const models = VALIDATION_MODELS.map(m => m.id);
  const total = (arm: string) => data.summary.filter(r => r.arm === arm).reduce((n, r) => n + r.successes, 0);
  const md = `# 局部位姿与候选判别：测量接口诊断

## 研究问题

延续论文的可审计多任务评测框架，本轮不扩大全量榜单，而是检验：
当模型不能输出正确完整结构时，它是否仍能恢复局部位姿，或在给定候选中识别正确布局？
通过图像/符号对照、输出形式对照、无图与候选置换对照，避免把所有失败归于“空间推理”。

## 协议

- 状态${data.status}，实际${data.responses}/${data.planned}次请求，费用$${data.newCost.toFixed(6)}，累计$${data.campaignAfter.toFixed(6)}。
- 四个不同来源、不同几何的两件前缀，排除前两轮已使用来源；统一灰底板/蓝查询件、最小XYZ=0，型号/BOM已给出。
- 四模型、六条件、每题一次提交；24题不是24个独立对象，重复配色和前缀不扩大统计样本。
- 图像组共用同一场景四视图；明确正交相机朝向、轴、单位、网格中心标签和位姿最低角定义。
- 四个候选均为合法结构、相同零件与朝向、高度，仅位置不同；标签A/B/C/D各正确一次。
- 置换只改变候选顺序，选择一致性按实际位姿而非标签比较；无图组保留候选、BOM和规则，随机猜测期望25%。
- 评分对180度等价方向和方砖朝向不惩罚，局部位姿按X/Y/Z/朝向分别报告；没有自动修正模型答案。

## 完整矩阵

| 条件 | ${models.map(label).join(' | ')} |
| --- | ${models.map(() => '---:').join(' | ')} |
${POSE_ARMS.map(arm => `| ${names[arm]} | ${models.map(model => frac(arm, model)).join(' | ')} |`).join('\n')}

分母为实际响应数；缺失项在analysis.json单列。服务失败不被当成模型认知失败。

## 局部位姿字段

| 模型 | 输入 | 格式合法 | X | Y | Z | 等价朝向 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
${data.summary.filter(r => r.arm.startsWith('pose')).map(r => `| ${label(r.model)} | ${names[r.arm]} | ${r.formatAccepted}/${r.n} | ${
      ['x', 'y', 'z', 'orientation'].map(k => `${r.fields[k].correct}/${r.fields[k].n}`).join(' | ')} |`).join('\n')}

## 置换一致性

| 模型 | 同一实际候选 | 两次均正确 | 配对场景 |
| --- | ---: | ---: | ---: |
${models.map(model => {
  const pairs = data.pairs.filter(p => p.model === model);
  return `| ${label(model)} | ${pairs.filter(p => p.sameSelectedPose === true).length}/${pairs.filter(p => p.sameSelectedPose !== null).length} | ${pairs.filter(p => p.bothCorrect).length} | ${pairs.filter(p => p.matched).length} |`;
}).join('\n')}

一致并不代表正确；始终选择同一错误位姿也会一致。每模型只有四组配对，不给出显著性或稳定排行榜结论。

## 判断

固定四模型合计：完整结构${total('full-rgb')}/16、局部位姿${total('pose-rgb')}/16、
四选一${total('choice-rgb')}/16、置换四选一${total('choice-permuted')}/16、
无图四选一${total('choice-no-image')}/16、符号位姿${total('pose-symbolic')}/16。
这里16次响应共享4个场景，不是16个独立样本。

${total('pose-rgb') > total('full-rgb')
    ? '局部位姿的精确成功数高于同场景完整结构，说明缩小输出目标在本样本中提供了不同测量信号。'
    : '局部位姿没有比完整结构获得更多精确成功，本轮不能支持“只缩短输出就能解除瓶颈”。'}
${total('choice-rgb') > total('choice-no-image')
    ? '给图四选一的成功数高于无图条件，有描述性的视觉条件差异；不能据此宣称统计显著或排除候选先验。'
    : '给图四选一没有高于无图基线，当前不支持该候选任务已可靠测到视觉增益；应保留这个负结果。'}
${total('pose-symbolic') > total('pose-rgb')
    ? '符号位姿高于图像位姿，支持继续区分输入信息条件。该对照提供了额外几何信息，不是纯粹的视觉因果干预。'
    : '符号输入未展示更高成功数，需要先核查基本接口再做感知归因。'}

四选一给出候选空间，和自由生成并不信息匹配；两件完整输出也很短，不能把差异直接叫“长序列生成失败”。
按模型看，完整结构与局部位姿的排序可不同；应检查同对象逐题分歧，而不是预设短输出总会更好。
置换前后的选择不稳定意味着候选题成绩必须连同顺序敏感性一起呈现。无图对照只有4题/模型，
即使超过25%的随机期望，也不能据此断言存在泄漏或视觉无效。
正确标签均衡不等于候选无偏；本轮候选只扰动位置，不能外推到型号、连接器或遮挡辨识。
本轮是基于先前结果设计的自适应开发实验，不是预注册确认研究；颜色高亮、已给型号和最小结构也限制外推。

## 对论文框架的修正

1. 贡献从“八任务数量更多”收敛到“同对象不同输入/输出协议下的能力测量与失败归因”；本轮是测量证据，不是新模型。
2. 主文分开呈现完整结构、局部位姿、候选识别，不能用某个条件替代另一条件的失败，也不混合成一个能力总分。
3. 原始预测、缺失项、费用、候选置换和字段错误进入补充材料；流程图明确模型、系统解析、事后评分边界。
4. 真正的确认性研究需在新的独立来源上冻结相机/输入协议，扩大来源与难度，保留无图/符号/顺序控制及人审。当前不宣称达到CVPR录取标准。

## 复现

\`node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts replay-pose-probes\`
离线检查固定输入、候选、源码、原响应和账单，不发起API调用。
protocol.json只冻结题目协议；oracle-audit.json是裁判侧材料，未发送给模型。
`;
  writeFileSync(resolve(POSE_DIR, 'REPORT.zh-CN.md'), md);
  return { status: data.status, responses: data.responses, newCost: data.newCost, totals: Object.fromEntries(POSE_ARMS.map(a => [a, total(a)])) };
}
