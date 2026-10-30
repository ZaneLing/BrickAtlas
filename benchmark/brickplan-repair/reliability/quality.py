"""Current-release review sampling and an independent Boolean geometry audit."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import argparse,json,hashlib
from reliability import ROOT,OUT
from expansion_v7.build import read,write
from bench_design.session import Session,internal_action

DATA=ROOT/'deliverables/brick-atlas-dataset-v1'

def select():
 rows=[json.loads(l) for mode in ('static','dynamic') for l in (DATA/'questions'/f'{mode}.jsonl').read_text().splitlines()]
 chosen=[];used=set()
 # Each length stratum contains distinct error families and distinct objects.
 for difficulty in ('short','medium','long'):
  for family in ('wrong-color','missing','buried-repair','rotated'):
   candidates=[r for r in rows if r['mode']=='static' and r['difficulty']==difficulty and r['family']==family and r['model'] not in used and r['id'].startswith('SC:')]
   if not candidates:continue
   r=min(candidates,key=lambda r:(r['activeParts'],r['id']));used.add(r['model']);chosen.append(r)
 # Continuous recovery is separately reviewable, never disguised as a static task.
 for family in ('D2','missing'):
  candidate=next((r for r in sorted(rows,key=lambda r:(r['activeParts'],r['id'])) if r['mode']=='dynamic' and (r['taskType']=='D2' if family=='D2' else r['family']==family) and r['id'].startswith('SC:') and r['model'] not in used),None)
  if candidate:chosen.append(candidate);used.add(candidate['model'])
 return [dict(code=f'R{i+1:03}',**r) for i,r in enumerate(chosen)]

def build():
 from dynamic_arena.tool_arena import PROTOCOL
 rows=select();sources={}
 for row in rows:
  folder=DATA/'private'/row['id'].split(':')[1]
  for path in sorted(folder.glob('*.private.json.gz')):sources[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
 for name in ('reliability/review.py','reliability/review.html','dynamic_arena/tool_arena.py','dynamic_arena/sensors.py'):
  path=ROOT/'benchmark/brickplan-repair'/name;sources[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
 version=hashlib.sha256(json.dumps(dict(tasks=rows,protocol=PROTOCOL,sources=sources),sort_keys=True).encode()).hexdigest()
 write(OUT/'review/tasks.private.json',dict(version=version,tasks=rows,sourceHashes=sources,apiCalls=0,humanResponses=0,
     scope='Stratified targeted quality sample, not a random error-rate estimator',
     independentRoles=['gt-answer-check','blind-operation','physical-action-check']))
 return rows

def geometry(rows):
 from bench_design.independent_geometry import check,calibrate
 probes=[]
 # New current-release cases, balanced accepted and rejected geometry; labels
 # stay evaluator-side. This uses different Boolean code, shared source meshes.
 for row in rows[:6]:
  s=Session.open(row['id'],OUT/'review/cache'/row['code'],'scripted:independent-check');s.autosave=False
  rt=s.ep.runtime;state=deepcopy(s.ep.state);picked=[]
  for action in s.ep.case['referenceActions'][:2]:
   _,fb=rt.check(state,action['actor'],action['type'],candidate=action.get('candidate'))
   if fb['code']=='OK':picked.append((deepcopy(state),deepcopy(action),fb))
   state,_=rt.check(state,action['actor'],action['type'],candidate=action.get('candidate'))
  for actor,key in s.initial.items():
   if not key:continue
   _,fb=rt.check(s.initial,actor,'detach')
   if fb['code']=='PATH_BLOCKED':picked.append((deepcopy(s.initial),dict(type='detach',actor=actor),fb));break
  for st,action,fb in picked:
   verdict=check(rt,st,action,fb)
   proposed=dict(st);proposed[action['actor']]=action.get('candidate','')
   probes.append(dict(code=f'P{len(probes)+1:03}',caseId=row['id'],reviewCode=row['code'],
       state=st,action=action,proposed=proposed,engineResult=fb,independent=verdict))
   print(row['code'],fb['code'],verdict['status'],flush=True)
 result=dict(apiCalls=0,calibration=calibrate(),cases=len({p['caseId'] for p in probes}),probes=probes,
     counts=dict(Counter(p['independent']['status'] for p in probes)),humanChecked=False,
     sharedMeshInputs=True,realPhysicsQualified=False,currentReleaseCases=True,
     scope='Independent endpoint and continuous straight sweep, not independent mesh truth or connector semantics')
 write(OUT/'review/geometry.private.json',result)
 return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--geometry',action='store_true');args=p.parse_args();rows=build()
 print('Prepared',len(rows),'current tasks in',len({r['model'] for r in rows}),'objects',flush=True)
 if args.geometry:print(json.dumps(geometry(rows)['counts']))

if __name__=='__main__':main()
