"""Recheck retained complete objects through the shared session adapter."""
from concurrent.futures import ProcessPoolExecutor,as_completed
import json
from scaling_release import OUT
from scaling_release.legacy import collect
from expansion_v7.build import read,write

def one(model,questions):
 from bench_design.session import Session
 from dynamic_arena.validate_replays import Witness
 from dynamic_arena.sensors import Sensors
 folder=OUT/'legacy/runtime'/model['id'];dest=OUT/'legacy/previews'/model['id'];dest.mkdir(parents=True,exist_ok=True);records=[]
 for q in questions:
  s=Session.open(q['id'],folder,'scripted:dataset-check',control=q['taskType']=='D0');s.autosave=False;sensors=Sensors(s)
  if q['taskType']=='D0':
   sensors.render(s.goal,focus='whole').save(dest/'overview.png')
   for role,state in [('initial',s.initial),('target',s.goal)]:
    for view in ('isometric','rear','top'):sensors.render(state,view).save(dest/f'{role}-{view}.png')
  if q['mode']=='static':
   for role,state in [('static-current',s.initial),('static-target',s.goal)]:
    for view in ('isometric','rear','top'):sensors.render(state,view).save(dest/f'{role}-{view}.png')
  witness=Witness(s)
  for _ in range(2*s.cap+4):
   a=json.loads(witness({}))
   if a['tool']=='observe':continue
   s.submit(dict(type=a['tool'],**a['args']))
   if s.done:break
  result=s.result();assert result['success'],(q['id'],result['terminalStatus'],result['stateMetrics'])
  if q['mode']=='dynamic' and q['taskType']!='D0':assert result['appliedEvents']>0,(q['id'],'Untriggered legacy reference')
  for i,e in enumerate(s.events):
   for role in ('before','after'):sensors.render(e[role]).save(dest/f'{q["family"]}-event-{i+1}-{role}.png')
  records.append(dict(id=q['id'],success=True,eventsApplied=result['appliedEvents'],moves=sum(r['action']['type'] in ('attach','detach') for r in s.records),referenceActions=[r['action'] for r in s.records],aliasSeed=41,apiCalls=0))
 write(OUT/'legacy/checks'/f'{model["id"]}.json',dict(passed=True,model=model['id'],questions=records,notModelPerformance=True));return model['id'],records

def main():
 models,questions=collect();results=[];failures=[]
 with ProcessPoolExecutor(max_workers=3) as ex:
  fs={ex.submit(one,m,[q for q in questions if q['model']==m['id']]):m['id'] for m in models}
  for f in as_completed(fs):
   try:mid,rs=f.result();results.extend(rs);print('LEGACY PASS',mid,len(rs),flush=True)
   except Exception as e:failures.append(dict(model=fs[f],reason=str(e)));print('LEGACY FAIL',fs[f],str(e),flush=True)
 write(OUT/'checks/legacy-replay.json',dict(passed=not failures,questions=results,failures=failures,apiCalls=0))

if __name__=='__main__':main()
