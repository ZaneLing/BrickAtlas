"""Bounded, semantic LDraw finishing modules, independent of the old task snapshot.

All selected source instances have explicit roles. Complete source context and
original bytes remain retained; no nearest-neighbour extraction or invented pose.
"""
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from bench_design.challenges import QUALITY
from bench_design import ROOT
from expansion_v7.build import read,write,states_for,run_witness,signature_key,HUMAN
from expansion_v7.runtime import runtime,execute,Episode
from expansion_v7.variants import augment,pad
from expansion_v7.prepare import find_order
from community_modules.core import source_certificate
from expansion_v7.run_episode import Packet

OUT=QUALITY/'source-expansion'
REVIEW_ANGLES={'isometric':(35,30),'rear':(145,30),'left':(-55,15)}
# Source indices are hand-selected after inspecting the complete model.
SPECS=[
 ('truck-cab-30024','30024-1','小卡车：车顶和排气管',list(range(36,48)),'驾驶室顶部的盖板、两根排气管和警示灯','rotated'),
 ('reindeer-antlers-30027','30027-1','驯鹿：鹿角收尾',[54,59,60,61,62,63,64,65],'头顶两侧的鹿角和中间连接板','offset'),
 ('wreath-leaves-30028','30028-1','节日花环：顶部叶片',[30,31,35,39,40],'花环上半圈的三块斜面叶片和两颗红果','wrong-color'),
 ('excavator-cab-4915','4915-1','挖掘机：驾驶室顶盖',[49,52,53,54,55],'驾驶室支撑、顶盖、前窗和排气管','offset'),
 ('robot-head-4917','4917-1','小机器人：头部和背部喷口',[48,49,50,51,52,53,54],'头部圆顶、眼部灯和背部的两个锥形喷口','rotated'),
 ('airplane-tail-7808','7808-1','黄色飞机：驾驶舱和机头',[26,27,28,29,30,31],'驾驶舱风挡和机头两侧白色盖板','offset'),
 ('steam-engine-roof-7810','7810-1','蒸汽火车：烟囱和阀门',[12,13,14,15,21,22,23,24,87],'锅炉上方的烟囱、圆顶阀门和支撑板','wrong-color'),
 ('lion-mane-4903','4903-1','小狮子：头顶鬃毛',[16,17,18,19,22,23,24,25,26],'头部两侧鬃毛、眼睛和头顶盖板','rotated'),
 ('elephant-head-4904','4904-1','小象：额头和眼睛',[13,14,15,18,19,20],'双眼、额头斜面和头顶盖板','wrong-color'),
 ('giraffe-head-4905','4905-1','长颈鹿：头部',[35,36,37,38,39],'头顶的耳朵、连接板和双角','extra-layer'),
 ('racer-cockpit-4016','4016-1','绿色小赛车：驾驶舱与车身',[10,11,16,17,18],'底盘和车轮已装好，只补驾驶舱与后盖','wrong-part'),
 ('prop-plane-top-4019','4019-1','螺旋桨飞机：机翼与驾驶舱',[11,12,13,14,15,16],'机身和轮子已装好，补主翼、驾驶舱和尾翼','rotated'),
 ('loader-hood-1633','1633-1','小铲车：引擎盖与车灯',[6,7,9,10,11],'铲斗和底盘已装好，补引擎盖和两盏前灯','offset'),
 ('airport-kiosk-1808','1808-1','小机场：服务亭屋顶',[40,41,42,45,46],'服务亭的红色斜屋顶','wrong-color'),
]


def prepare(spec):
    mid,number,title,indices,purpose,extra=spec
    model=('v23-'+number.removesuffix('-1')) if number in ('30023-1','1633-1') else 'r-omr-'+number
    mf=read(ROOT/'web/public/models'/model/'manifest.json');md=mf['model']
    chosen=dict(id=mid,model=model,indices=indices,original=mf.get('sourceFile','assets-source/brickplan-v23/original/'+number+'.mpd'),author=md['author'],url=md.get('downloadUrl',md['sourceUrl']))
    cert=source_certificate(chosen)
    cert['source'].update(sourceSetId=number,selectionKind='named-finishing-module',selectionReason=purpose,
        completeSourceRetained=True,sourceInstancesDropped=0,license=md.get('license',cert['source']['license']))
    if not indices:raise ValueError('No explicit semantic selection')
    rt=runtime(cert);normal=find_order(rt)
    if not normal or len(normal)!=len(indices):raise ValueError('No legal complete finishing witness; source selection not admitted')
    return cert,normal,dict(id=mid,title=title,sourceSetId=number,sourceModel=chosen['model'],sourceParts=len(mf['instances']),
        activeParts=len(indices),fixedSourceParts=len(mf['instances'])-len(indices),module=purpose,
        source=cert['source'],preferredFamily=extra,humanValidated=False,completeObject=False)


def visibility(renderer,before,after):
    """Render the complete scene: an orientation matrix difference is not evidence.

    Check both the private closeup and ordinary model-input module framing. No
    pieces are hidden to make the error visible. This is a screening gate, not
    a claim of human recognition or a replacement for independent inspection.
    """
    changed={a for a in set(before)|set(after) if before.get(a,'')!=after.get(a,'')}
    keys={k for state in (before,after) for a,k in state.items() if a in changed and k}
    pts=np.concatenate([renderer.bounds[k] for k in keys]);lo,hi=pts.min(0)-28,pts.max(0)+28
    renderer.bounds['_visibility_focus']=np.array([[x,y,z] for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])
    points=np.concatenate([renderer.bounds[k] for k,r in renderer.cert['candidates'].items() if r['kind']=='goal'])
    lo,hi=points.min(0)-[20,28,20],points.max(0)+[20,20,20]
    renderer.bounds['_visibility_module']=np.array([[x,y,z] for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])
    pixels={};public={}
    for dest,angles,frame in [(pixels,REVIEW_ANGLES,'_visibility_focus'),(public,dict(isometric=None,rear=None,top=None),'_visibility_module')]:
        for name,angle in angles.items():
            a,_=renderer.rgb(before,name if angle is None else 'isometric',angles=angle,frame_keys=[frame],size=(600,450),supersample=1)
            b,_=renderer.rgb(after,name if angle is None else 'isometric',angles=angle,frame_keys=[frame],size=(600,450),supersample=1)
            dest[name]=int(np.count_nonzero(np.max(abs(np.asarray(a).astype(int)-np.asarray(b).astype(int)),axis=2)>24))
    return dict(pixels=pixels,modelInputPixels=public,visible=max(pixels.values())>=50 and max(public.values())>=50,
        thresholdChangedPixels=50,channelDifferenceThreshold=24,referenceResolution=[600,450],allSceneGeometryRetained=True)


def guard_incidents(rt):
    """Check the actual state, including legal orders different from the witness.

    Never inject an invisible replacement just because it changed a matrix.
    If no visible legal event exists yet, the ordinary trigger retries later;
    if it never triggers, evaluation retains the untriggered classification.
    """
    from dynamic_v5.vision import DynamicVisionRenderer
    from community_modules.core import render_certificate
    original=rt.incident;renderer=None
    def visible_incident(family,state,latest=None,placement_order=None,variant=0):
        nonlocal renderer
        checked=set()
        for shift in range(max(1,sum(bool(k) for a,k in state.items() if a!=latest))):
            event=original(family,state,latest=latest,placement_order=placement_order,variant=variant+shift)
            if event is None:continue
            key=json.dumps(event['after'],sort_keys=True)
            if key in checked:continue
            checked.add(key)
            if renderer is None:renderer=DynamicVisionRenderer(render_certificate(rt.cert),runtime=rt)
            evidence=visibility(renderer,event['before'],event['after'])
            if evidence['visible']:
                event.update(visibilityCheck=evidence,selectedVariant=variant+shift)
                return event
        return None
    rt.incident=visible_incident
    return rt


def build_one(spec):
    mid=spec[0];folder=OUT/'models'/mid
    base,normal,meta=prepare(spec);cert=pad(augment(base));rt=runtime(cert);states=states_for(rt,normal)
    from dynamic_v5.vision import DynamicVisionRenderer
    from community_modules.core import render_certificate
    renderer=DynamicVisionRenderer(render_certificate(cert),runtime=rt)
    cases=[];excluded=[]
    def make(mode,family,cp=0):
        return dict(id=f'QN:{mid}::{mode}::{family}',module=mid,mode=mode,family=family,
            completedInstructionStep=cp if mode=='static' else 0,initial=deepcopy(states[cp] if mode=='static' else states[0]),
            goal=deepcopy(states[cp] if mode=='static' else states[-1]),events=[],humanErrorIds=HUMAN.get(family,[]),
            protocol='brickplan-source-diversity/1',sourceSetId=meta['sourceSetId'],track='named-module')
    control=make('dynamic','control');control.update(run_witness(cert,control,normal,rt.q));cases.append(control)
    for family in ['missing',meta['preferredFamily']]:
        search=[(cp,variant) for cp in sorted(range(3,len(normal)),key=lambda x:(abs(x-len(normal)*.65),x)) for variant in range(cp)]
        for cp,variant in search:
            incident=rt.incident(family,states[cp],latest=normal[cp-1]['actor'],placement_order={a['actor']:i for i,a in enumerate(normal[:cp])},variant=variant)
            if incident is None:continue
            evidence=visibility(renderer,incident['before'],incident['after'])
            if not evidence['visible']:
                excluded.append(dict(family=family,checkpoint=cp,variant=variant,reason='not-visually-observable',evidence=evidence));continue
            dynamic=make('dynamic',family);dynamic['events']=[dict(family=family,minimumInstalled=cp,minimumActionsSincePrevious=1,humanErrorIds=HUMAN[family],variant=variant)]
            try:dynamic.update(run_witness(cert,dynamic,normal,rt.q))
            except AssertionError:continue
            actual=dynamic['referenceEvents'][0]
            actual_visibility=visibility(renderer,actual['before'],actual['after'])
            if not actual_visibility['visible']:continue
            static=make('static',family,cp);static['initial']=deepcopy(actual['after']);static['goal']=deepcopy(actual['before'])
            end,checks=execute(rt,static['initial'],actual['recovery'])
            assert end==static['goal']
            static.update(referenceActions=actual['recovery'],referenceIncident=actual,referenceChecks=checks,
                legalWitnessOnly=True,humanValidated=False,modelEvaluated=False)
            for c in (static,dynamic):c['visibilityCheck']=actual_visibility
            cases.extend([static,dynamic]);break
        else:raise ValueError('No legal '+family+' incident; no partial model admitted')
    assert len(cases)==5
    for c in cases:c['physicalTaskSha256']=signature_key(rt,c)
    write(folder/'certificate.private.json.gz',cert);write(folder/'manual.private.json.gz',dict(actions=normal,states=states))
    meta['rejectedInvisibleIncidents']=excluded
    write(folder/'cases.private.json.gz',cases);write(folder/'metadata.json',meta)
    return meta,cases


@lru_cache(maxsize=1)
def index():return read(OUT/'index.json')


def source_row(cid):
    row=next(r for r in index()['cases'] if r['id']==cid);folder=OUT/'models'/row['model']
    c=next(c for c in read(folder/'cases.private.json.gz') if c['id']==cid)
    return dict(key=cid,bank='QN',model=row['model'],title=row['title'],mode=c['mode'],family=c['family'],case=c,
        evaluationMetadata=dict(canonicalId=cid,taskType='S1' if c['mode']=='static' else 'D0' if not c['events'] else 'D1',
            track='named-module-'+c['mode'],source='set:'+c['sourceSetId'].split('-')[0],model=row['model'],
            normalCanonicalId=f'QN:{row["model"]}::dynamic::control'))


def load(cid,directory):
    row=source_row(cid);folder=OUT/'models'/row['model'];cert=read(folder/'certificate.private.json.gz')
    ep=Episode(cert,row['case'],41);guard_incidents(ep.runtime)
    packet=Packet(ep,read(folder/'manual.private.json.gz'),directory)
    return row,ep,packet,None


def main():
    p=argparse.ArgumentParser();p.add_argument('--only');args=p.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    previous=read(OUT/'index.json') if (OUT/'index.json').exists() else dict(models=[],cases=[],rejected=[])
    for spec in SPECS:
        if args.only and args.only!=spec[0]:continue
        if any(r['id']==spec[0] for r in previous['models']):continue
        print('PREPARE',spec[0],flush=True)
        try:
            meta,cases=build_one(spec);previous['models'].append(meta)
            previous['cases'].extend(dict(id=c['id'],model=meta['id'],title=meta['title'],mode=c['mode'],family=c['family']) for c in cases)
            print('ADMITTED',spec[0],meta['activeParts'],len(cases),flush=True)
            previous['rejected']=[r for r in previous['rejected'] if r['id']!=spec[0]]
        except Exception as e:
            cause=e
            while cause.__cause__ is not None:cause=cause.__cause__
            previous['rejected'].append(dict(id=spec[0],reason=str(e)+'; '+str(cause)));print('REJECTED',spec[0],e,cause,flush=True)
        previous.update(apiCalls=0,addedToPublishedSnapshot=False,maxCasesPerSource=5,humanValidated=False)
        write(OUT/'index.json',previous)
    # One static and one dynamic example per object, arranged by source, not many variants of the same object.
    tasks=[]
    for mode in ['static','dynamic']:
        for i,meta in enumerate(previous['models']):
            row=next(c for c in previous['cases'] if c['model']==meta['id'] and c['mode']==mode and c['family']==meta['preferredFamily'])
            tasks.append(dict(code=f'N{(0 if mode=="static" else 100)+i+1:03}',caseId=row['id'],mode=mode,isNew=True))
    write(OUT/'review-tasks.json',dict(tasks=tasks))


if __name__=='__main__':main()
