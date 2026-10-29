"""Reproducible research indexes; admission counts exclude every withheld source."""
from collections import Counter
from pathlib import Path
import hashlib,json
from scaling_release import ROOT,OUT
from expansion_v7.build import read,write

NAMES={'control':'正常、无错误','missing':'少装／零件被拆走','wrong-color':'颜色错误','wrong-part':'用错零件','offset':'位置偏移','rotated':'方向错误','extra-layer':'多装一层','early-cover':'提前封口','buried-repair':'拆上层返修','left-right-swap':'左右装反','repeat-omission':'重复结构漏装','repeated-step':'步骤重复'}
ALIASES={'none':'control','removed_piece':'missing','wrong_color':'wrong-color','shifted_piece':'offset','rotated_piece':'rotated','wrong_part':'wrong-part','extra_layer':'extra-layer','early_cover':'early-cover','buried_wrong_color':'buried-repair','compound_fault':'compound'}
NAMES.update(multiple='连续多次干扰',compound='同次事件含多个错误')
ALIASES.update(wrong_size='wrong-part',swapped_positions='swapped-positions')
NAMES['swapped-positions']='两个零件的位置装反'

def family_name(value):
 return 'multiple' if value.startswith('multiple-') else ALIASES.get(value,value)

def scope_text(scope):
 kind=scope['kind']
 if kind=='complete-object':return '从白色凸点底板开始，拼好整个物件'
 if kind=='upper-finishing-stage':return '补完物件上方标出的收尾部分；下方主体已完成'
 if kind=='side-finishing-stage':return '补完物件侧面或端部标出的收尾部分；其余主体已完成'
 if kind=='instruction-finishing-stage':return '完成原说明的最后几步；操作范围在全景中标出'
 name=scope.get('description','').split('（')[0]
 return '完成图中标出的整个部分；其余主体已完成' if '子组件' in name or len(name)>35 else '完成图中标出的'+name+'；其余主体已完成'

def display_title(source):
 import re
 from dynamic_arena.curate_sources import RULES
 caption=source.get('sourceModelName') or ''
 if caption.lower() not in ('','main model','alternate model') and any(re.search(p,caption,re.I) for _,p in RULES):return caption
 return source['title']

def jsonl(path,rows):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(''.join(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n' for r in rows))

def main():
 from dynamic_arena.curate_sources import category
 from scaling_release.check import verified
 pool=read(OUT/'source-pool.json');models=[];questions=[];sources=[];designs=[];answers={}
 for source in sorted(pool['models'],key=lambda r:tuple(int(x) if x.isdigit() else x for x in r['setNumber'].split('-'))):
  number=source['setNumber'];folder=OUT/'private'/number;path=folder/'cases.private.json.gz'
  s=dict(source);s['sourceGroup']='set:'+number.split('-')[0];s['officialAlternate']=bool(source.get('officialAlternate'));s['objectCategory']=category(source)
  if not path.exists():
   status=read(folder/'status.json') if (folder/'status.json').exists() else dict(status='not-yet-checked',reason='Pending qualification')
   s.update(status=status['status'],reason=status.get('reason'),dynamicCases=0,staticCases=0)
   sources.append(s);continue
  if not verified(folder):
   status=read(folder/'check.json') if (folder/'check.json').exists() else {}
   s.update(status='awaiting-final-check' if status.get('passed',True) else 'withheld-final-check',reason=status.get('error') or 'Final source and replay audit required for current files',dynamicCases=0,staticCases=0)
   sources.append(s);continue
  meta=read(folder/'metadata.json');cases=read(path);cert=read(folder/'certificate.private.json.gz');n=meta['activeParts'];difficulty='short' if n<=7 else 'medium' if n<=15 else 'long'
  split=['development','validation','test'][0 if int(hashlib.sha256(s['sourceGroup'].encode()).hexdigest()[:8],16)%10<6 else 1 if int(hashlib.sha256(s['sourceGroup'].encode()).hexdigest()[:8],16)%10<8 else 2]
  # These source hashes define a reproducible grouping, not an unseen-model claim:
  # all sets touched during authoring remain marked authoringExposed.
  m=dict(id=meta['id'],setNumber=number,title=display_title(source),sourceSetTitle=source['title'],sourceModelName=meta.get('sourceModelName'),sourceGroup=s['sourceGroup'],sourceUrl=source['sourceUrl'],category=s['objectCategory'],sourceParts=meta['sourceParts'],activeParts=n,scope=meta['scope'],difficulty=difficulty,difficultyBasis='active parts only; human difficulty not calibrated',split=split,authoringExposed=True,humanValidated=False,modelEvaluated=False,status='machine-checked',dynamicCases=sum(c['mode']=='dynamic' for c in cases),staticCases=sum(c['mode']=='static' for c in cases),figures='no-figure-parts-found',preview=f'previews/{number}/overview.png')
  models.append(m);s.update(status='machine-checked',dynamicCases=m['dynamicCases'],staticCases=m['staticCases']);sources.append(s)
  for c in cases:
   family=c['family'];task='S0' if c['mode']=='static' and family=='control' else 'S1' if c['mode']=='static' else 'D0' if not c['events'] else 'D2' if len(c['events'])>1 else 'D1'
   q=dict(id=c['id'],model=m['id'],setNumber=number,title=m['title'],mode=c['mode'],track=('whole-object' if m['scope']['kind']=='complete-object' else 'finishing-stage')+'-'+c['mode'],taskType=task,family=family,familyZh=NAMES.get(family,'连续两次干扰'),humanErrorIds=c['humanErrorIds'],sourceGroup=s['sourceGroup'],split=split,authoringExposed=True,activeParts=n,difficulty=difficulty,referenceMoves=len(c['referenceActions']),scheduledEvents=len(c['events']),machineChecked=True,humanValidated=False,modelEvaluated=False,physicalTaskSha256=c['physicalTaskSha256'],gtFile=f'private/{number}/cases.private.json.gz',runtime='dynamic_arena.run' if c['mode']=='dynamic' else 'bench_design.run_episode',inputPolicy='tool-arena-pull-observation' if c['mode']=='dynamic' else 'matched-current-target-views-and-optional-instructions',outputPolicy='one structured observation or physical action per decision; finish explicitly',finalAcceptance='physical final-state equality and legal actions; no GT order matching')
   questions.append(q)
   answers[c['id']]=dict(referenceActions=c['referenceActions'],events=[dict(family=e['family'],changes=e['changes'],recovery=e['recovery']) for e in c.get('referenceEvents',[])],parts={r['actor']:dict(name=r['part']['name'],sourceIndex=r['part'].get('sourceIndex'),partNumber=r['part']['partNumber']) for r in cert['candidates'].values() if r['kind']=='goal'},legalWitnessOnly=True,globallyShortest=False)
  designs.append(read(OUT/'designs'/f'{number}.json'))
 community_count=len(models)
 from scaling_release.legacy import collect
 legacy_models,legacy_questions=collect();models+=legacy_models;questions+=legacy_questions
 for m in models:m['scopeDescriptionZh']=scope_text(m['scope'])
 for q in questions:
  q['assetFamily']=q['family'];q['nativeFamily']=q['family'];q['family']=family_name(q['family']);q['familyZh']=NAMES.get(q['family'],q['familyZh'])
  from scaling_release.static_bank import asset_key
  if q.get('legacy'):
   field='imageBase' if q['mode']=='static' else 'eventImageBase'
   q[field]=f'legacy/previews/{q["model"]}/cases/{asset_key(q["id"])}/'
  elif q['mode']=='static':q['imageBase']=f'previews/{q["setNumber"]}/static/{asset_key(q["id"])}/'
 for m in legacy_models:
  p=OUT/'legacy/checks'/f'{m["id"]}.json'
  if p.exists():
   for r in read(p)['questions']:answers[r['id']]=dict(referenceActions=r.get('referenceActions',[]),aliasSeed=41,legalWitnessOnly=True,globallyShortest=False)
 jsonl(OUT/'models.jsonl',models);jsonl(OUT/'sources.jsonl',sources)
 for mode in ['dynamic','static']:jsonl(OUT/'questions'/f'{mode}.jsonl',[q for q in questions if q['mode']==mode])
 counts=dict(sourceModels=len(sources),distinctSourceSets=len({s['sourceGroup'] for s in sources}),officialAlternates=sum(s['officialAlternate'] for s in sources),qualifiedCommunityModels=community_count,retainedDesignedModels=len(legacy_models),runnableModels=len(models),withheldOrPendingModels=len(sources)-community_count,dynamicQuestions=sum(q['mode']=='dynamic' for q in questions),staticQuestions=sum(q['mode']=='static' for q in questions),wholeObjectModels=sum(m['scope']['kind']=='complete-object' for m in models),finishingStageModels=sum(m['scope']['kind']!='complete-object' for m in models),byDifficulty=dict(Counter(m['difficulty'] for m in models)),byCategory=dict(Counter(m['category'] for m in models)),byError=dict(Counter(q['family'] for q in questions)))
 release=dict(schema='brick-atlas-dataset/1',status='machine-checked-human-review-pending',counts=counts,apiCalls=0,modelApiCostUSD=0,humanValidated=False,independentPhysicsValidated=False,minimum300RunnableModelsMet=len(models)>=300,sourceCountIsNotRunnableCount=True,legacyCatalogue='deliverables/brickplan-dynamic-arena/catalogue.json',legacyPolicy='Earlier tasks retained through Arena, not silently recounted as new OMR models.',splitCaveat='Source groups separated, but all sources used during authoring; this is NOT a fresh unseen test set.')
 write(OUT/'release.json',release);write(OUT/'gallery-data.json',dict(release=release,models=models,questions=questions,sources=sources,designs=designs))
 (OUT/'gallery-data.js').write_text('window.DATASET='+json.dumps(dict(release=release,models=models,questions=questions),ensure_ascii=False)+';\n')
 (OUT/'review-gt.private.js').write_text('window.REVIEW_GT='+json.dumps(answers,ensure_ascii=False)+';\n')
 lines=['# 完整模型和题目清单','',f"社区来源 {counts['sourceModels']} 个，其中 {community_count} 个通过检查、{counts['withheldOrPendingModels']} 个暂不采用；另保留并复查 {len(legacy_models)} 个已有完整物件。正式题库共 {len(models)} 个模型。",'', '**这里的「通过」是程序检查，不代表真人已确认，也不代表 API 模型做对。**','', '| 模型 | 范围／操作件数 | 难度（按长度） | 动态／静态题 | 错误类别 | 图 |','|---|---|---|---|---|---|']
 for m in models:
  qs=[q for q in questions if q['model']==m['id']];families='、'.join(dict.fromkeys(q['familyZh'] for q in qs))
  lines.append(f"| {m['setNumber']} · {m['title'].replace('|','/')} | {m['scopeDescriptionZh'].replace('|','/')}；{m['activeParts']} 件 | {m['difficulty']} | {m['dynamicCases']} / {m['staticCases']} | {families} | [全景与局部]({m['preview']}) |")
 lines+=['','## 未进入可运行题库的模型','','这些模型保留原文件和失败记录，不伪造 GT，不计入成功率分母。','','| 模型 | 原因 |','|---|---|']
 for s in sources:
  if s['status']!='machine-checked':lines.append(f"| {s['setNumber']} · {s['title'].replace('|','/')} | {s.get('reason','').replace('|','/')} |")
 (OUT/'MODEL-AND-QUESTION-LIST.zh-CN.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps(counts,ensure_ascii=False))

if __name__=='__main__':main()
