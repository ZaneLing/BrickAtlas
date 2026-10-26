"""Build a bounded blind operation / mechanical spotcheck review round."""
from collections import Counter
from copy import deepcopy
import argparse
import hashlib
import json
from pathlib import Path
from bench_design import ROOT,OUT
from bench_design.challenges import QUALITY
from bench_design.run_episode import public_rows,source_rows,load
from bench_design.session import Session,internal_action,assess_pair,digest
from bench_design.metrics import aggregate,aggregate_pairs
from expansion_v7.build import read,write


def pick_blind():
    rows=list(public_rows().values());rows=[r for r in rows if r['mainTaskCandidate'] and not r['isAlias']]
    chosen=[]
    def choose(predicate):
        found=next((r for r in rows if predicate(r) and r['id'] not in chosen),None)
        if found:chosen.append(found['id'])
    choose(lambda r:r['bank']=='O' and r['model']=='whole-4037' and r['taskType']=='S1' and r['errorCodes']==['E03'])
    choose(lambda r:r['bank']=='O' and r['model']=='whole-4018' and r['taskType']=='S0')
    choose(lambda r:r['bank']=='E7' and r['model']=='v7-long-bookshelf' and r['mode']=='static' and r['family']=='buried-repair')
    choose(lambda r:r['bank']=='M' and r['model']=='cottage-roof' and r['taskType']=='D0')
    challenges=read(QUALITY/'challenges.private.json.gz')['cases']
    for category in ['repair-overlap','three-incidents']:
        found=next(c for c in challenges if c['category']==category)
        chosen.append(found['id'])
    for code in ['E01','E02','E04','E05','E06']:
        choose(lambda r:r['bank']=='O' and r['taskType']=='S1' and code in r['errorCodes'])
    choose(lambda r:r['mode']=='static' and r['model']=='v7-long-city-bus' and 'E07' in r['errorCodes'])
    choose(lambda r:r['bank']=='E7' and r['mode']=='static' and r['family']=='early-cover')
    choose(lambda r:r['bank']=='M' and r['taskType']=='S0')
    choose(lambda r:r['bank']=='O' and r['model']=='whole-4017' and r['taskType']=='D0')
    choose(lambda r:r['bank']=='O' and r['model']=='whole-4018' and r['taskType']=='D1' and r['family']=='missing')
    choose(lambda r:r['bank']=='M' and r['model']=='racer-top' and r['taskType']=='D1' and r['family']=='missing')
    for category in ['buried-overlap','late-repair','repeated-color','orientation-repair','access-replanning','swap-repair']:
        found=next((c for c in challenges if c['category']==category),None)
        if found:chosen.append(found['id'])
    # Additional modules extend the queue, without making every question a gate.
    for mid in ['seaplane-tail','panda-head','white-house-roof','police-helicopter-top',
                'rockefeller-crown','brandenburg-top','orange-helicopter-tail','museum-roof-long']:
        choose(lambda r:r['model']==mid and r['mode']=='static' and r['family'] in ('missing','wrong-color'))
    choose(lambda r:r['bank']=='S' and r['taskType']=='S0')
    choose(lambda r:r['bank']=='S' and r['taskType']=='S1' and 'E04' in r['errorCodes'])
    choose(lambda r:r['bank']=='D' and r['model']=='obj-chair' and r['taskType']=='D0')
    choose(lambda r:r['bank']=='D' and r['model']=='obj-city-car' and r['taskType']=='D1' and 'E02' in r['errorCodes'])
    # Every added stress condition gets an operable review page. The first six
    # remain a short priority batch; submitting a subset is always allowed.
    for item in challenges:
        if item['id'] not in chosen:chosen.append(item['id'])
    return [dict(code=f'Q{i+1:03}',caseId=cid,priority=i<6,mode=('dynamic' if cid.startswith('QX:') else public_rows()[cid]['mode']))
            for i,cid in enumerate(chosen)]


def check_evaluation():
    checks=[];runs=[];pairs=[]
    root=QUALITY/'scripted-evidence';root.mkdir(exist_ok=True,parents=True)
    cid='E7:v7::v7-long-bookshelf::static::buried-repair::t7'
    session=Session.open(cid,root/'static-repair','scripted:static-repair')
    for a in session.row['case']['referenceActions']:
        assert session.submit(internal_action(session.ep,a))['code']=='OK'
    session.submit({'type':'finish'});result=session.result();assert result['success'] and result['executionMetrics']['acceptedMoves']==10
    checks.append(dict(name='static-repair',passed=True,success=True,referenceMoves=10));runs.append(result)
    # Alternative legal route: adjacent independent operations actually swapped.
    from expansion_v7.validate import alternate
    from expansion_v7.runtime import runtime
    folder=ROOT/'deliverables/brickplan-expansion-v7/models/v7-long-city-bus'
    cert=read(folder/'certificate.private.json.gz');normal=read(folder/'manual.private.json.gz')['actions']
    route=alternate(runtime(cert),normal);assert route is not None and route!=normal
    normal_id=next(r['id'] for r in public_rows().values() if r['model']=='v7-long-city-bus' and r['taskType']=='D0')
    session=Session.open(normal_id,root/'alternative-order','scripted:alternative-order')
    for a in route:assert session.submit(internal_action(session.ep,a))['code']=='OK'
    session.submit({'type':'finish'});assert session.result()['success'];runs.append(session.result())
    checks.append(dict(name='alternative-legal-order',passed=True,success=True,sequenceDiffers=True))
    # A module's exact public prefix and actual images are shared, then branches diverge.
    fault_id=next(r['id'] for r in public_rows().values() if r['bank']=='M' and r['model']=='cottage-roof' and r['taskType']=='D1' and r['family']=='missing')
    for label,stop_early in [('repaired',False),('untriggered',True)]:
        control=Session.open(fault_id,root/(label+'-control'),'scripted:'+label,control=True)
        fault=Session.open(fault_id,root/(label+'-fault'),'scripted:'+label)
        actions=fault.row['case']['referenceActions'];trigger=fault.row['case']['event']['minimumInstalled']
        prefix=0 if stop_early else max(0,trigger-1)
        normal_actions=[a for a in actions if a['type']=='attach' and a.get('candidate') in control.goal.values()]
        # Use the module's normal manual, rather than a fault-repair witness suffix.
        module=read(ROOT/'deliverables/brickplan-community-modules/gallery-data.js.json')
        info=next(m for m in module if m['id']=='cottage-roof')
        from community_modules.core import ModuleAssembly
        full=control.goal;normal_actions=[]
        order=info['manual']
        for step in order:
            # Existing M witnesses expose the internal actor/candidate pair here.
            actor=step.get('actor');key=step.get('candidate')
            if actor is None:
                actor=step.get('partId')
            if key is None and actor is not None:key=full[actor]
            if actor is not None:normal_actions.append(dict(type='attach',actor=actor,candidate=key))
        if not normal_actions:
            normal_case=next(c for c in read(ROOT/'deliverables/brickplan-community-modules/cottage-roof/cases.private.json') if c['mode']=='dynamic' and not c['event'])
            normal_actions=normal_case['referenceActions']
        if stop_early:
            for branch in [control,fault]:branch.observe();branch.submit({'type':'finish'})
        else:
            for action in normal_actions[:prefix]:
                for branch in [control,fault]:branch.observe();assert branch.submit(internal_action(branch.ep,action))['code']=='OK'
            for branch in [control,fault]:branch.observe()
            for action in normal_actions[prefix:]:
                assert control.submit(internal_action(control.ep,action))['code']=='OK'
                seen=len(fault.events);assert fault.submit(internal_action(fault.ep,action))['code']=='OK'
                if len(fault.events)>seen:
                    for undo in fault.events[-1]['native']['recovery']:
                        assert fault.submit(internal_action(fault.ep,undo))['code']=='OK'
            control.submit({'type':'finish'});fault.submit({'type':'finish'})
        pair=assess_pair(control,fault,prefix);pairs.append(pair)
        if stop_early:
            assert pair['metrics']['conditionalRecoverySuccess'] is None and fault.result()['incidentExposure']=='untriggered'
        else:
            assert pair['sharedPrefixProof']['verified'] and pair['metrics']['conditionalRecoverySuccess'] is True
        write(root/(label+'-pair.private.json'),pair);runs.extend([control.result(),fault.result()])
        checks.append(dict(name=label,passed=True,pair=pair['metrics']))
    item=next(c for c in read(QUALITY/'challenges.private.json.gz')['cases'] if c['category']=='repair-overlap')
    session=Session.open(item['id'],root/'overlapping-events','scripted:overlapping-events')
    for a in session.row['case']['referenceActions']:
        assert session.submit(internal_action(session.ep,a))['code']=='OK'
    session.submit({'type':'finish'});result=session.result()
    assert result['success'] and len(result['eventWindows'])==2
    assert result['eventWindows'][0]['observedRecovery'] is False
    assert result['eventWindows'][0]['endBeforeEventIndex']==2
    assert result['eventWindows'][1]['observedRecovery'] is True
    assert result['allIncidentCompletion'] is True and result['allWindowsRecovered'] is False
    checks.append(dict(name='new-event-during-unfinished-repair',passed=True,finalSuccess=True,
                       windows=result['eventWindows']));runs.append(result)
    for filename,data in [('normalized-runs.jsonl',runs),('normalized-pairs.jsonl',pairs)]:
        (root/filename).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in data))
    write(QUALITY/'evaluation-wiring-checks.json',dict(status='PASS',checks=checks,
        runGroups=aggregate(runs),pairGroups=aggregate_pairs(pairs),apiCalls=0,
        scope='Written policies and exact action/state/image logs; not learned-model or human performance.'))
    return checks


def build_physics(blind,limit=32):
    from bench_design.independent_geometry import check,calibrate
    probes=[];seen=set()
    old=[r['caseId'] for r in blind if not r['caseId'].startswith('QX:')]
    new=[r['caseId'] for r in blind if r['caseId'].startswith('QX:')]
    # Start with the difficult access states, then include a complete original.
    old.sort(key=lambda cid:('buried' not in cid,'early-cover' not in cid,cid))
    ids=[]
    for i in range(max(len(old),len(new))):
        if i<len(old):ids.append(old[i])
        if i<len(new):ids.append(new[i])
    for cid in ids:
        if len(probes)>=limit:break
        row,ep,_,_=load(cid,QUALITY/'probe-render-cache')
        state=deepcopy(row['case']['referenceEvents'][0]['after'] if cid.startswith('QX:') else ep.state)
        rt=ep.runtime;options=[];count_before=len(probes)
        for actor,key in state.items():
            if key:options.append(dict(type='detach',actor=actor))
        reference=(row['case']['referenceEvents'][0]['recovery'] if cid.startswith('QX:') else row['case'].get('referenceActions',row['case'].get('oraclePlan',[])))
        options=reference[:2]+options
        options+=[dict(type='attach',actor=r['actor'],candidate=k) for k,r in ep.cert['candidates'].items() if not state.get(r['actor'])][:60]
        accepted=blocked=colliding=0
        for action in options:
            actor=action.get('actor',action.get('partId'))
            action={**action,'actor':actor};after,verdict=rt.check(state,actor,action['type'],candidate=action.get('candidate'))
            code=verdict['code']
            if code not in ('OK','PATH_BLOCKED','ENDPOINT_COLLISION'):continue
            if code=='OK' and accepted>=1 or code=='PATH_BLOCKED' and blocked>=1 or code=='ENDPOINT_COLLISION' and colliding>=1:continue
            token=digest([cid,state,action])
            if token in seen:continue
            seen.add(token)
            if code=='OK':accepted+=1
            elif code=='PATH_BLOCKED':blocked+=1
            else:colliding+=1
            measured=check(rt,state,action,verdict)
            proposed={**state,actor:'' if action['type']=='detach' else action['candidate']}
            probe=dict(code=f'P{len(probes)+1:03}',caseId=cid,state=state,action=action,
                proposed=proposed,engineResult=verdict,independentResult=measured,
                sameAsBlindCase=next((x['code'] for x in blind if x['caseId']==cid),None))
            probes.append(probe);print('PHYSICS',probe['code'],code,measured['status'],flush=True)
            if len(probes)>=limit or len(probes)-count_before>=2:break
    write(QUALITY/'physics-probes.private.json.gz',dict(probes=probes))
    write(QUALITY/'independent-geometry-check.json',dict(backend='manifold3d',calibration=calibrate(),
        probes=len(probes),statuses=dict(Counter(p['independentResult']['status'] for p in probes)),
        cases=[dict(code=p['code'],caseId=p['caseId'],engine=p['engineResult']['code'],independent=p['independentResult']) for p in probes],
        humanChecked=False,realPhysicsQualified=False,apiCalls=0,
        backendSource='https://github.com/elalish/manifold',
        sharedMeshInputs=True,forceGravityAndClutchOutsideScope=True))
    return probes


def main():
    p=argparse.ArgumentParser();p.add_argument('--skip-physics',action='store_true');p.add_argument('--skip-evaluation',action='store_true');a=p.parse_args()
    if list((QUALITY/'submissions').glob('**/*.json')):raise SystemExit('Human submissions exist; create a new round rather than replacing task identities.')
    if not a.skip_evaluation:check_evaluation()
    blind=pick_blind()
    if not a.skip_physics:build_physics(blind)
    probes=read(QUALITY/'physics-probes.private.json.gz')['probes'] if (QUALITY/'physics-probes.private.json.gz').exists() else []
    task_sha=digest([blind,[(p['code'],p['caseId'],p['state'],p['action']) for p in probes]])
    write(QUALITY/'review-tasks.private.json',dict(schema='brick-atlas-quality-review/1',blind=blind,
        physics=[{k:p[k] for k in ('code','caseId','sameAsBlindCase')} for p in probes],taskVersion=task_sha))
    write(QUALITY/'round-status.json',dict(blindTasks=len(blind),priorityTasks=sum(x['priority'] for x in blind),
        physicalProbes=len(probes),newStressConditions=read(QUALITY/'challenge-catalogue.json')['count'],
        publicSnapshotTasks=5720,taskVersion=task_sha,humanSubmissions=0,humanQualification='PENDING',apiCalls=0))
    print('ROUND READY',len(blind),'blind tasks;',len(probes),'mechanical probes',flush=True)


if __name__=='__main__':main()
