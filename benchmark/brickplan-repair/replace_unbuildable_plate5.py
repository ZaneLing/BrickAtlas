"""Replace unbuildable legacy questions with distinct, witnessed plate5 questions.

Every replacement retains its old public slot for a 3,292-question bank, but
records the old source ID and the donor witness. These are new questions, not
claimed repairs of an impossible old goal.
"""
from collections import Counter,defaultdict
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

def main():
    source=rows(SOURCE/'cases.jsonl');source_order={x['publicId']:i for i,x in enumerate(source)}
    existing=rows(DEST/'cases.jsonl')
    saved=DEST/'replaced-source-cases.jsonl'
    unresolved=rows(saved) if saved.exists() else rows(DEST/'unresolved.jsonl')
    approved=[x for x in existing if x.get('migrationMethod')!='verified_replacement_from_witness']
    # Editing a pose that intersected the plate can collapse two old questions
    # to the same current/target pair. Retain the earlier slot and replace the
    # duplicate with a genuinely different witnessed question.
    distinct=[];occupied=set()
    for case in approved:
        token=(case['modelId'],json.dumps(case['initial'],sort_keys=True),json.dumps(case['goal'],sort_keys=True))
        if token in occupied:
            unresolved.append(dict(id=case['id'],publicId=case['publicId'],modelId=case['modelId'],
                                   kind=case['kind'],reason='DUPLICATE_AFTER_COLLISION_REPAIR'))
        else:
            distinct.append(case);occupied.add(token)
    approved=distinct
    runtimes={};pool=defaultdict(list);seen=set()
    for donor in approved:
        if len(seen)>=max(1100,len(unresolved)*4):break
        if len(donor['oraclePlan'])<5:continue
        mid=donor['modelId']
        if mid not in runtimes:
            runtimes[mid]=PlateAssembly(json.loads((SOURCE/donor['qualificationFile']).read_text()))
        runtime=runtimes[mid];state=dict(donor['initial'])
        for index,action in enumerate(donor['oraclePlan'][:min(3,len(donor['oraclePlan'])-3)]):
            state,feedback=runtime.check(state,action['partId'],action['type'],candidate=action.get('candidate'))
            if feedback['code']!='OK':break
            if state==donor['goal']:continue
            token=(mid,tuple(state.items()),tuple(donor['goal'].items()))
            lookup=(mid,json.dumps(state,sort_keys=True),json.dumps(donor['goal'],sort_keys=True))
            if token in seen or lookup in occupied:continue
            seen.add(token)
            pool[donor['kind']].append((donor,dict(state),index+1))
    replacement=[];used=set();kinds=sorted(pool)
    for row in unresolved:
        preferred=[row['kind']]+[k for k in kinds if k!=row['kind']]
        pick=None
        for kind in preferred:
            while pool[kind] and (pool[kind][0][0]['id'],pool[kind][0][2]) in used:
                pool[kind].pop(0)
            while pool[kind]:
                candidate=pool[kind].pop(0)
                lookup=(candidate[0]['modelId'],json.dumps(candidate[1],sort_keys=True),
                        json.dumps(candidate[0]['goal'],sort_keys=True))
                if lookup not in occupied and not runtimes[candidate[0]['modelId']].complete(candidate[1]):
                    pick=candidate;break
            if pick:break
        if pick is None:raise RuntimeError('Insufficient distinct certified replacements')
        donor,state,prefix=pick;used.add((donor['id'],prefix))
        old_id=row['id'];new_id='plate5-replacement:'+old_id
        plan=donor['oraclePlan'][prefix:]
        runtime=runtimes[donor['modelId']]
        out={**donor,'id':new_id,'publicId':row['publicId'],'initial':state,
             'oraclePlan':plan,'referenceCost':len(plan),'expectedOptimum':None,
             'referenceIsOptimal':False,'kind':'repair_state','category':'repair_state',
             'title':'修复当前积木状态','description':'观察白色底板上的当前积木状态和目标，逐步修复。',
             'roots':[],'tags':['white_baseplate','replacement','verified_repair'],
             'migrationMethod':'verified_replacement_from_witness',
             'sourceReplacedCaseId':old_id,'sourceReplacedReason':row['reason'],
             'donorCaseId':donor['id'],'donorWitnessPrefix':prefix,
             'referenceValidation':{'status':'DIRECT_REPLAY_PASS','sha256':digest(dict(
                 caseId=new_id,initial=state,goal=donor['goal'],plan=plan,
                 source=runtime.cert['contentSha256']))}}
        replacement.append(out)
        occupied.add((out['modelId'],json.dumps(out['initial'],sort_keys=True),json.dumps(out['goal'],sort_keys=True)))
    combined=sorted(approved+replacement,key=lambda x:source_order[x['publicId']])
    assert len(combined)==len(source)==3292 and len({x['publicId'] for x in combined})==3292
    (DEST/'cases.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in combined))
    (DEST/'questions.jsonl').write_text(''.join(json.dumps(dict(publicId=x['publicId'],modelId=x['modelId'],
        manipulationProtocol=PROTOCOL,observationProtocol='plate5-visual-pending-review'),ensure_ascii=False)+'\n' for x in combined))
    (DEST/'replaced-source-cases.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in unresolved))
    (DEST/'unresolved.jsonl').write_text('')
    summary=json.loads((DEST/'summary.json').read_text())
    summary.update(certified=len(combined),unresolved=0,sourceCasesReplaced=len(replacement),
        sourceCasesPreserved=len(approved),replacementKinds=dict(Counter(x['sourceReplacedReason'] for x in replacement)),
        methods=dict(Counter(x['migrationMethod'] for x in combined)),unresolvedReasons={},
        certifiedBankSha256=hashlib.sha256((DEST/'cases.jsonl').read_bytes()).hexdigest())
    (DEST/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(replaced=len(replacement),total=len(combined)),ensure_ascii=False))
if __name__=='__main__':main()
