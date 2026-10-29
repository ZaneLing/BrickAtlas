"""Replay two archived API traces and export faithful high-resolution figure states.

No provider calls. These are v2 qualitative development cases, never v3 results.
The GT row shares the recorded prefix through the incident, then follows a
privileged, legally replayed continuation. It is not a second learned run.
"""
from collections import defaultdict
from copy import deepcopy
import base64,gzip,hashlib,json
import numpy as np
from release_assets import HERE,ROOT,read,write,sha
from dynamic_arena.demo import create
from dynamic_arena.sensors import Sensors
from dynamic_v6.episode import continuation
from publication_plate import add_plate

RUNS=[('car','obj-city-car','incident-anthropic-claude-sonnet-5-5-obj-city-car-20261028-154133',
       'normal-anthropic-claude-sonnet-5-5-obj-city-car-20261028-153440'),
      ('chair','obj-chair','incident-openai-gpt-6-1-sol-obj-chair-20261028-153755',
       'normal-openai-gpt-6-1-sol-obj-chair-20261028-152256')]

def main():
 cache=HERE/'build/arena-scenes';cache.mkdir(parents=True,exist_ok=True)
 specs=[];rows=[];engines={};sources={};ledger=[]
 def add(tag,role,state,label,decision=None):
  name=f'arena-{tag}-{role}-{len(specs):02d}'
  specs.append(dict(name=name,model=tag,group=tag,state=dict(state),label=label,decision=decision,
                    caseId=f'arena:obj-{ "city-car" if tag=="car" else "chair"}:continuous-v1'))
  return name
 for tag,obj,run,normal in RUNS:
  folder=ROOT/'deliverables/brickplan-dynamic-arena/runs'/run
  record_path=folder/'record.private.json.gz';r=json.loads(gzip.decompress(record_path.read_bytes()))
  log=read(folder/'log.json');result=read(folder/'result.json')
  npth=folder.parent/normal/'result.json';normal_result=read(npth)
  for p in [record_path,folder/'log.json',folder/'result.json',npth]:sources[str(p.relative_to(ROOT))]=sha(p)
  assert normal_result['success'] and result['inputVersion'].endswith('brick-atlas-tool-arena/2')
  for field in ['model','caseId','inputVersion']:assert normal_result[field]==result[field]
  assert normal_result['taskType']=='D0' and normal_result['appliedEvents']==0
  assert normal_result['controllerMetrics']['budget']==result['controllerMetrics']['budget']
  s=create(HERE/'build/arena-replay'/tag,'scripted:publication-replay',model_id=obj);s.autosave=False
  for rec in r['records']:
   s.submit(rec['action']);actual=s.records[-1]
   for field in ['before','afterOwnActionBeforeExternalChange','after','feedback','newEventIndices']:
    assert actual[field]==rec[field],(run,rec['decision'],field)
  assert s.ep.state==r['final'] and s.result()['success']==result['success']
  ren=Sensors(s).renderer;add_plate(ren);engines[tag]=ren
  event=r['eventLedger'][0];at=event['atDecision'];records={x['decision']:x for x in r['records']}
  prefix=[(r['initial'],'Start',0),
          (records[5 if tag=='car' else 4]['after'],'d5: 2 parts' if tag=='car' else 'd4: 2 parts',5 if tag=='car' else 4),
          (event['before'],f'd{at}: before edit',at),
          (event['after'],'Hidden removal',at)]
  chosen=([15,17,19,21] if tag=='car' else [15,18,24,30])
  labels=(['d15: observe','d17: rejected','d19: restored','d21: success'] if tag=='car' else
          ['d15: builds on','d18: blocked','d24: wrong color','d30: wrong finish'])
  model_frames=[add(tag,'model',state,label,d) for state,label,d in prefix]
  model_frames += [add(tag,'model',records[d]['after'],label,d) for d,label in zip(chosen,labels)]
  # The event's own recovery is replayed first, then legal target completion.
  state=deepcopy(event['after']);gt_actions=[];gt_states=[]
  for a in event['native']['recovery']:
   state,fb=s.ep.runtime.check(state,a['actor'],a['type'],candidate=a.get('candidate'))
   assert fb['code']=='OK';gt_actions.append(a);gt_states.append(dict(state))
  tail=continuation(s.ep.runtime,state);assert tail is not None
  for a in tail:
   state,fb=s.ep.runtime.check(state,a.get('actor',a.get('partId')),a['type'],candidate=a.get('candidate'))
   assert fb['code']=='OK';gt_actions.append(a);gt_states.append(dict(state))
  assert s.ep.runtime.complete(state)
  # Four final panels include repair, legal continuation, verified endpoint.
  selected=[0,min(1,len(gt_states)-1),len(gt_states)-1,len(gt_states)-1]
  gt_labels=(['GT +1: restore','Target reached','Check endpoint','Finish: success'] if tag=='car' else
             ['GT +1: restore','GT +2: continue',f'GT +{len(gt_actions)}: complete','Finish: success'])
  gt_frames=model_frames[:4]+[add(tag,'gt',gt_states[k],label) for k,label in zip(selected,gt_labels)]
  item=dict(object=tag,runId=run,normalRunId=normal,model=result['model'],protocol='brick-atlas-tool-arena/2',
            currentProtocolResult=False,normalSucceeded=True,exactReplayPassed=True,incidentDecision=at,
            gtSharedPrefixThroughIncident=True,gtPrivileged=True,gtOptimalityClaim=False,
            gtActions=gt_actions,gtStates=gt_states,gtSuccess=True,modelSuccess=result['success'],
            modelFrames=model_frames,gtFrames=gt_frames,metrics=result['executionMetrics'],
            fullPlacement=result['stateMetrics']['fullPlacement'],eventWindows=result['eventWindows'],
            observations=result['controllerMetrics']['observeCalls'])
  rows.append(item)
  for c,rec in zip(log['calls'],r['records']):
   assert c['index']==rec['decision']
   ledger.append(dict(object=tag,decision=c['index'],modelOutput=c['modelOutput'],
                      feedback=c['environmentOutput']['code'],state=rec['after'],
                      eventApplied=bool(rec['newEventIndices'])))
  if tag=='car':
   call=log['calls'][14];assert call['modelOutput']['tool']=='observe'
   next_call=log['calls'][15];assert next_call['providerReceipt']
   sent=[b['image_url'] for b in next_call['modelInput']['messages'][-1]['content'] if b['type']=='image_url']
   assert [b['sha256'] for b in sent]==[b['sha256'] for b in call['environmentOutput']['images']]
   # Check original serialized provider request, not only the readable export.
   target_hash=next_call['providerReceipt']['requestBodySha256'];raw_request=None
   for p in (folder/'api').glob('*.request.json.gz'):
    data=gzip.decompress(p.read_bytes())
    if hashlib.sha256(data).hexdigest()==target_hash:raw_request=json.loads(data);break
   assert raw_request is not None
   actual=[b['image_url']['url'] for b in raw_request['messages'][-1]['content'] if b['type']=='image_url']
   assert [hashlib.sha256(base64.b64decode(url.split(',',1)[1])).hexdigest() for url in actual]==[b['sha256'] for b in sent]
   io=dict(runId=run,decision=15,request=call['modelOutput'],response=call['environmentOutput'],
           nextAction=log['calls'][15]['modelOutput'],actualInputs=[])
   for im in call['environmentOutput']['images']:
    if im['role'] not in ('current','target'):continue
    p=ROOT/'deliverables/brickplan-dynamic-arena'/im['url'].lstrip('/')
    assert sha(p)==im['sha256'];sources[str(p.relative_to(ROOT))]=sha(p)
    io['actualInputs'].append(dict(role=im['role'],path=str(p.relative_to(ROOT)),sha256=sha(p)))
 assets={};bounds=defaultdict(list);ground=defaultdict(list)
 for spec in specs:
  ren=engines[spec['model']];entries={**{a:a for a in ren.cert['fixed']},**spec['state']}
  keys=[k for k in entries.values() if k and k in ren.geometry];spec['meshes']=[]
  bounds[spec['group']].extend(ren.bounds[k]/20 for k in keys)
  ground[spec['group']].extend(float(ren.bounds[k][:,1].min()/20) for k in keys)
  for key in keys:
   name=hashlib.sha256((spec['model']+key).encode()).hexdigest()[:18]
   if name not in assets:
    v,c=ren.geometry[key];v=v.astype(np.float32);n=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-8)
    light=np.array([.3,.8,.5]);light/=np.linalg.norm(light);shade=.6+.4*np.abs(n@light)
    rgb=np.clip(np.rint(c.astype(float)/shade[:,None]),0,255)/255
    data=np.concatenate([v/20,np.repeat(rgb[:,None,:],3,axis=1)],axis=2).astype(np.float32)
    p=cache/(name+'.bin');data.tofile(p);assets[name]=dict(file=p.name,vertices=len(v)*3,sha256=sha(p))
   spec['meshes'].append(name)
  spec['stateSha256']=hashlib.sha256(json.dumps(spec['state'],sort_keys=True).encode()).hexdigest()
 groups={}
 for k,points in bounds.items():
  p=np.concatenate(points);groups[k]=dict(min=p.min(0).tolist(),max=p.max(0).tolist(),groundY=min(ground[k]),angles=[35,25])
 manifest=dict(schema='brick-atlas-archived-arena-scenes/1',size=[3200,2400],apiCalls=0,
               publicationOnly=True,evaluationInputUnchanged=True,assets=assets,groups=groups,scenes=specs)
 write(cache/'scenes.json',manifest)
 write(HERE/'evidence/arena-traces.json',dict(schema='brick-atlas-qualitative-traces/1',apiCalls=0,
       scope='Purposively selected historical v2 cases, not current-release performance or causal effects.',
       sources=sources,runs=rows,scenes=specs,groups=groups,decisionLedger=ledger,io=io))
 print('Verified two archived traces; exported',len(specs),'states; no API calls.')

if __name__=='__main__':main()
