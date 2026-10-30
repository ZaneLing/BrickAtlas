"""Maintain reports; continue untouched cases after isolated truncation.

Does not repeat an answered or interrupted condition, change prompts/budgets,
repair actions, reconcile uncertain billing, or bypass failed API certificates.
"""
import argparse,fcntl,json,os,subprocess,sys,time
from pathlib import Path
from unified_agent.experiment_batch import OUT,MODELS,PROTOCOL,slug,ledger_path,merged
from dynamic_arena.transport import write_json


def unlocked(model):
    with (OUT/'workers'/(slug(model)+'.lock')).open('a') as f:
        try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return False
    return True


def main():
    p=argparse.ArgumentParser();p.add_argument('--models',nargs='*',default=[]);p.add_argument('--reports-only',action='store_true');a=p.parse_args()
    if any(m not in MODELS for m in a.models):raise ValueError('Unknown model')
    path=OUT/'monitor.json';lock=(OUT/'monitor.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    state=json.loads(path.read_text()) if path.exists() else dict(continuations=[])
    state.update(pid=os.getpid(),startedAt=time.time(),models=a.models,reportsOnly=a.reports_only,active=True)
    seen={r['afterRun'] for r in state['continuations']};last_count=-1;last_report=0;children={}
    while not (OUT/'STOP_MONITOR').exists():
        report=merged();count=len(report['runs'])
        for child in children.values():child.poll()
        if (count!=last_count and time.time()-last_report>180) or report['allWorkersFinished']:
            for module in ['experiment_report','experiment_pdf']:
                with (OUT/(module+'.log')).open('a') as log:
                    result=subprocess.run([sys.executable,'-m','unified_agent.'+module],stdout=log,stderr=subprocess.STDOUT)
                state[module+'ExitCode']=result.returncode
            last_count=count;last_report=time.time();state['lastReportAt']=last_report
        for model in a.models if not a.reports_only else []:
            if not unlocked(model):continue
            rp=OUT/'workers'/(slug(model)+'.json')
            if not rp.exists():continue
            worker=json.loads(rp.read_text());block=worker.get('blockedReason') or {}
            runs=[r for r in worker['runs'] if r['inputVersion']==PROTOCOL]
            if not runs or worker.get('activeRun') or worker.get('finishedAt'):continue
            if block.get('terminal')!='output_truncated' or block.get('runId') in seen:continue
            # Repeated consecutive truncation needs a new interface review.
            if len(runs)>1 and all(r['terminalStatus']=='output_truncated' for r in runs[-2:]):continue
            ledger=json.loads(ledger_path(model).read_text())
            if any(c['status'] in ('pending','uncertain') for c in ledger['charges']):continue
            uid=block['runId'];seen.add(uid)
            state['continuations'].append(dict(model=model,afterRun=uid,at=time.time(),
                action='continue remaining registered conditions; do not rerun truncated condition',budgetChanged=False))
            write_json(path,state)
            log=(OUT/'workers'/(slug(model)+'.continuation.log')).open('a')
            children[model]=subprocess.Popen([sys.executable,'-m','unified_agent.experiment_batch','--model',model,'--resume'],stdout=log,stderr=subprocess.STDOUT)
            log.close()
        state.update(updatedAt=time.time(),archivedRuns=count,allWorkersFinished=report['allWorkersFinished'],
            pendingModels=report['pendingModels'])
        write_json(path,state)
        if report['allWorkersFinished']:break
        time.sleep(15)
    state['active']=False;state['stoppedAt']=time.time();write_json(path,state)


if __name__=='__main__':main()
