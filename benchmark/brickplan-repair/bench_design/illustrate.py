"""Native geometry comparisons for the classification guide, not generated art."""
from collections import Counter
import json
import numpy as np
from bench_design import OUT,ROOT
from bench_design.catalogue import rows_with_cases,module_runtime
from expansion_v7.build import read,write
from expansion_v7.runtime import Episode,public_action
from community_modules.core import render_certificate
from community_modules.run_episode import PALETTE
from dynamic_v5.vision import DynamicVisionRenderer
from matched_canvas import comparison
import re


def main():
    rows=rows_with_cases();assets=OUT/'assets';assets.mkdir(parents=True,exist_ok=True)
    PALETTE.update(dict(re.findall(r'CODE\s+(\d+)\s+VALUE\s+(#[0-9A-Fa-f]{6})',
        (ROOT/'assets-source/ldraw-library/locked/LDConfig.ldr').read_text())))
    selections=[]
    for code,family in [('E01','missing'),('E02','extra-layer'),('E03','wrong-color'),('E04','wrong-part'),('E05','offset'),('E06','rotated')]:
        selections.append((code,next(r for r in rows if r['bank']=='O' and r['model']=='whole-4037' and r['mode']=='static' and r['family']==family)))
    for code,family,mid in [('E07','left-right-swap','v7-long-city-bus'),('P01','early-cover','v7-long-bookshelf'),('P02','buried-repair','v7-long-bookshelf')]:
        selections.append((code,next(r for r in rows if r['bank']=='E7' and r['model']==mid and r['mode']=='static' and r['family']==family)))
    selections.append(('OK',next(r for r in rows if r['bank']=='O' and r['model']=='whole-4037' and r['mode']=='static' and r['family']=='control')))
    examples=[]
    for code,row in selections:
        rt=module_runtime(row['bank'],row['model']);c=row['case']
        renderer=DynamicVisionRenderer(render_certificate(rt.cert),rt)
        pts=np.concatenate([renderer.bounds[k] for k,r in rt.cert['candidates'].items() if r['kind']=='goal'])
        lo,hi=pts.min(0)-[20,28,20],pts.max(0)+[20,20,20]
        renderer.bounds['_module_frame']=np.array([[x,y,z] for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])
        im=comparison(renderer,c['initial'],c['goal'],'isometric','CURRENT NOW','TARGET: REQUIRED STAGE',frame_keys=['_module_frame'])
        path=assets/(code+'.png');im.save(path)
        source_root='brickplan-recognizable-models' if row['bank']=='O' else 'brickplan-expansion-v7'
        ep=Episode(read(ROOT/'deliverables'/source_root/'models'/row['model']/'certificate.private.json.gz'),c,41)
        actions=[public_action(ep,a) for a in c['referenceActions']]+[{'type':'finish'}]
        examples.append(dict(code=code,id=row['key'],title=row['title'],family=row['family'],
            image=str(path.relative_to(OUT)),targetStage=c['completedInstructionStep'],
            totalParts=len(rt.cert['source']['moduleSourceIndices']),referenceActions=actions,
            requiredReferenceOrder=False,referenceNotModelPerformance=True,
            instructions='The right image is the sole required stage target; the complete object reference does not replace it.'))
        print('ILLUSTRATED',code,row['model'],flush=True)
    write(OUT/'examples.json',examples)


if __name__=='__main__':main()
