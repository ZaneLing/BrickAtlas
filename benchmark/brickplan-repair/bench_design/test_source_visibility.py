"""Regression: symmetric rotations and alternate legal assembly orders."""
from pathlib import Path
from bench_design.source_expansion import OUT,read,write,runtime,guard_incidents,execute
from bench_design.session import Session,internal_action


def main():
    folder=OUT/'models/lion-mane-4903'
    rt=runtime(read(folder/'certificate.private.json.gz'));manual=read(folder/'manual.private.json.gz')
    state=manual['states'][6];latest=manual['actions'][5]['actor']
    order={a['actor']:i for i,a in enumerate(manual['actions'][:6])}
    raw=rt.incident('rotated',state,latest=latest,placement_order=order,variant=0)
    guard_incidents(rt)
    event=rt.incident('rotated',state,latest=latest,placement_order=order,variant=0)
    assert event and event['after']!=raw['after'] and event['visibilityCheck']['visible']
    assert execute(rt,event['after'],event['recovery'])[0]==state
    result=dict(status='PASS',invisibleVariantSkipped=True,requestedVariant=0,selectedVariant=event['selectedVariant'],
        visible=event['visibilityCheck'],legalRecovery=True,apiCalls=0)

    mid='truck-cab-30024';folder=OUT/'models'/mid
    rt=runtime(read(folder/'certificate.private.json.gz'));manual=read(folder/'manual.private.json.gz')
    original=manual['actions'];alternate=None
    for i in range(len(original)-1):
        candidate=original[:i]+[original[i+1],original[i]]+original[i+2:]
        end,_=execute(rt,manual['states'][0],candidate)
        if end is not None and rt.complete(end):alternate=candidate;break
    assert alternate and alternate!=original
    runs=[]
    for family in ('control','rotated'):
        case=f'QN:{mid}::dynamic::{family}'
        s=Session.open(case,Path('/tmp/brick-source-alternate')/family);s.autosave=False
        for action in alternate:
            count=len(s.events);assert s.submit(internal_action(s.ep,action))['code']=='OK'
            if len(s.events)>count:
                event=s.events[-1]['native'];assert event['visibilityCheck']['visible']
                for repair in event['recovery']:
                    assert s.submit(internal_action(s.ep,repair))['code']=='OK'
        s.submit(dict(type='finish'));assert s.result()['success']
        assert len(s.events)==(0 if family=='control' else 1)
        public=s.observe()
        assert 'visibilityCheck' not in str(public) and 'referenceActions' not in public and 'defaultView' not in public
        runs.append(dict(caseId=case,success=True,eventCount=len(s.events),privateVisibilityEvidenceNotExposed=True))
    result.update(alternateOrderDifferentFromReference=True,alternateOrder=alternate,alternateRuns=runs)
    write(OUT/'runtime-visibility-guard-check.json',result)
    print('PASS invisible-event rejection, alternate normal/fault routes, and private/public separation')


if __name__=='__main__':main()
