"""Recover plate5 tasks whose initial scene can be held during disassembly."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from baseplate import PlateAssembly,PROTOCOL
from static_v4.certify import digest

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'deliverables/brickplan-static-held4/combined'
DEST=ROOT/'deliverables/brickplan-static-plate5'

def rows(path):return [json.loads(x) for x in path.read_text().splitlines()]

def dismantle(runtime,initial,limit=2000):
    failed=set();calls=0
    def dfs(state):
        nonlocal calls
        token=tuple(state.values())
        if not any(token):return []
        if token in failed or calls>=limit:return None
        calls+=1
        for actor,key in state.items():
            if not key:continue
            after,feedback=runtime.check(state,actor,'detach')
            if feedback['code']!='OK':continue
            tail=dfs(after)
            if tail is not None:return [dict(type='detach',partId=actor)]+tail
        failed.add(token)
        return None
    return dfs(initial),calls

def main():
    source=rows(SOURCE/'cases.jsonl');order={c['id']:i for i,c in enumerate(source)}
    cases={c['id']:c for c in source}
    approved=rows(DEST/'cases.jsonl');unresolved=rows(DEST/'unresolved.jsonl')
    recovered=[];remaining=[];models={}
    for row in unresolved:
        if row['reason']!='INITIAL_HAS_NO_VERIFIED_DISASSEMBLY':
            remaining.append(row);continue
        case=cases[row['id']];mid=case['modelId']
        if mid not in models:
            runtime=PlateAssembly(json.loads((SOURCE/case['qualificationFile']).read_text()))
            models[mid]=(runtime,runtime.manual())
        runtime,goal_manual=models[mid]
        initial=runtime.state(runtime.migrate_state(case['initial']));goal=runtime.state(runtime.migrate_state(case['goal']))
        detaches,calls=dismantle(runtime,initial)
        if detaches is None or not goal_manual['pathVerified']:
            remaining.append({**row,'retryReason':'NO_DISASSEMBLY_FOUND','searchStates':calls});continue
        plan=detaches+[dict(type='attach',partId=a,candidate=goal[a]) for a in goal_manual['parts']]
        state=dict(initial)
        for action in plan:
            state,feedback=runtime.check(state,action['partId'],action['type'],candidate=action.get('candidate'))
            if feedback['code']!='OK':break
        if feedback['code']!='OK' or not runtime.complete(state):
            remaining.append({**row,'retryReason':'NEW_PLAN_REPLAY_FAILED'});continue
        recovered.append({**case,'initial':initial,'goal':goal,'oraclePlan':plan,
            'manipulationProtocol':PROTOCOL,'referenceCost':len(plan),'expectedOptimum':None,
            'referenceIsOptimal':False,'migrationMethod':'verified_held_component_dismantle',
            'sourceProtocol':'connector-workbench/4',
            'referenceValidation':{'status':'DIRECT_REPLAY_PASS','sha256':digest(dict(
                caseId=case['id'],initial=initial,goal=goal,plan=plan,source=runtime.cert['contentSha256']))}})
    combined=sorted(approved+recovered,key=lambda c:order[c['id']])
    assert len(combined)+len(remaining)==len(source)==3292
    (DEST/'cases.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in combined))
    (DEST/'questions.jsonl').write_text(''.join(json.dumps(dict(publicId=x['publicId'],modelId=x['modelId'],
        manipulationProtocol=PROTOCOL,observationProtocol='plate5-visual-pending-review'),ensure_ascii=False)+'\n' for x in combined))
    (DEST/'unresolved.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in remaining))
    summary=json.loads((DEST/'summary.json').read_text())
    summary.update(certified=len(combined),unresolved=len(remaining),
                   methods=dict(Counter(c['migrationMethod'] for c in combined)),
                   unresolvedReasons=dict(Counter(r['reason'] for r in remaining)),
                   certifiedBankSha256=hashlib.sha256((DEST/'cases.jsonl').read_bytes()).hexdigest())
    (DEST/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(recovered=len(recovered),certified=len(combined),unresolved=len(remaining)),ensure_ascii=False))

if __name__=='__main__':main()
