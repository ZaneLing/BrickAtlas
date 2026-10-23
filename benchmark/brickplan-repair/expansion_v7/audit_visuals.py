"""Exact-interface renders, machine visibility, and provisional structural groups."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image
from expansion_v7 import OUT
from expansion_v7.build import read,write
from expansion_v7.runtime import Episode
from expansion_v7.run_episode import Packet
from matched_canvas import comparison,panels

VIEWS=('isometric','rear','top')


def profile(meta, case, visibility):
    events=case.get('referenceEvents',[]) or ([case['referenceIncident']] if case.get('referenceIncident') else [])
    repair_moves=max((len(e['recovery']) for e in events),default=0)
    covers=max((len(e.get('temporarilyRemovedCorrectParts',[])) for e in events),default=0)
    active=meta['activeParts'];target_parts=sum(bool(k) for k in case['goal'].values())
    event_count=len(case.get('events',[]));length=active if case['mode']=='dynamic' else target_parts
    signals=[]
    if length>=20:signals.append('20 or more build/target parts')
    if covers:signals.append('must remove otherwise-correct cover in the certified witness')
    if event_count>=2:signals.append('multiple separated incidents')
    level=1+int(bool(signals))+int(len(signals)>=2)
    return dict(activeParts=active,moduleParts=active,targetParts=target_parts,
        processLength='short' if length<=12 else 'medium' if length<=24 else 'long',
        scheduledEvents=event_count,witnessRepairMoves=repair_moves,witnessCorrectCoverRemovals=covers,
        structuralGroup='L'+str(level),structuralReasons=signals,
        difficultyStatus='provisional-structural-proxy-not-human-or-model-validated',
        humanSuccessRate=None,modelSuccessRate=None,humanAttempts=0,modelAttempts=0,
        machineVisible=all(v['passed'] for v in visibility) if visibility else None,
        fullyOccludedOrLowContrast=any(not v['passed'] for v in visibility),
        minimumBestViewVisibleFraction=min((max(v['visibleFraction'].values()) for v in visibility),default=None),
        visibilityIsSeparateFromDifficulty=True)


def main():
    index=read(OUT/'index.json');profiles=[];gallery=[];visibility_rows=[]
    for meta in index['models']:
        mid=meta['id'];folder=OUT/'models'/mid
        if not (folder/'cases.private.json.gz').exists():continue
        cert=read(folder/'certificate.private.json.gz');cases=read(folder/'cases.private.json.gz')
        manual=read(folder/'manual.private.json.gz');control=next(c for c in cases if c['mode']=='dynamic' and not c['events'])
        ep=Episode(cert,control);packet=Packet(ep,manual,OUT/'assets'/mid)
        cache={}
        def rgb(state,view):
            key=(json.dumps(state,sort_keys=True),view)
            if key not in cache:
                cache[key]=packet.renderer.rgb(state,view,size=(800,600),supersample=1,frame_keys=['_module_frame'])
            return cache[key]
        def asset(image,role,**kwargs):
            record=packet.asset(image,role,**kwargs)
            record['file']=str(Path(record['file']).relative_to(OUT))
            return record
        # A full object view and a fixed module crop, both without error outlines.
        full_keys=list(packet.renderer.cert['fixed'])+[k for k,r in cert['candidates'].items() if r['kind']=='goal']
        image,_=packet.renderer.rgb(control['goal'],'isometric',size=(1600,1200),supersample=1,frame_keys=full_keys)
        full=asset(image,'complete-scene')
        model=dict(**meta,fullImage=full,cases=[],manual=[])
        for number,action in enumerate(manual['actions'],1):
            page=packet.manual_page(number)
            page['file']=str(Path(page['file']).relative_to(OUT))
            model['manual'].append(page)
        for case in cases:
            events=case.get('referenceEvents',[]) or ([case['referenceIncident']] if case.get('referenceIncident') else [])
            evidence=[];timeline=[]
            for number,event in enumerate(events,1):
                row=dict(caseId=case['id'],event=number,family=event['family'],changedPixels={},visibleFraction={})
                affected=set(event['affected'])|{a for a in event['after'] if event['after'][a]!=event['before'].get(a)}
                for view in VIEWS:
                    before,bmask=rgb(event['before'],view);after,amask=rgb(event['after'],view)
                    delta=np.max(np.abs(np.asarray(before,dtype=np.int16)-np.asarray(after,dtype=np.int16)),axis=2)
                    row['changedPixels'][view]=int(np.count_nonzero(delta>=24))
                    visible=0;isolated=0
                    ids=[packet.renderer.ids[a] for a in affected if a in packet.renderer.ids]
                    for state,mask in ((event['before'],bmask),(event['after'],amask)):
                        visible+=int(np.count_nonzero(np.isin(mask,ids)))
                        selected={a:state[a] for a in affected if state.get(a)}
                        if selected:
                            _,alone=packet.renderer.rgb(selected,view,size=(800,600),supersample=1,
                                frame_keys=['_module_frame'],fixtures=False)
                            isolated+=int(np.count_nonzero(alone))
                    row['visibleFraction'][view]=round(min(1.,visible/isolated),4) if isolated else 0.
                row.update(passed=max(row['changedPixels'].values())>=128,threshold=24,minimumPixels=128,
                    humanReadable=None,review='machine-only-human-pending')
                evidence.append(row);visibility_rows.append(row)
                pair_image=comparison(packet.renderer,event['before'],event['after'],'isometric',
                    'BEFORE EXTERNAL CHANGE','AFTER EXTERNAL CHANGE',frame_keys=['_module_frame'])
                timeline.append(dict(event=number,atManipulation=event.get('atManipulation'),
                    image=asset(pair_image,'research-event-comparison'),repairMoves=len(event['recovery']),
                    humanErrorIds=case['humanErrorIds']))
            current=case['initial'] if case['mode']=='static' or not events else events[0]['after']
            images={}
            for view in VIEWS:
                image=comparison(packet.renderer,current,case['goal'],view,'CURRENT NOW','TARGET (required state)',
                                 frame_keys=['_module_frame'])
                images[view]=asset(image,'current-target',view=view,panels=panels('current-now','target'))
            p=profile(meta,case,evidence);profiles.append(dict(caseId=case['id'],module=mid,**p))
            model['cases'].append(dict(id=case['id'],mode=case['mode'],family=case['family'],
                eventCount=len(case['events']),humanErrorIds=case['humanErrorIds'],images=images,
                timeline=timeline,profile=p,referenceIsProgramNotAI=True))
        gallery.append(model)
        print('VISUAL',mid,len(cases),len(cache),flush=True)
    write(OUT/'visibility.json',dict(status='MACHINE_CHECKED_HUMAN_PENDING',events=len(visibility_rows),
        passed=sum(v['passed'] for v in visibility_rows),rows=visibility_rows,apiCalls=0))
    write(OUT/'difficulty.json',dict(status='PROVISIONAL',cases=profiles,
        processGroups=dict(Counter(p['processLength'] for p in profiles)),
        structuralGroups=dict(Counter(p['structuralGroup'] for p in profiles)),
        empiricalValidationPending=True))
    write(OUT/'gallery.json',gallery)
    (OUT/'gallery-data.js').write_text('window.EXPANSION='+json.dumps(gallery,ensure_ascii=False)+';\n')


if __name__=='__main__':main()
