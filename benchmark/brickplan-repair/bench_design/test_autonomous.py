"""Scripted harness checks only. These are NOT results from an AI model."""
from copy import deepcopy
from pathlib import Path
import json
from bench_design.run_autonomous import AutonomousRun,decode,PRIVATE_FIELDS
from bench_design.session import Session,internal_action
from bench_design.challenges import QUALITY
from expansion_v7.designs import certificate
from expansion_v7.runtime import Episode,runtime,move
from expansion_v7.run_episode import Packet
from expansion_v7.build import write

ROOT=Path('/tmp/brick-autonomous-control-check')


def fixture(name,events=True):
    spec=dict(name='全程控制验证小桌',family='takeover-fixture',category='furniture',wrongColorActor='P002',wrongColor='#9b59b6',
        parts=[('F001','3005',-30,-24,-10,'#a66b35',0),('P001','3005',30,-24,-10,'#a66b35',0),
               ('P002','3005',-30,-24,10,'#a66b35',0),('P003','3005',30,-24,10,'#a66b35',0),
               ('P004','3020',0,-32,0,'#0055bf',0)])
    cert=certificate('takeover-fixture',spec);rt=runtime(cert)
    normal=[move(a,a+':goal') for a in ['F001','P001','P002','P003','P004']]
    case=dict(id='scripted-fixture:'+name,mode='dynamic',family='missing',initial={a:'' for a in rt.actors},goal=rt.goal,
        events=[dict(family='missing',minimumInstalled=3)] if events else [],completedInstructionStep=0,
        # Deliberately unusable witnesses: the controller must never run these.
        referenceActions=[dict(type='detach',actor='ORACLE_MUST_NOT_RUN')],oraclePlan=['POISON'],
        referenceEvents=[dict(recovery=['POISON'])])
    ep=Episode(cert,case,41);folder=ROOT/name;packet=Packet(ep,dict(actions=normal,states=[]),folder)
    row=dict(key=case['id'],bank='E7',model='takeover-fixture',mode='dynamic',case=deepcopy(case),
        evaluationMetadata=dict(canonicalId=case['id'],taskType='D1' if events else 'D0',track='whole-object-dynamic',source='original:takeover-fixture',model='takeover-fixture'))
    s=Session(row,ep,packet,None,folder,actor='scripted:controller-proof');s.autosave=False
    return s,normal


class ScriptedPolicy:
    def __init__(self,actions):self.actions=iter(actions);self.requests=[]
    def __call__(self,request):
        text=json.dumps(request,ensure_ascii=False)
        # Case poison, hidden ledger and action witnesses never enter prompts.
        assert 'ORACLE_MUST_NOT_RUN' not in text and 'POISON' not in text
        assert 'recoveryWitness' not in text and 'nextUnexecutedGuideAction' not in text
        assert request['messages'][0]['role']=='system'
        if self.requests:
            assert any(m['role']=='assistant' for m in request['messages'])
            assert len(request['messages'])>len(self.requests[-1]['messages'])
        self.requests.append(request)
        return next(self.actions)


def main():
    results=[]
    s,normal=fixture('continuous')
    # A different legal order from the normal witness. After the third attach,
    # the event removes P001. The policy continues one other leg before repair.
    chosen=[move(a,a+':goal') for a in ['P001','F001','P003','P002','P001','P004']]
    actions=[internal_action(s.ep,a) for a in chosen]
    actions.insert(3,dict(type='inspect_history',step=1));actions.append(dict(type='finish'))
    policy=ScriptedPolicy(actions);run=AutonomousRun(s,policy,max_decisions=12);out=run.run()
    assert out['normalizedResult']['success'] and out['normalizedResult']['appliedEvents']==1
    assert out['stageResets']==out['automaticRepairActions']==out['scriptedPrefixActions']==0
    assert out['historyQueries']==1 and len(s.records)==7
    assert [r['action'] for r in s.records[:-1]]==[internal_action(s.ep,a) for a in chosen]
    assert s.events[0]['native']['affected']==['P001']
    assert s.records[3]['action']==internal_action(s.ep,move('P002','P002:goal'))
    assert s.records[3]['after']['P001']=='' # no automatic repair while continuing
    history_request=policy.requests[4]
    assert any('HISTORICAL STEP 1 - NOT CURRENT' in b.get('text','') for b in history_request['messages'][-1]['content'])
    assert len(s.ep.events)==1 and s.ep.successful_installs==6
    results.append(dict(check='all-actions-from-policy-different-order-delayed-repair-history-no-reset',passed=True,acceptedMoves=6,historyQueries=1))
    s,_=fixture('premature-finish');policy=ScriptedPolicy([dict(type='finish')]);out=AutonomousRun(s,policy).run()
    assert not out['normalizedResult']['success'] and out['normalizedResult']['incidentExposure']=='untriggered'
    assert not any(s.ep.state.values()) and len(s.records)==1
    results.append(dict(check='policy-finish-is-final-no-oracle-rescue',passed=True))
    s,_=fixture('bad-format');policy=ScriptedPolicy(['[]',dict(type='finish')]);out=AutonomousRun(s,policy).run()
    assert out['normalizedResult']['executionMetrics']['formatErrorResponses']==1
    assert not any(s.ep.state.values())
    results.append(dict(check='malformed-output-never-replaced-by-reference-action',passed=True))
    s,_=fixture('transport-error')
    def failed(_):raise TimeoutError('scripted transport failure')
    out=AutonomousRun(s,failed).run();assert out['normalizedResult']['terminalStatus']=='service_error'
    assert out['normalizedResult']['success'] is None and not s.records
    results.append(dict(check='service-error-separated-from-ability',passed=True))
    s,_=fixture('harness-error')
    def broken_observation():raise OSError('scripted renderer failure')
    s.observe=broken_observation
    out=AutonomousRun(s,lambda _:dict(type='finish')).run()
    assert out['normalizedResult']['terminalStatus']=='harness_error' and out['normalizedResult']['success'] is None
    assert not s.records
    results.append(dict(check='harness-error-never-becomes-a-model-ability-failure',passed=True))
    s,_=fixture('module-scope');s.row['evaluationMetadata']['track']='named-module-dynamic'
    try:AutonomousRun(s,lambda _:dict(type='finish'));raise AssertionError('Module was mislabeled as whole-object takeover')
    except ValueError as e:assert 'module' in str(e)
    results.append(dict(check='module-is-not-silently-counted-as-full-object-control',passed=True))
    s,_=fixture('no-scripted-prefix');s.submit(internal_action(s.ep,move('F001','F001:goal')))
    try:AutonomousRun(s,lambda _:dict(type='finish'));raise AssertionError('Scripted prefix accepted')
    except ValueError:pass
    results.append(dict(check='scripted-start-rejected',passed=True))
    assert decode('null')==decode('[]')==dict(type='invalid')
    write(QUALITY/'autonomous-control-check.json',dict(status='PASS',checks=results,
        validationActor='scripted controller fixture, not an AI model',paidModelCalls=0,apiCostUSD=0,
        realHumanVotesWritten=0,formalModelPerformanceMeasured=False))
    print('PASS',len(results),'autonomous controller checks; scripted fixtures only, no model calls')


if __name__=='__main__':main()
