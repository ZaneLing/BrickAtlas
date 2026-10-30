"""Run the same agent and selected cases with interchangeable API backbones."""
import argparse,fcntl,json,re,time,uuid
from pathlib import Path
from bench_design.session import scheduled_of
from dynamic_arena import OUT as ARENA_OUT
from dynamic_arena.run import open_session,NoProvider
from dynamic_arena.transport import write_json
from unified_agent import RUN_OUT as OUT,PROTOCOL
from unified_agent.agent import VisualAgent
from unified_agent.profile import profile,for_session
from unified_agent.providers import PaidTransport,MODELS,LEDGER,total

CASES=('SC:4096-1-alt-1488:dynamic:buried-repair','D:obj-city-car--t5--removed_piece--v01')


def gate(normal,agent):
    return bool(normal and normal.get('success') is True and normal.get('arenaBranch')=='normal'
        and normal.get('caseId')==agent.session.row['key'] and normal.get('model')==agent.model
        and normal.get('inputVersion')==PROTOCOL and normal.get('agentContractSha256')==agent.contract_sha)


def execute(cid,model,condition,cap,configuration,normal=None,ledger_path=None,report_path=None):
    runid='agent-'+condition+'-'+re.sub('[^a-z0-9]+','-',model.lower()).strip('-')+'-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4]
    directory=ARENA_OUT/'runs'/runid
    session=open_session(cid,directory,model,condition=='normal')
    configuration=configuration or for_session(session)
    from unified_agent.readiness import require
    from unified_agent.casecheck import checked
    prerequisite=require(model,configuration)
    case_check=checked(cid,condition=='normal',images=True)
    if not case_check['passed']:raise ValueError('Case preflight failed: '+str(case_check))
    if case_check['moves']>configuration['maxActions'] or case_check['moves']+1>configuration['maxDecisions']:
        raise ValueError('Declared agent budget is below a verified feasible path')
    setup_error=None
    try:transport=PaidTransport(directory,cap,model,max_output=configuration['maxOutputTokensPerDecision'],ledger_path=ledger_path,
        reasoning_mode=configuration['reasoningMode'],timeout=configuration['requestTimeoutSeconds'])
    except Exception as exc:
        transport=NoProvider();transport.model=model;setup_error=str(exc)[:300]
    agent=VisualAgent(session,transport,configuration)
    if condition=='incident':
        if not gate(normal,agent):raise ValueError('Successful same-case, same-backbone, same-profile normal run is required')
        if not scheduled_of(session.ep):raise ValueError('Case has no incident schedule')
        session.normal_gate=dict(eligible=True,normalRunId=normal['arenaRunId'],sameCase=True,sameModel=True,
            sameAgentProfile=True,sharedPrefixVerified=False,
            interpretation='Independent normal prerequisite, not a matched-prefix causal estimate')
    print('START '+runid+' '+cid,flush=True)
    report_path=Path(report_path or OUT/'pilot.json')
    if report_path.exists():
        report=json.loads(report_path.read_text());report.pop('finishedAt',None)
        report['activeRun']=dict(arenaRunId=runid,caseId=cid,model=model,arenaBranch=condition,terminalStatus='running')
        write_json(report_path,report)
    if setup_error:
        session.terminal='service_error';agent.phase='finished';agent.spectator_frame();result=agent.result();result['setupError']=setup_error
        write_json(directory/'log.json',dict(protocol=PROTOCOL,calls=[],result=result));session.save()
    else:result=agent.run()
    result.update(arenaProtocol=PROTOCOL,arenaBranch=condition,arenaRunId=runid,actor=model,apiPreflight=prerequisite,casePreflight=case_check)
    for name in ['result.json','log.json','spectator.json']:
        path=directory/name
        value=result if name=='result.json' else json.loads(path.read_text())
        if name!='result.json':value['result']=result
        write_json(path,value)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--models',nargs='+',default=list(MODELS));p.add_argument('--cases',nargs='+',default=list(CASES))
    p.add_argument('--cap-usd',type=float,default=1.5);p.add_argument('--report',default='pilot.json')
    p.add_argument('--ledger',type=Path,default=LEDGER,help='Shared persistent cost ledger; never delete it to bypass a ceiling')
    a=p.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    report_path=OUT/a.report
    if report_path.exists():raise ValueError('Report already exists; never overwrite or silently repeat a paid pilot')
    report=dict(schema='brick-atlas-unified-agent-pilot/2',models=a.models,cases=a.cases,profile=profile(),
        budgetRule='Per-case public inventory and native limits; same for every backbone',
        planDeclaredBeforeCalls=True,repeats=1,startedAt=time.time(),runs=[],formalBenchmarkAggregate=False,
        incidentCondition='same case/backbone/profile normal success required; independent rollout, no shared-prefix causal claim')
    write_json(report_path,report)
    with (ARENA_OUT/'run.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        # Case-major order lets every backbone try the easier task first.
        for cid in a.cases:
            for model in a.models:
                try:normal=execute(cid,model,'normal',a.cap_usd,None,ledger_path=a.ledger,report_path=report_path)
                except ValueError as exc:
                    report.setdefault('notRun',[]).append(dict(caseId=cid,model=model,condition='normal-and-incident',reason='preflight_failed',detail=str(exc)[:400]))
                    write_json(report_path,report);continue
                report['runs'].append(normal);write_json(report_path,report)
                if normal['success'] is True:
                    report['runs'].append(execute(cid,model,'incident',a.cap_usd,normal['agentProfile'],normal,ledger_path=a.ledger,report_path=report_path))
                else:report.setdefault('notRun',[]).append(dict(caseId=cid,model=model,condition='incident',reason='normal_not_successful'))
                write_json(report_path,report)
                print('DONE '+model+' '+cid+' normal='+str(normal['success']),flush=True)
    if a.ledger.exists():
        ledger=json.loads(a.ledger.read_text());report['ledger']=dict(capUSD=ledger['capUSD'],budgetAccountedUpperUSD=total(ledger),
            confirmedUSD=sum(c.get('accountedUSD',0) for c in ledger['charges'] if c['status']=='settled'),
            estimatedNativeCosts={currency:sum(c.get('nativeCost',0) for c in ledger['charges'] if c.get('nativeCurrency')==currency and c['status']=='usage_estimated') for currency in ['USD','CNY']},
            unresolvedRequests=sum(c['status'] in ('pending','uncertain') for c in ledger['charges']))
    report['finishedAt']=time.time();write_json(report_path,report)
    print(json.dumps(report.get('ledger',{})),flush=True)


if __name__=='__main__':main()
