"""Current release -> paper evidence and exact publication scene exports.

Run after the release audit. No API calls and no edits to task/model inputs.
"""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,hashlib,json,sys,re
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];DATA=ROOT/'deliverables/brick-atlas-dataset-v1'
sys.path.insert(0,str(ROOT/'benchmark/brickplan-repair'))
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lines(p):return [json.loads(x) for x in p.read_text().splitlines()]
def write(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def snapshot():
 models=lines(DATA/'models.jsonl');questions=sum([lines(DATA/'questions'/f'{m}.jsonl') for m in ['static','dynamic']],[])
 files=[DATA/n for n in ['release.json','models.jsonl','questions/static.jsonl','questions/dynamic.jsonl','checks/release-check.json','checks/full-replay.json','checks/legacy-replay.json','checks/arena-replays.json']]
 paths=['benchmark/brickplan-repair/dynamic_arena/tool_arena.py','benchmark/brickplan-repair/dynamic_arena/sensors.py','benchmark/brickplan-repair/bench_design/metrics.py','benchmark/brickplan-repair/scaling_release/arena_metrics.py']
 files += [ROOT/n for n in paths]
 stats=dict(schema='brick-atlas-paper-release/1',date='2026-10-29',release=read(DATA/'release.json'),questions=len(questions),models=len(models),taskTypes=dict(Counter(q['taskType'] for q in questions)),sourceGroups=len({m['sourceGroup'] for m in models}),modelsBySplit=dict(Counter(m['split'] for m in models)),questionsBySplit=dict(Counter(q['split'] for q in questions)),allAuthoringExposed=all(m['authoringExposed'] for m in models),byTrack=dict(Counter(q['track'] for q in questions)),byLength={d:dict(models=sum(m['difficulty']==d for m in models),static=sum(q['difficulty']==d and q['mode']=='static' for q in questions),dynamic=sum(q['difficulty']==d and q['mode']=='dynamic' for q in questions)) for d in ['short','medium','long']},byFamily={f:dict(static=sum(q['family']==f and q['mode']=='static' for q in questions),dynamic=sum(q['family']==f and q['mode']=='dynamic' for q in questions)) for f in sorted({q['family'] for q in questions})},files={str(p.relative_to(ROOT)):sha(p) for p in files},formalModelStudyComplete=False,humanQualificationComplete=False,apiCalls=0)
 write(HERE/'evidence/release-dataset.json',stats);return models,questions,stats

def scenes(models,questions):
 from bench_design.session import Session
 from dynamic_arena.sensors import Sensors
 from publication_plate import add_plate
 from render import PALETTE
 PALETTE.update(dict(re.findall(r'CODE\s+(\d+)\s+VALUE\s+(#[0-9A-Fa-f]{6})',(ROOT/'assets-source/ldraw-library/locked/LDConfig.ldr').read_text())))
 cache=HERE/'build/release-scenes';cache.mkdir(parents=True,exist_ok=True);specs=[];engines={};sources={};selection={}
 def session(q):
  s=Session.open(q['id'],HERE/'build/scene-sessions'/hashlib.sha256(q['id'].encode()).hexdigest()[:12],'scripted:paper-geometry',control=q['taskType']=='D0');s.autosave=False
  ren=Sensors(s).renderer;add_plate(ren);engines[q['id']]=(s,ren);return s
 def add(q,s,name,state,group,focus=False):
  specs.append(dict(name=name,caseId=q['id'],model=q['model'],state=dict(state),group=group,frameKeys=['_module_frame'] if focus and '_module_frame' in engines[q['id']][1].bounds else None))
 # Compact eight-object strip: all IDs must occur in this release.
 objects=[('sc-2132-1','Cow'),('sc-7223-1-alt-831','Truck top'),('sc-4018-1','Ship'),('sc-4037-1','Helicopter'),('obj-chair','Chair'),('v7-long-bookshelf','Bookshelf'),('sc-561412-1','Tree top'),('sc-21035-1','Building top')]
 selection['objects']=[]
 for mid,label in objects:
  q=next(q for q in questions if q['model']==mid and q['taskType']=='D0');s=session(q);name='object-'+mid;add(q,s,name,s.goal,name);selection['objects'].append(dict(name=name,label=label,model=mid,caseId=q['id']))
 # Eight static pairs, with stage-specific target, one selected per family.
 selection['errors']=[]
 for family,label in [('missing','Missing'),('wrong-color','Wrong color'),('wrong-part','Wrong part'),('offset','Offset'),('rotated','Rotated'),('extra-layer','Extra layer'),('buried-repair','Buried repair'),('control','Correct (S0)')]:
  pool=[q for q in questions if q['mode']=='static' and q['family']==family]
  pool.sort(key=lambda q:(q['model'] not in ('sc-2132-1','obj-bookshelf','v7-long-bookshelf'),q['activeParts'],q['referenceMoves']))
  q=pool[0];s=session(q);stem='error-'+family
  for role,state in [('current',s.initial),('target',s.goal)]:add(q,s,stem+'-'+role,state,stem,True)
  selection['errors'].append(dict(name=stem,label=label,caseId=q['id'],model=q['model'],referenceMoves=q['referenceMoves']))
 # Exact static repair trajectory, maximum eight selected states.
 color_id=next(e['caseId'] for e in selection['errors'] if e['name']=='error-wrong-color')
 q=next(q for q in questions if q['id']==color_id);s=session(q)
 from dynamic_arena.validate_replays import Witness
 witness=Witness(s);frames=[dict(state=dict(s.initial),action='Start')]
 for _ in range(2*s.cap+4):
  a=json.loads(witness({}))
  if a['tool']=='observe':continue
  s.submit(dict(type=a['tool'],**a['args']))
  frames.append(dict(state=dict(s.ep.state),action=a['tool']))
  if s.done:break
 assert s.result()['success'];selection['repair']=[]
 for i,f in enumerate(frames):
  name='repair-'+str(i);add(q,s,name,f['state'],'repair',True);selection['repair'].append(dict(name=name,label=f['action'],caseId=q['id']))
 # Replay a current dynamic witness, preserving event-before/event-after states.
 q=next(q for q in questions if q['model']=='sc-2132-1' and q['taskType']=='D1' and q['family']=='missing');s=session(q);witness=Witness(s)
 frames=[dict(state=dict(s.initial),label='Start',kind='normal')];event_count=0
 for i in range(2*s.cap+4):
  action=json.loads(witness({}))
  if action['tool']=='observe':continue
  s.submit(dict(type=action['tool'],**action['args']))
  if len(s.events)>event_count:
   event=s.events[-1];frames.extend([dict(state=dict(event['before']),label='Before incident',kind='before'),dict(state=dict(event['after']),label='Hidden removal',kind='event')]);event_count=len(s.events)
  else:frames.append(dict(state=dict(s.ep.state),label=action['tool'].capitalize(),kind='normal'))
  if s.done:break
 assert s.result()['success'];important={0,len(frames)-1}|{i for i,f in enumerate(frames) if f['kind']!='normal'}
 for i in np.linspace(0,len(frames)-1,8,dtype=int):
  if len(important)<8:important.add(int(i))
 for i in range(len(frames)):
  if len(important)<8:important.add(i)
 selection['dynamic']=[]
 for j,i in enumerate(sorted(important)):
  f=frames[i];name='dynamic-'+str(j);add(q,s,name,f['state'],'dynamic',True);selection['dynamic'].append(dict(name=name,label=f['label'],kind=f['kind'],caseId=q['id'],sequenceIndex=i))
 assets={};bounds=defaultdict(list);ground=defaultdict(list)
 for s in specs:
  session_,ren=engines[s['caseId']];entries={**{a:a for a in ren.cert['fixed']},**s['state']};keys=[k for k in entries.values() if k and k in ren.geometry]
  bounds[s['group']].extend([ren.bounds[k]/20 for k in (s['frameKeys'] or keys) if k in ren.bounds]);ground[s['group']].extend(float(ren.bounds[k][:,1].min()/20) for k in keys);s['meshes']=[]
  for key in keys:
   name=hashlib.sha256((s['model']+key).encode()).hexdigest()[:18]
   if name not in assets:
    v,c=ren.geometry[key];v=v.astype(np.float32);normal=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-8);light=np.array([.3,.8,.5]);light/=np.linalg.norm(light);shade=.6+.4*np.abs(normal@light);rgb=np.clip(np.rint(c.astype(float)/shade[:,None]),0,255)/255
    data=np.concatenate([v/20,np.repeat(rgb[:,None,:],3,axis=1)],axis=2).astype(np.float32);p=cache/(name+'.bin');data.tofile(p);assets[name]=dict(file=p.name,vertices=len(v)*3,sha256=sha(p))
   s['meshes'].append(name)
  s['stateSha256']=hashlib.sha256(json.dumps(s['state'],sort_keys=True).encode()).hexdigest()
 groups={}
 for k,points in bounds.items():
  p=np.concatenate(points);groups[k]=dict(min=p.min(0).tolist(),max=p.max(0).tolist(),groundY=min(ground[k]))
 manifest=dict(schema='brick-atlas-release-scenes/1',size=[3200,2400],publicationOnly=True,evaluationInputUnchanged=True,apiCalls=0,assets=assets,groups=groups,scenes=specs)
 write(cache/'scenes.json',manifest);write(HERE/'evidence/release-render-states.json',{k:v for k,v in manifest.items() if k!='assets'});write(HERE/'evidence/release-figure-selection.json',selection)
 print('EXPORTED',len(specs),'scene states',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--scenes',action='store_true');a=p.parse_args();models,questions,stats=snapshot()
 if a.scenes:scenes(models,questions)
