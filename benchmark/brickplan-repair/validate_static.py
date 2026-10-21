"""Full active-bank validation and independent BFS checks of static A* optima."""
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
import time
from static_bench import (OUT, TYPES, DYNAMIC, Domain, digest, dump, exact_plan,
                          normalized_state, part_name, replacement_kind)


def main():
    start=time.time();index=json.loads((OUT/'index.json').read_text())
    exported=[json.loads(l) for l in (OUT/'cases.jsonl').read_text().splitlines()]
    checked,actions,bfs_checks,shape_checks=0,0,0,0
    representatives={};max_actors=0
    for model in index['models']:
        folder=OUT/'models'/model['modelId'];cert=json.loads((folder/'qualification.json').read_text());cases=json.loads((folder/'cases.json').read_text())
        content=deepcopy(cert);content.pop('contentSha256');assert digest(content)==cert['contentSha256']
        assert model['caseCount']==len(cases)
        assert 2<=sum(c['kind']=='wrong_color' for c in cases.values())<=3
        domain=Domain(cert,{});seen=set()
        actor_count=len({r['actor'] for r in cert['candidates'].values()});max_actors=max(max_actors,actor_count);assert actor_count<=53
        for c in cases.values():
            assert c['kind'] in TYPES and c['kind'] not in DYNAMIC
            assert c['benchmarkMode']=='static' and c['environmentChanges'] is False
            assert not set(c).intersection({'preIntervention','intervention','interventions','causalReplay','oldPlan','rejectedPrefix','branchCostEvidence'})
            assert c['qualificationSha256']==cert['contentSha256']
            sig=normalized_state(c,cert);assert sig not in seen,(c['id'],'duplicate physical layout');seen.add(sig)
            before=domain.pack(c,c['initial']);assert domain.valid(c,before)=='OK'
            state=before
            for action in c['oraclePlan']:
                state,check=domain.transition(c,state,action);assert check['code']=='OK',(c['id'],check)
                actions+=1
            assert state==domain.pack(c,c['goal'])
            plan,_=exact_plan(domain,c);assert len(plan)==c['expectedOptimum']==len(c['oraclePlan'])
            changed={a for a in c['actors'] if c['initial'][a]!=c['goal'][a]}
            groups=[a for r in c['roots'] for a in r['affectedActors']]
            assert len(groups)==len(set(groups)) and set(groups)==changed
            for replacement in c['repairEvidence']['replacements']:
                a,b=replacement['expected'],replacement['actual']
                if replacement['type'] in ('wrong_type','wrong_size'):
                    target=next(r['part'] for r in cert['candidates'].values() if r['part']['partNumber']==a['part'])
                    actual=next(r['part'] for r in cert['candidates'].values() if r['part']['partNumber']==b['part'])
                    assert replacement_kind(target,actual)==replacement['type'];shape_checks+=1
                assert a['name']==part_name(a['part']) and b['name']==part_name(b['part'])
            signature=(c['kind'],c['difficulty'],bool('--deep' in model['modelId']))
            representatives.setdefault(signature,(cert,c))
            checked+=1
        assert model['kinds']==dict(Counter(c['kind'] for c in cases.values()))
    # Independent FIFO BFS provides a cross-check of search, including large structures.
    for signature,(cert,c) in representatives.items():
        domain=Domain(cert,{});plan=domain.plan(c,domain.pack(c,c['initial']))
        assert plan is not None and len(plan)==c['expectedOptimum'],(signature,c['id'])
        bfs_checks+=1
    assert checked==len(exported)==index['caseCount']
    assert len({c['id'] for c in exported})==checked
    report=dict(schema='brickplan-static-validation/2',caseCount=checked,modelCount=len(index['models']),
                oracleActionsReplayed=actions,exactOptimaRecomputed=checked,independentBfsChecks=bfs_checks,
                replacementDefinitionsChecked=shape_checks,maxRegisteredActors=max_actors,
                minSingleColorPerModel=min(m['kinds']['wrong_color'] for m in index['models']),
                maxSingleColorPerModel=max(m['kinds']['wrong_color'] for m in index['models']),
                dynamicCases=0,duplicatePhysicalLayoutsWithinModel=0,
                maxOptimum=max(c['expectedOptimum'] for c in exported),
                visualCasesAdmitted=sum(c['observation']['visualEligibility']=='verified' for c in exported),
                benchmarkSha256=digest(exported),seconds=round(time.time()-start,2))
    dump(OUT/'static-validation.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
