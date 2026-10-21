"""Replay every recorded model action, then publish figures and a Chinese report."""
from pathlib import Path
from collections import Counter, defaultdict
import csv, hashlib, inspect, json, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from protocol import Episode, load
from run import ROOT, MODELS, dump, images as render_images
import os
OUT=ROOT/os.environ.get('BRICKPLAN_EVAL_OUT','deliverables/brickplan-api-pilot')
MODELS=['openai/gpt-4.1-mini','google/gemini-2.5-flash']  # Frozen historical report only
from render import Renderer

LABELS={'control':'无错误对照','wrong_color':'错色','missing':'漏件','wrong_type':'错形状/功能','wrong_size':'同类错尺寸','offset':'水平错位','rotation':'朝向错误','height_layer':'高度错层','swapped_positions':'位置互换','compound':'四处耦合'}
SHORT=['GPT-4.1 mini','Gemini 2.5 Flash']

def collect():
    rows=[];viewer=[];calls=[];replayed=0;images=set();review_cache={};renderers={}
    for file in sorted((OUT/'runs').glob('*.json')):
        r=json.loads(file.read_text());s=r['spec'];cert,cases=load(s['modelId'])
        ep=Episode(cert,cases[s['caseId']],s['mode'],s.get('event','none'),action_mask=s.get('actionMask',False))
        steps=[]
        for step in r['steps']:
            assert ep.assignments()==step['before'],(file,'before')
            obs=step['observation'];assert obs==ep.observe(r['track']),(file,'observation')
            if r['track']=='visual':assert 'current' not in obs and 'target' not in obs
            encoded=json.dumps(obs)
            assert all(secret not in encoded for secret in ('oraclePlan','expectedOptimum',':goal',':wrong',':color'))
            for path in step['images']:
                assert hashlib.sha256((OUT/path).read_bytes()).hexdigest()==Path(path).stem
                images.add(path)
            review_images=[]
            if not step['images']:
                key=(s['mode'],s['modelId']);statekey=key+(tuple(ep.state),)
                if statekey not in review_cache:
                    if key not in renderers:renderers[key]=Renderer(ep.cert)
                    review_cache[statekey]=render_images(ep,renderers[key],directory=OUT)
                review_images=review_cache[statekey]
            for ex in step.get('executions',[]):
                assert ep.step(ex['action'])==ex['feedback'],(file,'feedback')
                assert ep.assignments()==ex['after'],(file,'after')
                replayed+=1
            response=step.get('response')
            if response:calls.append({**response,'runId':r['id']})
            steps.append({'images':step['images'],'reviewerImages':review_images,'current':obs.get('current'),'target':obs.get('target'),
                          'response':response['content'] if response else r.get('error','Pending'),
                          'executions':step.get('executions',[]),'notice':obs['eventNotice']})
        assert ep.events==r.get('events',[])
        if 'metrics' in r:
            for k,v in r['metrics'].items():assert ep.score()[k]==v,(file,k)
        codes=Counter(ex['feedback']['code'] for st in r['steps'] for ex in st.get('executions',[]))
        score=ep.score()
        # A final review frame makes single-call successful repairs visible too.
        key=(s['mode'],s['modelId']);statekey=key+(tuple(ep.state),)
        if statekey not in review_cache:
            if key not in renderers:renderers[key]=Renderer(ep.cert)
            review_cache[statekey]=render_images(ep,renderers[key],directory=OUT)
        steps.append({'terminal':True,'images':[],'reviewerImages':review_cache[statekey],
                      'response':'API 中断时的审核状态' if r['status']=='error' else '按最后一个已执行动作恢复的回合终态',
                      'current':None,'target':None,'executions':[],'notice':bool(ep.events)})
        color_repaired=None
        if ep.events and s.get('event')=='color':
            event=ep.events[0];changed=[a for a in ep.actors if event['before'][a]!=event['after'][a]]
            color_repaired=all(ep.assignments()[a]==ep.case['goal'][a] for a in changed)
        row={'id':r['id'],'mode':s['mode'],'assistance':'legal_action_mask' if s.get('actionMask') else 'none',
             'model':r['model'],'track':r['track'],'modelId':s['modelId'],'kind':s.get('kind','dynamic'),
             'event':s.get('event','none'),'status':r['status'],**score,'colorRepairAtEnd':color_repaired,
             'calls':sum('response' in st for st in r['steps']),
             'costUSD':sum(st['response']['cost'] for st in r['steps'] if 'response' in st),
             'latencySeconds':sum(st['response']['latencyMs']/1000 for st in r['steps'] if 'response' in st),
             'codes':dict(codes)}
        rows.append(row);viewer.append({**row,'caseId':s['caseId'],'steps':steps,'events':r.get('events',[])})
    groups=[]
    for mode,assistance in [('static','none'),('dynamic','none'),('dynamic','legal_action_mask')]:
        for model in MODELS:
            for track in ['symbolic','visual']:
                allrows=[r for r in rows if (r['mode'],r['assistance'],r['model'],r['track'])==(mode,assistance,model,track)]
                rr=[r for r in allrows if r['status']=='complete'];tr=[r for r in rr if r['eventTriggered']]
                faults=[r for r in rr if r['kind']!='control']
                groups.append(dict(mode=mode,assistance=assistance,model=model,track=track,n=len(rr),success=sum(r['success'] for r in rr),
                    apiErrors=sum(r['status']=='error' for r in allrows),faultN=len(faults),faultSuccess=sum(r['success'] for r in faults),
                    triggered=len(tr),triggeredTotal=sum(r['eventTriggered'] for r in allrows),triggeredApiErrors=sum(r['eventTriggered'] and r['status']=='error' for r in allrows),recovered=sum(r['success'] for r in tr),meanTargetRecall=np.mean([r['targetPartRecall'] for r in rr]).item() if rr else None,
                    actions=sum(r['manipulations'] for r in rr),invalid=sum(r['invalidActions'] for r in rr)))
    recon=OUT/'accounting/reconciliations.json'
    upper=sum(e['interruptedCostUpperBoundUSD'] for e in json.loads(recon.read_text())['events']) if recon.exists() else 0
    auth=json.loads((OUT/'budget-authorization.json').read_text());ledger=json.loads((ROOT/'benchmark/.runtime/campaign-ledger.json').read_text())
    unresolved=sum(c['reserved'] for c in ledger['charges'] if c['actual'] is None)
    upper+=unresolved
    spent=sum(c['actual'] if c['actual'] is not None else c['reserved'] for c in ledger['charges'])-auth['baselineSpentUSD']
    summary={'date':'2026-10-14','rows':rows,'groups':groups,'knownResponseCalls':len(calls),'knownResponseCostUSD':sum(c['cost'] for c in calls),
             'interruptedRequestCostUpperBoundUSD':upper,'allPilotCostUpperBoundUSD':sum(c['cost'] for c in calls)+upper,
             'chargedSinceAuthorizationUpperBoundUSD':spent,'additionalCapUSD':2,'unsettledCharges':sum(c['status']!='settled' for c in ledger['charges']),
             'audit':{'replayedActions':replayed,'verifiedImages':len(images),'publicObservationsMatched':True,'privateLabelsAbsent':True},
             'coverage':{'plannedRuns':64,'attemptedRuns':len(rows),'completedRuns':sum(r['status']=='complete' for r in rows),'apiErrors':sum(r['status']=='error' for r in rows),'running':sum(r['status']=='running' for r in rows)},
             'sourceHashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*') if p.suffix in ('.py','.c','.ts','.html')}}
    dump(OUT/'summary.json',summary)
    with (OUT/'results.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=[k for k in rows[0] if k!='codes']);w.writeheader();w.writerows({k:v for k,v in r.items() if k!='codes'} for r in rows)
    return summary,viewer

def interval(k,n):
    if not n:return 0,0
    z=1.96;p=k/n;den=1+z*z/n;center=(p+z*z/(2*n))/den;half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return center-half,center+half

def plots(summary):
    dest=OUT/'plots';dest.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#f7f9fc','axes.facecolor':'white','savefig.facecolor':'#f7f9fc'})
    def save(fig,name):
        for ext in ('png','svg','pdf'):fig.savefig(dest/f'{name}.{ext}',dpi=180,bbox_inches='tight')
        plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(15,4.2),layout='constrained')
    for ax,(mode,assist,title) in zip(axes,[('static','none','Static repair / hard pilot'),('dynamic','none','Dynamic / from empty'),('dynamic','legal_action_mask','Dynamic / legal-action diagnostic')]):
        gg=[g for g in summary['groups'] if (g['mode'],g['assistance'])==(mode,assist)]
        for i,g in enumerate(gg):
            n=g['n'];k=g['success'];p=k/n if n else 0;lo,hi=interval(k,n)
            ax.bar(i,p,color='#2864d8' if g['track']=='symbolic' else '#ee8657',width=.62)
            if n:ax.errorbar(i,p,yerr=[[max(0,p-lo)],[max(0,hi-p)]],color='#32445c',capsize=4,fmt='none')
            ax.text(i,min(.94,hi+.035),f'{k}/{n}' if n else 'API error' if g['apiErrors'] else 'not run',ha='center',fontsize=10)
        ax.set(ylim=(0,1.15),yticks=[0,.25,.5,.75,1],yticklabels=['0%','25%','50%','75%','100%'],xticks=range(4),xticklabels=['GPT\nText','GPT\nVision','Gemini\nText','Gemini\nVision'],title=title)
        ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
    fig.suptitle('Exact completion: correct target AND explicit finish',fontsize=16)
    fig.supxlabel('Bars: observed fractions. Whiskers: descriptive Wilson 95% intervals; selected cases, not bank population estimates.',fontsize=9)
    save(fig,'completion')
    rows=summary['rows'];kinds=list(LABELS);matrix=np.full((len(kinds),4),np.nan)
    for r in rows:
        if r['mode']=='static' and r['status']=='complete':matrix[kinds.index(r['kind']),MODELS.index(r['model'])*2+['symbolic','visual'].index(r['track'])]=int(r['success'])
    fig,ax=plt.subplots(figsize=(8,5.6),layout='constrained');ax.imshow(matrix,cmap=matplotlib.colors.ListedColormap(['#f7d8cb','#badcc9']),vmin=0,vmax=1,aspect='auto')
    for (y,x),v in np.ndenumerate(matrix):ax.text(x,y,'PASS' if v==1 else 'FAIL' if v==0 else 'N/A',ha='center',va='center',color='#243648')
    ax.set(xticks=range(4),xticklabels=['GPT / Text','GPT / Vision','Gemini / Text','Gemini / Vision'],yticks=range(len(kinds)),yticklabels=[k.replace('_',' ') for k in kinds],title='Static pilot: one frozen case per row, per condition')
    save(fig,'static_cases')
    fig,axes=plt.subplots(1,2,figsize=(12,4.4),layout='constrained')
    counter=Counter()
    for r in rows:counter.update({k:v for k,v in r['codes'].items() if k not in ('OK','SUCCESS','ENVIRONMENT_CHANGED','OBSERVATION_READY')})
    names=[k for k,_ in counter.most_common()];axes[0].barh(names[::-1],[counter[k] for k in names[::-1]],color='#ee8657');axes[0].set(title='Rejected actions / wrong finishes',xlabel='Recorded occurrences')
    labels=[];trigger=[];recover=[]
    for assist in ['none','legal_action_mask']:
        rr=[r for r in rows if r['mode']=='dynamic' and r['assistance']==assist and r['event']!='none']
        labels.append(('Baseline' if assist=='none' else 'Legal-action diagnostic')+f' (n={len(rr)})');trigger.append(sum(r['eventTriggered'] for r in rr));recover.append(sum(r['success'] and r['eventTriggered'] for r in rr))
    x=np.arange(2);axes[1].bar(x-.17,trigger,.34,label='Event actually triggered',color='#2864d8');axes[1].bar(x+.17,recover,.34,label='Recovered after event',color='#218068');axes[1].set(xticks=x,xticklabels=labels,title='Dynamic intervention accounting',ylabel='Episodes');axes[1].legend(fontsize=9)
    for i,v in enumerate(trigger):axes[1].text(i-.17,v+.05,str(v),ha='center')
    save(fig,'failures_and_events')
    bank=json.loads((ROOT/'deliverables/brickplan-repair-library/index.json').read_text())
    fig,axes=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    kk=list(bank['kinds']);vv=[bank['kinds'][k] for k in kk]
    axes[0].barh([k.replace('_',' ') for k in kk],vv,color=['#ee8657' if k=='compound' else '#2864d8' for k in kk])
    axes[0].set(title='Static bank: primary case type',xlabel='Cases (compound counted once)')
    for i,v in enumerate(vv):axes[0].text(v+8,i,str(v),va='center',fontsize=9)
    axes[0].set_xlim(0,max(vv)*1.15)
    bins=[f'D{i}' for i in range(6)];values=[bank['difficulty'].get(k,0) for k in bins]
    axes[1].bar(bins,values,color=['#adc0d6','#93b1df','#7198d1','#527fc1','#386aad','#214f8b'])
    for i,v in enumerate(values):axes[1].text(i,v+15,str(v),ha='center',fontsize=9)
    axes[1].set(title='Certified repair cost, original per-case domain',ylabel='Cases',ylim=(0,max(values)*1.15))
    fig.supxlabel('2,541 cases / 127 structure entries. Difficulty measures planning operations, not visual recognition.',fontsize=10)
    save(fig,'bank_profile')

def report(summary):
    bank=json.loads((ROOT/'deliverables/brickplan-repair-library/index.json').read_text())
    lines=[]
    for g in summary['groups']:
        mode='静态' if g['mode']=='static' else '动态＋合法动作辅助' if g['assistance']!='none' else '动态'
        model=SHORT[MODELS.index(g['model'])];track='文本完整状态' if g['track']=='symbolic' else '多视图＋逐件查看'
        recovery=f"{g['recovered']}/{g['triggered']}" if g['triggered'] else 'N/A（无完整触发回合）'
        if g['triggeredApiErrors']:recovery+=f"；另有{g['triggeredApiErrors']}例触发后API中断"
        if g['mode']=='static':recovery='—'
        lines.append(f"| {mode} | {model} | {track} | {g['success']}/{g['n']} | {g['apiErrors']} | {recovery} |")
    txt=f'''# BrickPlan 静态修复与动态搭建：API 小样本报告

日期：2026-10-14。服务：OpenRouter；模型：GPT-4.1 mini、Gemini 2.5 Flash。真实调用、非模拟模型回答。

## 结论与设计核对

当前静态任务符合“给定一个状态，修复到目标”的核心定义：初态固定，修复期间没有外部干预；允许转动、观察、拆装。动态从零搭建独立记录，未混入静态类别。当前交付是可验证的几何规划 Bench 和小样本试跑，**尚不足以宣称完整研究评测已完成**。

- 当前静态库 {bank['caseCount']} 例、{bank['modelCount']} 个结构条目、{bank['kinds']['compound']} 例复合错误；每结构单独错色保持 2–3 例。
- 本轮新增 8 例四处错误耦合，修复需要 13–29 步；结构约束比自由编辑下界多 6–22 步。全部初态合法且有精确修复计划。
- 127 个条目由 123 个原有模型子结构及 4 个 16 件扩展子结构组成；并非 127 个完整套装。122 个来源精确，5 个保留重构标记。
- 当前类型包括漏件、错色、错形状/功能、同类错尺寸、水平错位、朝向、错层、多余件、位置互换与复合。多余垫片常与错层共存，不把同一状态重复包装成新错误。
- 难度来自深层嵌入、共享拆修通道、支撑依赖、需要暂拆正确件和多根错误相互耦合。动态的取走、过早封闭、旧计划失效不作为静态主类。

![题库类型与难度](plots/bank_profile.png)

## 模型能看见什么、能转动吗

**能。** 文本赛道得到完整当前/目标状态、零件目录及认证约束。视觉赛道得到实际当前/目标的七视图（等轴、前后左右、上下）和**所有注册零件**的逐件对照；模型可用 `inspect` 请求任意方位角／俯仰角或检查单件。观察不改变结构，拆装成本为零，但占一次模型交互轮。

仅转动外部相机仍可能看不到封闭内部。本版统一逐件查看解决这一点：所有件一视同仁，不只显示错误件。2541 例的每个错误根均通过实际初态/目标逐件 RGB 差异检测（7 视角、256×192、通道差≥24、至少24像素）。这证明约定观察方式下存在可见差异，**不证明外部视角或每张默认图都能辨认，也不代表模型已经识别正确**。

视觉输入不带当前/目标符号状态、错误标签、差异清单、审核高亮或最优计划。目录在同一结构各案例中固定，含全部干扰件和候选位置，ID 匿名化。单件图使用同一坐标框架，保留位姿差异。该赛道测合成图像与结构修复，不是自然照片感知或纯图像无几何目录测试。

## 实验设置

静态选 10 例：无错误对照 1 例，9 个错误类别各 1 例，按预先冻结规则选择偏难样本（其中 6 例 D5）。不能把该小样本平均数当作 2541 例全库准确率。每模型各跑文本与视觉、每条件一次、温度0、最多8轮、每轮最多8动作；在第一个拒绝、观察请求、环境扰动或结束时丢弃余下动作。每请求最多2200输出tokens，Gemini reasoning关闭、JSON输出、90秒超时；低价服务路由且不自动fallback。结果只适用于这一推理设置。

动态基线选一个经从空场景验证的 11 件结构 `v23-3223`，包括无扰动与中途取走、换色、位姿改变、提前封闭4种条件。初始没有真实积木；虚拟台面仅提供锚点。装上至少5件后尝试干预，仅提交合法状态变化；达不到触发条件就记“未触发”。无物理仿真或机器人控制。

另设合法动作辅助诊断：同一结构中途换色，公开当前**全部合法动作**，每轮执行1动作、最多20轮。合法动作计算不用目标和答案，但会提供额外状态可行性信息，因此与原始赛道分开统计。这组用于检查模型是否能越过搭建瓶颈并真正遇到扰动，不能当作无辅助能力。

动态基线若未达到触发门槛，不同干预条件的实际输入可能完全相同，不能将这些回合解释为已经测过四类修复能力。完整流程成功与“局部换色已修复”分开记录：`colorRepairAtEnd` 只检查干预改动的两个实体，不能替代整体任务成功。

## 实测结果

主要指标为最终状态完全正确且模型显式 `finish`。只到达正确状态但未结束不算成功；无错误对照单独保留。API 中断不计作模型能力失败，表中另列。扰动恢复只对真正触发的例子计分。

| 任务 | 模型 | 输入 | 完成数/有效例数 | API 中断 | 触发后恢复 |
|---|---|---|---:|---:|---:|
{chr(10).join(lines)}

静态仅统计真正需要修复的9例（去掉无错误对照）：GPT-4.1 mini 文本 {next(g['faultSuccess'] for g in summary['groups'] if g['mode']=='static' and g['model']==MODELS[0] and g['track']=='symbolic')}/9，Gemini 2.5 Flash 文本 {next(g['faultSuccess'] for g in summary['groups'] if g['mode']=='static' and g['model']==MODELS[1] and g['track']=='symbolic')}/9；视觉均0/9。模型主动 `inspect` 次数、目标件完成比例、无效动作等逐运行指标在 CSV 中，成功率不使用被大量未用干扰件抬高的全状态平均准确率。

![完整任务成功率](plots/completion.png)

图中的 Wilson 区间仅描述选中小样本的二项比例；样本非随机、共享结构且每例一次，不能用于声称模型总体排名或统计显著差异。

![逐类型结果](plots/static_cases.png)

![无效动作与扰动触发](plots/failures_and_events.png)

失败分析应结合逐步轨迹：文本输入已给定状态却持续触发 `DISCONNECTED` / `PATH_BLOCKED`，提示规划和反馈利用存在问题；视觉对照在完全正确状态中误拆，提示视觉状态理解或零件 ID 对齐存在问题。无法仅凭最终成功率把所有视觉失败归因于遮挡。交互报告可逐轮查看实际输入图、原始回复和执行反馈；文本赛道额外生成的结构图明确标记为审核回放，未传给文本模型。无效动作图包含 API 中断前已发生的动作，动态触发图也保留中断回合的已发生干预；恢复率只对完整回合计分。

动态辅助诊断中，{sum(r['colorRepairAtEnd'] is True and r['status']=='complete' for r in summary['rows'] if r['assistance']=='legal_action_mask')} 个完整回合已在结束时修复中途换色，但仍未完成全部搭建。可在逐轮回放中区分“局部修复成功”和“全流程未完成”。所有模型主动观察请求共 {sum(r['inspectCalls'] for r in summary['rows'])} 次；主动接口可用不等于模型实际使用了它。

## 费用、证据与复现

- 已拿到返回的真实请求：{summary['knownResponseCalls']} 次，`usage.cost` 合计 **${summary['knownResponseCostUSD']:.6f}**。
- 中断请求账单上界：${summary['interruptedRequestCostUpperBoundUSD']:.7f}，使用服务商当日总用量减去已知请求；可能包含无关活动，因此不冒充逐请求精确账单。原请求未重试。
- 包括预检和中断上界，本试跑总费用最多 **${summary['allPilotCostUpperBoundUSD']:.6f}**；新增2美元授权后账本增量最多 **${summary['chargedSinceAuthorizationUpperBoundUSD']:.6f}**。未重置历史账本。
- 全静态库独立重算 2541 例，回放 18366 个答案动作，58 组独立 BFS 交叉检查通过。
- 本报告逐条复放 {summary['audit']['replayedActions']} 个真实模型动作，核对每步输入、状态变化、反馈与扰动；{summary['audit']['verifiedImages']} 张输入图通过内容 SHA256 核对。源码哈希在 `summary.json`。
- 动态环境的 oracle 从空场景搭建与4类扰动恢复已验证；oracle 成功不计入模型得分。

文件：`runs/` 保存完整模型输入、原始输出、用量、动作及私有审核真值；`images/` 保存实际传图及审核回放图；`selection.json` 为冻结选题；`results.csv` 为逐运行指标；`summary.json` 为汇总及源码指纹；`plots/` 提供 PNG/SVG/PDF。独立绘图脚本 `plot.py` 只读取旁边的 `summary.json` 和 `bank-profile.json`，不调用 API；完整回放核验脚本是 `benchmark/brickplan-repair/eval/report.py`。

复现（仓库根目录，密钥仅放本地 `.env`）：

```bash
benchmark/.runtime/mlx-env/bin/python -B benchmark/brickplan-repair/validate_static.py
benchmark/.runtime/mlx-env/bin/python -B benchmark/brickplan-repair/eval/validate.py
benchmark/.runtime/mlx-env/bin/python -B benchmark/brickplan-repair/eval/report.py
# 下列命令调用付费 API；现有运行不重复调用，遵守本轮账本额度
benchmark/.runtime/mlx-env/bin/python -B benchmark/brickplan-repair/eval/run.py
benchmark/.runtime/mlx-env/bin/python -B benchmark/brickplan-repair/eval/run.py --assisted --calls 20
```

## 还未满足的研究要求

这轮回答了接口是否能跑、给定观测下模型在哪里失败；尚未完成全库、多种子、更强模型和人工基线评测。视觉 admission 是像素可辨性门槛，不是人类识别实验。已有候选目录限制了开放式搭建空间，理想连接和直线拆装不代表物理世界可行性。

新 API 目录覆盖结构内全部候选，比原题库单例动作空间更大；原有最优步数仅作题库难度参考，不能直接用于 API 最优率或 regret。下一步应冻结新的统一动作域并重新求解参考成本。

类型扩展可优先增加非对称子组件整体反装、重复模块装错槽位、相同外观而连接关系不同等；需要先得到真实几何与不同目标证据，不能只增标签。本轮已实现的是有验证证据的四错误耦合，其他建议未算入数量。

API 参考：[OpenRouter 图像输入](https://openrouter.ai/docs/guides/overview/multimodal/image-understanding)、[用量记账](https://openrouter.ai/docs/guides/guides/usage-accounting)。
'''
    (OUT/'REPORT.zh-CN.md').write_text('> **旧协议结果（已停用）**：text 提供完整状态，不能作为视觉识别成绩；旧 views 使用低分辨率拼图、覆盖编号和几何文字辅助，不能代表新版视觉输入效果。仅保留原始证据，不再用于当前 VLM 结论。修正见 [视觉协议 v3](../brickplan-visual-input-v3/README.zh-CN.md)。\n\n'+txt)

def html(summary,viewer):
    template=(Path(__file__).parent/'report-template.html').read_text()
    compact={'summary':{k:v for k,v in summary.items() if k not in ('rows','sourceHashes')},'runs':viewer}
    (OUT/'report.html').write_text(template.replace('__DATA__',json.dumps(compact,ensure_ascii=False).replace('</','<\\/')))

if __name__=='__main__':
    summary,viewer=collect();plots(summary);report(summary);html(summary,viewer)
    bank=json.loads((ROOT/'deliverables/brickplan-repair-library/index.json').read_text())
    dump(OUT/'bank-profile.json',{k:bank[k] for k in ('caseCount','modelCount','kinds','difficulty')})
    source="from pathlib import Path\nfrom collections import Counter\nimport json,math\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nOUT=Path(__file__).resolve().parent\nMODELS="+repr(MODELS)+"\nLABELS="+repr(LABELS)+"\n\n"+inspect.getsource(interval)+"\n\n"+inspect.getsource(plots)+"\nplots(json.loads((OUT/'summary.json').read_text()))\n"
    source=source.replace("ROOT/'deliverables/brickplan-repair-library/index.json'","OUT/'bank-profile.json'")
    (OUT/'plot.py').write_text(source)
    print(json.dumps({k:v for k,v in summary.items() if k not in ('rows','sourceHashes','groups')},ensure_ascii=False))
