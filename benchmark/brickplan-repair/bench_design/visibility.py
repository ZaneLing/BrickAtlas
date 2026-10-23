"""Pixel-change checks for the 46 new complete-object conditions, same camera."""
import numpy as np
from bench_design import OUT,ROOT
from expansion_v7.build import read,write
from expansion_v7.runtime import runtime
from community_modules.core import render_certificate
from dynamic_v5.vision import DynamicVisionRenderer


def main():
    rows=[];root=ROOT/'deliverables/brickplan-recognizable-models'
    for meta in read(root/'admission-screen.json')['admitted']:
        folder=root/'models'/meta['id'];cert=read(folder/'certificate.private.json.gz');rt=runtime(cert)
        renderer=DynamicVisionRenderer(render_certificate(rt.cert),rt)
        pts=np.concatenate([renderer.bounds[k] for k,r in rt.cert['candidates'].items() if r['kind']=='goal'])
        lo,hi=pts.min(0)-[20,28,20],pts.max(0)+[20,20,20]
        renderer.bounds['_module_frame']=np.array([[x,y,z] for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])
        cache={}
        def rgb(state,view):
            key=(tuple(sorted(state.items())),view)
            if key not in cache:cache[key]=np.asarray(renderer.rgb(state,view,size=(800,600),supersample=1,frame_keys=['_module_frame'])[0]).astype(np.int16)
            return cache[key]
        for c in read(folder/'cases.private.json.gz'):
            event=(c.get('referenceEvents') or [c.get('referenceIncident')])[0]
            if not event:
                rows.append(dict(id='O:'+c['id'],status='control',humanValidated=False));continue
            delta={v:int(np.count_nonzero(np.max(np.abs(rgb(event['before'],v)-rgb(event['after'],v)),axis=2)>=24)) for v in ('isometric','rear','top')}
            rows.append(dict(id='O:'+c['id'],status='machine-visible' if max(delta.values())>=128 else 'low-visibility',
                changedPixels=delta,minimumPixels=128,pixelThreshold=24,scenePixels=[800,600],humanValidated=False,
                actualPolicyRouteMustBeRechecked=True))
    write(OUT/'new-object-visibility.json',dict(rows=rows,cases=len(rows),apiCalls=0,
        scope='Reference incident images only. Pixel difference does not certify human readability or detection ability.'))
    print('VISIBILITY',len(rows),sum(r['status']=='machine-visible' for r in rows),'visible',flush=True)


if __name__=='__main__':main()
