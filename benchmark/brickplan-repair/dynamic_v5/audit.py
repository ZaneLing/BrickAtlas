"""Direct /5 replay of every build, intervention, recovery, and control."""
from collections import Counter
from pathlib import Path
import json
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from dynamic_v5.episode import BANK, DynamicEpisode, load_case
from static_v4.certify import digest

def audit_case(case_id):
    cert, case=load_case(case_id)
    ep=DynamicEpisode(cert,case)
    source=json.loads((BANK/'models'/case['modelId']/'evidence.json').read_text())
    plan=source['buildWitness']
    assert ep.runtime.manual()['pathVerified']
    before_event=None
    for i, action in enumerate(plan,1):
        public=dict(type='attach',partId=ep.alias[action['partId']],candidate=ep.pose(action['candidate']))
        feedback=ep.step(public)
        assert feedback=={'code':'OK'}, (case_id,i,feedback)
        assert 'event' not in json.dumps(ep.observe()).lower(), 'Public observation exposed intervention metadata'
        if i==case['trigger']:
            before_event=ep.event['beforeSha256'] if ep.event else digest(ep.state)
        if ep.event:
            break
    assert before_event is not None
    if case['kind']=='none':
        assert ep.event is None
        for action in plan[len(ep.records):]:
            assert ep.step(dict(type='attach',partId=ep.alias[action['partId']],candidate=ep.pose(action['candidate'])))=={'code':'OK'}
    else:
        assert ep.event is not None, case_id
        assert ep.event['kind']==case['kind']
        assert ep.event['beforeSha256']==case['privateEvent']['beforeSha256']
        if case['kind']=='extra_layer':
            graph,_=ep.runtime.connections(ep.state)
            assert any(a!='@baseplate' for a in graph['X001']), (case_id,'spare must be on structure')
        for action in case['privateEvent']['recoveryWitness']:
            public=dict(type=action['type'],partId=ep.alias[action['partId']])
            if 'candidate' in action:public['candidate']=ep.pose(action['candidate'])
            feedback=ep.step(public)
            assert feedback=={'code':'OK'}, (case_id,action,feedback)
    assert ep.step({'type':'finish'})=={'code':'SUCCESS'}
    assert ep.score()['success']
    return dict(caseId=case_id,kind=case['kind'],modelId=case['modelId'],
                eventTriggered=bool(ep.event),oracleMoves=ep.score()['legalMoves'],
                eventBeforeSha256=before_event,chainSha256=ep.chain)

def main():
    cases=json.loads((BANK/'index.json').read_text())['cases']
    results=[audit_case(c['id']) for c in cases]
    # The agent may choose a different legal order; intervention selection must
    # certify its live prefix instead of assuming the authored witness order.
    cert,case=load_case('sr4-independent-1--t3--removed_piece')
    adaptive=DynamicEpisode(cert,case)
    for actor in ('F001','P001','P002'):
        action=dict(type='attach',partId=adaptive.alias[actor],candidate=adaptive.pose(adaptive.runtime.goal[actor]))
        assert adaptive.step(action)=={'code':'OK'}
    assert adaptive.event and adaptive.event['provenance']=='adaptive-certified'
    for action in adaptive.event['recoveryWitness']:
        public=dict(type=action['type'],partId=adaptive.alias[action['partId']])
        if 'candidate' in action:public['candidate']=adaptive.pose(action['candidate'])
        assert adaptive.step(public)=={'code':'OK'}
    assert adaptive.step({'type':'finish'})=={'code':'SUCCESS'}
    path=BANK/'audit.json'
    path.write_text(json.dumps(dict(schema='brickplan-dynamic-audit/1',total=len(results),
                                    passed=len(results),kinds=dict(Counter(r['kind'] for r in results)),
                                    adaptiveAlternatePrefixPassed=True,
                                    results=results),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(total=len(results),passed=len(results),kinds=dict(Counter(r['kind'] for r in results))),ensure_ascii=False))

if __name__=='__main__':main()
