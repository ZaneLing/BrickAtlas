"""Measured, deterministic executor diagnostics; no learned-agent/API results."""
from pathlib import Path
import hashlib,json,sys,time
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'benchmark/brickplan-repair/community_modules'))
from core import Episode,ModuleAssembly,OUT,dump


def action(ep,a):
    result=dict(type=a['type'],partId=ep.actor_alias[a['actor']])
    if a['type']=='attach':result['candidate']=ep.pose_alias[a['candidate']]
    return result


def replay(cert,case,route,repair):
    ep=Episode(cert,case)
    for a in route:
        ep.step(action(ep,a))
        if repair and ep.history[-1]['eventApplied']:
            for undo in ep.last_event['recovery']:ep.step(action(ep,undo))
    ep.step({'type':'finish'})
    return dict(score=ep.score(),legalActions=sum(r['result']['code']=='OK' for r in ep.history),
                illegalActions=sum(r['result']['code']!='OK' for r in ep.history),
                events=sum(r['eventApplied'] for r in ep.history))


def main():
    start=time.time();modules=json.loads((OUT/'gallery-data.js.json').read_text());rows=[];sources={}
    for m in modules:
        base=OUT/m['id']
        cert=json.loads((base/'certificate.private.json').read_text())
        cases=json.loads((base/'cases.private.json').read_text())
        manual=json.loads((base/'manual.private.json').read_text())
        rt=ModuleAssembly(cert);cp=cert['checkpoint']
        reference=manual['states'][cp]
        for filename in ('certificate.private.json','cases.private.json','manual.private.json','order-checks.json'):
            p=base/filename;sources[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
        for route_name,actors in [('reference',m['orderChecks']['referenceOrder']),('alternative',m['orderChecks']['alternateOrder'])]:
            route=[dict(type='attach',actor=a,candidate=a+':goal') for a in actors]
            state={a:'' for a in rt.actors};states=[];checks=[]
            for a in route:
                state,check=rt.check(state,a['actor'],'attach',candidate=a['candidate'])
                assert check['code']=='OK';states.append(dict(state));checks.append(check)
            assert rt.complete(state)
            exact_opportunity=any(rt.signature(s)==rt.signature(reference) for s in states)
            sequence_accept=all(rt.signature(s)==rt.signature(manual['states'][i]) for i,s in enumerate(states,1))
            for c in cases:
                if c['mode']!='dynamic':continue
                blind=replay(cert,c,route,False);oracle=replay(cert,c,route,True)
                assert oracle['score']['success'] and (c['family']=='control' or oracle['events']==1)
                assert blind['score']['success']==(c['family']=='control')
                rows.append(dict(model=m['id'],route=route_name,family=c['family'],
                    exactPrefixTriggerOpportunity=exact_opportunity,
                    sequentialIntermediateAcceptance=sequence_accept,
                    finalNormalGeometryCorrect=True,blind=blind,privileged=oracle))
        print('STUDY',m['id'],flush=True)
    conditions={}
    for route in ('reference','alternative'):
        selected=[r for r in rows if r['route']==route];faults=[r for r in selected if r['family']!='control'];controls=[r for r in selected if r['family']=='control']
        conditions[route]=dict(models=len(controls),faultTrials=len(faults),
            exactPrefixTriggers=sum(r['exactPrefixTriggerOpportunity'] for r in faults),
            actualStateTriggers=sum(r['privileged']['score']['eventApplied'] for r in faults),
            sequentialNormalAccepted=sum(r['sequentialIntermediateAcceptance'] for r in controls),
            terminalNormalAccepted=sum(r['finalNormalGeometryCorrect'] for r in controls),
            blindControlCompleted=sum(r['blind']['score']['success'] for r in controls),
            blindFaultCompleted=sum(r['blind']['score']['success'] for r in faults),
            privilegedCompleted=sum(r['privileged']['score']['success'] for r in selected))
    output=dict(schema='brickplan-paper-protocol-study/1',date='2026-10-25',originalDesignDate='2026-10-21',
        scope='Deterministic selected-route regression experiment; not random routes or learned models.',
        trials=len(rows),conditions=conditions,rows=rows,sources=sources,apiCalls=0,seconds=round(time.time()-start,2))
    dump(HERE/'evidence/protocol-study.json',output)
    print(json.dumps(conditions,indent=2))


if __name__=='__main__':main()
