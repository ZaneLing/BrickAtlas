"""Independent physical replay, event scheduling, flexible order, and leak checks."""
from collections import Counter
from copy import deepcopy
import json
import time
from pathlib import Path
from expansion_v7 import ROOT,OUT
from expansion_v7.build import read,write,states_for,run_witness,digest
from expansion_v7.runtime import Episode,execute,move,public_action,runtime,fork
from expansion_v7.evaluate import pair
from evaluation_outcomes import service_error


def check_inventory(cert):
    rows={}
    for key,row in cert['candidates'].items():
        part=row['part'];identity=(part['canonical'],part['colorHex'].lower())
        if row['actor'] in rows:assert rows[row['actor']]==identity,(row['actor'],'Physical part changes type/color between candidates')
        rows[row['actor']]=identity
    counts=Counter(r['actor'] for r in cert['candidates'].values())
    assert len(set(counts.values()))==1
    if cert.get('environmentMode')!='white-baseplate':
        assert not (set(cert['fixed'])&set(counts))


def alternate(rt,normal):
    initial={a:'' for a in rt.actors}
    for i in range(len(normal)-1):
        trial=normal[:i]+[normal[i+1],normal[i]]+normal[i+2:]
        end,_=execute(rt,initial,trial)
        if end is not None and rt.complete(end):return trial
    return None


def independent_replay(rt,case):
    state=dict(case['initial']);event_by_action={e['atManipulation']:e for e in case.get('referenceEvents',[])}
    for index,action in enumerate(case['referenceActions'],1):
        state,evidence=execute(rt,state,[action])
        assert state is not None,(case['id'],'Reference action rejected',action,evidence)
        if index in event_by_action:
            incident=event_by_action[index]
            assert state==incident['before']
            before=dict(state);state,checks=execute(rt,state,incident['changes'])
            assert state==incident['after'] and state!=before
            restored,_=execute(rt,state,incident['recovery'])
            assert restored==before
    target=dict(rt.goal);rt.goal=case['goal']
    try:assert rt.complete(state),case['id']
    finally:rt.goal=target


def main():
    started=time.time();index=read(OUT/'index.json');results=[];total=0;alt_conditions=0
    legacy=[ROOT/'deliverables/brickplan-static-plate5/cases.jsonl',
            ROOT/'deliverables/brickplan-dynamic-v6/cases.private.json',
            ROOT/'deliverables/brickplan-community-modules/cases.private.jsonl']
    legacy_hashes={str(p.relative_to(ROOT)):__import__('hashlib').sha256(p.read_bytes()).hexdigest() for p in legacy}
    for meta in index['models']:
        mid=meta['id'];folder=OUT/'models'/mid
        cert=read(folder/'certificate.private.json.gz');cases=read(folder/'cases.private.json.gz')
        normal=read(folder/'manual.private.json.gz')['actions'];rt=runtime(cert)
        check_inventory(cert)
        for case in cases:
            independent_replay(rt,case);total+=1
        control=next(c for c in cases if c['mode']=='dynamic' and not c['events'])
        ep=Episode(cert,control,seed=71);ep.runtime.q=rt.q
        before=dict(ep.state);ep.step({'type':'invalid','candidate':'secret'})
        assert ep.state==before and ep.feedback['code']=='INVALID_REQUEST' and len(ep.decisions)==1
        ep.step({'type':'inspect','view':'top'});assert ep.state==before and ep.previous==before
        ep.step(public_action(ep,normal[0]));assert ep.feedback['code']=='OK'
        before=dict(ep.state);ep.step(public_action(ep,normal[0]))
        assert ep.state==before and ep.feedback['code']=='ALREADY_INSTALLED'
        ep.step({'type':'finish'});assert not ep.score()['success']
        # Identical fixed common prefix before a real event, including aliases.
        fault=next(c for c in cases if c['mode']=='dynamic' and c['events'])
        cp=fault['events'][0]['minimumInstalled']
        prefix=Episode(cert,control,seed=71);prefix.runtime.q=rt.q
        for action in normal[:cp-1]:prefix.step(public_action(prefix,action))
        left,right=fork(prefix,fault);left.runtime.q=right.runtime.q=rt.q
        assert left.decisions==right.decisions and left.state==right.state
        for branch in (left,right):branch.step(public_action(branch,normal[cp-1]))
        assert not left.events and right.events
        assert left.history[-1]['before']==right.history[-1]['before']
        assert set(left.observe())==set(right.observe())
        forbidden={'family','events','event','goal','initial','referenceActions','humanErrorIds','scheduledEvents'}
        assert not forbidden.intersection(right.observe())
        assert [h['partId'] for h in left.observe()['handles']]==[h['partId'] for h in right.observe()['handles']]
        other=alternate(rt,normal);alternate_count=0
        if other:
            for case in [c for c in cases if c['mode']=='dynamic' and (not c['events'] or len(c['events'])>1)]:
                # Certify actual-state feasibility in another legal order. Any
                # untriggered variant is reported, never silently called repaired.
                try:run_witness(cert,case,other,rt.q);alternate_count+=1
                except AssertionError:pass
            assert alternate_count>=1
            alt_conditions+=alternate_count
        source=cert['source']
        if source.get('original'):
            assert __import__('hashlib').sha256((ROOT/source['original']).read_bytes()).hexdigest()==source['originalSha256']
            moving=set(source['moduleSourceIndices'])
            fixed={p['sourceIndex'] for p in cert['fixed'].values()}
            unknown={p['part']['sourceIndex'] for p in cert.get('conservativeContext',{}).values()}
            assert moving.isdisjoint(fixed|unknown) and fixed.isdisjoint(unknown)
            assert moving|fixed|unknown==set(range(source['totalInstances']))
        results.append(dict(module=mid,cases=len(cases),independentReplay='PASS',
            inventoryIdentity='PASS',uniformCandidateCounts='PASS',sharedPrefix='PASS',
            inspectionAndInvalidAction='PASS',sourceCoverage='PASS',
            alternativeOrderExists=other is not None,alternativeOrderConditionsPassed=alternate_count,
            alternativeOrderTried=[c['id'] for c in cases if c['mode']=='dynamic' and (not c['events'] or len(c['events'])>1)] if other else []))
        print('VALIDATED',mid,len(cases),'alternate',alternate_count,flush=True)
    success=dict(success=True)
    for scheduled,applied,expected in ((2,2,True),(2,1,False),(3,0,False),(0,0,False)):
        score=dict(success=True,eventApplied=bool(applied),scheduledEvents=scheduled,appliedEvents=applied)
        result=pair(success,score)
        assert result['recoveryPairEligible']==expected
        if not expected:assert result['repairSuccess'] is None
    assert pair(dict(success=False),dict(success=True,eventApplied=True,scheduledEvents=2,appliedEvents=2))['repairSuccess'] is None
    for status in ('HTTP 403','HTTP 429','timeout'):
        assert service_error(status)['category'] in ('request_rejected','rate_limited','timeout')
        assert pair(success,dict(success=True,eventApplied=True,scheduledEvents=2,appliedEvents=2),intervention_status='api_error')['repairSuccess'] is None
    for path,expected in legacy_hashes.items():
        assert __import__('hashlib').sha256((ROOT/path).read_bytes()).hexdigest()==expected
    write(OUT/'validation.json',dict(status='PASS',cases=total,models=len(results),rows=results,
        alternativeOrderConditions=alt_conditions,multiEventEligibility='PASS',serviceErrorsSeparate='PASS',
        legacyBanksUnchanged=legacy_hashes,apiModelCalls=0,humanAttempts=0,
        seconds=round(time.time()-started,2),scope='Program replay and contract evidence, not AI or human performance'))


if __name__=='__main__':main()
