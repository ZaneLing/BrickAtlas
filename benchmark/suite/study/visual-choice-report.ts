import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { poseQuestions, scorePose } from './pose-probes';
import { orderQuestions, orderScore } from './order-study';
import { VISUAL_CHOICE_DIR, replayVisualChoice } from './visual-choice-run';

export async function reportVisualChoice() {
  const verification = await replayVisualChoice();
  // Ground truth is loaded only after immutable predictions have been produced and independently replayed.
  const pose = new Map(poseQuestions().map(q => [q.id, q]));
  const order = new Map(orderQuestions().map(q => [q.id, q]));
  const run = JSON.parse(readFileSync(resolve(VISUAL_CHOICE_DIR, 'run.json'), 'utf8'));
  const rows = run.rows.map((r: any) => {
    const raw = JSON.stringify(r.prediction.answer);
    const score = r.cohort === 'pose-probes' ? scorePose(pose.get(r.id)!, raw) : orderScore(order.get(r.id)!, raw);
    return { cohort: r.cohort, id: r.id, group: r.group, arm: r.arm,
      answered: r.prediction.answer !== null, success: score.success, reason: r.prediction.reason,
      selectedKey: r.prediction.selectedKey, margin: r.prediction.margin,
      bestDistance: r.prediction.ranking[0]?.distance ?? null, hypotheses: r.prediction.hypotheses };
  });
  const aggregate = (selected: typeof rows) => ({ cases: selected.length,
    sourceGroups: new Set(selected.map((r: any) => r.group)).size,
    answered: selected.filter((r: any) => r.answered).length,
    successes: selected.filter((r: any) => r.success === 1).length,
    abstentions: selected.filter((r: any) => !r.answered).length });
  const arms = [...new Set<string>(rows.map((r: any) => `${r.cohort}:${r.arm}`))].map(name => ({
    name, ...aggregate(rows.filter((r: any) => `${r.cohort}:${r.arm}` === name)),
  }));
  const pairs = rows.filter((r: any) => ['original', 'choice-rgb'].includes(r.arm)).map((r: any) => {
    const p = rows.find((p: any) => p.cohort === r.cohort && p.group === r.group
      && ['permuted', 'choice-permuted'].includes(p.arm));
    assert.ok(p);
    const repeat = rows.find((p: any) => p.cohort === r.cohort && p.group === r.group && p.arm === 'repeat');
    const replacement = run.replacements.find((p: any) => p.cohort === r.cohort && p.id === r.id);
    assert.ok(replacement);
    return { cohort: r.cohort, group: r.group,
      permutationSamePose: r.selectedKey && p.selectedKey ? r.selectedKey === p.selectedKey : null,
      repeatedSamePose: repeat && r.selectedKey && repeat.selectedKey ? r.selectedKey === repeat.selectedKey : null,
      replacementAnswered: replacement.prediction.answer !== null,
      replacementChangesPose: r.selectedKey && replacement.prediction.selectedKey
        ? r.selectedKey !== replacement.prediction.selectedKey : null,
      replacementBestDistance: replacement.prediction.ranking[0]?.distance ?? null };
  });
  const replacementControl = { attempted: pairs.length,
    pairedAnswered: pairs.filter((p: any) => p.replacementChangesPose !== null).length,
    changed: pairs.filter((p: any) => p.replacementChangesPose === true).length,
    replacementAbstentions: pairs.filter((p: any) => !p.replacementAnswered).length };
  const result = { version: 'visual-choice-report-1', ...verification, arms, pairs, rows, replacementControl,
    elapsedMs: run.elapsedMs, runHash: digest(readFileSync(resolve(VISUAL_CHOICE_DIR, 'run.json'), 'utf8')),
    scope: 'Renderer-aware, public-BOM/candidate, blue-on-gray two-piece analysis-by-synthesis baseline; not a learned model or independent observation validator.',
    caveats: ['4 pose sources and 12 order sources are reused development objects, not 60 independent objects.',
      'All image conditions use three orthographic views. The original LLMs also received isometric views.',
      'Same renderer and canonical colors strongly favor this specialized baseline; no general semantic reconstruction claim.',
      'No-image abstention is deliberate, not a stochastic chance baseline.',
      'Replacement controls are mismatched observations and BOM; report image dependence, never task accuracy or causality.',
      'Missing target masks or tied candidates abstain. No rejection threshold for nonmatching but nonblank out-of-domain images is calibrated.',
      'Candidate rendering uses known simulator access and additional compute. Do not pool with one-shot model scores.'] };
  atomicJson(resolve(VISUAL_CHOICE_DIR, 'analysis.json'), result);
  const same = pairs.filter((p: any) => p.permutationSamePose === true).length;
  writeFileSync(resolve(VISUAL_CHOICE_DIR, 'REPORT.zh-CN.md'), '# 公开输入视觉匹配专用基线\n\n' +
    '方法：从公开BOM、候选、目录和最小角原点约定枚举合法两件结构，复用已知渲染器生成三个正交视图；' +
    '只比较蓝色查询件的像素掩膜IoU，按候选最优合法解释选择。标题、页脚、灰色底座与中性网格文字不参与匹配。' +
    '无图、无蓝色掩膜或候选并列时拒答，不按标签打破平局。底座位置和朝向经过枚举，不读取真值。\n\n' +
    '| 开发集/条件 | 成功/题数 | 已答 | 拒答 | 来源对象 |\n| --- | ---: | ---: | ---: | ---: |\n' +
    arms.map(a => `| ${a.name} | ${a.successes}/${a.cases} | ${a.answered} | ${a.abstentions} | ${a.sourceGroups} |`).join('\n') +
    `\n\n换序后选择相同位姿：${same}/${pairs.length}；换图共${replacementControl.attempted}次，其中${replacementControl.replacementAbstentions}次拒答，` +
    `其余${replacementControl.pairedAnswered}个有效配对中${replacementControl.changed}次选择改变。拒答不计为“不变”。\n` +
    `\n实际生成${run.renders}个候选视图，执行耗时${(run.elapsedMs / 1000).toFixed(1)}秒；0次API请求。重放会重算像素匹配，但使用已存候选图，不重新启动浏览器。\n\n` +
    '## 解释边界\n\n' + result.caveats.map(c => `- ${c}`).join('\n') +
    '\n\n本结果可检验此小型、已知渲染器域是否包含可利用的候选位置图像信号，不是独立人审、真实图像或任意CAD有效性证据。' +
    '算法在既有开发结果之后设计，不作为事前冻结的独立确认研究。原模型结果保持不变。\n');
  return result;
}
