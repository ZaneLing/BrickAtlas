"""Keep earlier complete designed objects, without multiplying source modules."""
from collections import defaultdict
import json
from scaling_release import ROOT,OUT
from expansion_v7.build import read,write


def collect():
 rows=[json.loads(s) for s in (ROOT/'deliverables/brickplan-benchmark-spec/questions.jsonl').read_text().splitlines()]
 groups=defaultdict(list)
 for r in rows:
  if r.get('source','').startswith('procedural-family:') and not r.get('isAlias') and r.get('track') in ('whole-object-dynamic','whole-object-static'):groups[r['model']].append(r)
 models=[];questions=[]
 for mid,rs in sorted(groups.items()):
  normal=next((r for r in rs if r['taskType']=='D0'),None)
  if normal is None:continue
  selected=[normal];families=set()
  for r in rs:
   if r['mode']=='dynamic' and r['taskType']=='D1' and r['family'] not in families:
    selected.append(r);families.add(r['family'])
   if len(families)==5:break
  multi=next((r for r in rs if r['taskType']=='D2'),None)
  static=next((r for r in rs if r['mode']=='static' and r.get('family')=='buried-repair'),None)
  if multi:selected.append(multi)
  if static:selected.append(static)
  n=normal['activeParts'];level='short' if n<=7 else 'medium' if n<=15 else 'long'
  m=dict(id=mid,setNumber=mid,title=normal['title'],sourceModelName=None,sourceGroup=normal['source'],sourceUrl=None,category=normal['source'].split(':')[-1],sourceParts=n,activeParts=n,scope=dict(kind='complete-object',description='既有完整物件，从白色凸点底板开始'),difficulty=level,difficultyBasis='active parts only; human difficulty not calibrated',split='development',authoringExposed=True,humanValidated=False,modelEvaluated=False,status='legacy-machine-checked',dynamicCases=sum(r['mode']=='dynamic' for r in selected),staticCases=sum(r['mode']=='static' for r in selected),figures='designed from ordinary bricks; no minifigure inventory',preview=f'legacy/previews/{mid}/overview.png',legacy=True)
  models.append(m)
  for r in selected:
   questions.append(dict(id=r['id'],model=mid,setNumber=mid,title=m['title'],mode=r['mode'],track=r['track'],taskType=r['taskType'],family=r['family'],familyZh=r['errorName'],sourceGroup=r['source'],split='development',authoringExposed=True,activeParts=n,difficulty=level,referenceMoves=r.get('referenceRepairMoves'),scheduledEvents=0 if r['taskType'] in ('D0','S0','S1') else int(r['eventLevel'][1:]) if r.get('eventLevel','').startswith('T') else 1,machineChecked=True,humanValidated=False,modelEvaluated=False,gtFile='existing private source bank via bench_design.run_episode.load',runtime='dynamic_arena.run' if r['mode']=='dynamic' else 'bench_design.run_episode',inputPolicy='tool-arena-pull-observation' if r['mode']=='dynamic' else 'matched-current-target-views',outputPolicy='one structured action per decision; finish explicitly',finalAcceptance='physical final-state equality and legal actions; no GT order matching',legacy=True))
 for q in questions:
  if q['family']=='none':q['family']='control'
  path=OUT/'legacy/checks'/f'{q["model"]}.json'
  if path.exists():
   verified=next((r for r in read(path)['questions'] if r['id']==q['id']),None)
   if verified:q.update(referenceMoves=verified['moves'],scheduledEvents=verified['eventsApplied'])
 category_map={**{k:'furniture-object' for k in ['beds','seating','storage','tables','screens','appliances','instruments','lighting','signals','water-features']},**{k:'house-building' for k in ['spans','towers','buildings','stairs']},**{k:'robot-machine' for k in ['lifting-machines','counter-machines','frame-machines','humanoid','utility-vehicles']},'road-vehicles':'road-vehicle','rail-vehicles':'railway','watercraft':'boat'}
 for m in models:m['category']=category_map.get(m['category'],m['category'])
 write(OUT/'legacy/index.json',dict(models=models,questions=questions,policy='Up to seven dynamic and one static representative per existing complete designed object; all historical cases remain in their original banks. No cropped diagnostics counted as new objects.'))
 return models,questions

if __name__=='__main__':
 m,q=collect();print(len(m),'legacy complete objects',len(q),'selected questions')
