"""Exact geometry exports for publication-only physically shaded renders.

No evaluation scene, camera, input, or task is modified. All displayed states
come from current task certificates or the sanitized historical trace export.
"""
from pathlib import Path
from collections import defaultdict
import json,sys,hashlib,re
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'benchmark/brickplan-repair'))
from bench_design.catalogue import rows_with_cases,module_runtime
from community_modules.core import render_certificate
from dynamic_v5.vision import DynamicVisionRenderer
from baseplate import PlateAssembly
from render import PALETTE
from bench_design.metrics import state_metrics
PALETTE.update(dict(re.findall(r'CODE\s+(\d+)\s+VALUE\s+(#[0-9A-Fa-f]{6})',
    (ROOT/'assets-source/ldraw-library/locked/LDConfig.ldr').read_text())))
OUT=HERE/'figures-publication';CACHE=HERE/'build/publication-scenes'
OUT.mkdir(exist_ok=True);CACHE.mkdir(parents=True,exist_ok=True)
rows={r['key']:r for r in rows_with_cases()};examples=json.loads((ROOT/'deliverables/brickplan-benchmark-spec/examples.json').read_text())
specs=[];groups={};engines={};sources={}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def engine(bank,mid):
 key=(bank,mid)
 if key not in engines:
  if bank=='D':
   rt=PlateAssembly(json.loads((ROOT/'deliverables/brickplan-dynamic-v6/models'/mid/'qualification.json').read_text()));ren=DynamicVisionRenderer(rt.cert,rt)
  else:rt=module_runtime(bank,mid);ren=DynamicVisionRenderer(render_certificate(rt.cert),rt)
  engines[key]=(rt,ren)
 return engines[key]
def add(name,bank,mid,state,group,scope='current',frame_keys=None):
 rt,ren=engine(bank,mid)
 specs.append(dict(name=name,bank=bank,model=mid,state=state,group=group,scope=scope,frameKeys=frame_keys))
 return rt,ren
# Atomic static pairs and two process burdens; stage goals, never future states.
for e in examples:
 r=rows[e['id']];c=r['case']
 detail=None
 if e['code']=='E04':
  detail=[c['initial'][c['referenceActions'][0]['actor']],c['referenceActions'][1]['candidate']]
 for suffix,state in [('current',c['initial']),('target',c['goal'])]:add(e['code']+'-'+suffix,r['bank'],r['model'],state,e['code'],frame_keys=detail)
# A numerical worked repair, computed by the actual current scorer.
e=next(e for e in examples if e['code']=='E03');r=rows[e['id']];c=r['case'];rt,_=engine(r['bank'],r['model'])
a=c['referenceActions'][0];midway,fb=rt.check(c['initial'],a['actor'],a['type'],candidate=a.get('candidate'));assert fb['code']=='OK'
add('metric-remove',r['bank'],r['model'],midway,'E03')
worked=dict(caseId=e['id'],states=[dict(label=label,state=state,metrics=state_metrics(rt,c['initial'],state,c['goal'],finished=(label=='Replaced')))
    for label,state in [('Initial',c['initial']),('Removed',midway),('Replaced',c['goal'])]],referenceOnly=True,modelPerformance=False)
(HERE/'evidence/worked-metric-example.json').write_text(json.dumps(worked,indent=2)+'\n')
# Retained object/module coverage is re-rendered with the same publication style.
mainrows=[json.loads(l) for l in (ROOT/'deliverables/brickplan-benchmark-spec/questions.jsonl').read_text().splitlines()]
for mid in dict.fromkeys(r['model'] for r in mainrows if r['mainTaskCandidate'] and r['track']=='whole-object-dynamic' and r['bank']=='D'):
 rt,_=engine('D',mid);add('atlas-'+mid,'D',mid,rt.goal,'atlas-'+mid)
for mid in dict.fromkeys(r['model'] for r in mainrows if r['track']=='dynamic-structure-diagnostic'):
 rt,_=engine('D',mid);add('diagnostic-'+mid,'D',mid,rt.goal,'diagnostic-'+mid)
for mid,label in [('v7-long-stone-bridge','bridge'),('v7-long-cottage','cottage')]:
 rt,_=engine('E7',mid);add('object-'+label,'E7',mid,rt.goal,'object-'+label)
for mid in dict.fromkeys(r['model'] for r in mainrows if r['mainTaskCandidate'] and r['track']=='named-module-dynamic'):
 bank='E7' if mid=='museum-roof-long' else 'M';rt,_=engine(bank,mid);add('atlas-'+mid,bank,mid,rt.goal,'atlas-'+mid)
# Eight complete, named and longer objects for a compact contextual strip.
for bank,mid,label in [('O','whole-4018','ship'),('O','whole-4017','sea-helicopter'),('O','whole-4037','mini-helicopter'),('E7','v7-long-bookshelf','bookshelf'),('E7','v7-long-city-bus','bus'),('E7','v7-long-gantry-press','press'),('M','racer-top','racer'),('M','seaplane-tail','seaplane')]:
 rt,ren=engine(bank,mid);add('object-'+label,bank,mid,rt.goal,'object-'+label)
# Full context plus remaining-module stages for the hero and interface figure.
mid='racer-top';rt,ren=engine('M',mid)
manual=json.loads((ROOT/'deliverables/brickplan-community-modules'/mid/'manual.private.json').read_text())
for i in [0,2,3,len(manual['states'])-1]:add('racer-stage-'+str(i),'M',mid,manual['states'][i],'racer-context')
change=json.loads((ROOT/'deliverables/brickplan-community-modules'/mid/'perturbations.private.json').read_text())
add('racer-event','M',mid,change['extra-layer']['after'],'racer-context')
# Buried-error witness: remove covers, exchange the wrong brick, restore covers.
e=next(e for e in examples if e['code']=='P02');r=rows[e['id']];c=r['case'];rt,_=engine(r['bank'],r['model']);state=dict(c['initial'])
for i,a in enumerate(c['referenceActions'],1):
 state,fb=rt.check(state,a['actor'],a['type'],candidate=a.get('candidate'));assert fb['code']=='OK'
 if i in [4,6,10]:add('buried-after-'+str(i),r['bank'],r['model'],dict(state),'P02')
# Two roof orders: verified historical normal routes, for the protocol figure.
mid='cottage-roof';rt,ren=engine('M',mid)
manual=json.loads((ROOT/'deliverables/brickplan-community-modules'/mid/'manual.private.json').read_text())
order=json.loads((ROOT/'deliverables/brickplan-community-modules'/mid/'order-checks.json').read_text())
# Use the route indices embedded in the gallery, which the study re-executes.
gallery=json.loads((ROOT/'deliverables/brickplan-community-modules/gallery-data.js.json').read_text())
entry=next(x for x in gallery if x['id']==mid)
for route in ['referenceOrder','alternateOrder']:
 state={a:'' for a in rt.actors}
 for i,a in enumerate(entry['orderChecks'][route],1):
  state,fb=rt.check(state,a,'attach',candidate=a+':goal');assert fb['code']=='OK'
  if i in [2,3,4,len(entry['orderChecks'][route])]:
   keys=[k for k in state.values() if k]+[k for k,r in rt.cert['candidates'].items() if r['kind']=='goal']
   add('roof-'+route+'-'+str(i),'M',mid,dict(state),'roof-detail',frame_keys=keys)
# Sanitized archived traces: state hashes checked in verify.py. They remain historical.
p=HERE/'evidence/repair-comparison.json';q=json.loads(p.read_text());sources[str(p.relative_to(ROOT))]=digest(p)
rt=PlateAssembly(q['certificate']);ren=DynamicVisionRenderer(rt.cert,rt);engines[('archive','car')]=(rt,ren)
for label,frames in [('gt',q['gt'])]+[(t['condition'],[t['frames'][i] for i in t['selectedIndices']]) for t in q['traces']]:
 for i,f in enumerate(frames):specs.append(dict(name='car-'+label+'-'+str(i),bank='archive',model='car',state=f['state'],group='car-traces',scope='historical-v5',frameKeys=None))
# One mesh per used pose; retain colors and transforms exactly.
assets={};bounds=defaultdict(list);ground=defaultdict(list)
for s in specs:
 rt,ren=engines[(s['bank'],s['model'])]
 entries={**{a:a for a in ren.cert['fixed']},**s['state']};keys=[k for k in entries.values() if k and k in ren.geometry]
 usebounds=s['frameKeys'] or keys
 bounds[s['group']].extend([ren.bounds[k]/20 for k in usebounds if k in ren.bounds])
 ground[s['group']].extend(float(ren.bounds[k][:,1].min()/20) for k in keys)
 s['meshes']=[]
 for key in keys:
  name=hashlib.sha256((s['bank']+s['model']+key).encode()).hexdigest()[:18]
  if name not in assets:
   v,c=ren.geometry[key];v=v.astype(np.float32)
   normal=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-8)
   light=np.array([.3,.8,.5]);light/=np.linalg.norm(light);shade=.6+.4*np.abs(normal@light)
   rgb=np.clip(np.rint(c.astype(float)/shade[:,None]),0,255)/255
   data=np.concatenate([v/20,np.repeat(rgb[:,None,:],3,axis=1)],axis=2).astype(np.float32)
   f=CACHE/(name+'.bin');data.tofile(f);assets[name]=dict(file=f.name,vertices=len(v)*3,sha256=digest(f))
  s['meshes'].append(name)
 s['stateSha256']=hashlib.sha256(json.dumps(s['state'],sort_keys=True).encode()).hexdigest()
for k,points in bounds.items():
 p=np.concatenate(points);groups[k]=dict(min=p.min(0).tolist(),max=p.max(0).tolist(),groundY=min(ground[k]))
 if k in ('E05','E06'):groups[k]['angles']=[195,15]
manifest=dict(schema='brickplan-publication-scenes/1',size=[3200,2400],renderer='Three.js physically shaded exact LDraw triangles',
 publicationOnly=True,evaluationInputUnchanged=True,apiCalls=0,sources=sources,assets=assets,groups=groups,scenes=specs)
(HERE/'evidence/publication-render-states.json').write_text(json.dumps({k:v for k,v in manifest.items() if k!='assets'},indent=2)+'\n')
(CACHE/'scenes.json').write_text(json.dumps(manifest,separators=(',',':')))
print('EXPORTED',len(specs),'scene states;',len(assets),'meshes;',sum((CACHE/a['file']).stat().st_size for a in assets.values())//1024//1024,'MiB',flush=True)
