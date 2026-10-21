"""Offline visual input export; never calls a provider or reads credentials."""
import argparse
from copy import deepcopy
import json,sys,shutil
from pathlib import Path
from protocol import Episode,load
from vision import VisionRenderer,observe,images,request_body,VERSION
from render import VIEWS
ROOT=Path(__file__).resolve().parents[3]
def dump(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def export(model,case_id,out):
    cert,cases=load(model);case=cases[case_id]
    ep=Episode(cert,case,seed=41,protocol_version='v3');renderer=VisionRenderer(cert)
    out.mkdir(parents=True,exist_ok=True)
    observation=observe(ep);records=images(ep,renderer,out)
    request=request_body('YOUR_VISION_MODEL',observation,records,out)
    dump(out/'views.observation.json',observation);dump(out/'views.request.json',request)
    readable=deepcopy(request)
    refs=iter(records)
    for item in readable['messages'][1]['content']:
        if item['type']=='image_url':item['image_url']['url']=next(refs)['file']
    dump(out/'views.readable.json',{'displayOnly':True,'request':readable})
    for r in records:
        if r['role'] in ('current','target') and r.get('view')=='isometric':
            shutil.copyfile(out/r['file'],out/f"views-{r['role']}.png")
        if r['role']=='inventory':shutil.copyfile(out/r['file'],out/f"inventory-{r['page']}.png")
    # Extra camera samples are offline review files, not silently appended to the request.
    extra=[]
    for view in VIEWS:
        for role,state in [('current',ep.assignments()),('target',ep.case['goal'])]:
            file=f'{role}-{view}.png';renderer.rgb(state,view)[0].save(out/file)
            extra.append({'file':file,'role':role,'view':view,'width':1600,'height':1200})
    dump(out/'manifest.json',{'protocol':VERSION,'caseId':case_id,'modelId':model,'apiCalls':0,
         'requestImages':records,'offlineAllViews':extra,'requestReconstructed':True,
         'nativeRenderSize':[3200,2400],'deliveredSceneSize':[1600,1200],'supersampling':2,
         'mainSceneLabels':False,'pngLossless':True,'inventoryLabels':'caption strips only',
         'textTrackEnabled':False,'oldResultsComparable':False})
    print(json.dumps({'out':str(out),'requestImages':len(records),'apiCalls':0}),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model',default='10001');p.add_argument('--case',default='10001:height_layer:a65ccf24');p.add_argument('--out',type=Path,default=ROOT/'deliverables/brickplan-visual-input-v3');args=p.parse_args();export(args.model,args.case,args.out)
