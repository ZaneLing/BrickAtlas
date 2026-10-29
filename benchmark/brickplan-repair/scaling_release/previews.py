"""True source renders: overall context, highlighted scope, matched close views."""
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import argparse,json,traceback,hashlib
import numpy as np
from PIL import Image,ImageFilter
from scaling_release import ROOT,OUT
from expansion_v7.build import read,write

def one(number):
 from expansion_v7.runtime import runtime
 from dynamic_v5.vision import DynamicVisionRenderer
 from dynamic_arena.plate_render import ArenaVision
 from community_modules.core import render_certificate
 from render import PALETTE
 import re
 folder=OUT/'private'/number;dest=OUT/'previews'/number;dest.mkdir(parents=True,exist_ok=True)
 stamp=hashlib.sha256((folder/'certificate.private.json.gz').read_bytes()+(folder/'cases.private.json.gz').read_bytes()+Path(__file__).read_bytes()).hexdigest()
 if (dest/'complete.json').exists() and read(dest/'complete.json').get('inputSha256')==stamp:return number,'cached'
 cert=read(folder/'certificate.private.json.gz');cases=read(folder/'cases.private.json.gz');rt=runtime(cert)
 PALETTE.update(dict(re.findall(r'CODE\s+(\d+)\s+VALUE\s+(#[0-9A-Fa-f]{6})',(ROOT/'assets-source/ldraw-library/locked/LDConfig.ldr').read_text())))
 ren=ArenaVision(cert,rt) if hasattr(rt,'baseplate') else DynamicVisionRenderer(render_certificate(cert),rt)
 selected=[k for k,r in cert['candidates'].items() if r['kind']=='goal']
 pts=np.concatenate([ren.bounds[k] for k in selected]);lo,hi=pts.min(0)-[20,28,20],pts.max(0)+[20,20,20]
 ren.bounds['_release_frame']=np.array([[x,y,z] for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])
 frame=['_release_frame'];control=next(c for c in cases if c['mode']=='dynamic' and c['family']=='control');static=next(c for c in cases if c['mode']=='static')
 full,mask=ren.rgb(control['goal'],'isometric',size=(900,675),supersample=1)
 movable=[ren.ids[r['actor']] for k,r in cert['candidates'].items() if k in selected]
 mask=Image.fromarray(np.uint8(np.isin(mask,movable))*255)
 border=Image.fromarray(np.uint8(np.maximum(0,np.asarray(mask.filter(ImageFilter.MaxFilter(5))).astype(int)-np.asarray(mask).astype(int))))
 full.paste((0,151,164),(0,0),border);full.save(dest/'overview.png')
 roles={'initial':control['initial'],'target':control['goal'],'static-current':static['initial'],'static-target':static['goal']}
 for name,state in roles.items():
  for view in ['isometric','rear','top']:
   ren.rgb(state,view,size=(800,600),supersample=1,frame_keys=frame)[0].save(dest/f'{name}-{view}.png')
 from scaling_release.static_bank import asset_key
 for s in (c for c in cases if c['mode']=='static'):
  target=dest/'static'/asset_key(s['id']);target.mkdir(parents=True,exist_ok=True)
  for role,state in [('static-current',s['initial']),('static-target',s['goal'])]:
   for view in ['isometric','rear','top']:
    ren.rgb(state,view,size=(800,600),supersample=1,frame_keys=frame)[0].save(target/f'{role}-{view}.png')
 for c in cases:
  for i,e in enumerate(c.get('referenceEvents',[])):
   for role in ['before','after']:
    ren.rgb(e[role],'isometric',size=(800,600),supersample=1,frame_keys=frame)[0].save(dest/f'{c["family"]}-event-{i+1}-{role}.png')
 write(dest/'complete.json',dict(inputSha256=stamp,sourceGeometryModified=False,sameCanvasAndCamera=True,overviewCyan='selected task scope, not an error hint',eventImages='private witness illustration for human review only; never initial model observation'))
 return number,'rendered'

def main():
 p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=3);a=p.parse_args()
 rows=[p.parent.name for p in (OUT/'private').glob('*/cases.private.json.gz')]
 failures=[]
 with ProcessPoolExecutor(max_workers=a.workers) as pool:
  futures={pool.submit(one,r):r for r in rows}
  for f in as_completed(futures):
   try:n,status=f.result();print('IMAGE',n,status,flush=True)
   except Exception as e:failures.append(dict(model=futures[f],reason=str(e)));print('IMAGE FAIL',futures[f],str(e)[:150],flush=True)
 write(OUT/'checks/preview-check.json',dict(checked=len(rows),failures=failures,passed=not failures))

if __name__=='__main__':main()
