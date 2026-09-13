import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { STUDY, } from './protocol';
import { BENCHMARK } from '../storage';
import { EXTERNAL_SOURCE_CANDIDATES, sourceGate } from './source-policy';
import { humanAuditStatus } from './human-audit';
import { exposureAudit } from './exposure';

interface Gate { id: string; passed: boolean; evidence: string[]; reason: string }
export function summarizeReadiness(gates: Gate[]) {
  if (!gates.length || new Set(gates.map(g => g.id)).size !== gates.length) throw new Error('Unique, nonempty gates required');
  return { passed: gates.filter(g => g.passed).map(g => g.id), pending: gates.filter(g => !g.passed).map(g => g.id),
    allPassed: gates.every(g => g.passed) };
}
export function researchReadiness() {
  const read = (path: string) => existsSync(resolve(STUDY, path)) ? JSON.parse(readFileSync(resolve(STUDY, path), 'utf8')) : null;
  const audit = humanAuditStatus(), exposure = exposureAudit();
  const clean = read('clean-verification.json'), order = read('order-study/analysis.json');
  const external = EXTERNAL_SOURCE_CANDIDATES.map(asset => ({ asset, gate: sourceGate(asset) }));
  const gates: Gate[] = [
    { id: 'research-contract', passed: existsSync(resolve(BENCHMARK, 'suite/study/RESEARCH_CONTRACT.md')),
      evidence: ['../../study/RESEARCH_CONTRACT.md'], reason: 'Closest-work core, falsifiable questions and information/statistical boundaries are documented; not an exhaustive novelty certification.' },
    { id: 'source-exposure-accounting', passed: exposure.observedGroups > 0,
      evidence: ['exposure-register.json'], reason: 'Training, validation, published pilot and merely prepared sources are distinguished.' },
    { id: 'external-semantic-data', passed: external.some(e => e.gate.readyForRelease),
      evidence: [], reason: 'No actual licensed human-designed/semantic structure layer has been integrated and audited.' },
    { id: 'measurement-repeat-control', passed: order?.status === 'complete' && order?.responses === 192,
      evidence: order ? ['order-study/analysis.json'] : [], reason: 'Same-order resampling and permutation must be paired on all 12 selected sources; completion is not proof of an effect.' },
    { id: 'independent-confirmation', passed: false, evidence: [],
      reason: 'All current model experiments remain adaptive development. A separately sourced frozen confirmation and justified precision are absent.' },
    { id: 'independent-human-review', passed: audit.completeConsensus && audit.independenceVerifiedExternally,
      evidence: ['human-audit/status.json'], reason: `${audit.submissions} real submitted labels; ${audit.consensusItems}/${audit.queued} consensus items. Template generation is not human review.` },
    { id: 'runtime-free-replay', passed: clean?.passed === true,
      evidence: clean ? ['clean-verification.json'] : [], reason: 'Same-machine copied environment without runtime/key; does not certify a second-person install.' },
    { id: 'external-reproduction', passed: false, evidence: [],
      reason: 'No independently executed second-environment reproduction receipt is available.' },
    { id: 'submission-manuscript', passed: false, evidence: ['../../../paper/main.tex'],
      reason: 'Development manuscript and supplement can be built; scientific gates and target-year submission checks remain outstanding.' },
  ];
  const summary = summarizeReadiness(gates);
  const result = { version: 'six-work-package-readiness-1', ...summary, gates, externalSources: external,
    humanReview: { queued: audit.queued, submitted: audit.submissions, consensus: audit.consensusItems },
    caveat: 'Internal evidence readiness, not a conference acceptance probability. Unavailable external evidence is intentionally not inferred from software tests.' };
  atomicJson(resolve(STUDY, 'research-readiness.json'), result);
  const documents = ['RESEARCH_CONTRACT.md', 'EXTERNAL_VALIDATION.md', 'source-policy.ts', 'exposure.ts', 'human-audit.ts', 'readiness.ts'];
  atomicJson(resolve(STUDY, 'research-governance-sources.json'), Object.fromEntries(documents.map(p =>
    [p, digest(readFileSync(resolve(BENCHMARK, 'suite/study', p), 'utf8'))])));
  const report = `# 六项总体计划：证据汇总\n\n本报告持续累积同一个总体目标，不把阶段性交付等同于研究完成。当前完整就绪：${summary.allPassed ? '是' : '否'}。\n\n` +
    '| 总工作包 | 已具备 | 尚未完成 |\n| --- | --- | --- |\n' +
    '| 1. 研究定位 | 最近邻核心比较、H1-H5及反证条件、信息/统计合同 | 最终全文相关工作核对与独立研究判断 |\n' +
    '| 2. 数据与划分 | 暴露登记、分组隔离、许可发布检查 | 实际有授权的外部语义层、新冻结确认测试 |\n' +
    `| 3. 测量有效性 | 多解/原点/复制基线/字段诊断，重复对照${order?.status ?? '未完成'} | 人类指标校准及外部域有效性 |\n` +
    `| 4. 模型与统计 | 既有四模型验证、10组训练、重复/换序${order?.responses ?? 0}/192调用 | 充分来源与有效专用基线、独立确认性结论 |\n` +
    `| 5. 独立审核复现 | 96候选审核包、版本/重复/分歧检查、同机离线复算 | ${audit.submissions}条真实审核；第二人复现仍待完成 |\n` +
    '| 6. 论文与交付 | 论文、表格、原始日志、证据与总验收报告 | 主张收敛、科学门槛和实际届次提交核验 |\n\n' +
    '## 核心结果与解释\n\n' +
    '数据为5,120个程序结构、117,910个任务条件，不能将题数视为独立样本数。10组本地训练/基线共3,370条预测；没有编辑迁移正证据。四模型180次验证只有3个来源对象，不能据此确定稳定排名。\n\n' +
    (order ? '| 模型 | 同序重复不一致 | 换序不一致 | 超额不一致均值 [95%来源bootstrap区间] |\n| --- | ---: | ---: | --- |\n' +
      order.byModel.map((m: any) => `| ${m.model} | ${m.repeatMismatch}/${m.pairedGroups} | ${m.permutationMismatch}/${m.pairedGroups} | ${
        m.excessMismatchInterval ? `${m.excessMismatchInterval.mean.toFixed(3)} [${m.excessMismatchInterval.low.toFixed(3)}, ${m.excessMismatchInterval.high.toFixed(3)}]` : '缺失'} |`).join('\n') +
      `\n\n本次${order.responses}次调用、${order.sourceGroups}个来源，新费用$${order.newCost.toFixed(9)}；原累计账本$${order.campaignAfter.toFixed(9)}。` +
      '比较实际位姿而非选项标签。结果支持当前开发样本内的候选顺序敏感性，不证明总体规律、认知原因或稳定模型排名；各模型共享来源，不能合并扩大独立样本数。\n\n' : '') +
    '## 技术交付\n\n' +
    `无runtime/无密钥同机复算：${clean?.passed ? '通过' : '未通过'}，${clean?.commands?.length ?? 0}个命令；不等于外部独立安装。` +
    '主文与补充材料见../../../../paper/，页数和编译检查以各自verification.json为准。技术发布清单与本研究就绪门槛分离。\n\n' +
    '## 门槛明细\n\n' + gates.map(g => `- ${g.passed ? '通过' : '待完成'}：${g.id}。${g.reason}`).join('\n') +
    '\n\n## 必须由外部提供的证据\n\n真实审核者的独立标签与仲裁、数据权利方许可及实际结构文件、第二环境执行记录。若确认研究超出原累计$4.50预算，需要新的明确费用授权，不能重置账本。\n' +
    '\n具体交接与冻结要求见../../../study/EXTERNAL_VALIDATION.md。剩余研究不只需要外部参与：外部数据适配、有效专用基线及确认性实验仍需实现和验证，不能把全部缺口转交给人工。\n' +
    '\n这些门槛没有通过时，不报告“已达到录取标准”。代码生成的许可字段、审核模板、统计表和PDF不是独立研究证据。\n';
  mkdirSync(resolve(STUDY, 'governance'), { recursive: true });
  writeFileSync(resolve(STUDY, 'governance/SUMMARY.zh-CN.md'), report);
  return result;
}
