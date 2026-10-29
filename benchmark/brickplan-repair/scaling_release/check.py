"""Replay every released question and independently re-read original source files.

Independent serialization/loader check, NOT an independent physics engine.
"""
from concurrent.futures import ProcessPoolExecutor,as_completed
from copy import deepcopy
import argparse,hashlib,json
from scaling_release import ROOT,OUT
from expansion_v7.build import read,write

def checksum_for(folder):
 from pathlib import Path
 paths=[folder/n for n in ['metadata.json','certificate.private.json.gz','manual.private.json.gz','cases.private.json.gz']]
 return hashlib.sha256(b''.join(p.read_bytes() for p in paths)+Path(__file__).read_bytes()).hexdigest()

def verified(folder):
 p=folder/'check.json'
 if not p.exists():return False
 value=read(p)
 return bool(value.get('passed') and value.get('checksum')==checksum_for(folder))

def one(number):
 from expansion_v7.runtime import Episode,runtime,public_action,execute
 from dynamic_arena.source_library import flatten
 from dynamic_arena.curate_sources import FigureAudit
 folder=OUT/'private'/number;paths=[folder/n for n in ['metadata.json','certificate.private.json.gz','manual.private.json.gz','cases.private.json.gz']]
 from pathlib import Path
 checksum=checksum_for(folder);checkfile=folder/'check.json'
 if checkfile.exists():
  old=read(checkfile)
  if old.get('checksum')==checksum and old.get('passed'):return old
 meta,cert,manual,cases=map(read,paths);checks=[];errors=[]
 try:
  original=ROOT/cert['source']['original'];raw=original.read_bytes()
  assert hashlib.sha256(raw).hexdigest()==cert['source']['originalSha256'],'Original source hash changed'
  instances,author,license_=flatten(raw)
  mfpath=OUT/'checks/original-manifests'/f'{number}.json';write(mfpath,dict(instances=instances))
  figure=FigureAudit().audit(dict(manifest=str(mfpath.relative_to(ROOT)),sourceFile=str(original.relative_to(ROOT))))
  assert figure['status']=='no-figure-parts-found',figure
  source_parts=[r['part'] for r in cert['candidates'].values() if r['kind']=='goal']+list(cert['fixed'].values())+[r['part'] for r in cert.get('conservativeContext',{}).values()]
  represented={r['sourceIndex'] for r in source_parts if 'sourceIndex' in r}
  assert represented==set(range(len(instances))),('Missing original instances',len(represented),len(instances))
  import numpy as np
  from geometry import AXIS_INVERSE
  for part in source_parts:
   if 'sourceIndex' not in part:continue
   original_part=instances[part['sourceIndex']]
   raw_matrix=AXIS_INVERSE@np.asarray(original_part['originalMatrix']).reshape(4,4).T
   same_name=part['partNumber']==original_part['partNumber']
   if not same_name:
    from render import ldraw
    same_name=ldraw.resolve(part['partNumber']+'.dat').read_bytes()==ldraw.resolve(original_part['partNumber']+'.dat').read_bytes()
   assert same_name and str(part['colorCode'])==str(original_part['colorCode']),('Source part/color changed',part['sourceIndex'])
   assert np.allclose(part['rawMatrix'],raw_matrix,rtol=0,atol=1e-7),('Source placement changed',part['sourceIndex'])
  goal_indices={r['part']['sourceIndex'] for r in cert['candidates'].values() if r['kind']=='goal'}
  assert goal_indices==set(meta['scope']['indices'])==set(cert['source']['moduleSourceIndices']),'Scope metadata/certificate mismatch'
  assert len(manual['actions'])==meta['activeParts']==len(goal_indices),'Manual length/metadata mismatch'
  assert len({c['id'] for c in cases})==len(cases)
  assert 2 <= sum(c['mode']=='static' for c in cases) <= 6
  assert sum(c['mode']=='static' and c['family']=='control' for c in cases)==1
  from expansion_v7.build import signature_key
  rt0=runtime(cert)
  assert len({signature_key(rt0,c) for c in cases if c['mode']=='static'})==sum(c['mode']=='static' for c in cases)
  rt=runtime(cert)
  for c in cases:
   assert not set(c['humanErrorIds']) & {'H12','H14','H15','H16','H17'}
   ep=Episode(cert,c,41);ep.runtime.q=rt.q
   for a in c['referenceActions']:
    ep.step(public_action(ep,a));assert ep.feedback['code']=='OK',(c['id'],a,ep.feedback)
   ep.step(dict(type='finish'));score=ep.score()
   assert score['success'],(c['id'],score)
   assert len(ep.events)==len(c['events']),(c['id'],'Event count mismatch')
   if c['events']:
    v=c['visibilityCheck'];assert all(x['visible'] for x in (v if isinstance(v,list) else [v]))
   checks.append(dict(id=c['id'],success=True,eventsApplied=len(ep.events),referenceMoves=len(c['referenceActions'])))
  # An adjacent independent swap is a second legal trajectory, when available.
  normal=manual['actions'];control=next(c for c in cases if c['mode']=='dynamic' and not c['events']);alternate=None
  for i in range(len(normal)-1):
   sequence=deepcopy(normal);sequence[i],sequence[i+1]=sequence[i+1],sequence[i]
   end,_=execute(rt,control['initial'],sequence)
   if end is not None and rt.signature(end)==rt.signature(control['goal']):
    ep=Episode(cert,control,41);ep.runtime.q=rt.q
    for a in sequence:ep.step(public_action(ep,a));assert ep.feedback['code']=='OK'
    ep.step(dict(type='finish'));assert ep.score()['success'];alternate=dict(swappedSteps=[i+1,i+2],accepted=True);break
  out=dict(setNumber=number,checksum=checksum,passed=True,cases=checks,figureAudit=figure,originalInstances=len(instances),allOriginalInstancesRepresented=True,alternateLegalOrder=alternate,alternateSearch='adjacent independent swaps only; absent does not prove uniqueness',independentPhysicsEngine=False,apiCalls=0)
 except Exception as exc:
  out=dict(setNumber=number,checksum=checksum,passed=False,cases=checks,error=str(exc),apiCalls=0)
 write(checkfile,out);return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=3);a=p.parse_args();rows=[p.parent.name for p in (OUT/'private').glob('*/cases.private.json.gz')];results=[]
 with ProcessPoolExecutor(max_workers=a.workers) as ex:
  fs={ex.submit(one,n):n for n in rows}
  for f in as_completed(fs):
   try:r=f.result()
   except Exception as e:r=dict(setNumber=fs[f],passed=False,error=str(e))
   results.append(r);print('CHECK PASS' if r['passed'] else 'CHECK FAIL',r['setNumber'],r.get('error',''),flush=True)
 write(OUT/'checks/full-replay.json',dict(passed=all(r['passed'] for r in results),checkedModels=len(results),checkedQuestions=sum(len(r.get('cases',[])) for r in results),failed=[r for r in results if not r['passed']],results=results,apiCalls=0,notModelPerformance=True,notIndependentPhysicsValidation=True))

if __name__=='__main__':main()
