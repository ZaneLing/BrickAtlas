"""Recheck retained complete objects through the shared session adapter."""
from concurrent.futures import ProcessPoolExecutor,as_completed
import argparse,hashlib,json
from scaling_release import OUT,ROOT
from scaling_release.legacy import collect
from scaling_release.static_bank import asset_key
from expansion_v7.build import read,write

def one(model,questions,force=False):
 from bench_design.session import Session
 from dynamic_arena.validate_replays import Witness
 from dynamic_arena.sensors import Sensors
 folder=OUT/'legacy/runtime'/model['id'];dest=OUT/'legacy/previews'/model['id'];dest.mkdir(parents=True,exist_ok=True)
 check=OUT/'legacy/checks'/f'{model["id"]}.json';old=read(check) if check.exists() else {};cache={r['id']:r for r in old.get('questions',[])}
 code_hash=hashlib.sha256(b''.join(p.read_bytes() for p in sorted((ROOT/'benchmark/brickplan-repair').rglob('*.py')))).hexdigest()
 records=[];failures=[];static_written=False
 for q in questions:
  case_dest=dest/'cases'/asset_key(q['id']);case_dest.mkdir(parents=True,exist_ok=True)
  existing=cache.get(q['id']);expected=[]
  if q['mode']=='static':expected=[case_dest/f'{role}-{view}.png' for role in ('static-current','static-target') for view in ('isometric','rear','top')]
  elif q['taskType']!='D0' and existing:expected=[case_dest/f'{q["family"]}-event-{i+1}-{role}.png' for i in range(existing['eventsApplied']) for role in ('before','after')]
  else:expected=[dest/f'{role}-{view}.png' for role in ('initial','target') for view in ('isometric','rear','top')]
  try:
   s=Session.open(q['id'],folder,'scripted:dataset-check',control=q['taskType']=='D0');s.autosave=False;sensors=Sensors(s)
   fingerprint=hashlib.sha256((code_hash+json.dumps([s.ep.case,s.ep.runtime.cert],sort_keys=True,default=str)).encode()).hexdigest()
   if existing and not force and existing.get('fingerprint')==fingerprint and all(p.exists() for p in expected):
    records.append(existing);continue
   if q['taskType']=='D0':
    sensors.render(s.goal,focus='whole').save(dest/'overview.png')
    for role,state in [('initial',s.initial),('target',s.goal)]:
     for view in ('isometric','rear','top'):sensors.render(state,view).save(dest/f'{role}-{view}.png')
   witness=Witness(s)
   for _ in range(2*s.cap+4):
    a=json.loads(witness({}))
    if a['tool']=='observe':continue
    s.submit(dict(type=a['tool'],**a['args']))
    if s.done:break
   result=s.result();assert result['success'],(result['terminalStatus'],result['stateMetrics'])
   if q['mode']=='dynamic' and q['taskType']!='D0':
    assert result['appliedEvents']==result['scheduledEvents']>0,'Reference did not trigger every scheduled event'
    assert result['effectiveIncidentVerified'],'Reference incident had no verified effective change'
   if q['mode']=='static':
    for role,state in [('static-current',s.initial),('static-target',s.goal)]:
     for view in ('isometric','rear','top'):
      im=sensors.render(state,view);im.save(case_dest/f'{role}-{view}.png')
      if not static_written:im.save(dest/f'{role}-{view}.png')
    static_written=True
    visible=any((case_dest/f'static-current-{v}.png').read_bytes()!=(case_dest/f'static-target-{v}.png').read_bytes() for v in ('isometric','rear','top'))
    assert q['taskType']=='S0' or visible,'Static defect invisible in all three default exported views; human visibility qualification required'
   for i,e in enumerate(s.events):
    for role in ('before','after'):sensors.render(e[role]).save(case_dest/f'{q["family"]}-event-{i+1}-{role}.png')
   records.append(dict(id=q['id'],success=True,fingerprint=fingerprint,effectiveIncidentVerified=result['effectiveIncidentVerified'],staticVisible=visible if q['mode']=='static' else None,eventsApplied=result['appliedEvents'],moves=sum(r['action']['type'] in ('attach','detach') for r in s.records),referenceActions=[r['action'] for r in s.records],aliasSeed=41,apiCalls=0))
  except Exception as e:
   failures.append(dict(id=q['id'],model=model['id'],reason=str(e),status='withheld-reference-check',notModelFailure=True));print('WITHHELD',q['id'],str(e)[:130],flush=True)
  write(check,dict(passed=not failures,publishedSubsetPassed=bool(records),model=model['id'],questions=records,withheld=failures,notModelPerformance=True))
 write(check,dict(passed=not failures,publishedSubsetPassed=bool(records),model=model['id'],questions=records,withheld=failures,notModelPerformance=True))
 return model['id'],records,failures

def main():
 p=argparse.ArgumentParser();p.add_argument('--force',action='store_true');p.add_argument('--workers',type=int,default=3);a=p.parse_args()
 models,questions=collect(include_unchecked=True);results=[];failures=[]
 with ProcessPoolExecutor(max_workers=a.workers) as ex:
  fs={ex.submit(one,m,[q for q in questions if q['model']==m['id']],a.force):m['id'] for m in models}
  for f in as_completed(fs):
   try:mid,rs,rejected=f.result();results.extend(rs);failures.extend(rejected);print('LEGACY CHECKED',mid,len(rs),'withheld',len(rejected),flush=True)
   except Exception as e:failures.append(dict(model=fs[f],reason=str(e)));print('LEGACY FAIL',fs[f],str(e),flush=True)
 write(OUT/'checks/legacy-replay.json',dict(passed=not failures,publishedSubsetPassed=all(r['success'] for r in results),questions=results,failures=failures,apiCalls=0))

if __name__=='__main__':main()
