"""Repair legacy initial states that intersect the white baseplate.

The colliding pose is replaced by an uninstalled part. The resulting changed
question is replayed and recorded as such, never presented as an unchanged
legacy task.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from baseplate import PlateAssembly,PROTOCOL
from recover_plate5_disassembly import dismantle
from static_v4.certify import digest

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'deliverables/brickplan-static-held4/combined'
DEST=ROOT/'deliverables/brickplan-static-plate5'
def rows(path):return [json.loads(x) for x in path.read_text().splitlines()]

def main():
    source=rows(SOURCE/'cases.jsonl');by_id={x['id']:x for x in source};order={x['id']:i for i,x in enumerate(source)}
    approved=rows(DEST/'cases.jsonl');unresolved=rows(DEST/'unresolved.jsonl')
    models={};recovered=[];remaining=[]
    for row in unresolved:
        if row['reason']!='INITIAL_INTERSECTS_BASEPLATE':
            remaining.append(row);continue
        case=by_id[row['id']];mid=case['modelId']
        if mid not in models:
            runtime=PlateAssembly(json.loads((SOURCE/case['qualificationFile']).read_text()))
            models[mid]=(runtime,runtime.manual())
        runtime,manual=models[mid]
        if not manual['pathVerified']:
            remaining.append({**row,'retryReason':'GOAL_UNBUILDABLE'});continue
        initial=runtime.state(runtime.migrate_state(case['initial']))
        goal=runtime.state(runtime.migrate_state(case['goal']))
        removed=[]
        for actor,key in initial.items():
            if key and runtime.plate_collision(runtime.row(key)['part']):
                initial[actor]='';removed.append(actor)
        if not removed or runtime.complete(initial):
            remaining.append({**row,'retryReason':'NO_USEFUL_COLLISION_EDIT'});continue
        detaches,calls=dismantle(runtime,initial,limit=3000)
        if detaches is None:
            remaining.append({**row,'retryReason':'NO_DISASSEMBLY_FOUND','searchStates':calls});continue
        plan=detaches+[dict(type='attach',partId=a,candidate=goal[a]) for a in manual['parts']]
        state=dict(initial)
        for action in plan:
            state,feedback=runtime.check(state,action['partId'],action['type'],candidate=action.get('candidate'))
            if feedback['code']!='OK':break
        if feedback['code']!='OK' or not runtime.complete(state):
            remaining.append({**row,'retryReason':'NEW_PLAN_REPLAY_FAILED'});continue
        converted={**case,'initial':initial,'goal':goal,'oraclePlan':plan,
            'manipulationProtocol':PROTOCOL,'referenceCost':len(plan),'expectedOptimum':None,
            'referenceIsOptimal':False,'migrationMethod':'edited_initial_collision_removed',
            'sourceProtocol':'connector-workbench/4','sourceInitialEdited':True,
            'sourceCollisionActorsRemoved':removed,
            'referenceValidation':{'status':'DIRECT_REPLAY_PASS','sha256':digest(dict(
                caseId=case['id'],initial=initial,goal=goal,plan=plan,source=runtime.cert['contentSha256']))}}
        recovered.append(converted)
    combined=sorted(approved+recovered,key=lambda c:order[c['id']])
    assert len(combined)+len(remaining)==len(source)
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
