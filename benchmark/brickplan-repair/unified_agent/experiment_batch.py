"""Expanded, predeclared experiment. One backbone worker and ledger per model.

Only explicit HTTP 429 rejections without generation may be retried. Actual
model decisions, truncations and uncertain requests are never silently retried.
"""
import argparse,fcntl,json,time,hashlib
from pathlib import Path
from unified_agent import ROOT,PROTOCOL
from unified_agent.ark_batch import MODELS,IsolatedViewerAgent
from unified_agent.providers import PaidTransport,total
from unified_agent.failures import ProviderError
from unified_agent.readiness import probe
from unified_agent.run import execute
from dynamic_arena.transport import write_json

OUT=ROOT/'deliverables/brick-atlas-experiments-v3'


def slug(model):return model.replace('/','--')
def ledger_path(model):return OUT/'ledgers'/(slug(model)+'.json')


class BatchTransport:
    def __init__(self,*args,**kwargs):self.inner=PaidTransport(*args,**kwargs)
    def __getattr__(self,key):return getattr(self.inner,key)
    def __call__(self,payload):
        for attempt in range(4):
            try:return self.inner(payload)
            except ProviderError as exc:
                last=self.inner.ledger['charges'][-1] if self.inner.ledger.get('charges') else {}
                if exc.status!=429 or last.get('status')!='rejected_before_generation' or attempt==3:raise
                path=self.directory/'rate-limit-retries.json'
                rows=json.loads(path.read_text()) if path.exists() else []
                delay=65*(attempt+1)
                rows.append(dict(archiveId=last['id'],reason='HTTP 429 with no generation',delaySeconds=delay,
                    taskStateUnchanged=True,samePayload=True,at=time.time()))
                write_json(path,rows)
                print('WAIT_RATE_LIMIT',self.model,delay,'seconds; no generated answer repeated',flush=True)
                time.sleep(delay)


def merged():
    reports=[json.loads(p.read_text()) for p in sorted((OUT/'workers').glob('*.json'))]
    runs=[r for p in reports for r in p['runs']]
    missing=[r for p in reports for r in p.get('notRun',[])]
    api=[];costs={};plan=json.loads((OUT/'plan.json').read_text())
    hello_path=OUT/'diagnostics/hello-20261030/summary.json'
    hello={r['model']:r for r in json.loads(hello_path.read_text())} if hello_path.exists() else {}
    for model in MODELS:
        path=OUT/'preflight'/slug(model)/'certificate.json'
        if path.exists():
            c=json.loads(path.read_text());api.append(dict(model=model,passed=c['passed'],inferenceModel=c['inferenceModel'],error=c.get('error',{}).get('code'),
                errorMessage=c.get('error',{}).get('message'),passedProbes=len(c.get('probes',[])),checkedAt=c['checkedAt'],checkType='image-history-contract',requiredProbes=3))
        elif model in hello:
            c=hello[model];api.append(dict(model=model,passed=False,inferenceModel=c['inferenceModel'],error=c.get('error',{}).get('code'),
                errorMessage=c.get('error',{}).get('message'),checkType='hello-only',helloPassed=c['httpPassed'],passedProbes=0,requiredProbes=3))
        else:api.append(dict(model=model,passed=False,error='NOT_CHECKED',passedProbes=0,requiredProbes=3,checkType='none'))
        path=ledger_path(model)
        if path.exists():
            ledger=json.loads(path.read_text());costs[model]=dict(estimateCNY=sum(c.get('nativeCost',0) for c in ledger['charges']),
                requests=len(ledger['charges']),uncertain=sum(c['status'] in ('pending','uncertain') for c in ledger['charges']))
    return dict(protocol=PROTOCOL,runs=runs,notRun=missing,apiStatus=api,costs=costs,
        pendingModels=[m for m in MODELS if not any(p['model']==m and p.get('finishedAt') for p in reports)],
        plannedBaseRuns=sum(len(j) for j in plan['jobs'].values()),
        activeRuns=[p['activeRun'] for p in reports if p.get('activeRun')],
        workers=[{k:p.get(k) for k in ('model','finishedAt','blockedReason','startedAt')} for p in reports],
        allWorkersFinished=len(reports)==len(MODELS) and all(p.get('finishedAt') for p in reports))


def main():
    p=argparse.ArgumentParser();p.add_argument('--model',required=True,choices=MODELS)
    p.add_argument('--preflight-only',action='store_true');p.add_argument('--refresh-preflight',action='store_true')
    p.add_argument('--resume',action='store_true');a=p.parse_args()
    if (OUT/'completed.json').exists():raise ValueError('Completed experiment; no new paid calls allowed')
    plan=json.loads((OUT/'plan.json').read_text());cap=plan['modelBudgetCNY'][a.model]*.2
    (OUT/'workers').mkdir(exist_ok=True,parents=True)
    lock=(OUT/'workers'/(slug(a.model)+'.lock')).open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    path=OUT/'workers'/(slug(a.model)+'.json')
    report=json.loads(path.read_text()) if path.exists() else dict(model=a.model,protocol=PROTOCOL,startedAt=time.time(),runs=[],notRun=[],
        planSha256=hashlib.sha256((OUT/'plan.json').read_bytes()).hexdigest(),
        staticInterpretation='Static checkpoint operated by the common visual agent, not one-shot answering.',
        incidentCondition='Same case/backbone/profile successful independent normal branch required')
    if path.exists() and not a.resume and not a.preflight_only:raise ValueError('Existing report: explicit --resume required')
    if report.get('activeRun'):raise ValueError('Reconcile prior active run before resume; never silently repeat it')
    cert=probe(a.model,cap,ledger_path(a.model),a.refresh_preflight,root=OUT,transport_factory=BatchTransport)
    if a.preflight_only:return
    if not cert['passed']:
        report['blockedReason']=cert.get('error');write_json(path,report);return
    report.pop('blockedReason',None);report.pop('finishedAt',None);write_json(path,report)
    done={(r['caseId'],r['arenaBranch']) for r in report['runs']}
    done.update((r['caseId'],r['condition']) for r in report['notRun'])
    def run(job,condition,normal=None):
        cid=job['caseId'];key=(cid,condition)
        if key in done:return next((r for r in report['runs'] if (r['caseId'],r['arenaBranch'])==key),None)
        if condition=='incident' and (not normal or normal.get('success') is not True):
            report['notRun'].append(dict(model=a.model,caseId=cid,condition=condition,group=job['group'],objectTitle=job['title'],reason='normal_not_successful'))
            done.add(key);write_json(path,report);return
        result=execute(cid,a.model,condition,cap,normal['agentProfile'] if normal else None,normal,
            ledger_path=ledger_path(a.model),report_path=path,certificate_root=OUT,
            transport_factory=BatchTransport,agent_factory=IsolatedViewerAgent)
        result.update(objectTitle=job['title'],objectId=job['model'],lengthGroup=job['difficulty'],
            activeParts=job['activeParts'],sampleGroup=job['group'],errorFamily=job['family'],sampleIndex=job['sampleIndex'])
        report['runs'].append(result);report.pop('activeRun',None);done.add(key);write_json(path,report)
        print('RESULT',a.model,job['sampleIndex'],condition,result['terminalStatus'],result['success'],flush=True)
        if result['terminalStatus'] in ('client_budget_exhausted','output_truncated','harness_error','provider_output_error','service_error'):
            # Stop at an infrastructure problem, instead of burning through
            # the rest of the task list with known-broken inputs or quota.
            report['blockedReason']=dict(runId=result['arenaRunId'],terminal=result['terminalStatus'])
            write_json(path,report);raise SystemExit(2)
        return result
    for job in plan['jobs'][a.model]:
        if job['condition']=='static':run(job,'static')
        else:
            normal=run(job,'normal')
            if job['scheduledEvents']:run(job,'incident',normal)
    report['finishedAt']=time.time();write_json(path,report)
    print('FINISHED',a.model,'runs',len(report['runs']),'notRun',len(report['notRun']),flush=True)


if __name__=='__main__':main()
