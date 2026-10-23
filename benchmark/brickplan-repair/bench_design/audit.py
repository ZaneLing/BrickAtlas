"""Fresh replay of every retained execution condition; no provider requests."""
from collections import Counter,defaultdict
import hashlib
import time
from bench_design import ROOT,OUT
from expansion_v7.build import read,write,states_for
from expansion_v7.validate import independent_replay
from expansion_v7.runtime import runtime,public_action
from expansion_v7.scope import allowed
from community_modules.core import ModuleAssembly,Episode as ModuleEpisode
from baseplate import PlateAssembly
from plate5_eval import cases as static_cases,evaluate as static_evaluate
from dynamic_v6.build import perform


def main():
    start=time.time();counts=Counter();failures=[];by_model=[]
    sources=[ROOT/'deliverables/brickplan-static-plate5/cases.jsonl',
             ROOT/'deliverables/brickplan-dynamic-v6/cases.private.json',
             ROOT/'deliverables/brickplan-community-modules/cases.private.jsonl']
    original={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    for c in static_cases().values():
        try:
            result=static_evaluate(c['publicId'],[*c['oraclePlan'],{'type':'finish'}])
            assert result['success'] and result['invalidMoves']==0
            counts['S']+=1
        except Exception as exc:failures.append(dict(bank='S',id=c['id'],reason=str(exc)[:300]))
    print('REPLAY S',counts['S'],'failures',len(failures),flush=True)
    groups=defaultdict(list)
    for c in read(sources[1])['cases']:
        if allowed(c):groups[c['modelId']].append(c)
    for mid,cases in groups.items():
        folder=ROOT/'deliverables/brickplan-dynamic-v6/models'/mid
        rt=PlateAssembly(read(folder/'qualification.json'))
        normal=read(folder/'evidence.json')['buildWitness']
        state={a:'' for a in rt.actors};states=[state]
        def apply(state,actions):
            for action in actions:
                state=perform(rt,state,action)
                assert state is not None,action
            return state
        for action in normal:states.append(apply(states[-1],[action]))
        assert rt.complete(states[-1])
        for c in cases:
            try:
                cp=c['trigger'];event=c.get('privateEvent')
                if event:
                    after=apply(states[cp],event['transaction'])
                    assert rt.signature(after)!=rt.signature(states[cp])
                    end=apply(after,event['recoveryWitness'])
                else:end=apply(states[cp],normal[cp:])
                assert rt.complete(end);counts['D']+=1
            except Exception as exc:failures.append(dict(bank='D',id=c['id'],reason=str(exc)[:300]))
        by_model.append(dict(bank='D',id=mid,conditions=len(cases)))
    print('REPLAY D',counts['D'],'failures',len(failures),flush=True)
    for meta in read(ROOT/'deliverables/brickplan-community-modules/gallery-data.js.json'):
        folder=ROOT/'deliverables/brickplan-community-modules'/meta['id']
        cert=read(folder/'certificate.private.json');cases=read(folder/'cases.private.json')
        cache=ModuleAssembly(cert).q
        for c in cases:
            try:
                ep=ModuleEpisode(cert,c,41);ep.runtime.q=cache
                for action in c['referenceActions']:
                    ep.step(public_action(ep,action));assert ep.feedback['code']=='OK'
                ep.step({'type':'finish'});assert ep.score()['success'];counts['M']+=1
            except Exception as exc:failures.append(dict(bank='M',id=c['id'],reason=str(exc)[:300]))
    print('REPLAY M',counts['M'],'failures',len(failures),flush=True)
    for bank,root in [('E7',ROOT/'deliverables/brickplan-expansion-v7'),('O',ROOT/'deliverables/brickplan-recognizable-models')]:
        models=read(root/'index.json')['models'] if bank=='E7' else read(root/'admission-screen.json')['admitted']
        for meta in models:
            folder=root/'models'/meta['id'];cert=read(folder/'certificate.private.json.gz')
            rt=runtime(cert);cases=read(folder/'cases.private.json.gz')
            for c in cases:
                try:independent_replay(rt,c);counts[bank]+=1
                except Exception as exc:failures.append(dict(bank=bank,id=c['id'],reason=str(exc)[:300]))
            by_model.append(dict(bank=bank,id=meta['id'],conditions=len(cases)))
            print('REPLAY',bank,meta['id'],len(cases),'failures',len(failures),flush=True)
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in original.items())
    write(OUT/'physical-audit.json',dict(status='PASS' if not failures else 'FAIL',
        executionConditionsPassed=sum(counts.values()),perBank=dict(counts),failures=failures,
        referenceDataUnchanged=original,seconds=round(time.time()-start,2),models=by_model,
        scope='Fresh legal reference replays, including 83 historical adapters and duplicate conditions; not model performance or human image review.',
        humanCaseReview=False,paidApiCalls=0))
    print('PHYSICAL AUDIT',dict(counts),'failures',len(failures),flush=True)
    assert not failures,failures


if __name__=='__main__':main()
