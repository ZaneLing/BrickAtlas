"""Promote complete small OMR sources only after legal full-build and repair replay."""
from pathlib import Path
from copy import deepcopy
import argparse,hashlib,json
from dynamic_arena import ROOT,OUT
from expansion_v7.build import read,write,states_for,run_witness,HUMAN
from recognizable_models.intake import ingest
from recognizable_models.prepare import complete_certificate
from expansion_v7.prepare import find_order
from expansion_v7.runtime import runtime,Episode
from expansion_v7.run_episode import Packet

DEST=OUT/'new-objects'


def qualify(row):
    number=row['setNumber'];mid='arena-'+number;folder=DEST/mid
    ingest(dict(set=number,file=row['sourceFile'],title=row['title'],pageUrl=row['sourceUrl'],url=row['downloadUrl'],sha256=row['sourceHash']))
    spec=dict(id=mid,model='r-omr-'+number,title=row['title'])
    cert,mf=complete_certificate(spec);rt=runtime(cert);normal=find_order(rt)
    if not normal:raise ValueError('No legal complete assembly witness found; source retained, task withheld')
    states=states_for(rt,normal)
    def case(family):return dict(id=f'A4:{mid}::{family}',module=mid,mode='dynamic',family=family,initial=deepcopy(states[0]),goal=deepcopy(states[-1]),events=[],completedInstructionStep=0,humanErrorIds=HUMAN.get(family,[]),sourceSetId=number,protocol='arena-source-whole/1',track='whole-object')
    control=case('control');control.update(run_witness(cert,control,normal,rt.q))
    incident=case('missing');found=None
    for cp in range(max(2,len(normal)//2),len(normal)):
        trial=deepcopy(incident);trial['events']=[dict(family='missing',minimumInstalled=cp,minimumActionsSincePrevious=1,humanErrorIds=HUMAN['missing'],variant=0)]
        try:trial.update(run_witness(cert,trial,normal,rt.q))
        except (AssertionError,ValueError):continue
        if trial.get('referenceEvents'):found=trial;break
    if not found:raise ValueError('No legal triggered-and-recovered missing-part witness')
    from dynamic_v5.vision import DynamicVisionRenderer
    from bench_design.source_expansion import visibility
    renderer=DynamicVisionRenderer(rt.cert,rt)
    event=found['referenceEvents'][0];evidence=visibility(renderer,event['before'],event['after'])
    if not evidence['visible']:raise ValueError('Error insufficiently visible at model-input size')
    found['visibilityCheck']=evidence
    write(folder/'certificate.private.json.gz',cert);write(folder/'manual.private.json.gz',dict(actions=normal,states=states));write(folder/'cases.private.json.gz',[control,found])
    meta=dict(id=mid,sourceLibraryId=row['id'],setNumber=number,title=row['title'],parts=len(normal),sourceHash=row['sourceHash'],sourceUrl=row['sourceUrl'],completeObject=True,allSourcePartsOperable=True,sourceInstancesDropped=0,normalBuildVerified=True,repairVerified=True,humanQualified=False,apiModelEvaluated=False)
    write(folder/'metadata.json',meta);return meta


def load(cid,directory):
    mid=cid.split(':')[1];folder=DEST/mid;meta=read(folder/'metadata.json');case=next(c for c in read(folder/'cases.private.json.gz') if c['id']==cid)
    cert=read(folder/'certificate.private.json.gz');ep=Episode(cert,case,41)
    from bench_design.source_expansion import guard_incidents
    guard_incidents(ep.runtime)
    packet=Packet(ep,read(folder/'manual.private.json.gz'),directory)
    row=dict(key=cid,bank='A4',model=mid,title=meta['title'],mode='dynamic',case=case,family=case['family'],evaluationMetadata=dict(canonicalId=cid,taskType='D0' if not case['events'] else 'D1',track='whole-object-dynamic',source='set:'+meta['setNumber'].split('-')[0],model=mid))
    return row,ep,packet,None


def main():
    p=argparse.ArgumentParser();p.add_argument('--limit',type=int,default=16);a=p.parse_args();index=DEST/'index.json'
    data=read(index) if index.exists() else dict(models=[],rejected=[],apiCalls=0)
    seen={r['setNumber'] for r in data['models']}|{r['setNumber'] for r in data['rejected']}
    rows=[r for r in read(OUT/'source-library.json')['models'] if r['id'].startswith('arena-omr-') and r['setNumber'] not in seen and r['parts']<=50 and not any(w in r['title'].lower() for w in ['figure','fabuland'])]
    for r in rows[:a.limit]:
        print('QUALIFY',r['setNumber'],r['title'],flush=True)
        try:meta=qualify(r);data['models'].append(meta);print('ADMITTED',r['setNumber'],flush=True)
        except Exception as e:
            cause=e
            while cause.__cause__ is not None:cause=cause.__cause__
            data['rejected'].append(dict(setNumber=r['setNumber'],reason=str(e)+'; '+str(cause)));print('WITHHELD',r['setNumber'],str(cause)[:180],flush=True)
        write(index,data)


if __name__=='__main__':main()
