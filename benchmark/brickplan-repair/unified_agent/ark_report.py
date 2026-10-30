"""Rebuild transparent pilot tables and Matplotlib figures from immutable runs."""
import gzip,hashlib,html,json,statistics,time
from collections import Counter
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
from PIL import Image
from dynamic_arena import OUT as ARENA
from dynamic_arena.transport import write_json
from unified_agent.ark_batch import OUT,MODELS,LEDGER,combined_report

LABELS=['GPT-6.1 Sol','Seed 2.1 Pro','DeepSeek V4.1 Flash','Qwen3.8 Flash']
SHORT=dict(zip(MODELS,LABELS));ARMS={'S0':'静态正常现场','S1':'静态故障现场','D0':'正常拼装','D1':'单次事故','D2':'两次事故'}
VALID={'completed','model_budget_exhausted'}
STATUS={'completed':'已提交','model_budget_exhausted':'单题额度用完','service_error':'API 中断','output_truncated':'输出截断','provider_output_error':'API 返回异常','client_budget_exhausted':'费用额度停止','harness_error':'程序中断'}

def mean(xs):return sum(xs)/len(xs) if xs else None
def fmt(x,n=3):return '—' if x is None else f'{x:.{n}f}'
def table(headers,rows):return ['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']+['| '+' | '.join(str(c) for c in r)+' |' for r in rows]

def rows(report):
 out=[]
 for r in report['runs']:
  s,e,c,u=r['stateMetrics'],r['executionMetrics'],r['controllerMetrics'],r['providerUsage']
  log=json.loads((ARENA/'runs'/r['arenaRunId']/'log.json').read_text())
  codes=Counter(call.get('environmentOutput',{}).get('code','unknown') for call in log['calls'])
  counts=r['inputMetrics']['imageCounts'];nqr=r['normalQualifiedRecovery']
  out.append(dict(model=r['model'],label=SHORT[r['model']],object=r['objectTitle'],objectId=r['objectId'],caseId=r['caseId'],runId=r['arenaRunId'],
   arm=r['arenaBranch'],taskType=r['taskType'],lengthGroup=r['lengthGroup'],fullModuleParts=r['activeParts'],targetParts=s['fullPlacement']['tp']+s['fullPlacement']['fn'],terminal=r['terminalStatus'],
   success=r['success'],eligible=r['terminalStatus'] in VALID,assemblyEligible=r['assemblyScoreEligible'],
   apiError=next((x['error'].get('code') for x in reversed(log['calls']) if x.get('error')),None),
   f1=s['fullPlacement']['f1'],typeColorF1=s['partTypeColor']['f1'],shapePoseF1=s['shapeAndPose']['f1'],colorPoseF1=s['colorAndPose']['f1'],
   initialResidual=s['initialEditResidual'],finalResidual=s['finalEditResidual'],errorReduction=s['errorReduction'],finalDamage=s['finalDamageCount'],falseRepair=e['falseRepair'],
   decisions=c['decisions'],calls=r['apiCalls'],attach=sum(x.get('modelOutput',{}).get('tool')=='attach' for x in log['calls']),
   detach=sum(x.get('modelOutput',{}).get('tool')=='detach' for x in log['calls']),observe=c['observeCalls'],inspect=c['inspectCalls'],recall=c['recallCalls'],
   freshCurrentObservations=sum(x.get('modelOutput',{}).get('tool')=='observe' and 'current' in x.get('modelOutput',{}).get('args',{}).get('show',[]) and x.get('environmentOutput',{}).get('code')=='OBSERVED' for x in log['calls']),
   candidateQueries=sum(x.get('modelOutput',{}).get('tool')=='inspect' and 'partId' in x.get('modelOutput',{}).get('args',{}) and x.get('environmentOutput',{}).get('code')=='OBSERVED' for x in log['calls']),
   manualQueries=sum(x.get('modelOutput',{}).get('tool')=='inspect' and 'manualStep' in x.get('modelOutput',{}).get('args',{}) and x.get('environmentOutput',{}).get('code')=='OBSERVED' for x in log['calls']),
   invalidCandidateRequests=codes['UNREGISTERED_POSE'],
   moves=e['acceptedMoves'],manipulations=e['wellFormedManipulationAttempts'],legalActionRate=e['legalActionRate'],physicalRejections=e['physicalRejections'],resourceRejections=e['resourceRejections'],
   formatErrors=e['formatErrorResponses'],schemaErrors=e['schemaErrorResponses'],budgetRejections=e['budgetRejectedResponses'],feedbackCodes=dict(codes),
   referenceMoves=r['casePreflight']['moves'],scheduled=r['scheduledEvents'],applied=r['appliedEvents'],recoveryEligible=nqr['eligible'],recoverySuccess=nqr['success'],recoveryReason=nqr['reason'],eventWindows=r['eventWindows'],
   inputTokens=u['promptTokens'],outputTokens=u['completionTokens'],reasoningTokens=u['reasoningTokens'],cny=u['nativeCosts'].get('CNY',0),
   imagesTotal=sum(counts),imagesMean=mean(counts),imagesMax=max(counts,default=0),
   url='http://127.0.0.1:8831/ark?run='+r['arenaRunId']))
 return out

def summary(data,charges):
 out=[]
 for model in MODELS:
  rs=[r for r in data if r['model']==model];cs=[c for c in charges if c['model']==model]
  row=dict(model=model,label=SHORT[model],runs=len(rs),apiRequests=len(cs),inputTokens=sum(c.get('promptTokens',0) for c in cs),outputTokens=sum(c.get('completionTokens',0) for c in cs),
   reasoningTokens=sum(c.get('reasoningTokens') or 0 for c in cs),cny=sum(c.get('nativeCost',0) for c in cs),
   technical=sum(not r['eligible'] for r in rs),schema=sum(r['formatErrors']+r['schemaErrors'] for r in rs),assemblyEligible=sum(r['assemblyEligible'] for r in rs),
   rejectedAPI=sum(c['status']=='rejected_before_generation' for c in cs),uncertainAPI=sum(c['status'] in ('pending','uncertain') for c in cs))
  times=[c['latencySeconds'] for c in cs if c.get('promptTokens') is not None and 'latencySeconds' in c]
  row.update(apiLatencyMedian=statistics.median(times) if times else None,apiLatencyP90=float(np.percentile(times,90)) if times else None,
   falseRepairCount=sum(r['falseRepair'] for r in rs if r['taskType']=='S0' and r['eligible']),
   structureCorrectWithoutFinish=sum(r['f1']==1 and r['success'] is False for r in rs if r['eligible']))
  for group,kinds in [('control',{'S0'}),('repair',{'S1'}),('normal',{'D0'}),('incident',{'D1','D2'})]:
   selected=[r for r in rs if r['taskType'] in kinds]
   valid=[r for r in selected if r['eligible'] and (group!='incident' or r['recoveryEligible'])]
   row[group]=dict(run=len(selected),denominator=len(valid),success=sum(r['success'] is True for r in valid),f1=mean([r['f1'] for r in valid]))
  out.append(row)
 return out

def plots(data,stats,plan):
 folder=OUT/'plots';folder.mkdir(exist_ok=True)
 font=Path('/System/Library/Fonts/Supplemental/Comic Sans MS.ttf')
 if font.exists():font_manager.fontManager.addfont(str(font));plt.rcParams['font.family']='Comic Sans MS'
 plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42,'savefig.dpi':240})
 def save(fig,name):
  for ext in ('png','svg','pdf'):
   path=folder/(name+'.'+ext);fig.savefig(path,bbox_inches='tight',facecolor='white')
   if ext=='svg':path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
  plt.close(fig)
 fig,axs=plt.subplots(1,4,figsize=(14,3.5),sharey=True)
 for ax,group,title in zip(axs,['control','repair','normal','incident'],['Correct static scene','Faulty static scene','Normal build','Qualified recovery']):
  for i,s in enumerate(stats):
   g=s[group];v=g['success']/g['denominator'] if g['denominator'] else 0
   ax.bar(i,v,color='#168b8b' if g['denominator'] else '#d9dfe3',width=.65)
   ax.text(i,v+.035,f"{g['success']}/{g['denominator']}" if g['denominator'] else 'N/A',ha='center',fontsize=9)
  ax.set_title(title);ax.set_xticks(range(4),['Sol','Seed Pro','DS Flash','Qwen'],rotation=25);ax.set_ylim(0,1.18);ax.grid(axis='y',alpha=.2)
 axs[0].set_ylabel('Successful / eligible episodes')
 fig.suptitle('Small pilot: denominators shown; unavailable runs are not zero scores',y=1.06)
 save(fig,'success-rates')
 tasks=[]
 for i,obj in enumerate(plan['objects']):
  tasks.extend([(f"O{i+1} / {label}",cid,arm) for label,cid,arm in [('S0',obj['staticCases'][0],'static'),('S1',obj['staticCases'][1],'static'),('D0',obj['dynamicCase'],'normal'),('D+',obj['dynamicCase'],'incident')]])
 grid=np.full((len(tasks),4),np.nan);labels={}
 for y,(_,cid,arm) in enumerate(tasks):
  for x,m in enumerate(MODELS):
   r=next((r for r in data if r['model']==m and r['caseId']==cid and r['arm']==arm),None)
   if r:
    if r['eligible'] and (arm!='incident' or r['recoveryEligible']):grid[y,x]=r['f1'];labels[y,x]=f"{r['f1']:.2f}"+(' OK' if r['success'] else '')
    else:labels[y,x]='INT' if not r['eligible'] else 'N/T'
   else:labels[y,x]='N/A'
 fig,ax=plt.subplots(figsize=(7.5,7.5));cmap=plt.colormaps['YlGnBu'].copy();cmap.set_bad('#e9ecef')
 im=ax.imshow(grid,vmin=0,vmax=1,cmap=cmap,aspect='auto');ax.set_xticks(range(4),['Sol','Seed Pro','DS Flash','Qwen']);ax.set_yticks(range(len(tasks)),[t[0] for t in tasks]);ax.set_title('Final placement F1 by task and backbone')
 for (y,x),label in labels.items():ax.text(x,y,label,ha='center',va='center',fontsize=9,color='white' if grid[y,x]>.65 else '#253843')
 fig.colorbar(im,ax=ax,label='F1');fig.text(.08,-.015,'O1 Cement mixer | O2 Airplane | O3 Tractor | O4 Bookshelf\nINT: technical interruption; N/T: incident not fully triggered; N/A: not run.',fontsize=9)
 save(fig,'case-matrix')
 fig,axs=plt.subplots(1,2,figsize=(11,3.7));x=np.arange(4)
 axs[0].bar(x,[s['inputTokens']/1e6 for s in stats],color='#236b83',label='Input')
 axs[0].bar(x,[s['outputTokens']/1e6 for s in stats],bottom=[s['inputTokens']/1e6 for s in stats],color='#e5a44d',label='Output incl. reported reasoning')
 axs[0].set_ylabel('Million tokens');axs[0].legend(fontsize=8);axs[0].set_title('All returned usage, including probes')
 axs[1].bar(x,[s['cny'] for s in stats],color=['#b7c0c6','#168b8b','#168b8b','#168b8b'])
 for i,s in enumerate(stats):axs[1].text(i,s['cny'],f"{s['cny']:.3f}",ha='center',va='bottom')
 axs[1].set_ylabel('CNY estimate');axs[1].set_title('Sol provisional; other models at list rates')
 for ax in axs:ax.set_xticks(x,['Sol','Seed Pro','DS Flash','Qwen']);ax.grid(axis='y',alpha=.15)
 save(fig,'tokens-and-cost')
 codes=Counter()
 for r in data:codes.update(r['physicalRejections']);codes.update(r['resourceRejections'])
 fig,ax=plt.subplots(figsize=(10,3.8));names=[x for x,n in codes.most_common()]
 if names:
  bottom=np.zeros(len(names))
  for m,color in zip(MODELS,['#356a94','#168b8b','#dc9a43','#805ca0']):
   c=Counter()
   for r in data:
    if r['model']==m:c.update(r['physicalRejections']);c.update(r['resourceRejections'])
   values=np.array([c[n] for n in names]);ax.bar(range(len(names)),values,bottom=bottom,label=SHORT[m],color=color);bottom+=values
  ax.set_xticks(range(len(names)),names,rotation=18,ha='right');ax.legend(fontsize=8)
 else:ax.text(.5,.5,'No physical rejections recorded',ha='center',transform=ax.transAxes)
 ax.set_title('Rejected action attempts (not episode failures)');ax.set_ylabel('Attempts');save(fig,'physical-rejections')
 # Actual scene snapshots only. A target image is a target, never labelled a GT trajectory.
 candidates=[r for r in data if r['referenceMoves']>0 and r['moves']>0]
 selected=sorted(candidates,key=lambda r:(r['arm']=='incident',r['success'] is True,r['moves']),reverse=True)[:2]
 if selected:
  fig,axs=plt.subplots(len(selected),7,figsize=(17,3*len(selected)),squeeze=False)
  for rid,r in enumerate(selected):
   state=json.loads((ARENA/'runs'/r['runId']/'spectator.json').read_text());frames=state['frames'];ids=np.linspace(0,len(frames)-1,6,dtype=int)
   for col,idx in enumerate(ids):
    f=frames[int(idx)];ax=axs[rid,col];ax.imshow(Image.open(ARENA/f['scenes']['isometric']['current'].lstrip('/')));ax.axis('off');ax.set_title('Start' if idx==0 else f"Decision {f['index']}",fontsize=10)
   ax=axs[rid,6];ax.imshow(Image.open(ARENA/frames[-1]['scenes']['isometric']['target'].lstrip('/')));ax.axis('off');ax.set_title('Target',fontsize=10)
   axs[rid,0].text(0,1.20,f"{r['label']} / {r['taskType']} / F1={r['f1']:.2f} / success={r['success']}",transform=axs[rid,0].transAxes,fontsize=11)
  fig.subplots_adjust(wspace=.03,hspace=.42);save(fig,'actual-trajectories')
  reference=OUT/'reference/index.json'
  if reference.exists():
   refs=json.loads(reference.read_text())['rows']
   r=selected[0];ref=next(x for x in refs if x['caseId']==r['caseId'] and x['arm']==r['arm'])
   state=json.loads((ARENA/'runs'/r['runId']/'spectator.json').read_text())
   model_frames=[state['frames'][0]]+[f for f in state['frames'][1:] if (f.get('action') or {}).get('tool') in ('attach','detach','finish')]
   if len(model_frames)==1:model_frames=state['frames']
   fig,axs=plt.subplots(2,7,figsize=(17,5.3),squeeze=False)
   for row,frames,label in [(0,model_frames,r['label']+' / actual actions'),(1,ref['frames'],'Legal reference / one valid order')]:
    ids=np.linspace(0,len(frames)-1,min(6,len(frames)),dtype=int)
    for col in range(6):
     ax=axs[row,col];ax.axis('off')
     if col>=len(ids):continue
     f=frames[int(ids[col])];path=ARENA/f['scenes']['isometric']['current'].lstrip('/') if row==0 else OUT/f['image']
     ax.imshow(Image.open(path));ax.set_title('Start' if ids[col]==0 else ('Decision '+str(f['index']) if row==0 else 'Move '+str(f['index'])),fontsize=10)
    ax=axs[row,6];ax.imshow(Image.open(ARENA/state['frames'][-1]['scenes']['isometric']['target'].lstrip('/')));ax.axis('off');ax.set_title('Target',fontsize=10)
    axs[row,0].text(0,1.20,label,transform=axs[row,0].transAxes,fontsize=11)
   fig.subplots_adjust(wspace=.03,hspace=.4);save(fig,'model-vs-reference')

def main():
 report=combined_report();plan=json.loads((OUT/'plan.json').read_text());ledger=json.loads(LEDGER.read_text());data=rows(report);stats=summary(data,ledger['charges'])
 write_json(OUT/'combined-pilot.json',report)
 metrics=dict(generatedAt=time.time(),scope=report['staticInterpretation'],rows=data,summary=stats,notRun=report.get('notRun',[]),pendingModels=report.get('pendingModels',[]),
  definitions={'success':'Explicit finish and physically equivalent target, with final constraints.','F1':'2TP/(2TP+FP+FN), physical part type/color/pose equivalence. Fixed context excluded.',
  'qualifiedRecovery':'Successful matched normal prerequisite; completed or model-budget-exhausted incident episode, all scheduled effective events applied.',
  'legalActionRate':'Accepted physical moves / well-formed physical attempts, per evaluator. Not an episode success rate.',
  'falseRepair':'At least one accepted move on an initially correct S0 scene; extra observations alone do not count.',
  'errorReduction':'1 - final edit residual / initial residual; N/A when initial residual is zero. Can be negative.',
  'referenceMoves':'One legal reference path, not a proven shortest path. Alternative orders are accepted.'})
 write_json(OUT/'metrics.json',metrics);plots(data,stats,plan)
 def ratio(g):return f"{g['success']}/{g['denominator']}" if g['denominator'] else '—（无有效题）'
 md=['# 四模型小批量实验：结果与用量','',
 '[逐步回放](http://127.0.0.1:8831/ark) · [完整指标 JSON](metrics.json) · [预先登记题单](plan.json)','',
 '**这是一批流程试验，不是全库成绩或模型排名。** 每个条件只跑一次。静态现场也由同一视觉 Agent 操作，当前表格不代表一次性静态问答。',
 '所有动作由真实 API 模型决定。正常拼装成功后才进入同物件事故分支；未运行、API 中断、截断、预算停止不当作拼装失败。','',
 '## 1. 结果汇总','']
 md+=table(['Backbone 版本','路由','请求模型/接入点','接口预检'],[[s['model'], 'Aliyun' if s['model'].startswith('qwen') else 'Ark',s['inferenceModel'],'通过（运行仍可能限流）' if s['passed'] else s.get('error') or '未通过'] for s in report.get('apiStatus',[])])
 md+=['']
 md+=table(['物件','完整待拼模块件数','静态阶段目标件数','长度组','静态错误','预设动态错误'],[[o['title'],o['activeParts'],next((r['targetParts'] for r in data if r['objectId']==o['model'] and r['arm']=='static'),'—'),o['lengthGroup'],o['staticError'],o['dynamicError']] for o in plan['objects']])
 md+=['','长度组只用于覆盖不同规模，尚不是经过真人和模型表现验证的难度等级。当前批次使用 v2 输入；收尾后的 v3 输入修正没有重新调用模型或改写这些成绩。','']
 md+=table(['模型 / 路由','静态正常现场','静态故障','正常拼装','合格事故修复','技术中断'],[[s['label']+(' / Aliyun' if s['model'].startswith('qwen') else ' / Ark'),*(ratio(s[g]) for g in ('control','repair','normal','incident')),s['technical']] for s in stats])
 md+=['','表内为成功数 / 有效运行数。事故分母还要求正常前置通过、事故全部真实发生。格式错误保留在端到端结果中；只分析拆装能力时另看 `assemblyEligible`。','',
 '### 指标是什么意思','']
 md+=table(['指标','怎么算、说明什么'],[
  ['完成率','合法最终结构与目标等价，并明确调用 finish，才算成功。API 中断不进入能力分母。'],
  ['结构 F1','综合零件种类、颜色、位置是否正确：2TP/(2TP+FP+FN)。只算可操作部分，固定背景不加分。'],
  ['正常现场误动','本来正确的 S0 题中，是否执行了至少一次被接受的拆装。多观察不算误动。'],
  ['错误减少率','1 − 最后错误残差/初始错误残差。负数表示越修越错；初始无错时不适用。'],
  ['正确部分损坏','起点正确的部件，到最后还有多少被弄错或拆掉。'],
  ['合法动作率','被环境接受的拆装次数/格式完整的拆装尝试。与整题成功率分开。'],
  ['合格事故修复率','同题正常拼装成功，且事故分支所有安排的事故都生效，才进入修复分母。'],
  ['分次事故恢复','每次事故到下一次事故之前是否恢复、多久恢复、恢复后能否保持。详情保留在 eventWindows。'],
  ['观察与查页','新现场图、候选位置页、说明书页分别统计；不是简单把所有工具调用当观察。'],
  ['Token / 时间 / 费用','输入含图片编码，输出已包含服务商报告的推理 token，不能再加一次。API 耗时含网络，不含客户端限流等待。'],
  ['GT 步数','一条已验证的参考路线，供检查与对照；不是唯一顺序，也不是最短路线证明。']])
 md+=['',
 '![成功率与有效分母](plots/success-rates.png)','', '## 2. 逐题结果','']
 md+=table(['物件','模型','题型','结果','F1','轮数','合法动作/尝试','新现场图','候选/说明页','GT动作','事故触发'],[[r['object'],r['label'],ARMS[r['taskType']],f"[{'成功' if r['success'] is True else '未完成' if r['success'] is False else STATUS.get(r['terminal'],r['terminal'])}]({r['url']})",fmt(r['f1']),r['decisions'],f"{r['moves']}/{r['manipulations']}",r['freshCurrentObservations'],f"{r['candidateQueries']}/{r['manualQueries']}",r['referenceMoves'],f"{r['applied']}/{r['scheduled']}" if r['scheduled'] else '不适用'] for r in data])
 md+=['','GT 动作数是一条已验证的合法路径，不要求模型按该顺序，也不能当作最短步数。技术中断的 F1 只是停止时的现场状态。','',
 '![逐题结构正确程度](plots/case-matrix.png)','', '## 3. Token、费用、图片负担','']
 md+=table(['模型','API请求（含检查）','输入tokens','输出tokens','其中推理tokens','费用估算 CNY','API拒绝/未确定'],[[s['label'],s['apiRequests'],s['inputTokens'],s['outputTokens'],s['reasoningTokens'],fmt(s['cny'],4),f"{s['rejectedAPI']}/{s['uncertainAPI']}"] for s in stats])
 md+=['','Sol 的 Ark 价格未公开核实，用户已授权直接运行；Sol 金额仅用 OpenAI 原生 $2/$10 每百万 token × 假设 7.5 汇率换算。**它不是 Ark 账单，不构成实际费用硬上限。** 其余按 Ark 高峰常规价格 / Aliyun 返回的最高价档估算，不假设缓存、免费额度和折扣。费用包含接口检查、失败和被中止尝试。',
 '价格来源：[Ark](https://docs.volcengine.com/docs/ark/model-pricing?lang=zh&redirect=1)、[OpenAI Sol 原生参考价](https://developers.openai.com/api/docs/models/gpt-6.1-sol)、Aliyun 已归档 `provider.json` 中的认证目录响应。','',
 '![用量与费用](plots/tokens-and-cost.png)','']
 md+=table(['模型','API耗时中位数/秒','P90/秒','正常现场误动题数','结构正确但未提交题数'],[[s['label'],fmt(s['apiLatencyMedian'],2),fmt(s['apiLatencyP90'],2),s['falseRepairCount'],s['structureCorrectWithoutFinish']] for s in stats])
 md+=['','Seed Pro 为处理端点限流，在调用之间额外等待 65 秒。这会增加整场耗时，但不改变题目状态或动作预算。','']
 md+=table(['物件/题型','模型','输入tokens','输出tokens','费用 CNY','图片 平均/最大','格式/字段错误'],[[r['object']+'/'+r['taskType'],r['label'],r['inputTokens'],r['outputTokens'],fmt(r['cny'],4),f"{fmt(r['imagesMean'],1)}/{r['imagesMax']}",f"{r['formatErrors']}/{r['schemaErrors']}"] for r in data])
 md+=['','### 扩大试验时的粗估','', '以下只用没有技术中断的已尝试题目，包含用完动作额度而未成功的运行；不只挑成功的便宜题。每 100 题的金额是样本均价乘 100，不是上限或置信区间。','']
 projection=[]
 for model in MODELS:
  for kind,label in [('static','静态现场 Agent'),('normal','正常拼装 Agent')]:
   sample=[r for r in data if r['model']==model and r['arm']==kind and r['eligible']]
   projection.append([SHORT[model],label,len(sample),fmt(mean([r['cny'] for r in sample]),4),fmt(mean([r['cny']*100 for r in sample]),2),round(mean([r['inputTokens']+r['outputTokens'] for r in sample])) if sample else '—'])
 md+=table(['模型','条件','有效样本','每题平均 CNY','100题粗估 CNY','每题平均总tokens'],projection)
 md+=['','Seed 的有效样本只有静态正常现场，不能据此估算故障修复。Sol 未获得生成结果。**事故修复没有合格样本，暂不能给全动态题库一个有依据的总价。** 下一批应先取得正常拼装成功和事故修复样本，再估算扩大量；不按本次跳过事故带来的低费用作宣传。','']
 md+=['','## 4. 错误与行为','', '![物理动作被拒绝的类型](plots/physical-rejections.png)','',
 '碰撞、无连接、拆出路径被挡，是几何动作检查拒绝；UNREGISTERED_POSE 是选了该零件未提供的位置编号，单独归为编号选择错误。JSON/字段错误另列。新现场图只统计成功观察 current；候选页也能透露部分当前场景，但展示的是假设放置，不能等同于一次直接观察。','']
 md+=table(['物件/题型','模型','最终多/少件残差','已有正确件损坏','正常现场误操作','拒绝类型'],[[r['object']+'/'+r['taskType'],r['label'],r['finalResidual'],r['finalDamage'],'是' if r['falseRepair'] else '否',', '.join(f'{k}:{v}' for k,v in r['physicalRejections'].items()) or '—'] for r in data])
 interrupted=[r for r in data if not r['eligible']]
 if interrupted:
  md+=['','### 中断明细','']+table(['物件/题型','模型','中断原因','请求次数','停止时 F1（不是成功率）'],[[r['object']+'/'+r['taskType'],r['label'],r['apiError'] or r['terminal'],r['calls'],fmt(r['f1'])] for r in interrupted])
 if (OUT/'plots/actual-trajectories.png').exists():md+=['','![真实模型操作过程，末列为目标](plots/actual-trajectories.png)','']
 if (OUT/'plots/model-vs-reference.png').exists():md+=['![模型实际操作与合法参考路径对照](plots/model-vs-reference.png)','上排来自真实模型日志，下排是程序执行的一条合法参考路径。GT 未提供给模型；不是最优路径证明。','']
 md+=['## 5. 输入和公平性边界','',
 '- 起点提供当前三视图、目标三视图和库存第一页，共 7 张；每次动作后不自动刷新现场。模型主动调用 observe 才能看新状态。',
 '- 后续保留三个目标、最近两次现场观察、库存页、最近候选或说明书页和最近 8 轮文字历史。图片数量由模型的观察选择决定，逐轮可查。',
 '- 同物件、同条件的目标、库存、候选位置、动作/观察/输出预算一致。模型推理开关按 API 能力设置，不能声称实际算力相等。',
 '- 本批 v2 静态题是给定阶段的验收目标，但可查说明书包含后续步骤；虽标记为 referenceOnly / isTarget=false，仍可能诱发过度拼装。这是解释风险，不能把所有静态失误都归因于视觉能力。后续 v3 已明确当前阶段目标并禁止查询越过该阶段的步骤；本批未重跑，改善效果尚未测量。',
 '- 正常和事故是两次独立运行，不是同一轨迹在事故点分叉。静态与动态目标也并非逐现场配对，所以这批不能计算纯粹的“动态额外困难”。',
 '- 参考路径、三视图和合法动作检查来自现有引擎，不能替代真人盲操作与独立物理验证。','',
 '## 6. 未运行条件','']
 md+=table(['模型','物件','分支','原因'],[[SHORT[r['model']],r.get('objectTitle',r['caseId']),r['condition'],r['reason']] for r in report.get('notRun',[])])
 md+=['','本批状态：'+('全部预定条件已归档为运行结果或未运行原因。' if report.get('allWorkersFinished') else '仍有运行未结束。'),'','## 7. 检查结果与仍需补证','']
 audits=[]
 for filename,label in [('selected-cases.json','16 个任务条件的参考动作与图片'),('evidence-audit.json','原始请求、返回用量与图片哈希'),('fairness-audit.json','同条件下各模型的输入与预算'),('final-visual-audit.json','最终三视图一致但结构评分不同的排查')]:
  p=OUT/'checks'/filename
  if p.exists():
   a=json.loads(p.read_text());ok=a.get('passed',a.get('flagged',1)==0)
   audits.append([label,'通过' if ok else '待复核',f'[证据](checks/{filename})'])
 md+=table(['检查','结果','明细'],audits)
 md+=['','[无付费单元/集成检查日志](checks/unit-tests.txt)。上述检查证明保存的输入、用量和当前引擎内部执行一致；它们不证明真人可读性，也不替代独立几何/拆装验证。','',
 '本批暴露的下一步重点：先解决 Sol Key/接入点权限和 Seed TPM；用 v3 静态阶段输入做小规模对照；排查候选页中零件/位置选择和重复尝试；为不支持强制 JSON 的后端单独报告格式遵循；获得正常拼装通过样本后再测持续修复。当前结果不能支持“所有失败都来自模型视觉能力”的结论。','',
 '## 8. 文件与复现','',
 '- `combined-pilot.json` 合并全部模型的运行评分；`pilot.json` 为先启动的 Qwen 报告，其余在 `workers/`；`metrics.json` 保存逐题数值、汇总和指标定义。',
 '- [本批之后的输入修正](INPUT-FIX.zh-CN.md) 与 [查看/另开批次说明](RUN.zh-CN.md)。',
 '- `checks/selected-cases.json` 保存 16 个条件的无 API 参考路径和图片检查。',
 '- `preflight/` 和 `diagnostics/` 保存接口检查、原始拒绝原因与修复后检查。',
 '- `../brickplan-dynamic-arena/runs/<runId>/` 保存每轮 JSON、实际输入图、现场回放和原始 API 请求/响应。',
 '- `plots/` 提供 PNG、SVG、PDF，图中文字使用 Comic Sans MS。',
 '- 重新生成表图：`PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.ark_report`。不会调用模型。','']
 (OUT/'README.zh-CN.md').write_text('\n'.join(md))
 # A portable, compact index. Full per-step replay remains on the local read-only server.
 try:
  import markdown
  body=markdown.markdown('\n'.join(md),extensions=['tables','fenced_code'])
 except ImportError:
  body='<h1>实验结果</h1><p><a href="README.zh-CN.md">完整中文报告</a></p>'
  for name in ('success-rates','case-matrix','tokens-and-cost','physical-rejections','actual-trajectories'):
   if (OUT/'plots'/f'{name}.png').exists():body+=f'<img src="plots/{name}.png" alt="{name}">'
  body+='<pre>'+html.escape('\n'.join(md))+'</pre>'
 (OUT/'index.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Brick Atlas 实验结果</title><style>body{font:15px/1.7 -apple-system,"PingFang SC",sans-serif;color:#223a45;margin:32px auto;max-width:1400px;padding:0 22px}h1,h2{color:#126e79}table{border-collapse:collapse;display:block;overflow:auto;white-space:nowrap;font-size:13px;margin:18px 0}th,td{border-bottom:1px solid #d5e1e4;padding:8px 11px}th{background:#edf4f5}img{max-width:100%;display:block;margin:20px auto}a{color:#087d8e}pre{white-space:pre-wrap;overflow-wrap:anywhere}code{background:#f0f4f5}</style>'+body+'</html>')
 print('REPORT',len(data),'runs',len(ledger['charges']),'API attempts',flush=True)

if __name__=='__main__':main()
