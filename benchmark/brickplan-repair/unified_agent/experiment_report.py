"""Read-only reports and plots for the expanded experiment; never calls a model."""
import base64,gzip,hashlib,html,json,statistics,time
from collections import Counter,defaultdict
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
from PIL import Image
from dynamic_arena import OUT as ARENA
from dynamic_arena.transport import write_json
from unified_agent.experiment_batch import OUT,MODELS,merged,ledger_path,PROTOCOL
from unified_agent.ark_report import rows as old_rows,summary as model_summary,table,fmt,SHORT,ARMS


def collect():
    report=merged();data=old_rows(report);by_id={r['arenaRunId']:r for r in report['runs']}
    for row in data:
        raw=by_id[row['runId']]
        row.update(group=raw['sampleGroup'],family=raw['errorFamily'],sampleIndex=raw['sampleIndex'],inputVersion=raw['inputVersion'],
            goalSatisfied=raw['stateMetrics']['finalEquivalent'] and raw['stateMetrics']['finalConstraintsSatisfied'],
            url='http://127.0.0.1:8832/experiments?run='+row['runId'])
        log=json.loads((ARENA/'runs'/row['runId']/'log.json').read_text())
        row['normalizations']=sum(bool(c.get('outputValidation',{}).get('normalizations')) for c in log['calls'])
        row['proseJSONAccepted']=sum(any('JSON' in n for n in c.get('outputValidation',{}).get('normalizations',[])) for c in log['calls'])
        row['detailQueries']=sum('candidate' in c.get('modelOutput',{}).get('args',{}) and c.get('modelOutput',{}).get('tool')=='inspect' for c in log['calls'])
        row['pointQueries']=sum('point' in c.get('modelOutput',{}).get('args',{}) and c.get('modelOutput',{}).get('tool')=='inspect' for c in log['calls'])
    charges=[]
    for model in MODELS:
        p=ledger_path(model)
        if p.exists():charges+=json.loads(p.read_text())['charges']
    # Keep every attempt in data. Aggregates use the latest archived attempt
    # for each registered condition, never a success-selected attempt.
    latest={}
    for row in data:
        if row['inputVersion']==PROTOCOL:latest[row['model'],row['caseId'],row['arm']]=row
    primary=[r for r in latest.values() if r['group']=='new-sample']
    stats=model_summary(primary,charges)
    for stat in stats:
        rs=[r for r in primary if r['model']==stat['model']]
        for name,kinds in [('static',{'S0','S1'}),('normal',{'D0'}),('incident',{'D1','D2'})]:
            valid=[r for r in rs if r['taskType'] in kinds and r['eligible'] and (name!='incident' or r['recoveryEligible'])]
            stat[name+'Structure']=dict(n=len(valid),satisfied=sum(r['goalSatisfied'] for r in valid))
        stat['structureCorrectWithoutFinish']=sum(r['goalSatisfied'] and r['success'] is False for r in rs if r['eligible'])
        attempts=sum(r['manipulations'] for r in rs);moves=sum(r['moves'] for r in rs)
        stat['actionSummary']=dict(accepted=moves,attempts=attempts,rate=moves/attempts if attempts else None)
        stat['completionByLength']={}
        for length in ['short','medium','long']:
            stat['completionByLength'][length]={}
            for arm in ['static','normal','incident']:
                selected=[r for r in rs if r['lengthGroup']==length and r['arm']==arm and r['eligible'] and (arm!='incident' or r['recoveryEligible'])]
                stat['completionByLength'][length][arm]=dict(n=len(selected),success=sum(r['success'] is True for r in selected),
                    f1=statistics.mean(r['f1'] for r in selected) if selected else None)
        stat['newSampleCompleted']=dict(static=sum(r['arm']=='static' for r in rs),normal=sum(r['arm']=='normal' for r in rs),incident=sum(r['arm']=='incident' for r in rs))
        stat['technicalCodes']=dict(Counter(r['apiError'] or r['terminal'] for r in rs if not r['eligible']))
        stat['toolSummary']={k:sum(r[k] for r in rs) for k in ['freshCurrentObservations','candidateQueries','detailQueries','pointQueries','manualQueries','formatErrors','schemaErrors','proseJSONAccepted']}
    return report,data,primary,stats,charges


def make_plots(primary,stats,plan):
    folder=OUT/'plots';folder.mkdir(exist_ok=True)
    for name in ['actual-trajectories','model-vs-reference-1','model-vs-reference-2']:
        for ext in ['png','svg','pdf']:(folder/(name+'.'+ext)).unlink(missing_ok=True)
    font=Path('/System/Library/Fonts/Supplemental/Comic Sans MS.ttf')
    if font.exists():font_manager.fontManager.addfont(str(font));plt.rcParams['font.family']='Comic Sans MS'
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42,'savefig.dpi':240})
    colors=['#416eab','#178b83','#df9b43','#8764a7'];labels=['Sol','Seed Pro','DS Flash','Qwen']
    def save(fig,name):
        for ext in ['png','svg','pdf']:
            p=folder/(name+'.'+ext);fig.savefig(p,bbox_inches='tight',facecolor='white')
            if ext=='svg':p.write_text('\n'.join(l.rstrip() for l in p.read_text().splitlines())+'\n')
        plt.close(fig)
    fig,axs=plt.subplots(1,4,figsize=(14,3.4),sharey=True)
    for ax,key,title in zip(axs,['control','repair','normal','incident'],['Correct static','Faulty static','Normal build','Qualified recovery']):
        for i,s in enumerate(stats):
            g=s[key];n=g['denominator'];v=g['success']/n if n else 0
            ax.bar(i,v,color=colors[i] if n else '#dbe0e2');ax.text(i,v+.025,f"{g['success']}/{n}" if n else 'N/A',ha='center',fontsize=9)
        ax.set_xticks(range(4),labels,rotation=20);ax.set_ylim(0,1.17);ax.set_title(title);ax.grid(axis='y',alpha=.15)
    axs[0].set_ylabel('Explicit completion / eligible runs');save(fig,'success-rates')
    fig,axs=plt.subplots(1,3,figsize=(12,3.4),sharey=True)
    for ax,name,title in zip(axs,['static','normal','incident'],['Static final structure','Normal final structure','Recovery final structure']):
        for i,s in enumerate(stats):
            g=s[name+'Structure'];v=g['satisfied']/g['n'] if g['n'] else 0
            ax.bar(i,v,color=colors[i]);ax.text(i,v+.025,f"{g['satisfied']}/{g['n']}" if g['n'] else 'N/A',ha='center')
        ax.set_title(title);ax.set_xticks(range(4),labels,rotation=20);ax.set_ylim(0,1.17)
    axs[0].set_ylabel('Target satisfied at stop (finish not required)');save(fig,'structure-satisfaction')
    for arm in ['static','normal','incident']:
        matrix=np.full((50,4),np.nan);annotations={}
        for y,pair in enumerate(plan['selected']):
            cid=pair['static' if arm=='static' else 'dynamic']['id']
            for x,model in enumerate(MODELS):
                r=next((r for r in primary if r['model']==model and r['caseId']==cid and r['arm']==arm),None)
                if r:
                    if r['eligible'] and (arm!='incident' or r['recoveryEligible']):matrix[y,x]=r['f1'];annotations[y,x]='OK' if r['success'] else f"{r['f1']:.2f}"
                    else:annotations[y,x]='INT'
                else:annotations[y,x]='—'
        fig,ax=plt.subplots(figsize=(6.5,13));cmap=plt.colormaps['YlGnBu'].copy();cmap.set_bad('#e9edef')
        im=ax.imshow(matrix,cmap=cmap,vmin=0,vmax=1,aspect='auto');ax.set_xticks(range(4),labels)
        ax.set_yticks(range(50),[f"{p['index']:02} / {p['static' if arm=='static' else 'dynamic']['family']}" for p in plan['selected']],fontsize=7)
        for (y,x),value in annotations.items():ax.text(x,y,value,ha='center',va='center',fontsize=7,color='white' if matrix[y,x]>.65 else '#253843')
        ax.set_title(arm.title()+' / final placement F1');fig.colorbar(im,ax=ax,shrink=.5,label='F1')
        fig.text(.05,.01,'INT: technical interruption; dash: not run / not qualified / pending.',fontsize=8);save(fig,'matrix-'+arm)
    families=sorted({r['family'] for r in primary if r['taskType']=='S1'})
    fig,ax=plt.subplots(figsize=(13,4))
    for i,model in enumerate(MODELS):
        values=[]
        for family in families:
            rs=[r for r in primary if r['model']==model and r['taskType']=='S1' and r['family']==family and r['eligible']]
            values.append(sum(r['f1'] for r in rs)/len(rs) if rs else np.nan)
        ax.bar(np.arange(len(families))+(i-1.5)*.2,values,.2,label=labels[i],color=colors[i])
    ax.set_xticks(range(len(families)),families,rotation=30,ha='right');ax.set_ylim(0,1.05);ax.set_ylabel('Mean final placement F1');ax.set_title('Static faults by error family (no values for missing groups)');ax.legend();save(fig,'error-families')
    fig,axs=plt.subplots(1,2,figsize=(11,3.6));x=np.arange(4)
    axs[0].bar(x,[s['inputTokens']/1e6 for s in stats],label='Input',color='#276b85')
    axs[0].bar(x,[s['outputTokens']/1e6 for s in stats],bottom=[s['inputTokens']/1e6 for s in stats],label='Output including reasoning',color='#dda04b')
    axs[0].set_ylabel('Million tokens');axs[0].legend(fontsize=8);axs[0].set_title('All requests, including checks and supplements')
    axs[1].bar(x,[s['cny'] for s in stats],color=colors)
    for i,s in enumerate(stats):axs[1].text(i,s['cny'],f"{s['cny']:.2f}",ha='center',va='bottom')
    axs[1].set_ylabel('CNY estimate');axs[1].set_title('Usage estimate; Sol Ark price provisional')
    for ax in axs:ax.set_xticks(x,labels)
    save(fig,'tokens-and-cost')
    fig,ax=plt.subplots(figsize=(10,3.6));bottom=np.zeros(4)
    for key,label in [('freshCurrentObservations','Current observation'),('candidateQueries','Candidate queries incl. detail'),('manualQueries','Manual pages'),('pointQueries','Visible-part identification')]:
        values=np.array([sum(r[key] for r in primary if r['model']==m) for m in MODELS]);ax.bar(x,values,bottom=bottom,label=label);bottom+=values
    ax.set_xticks(x,labels);ax.set_ylabel('Tool calls');ax.set_title('Observation choices by the model');ax.legend(fontsize=8);save(fig,'observation-actions')
    fig,axs=plt.subplots(1,2,figsize=(12,3.5),sharey=True)
    for ax,arm in zip(axs,['static','normal']):
        for i,s in enumerate(stats):
            values=[s['completionByLength'][length][arm] for length in ['short','medium','long']]
            yy=[g['success']/g['n'] if g['n'] else np.nan for g in values];xx=np.arange(3)+(i-1.5)*.18
            ax.bar(xx,yy,.18,color=colors[i],label=labels[i])
            for xx0,yy0,g in zip(xx,yy,values):
                if g['n']:ax.text(xx0,yy0+.025,str(g['success'])+'/'+str(g['n']),ha='center',fontsize=7)
        ax.set_xticks(range(3),['Short','Medium','Long']);ax.set_title(arm.title()+' / length groups');ax.set_ylim(0,1.18)
    axs[0].set_ylabel('Explicit completion rate');axs[1].legend(fontsize=8);save(fig,'length-groups')
    codes=Counter()
    for r in primary:codes.update(r['physicalRejections']);codes.update(r['resourceRejections'])
    fig,ax=plt.subplots(figsize=(12,3.6));names=[k for k,v in codes.most_common()];bottom=np.zeros(len(names))
    for i,m in enumerate(MODELS):
        cc=Counter()
        for r in primary:
            if r['model']==m:cc.update(r['physicalRejections']);cc.update(r['resourceRejections'])
        values=np.array([cc[n] for n in names]);ax.bar(range(len(names)),values,bottom=bottom,color=colors[i],label=labels[i]);bottom+=values
    ax.set_xticks(range(len(names)),names,rotation=20,ha='right');ax.set_title('Rejected attempts by feedback code (not failure causes)');ax.set_ylabel('Attempts');ax.legend(fontsize=8);save(fig,'action-rejections')
    candidates=sorted([r for r in primary if r['arm']=='normal' and r['moves']>0],key=lambda r:(r['success'] is True,r['f1'],r['moves']),reverse=True)
    if candidates:
        chosen=candidates[:2];fig,axs=plt.subplots(len(chosen),7,figsize=(17,3*len(chosen)),squeeze=False)
        for y,r in enumerate(chosen):
            state=json.loads((ARENA/'runs'/r['runId']/'spectator.json').read_text());frames=[state['frames'][0]]+[f for f in state['frames'][1:] if (f.get('action') or {}).get('tool') in ('attach','detach','finish')]
            for col,idx in enumerate(np.linspace(0,len(frames)-1,6,dtype=int)):
                f=frames[int(idx)];ax=axs[y,col];ax.imshow(Image.open(ARENA/f['scenes']['isometric']['current'].lstrip('/')));ax.axis('off');ax.set_title('Start' if idx==0 else 'Decision '+str(f['index']))
            axs[y,6].imshow(Image.open(ARENA/frames[-1]['scenes']['isometric']['target'].lstrip('/')));axs[y,6].axis('off');axs[y,6].set_title('Target')
            axs[y,0].text(0,1.2,f"{r['label']} / case {r['sampleIndex']:02} / {'completed' if r['success'] else 'not completed'} / F1 {r['f1']:.2f}",transform=axs[y,0].transAxes)
        fig.subplots_adjust(wspace=.03,hspace=.4);save(fig,'actual-trajectories')
    reference_path=OUT/'reference/index.json'
    if reference_path.exists():
        references={(r['caseId'],r['arm']):r for r in json.loads(reference_path.read_text())['rows']}
        comparisons=sorted([r for r in primary if (r['caseId'],r['arm']) in references and r['moves']>0],key=lambda r:(r['arm']=='static',r['success'] is True,r['f1']),reverse=True)[:2]
        for i,r in enumerate(comparisons):
            ref=references[r['caseId'],r['arm']];state=json.loads((ARENA/'runs'/r['runId']/'spectator.json').read_text())
            frames=[state['frames'][0]]+[f for f in state['frames'][1:] if (f.get('action') or {}).get('tool') in ('attach','detach','finish')]
            fig,axs=plt.subplots(2,7,figsize=(17,5.5),squeeze=False)
            for y,items,label in [(0,frames,r['label']+' / actual / '+('completed' if r['success'] else 'not completed')),(1,ref['frames'],'Legal reference / one valid order / completed')]:
                indices=np.linspace(0,len(items)-1,min(6,len(items)),dtype=int)
                for col in range(6):
                    ax=axs[y,col];ax.axis('off')
                    if col>=len(indices):continue
                    f=items[indices[col]];image_path=ARENA/f['scenes']['isometric']['current'].lstrip('/') if y==0 else OUT/f['image']
                    ax.imshow(Image.open(image_path));ax.set_title('Start' if indices[col]==0 else ('Decision ' if y==0 else 'Move ')+str(f['index']))
                axs[y,6].imshow(Image.open(ARENA/frames[-1]['scenes']['isometric']['target'].lstrip('/')));axs[y,6].axis('off');axs[y,6].set_title('Target')
                axs[y,0].text(0,1.2,label,transform=axs[y,0].transAxes,fontsize=10)
            fig.subplots_adjust(wspace=.03,hspace=.4);save(fig,'model-vs-reference-'+str(i+1))


def markdown_report(report,data,primary,stats,charges,plan):
    def ratio(g):return f"{g['success']}/{g['denominator']}" if g['denominator'] else '未测到有效结果'
    md=['# Brick Atlas 扩展实验报告','',f"更新：{time.strftime('%Y-%m-%d %H:%M:%S')}（本机时间）",'',
        '**状态：'+('全部完成' if report['allWorkersFinished'] else '进行中；以下只包含已归档结果，不能当成最终全量成绩')+'。**','',
        '[本机逐步回放](http://127.0.0.1:8832/experiments) · [指标 JSON](metrics.json) · [输入与程序修复](REPAIRS.zh-CN.md)','',
        '## 1. 这次测什么','',
        '四个模型使用同一视觉 Agent、同一题单、观察规则和预算。每个模型50道静态阶段题、50道正常拼装题。正常拼装通过后，另跑同题事故分支；未通过时不把事故修复记为失败。上一批 Sol 缺项、Seed 中断题另列补测。',
        '静态题也允许模型调用观察与拆装工具，不是一次性静态选择题。静态与动态不保证目标和现场完全配对，本批不能量化纯粹的动态额外难度。',
        '当前统一输入版本：'+PROTOCOL+'。v4运行时发现view和分页的公共说明存在歧义，已作为接口排查记录保留；包括成功题在内，所有条件都用v5统一重跑，主表仅含v5，不挑成功结果。两版本费用全部保留。','',
        f"新样本：{plan['independentObjects']}个物件、{plan['sourceGroups']}个原始来源组；短/中/长为{plan['selectedLengths']}。这里是过程长度分组，不能直接等同于人类难度。",'',
        '## 2. 新样本结果','', '### 运行进度与接口状态','']
    statuses={s['model']:s for s in report['apiStatus']}
    md+=table(['模型','静态已归档/计划','正常拼装已归档/计划','事故已归档','接口检查'],[
        [s['label'],f"{s['newSampleCompleted']['static']}/50",f"{s['newSampleCompleted']['normal']}/50",s['newSampleCompleted']['incident'],
         '图像/历史/接口检查通过' if statuses[s['model']]['passed'] else str(statuses[s['model']].get('error'))+'；已通过'+str(statuses[s['model']]['passedProbes'])+'/3项图像检查'] for s in stats])
    md+=['','“已归档”包括明确记录的技术中断。未运行不是0分。hello通过只证明短文本调用可用，不能证明实际多图和长历史输入可用。','', '### 完成结果','']
    md+=table(['模型','静态正常','静态故障','正常拼装','合格事故修复','技术中断'],[[s['label'],*(ratio(s[k]) for k in ['control','repair','normal','incident']),s['technical']] for s in stats])
    md+=['','分数是成功数/有效分母。API中断、截断、程序错误和费用停止不进入能力分母；模型用完该题决策预算仍未完成，计入端到端未完成。格式错误单独保留，不能全归因为视觉识别。','',
        '![完成率及分母](plots/success-rates.png)','',
        '### 结构拼对和主动提交，分开看','',
        '完成率要求结构正确并调用finish；下表只看停止时结构是否达标，避免把“拼对了但没有主动提交”混同于结构错误。','']
    md+=table(['模型','静态结构达标','正常拼装结构达标','事故后结构达标'],[[s['label'],*[f"{s[k+'Structure']['satisfied']}/{s[k+'Structure']['n']}" if s[k+'Structure']['n'] else '不适用' for k in ['static','normal','incident']]] for s in stats])
    md+=['','![结构达标率](plots/structure-satisfaction.png)','', '## 3. 指标说明','']
    md+=table(['指标','含义'],[
        ['提交完成率','最终物理结构等价、约束通过，并主动finish。'],['结构达标率','停止时物理结构等价且约束通过；不额外要求finish。'],
        ['结构F1','零件种类、颜色、位置共同匹配，2TP/(2TP+FP+FN)；固定背景不加分。'],
        ['错误减少率','1-最终错误残差/初始残差；初始无错则不适用。'],['正确部分损坏','起点正确的件，到最后被弄错或拆掉的数量。'],
        ['合法动作率','接受的拆装次数/格式完整的拆装尝试。不是整题成功率。'],['正常现场误动','无错题执行过被接受的拆装；仅观察不算。'],
        ['合格事故修复','同题同模型正常前置成功、事故全部真实生效，才进入分母。'],
        ['观察策略','直接看现场、查候选、候选放大、点选辨认、查说明书分别记录。'],
        ['接口适配','接受的单JSON包装、字段错误、截断、服务失败分别统计。'],['效率','动作、API请求、输入/输出token、响应耗时和费用；参考路线不是最短路线证明。']])
    md+=['','## 4. 按错误类型与题目查看','', '![按静态错误类型](plots/error-families.png)','',
        '![静态逐题F1](plots/matrix-static.png)','', '![正常拼装逐题F1](plots/matrix-normal.png)','', '![事故逐题F1](plots/matrix-incident.png)','',
        '## 5. 费用、token和观察负担','']
    md+=table(['模型','请求数（含检查）','输入token','输出token','费用估算CNY','API拒绝','未确定请求'],[[s['label'],s['apiRequests'],s['inputTokens'],s['outputTokens'],fmt(s['cny'],4),s['rejectedAPI'],s['uncertainAPI']] for s in stats])
    md+=['','输出token已包含服务商报告的推理token，不能再叠加。金额来自实际返回用量乘已记录单价；不是账单。Sol的Ark价格未核实，使用明确标注的暂估价。hello诊断的微量用量另见 diagnostics/hello-20261030。','',
        '![用量和费用](plots/tokens-and-cost.png)','', '![观察策略](plots/observation-actions.png)','',
        '### 按过程长度分组','', '![长度分组](plots/length-groups.png)','',
        '### 操作合法性与接口错误','']
    md+=table(['模型','接受动作/拆装尝试','合法率','放大候选','点选辨认','JSON格式错','字段错','接受完整JSON包装','技术中断原因'],[
        [s['label'],str(s['actionSummary']['accepted'])+'/'+str(s['actionSummary']['attempts']),fmt(s['actionSummary']['rate']),
         s['toolSummary']['detailQueries'],s['toolSummary']['pointQueries'],s['toolSummary']['formatErrors'],s['toolSummary']['schemaErrors'],s['toolSummary']['proseJSONAccepted'],s['technicalCodes']] for s in stats])
    md+=['','![动作拒绝码](plots/action-rejections.png)','',
        '## 6. 我们这边修了什么','',
        '- 静态说明书只能看到本题目标阶段，明确剩余库存可以不用。',
        '- 增加单个候选位置的全尺寸对照，保持当前/预览同画布。',
        '- 增加点选当前图辨认可见零件编号，不查询隐藏件或答案。',
        '- 说明书标出所示零件的操作编号，不再要求先猜图片对应哪个匿名编号；不提供目标位置编号。',
        '- 接受代码围栏或解释之后的唯一完整JSON；拒绝多个对象、缺损JSON和截断。',
        '- 单轮输出预留从8192降到2048；较大图片包和长历史也做接口检查。截断仍不执行。',
        '- 只对明确未生成内容的429有限重试，等待时不改变题目状态；权限错误和未知计费请求不盲重试。',
        '- 原始响应中的模型版本要与配置匹配，防止接入点指向别的模型而被误标。',
        '- 旧实验不改分；新输入、补测和新增样本分开保存。','',
        '- v5把观察和点选的view取值逐工具列明；明确旋转是相对角度、点选坐标是0到1、放大候选时不带page。动作规则和单题预算保持一致。','',
        '本批曾出现长段解释达到2048输出token上限，完整动作尚未返回。这类记录保留为截断，不执行、不计入拼装能力分母，也不自动重复生成。统一额度不能保证永不截断；若提高额度，需要给全部模型另设同一实验条件。','',
        '这些修正解决接口和操作可用性问题，不代表已证明所有题目都适合真人、所有拆装都符合真实力学。','',
        '## 7. 上一批补测','']
    supplements=[r for r in data if r['group']!='new-sample' and r['inputVersion']==PROTOCOL]
    md+=table(['物件','模型','分支','结果','F1','API请求','CNY'],[[r['object'],r['label'],r['arm'],'成功' if r['success'] else '未完成' if r['success'] is False else r['terminal'],fmt(r['f1']),r['calls'],fmt(r['cny'],4)] for r in supplements])
    md+=['','补测使用修正后的输入，不能直接与旧输入成绩合并成同一设置的均值。','', '## 8. 真实操作轨迹与剩余问题','']
    if (OUT/'plots/actual-trajectories.png').exists():md+=['![模型实际动作过程](plots/actual-trajectories.png)','']
    for i in (1,2):
        if (OUT/f'plots/model-vs-reference-{i}.png').exists():md+=[f'![实际模型与合法参考过程对比{i}](plots/model-vs-reference-{i}.png)','']
    md+=['参考行由程序执行一条合法路线生成，未发送给模型，不证明路线最短，也不要求模型照同样顺序操作。','']
    md+=['若正常拼装未通过，就没有该条件下的动态修复证据。动作被拒可能涉及位置或顺序判断；不能只根据拒绝码认定模型不懂物理。候选预览可读性仍需真人盲操作，拆装合法性仍需独立验证。',
        '目前参考路径可执行和图片可见性检查来自同一实现；不能当成独立验证。按家族/长度的样本量较小，结果不支持正式模型排名或显著性结论。','',
        '## 9. 逐题记录','']
    md+=table(['编号','物件','模型','题型/错误','结果','F1','动作/尝试','输入/输出token','CNY','回放'],[[r['sampleIndex'],r['object'],r['label'],r['taskType']+'/'+r['family'],'成功' if r['success'] else '未完成' if r['success'] is False else r['terminal'],fmt(r['f1']),f"{r['moves']}/{r['manipulations']}",f"{r['inputTokens']}/{r['outputTokens']}",fmt(r['cny'],4),f"[查看]({r['url']})"] for r in data if r['inputVersion']==PROTOCOL])
    md+=['', '旧v4接口排查记录共'+str(sum(r['inputVersion']!=PROTOCOL for r in data))+'次，完整保存在metrics.json的rows中，并标注inputVersion；不混入当前主表。','']
    md+=['','## 10. 文件','', '`metrics.json` 保存完整指标；`workers/` 保存模型报告；`ledgers/`保存请求用量；`plots/`保存PNG/SVG/PDF；原始模型输入输出和场景图保存在各个 arena run 中。','']
    return '\n'.join(md)


def main():
    report,data,primary,stats,charges=collect();plan=json.loads((OUT/'plan.json').read_text())
    make_plots(primary,stats,plan)
    metrics=dict(generatedAt=time.time(),complete=report['allWorkersFinished'],inputVersion=PROTOCOL,rows=data,primaryRows=primary,summary=stats,
        notRun=report['notRun'],apiStatus=report['apiStatus'],workers=report['workers'],planSha256=hashlib.sha256((OUT/'plan.json').read_bytes()).hexdigest())
    write_json(OUT/'metrics.json',metrics);write_json(OUT/'combined-report.json',report)
    md=markdown_report(report,data,primary,stats,charges,plan);(OUT/'README.zh-CN.md').write_text(md)
    import markdown
    body=markdown.markdown(md,extensions=['tables','fenced_code'])
    style='body{font:15px/1.7 -apple-system,"PingFang SC",sans-serif;color:#213a46;max-width:1350px;margin:30px auto;padding:0 20px}table{display:block;overflow:auto;border-collapse:collapse;font-size:12px;white-space:nowrap}td,th{padding:7px;border-bottom:1px solid #d8e3e6}th{background:#edf4f5}h1,h2{color:#126c75}img{max-width:100%;max-height:1400px;display:block;margin:20px auto}a{color:#087d87}'
    (OUT/'index.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>Brick Atlas 扩展实验</title><style>'+style+'</style>'+body+'</html>')
    print('REPORT',len(data),'archived runs;',len(primary),'new sample conditions;',len(charges),'requests',flush=True)


if __name__=='__main__':main()
