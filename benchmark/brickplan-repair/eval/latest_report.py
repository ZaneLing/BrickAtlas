"""Audit latest runs and generate an independently reproducible matched-case plot."""
import os,json,shutil,inspect
from pathlib import Path
os.environ['BRICKPLAN_EVAL_OUT']='deliverables/brickplan-api-latest-2026-10-14'
import run,report
report.MODELS=['openai/gpt-6.1-sol','google/gemini-4-argon']
shutil.copy(run.ROOT/'deliverables/brickplan-api-pilot/budget-authorization.json',run.OUT/'budget-authorization.json')
s,viewer=report.collect()
s['coverage']['plannedRuns']=12
s['groups']=[g for g in s['groups'] if g['n'] or g['apiErrors']]
s['protocolSettings']=json.loads((run.OUT/'selection.json').read_text())
old=[]
for f in (run.ROOT/'deliverables/brickplan-api-pilot/runs').glob('*.json'):
 r=json.loads(f.read_text())
 if r['spec'] in s['protocolSettings']['specs']:
  old.append({'model':r['model'],'track':r['track'],'kind':r['spec'].get('kind','dynamic'),'success':r['metrics']['success'],'status':r['status'],'maxCalls':r['maxCalls'],'id':r['id']})
s['matchedHistoricalRuns']=old
accounting=run.OUT/'accounting-final.json'
if accounting.exists():s['accountingCheck']=json.loads(accounting.read_text())
run.dump(run.OUT/'summary.json',s)
plot=r'''from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
OUT=Path(__file__).resolve().parent
s=json.loads((OUT/'summary.json').read_text()); dest=OUT/'plots';dest.mkdir(exist_ok=True)
models=['openai/gpt-4.1-mini','google/gemini-2.5-flash','openai/gpt-6.1-sol','google/gemini-4-argon']
labels=['GPT-4.1 mini (8 calls)','Gemini 2.5 Flash (8 calls)','GPT-6.1 Sol (4 calls)','Gemini 4 Argon (4 calls)']
kinds=['height_layer','compound','dynamic']; rows=s['matchedHistoricalRuns']+s['rows']
fig,axes=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
for ax,track in zip(axes,['symbolic','visual']):
 a=np.full((3,4),np.nan)
 for r in rows:
  if r['track']==track and r['status']=='complete':a[kinds.index(r['kind']),models.index(r['model'])]=int(r['success'])
 ax.imshow(a,cmap=matplotlib.colors.ListedColormap(['#f7d8cb','#b7dfca']),vmin=0,vmax=1,aspect='auto')
 for (y,x),v in np.ndenumerate(a):ax.text(x,y,'PASS' if v==1 else 'FAIL' if v==0 else 'API ERROR',ha='center',va='center',fontsize=10)
 ax.set(xticks=range(4),xticklabels=labels,yticks=range(3),yticklabels=['Height layer / 3 actions','Coupled faults / 29 actions','From empty + color event'],title='Text state' if track=='symbolic' else '7 views + uniform part atlas')
 ax.tick_params(axis='x',rotation=30)
fig.suptitle('Same 3 source cases: historical vs latest model configurations',fontsize=14)
fig.supxlabel('One run per cell; selected cases, not bank accuracy. Latest: low reasoning, 4096 output tokens; old: 2200, Gemini reasoning off.',fontsize=9)
for ext in ('png','svg','pdf'):fig.savefig(dest/f'completion.{ext}',dpi=180,bbox_inches='tight')
plt.close(fig)
'''
(run.OUT/'plot.py').write_text(plot)
exec(compile(plot,str(run.OUT/'plot.py'),'exec'),{'__file__':str(run.OUT/'plot.py')})
table='\n'.join(f"| {r['model']} | {r['track']} | {r['kind']} | {'完成' if r['success'] else '未完成'} | {r['calls']} | {r['manipulations']} | {r['invalidActions']} |" for r in s['rows'])
text=f'''# BrickPlan 最新模型 API 实测

日期：2026-10-14。OpenRouter 实际调用；精确 ID：`openai/gpt-6.1-sol`、`google/gemini-4-argon`。

## 结果

12/12 回合精确完成；两个模型分别完成全部 6 个条件（2 个静态案例 × 文本/视觉，1 个动态案例 × 文本/视觉）。静态包括 3 步层高修复、29 步四处耦合修复。4 个动态回合均从 0 开始，真实触发换色扰动后完成整体搭建；没有使用合法动作 mask。

| 模型 | 输入 | 案例 | 结果 | API轮次 | 拆装尝试 | 无效动作 |
|---|---|---|---|---:|---:|---:|
{table}

## 可比性与边界

预先选择上一轮同一层高、最难复合、动态换色案例，未根据新模型结果挑样本。当前最多4轮、每轮最多8动作、输出含推理最多4096 tokens、reasoning effort=low；旧轮最多8轮、2200 tokens、Gemini关闭推理。因此图是同案例下不同模型配置的实际结果，不是纯模型变量的严格消融。旧结果按原始完整8轮保留；没有重跑或截断来美化差异。仅3个源案例、每条件单次，12/12不能推出全库100%准确率。

视觉输入仍为统一7视图和全零件逐件图；可请求转动/视角/逐件检查，内部遮挡通过对所有件同等开放的检查接口消除。没有错误标记、目标候选标签或oracle轨迹传给模型。

## 核验与费用

真实 API 返回 {s['knownResponseCalls']} 次，新模型费用 ${s['knownResponseCostUSD']:.8f}。连同上一轮，本次授权累计费用上界 ${s['chargedSinceAuthorizationUpperBoundUSD']:.8f} / $2；未结算请求 {s['unsettledCharges']}。

重放验证 {s['audit']['replayedActions']} 个动作、核对 {s['audit']['verifiedImages']} 张实际输入图的 SHA-256；观察、状态、反馈、事件及指标全部一致。`runs/` 保存每轮原始回复、请求观察、图像引用和执行记录，`summary.json` 保存旧版匹配结果。

供应商当日账户用量快照为 $1.332591501，较本项目已归因费用多 $0.027764161；这部分没有对应本轮 generation ID，不能归因给本次模型成绩。即使将其全部保守计入，本轮仍低于 $2。详见 `accounting-final.json`。

## 产物和复现

`report.html` 可逐轮回放；`plots/completion.png`、SVG、PDF 为 Matplotlib 图；`python plot.py` 可离线重绘。`model-catalog.json` 是运行前冻结的 OpenRouter 目录，模型映射不会使用 latest 浮动别名。

来源：[OpenAI GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol)、[OpenRouter Gemini 4 Argon](https://openrouter.ai/google/gemini-4-argon)、[OpenRouter 目录](https://openrouter.ai/api/v1/models)。日期以目录快照为准，账户可用性由本轮真实返回验证。
'''
(run.OUT/'REPORT.zh-CN.md').write_text('> 旧协议已停用，不能作为新版视觉成绩。见 ../brickplan-visual-input-v3/README.zh-CN.md。\n\n'+text)
t=(Path(__file__).parent/'report-template.html').read_text()
t=t.replace('API 实测与动态回放','最新模型实测与动态回放').replace("r.model.includes('gpt')?'GPT mini':'Gemini Flash'","r.model.includes('gpt')?'GPT‑6.1 Sol':'Gemini 4 Argon'")
t=t.replace('每个模型/输入条件共选10例，含1例无错误对照，偏重高难度','每个模型/输入条件预选2例：层高修复和29步复合修复').replace('基线最多8轮；合法动作辅助诊断最多20轮，单独计分','换色扰动，最多4轮，不使用合法动作辅助').replace('试跑总费用上界 · 含预检与中断','本次新模型调用费用 · 总授权仍为 $2')
t=t.replace('<option value="static_cases">静态逐类别结果</option><option value="failures_and_events">无效动作与动态触发</option><option value="bank_profile">题库类型与难度</option>','')
t=t.replace('<h2>如何理解这轮结果</h2>','<h2>12/12 小样本完成</h2><p>新模型低推理档、最多4轮；旧模型最多8轮。图为同案例不同配置对照。<a href="../report.html">上一轮完整报告 ↗</a></p>')
compact={'summary':{k:v for k,v in s.items() if k not in ('rows','sourceHashes')},'runs':viewer}
(run.OUT/'report.html').write_text(t.replace('__DATA__',json.dumps(compact,ensure_ascii=False).replace('</','<\\/')))
print(json.dumps({k:s[k] for k in ['coverage','knownResponseCalls','knownResponseCostUSD','chargedSinceAuthorizationUpperBoundUSD','audit']}))
