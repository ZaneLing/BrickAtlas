import assert from 'node:assert/strict';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { getSpec, taskForV2 } from '../v2/cases';
import type { PublicTask } from '../shared';
import { evaluateStrict } from './strict-evaluate';
import { parseJSON } from '../score';
import { key, decode } from '../geometry';
import { FAILURE_STAGES } from './failure-diagnostics';
import { VALIDATION_DIR, replayModelValidation } from './model-validation';

export function classifyPatterns(patterns: Array<Array<number | null>>) {
  const complete = patterns.length > 0 && patterns.every(p => p.length > 0 && p.every(v => v !== null));
  return {
    modelOutcomesDiffer: complete && new Set(patterns.map(p => JSON.stringify(p))).size > 1,
    aggregateCountsDiffer: complete && new Set(patterns.map(p => p.reduce<number>((n, v) => n + (v ?? 0), 0))).size > 1,
    classification: !complete ? 'incomplete' : patterns.every(p => p.every(v => v === 0)) ? 'floor'
      : patterns.every(p => p.every(v => v === 1)) ? 'ceiling' : 'mixed',
  };
}

export function copyInputAnswer(input: PublicTask): unknown {
  if (!['complete', 'edit', 'repair'].includes(input.kind) || !input.input.current) return null;
  const structure = structuredClone(input.input.current);
  return input.kind === 'repair' ? { structure, faultIds: [] } : structure;
}

export function validationAggregate(rows: any[], planned: number) {
  assert.ok(rows.length <= planned);
  const keys = [...new Set<string>(rows.flatMap(r => Object.keys(r.diagnosis.verdict.metrics)))];
  const metric = (key: string) => {
    const values = rows.map(r => r.diagnosis.verdict.metrics[key]).filter((v): v is number => typeof v === 'number');
    return { value: values.length ? values.reduce((n, v) => n + v, 0) / values.length : null, denominator: values.length };
  };
  return { planned, returned: rows.length, missing: planned - rows.length,
    successes: rows.filter(r => r.diagnosis.verdict.metrics.success === 1).length,
    formatAccepted: rows.filter(r => r.diagnosis.formatAccepted).length,
    truncated: rows.filter(r => r.diagnosis.tokenLimitReached).length,
    stages: Object.fromEntries(FAILURE_STAGES.map(s => [s, rows.filter(r => r.diagnosis.stage === s).length])),
    metrics: Object.fromEntries(keys.map(k => [k, metric(k)])),
    cost: rows.reduce((n, r) => n + r.call.cost, 0),
    inputTokens: rows.reduce((n, r) => n + r.call.promptTokens, 0),
    outputTokens: rows.reduce((n, r) => n + r.call.completionTokens, 0),
    reasoningTokens: rows.reduce((n, r) => n + r.call.reasoningTokens, 0),
    latencyMs: rows.length ? rows.reduce((n, r) => n + r.call.latencyMs, 0) / rows.length : null };
}

export function validationReport() {
  const replay = replayModelValidation();
  const ladderFile = resolve(VALIDATION_DIR, 'ladder/replay.json');
  const ladder = existsSync(ladderFile) ? JSON.parse(readFileSync(ladderFile, 'utf8')) : null;
  const normalizedFile = resolve(VALIDATION_DIR, 'ladder-normalized/replay.json');
  const normalized = existsSync(normalizedFile) ? JSON.parse(readFileSync(normalizedFile, 'utf8')) : null;
  const run = JSON.parse(readFileSync(resolve(VALIDATION_DIR, 'run.json'), 'utf8'));
  const protocol = JSON.parse(readFileSync(resolve(VALIDATION_DIR, 'protocol.json'), 'utf8'));
  const mainInputs = protocol.rows.filter((r: any) => r.arm === 'ordinary');
  const taskKeys = [...new Set<string>(mainInputs.map((r: any) => {
    const s = getSpec(r.caseId); return `${s.kind}/${s.variant}`;
  }))];
  const models: string[] = protocol.models.map((m: any) => m.id);
  const primary = run.rows.filter((r: any) => r.arm === 'ordinary');
  const tasks = taskKeys.map(task => {
    const inputs = mainInputs.filter((r: any) => { const s = getSpec(r.caseId); return `${s.kind}/${s.variant}` === task; });
    const byModel = models.map(model => ({ model, ...validationAggregate(primary.filter((r: any) =>
      r.model === model && inputs.some((i: any) => i.id === r.id)), inputs.length) }));
    const signatures = models.map(model => inputs.map((input: any) =>
      primary.find((r: any) => r.model === model && r.id === input.id)?.diagnosis.verdict.metrics.success ?? null));
    return { task, byModel, ...classifyPatterns(signatures) };
  });
  const byModel = models.map(model => ({ model,
    ...validationAggregate(primary.filter((r: any) => r.model === model), mainInputs.length) }));
  const sizes = protocol.chosen.flatMap((o: any) => models.map(model => ({ model, ...o,
    ...validationAggregate(primary.filter((r: any) => r.model === model && getSpec(r.caseId).group === o.group), 13) })));
  const controls = models.flatMap(model => ['no-image', 'symbolic-reference'].map(arm => {
    const rows = run.rows.filter((r: any) => r.model === model && r.arm === arm);
    const pairs = rows.map((r: any) => {
      const before = primary.find((b: any) => b.model === model && b.caseId === r.caseId);
      return { caseId: r.caseId, before: before?.diagnosis.verdict.metrics.success ?? null,
        after: r.diagnosis.verdict.metrics.success,
        surfaceBefore: before?.diagnosis.verdict.metrics.surfaceF1 ?? null,
        surfaceAfter: r.diagnosis.verdict.metrics.surfaceF1 ?? null };
    });
    return { model, arm, ...validationAggregate(rows, 3), pairs };
  }));
  const pairedModels = models.flatMap((a, i) => models.slice(i + 1).map(b => {
    const objects = protocol.chosen.map((o: any) => {
      const matched = mainInputs.filter((r: any) => getSpec(r.caseId).group === o.group).flatMap((input: any) => {
        const ra = primary.find((r: any) => r.model === a && r.id === input.id);
        const rb = primary.find((r: any) => r.model === b && r.id === input.id);
        return ra && rb ? [rb.diagnosis.verdict.metrics.success - ra.diagnosis.verdict.metrics.success] : [];
      });
      return { group: o.group, matchedTasks: matched.length, delta: matched.length ? matched.reduce((n: number, v: number) => n + v, 0) / matched.length : null };
    });
    return { a, b, objects, inference: 'Three object clusters only; no confidence interval, p-value or stable-ranking claim.' };
  }));
  const copyRows = primary.flatMap((row: any) => {
    const task = taskForV2(getSpec(row.caseId)), baselineAnswer = copyInputAnswer(task.public);
    if (!baselineAnswer) return [];
    const baseline = evaluateStrict(task, baselineAnswer);
    const parsed = parseJSON(row.call.content) as any;
    const predicted = decode(task.spec.kind === 'repair' ? parsed?.structure : parsed);
    const current = decode(task.public.input.current)!;
    return [{ caseId: row.caseId, model: row.model, task: `${task.spec.kind}/${task.spec.variant}`,
      baseline, verdict: row.diagnosis.verdict,
      unchangedStructure: predicted ? digest(current.parts.map(p => key(p)).sort())
        === digest(predicted.parts.map(p => key(p)).sort()) : false,
      partF1Delta: row.diagnosis.verdict.metrics.partF1 - baseline.metrics.partF1! }];
  });
  const copySummary = taskKeys.flatMap(task => models.flatMap(model => {
    const rows = copyRows.filter((r: any) => r.task === task && r.model === model);
    return rows.length ? [{ task, model, n: rows.length,
      baselineSuccess: rows.reduce((n: number, r: any) => n + r.baseline.metrics.success, 0),
      baselinePartF1: rows.reduce((n: number, r: any) => n + r.baseline.metrics.partF1, 0) / rows.length,
      modelPartF1: rows.reduce((n: number, r: any) => n + r.verdict.metrics.partF1, 0) / rows.length,
      delta: rows.reduce((n: number, r: any) => n + r.partF1Delta, 0) / rows.length,
      unchangedStructure: rows.filter((r: any) => r.unchangedStructure).length }] : [];
  }));
  const result = { version: 'model-validation-analysis-1', replay, protocolHash: digest(protocol),
    rawRunHash: digest(readFileSync(resolve(VALIDATION_DIR, 'run.json'), 'utf8')),
    byModel, tasks, sizes, controls, pairedModels, ladder, normalizedLadder: normalized,
    copyInput: { rows: copyRows, summary: copySummary,
      scope: 'Public-input deterministic no-op baseline for completion/edit/repair only. No target used to construct the answer. Not a neural result.' },
    assessment: { floors: tasks.filter(t => t.classification === 'floor').map(t => t.task),
      ceilings: tasks.filter(t => t.classification === 'ceiling').map(t => t.task),
      mixed: tasks.filter(t => t.classification === 'mixed').map(t => t.task),
      discriminatingTasks: tasks.filter(t => t.modelOutcomesDiffer).map(t => t.task),
      reliableRankingEstablished: false, targetCapabilityFullyValidated: false,
      interpretation: 'Descriptive sensitivity screen, not a confirmatory ranking. Mixed successes alone do not imply between-model discrimination; paired per-case patterns are checked separately.' } };
  atomicJson(resolve(VALIDATION_DIR, 'analysis.json'), result);
  const label = (s: string) => s.replace('openai/', '').replace('google/', '').replace('qwen/', '');
  const frac = (r: { successes: number; returned: number }) => `${r.successes}/${r.returned}`;
  const percent = (m: { value: number | null } | undefined) => m?.value == null ? 'N/A' : (m.value * 100).toFixed(1) + '%';
  const partialKeys = ['fieldAccuracy', 'connectedAccuracy', 'aboveAccuracy', 'contactStudsAccuracy', 'shortestPathAccuracy',
    'partF1', 'bomF1', 'surfaceF1', 'additionF1', 'preservation', 'constraintAccuracy', 'legalPrefix',
    'localizationF1', 'restorationSuccess'];
  const md = `# OpenRouter 多模型验证报告

## 执行与结论边界

- 固定主验证状态：${replay.status}；已返回 ${replay.responses}/${replay.expected} 个响应；新增费用 $${replay.newCost.toFixed(6)}，该阶段结束累计 $${run.campaignAfter.toFixed(6)}。
- 4个模型共享3个验证对象（12/20/29件），每模型39个主任务、6个诊断任务。不是180个独立对象，也不是全量评测。
- 样本、模型、提示、JSON模式、2200输出token上限和每题1次提交在运行前冻结；模型顺序轮转，失败不重试、不修答、不按结果选样。
- 所有成绩按原响应重算并核对账单。无图和完整符号参考独立列出，不混入主榜。
- 尺寸和结构族混杂；此次不覆盖独立零件识别、OOD结构族、复杂连接或真实人类设计对象。
- 模型选择覆盖一个同家族大小对照、一个Google模型和一个开放权重VLM，不代表覆盖所有前沿模型。统一JSON输出模式也是Harness条件，不能称为完全无约束的原生能力。

## 综合判断

${result.assessment.discriminatingTasks.length ? `在${taskKeys.length}个任务变体中，有${result.assessment.discriminatingTasks.length}个在同题上表现出模型差异，说明这个小样本已有局部区分信号。` : '当前完整配对题尚未显示模型间的精确成功差异。'}
同时有${result.assessment.floors.length}个变体全零、${result.assessment.ceilings.length}个全满。
这是一轮有用的诊断结果，但不是充分成熟的benchmark证据：任务分层不等于可靠模型排名，三个独立对象也无法证明总体难度曲线。
${result.assessment.floors.includes('reconstruct/full') ? '普通重建在精确成功上仍为地板，应先校准更低难度和局部指标，再扩大相同难度的调用量。' : '普通重建的样本内结果见下表，仍需其他来源对象重复。'}
报告不把较大的型号预设为赢家，也不因为出现预期排序就宣称结果更好。

## 能力矩阵

| 任务/变体 | ${models.map(label).join(' | ')} | 样本内形态 |
| --- | ${models.map(() => '---:').join(' | ')} | --- |
${tasks.map(t => `| ${t.task} | ${t.byModel.map(frac).join(' | ')} | ${t.classification} |`).join('\n')}

分母是实际返回数；未返回数量见analysis.json，不能把服务失败解释为模型不会。
floor=全部模型精确成功为零；ceiling=全部成功；mixed=其他情况。该分类仅描述这3个对象，不是总体难度标签。

## 格式、成本与规模

| 模型 | 主任务成功* | 格式合法 | 截断 | 主任务费用 | 平均延迟ms |
| --- | ---: | ---: | ---: | ---: | ---: |
${byModel.map(r => `| ${label(r.model)} | ${frac(r)} | ${r.formatAccepted}/${r.returned} | ${r.truncated} | $${r.cost.toFixed(6)} | ${r.latencyMs?.toFixed(0) ?? 'N/A'} |`).join('\n')}

*混合任务成功总数仅作执行摘要，不能作为统一“智能分数”或可靠排名。

| 件数/结构族 | ${models.map(label).join(' | ')} |
| --- | ${models.map(() => '---:').join(' | ')} |
${protocol.chosen.map((o: any) => `| ${o.pieces}/${o.policy} | ${models.map(m => frac(sizes.find((r: any) => r.model === m && r.group === o.group)!)).join(' | ')} |`).join('\n')}

## 分层指标

以下指标以所有已返回响应为分母，畸形答案仍保留零分；N/A表示任务不适用。

| 任务 | 模型 | 指标及均值 |
| --- | --- | --- |
${tasks.flatMap(t => t.byModel.map(m => `| ${t.task} | ${label(m.model)} | ${partialKeys.filter(k => m.metrics[k]).map(k => `${k}=${percent(m.metrics[k])}`).join('; ')} |`)).join('\n')}

## 同对象诊断

| 模型 | 无图重建 | 符号参考重建 | 符号参考完整结构正确率 |
| --- | ---: | ---: | ---: |
${models.map(m => {
  const symbolic = controls.find(c => c.model === m && c.arm === 'symbolic-reference')!;
  return `| ${label(m)} | ${frac(controls.find(c => c.model === m && c.arm === 'no-image')!)} | ${frac(symbolic)} | ${percent(symbolic.metrics.fullStructureSuccess)} |`;
}).join('\n')}

为控制评分变化，主实验与两个对照沿用相同的普通重建成功判据（合法性+BOM+可见表面）；完整结构正确率另列。
符号参考提供额外真值信息，改善不等于纯视觉因果效应；无图仍保留BOM。需要结合表面/部件分数与格式失败，而非只看0/1。

## 高分是否只是复制输入

复制基线只返回公开current结构；修复题额外返回空faultIds，不读取目标来构造答案。
保留区域占比高时，partF1很高也可能没有修好任何错误。以下差值只作诊断，不替代原评分。

| 任务 | 模型 | 复制基线Part-F1 | 模型Part-F1 | 差值 | 输出结构未变 |
| --- | --- | ---: | ---: | ---: | ---: |
${copySummary.map((r: any) => `| ${r.task} | ${label(r.model)} | ${(r.baselinePartF1 * 100).toFixed(1)}% | ${(r.modelPartF1 * 100).toFixed(1)}% | ${(r.delta * 100).toFixed(1)} pp | ${r.unchangedStructure}/${r.n} |`).join('\n')}

正常无故障题上不修改是正确控制行为；在有故障题上必须结合定位和目标区域恢复判断。
补全应同时看新增部分F1，修复应同时看故障定位、恢复成功，不能仅凭整体Part-F1判断能力。

## 结果是否“漂亮”

- 模型逐题结果确实不同的任务：${result.assessment.discriminatingTasks.join('、') || '无'}。
- 样本内兼有成功/失败的任务：${result.assessment.mixed.join('、') || '无'}；这本身不等于模型之间有差异。
- 精确成功地板：${result.assessment.floors.join('、') || '无'}。
- 精确成功天花板：${result.assessment.ceilings.join('、') || '无'}。
- 好的结果应能解释差异来自哪里，并经新对象复现；不要求模型按预设顺序排列。当前只能判断局部可区分性，不能宣布benchmark已得到充分验证或达到CVPR录用水平。
- 若某任务全零，先看格式、几何和局部指标；若全满，将其保留为基础控制，不让它支配总分。模型间只有一两题差异时不作显著性解释。
- 已有完整算法审计中，高度排序解完全部10240道装拆题。因此本轮规划差异可说明固定输入下的约束遵循差异，不能证明需要复杂搜索。

## 已落实的改进

1. 从单一成功总数改为“任务变体×模型×件数”诊断，保留格式、几何、结构、执行与故障定位的分层指标。
2. 为无图/符号参考建立同对象配对记录；新增模型测试与既有730条API证据隔离，评分器不变。
3. 新增缺失、截断、成本、实际provider和token记录；账单未确定就停止，不把网络故障写成能力零分。
4. analysis.json保留每对模型的对象级差值，不把同对象13道题当独立统计样本。
5. 新增只用公开输入构造的复制基线，量化整体结构分数中“原本就正确”的部分，保留原始成功判据。

## 下一阶段

先在其余未用验证对象上扩展重复，分开控制件数、结构族、遮挡和连接复杂度。针对地板任务设计更小结构/局部位姿/连接问答的阶梯，针对天花板保留基础控制并增加真实子装配编辑。新题需先独立验证，不为拉开模型差距而定制答案。
冻结当前报告后才设计后续提示或工具消融；这些开发对象不得升级成“未见正式测试”。需另有授权语义数据、人工指标校准和更充分模型比较，才能支持广泛能力主张。

## 重建难度阶梯

${ladder ? `已追加 ${ladder.responses}/24 次独立记录的开发调用，新增费用 $${ladder.newCost.toFixed(6)}。
主验证与阶梯合计费用 $${(replay.newCost + ladder.newCost).toFixed(6)}。

| 件数/输入 | ${models.map(label).join(' | ')} |
| --- | ${models.map(() => '---:').join(' | ')} |
${[2, 4, 8].flatMap(count => ['ordinary', 'symbolic'].map(condition =>
  `| ${count}/${condition === 'ordinary' ? 'RGB+BOM' : '符号参考'} | ${models.map(model =>
    frac(ladder.rows.find((r: any) => r.count === count && r.condition === condition && r.model === model))).join(' | ')} |`)).join('\n')}

这六道题来自一个其他验证对象的嵌套前缀，不能当成六个独立对象。它检查更低复杂度区间是否有可测信号；前缀变化同时改变几何，不能归因于件数本身。后续需扩展多个独立来源，按遮挡和连接分层重复。`
    : '阶梯输入已准备，尚无完成的模型结果；不得用未执行的实验作结论。'}

### 原点问题与修订验证

逐答复查发现v1裁剪前缀未重新归一化：2件和4件结构的最小Z为1，但图像页脚仍沿用“原点为最小角”的说明。
Gemini的2件输出与真值只差整体平移；这是评价接口的干扰因素，不能将v1全零无条件解释为视觉能力缺失。
v1原答、费用和分数保持不变，originAudit只作事后诊断；不把平移对齐后的结果补记模型成功。

${normalized ? `v2将每个前缀重新平移到最小XYZ均为0，并明确写入题面，另行调用${normalized.responses}/24次，新增费用$${normalized.newCost.toFixed(6)}。
全部三轮合计新增$${(replay.newCost + (ladder?.newCost ?? 0) + normalized.newCost).toFixed(6)}，没有重置累计账本。

| 件数/归一化输入 | ${models.map(label).join(' | ')} |
| --- | ${models.map(() => '---:').join(' | ')} |
${[2, 4, 8].flatMap(count => ['ordinary', 'symbolic'].map(condition =>
  `| ${count}/${condition === 'ordinary' ? 'RGB+BOM' : '符号参考'} | ${models.map(model =>
    frac(normalized.rows.find((r: any) => r.count === count && r.condition === condition && r.model === model))).join(' | ')} |`)).join('\n')}

两版同时改变了坐标原点、对应图片和说明文字，并重新采样，不能把全部分数变化因果归于某一个改动。v2仍是同一来源的自适应开发验证，不是独立确认集。`
    : '归一化v2独立准备并验证真值；尚未取得完成的模型结果。'}

${normalized ? `归一化后RGB+BOM成功${normalized.rows.filter((r: any) => r.condition === 'ordinary').reduce((n: number, r: any) => n + r.successes, 0)}/12，
符号参考成功${normalized.rows.filter((r: any) => r.condition === 'symbolic').reduce((n: number, r: any) => n + r.successes, 0)}/12。
修正原点后出现有限成功信号，但当前数据仍不足以形成稳定的重建能力阶梯。“已修复题面原点问题”和“已建立有效能力分层”是两件不同的事。` : ''}

下一项优先检查是具有明确相机/坐标约定的局部位姿、候选判别与逐字段任务，区分视觉理解、坐标映射和长JSON生成。不要继续扩大未经这种校准的全结构重建调用。

## 复现

运行 \`node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts replay-model-validation\` 可离线复算，不需要API密钥。
原始响应、固定输入、价目快照、账单、分析和源码版本分别见同目录run.json、protocol.json、ledger.json、analysis.json。
`;
  writeFileSync(resolve(VALIDATION_DIR, 'REPORT.zh-CN.md'), md);
  return { ...result.assessment, ...replay };
}
