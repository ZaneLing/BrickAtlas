"""Structural descriptors for every physical task in the combined source split."""
from collections import Counter
import json
from expansion_v7 import ROOT,OUT
from expansion_v7.build import read,write


def description(parts,moves,covers,events):
    signals=[]
    if parts>=20:signals.append('at least 20 target/build parts')
    if covers:signals.append('correct target placements removed in reference witness')
    if events>=2:signals.append('multiple incidents')
    return dict(targetParts=parts,witnessRepairMoves=moves,witnessCoverRemovals=covers,
        scheduledEvents=events,structuralGroup='L'+str(1+int(bool(signals))+int(len(signals)>=2)),
        structuralReasons=signals,humanAttempts=0,modelAttempts=0,
        humanSuccessRate=None,modelSuccessRate=None,status='PROVISIONAL_NOT_EMPIRICALLY_VALIDATED',
        witnessIsNotShortestPath=True)


def main():
    master=read(OUT/'global-splits.json');features={}
    for line in (ROOT/'deliverables/brickplan-static-plate5/cases.jsonl').read_text().splitlines():
        c=json.loads(line);moves=c.get('oraclePlan',[])
        exact_removals=sum(a.get('type')=='detach' and bool(c['initial'].get(a.get('partId',a.get('actor'))))
            and c['initial'].get(a.get('partId',a.get('actor')))==c['goal'].get(a.get('partId',a.get('actor'))) for a in moves)
        features['S:'+c['id']]=dict(**description(sum(bool(k) for k in c['goal'].values()),len(moves),exact_removals,0),
            visibilityStatus='full-bank-render-review-pending',coverCountDefinition='Exact target handles in saved reference; not minimum geometric removals')
    legacy_models={}
    for c in read(ROOT/'deliverables/brickplan-dynamic-v6/cases.private.json')['cases']:
        e=c.get('privateEvent') or {}
        repair,covers=e.get('repairPrefixMoves'),e.get('temporaryCorrectRemovals')
        if not e:repair=covers=0
        elif repair is None:
            # Older witnesses combine repair and remaining construction. Derive
            # the first return to the saved prefix instead of calling the entire
            # continuation a repair, or filling missing metadata with zero.
            mid=c['modelId']
            if mid not in legacy_models:
                folder=ROOT/'deliverables/brickplan-dynamic-v6/models'/mid
                cert=read(folder/'qualification.json')
                legacy_models[mid]=(cert,read(folder/'evidence.json')['buildWitness'])
            cert,plan=legacy_models[mid]
            before={r['actor']:'' for r in cert['candidates'].values()}
            def apply(state,action):
                state[action['partId']]='' if action['type']=='detach' else action['candidate']
            for action in plan[:c['trigger']]:apply(before,action)
            state=dict(before)
            for action in e['transaction']:apply(state,action)
            initial=dict(state);removed=0
            for number,action in enumerate(e['recoveryWitness'],1):
                actor=action['partId']
                removed+=int(action['type']=='detach' and bool(initial.get(actor))
                    and initial.get(actor)==before.get(actor))
                apply(state,action)
                if state==before:repair,covers=number,removed;break
        features['D:'+c['id']]=dict(**description(c['targetParts'],repair,covers,int(bool(e))),
            eventStage=c.get('stage'),visibilityStatus='Use v6 visibility audit; human validation pending')
    for m in read(ROOT/'deliverables/brickplan-community-modules/gallery-data.js.json'):
        for c in read(ROOT/'deliverables/brickplan-community-modules'/m['id']/'cases.private.json'):
            e=c.get('referenceIncident') or {}
            features['M:'+c['id']]=dict(**description(sum(bool(k) for k in c['goal'].values()),len(e.get('recovery',c.get('referenceActions',[]))),0,int(bool(c.get('event')))),
                moduleParts=m['remaining'],visibilityStatus='Original module pixel checks; human validation pending')
    for c in read(OUT/'difficulty.json')['cases']:
        features['E7:'+c['caseId']]={k:v for k,v in c.items() if k not in ('caseId','module')}
    rows=[dict(caseId=r['id'],track=r['track'],source=r['source'],split=r['split'],**features[r['id']]) for r in master['cases']]
    write(OUT/'difficulty-all.json',dict(cases=rows,counts=dict(Counter(r['structuralGroup'] for r in rows)),
        calibratedHumanRows=0,calibratedModelRows=0,empiricalLabels=False,
        guidance='Compare within track. Visibility is a separate axis; hidden information is not automatically a hard perception question.'))
    print('DIFFICULTY',len(rows),'structural descriptors; empirical rates remain null',flush=True)


if __name__=='__main__':main()
