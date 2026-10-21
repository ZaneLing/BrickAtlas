"""Offline visual pipeline audit; representative cases, not an accuracy experiment."""
from pathlib import Path
import json,time
import numpy as np
from PIL import Image
from protocol import Episode,load
from vision import VisionRenderer,qualify,images,observe,request_body,SIZE
from render import Renderer
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'deliverables/brickplan-visual-input-v3'
rows=[json.loads(l) for l in (ROOT/'deliverables/brickplan-repair-library/cases.jsonl').read_text().splitlines()]
selected=[]
for kind in sorted({c['kind'] for c in rows}):
    pool=[c for c in rows if c['kind']==kind]
    # Freeze before auditing any pixels: smallest action count, except hardest compound.
    chosen=sorted(pool,key=lambda c:(-c['expectedOptimum'] if kind=='compound' else c['expectedOptimum'],c['id']))[0]
    selected.append(chosen)
report=[];started=time.time()
for case in selected:
    cert,_=load(case['modelId']);ep=Episode(cert,case,protocol_version='v3');renderer=VisionRenderer(cert)
    admission=qualify(ep,renderer)
    im,mask=renderer.rgb(ep.assignments());_,old=Renderer(cert).render(ep.assignments(),size=(384,288))
    yy,xx=np.where(mask);oy,ox=np.where(old)
    row={'caseId':case['id'],'modelId':case['modelId'],'kind':case['kind'],'admission':admission,
         'oldViewSize':[384,288],'newViewSize':list(SIZE),
         'oldObjectBoundingBox':[int(np.ptp(ox)+1),int(np.ptp(oy)+1)],
         'newObjectBoundingBox':[int(np.ptp(xx)+1),int(np.ptp(yy)+1)]}
    assert admission['passed'],row
    assert min(xx)>0 and max(xx)<SIZE[0]-1 and min(yy)>0 and max(yy)<SIZE[1]-1,row
    if case['kind']=='compound':
        folder=OUT/'compound';folder.mkdir(exist_ok=True)
        im.save(folder/'views-current.png');renderer.rgb(ep.case['goal'])[0].save(folder/'views-target.png')
        records=images(ep,renderer,folder)
        req=request_body('YOUR_VISION_MODEL',observe(ep),records,folder)
        for item,record in zip([x for x in req['messages'][1]['content'] if x['type']=='image_url'],records):item['image_url']['url']=record['file']
        (folder/'views.readable.json').write_text(json.dumps({'displayOnly':True,'request':req},ensure_ascii=False,indent=2)+'\n')
    report.append(row);print(case['kind'],'passed',flush=True)
counts=[]
for model in json.loads((ROOT/'deliverables/brickplan-repair-library/index.json').read_text())['models']:
    cert,_=load(model['modelId']);n=len({c['actor'] for c in cert['candidates'].values()});counts.append(n)
result={'protocol':'visual-rgb-v3','apiCalls':0,'casesChecked':len(report),'allPassed':True,'seconds':round(time.time()-started,2),
        'maxActorsAcrossBank':max(counts),'maximumImagesPerRequest':6+(max(counts)+11)//12+2,
        'scope':'Representative pipeline and uniform-inspection visibility audit; not full-bank qualification or measured VLM accuracy.', 'rows':report}
assert result['maximumImagesPerRequest']<=16
(OUT/'quality-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
