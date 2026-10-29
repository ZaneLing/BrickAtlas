"""Per-source full-object or explicit finishing-stage qualification.

No unsupported part is silently removed from a selected scope. Entire original
context remains visible and participates in collision checks. Failed scopes are
retained in the per-model audit, not counted as qualified questions.
"""
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
import argparse,hashlib,json,re,traceback,fcntl
import numpy as np
from scaling_release import ROOT,OUT
from expansion_v7.build import read,write
from recognizable_models.intake import ingest,lock_embedded_parts
from recognizable_models.prepare import complete_certificate
from community_modules.core import source_certificate,LocalQualifier
from expansion_v7.prepare import find_order
from expansion_v7.runtime import runtime

KEYWORDS={
 'roof':'屋顶','cockpit':'驾驶舱','canopy':'驾驶舱盖','cabin':'驾驶室','cab ':'驾驶室',
 'engine':'引擎','bonnet':'引擎盖','hood':'引擎盖','rotor':'旋翼','tail':'尾部',
 'wing':'机翼','head':'头部','neck':'颈部','petal':'花瓣','flower':'花朵','chimney':'烟囱',
 'upper':'上部结构','nose':'前端','bridge':'舰桥','crane':'吊臂','turret':'顶部转台',
 'stern':'船尾','front':'前部','rear':'后部','body':'主体','hull':'船体','door':'门'}


def manifest(row):
 path=ROOT/row['manifest'];mf=read(path)
 # Use existing derived manifests when provenance and detailed descriptions exist.
 if all('displayName' in p and 'colorHex' in p for p in mf['instances']) and path.with_name('provenance.json').exists():
  prov=read(path.with_name('provenance.json'));source=row.get('sourceFile') or mf.get('sourceFile') or prov.get('source',{}).get('path')
  if not source:source=next((r['file'] for r in prov.get('resources',[]) if r.get('file','').lower().endswith(('.mpd','.ldr'))),None)
  if source and (ROOT/source).exists():
   lock_embedded_parts(ROOT/source)
   if not all('sourceSubmodelInstancePath' in p for p in mf['instances']):
    record=dict(set=row['setNumber'],file=source,title=row['title'],pageUrl=row['sourceUrl'],url=row.get('downloadUrl',row['sourceUrl']),sha256=hashlib.sha256((ROOT/source).read_bytes()).hexdigest())
    ingest(record,model_prefix='sc-source-');mid='sc-source-'+row['setNumber'];return mid,read(ROOT/'web/public/models'/mid/'manifest.json')
   mf['sourceFile']=source;mf['model']['setNumber']=row['setNumber'];mid='sc-source-'+row['setNumber'];dest=ROOT/'web/public/models'/mid
   write(dest/'manifest.json',mf);write(dest/'provenance.json',prov);return mid,mf
  return path.parent.name,mf
 source=row.get('sourceFile') or mf.get('sourceFile')
 if not source:raise ValueError('Original source file path unavailable')
 record=dict(set=row['setNumber'],file=source,title=row['title'],pageUrl=row['sourceUrl'],url=row.get('downloadUrl',row['sourceUrl']),sha256=row.get('sourceHash'))
 ingest(record);path=ROOT/'web/public/models'/('r-omr-'+row['setNumber'])/'manifest.json';return path.parent.name,read(path)


def cached(row):
 """Reuse independently stored, source-preserving whole/named certificates."""
 if row.get('officialAlternate'):return None
 sources=[]
 for directory in [ROOT/'deliverables/brickplan-quality-round/source-expansion/models',ROOT/'deliverables/brickplan-dynamic-arena/new-objects',ROOT/'deliverables/brickplan-recognizable-models/models']:
  for p in directory.glob('*/metadata.json'):
   m=read(p);number=m.get('setNumber',m.get('sourceSetId',m.get('source',{}).get('sourceSetId')))
   if number!=row['setNumber']:continue
   certfile=p.parent/'certificate.private.json.gz';manualfile=p.parent/'manual.private.json.gz'
   if not certfile.exists():certfile=p.parent/'base-certificate.private.json.gz';manualfile=p.parent/'base-manual.private.json.gz'
   if certfile.exists() and manualfile.exists():sources.append((m,certfile,manualfile))
 if not sources:
  d=ROOT/'deliverables/brickplan-community-modules'
  for c in d.glob('*/certificate.private.json'):
   cert=read(c);source=cert.get('source',{});n=str(source.get('modelId',''));found=re.search(r'(?<!\d)'+re.escape(row['setNumber'].split('-')[0])+r'(?!\d)',n)
   f=c.with_name('manual.private.json')
   if found and f.exists():sources.append((dict(title=source.get('selectionReason',c.parent.name)),c,f))
 if not sources:return None
 m,c,f=sorted(sources,key=lambda x:(not x[0].get('completeObject',x[0].get('kind')=='complete'),-x[0].get('activeParts',x[0].get('parts',0))))[0]
 cert=read(c);manual=read(f);normal=manual['actions']
 if len(normal)<3:return None
 return cert,normal,dict(kind='complete-object' if cert.get('environmentMode')=='white-baseplate' else 'named-finishing-module',description=m.get('module',m.get('title',row['title'])),selectionMethod='reused-source-checked-scope',indices=cert['source']['moduleSourceIndices'])


def scopes(mf):
 parts=mf['instances'];groups=defaultdict(list)
 for i,p in enumerate(parts):
  for name in set(p.get('sourceSubmodelPath',p.get('path',[]))+[p.get('sourceFile','')]):groups[name].append(i)
  path=p.get('sourceSubmodelInstancePath',[])
  for depth in range(1,len(path)+1):groups[' / '.join(path[:depth])].append(i)
 candidates=[]
 for name,indices in groups.items():
  if len(indices)==len(parts) or not 3<=len(indices)<=32:continue
  semantic=next((v for k,v in KEYWORDS.items() if re.search(r'\b'+re.escape(k),name,re.I)),None)
  candidates.append(dict(kind='named-finishing-module',description=(semantic or '完整子组件')+'（原作者子模型 '+name+'）',selectionMethod='author-named-submodel' if semantic else 'author-submodel',indices=indices))
 # Genuine source STEP groups only, never interpret source line order as instructions.
 if len(groups)==1:
  steps=defaultdict(list)
  for i,p in enumerate(parts):
   step=p.get('sourceStep',p.get('buildStep'))
   if step is not None:steps[step].append(i)
  if len(steps)>=3:
   ids=[]
   for step in sorted(steps,reverse=True):
    ids=steps[step]+ids
    if len(ids)>32:break
    if len(ids)>=3:candidates.append(dict(kind='instruction-finishing-stage',description=f'原作者最后 {len([s for s in steps if s>=step])} 个说明步骤的收尾',selectionMethod='author-step-suffix',indices=ids.copy()))
 # A complete horizontal finishing band, not a nearest-neighbour crop. All parts
 # in that band must be operable; failed selections are rejected as a whole.
 heights=[round(np.asarray(p['originalMatrix']).reshape(4,4).T[1,3],3) for p in parts]
 top=max(heights);bottom=min(heights)
 for level in sorted(set(heights),reverse=True):
  ids=[i for i,y in enumerate(heights) if y>=level-.001]
  if len(ids)>32:break
  if len(ids)<3 or len(ids)>=len(parts):continue
  if level<bottom+(top-bottom)*.55:continue
  candidates.append(dict(kind='upper-finishing-stage',description='完整物件的上方收尾层（全部所选零件在图中标出；下方主体已完成）',selectionMethod='complete-upper-height-band',heightThreshold=level,indices=ids))
 # Side and end components can be clearer than the top (e.g. wings).
 positions=np.array([np.asarray(p['originalMatrix']).reshape(4,4).T[:3,3] for p in parts])
 for axis in (0,2):
  for sign in (-1,1):
   values=np.round(positions[:,axis]*sign,3);hi,lo=max(values),min(values)
   for level in sorted(set(values),reverse=True):
    ids=[i for i,v in enumerate(values) if v>=level-.001]
    if len(ids)>32:break
    if len(ids)<3 or len(ids)>=len(parts) or level<lo+(hi-lo)*.65:continue
    candidates.append(dict(kind='side-finishing-stage',description='完整物件的侧面／端部收尾区域（以标注图与逐件说明为准，保留全部主体）',selectionMethod='complete-exterior-coordinate-band',axis=axis,sign=sign,threshold=level,indices=ids))
 seen=set();out=[]
 for c in candidates:
  key=tuple(sorted(c['indices']))
  if key in seen:continue
  seen.add(key);out.append(c)
 # Prefer meaningful authored scopes; within a type aim for 8–16 actions.
 target=24 if len(parts)>=180 else 16 if len(parts)>=80 else 10
 out.sort(key=lambda c:({'author-named-submodel':0,'author-step-suffix':1,'author-submodel':2,'complete-upper-height-band':3,'complete-exterior-coordinate-band':4}[c['selectionMethod']],abs(len(c['indices'])-target)))
 return out


def prepare(row):
 folder=OUT/'private'/row['setNumber'];cached_result=cached(row);attempts=[]
 if cached_result:
  cert,normal,scope=cached_result
 else:
  mid,mf=manifest(row)
  if len(mf['instances'])<=50:
   try:
    cert,_=complete_certificate(dict(id='sc-'+row['setNumber'],model=mid,title=row['title']));normal=find_order(runtime(cert))
    if normal:cached_result=(cert,normal,dict(kind='complete-object',description='完整物件，从白色凸点底板开始',selectionMethod='all-original-parts',indices=list(range(len(mf['instances'])))))
   except Exception as e:attempts.append(dict(scope='complete-object',reason=cause(e)))
  if cached_result:cert,normal,scope=cached_result
  else:
   original=row.get('sourceFile') or mf.get('sourceFile')
   if not original:
    prov=read(ROOT/'web/public/models'/mid/'provenance.json');original=prov.get('source',{}).get('path')
   if not original:raise ValueError('Original path not recorded')
   md=mf['model'];base=source_certificate(dict(id='sc-'+row['setNumber'],model=mid,indices=[],original=original,author=row.get('author',md.get('author')),url=row['sourceUrl']))
   options=scopes(mf);shared=LocalQualifier()
   for scope in options:
    ids=scope['indices'];missing=[i for i in ids if 'F'+str(i) not in base['fixed']]
    if missing:attempts.append(dict(scope=scope,reason='Unsupported selected parts',indices=missing));continue
    cert=deepcopy(base)
    for i in ids:
     actor='P'+str(i);part=cert['fixed'].pop('F'+str(i));cert['candidates'][actor+':goal']=dict(actor=actor,kind='goal',part=part)
    cert['source']['moduleSourceIndices']=ids
    try:
     rt=runtime(cert);rt.q=shared;normal=find_order(rt)
    except Exception as e:attempts.append(dict(scope=scope,reason=cause(e)));continue
    if normal:break
    attempts.append(dict(scope=scope,reason='No complete legal normal build witness'))
   else:
    write(folder/'prepare-failure.json',dict(setNumber=row['setNumber'],title=row['title'],attempts=attempts,options=len(options)))
    raise ValueError('No qualified whole or finishing scope')
 cert['source'].update(sourceSetId=row['setNumber'],license=row.get('license',cert['source'].get('license')),selectionKind=scope['kind'],selectionReason=scope['description'],sourceInstancesDropped=0,completeSourceRetained=True)
 cert['id']='sc-'+row['setNumber']
 write(folder/'base-certificate.private.json.gz',cert);write(folder/'base-manual.private.json.gz',dict(actions=normal))
 meta=dict(id=cert['id'],setNumber=row['setNumber'],title=row['title'],sourceModelName=row.get('sourceModelName'),category=row['objectCategory'],sourceParts=row['parts'],activeParts=len(normal),scope=scope,source=row,normalBuildVerified=True,humanValidated=False,attempts=attempts)
 write(folder/'metadata.json',meta)
 (folder/'status.json').unlink(missing_ok=True)
 return meta


def cause(e):
 while e.__cause__:e=e.__cause__
 return str(e)[:300]


def main():
 p=argparse.ArgumentParser();p.add_argument('--set',required=True);a=p.parse_args();row=next(r for r in read(OUT/'source-pool.json')['models'] if r['setNumber']==a.set)
 folder=OUT/'private'/a.set;folder.mkdir(parents=True,exist_ok=True)
 lock=(folder/'work.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX)
 if (folder/'metadata.json').exists():print('READY CACHED',a.set,flush=True);return
 try:m=prepare(row);print('READY',a.set,m['activeParts'],m['scope']['selectionMethod'],flush=True)
 except Exception as e:
  write(OUT/'private'/a.set/'status.json',dict(status='withheld',phase='prepare',reason=cause(e)));print('WITHHELD',a.set,cause(e),flush=True)
if __name__=='__main__':main()
