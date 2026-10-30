"""Load admitted retained tasks without loading unrelated historical banks."""
from functools import lru_cache
from copy import deepcopy
import json
from reliability import ROOT
from expansion_v7.build import read

@lru_cache(maxsize=1)
def index():
 root=ROOT/'deliverables/brick-atlas-dataset-v1/questions'
 return {q['id']:q for mode in ('static','dynamic') for q in map(json.loads,(root/f'{mode}.jsonl').read_text().splitlines())}

def load(cid,directory):
 q=index()[cid];bank=cid.split(':')[0];mid=q['model']
 if bank=='E7':
  from expansion_v7.runtime import Episode
  from expansion_v7.run_episode import Packet
  folder=ROOT/'deliverables/brickplan-expansion-v7/models'/mid
  case=deepcopy(next(c for c in read(folder/'cases.private.json.gz') if c['id']==cid[3:]))
  ep=Episode(read(folder/'certificate.private.json.gz'),case,41)
  packet=Packet(ep,read(folder/'manual.private.json.gz'),directory);renderer=None
 elif bank=='D':
  from dynamic_v6.episode import DynamicEpisode
  from dynamic_v6.interface import renderer_for
  folder=ROOT/'deliverables/brickplan-dynamic-v6/models'/mid
  cases=read(folder/'cases.json');cases=cases.get('cases',[]) if isinstance(cases,dict) else cases
  case=deepcopy(next(c for c in cases if c['id']==cid[2:]))
  ep=DynamicEpisode(read(folder/'qualification.json'),case,41);packet=None;renderer=renderer_for(ep)
 else:raise ValueError('Not a retained active bank')
 normal=next((r['id'] for r in index().values() if r['model']==mid and r['taskType']=='D0'),None)
 meta=dict(canonicalId=cid,taskType=q['taskType'],track=q['track'],source=q['sourceGroup'],model=mid)
 if normal:meta['normalCanonicalId']=normal
 row=dict(key=cid,bank=bank,model=mid,title=q['title'],mode=q['mode'],case=case,family=q['family'],evaluationMetadata=meta)
 return row,ep,packet,renderer
