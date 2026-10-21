"""Compare actual faulty and goal RGB; qualify every defect under uniform inspection."""
import json,sys,time
from pathlib import Path
import numpy as np
from render import Renderer,VIEWS
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from static_bench import OUT,dump,aggregate
start=time.time();rows=[]
for folder in sorted((OUT/'models').iterdir()):
    if not (folder/'record.json').exists():continue
    cases=json.loads((folder/'cases.json').read_text());cert=json.loads((folder/'qualification.json').read_text())
    r=Renderer(cert);cache={}
    def pixels(actor,key,view):
        sig=(actor,key,view)
        if sig not in cache:cache[sig]=np.array(r.render({actor:key},view,(256,192),only=actor)[0]).astype('int16')
        return cache[sig]
    for c in cases.values():
        rootrows=[]
        for root in c['roots']:
            evidence=[]
            for actor in root['affectedActors']:
                for view in VIEWS:
                    diff=np.max(np.abs(pixels(actor,c['initial'][actor],view)-pixels(actor,c['goal'][actor],view)),axis=2)
                    count=int(np.count_nonzero(diff>=24))
                    evidence.append({'actor':actor,'view':view,'changedPixels':count})
            best=max(evidence,key=lambda e:e['changedPixels'])
            rootrows.append({'type':root['type'],'best':best,'observable':best['changedPixels']>=24})
        eligible=all(row['observable'] for row in rootrows)
        c['observation'].update(visualEligibility='verified' if eligible else 'excluded_visually_ambiguous',
              evaluationAdapterConnected=True,track='multiview_with_uniform_piece_inspection',
              reason='每处错误在统一单件检查下存在可辨像素差异。' if eligible else '至少一处姿态差异在七视图单件检查中仍不可辨；不计入视觉赛道。',
              actualStatePixelAudit={'resolution':[256,192],'rgbThreshold':24,'minimumChangedPixels':24,'roots':rootrows,
                'scope':'Uniform isolated-piece observation, no fault-based highlighting. Does not assert every error is visible in exterior views.'})
        c['tags']=[x for x in c['tags'] if x not in ('visual_unverified','visual_ambiguous')]
        if not eligible:c['tags'].append('visual_ambiguous')
        rows.append({'id':c['id'],'model':folder.name,'kind':c['kind'],'eligible':eligible,'roots':rootrows})
    dump(folder/'cases.json',cases)
    print(folder.name,len(cases),sum(not row['eligible'] for row in rows),'excluded cumulative',flush=True)
report={'schema':'brickplan-actual-rgb-admission/1','cases':len(rows),'admitted':sum(r['eligible'] for r in rows),
        'excluded':sum(not r['eligible'] for r in rows),'seconds':round(time.time()-start,1),
        'track':'multiview_with_uniform_piece_inspection','rows':rows}
dump(OUT/'visual-admission.json',report);aggregate()
print(json.dumps({k:v for k,v in report.items() if k!='rows'}),flush=True)
