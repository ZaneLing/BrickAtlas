"""Reference-only access/repeated-fault scenes; no learned-agent claims."""
from collections import defaultdict
from copy import deepcopy
import hashlib,json
import numpy as np
from release_assets import HERE,ROOT,read,write,sha
from bench_design.session import Session
from dynamic_arena.sensors import Sensors
from dynamic_arena.validate_replays import Witness
from publication_plate import add_plate

def main():
 cache=HERE/'build/capability-scenes';cache.mkdir(parents=True,exist_ok=True)
 specs=[];engines={};traces=[]
 for key,cid in [('access','E7:v7::v7-long-bookshelf::static::buried-repair::t7'),
                 ('repeated','SC:2132-1:dynamic:multiple-missing-then-offset')]:
  s=Session.open(cid,HERE/'build/capability-reference'/key,'scripted:capability-reference');s.autosave=False
  witness=Witness(s);states=[dict(state=deepcopy(s.initial),label='Faulty start' if key=='access' else 'Start')]
  for _ in range(s.cap):
   a=json.loads(witness({}));n=len(s.events)
   s.submit(dict(type='inspect',view='isometric') if a['tool']=='observe' else dict(type=a['tool'],**a['args']))
   if len(s.events)>n:
    event=s.events[-1]
    states.extend([dict(state=deepcopy(event['before']),label=f'Before event {len(s.events)}'),
                   dict(state=deepcopy(event['after']),label=f'After event {len(s.events)}')])
   elif a['tool']!='observe':states.append(dict(state=deepcopy(s.ep.state),label=a['tool'],decision=len(s.records)))
   if s.done:break
  assert s.result()['success'] and len(s.events)==(0 if key=='access' else 2)
  ren=Sensors(s).renderer;add_plate(ren);engines[key]=ren
  names=[]
  for i,st in enumerate(states):
   name=f'{key}-{i:02d}';specs.append(dict(name=name,group=key,model=key,caseId=cid,**st));names.append(name)
  traces.append(dict(key=key,caseId=cid,states=names,apiCalls=0,referenceOnly=True,success=True,
      records=s.records,events=s.events,initial=s.initial,target=s.goal,referenceOptimal=False))
 assets={};bounds=defaultdict(list);ground=defaultdict(list)
 for spec in specs:
  ren=engines[spec['model']];entries={**{a:a for a in ren.cert['fixed']},**spec['state']}
  keys=[k for k in entries.values() if k and k in ren.geometry];spec['meshes']=[]
  bounds[spec['group']].extend(ren.bounds[k]/20 for k in keys)
  ground[spec['group']].extend(float(ren.bounds[k][:,1].min()/20) for k in keys)
  for k in keys:
   name=hashlib.sha256((spec['model']+k).encode()).hexdigest()[:18]
   if name not in assets:
    v,c=ren.geometry[k];v=v.astype(np.float32);n=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-8)
    light=np.array([.3,.8,.5]);light/=np.linalg.norm(light);shade=.6+.4*np.abs(n@light)
    rgb=np.clip(np.rint(c.astype(float)/shade[:,None]),0,255)/255
    data=np.concatenate([v/20,np.repeat(rgb[:,None,:],3,axis=1)],axis=2).astype(np.float32)
    p=cache/(name+'.bin');data.tofile(p);assets[name]=dict(file=p.name,vertices=len(v)*3,sha256=sha(p))
   spec['meshes'].append(name)
  spec['stateSha256']=hashlib.sha256(json.dumps(spec['state'],sort_keys=True).encode()).hexdigest()
 groups={}
 for k,points in bounds.items():
  p=np.concatenate(points);groups[k]=dict(min=p.min(0).tolist(),max=p.max(0).tolist(),groundY=min(ground[k]),angles=[35,25])
 write(cache/'scenes.json',dict(size=[3200,2400],assets=assets,groups=groups,scenes=specs))
 write(HERE/'evidence/capability-reference-scenes.json',dict(apiCalls=0,referenceOnly=True,scenes=specs,traces=traces,groups=groups))
 print('Reference-only scene states:',len(specs))

if __name__=='__main__':main()
