"""Additive, source-preserving stress conditions; pending independent admission.

These do not silently increase the published 5,720-task snapshot. Every retained
new condition has an executed witness, including incidents inside ongoing repair.
"""
from copy import deepcopy
from pathlib import Path
import argparse
import hashlib
from bench_design import ROOT
from bench_design.policy import descriptors, tags
from expansion_v7.build import read, write, HUMAN, digest
from expansion_v7.runtime import Episode, public_action
from expansion_v7.scope import allowed

QUALITY = ROOT/'deliverables/brickplan-quality-round'
MODELS = ['v7-long-bookshelf','v7-long-city-bus','v7-long-stone-bridge',
          'v7-long-gantry-press','v7-long-cottage','museum-roof-long',
          'cottage-roof','racer-top','seaplane-tail','repair-truck-cab',
          'panda-head','burger-stand-roof','white-house-roof',
          'police-helicopter-top','rockefeller-crown','brandenburg-top',
          'orange-helicopter-tail']
PATTERNS = [
    ('repair-overlap', ['offset','extra-layer'], '第二次事故发生在第一次修复尚未完成时', 1),
    ('buried-overlap', ['buried-repair','wrong-color'], '拆开上层返修时又出现新错误', 1),
    ('three-incidents', ['missing','wrong-color','offset'], '连续三次不同事故，修好后继续完成', 2),
    ('late-repair', ['wrong-part','missing'], '接近完成时发现错件并再次缺件', 2),
    ('repeated-color', ['wrong-color','wrong-color'], '修好后再次出现同类错误', 3),
    ('orientation-repair', ['rotated','missing'], '方向异常与后续缺件的连续修复', 2),
    ('access-replanning', ['early-cover','missing'], '提前封口后重新安排安装路线', 1),
    ('swap-repair', ['left-right-swap'], '可交换位置的不同零件被互换', 1),
]


def witness(cert, case, normal, qualifier=None):
    ep=Episode(cert,case,41)
    if qualifier is not None:ep.runtime.q=qualifier
    queue=deepcopy(normal);actions=[];seen=0
    while queue and len(actions)<240:
        action=queue.pop(0);actor=action['actor'];current=ep.state.get(actor)
        if action['type']=='detach' and not current:continue
        if action['type']=='attach' and current==action['candidate']:continue
        if action['type']=='attach' and current:
            queue.insert(0,action);action=dict(type='detach',actor=actor)
        ep.step(public_action(ep,action));actions.append(action)
        if ep.feedback['code']!='OK':raise ValueError('witness-rejected:'+ep.feedback['code'])
        if len(ep.events)>seen:
            incident=ep.events[-1];seen=len(ep.events)
            queue=deepcopy(incident['recovery'])+queue
    if queue:raise ValueError('witness-move-cap')
    ep.step(dict(type='finish'))
    if not ep.score()['success']:raise ValueError('witness-final-incomplete')
    if len(ep.events)!=len(case['events']):raise ValueError('not-all-events-triggered')
    # Count an incident within the previous event's still-unrepaired window.
    overlap=False
    for a,b in zip(ep.events,ep.events[1:]):
        goal=ep.runtime.signature(case['goal']);old=ep.runtime.signature(a['before'])
        changed=ep.runtime.signature(a['after']);current=ep.runtime.signature(b['before'])
        lost=(old&goal)-changed;excess=(changed-goal)-(old-goal)
        if any(current[k]<(old&goal)[k] for k in lost) or any((current-goal)[k]>(old-goal)[k] for k in excess):
            overlap=True
    return dict(referenceActions=actions,referenceEvents=deepcopy(ep.events),
                referenceScore=ep.score(),actualOverlapDuringUnrepairedWindow=overlap)


def build(limit=48):
    QUALITY.mkdir(parents=True,exist_ok=True)
    candidates=[];rejected=[];seen=set();sources={}
    import json
    published=[json.loads(x) for x in (ROOT/'deliverables/brickplan-benchmark-spec/questions.jsonl').read_text().splitlines()]
    # Round-robin over the models prevents one convenient object filling the bank.
    prepared=[]
    for mid in MODELS:
        folder=ROOT/'deliverables/brickplan-expansion-v7/models'/mid
        cert=read(folder/'certificate.private.json.gz');manual=read(folder/'manual.private.json.gz')
        cases=read(folder/'cases.private.json.gz')
        base=next(c for c in cases if c['mode']=='dynamic' and not c['events'])
        from expansion_v7.runtime import runtime
        prepared.append((mid,folder,cert,manual,base,runtime(cert).q))
        sources[mid]={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in [folder/'certificate.private.json.gz',folder/'manual.private.json.gz']}
    for pi,(label,families,why,gap) in enumerate(PATTERNS):
        accepted_category=0
        shift=(pi*2)%len(prepared)
        for mid,folder,cert,manual,base,qualifier in prepared[shift:]+prepared[:shift]:
            if len(candidates)>=limit:break
            if accepted_category>=max(1,limit//len(PATTERNS)):break
            n=sum(bool(k) for k in base['goal'].values())
            cp=max(3,min(n-1,7 if families[0]=='buried-repair' else n-2 if label=='late-repair' else max(3,n//3)))
            case=deepcopy(base)
            case.update(id='quality::'+mid+'::'+label, family='multiple-'+'then-'.join(families) if len(families)>1 else families[0],
                        events=[dict(family=f,minimumInstalled=cp if i==0 else max(2,cp-2),
                                     minimumActionsSincePrevious=1 if i==0 else gap,
                                     humanErrorIds=HUMAN[f],variant=(pi+i)%3) for i,f in enumerate(families)],
                        humanErrorIds=sorted({h for f in families for h in HUMAN[f]}),
                        legalWitnessOnly=True,humanValidated=False,modelEvaluated=False)
            assert allowed(case)
            for key in ['referenceActions','referenceEvents','referenceScore','physicalTaskSha256']:
                case.pop(key,None)
            try:
                measured=witness(cert,case,manual['actions'],qualifier)
                if label in ('repair-overlap','buried-overlap') and not measured['actualOverlapDuringUnrepairedWindow']:
                    raise ValueError('second-incident-was-not-inside-unrepaired-window')
                fingerprint=digest(dict(model=mid,initial=case['initial'],goal=case['goal'],schedule=case['events'],
                    effects=[(e['atManipulation'],e['before'],e['after']) for e in measured['referenceEvents']]))
                if fingerprint in seen:raise ValueError('duplicate-stress-condition')
                seen.add(fingerprint);case.update(measured)
                key='QX:'+case['id'];moves=max(len(e['recovery']) for e in case['referenceEvents'])
                covers=max(len(e.get('temporarilyRemovedCorrectParts',[])) for e in case['referenceEvents'])
                codes,name=tags(case['family'])
                metadata=dict(canonicalId=key,taskType='D2' if len(families)>1 else 'D1',
                    track='whole-object-dynamic' if mid.startswith('v7-long-') else 'named-module-dynamic',
                    source=next(r['source'] for r in published if r['model']==mid),model=mid,
                    normalCanonicalId=next(r['canonicalId'] for r in published if r['model']==mid and r['taskType']=='D0'))
                candidates.append(dict(id=key,model=mid,category=label,purpose=why,case=case,
                    evaluationMetadata=metadata,errorCodes=codes,
                    descriptors=descriptors(n,moves,covers,len(families),case['family']),
                    certificate=str((folder/'certificate.private.json.gz').relative_to(ROOT)),
                    manual=str((folder/'manual.private.json.gz').relative_to(ROOT)),
                    conditionSha256=fingerprint,releaseStatus='pending-human-and-independent-qualification'))
                accepted_category+=1
                print('ADDED',len(candidates),mid,label,flush=True)
            except (ValueError,AssertionError,KeyError) as exc:
                rejected.append(dict(model=mid,category=label,reason=str(exc)[:220]))
                print('NOT ADMITTED',mid,label,str(exc)[:80],flush=True)
    write(QUALITY/'challenges.private.json.gz',dict(schema='brick-atlas-targeted-stress/1',cases=candidates))
    public=[{k:v for k,v in c.items() if k not in ('case','certificate','manual')} for c in candidates]
    write(QUALITY/'challenge-catalogue.json',dict(cases=public,count=len(public),existingPublishedTasks=5720,
        addedToPublishedSnapshot=False,humanQualified=False,apiCalls=0))
    write(QUALITY/'challenge-generation.json',dict(accepted=len(candidates),rejected=rejected,sources=sources,
        witnessOnly=True,independentGeometryQualified=False,humanQualified=False,apiCalls=0))
    return candidates


def load_challenge(case_id,directory):
    item=next(c for c in read(QUALITY/'challenges.private.json.gz')['cases'] if c['id']==case_id)
    cert=read(ROOT/item['certificate']);case=deepcopy(item['case'])
    ep=Episode(cert,case,41)
    from expansion_v7.run_episode import Packet
    packet=Packet(ep,read(ROOT/item['manual']),directory)
    if cert.get('environmentMode')!='white-baseplate':
        import numpy as np
        keys=list(packet.renderer.cert['fixed'])+[k for k,r in cert['candidates'].items() if r['kind']=='goal']
        packet.renderer.bounds['_module_frame']=np.concatenate([packet.renderer.bounds[k] for k in keys])
    row=dict(key=case_id,bank='E7',model=item['model'],case=case,mode='dynamic',
             evaluationMetadata=item['evaluationMetadata'])
    return row,ep,packet,None


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--limit',type=int,default=48)
    build(parser.parse_args().limit)
