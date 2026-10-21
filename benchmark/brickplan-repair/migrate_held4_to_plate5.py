"""Re-certify every held4 static task under the actual white-baseplate executor.

No failed source task is silently dropped: certified tasks and unresolved cases
have separate complete inventories. A full dismantle/rebuild witness is used
only when the source repair path cannot be executed under plate5.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from baseplate import PlateAssembly, PROTOCOL
from static_v4.certify import digest

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'deliverables/brickplan-static-held4/combined'
DEST=ROOT/'deliverables/brickplan-static-plate5'
AUDITS=[ROOT/'deliverables/brickplan-plate-audit-2026-10-16/rows.jsonl',
        ROOT/'deliverables/brickplan-static-held4/expansion/plate5-audit/rows.jsonl']

def read(path):return json.loads(path.read_text())
def lines(path):return [json.loads(line) for line in path.read_text().splitlines()]
def dump(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def plan_from_manual(runtime,initial,goal,goal_manual):
    if any(runtime.plate_collision(p) for p in runtime.present(initial).values()):
        return None,'INITIAL_INTERSECTS_BASEPLATE'
    if not goal_manual['pathVerified']:
        return None,'GOAL_HAS_NO_VERIFIED_BUILD_ORDER'
    first=runtime.manual(initial)
    if not first['pathVerified']:
        return None,'INITIAL_HAS_NO_VERIFIED_DISASSEMBLY'
    plan=[dict(type='detach',partId=actor) for actor in reversed(first['parts'])]
    plan += [dict(type='attach',partId=actor,candidate=goal[actor]) for actor in goal_manual['parts']]
    state=dict(initial)
    for index,action in enumerate(plan):
        state,feedback=runtime.check(state,action['partId'],action['type'],candidate=action.get('candidate'))
        if feedback['code']!='OK':return None,f'REPLAY_{index}_{feedback["code"]}'
    if not runtime.complete(state):return None,'FINAL_NOT_GOAL'
    return plan,None

def main():
    cases=lines(SOURCE/'cases.jsonl')
    audits={row['caseId']:row for path in AUDITS for row in lines(path)}
    if len(cases)!=3292 or len(audits)!=3292 or {c['id'] for c in cases}!=set(audits):
        raise RuntimeError('Source or audit denominator changed')
    approved=[];questions=[];unresolved=[];methods=Counter();model_counts=Counter()
    current_model=None;runtime=None;goal_manual=None
    for number,case in enumerate(cases,1):
        if case['modelId']!=current_model:
            current_model=case['modelId']
            cert=read(SOURCE/case['qualificationFile'])
            runtime=PlateAssembly(cert)
            goal_manual=None
        initial=runtime.state(runtime.migrate_state(case['initial']))
        goal=runtime.state(runtime.migrate_state(case['goal']))
        if goal!=runtime.goal:
            unresolved.append(dict(id=case['id'],publicId=case['publicId'],modelId=current_model,kind=case['kind'],reason='GOAL_MISMATCH'))
            continue
        audit=audits[case['id']]
        if audit['status']=='PASS':
            plan=case['oraclePlan'];method='direct_source_plan'
        else:
            if goal_manual is None:goal_manual=runtime.manual(goal)
            plan,reason=plan_from_manual(runtime,initial,goal,goal_manual)
            if plan is None:
                unresolved.append(dict(id=case['id'],publicId=case['publicId'],modelId=current_model,kind=case['kind'],reason=reason,sourceIssues=audit['issues']))
                continue
            method='verified_dismantle_rebuild'
        converted={**case,'initial':initial,'goal':goal,'oraclePlan':plan,
                   'manipulationProtocol':PROTOCOL,'referenceCost':len(plan),
                   'expectedOptimum':None,'referenceIsOptimal':False,
                   'migrationMethod':method,'sourceProtocol':'connector-workbench/4',
                   'referenceValidation':{'status':'DIRECT_REPLAY_PASS','sha256':digest(dict(
                       caseId=case['id'],initial=initial,goal=goal,plan=plan,source=runtime.cert['contentSha256']))}}
        approved.append(converted)
        questions.append(dict(publicId=case['publicId'],modelId=current_model,
                              manipulationProtocol=PROTOCOL,observationProtocol='plate5-visual-pending-review'))
        methods[method]+=1;model_counts[current_model]+=1
        if number%100==0:print(f'{number}/3292 certified={len(approved)} unresolved={len(unresolved)}',flush=True)
    DEST.mkdir(parents=True,exist_ok=True)
    (DEST/'cases.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in approved))
    (DEST/'questions.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in questions))
    (DEST/'unresolved.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in unresolved))
    summary=dict(schema='brickplan-static-plate5-migration/1',sourceCases=len(cases),certified=len(approved),
                 unresolved=len(unresolved),methods=dict(methods),unresolvedReasons=dict(Counter(x['reason'] for x in unresolved)),
                 modelConfigurations=len(model_counts),protocol=PROTOCOL,
                 sourceBankSha256=hashlib.sha256((SOURCE/'cases.jsonl').read_bytes()).hexdigest(),
                 certifiedBankSha256=hashlib.sha256((DEST/'cases.jsonl').read_bytes()).hexdigest())
    dump(DEST/'summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
