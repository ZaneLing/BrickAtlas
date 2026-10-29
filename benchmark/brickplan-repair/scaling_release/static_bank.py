"""Keep distinct static repairs for each qualified error family plus a control."""
from concurrent.futures import ProcessPoolExecutor,as_completed
from copy import deepcopy
import hashlib,json
from scaling_release import OUT
from expansion_v7.build import read,write,signature_key
from expansion_v7.runtime import Episode,runtime,public_action

def asset_key(cid):
 return hashlib.sha256(cid.encode()).hexdigest()[:16]

def expand(cert,cases,cache=None):
 rt=runtime(cert)
 if cache is not None:rt.q=cache
 result=deepcopy(cases);seen={signature_key(rt,c) for c in result};ids={c['id'] for c in result}
 singles=[c for c in result if c['mode']=='dynamic' and len(c['events'])==1]
 for d in singles:
  e=d['referenceEvents'][0];cid=d['id'].replace(':dynamic:',':static:')
  if cid in ids:continue
  s={k:deepcopy(v) for k,v in d.items() if k not in ('referenceEvents','referenceScore','physicalTaskSha256')}
  s.update(id=cid,mode='static',initial=deepcopy(e['after']),goal=deepcopy(e['before']),events=[],completedInstructionStep=d['events'][0]['minimumInstalled'],referenceActions=deepcopy(e['recovery']),referenceIncident=deepcopy(e),pairedDynamicId=d['id'])
  key=signature_key(rt,s)
  if key in seen:continue
  ep=Episode(cert,s,41);ep.runtime.q=rt.q
  for a in s['referenceActions']:
   ep.step(public_action(ep,a));assert ep.feedback['code']=='OK',(cid,ep.feedback)
  ep.step(dict(type='finish'));assert ep.score()['success'],cid
  s.update(referenceScore=ep.score(),physicalTaskSha256=key,legalWitnessOnly=True,humanValidated=False,modelEvaluated=False)
  result.append(s);seen.add(key);ids.add(cid)
 if not any(c['mode']=='static' and c['family']=='control' for c in result):
  first=next(c for c in result if c['mode']=='static');s=deepcopy(first)
  s.update(id=first['id'].rsplit(':',1)[0]+':control',family='control',initial=deepcopy(first['goal']),referenceActions=[],referenceIncident=None,visibilityCheck=None,humanErrorIds=[],pairedDynamicId=next(c['id'] for c in result if c['mode']=='dynamic' and c['family']=='control'))
  ep=Episode(cert,s,41);ep.runtime.q=rt.q;ep.step(dict(type='finish'));assert ep.score()['success']
  s.update(referenceScore=ep.score(),physicalTaskSha256=signature_key(rt,s));result.append(s)
 return result

def one(number):
 folder=OUT/'private'/number;cert=read(folder/'certificate.private.json.gz');old=read(folder/'cases.private.json.gz');cases=expand(cert,old)
 assert {c['id'] for c in old}<={c['id'] for c in cases}
 meta=read(folder/'metadata.json');meta.update(caseCount=len(cases),staticCases=sum(c['mode']=='static' for c in cases),families=sorted({c['family'] for c in cases}),staticSelection='one qualified snapshot per distinct error family plus one clean control; exact physical duplicates excluded')
 write(folder/'cases.private.json.gz',cases);write(folder/'metadata.json',meta)
 design=read(OUT/'designs'/f'{number}.json');design['cases']=[dict(id=c['id'],mode=c['mode'],family=c['family'],events=len(c['events']),referenceMoves=len(c['referenceActions'])) for c in cases];design['staticSelection']=meta['staticSelection'];write(OUT/'designs'/f'{number}.json',design)
 return dict(model=number,previousStatic=sum(c['mode']=='static' for c in old),static=meta['staticCases'],added=len(cases)-len(old))

def main():
 numbers=[p.parent.name for p in (OUT/'private').glob('*/cases.private.json.gz')];rows=[]
 with ProcessPoolExecutor(max_workers=3) as ex:
  fs={ex.submit(one,n):n for n in numbers}
  for f in as_completed(fs):
   r=f.result();rows.append(r);print('STATIC',r['model'],r['static'],flush=True)
 write(OUT/'checks/static-expansion.json',dict(models=len(rows),static=sum(r['static'] for r in rows),added=sum(r['added'] for r in rows),rows=rows,apiCalls=0))

if __name__=='__main__':main()
