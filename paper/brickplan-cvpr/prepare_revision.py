"""Compile current benchmark coverage and unmeasured experiment templates."""
from collections import Counter,defaultdict
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def tex(s):return str(s).replace('_',r'\_').replace('&',r'\&').replace('%',r'\%')

static_path=ROOT/'deliverables/brickplan-static-plate5/cases.jsonl'
static=[json.loads(l) for l in static_path.read_text().splitlines()]
oldindex=read(ROOT/'deliverables/brickplan-static-held4/combined/index.json')
metadata={m['modelId']:m for m in oldindex['models']}
dynpath=ROOT/'deliverables/brickplan-dynamic-v6/cases.private.json';dynamic=read(dynpath)['cases']
commroot=ROOT/'deliverables/brickplan-community-modules';community=read(commroot/'gallery-data.js.json')
sources={str(p.relative_to(ROOT)):sha(p) for p in [static_path,dynpath,commroot/'gallery-data.js.json',ROOT/'deliverables/brickplan-static-held4/combined/index.json']}
rows=[]
for track,cs in [('S',static),('D',dynamic)]:
 groups=defaultdict(list)
 for c in cs:groups[c['modelId']].append(c)
 for i,(mid,rs) in enumerate(sorted(groups.items()),1):
  if track=='S':
   m=metadata[mid];n=m['caseParts'];title=m.get('title',mid);source=mid.split('--')[0];category='source-part configuration';control=sum(not c['oraclePlan'] for c in rs);kinds=Counter(c['category'] for c in rs)
   cert=(ROOT/'deliverables/brickplan-static-held4/combined'/rs[0]['qualificationFile']).resolve()
  else:
   m=rs[0];n=m['targetParts'];title=m.get('objectNameZh',mid);source=m['sourceFamily'];category=m.get('objectCategory','mechanism');control=sum(c['kind']=='none' for c in rs);kinds=Counter(c['kind'] for c in rs)
   cert=ROOT/'deliverables/brickplan-dynamic-v6/models'/mid/'qualification.json'
  sources[str(cert.relative_to(ROOT))]=sha(cert)
  rows.append(dict(track=track,label=f'{track}{i:03}',id=mid,name=title,sourceGroup=source,parts=n,cases=len(rs),controls=control,errorCounts=dict(kinds),category=category,certificate=str(cert.relative_to(ROOT)),example=rs[0].get('publicId',rs[0]['id'])))
for i,m in enumerate(community,1):
 p=commroot/m['id']/'provenance.json';pr=read(p);sources[str(p.relative_to(ROOT))]=sha(p)
 rows.append(dict(track='M',label=f'M{i:03}',id=m['id'],name=m['title'],sourceGroup=m['model'],parts=m['remaining'],sourceParts=m['total'],cases=8,controls=2,errorCounts={'control':2,'missing':2,'wrong-color':2,'extra-layer':2},category='community module',certificate=str((commroot/m['id']/'certificate.private.json').relative_to(ROOT))))
assert len(rows)==240 and sum(r['cases'] for r in rows)==5260
old4=['obj-chair','obj-table','obj-city-car','obj-crane']
oldD=read(ROOT/'deliverables/brickplan-dynamic-v5/index.json');oldids={r['modelId'] for r in oldD['cases']};newids={r['id'] for r in rows if r['track']=='D'}
assert oldids<=newids and len(oldids)==30 and all(x in newids for x in old4)
staticids={r['id'] for r in rows if r['track']=='S'};commids={r['sourceGroup'] for r in rows if r['track']=='M'}
coverage=dict(schema='brickplan-all-track-coverage/1',caseRecords=5260,staticCases=3340,dynamicCases=1920,configurationEntries=240,
              trackCounts={'S':{'configurations':160,'cases':3292},'D':{'structures':68,'completeObjects':42,'mechanismStructures':26,'cases':1872},'M':{'modules':12,'staticCases':48,'dynamicCases':48}},
              continuity={'previousStaticConfigurations':127,'currentStaticConfigurations':160,'previousDynamicStructures':30,'retainedDynamicStructures':len(oldids&newids),'retainedOriginalObjects':old4,'addedDynamicObjectDesigns':38},
              overlaps={'sameIdStaticDynamic':sorted(staticids&newids),'communitySourceAlsoInStatic':sorted(commids&{s.split('--')[0] for s in staticids})},
              countNote='240 is track-specific configuration entries, not 240 independent physical models; older versions are not added again.',models=rows,sources=sources)
dump(HERE/'evidence/benchmark-coverage.json',coverage)
# Full readable list with direct paths into actual benchmark definitions.
md=['# 全部 benchmark 模型与题目清单','', '这次论文覆盖之前的静态配置、动态完整物件和局部结构，以及后来增加的社区模块。12 个社区模块不是整个 bench。','',
'| 部分 | 配置/结构 | 题目 |','|---|---:|---:|','| S：白底板静态 | 160 | 3,292 |','| D：动态（42 个完整物件 + 26 个机制结构） | 68 | 1,872 |','| M：社区模块 | 12 | 96（静态 48 + 动态 48） |','| 合计 | 240 个分轨配置条目，不当成 240 个独立模型 | 5,260 条当前题目记录 |','',
'原来的 127 种静态配置已包含在 160 种里；原来的 30 个动态结构全部保留在 68 个里，包含最初的椅子、桌子、小汽车、吊机。旧版题量不能再累加一次。静态、动态以及社区模块也可能来自同一个原始套装，因此按来源分组比较。','']
for track,title in [('S','静态：全部 160 种配置'),('D','动态：全部 68 种结构'),('M','社区：全部 12 个模块')]:
 md += [f'## {title}','', '| 编号 | 模型/配置 | 名称 | 目标件数 | 题数 | 正常题 | 错误与数量 |','|---|---|---|---:|---:|---:|---|']
 for r in rows:
  if r['track']!=track:continue
  errors='；'.join(f'{k}: {v}' for k,v in sorted(r['errorCounts'].items()))
  md.append(f"| {r['label']} | `{r['id']}` | {r['name']} | {r['parts']} | {r['cases']} | {r['controls']} | {errors} |")
 md.append('')
(HERE/'ALL-MODELS.zh-CN.md').write_text('\n'.join(md).rstrip()+'\n')
# Two compact full-width tables enumerate every static model configuration.
staticrows=[r for r in rows if r['track']=='S'];out=[]
for page in range(2):
 group=staticrows[page*80:(page+1)*80]
 out += [r'\begin{table*}[p]',r'\centering\footnotesize',r'\caption{\textbf{Complete static configuration inventory ('+str(page+1)+r'/2).} P: target parts; Q: current questions. Identifiers refer to the accompanying full model catalogue.}',r'\begin{tabular}{@{}llrr@{\qquad}llrr@{}}',r'\toprule',r'Index & Model/configuration & P & Q & Index & Model/configuration & P & Q\\',r'\midrule']
 for i in range(40):
  cells=[]
  for r in [group[i],group[i+40]]:cells += [r['label'],r'\texttt{'+tex(r['id'])+'}',str(r['parts']),str(r['cases'])]
  out.append(' & '.join(cells)+r'\\')
 out += [r'\bottomrule',r'\end{tabular}',r'\end{table*}']
(HERE/'static-inventory.tex').write_text('\n'.join(out)+'\n')
# Named candidates; all measured cells remain null. No model API is called.
roster_path=HERE/'evidence/model-roster.json'
models=read(roster_path)['models']
diagnostic_ids={'gpt61_sol','gemini4_argon','qwen35_27b'}
diagnostic_models=[m for m in models if m['id'] in diagnostic_ids]
metrics=['static_S_success','static_M_success','dynamic_D_control_success','dynamic_D_trigger_coverage','dynamic_D_recovery','dynamic_M_control_success','dynamic_M_trigger_coverage','dynamic_M_recovery','illegal_attempt_rate','decision_count','latency_seconds','cost_usd']
result=dict(schema='brickplan-planned-results/1',status='NOT_RUN',models=models,seeds=[41,42,43],main=[dict(model=m['id'],**{k:None for k in metrics}) for m in models],human=dict(status='NOT_COLLECTED',**{k:None for k in metrics}),
            ablations=[dict(variant=v,model=m['id'],D_recovery=None,M_recovery=None,illegal_rate=None) for v in ['full','no_previous_view','no_manual_M_only','no_candidate_preview','legality_success_failure_only','symbolic_state_privileged'] for m in diagnostic_models],
            perError=[dict(error=k,**{m['id']:None for m in models},human=None) for k in sorted({c['kind'] for c in dynamic if c['kind']!='none'})],
            difficulty=[dict(partsBin=b,stage=s,temporaryDisassembly=t,recovery=None,n=None) for b in ['4-7','8-10','11-16'] for s in ['early','middle','late'] for t in [False,True]])
result['efficiency']=[dict(track=t,model=m['id'],pairedRecovery=None,pairedDenominator=None,decisions=None,inspections=None,legalMoves=None,rejectedMoves=None,seconds=None,inputTokens=None,outputTokens=None,costUSD=None) for t in ['S','D','M'] for m in models]
result['failureLedger']=[dict(track=t,model=m['id'],serviceFailures=None,invalidOutputs=None,rejectedActions=None,untriggeredFaultJobs=None,wrongFinishOrBudgetEnd=None,controlPassFaultFail=None,wrongAnomalyJudgment=None) for t in ['S','D','M'] for m in models]
result['humanPanel']=[dict(agent=a,staticSuccess=None,D_control=None,D_trigger=None,D_recovery=None,M_control=None,M_trigger=None,M_recovery=None,staticFalseAlarm=None,medianSeconds=None) for a in ['humans']+[m['id'] for m in models]]
result['note']='Uncollected measurements only. Save collected outputs as separate run artifacts; regenerating this template resets null values.'
dump(HERE/'evidence/results-template.json',result)
print(json.dumps({k:v for k,v in coverage.items() if k not in ['models','sources']},ensure_ascii=False,indent=2))

# Preserve both earlier banks explicitly, so continuity is independently checkable.
old_static_path=ROOT/'deliverables/brickplan-repair-library/index.json'
old_s={m['modelId'] for m in read(old_static_path)['models']}
assert len(old_s)==127 and old_s<=staticids
coverage['continuity']['retainedStaticConfigurations']=len(old_s&staticids)
for path in [old_static_path,ROOT/'deliverables/brickplan-dynamic-v5/index.json']:
 sources[str(path.relative_to(ROOT))]=sha(path)
dump(HERE/'evidence/benchmark-coverage.json',coverage)

# Exact planned case IDs and six counterbalanced participant schedules.
import random
splitpath=ROOT/'deliverables/brickplan-static-held4/combined/splits.json'
balpath=ROOT/'deliverables/brickplan-dynamic-v6/balanced-evaluation.json'
original_split=read(splitpath);balanced=read(balpath)['sets']['evaluation']
source_to_split={source:name for name,spec in original_split['splits'].items() for source in spec['sourceModels']}
old_assignments={q:name for name,spec in original_split['splits'].items() for q in spec['publicIds']}
split={'schema':'source-family-split/2-white-baseplate','seed':original_split['seed'],'rule':'Keep source assignment; assign migrated questions by CURRENT model source, not pre-migration public ID.',
       'sourceBankSha256':sha(static_path),'previousSplitSha256':sha(splitpath),'splits':{},'reassignments':[]}
for name,spec in original_split['splits'].items():
 ids=[c['publicId'] for c in static if source_to_split[c['modelId'].split('--')[0]]==name]
 split['splits'][name]={'sourceModels':spec['sourceModels'],'publicIds':ids,'cases':len(ids)}
for c in static:
 current=source_to_split[c['modelId'].split('--')[0]];previous=old_assignments[c['publicId']]
 if current!=previous:split['reassignments'].append({'publicId':c['publicId'],'modelId':c['modelId'],'previous':previous,'current':current})
assert len(split['reassignments'])==151
current_splitpath=ROOT/'deliverables/brickplan-static-plate5/splits.json';dump(current_splitpath,split)
test=split['splits']['test'];ss={c['publicId']:c for c in static};ds={c['id']:c for c in dynamic}
assert len(test['publicIds'])==467 and len(test['sourceModels'])==20
assert all(ss[q]['modelId'].split('--')[0] in test['sourceModels'] for q in test['publicIds'])
for a,b in [('train','dev'),('train','test'),('dev','test')]:
 assert not set(split['splits'][a]['sourceModels'])&set(split['splits'][b]['sourceModels'])
assert len(balanced['interventions'])==168 and len(balanced['controls'])==72
assert set(balanced['interventions']+balanced['controls'])<=ds.keys()
cc=[];designsources={str(path.relative_to(ROOT)):sha(path) for path in [splitpath,current_splitpath,balpath,static_path,dynpath,roster_path]}
for m in community:
 path=commroot/m['id']/'cases.private.json';cc+=read(path);designsources[str(path.relative_to(ROOT))]=sha(path)
cs={c['id']:c for c in cc}
Mstatic=[c['id'] for c in cc if c['mode']=='static'];Mfault=[c['id'] for c in cc if c['mode']=='dynamic' and c['family']!='control'];Mnormal=[c['id'] for c in cc if c['mode']=='dynamic' and c['family']=='control']
assert (len(Mstatic),len(Mfault),len(Mnormal))==(48,36,12)
pairs=[];used=set();controls={c['modelId']:c['publicId'] for c in static if not c['oraclePlan']}
available={kind:sorted([ss[q] for q in test['publicIds'] if ss[q]['category']==kind and ss[q]['oraclePlan']],key=lambda c:hashlib.sha256(c['publicId'].encode()).hexdigest()) for kind in sorted({ss[q]['category'] for q in test['publicIds']})}
while len(used)<12:
 before=len(used)
 for kind,candidates in available.items():
  c=next((c for c in candidates if c['modelId'].split('--')[0] not in used),None)
  if c is None:continue
  source=c['modelId'].split('--')[0]
  pairs.append(dict(pairId=f'HS{len(used)+1:02}',track='S',source=source,fault=c['publicId'],control=controls[c['modelId']],error=c['category']))
  used.add(source)
  if len(used)==12:break
 assert len(used)>before,'Cannot fill twelve independent static source pairs'

used=set()
for kind in sorted({ds[q]['kind'] for q in balanced['interventions']}):
 candidates=[ds[q] for q in balanced['interventions'] if ds[q]['kind']==kind]
 c=min(candidates,key=lambda c:(c['modelId'] in used,not c['modelId'].startswith('obj-'),hashlib.sha256(c['id'].encode()).hexdigest()))
 normal=next(d['id'] for d in dynamic if d['pairedGroup']==c['pairedGroup'] and d['kind']=='none')
 pairs.append(dict(pairId=f'HD{len(pairs)-11:02}',track='D',source=c['sourceFamily'],fault=c['id'],control=normal,error=kind))
 used.add(c['modelId'])
for i,m in enumerate(community):
 fault=next(c for c in cc if c['module']==m['id'] and c['mode']=='dynamic' and c['family']==['missing','wrong-color','extra-layer'][i%3])
 normal=next(c['id'] for c in cc if c['module']==m['id'] and c['mode']=='dynamic' and c['family']=='control')
 pairs.append(dict(pairId=f'HM{i+1:02}',track='M',source=m['model'],fault=fault['id'],control=normal,error=fault['family']))
assert len(pairs)==36
schedules=[];appear=Counter()
for h in range(6):
 schedule=[]
 for i,pair in enumerate(pairs):
  condition='fault' if (h+i)%6<3 else 'control'
  entry=dict(pairId=pair['pairId'],track=pair['track'],condition=condition,caseId=pair[condition]);schedule.append(entry);appear[(pair['pairId'],condition)]+=1
 random.Random(20261021+h).shuffle(schedule)
 schedules.append(dict(participant=f'H{h+1}',conditions=schedule))
assert set(appear.values())=={3} and len(appear)==72
for schedule in schedules:
 assert len(schedule['conditions'])==36 and len({e['pairId'] for e in schedule['conditions']})==36
 assert sum(e['condition']=='fault' for e in schedule['conditions'])==18
manifest=dict(schema='brickplan-experiment-design/1',status='PLANNED_NOT_EXECUTED',models=models,seeds=[41,42,43],
 primary={'S':{'caseIds':test['publicIds'],'sourceGroups':test['sourceModels'],'visualAdmission':'PENDING'},'D':{'faultIds':balanced['interventions'],'normalIds':balanced['controls'],'pairing':'clone environment and visible conversation at admissible prefix; separate control continuation per fault'},'M':{'staticIds':Mstatic,'faultIds':Mfault,'normalIds':Mnormal,'scope':'Public development panel, not unseen-source evaluation'}},
 workUnits=dict(staticAttempts=(467+48)*len(models)*3,dynamicJobs=(168+72+36+12)*len(models)*3,faultJobsWithTwoContinuations=(168+36)*len(models)*3,total=(467+48+168+72+36+12)*len(models)*3,apiCalls=None,additionalWork=['human common panel','ablations','perception probe','cross-model recovery','strategy and visual robustness','full-bank coverage','visual admission']),
 human=dict(independentParticipants=6,pairs=pairs,conditions=72,completions=216,repeatsPerCondition=3,schedules=schedules,interface='Buttons and graphical actions; no written answer or JSON required',comparison='Between-participant conditions, not matched-history human trajectories'),
 decisionBudget='max(40, 6*N+20) per track; M additionally 4*N+12 manipulation attempts',
 transportRetries=2,sourceBootstrapReplicates=2000,capNote='No paid calls are authorized by this planning artifact alone; execution remains a later task.',sources=designsources)
dump(HERE/'evidence/experiment-design.json',manifest)

# Add diagnostic designs and generate publication tables from the same roster.
import subprocess,sys
subprocess.run([sys.executable,str(HERE/"expand_experiments.py")],check=True)
