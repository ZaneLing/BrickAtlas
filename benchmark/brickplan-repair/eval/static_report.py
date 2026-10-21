"""Local Markdown only: exact replay, error taxonomy, matched-case matrices and cost."""
from pathlib import Path
from collections import Counter,defaultdict
from copy import deepcopy
import json,hashlib,csv,math
from protocol import Episode,load
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'deliverables/brickplan-static-audit-2026-10-14'
LABELS={'control':'无错误对照','wrong_color':'错色','missing':'漏件','wrong_type':'错形状/功能','wrong_size':'同类错尺寸','offset':'水平错位','rotation':'朝向错误','height_layer':'高度错层','swapped_positions':'位置互换','compound':'四处耦合','extra':'独立多余件'}
MODELS=['openai/gpt-6.1-sol','google/gemini-4-argon','anthropic/claude-sonnet-5.5']
SHORT={'openai/gpt-6.1-sol':'GPT‑6.1 Sol','google/gemini-4-argon':'Gemini 4 Argon','anthropic/claude-sonnet-5.5':'Claude Sonnet 5.5'}
selection=json.loads((OUT/'selection.json').read_text());bank=json.loads((OUT/'bank-audit.json').read_text());specs=selection['specs']
opt={r['caseId']:r.get('expandedOptimum') for r in bank['expandedDomainOptima']}
rows=[];imagepaths=set();replayed=0
for f in sorted((OUT/'runs').glob('*.json')):
 r=json.loads(f.read_text());spec=r['spec'];cert,cs=load(spec['modelId']);ep=Episode(cert,cs[spec['caseId']],seed=spec['seed'],protocol_version=spec['protocolVersion']);codes=Counter();formats=0;blocked_repeats=0;previous_rejections=set();first_wrong=[];providers=set();last_feedback=[]
 for step in r['steps']:
  assert step['observation']==ep.observe(r['track']),(f,'observation')
  assert step['before']==ep.assignments(),(f,'state')
  if r['track']=='visual':assert 'current' not in step['observation'] and 'target' not in step['observation']
  assert not any(k in json.dumps(step['observation']) for k in ('oraclePlan','expectedOptimum',':goal',':wrong'))
  for path in step['images']:
   imagepaths.add(path);assert hashlib.sha256((OUT/path).read_bytes()).hexdigest()==Path(path).stem
  if 'response' in step:
   providers.add(step['response']['provider'])
   try:
    obj=json.loads(step['response']['content']);acts=obj.get('actions');assert isinstance(acts,list) and 1<=len(acts)<=8
   except (ValueError,AttributeError,AssertionError):formats+=1
  for e in step.get('executions',[]):
   before=ep.assignments();feedback=ep.step(e['action']);assert feedback==e['feedback'] and ep.assignments()==e['after'];replayed+=1
   code=feedback['code'];codes[code]+=1
   if code not in ('OK','SUCCESS','OBSERVATION_READY'):
    sig=json.dumps([before,e['action'],code],sort_keys=True)
    blocked_repeats+=sig in previous_rejections;previous_rejections.add(sig)
    if len(first_wrong)<4:first_wrong.append({'call':step['callIndex']+1,'action':e['action'],'feedback':feedback})
 assert ep.events==r.get('events',[])
 if 'metrics' in r:assert ep.score()==r['metrics']
 score=ep.score();validmoves=sum(codes[k] for k in ('OK',))
 row={'id':r['id'],'caseId':spec['caseId'],'structure':spec['modelId'],'model':r['model'],'track':r['track'],'kind':spec['kind'],'stratum':spec['stratum'],'status':r['status'],'stopReason':r.get('stopReason',r.get('error')),'restrictedCost':spec['restrictedCost'],'expandedOptimum':opt.get(spec['caseId']),**score,'responses':sum('response'in x for x in r['steps']),'costUSD':sum(x['response']['cost'] for x in r['steps'] if 'response'in x),'formatFailures':formats,'repeatedRejections':blocked_repeats,'codes':dict(codes),'firstProblems':first_wrong,'providers':sorted(providers),'validManipulations':validmoves}
 rows.append(row)
ledger=json.loads((ROOT/'benchmark/.runtime/campaign-ledger.json').read_text());charges=[c for c in ledger['charges'] if c.get('authorization')=='static-audit-2026-10-14'];cost=sum(c['actual'] if c['actual']is not None else c['reserved'] for c in charges);known=sum(r['costUSD'] for r in rows);unsettled=[c for c in charges if c['status']!='settled']
complete=[r for r in rows if r['status']=='complete'];pending=[r for r in rows if r['status']=='running'];errors=[r for r in rows if r['status']=='error'];budget=[r for r in rows if r['status']=='budget_exhausted'];assert cost<=5+1e-9
summary={'selection':selection,'rows':rows,'knownResponseCostUSD':known,'costUpperBoundUSD':cost,'reservedOrUncertainUpperBoundUSD':cost-known,'calls':sum(r['responses'] for r in rows),'completed':len(complete),'attempted':len(rows),'apiErrors':len(errors),'budgetStopped':len(budget),'running':len(pending),'planned':len(specs)*6,'unsettledCharges':len(unsettled),'replayedActions':replayed,'verifiedImages':len(imagepaths),'models':MODELS}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
fields=[k for k in rows[0] if k not in ('codes','firstProblems','providers')]
with (OUT/'results.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:r[k] for k in fields} for r in rows)

def frac(rr):return f"{sum(r['success'] for r in rr)}/{len(rr)}" if rr else '未完成测试'
def cell(r):
 if not r:return '未运行'
 if r['status']=='error':return 'API错误'
 if r['status']=='budget_exhausted':return '预算停止'
 if r['status']!='complete':return r['status']
 return ('✓' if r['success'] else '✗')+f" {r['responses']}轮 / {r['manipulations']}动作"+(f" / {r['formatFailures']}格式错" if r['formatFailures'] else '')
lookup={(r['caseId'],r['model'],r['track']):r for r in rows}
matched=[s for s in specs if all(lookup.get((s['caseId'],m,t),{}).get('status')=='complete' for m in MODELS for t in ['symbolic','visual'])]
overview=[]
for m in MODELS:
 for t in ['symbolic','visual']:
  rr=[r for r in complete if r['model']==m and r['track']==t];fault=[r for r in rr if r['kind']!='control'];common=[r for r in rr if any(s['caseId']==r['caseId'] for s in matched)]
  interrupted=[r for r in rows if r['model']==m and r['track']==t and r['status'] in ('error','budget_exhausted')]
  overview.append(f"| {SHORT[m]} | {'文本状态' if t=='symbolic' else '多视图+逐件图'} | {frac(rr)} | {frac(fault)} | {frac(common)} | {sum(r['invalidActions'] for r in rr)} | {sum(r['formatFailures'] for r in rr)} | {sum(r['status']=='error' for r in interrupted)} / {sum(r['status']=='budget_exhausted' for r in interrupted)} |")
matrix=[]
for kind in LABELS:
 line=[LABELS[kind]]
 for m in MODELS:
  for t in ['symbolic','visual']:line.append(frac([r for r in complete if (r['kind'],r['model'],r['track'])==(kind,m,t)]))
 matrix.append('| '+' | '.join(line)+' |')
hardtable=[]
seen_structures=set()
for s in specs:
 if s['stratum']!='four_fault' or s['modelId'] in seen_structures:continue
 seen_structures.add(s['modelId'])
 hardtable.append('| '+s['modelId']+' | '+str(s['restrictedCost'])+' | '+' | '.join(cell(lookup.get((s['caseId'],m,'symbolic'))) for m in MODELS)+' |')
details=[]
for i,s in enumerate(specs):
 details.append(f"## {i+1}. {LABELS[s['kind']]} · {s['modelId']}\n\nCase：`{s['caseId']}`。原域最优 {s['restrictedCost']} 步；实际 API 扩展域最优：{opt.get(s['caseId']) if opt.get(s['caseId']) is not None else '30,000 节点内未证明，不能沿用原最优断言'}。seed={s['seed']}。\n\n| API 模型 | 文本 | 多视图 |\n|---|---|---|")
 for m in MODELS:details.append(f"| {SHORT[m]} | {cell(lookup.get((s['caseId'],m,'symbolic')))} | {cell(lookup.get((s['caseId'],m,'visual')))} |")
 for m in MODELS:
  for t in ['symbolic','visual']:
   r=lookup.get((s['caseId'],m,t))
   if not r:continue
   details.append(f"\n- [{SHORT[m]} / {t} 原始记录](runs/{r['id']}.json)：终态剩余 {r['remainingMismatches']} 处，目标件恢复率 {r['targetPartRecall']:.1%}，停止原因 `{r['stopReason']}`，服务商 {', '.join(r['providers'])}。")
   for e in r['firstProblems']:details.append(f"  - 第 {e['call']} 轮：`{json.dumps(e['action'],ensure_ascii=False)}` → `{json.dumps(e['feedback'],ensure_ascii=False)}`。")
(OUT/'03-CASE-DETAILS.zh-CN.md').write_text('> **旧协议结果（已停用）**：text 提供完整状态，不能作为视觉识别成绩；旧 views 使用低分辨率拼图、覆盖编号和几何文字辅助，不能代表新版视觉输入效果。仅保留原始证据，不再用于当前 VLM 结论。修正见 [视觉协议 v3](../brickplan-visual-input-v3/README.zh-CN.md)。\n\n'+'# 静态实验逐案例明细\n\n完成条件为精确目标状态且显式 finish。预算停止、API 中断与模型未完成分别记录。所有数字由真实动作重放产生。\n\n'+'\n'.join(details)+'\n')
formatfile=OUT/'format-diagnostic.json';formats=json.loads(formatfile.read_text()) if formatfile.exists() else []
text=f'''# 静态 Bench：真实 API 测试结果

日期：2026-10-14。仅静态状态修复，本轮未运行动态搭建或物理仿真。产物只在本地，不生成实验网页。

## 先看结论

- 三个 API 模型：GPT‑6.1 Sol、Gemini 4 Argon、Claude Sonnet 5.5，固定完整 ID 见下方协议。
- 已正常结束 **{len(complete)}** 个回合，其中精确完成 **{sum(r['success'] for r in complete)}**；API错误 **{len(errors)}**，预算停止 **{len(budget)}**，仍在运行 **{len(pending)}**。正常结束包括“模型完成”和“6轮耗尽”，后者算任务失败。
- 计划预选 26 案例 × 3 API 模型 × 2 输入条件 = 156 回合；这是待测清单，未运行格子不算测试成功或失败。完整六条件共同完成的配对案例 **{len(matched)}** 个。
- 真实 API 返回 **{summary['calls']}** 次，已知返回费用 **${known:.8f}**，含中断请求整笔预留的保守费用上界 **${cost:.8f} / $5**；未结算条目 {len(unsettled)}。这是本次新增额度，未挪用此前 $2 的余额。
- 核验了 **{replayed}** 个实际动作、**{len(imagepaths)}** 张输入图的 SHA-256；所有记录中的观察、动作反馈、状态和成功指标逐项重放一致。

**判断：选定的八类单错文本题，GPT 与 Gemini 均为 8/8；四处耦合题也能完成，当前完整状态/约束辅助条件对它们的区分度有限。Claude 的低分明显受到格式问题影响，同时存在真实的路径/支撑规划失败，不能把全部失败归到同一原因。** 本轮实际触达 {len(set(r['caseId'] for r in rows))} 个源案例、{len(set(r['structure'] for r in rows))} 个结构，不是全库测试。

## 各模型 / 输入成绩

主指标：目标状态精确一致，且模型显式提交 finish。目标件恢复率作为局部进展，不能替代成功率。分母仅含正常返回并走完该回合的任务；服务错误和预算截断另列。

| API 模型 | 输入 | 成功/正常结束 | 排除对照后 | 六条件共同案例 | 无效动作 | 格式错误回复 | API中断/预算停止 |
|---|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(overview)}

**分母不同的行不可直接排名。** 共同案例列使用同一组 {len(matched)} 个源案例；它仍是小规模、刻意选难的单次实验，不代表 2541 例全库总体准确率，也不能作显著性结论。

## 按错误类别分解

表中为“完成数 / 已正常结束回合数”，不是错误识别准确率；协议没有单独要求模型输出错误类别标签。

| 类别 | GPT 文本 | GPT 视觉 | Gemini 文本 | Gemini 视觉 | Claude 文本 | Claude 视觉 |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(matrix)}

`独立多余件` 无独立入库案例；多余垫片出现在高度错层和部分复合题中，因此不能据此宣称该独立类型已测。

## 很难的复合题能不能做对

下面是每个复合来源结构的代表题，使用同一案例的文本条件。动作数包含被拒绝的尝试；对成功解另检查有效拆装数。

| 结构 | 原域参考动作数 | GPT | Gemini | Claude |
|---|---:|---|---|---|
{chr(10).join(hardtable)}

- 10001--deep 的 29 步题：三者文本均达到目标；GPT、Gemini 各29次有效拆装，Claude 31次尝试中29次有效、2次拒绝。该题扩展域最优29已证。视觉下 GPT、Gemini 也完成，Claude 6轮后还差3处。
- v23-30571--deep 的13步题：GPT、Gemini 均13次完成；Claude 先有路径错误，后连续格式失败，仅执行8次有效拆装。
- v23-3223--deep 的28步参考题：GPT、Gemini 最终均执行30次有效拆装，确实比已知可行参考计划多2次；Claude 有3次路径错误、2次支撑错误，6轮后未完成。扩展域最优未证明，不能称“距真实最优正好2步”。
- v23-6678--deep 的27步参考题：GPT、Gemini 各27次有效拆装完成；Claude 在预算截断时尚未完成，不能计为模型失败。

当前最难复合题存在多步约束，但至少在完整状态与约束公开的条件下，GPT、Gemini 已能稳定完成这几道选定题。更有价值的下一步是扩大耦合机制与来源结构，而不只是继续增加同模板题数。

![所有预选案例的实际运行矩阵](static-result-matrix.png)

图中灰色为未运行，API为服务中断，$为预算截断，J为全程格式失败且未执行拆装，T为目标已到达但未显式finish。图片序号对应逐案例明细。

## 怎么理解失败

- `PATH_BLOCKED`：动作没有先清除路径上的零件；`DISCONNECTED_ASSEMBLY`：拆件后其他件失去与固定基座相连的支撑路径。这两类属于当前离散结构规则上的错误。
- `INVALID_ACTION` 可能来自整个回复不是合法 JSON，不能一概解读为几何或规划能力差。原始回复、服务商及第一批被拒动作在 [逐案例明细](03-CASE-DETAILS.zh-CN.md)。
- 离线格式诊断检查到 {len(formats)} 条不合规回复，{sum(r['candidateJSONObjects']==1 for r in formats)} 条含唯一可提取的 actions 对象；其中 {sum(r.get('successIfOnlyFormattingRelaxed',False) for r in formats)} 条从该轮实际状态出发，只放宽格式即可立即完成。此诊断没有额外 API 调用，没有替换主成绩，也没有把多轮反事实串起来。
- `call_budget` 表示 6 轮内未完成，不证明无限轮次也无法修复。每次 inspect 占一次 API 回合但不计拆装动作；主动观察与操控共享回合额度，应在后续版本拆分预算。
- `GOAL_NOT_MET` 如出现，才属于显式错误结束；没有该反馈的失败不会标成“提前 finish”。

### 已确认的失败实例

| 现象 | 证据 | 能得出的结论 |
|---|---|---|
| 反复拆断支撑 | Gemini视觉朝向题：6次 `DISCONNECTED_ASSEMBLY`，其中2次是在完全相同状态重复相同被拒动作；最终剩7处不匹配。 | 存在具体的支撑约束/反馈利用失误。不能笼统归因于遮挡。 |
| 复杂结构拆装规划失败 | Claude文本 v23-3223--deep 复合题：3次路径阻挡、2次支撑断开，没有JSON格式错；最终未完成。 | 这是清晰的规划失败样本，不能用格式问题解释。 |
| 正确计划被接口丢弃 | Claude文本高度错层题：回复附带说明文字与多余围栏，6轮均拒绝；每轮提取唯一JSON后都能从实际状态立即完成。 | 严格接口分数与修复规划能力存在差异。 |
| 已修好却没有结束提交 | Claude位置互换题的文本、视觉条件都达到精确目标，但在6轮内没有有效finish。 | 应分别报告“状态恢复成功”和“协议完成成功”。 |

全部正常结束回合中，状态已完全匹配的为 {sum(r['targetMatched'] for r in complete)}/{len(complete)}，显式协议完成为 {sum(r['success'] for r in complete)}/{len(complete)}。本轮没有错误finish导致的 `GOAL_NOT_MET`。9条格式放宽后立即成功的回复来自重复轮次，不是9个独立成功案例；涉及 {len({r['runId'] for r in formats if r.get('successIfOnlyFormattingRelaxed')})} 个回合。

## 协议与此前结果的区别

精确模型 ID：`openai/gpt-6.1-sol`、`google/gemini-4-argon`、`anthropic/claude-sonnet-5.5`。通过 OpenRouter 价格上限路由；实际 provider 随响应存档，因此成绩归属于“模型 + 服务商 + 请求配置”的组合。价格目录冻结在 [model-pricing.json](model-pricing.json)。

所有模型最多6轮、每轮最多8动作；4096输出token上限（含服务商计算的推理token），请求 `reasoning.effort=low`，请求 JSON object；同一源案例使用相同匿名ID seed和图像。响应推理token以 usage为准，不能从请求参数推断服务商实际执行了同等推理计算量。

实际返回的服务商：GPT为Azure（54次），Gemini为Google（62次），Claude为Google（109次）；这里的Google是API响应的provider字段，不是改用了Gemini模型。记录的推理token合计分别为1,784、0、22,747；225次返回的finishReason均为stop，未见输出token上限截断。这不证明无隐藏推理，只说明返回usage如此记录。

每轮为一次独立请求，提供完整当轮观察及最近8条动作反馈；没有传入模型此前的推理文本或完整聊天历史。系统提示保留兼容动态任务的说明，但本轮 mode 全部为 static、没有任何过程扰动。协议不会把动作失败后的余下动作继续执行。

本轮使用 `all-registered-candidates-v2`：候选列表顺序随机化，attach必须显式给出candidate。原来367个有多个候选的目标零件，正确候选全部排首位；另有省略candidate默认填正确位置的执行器漏洞。本轮已修复。旧两轮共386次attach未实际省略candidate，不能声称这个漏洞已解释旧成绩；固定顺序仍是未控制的捷径风险。因此旧轮成绩不与本轮直接合并。

视觉输入包含七视图、对所有件开放的逐件当前/目标对照图；还提供匿名零件目录、候选变换和完整支撑/碰撞/路径约束。它是**有结构信息辅助的视觉修复**，不等同于只给RGB图片的纯视觉机器人测试。没有向模型传错误类型、错误ID列表、最优解或只包含本例正确/错误位置的目录。

## 采样与花费限制

预先选择每个可用单一错误类别的最难例 + 另一结构例，全部8个四处耦合例，2个对照；共17个结构。4处耦合例来自4个深层结构。运行中仅按已观察费用调整任务执行先后：先覆盖类别，再补不同结构的复合与重复例；案例集合未改、失败未删。调度暂停发生在发请求和预留费用之前，原始检查点保存在 scheduler-checkpoints/。详见 [selection.json](selection.json)、[schedule.json](schedule.json)。

发生三次服务中断后，剩余额度优先覆盖八类单错的文本条件，以及各个复合来源结构的文本条件；随后才补余下视觉格子。因此视觉和文本覆盖不完全配对，应使用共同案例列比较。

每个请求先按字节数、图像数、输出上限预留保守费用；无法容纳下一笔预留时停止，所以实际消耗可能略低于$5。HTTP中断不会静默重试；整笔预留先保守记账。本API密钥存在其他并行使用，账户总用量差额无法直接当成本实验账单。

## 本地交付

- [Bench 完整度、正确性、难度和真实世界 gap 评估](02-BENCH-ASSESSMENT.zh-CN.md)
- [逐案例、逐模型的错误证据](03-CASE-DETAILS.zh-CN.md)
- [汇总原始数据](summary.json)、[逐回合 CSV](results.csv)、[格式诊断](format-diagnostic.json)
- [本轮独立账本](charges.json)、[中断请求费用处理](uncertain-charges.json)、[证据文件哈希](evidence-manifest.json)
- `runs/` 保存完整公开观察、模型原始回复、执行反馈；`images/` 保存模型实际看到的图。

外部配置依据：[OpenAI GPT‑6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol)、[OpenRouter Gemini 4 Argon](https://openrouter.ai/google/gemini-4-argon)、[OpenRouter Claude Sonnet 5.5](https://openrouter.ai/anthropic/claude-sonnet-5.5)。以上网页只用于模型配置；实验结论来源于本地真实调用记录。
'''
(OUT/'01-RESULTS.zh-CN.md').write_text('> **旧协议结果（已停用）**：text 提供完整状态，不能作为视觉识别成绩；旧 views 使用低分辨率拼图、覆盖编号和几何文字辅助，不能代表新版视觉输入效果。仅保留原始证据，不再用于当前 VLM 结论。修正见 [视觉协议 v3](../brickplan-visual-input-v3/README.zh-CN.md)。\n\n'+text)
print(json.dumps({k:v for k,v in summary.items() if k not in ('rows','selection')},ensure_ascii=False))
