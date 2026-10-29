"""At most five matched static/dynamic conditions per admitted complete object."""
from copy import deepcopy
from collections import Counter
from dynamic_arena import OUT
from dynamic_arena.qualify_sources import DEST
from expansion_v7.build import read,write,run_witness,HUMAN
from expansion_v7.runtime import runtime,execute,Episode
from expansion_v7.variants import augment,pad
from bench_design.source_expansion import visibility
from dynamic_v5.vision import DynamicVisionRenderer
from community_modules.core import render_certificate


def build(meta):
    folder=DEST/meta['id'];original=read(folder/'certificate.private.json.gz');manual=read(folder/'manual.private.json.gz');normal=manual['actions']
    cert=pad(augment(original));rt=runtime(cert)
    from expansion_v7.build import states_for
    states=states_for(rt,normal);renderer=DynamicVisionRenderer(render_certificate(cert),rt)
    def case(mode,family,cp=0):
        return dict(id=f'A4:{meta["id"]}::{family}' if mode=='dynamic' else f'A4:{meta["id"]}::static-{family}',module=meta['id'],mode=mode,family=family,initial=deepcopy(states[0] if mode=='dynamic' else states[cp]),goal=deepcopy(states[-1] if mode=='dynamic' else states[cp]),events=[],completedInstructionStep=cp,humanErrorIds=HUMAN.get(family,[]),sourceSetId=meta['setNumber'],protocol='arena-source-whole/2',track='whole-object')
    control=case('dynamic','control');control.update(run_witness(cert,control,normal,rt.q));cases=[control];rejected=[]
    category=meta.get('objectCategory','other')
    preferences={'animal':['rotated','offset'],'plant-food':['wrong-color','offset'],'boat':['offset','wrong-part'],'furniture-object':['wrong-color','offset'],'house-building':['wrong-color','extra-layer']}.get(category,['offset','wrong-color'])
    for family in ['missing']+preferences+['wrong-part','rotated','extra-layer']:
        if len(cases)>=5:break
        if any(c['family']==family for c in cases):continue
        success=False
        for cp in sorted(range(2,len(normal)),key=lambda x:abs(x-len(normal)*.6)):
            d=case('dynamic',family);d['events']=[dict(family=family,minimumInstalled=cp,minimumActionsSincePrevious=1,humanErrorIds=HUMAN[family],variant=0)]
            try:
                d.update(run_witness(cert,d,normal,rt.q));e=d['referenceEvents'][0];v=visibility(renderer,e['before'],e['after'])
                if not v['visible']:continue
                d['visibilityCheck']=v
                s=case('static',family,cp);s.update(initial=e['after'],goal=e['before'],referenceActions=e['recovery'],referenceIncident=e,visibilityCheck=v,legalWitnessOnly=True,humanValidated=False,modelEvaluated=False)
                end,checks=execute(rt,s['initial'],s['referenceActions'])
                assert end==s['goal'];s['referenceChecks']=checks
                # Judge final physical state, not matching the reference sequence.
                ep=Episode(cert,s);ep.state=end;assert ep.runtime.complete(end)
                cases.extend([d,s]);success=True;break
            except (ValueError,AssertionError):continue
        if not success:rejected.append(dict(family=family,reason='No visible legal triggered and recovered witness'))
    if len(cases)<3:raise ValueError('No matched repair pair')
    write(folder/'certificate.private.json.gz',cert);write(folder/'manual.private.json.gz',dict(actions=normal,states=states));write(folder/'cases.private.json.gz',cases)
    meta.update(caseCount=len(cases),dynamicCases=sum(c['mode']=='dynamic' for c in cases),staticCases=sum(c['mode']=='static' for c in cases),families=sorted({c['family'] for c in cases}),designRejected=rejected,maxCasesPerObject=5,sequenceScoring=False)
    write(folder/'metadata.json',meta);return meta,cases


def main():
    data=read(DEST/'index.json');active={r['setNumber']:r for r in read(OUT/'source-library.json')['models']};allcases=[]
    for m in data['models']:
        if m['setNumber'] not in active:continue
        m['objectCategory']=active[m['setNumber']]['objectCategory']
        try:meta,cases=build(m);m.update(meta);allcases.extend(dict(caseId=c['id'],model=m['id'],title=m['title'],sourceSetId=m['setNumber'],mode=c['mode'],family=c['family'],taskType='S1' if c['mode']=='static' else 'D0' if not c['events'] else 'D1',gtFile=str((DEST/m['id']/'cases.private.json.gz').relative_to(OUT)),humanValidated=False) for c in cases);print('DESIGNED',m['id'],len(cases),flush=True)
        except Exception as e:print('DESIGN WITHHELD',m['id'],str(e)[:180],flush=True)
        write(DEST/'index.json',data)
    write(OUT/'curated-questions.json',dict(cases=allcases,counts=dict(Counter(c['taskType'] for c in allcases)),apiCalls=0,referenceOnly=True))

if __name__=='__main__':main()
