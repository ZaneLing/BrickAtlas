"""No-API feasibility and rendered visibility checks for the registered sample."""
import json,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from unified_agent.experiment_batch import OUT
from unified_agent.casecheck import checked
from dynamic_arena.transport import write_json


def main():
    plan=json.loads((OUT/'plan.json').read_text());tasks=set()
    for jobs in plan['jobs'].values():
        for job in jobs:
            tasks.add((job['caseId'],job['condition']=='normal'))
            if job['scheduledEvents']:tasks.add((job['caseId'],False))
    rows=[];started=time.time()
    with ProcessPoolExecutor(max_workers=3) as pool:
        futures={pool.submit(checked,cid,normal,True):(cid,normal) for cid,normal in tasks}
        for f in as_completed(futures):
            row=f.result();rows.append(row)
            if not row['passed'] or len(rows)%10==0:print('CASE_CHECK',len(rows),'/',len(tasks),row['caseId'],row.get('error','PASS'),flush=True)
    result=dict(passed=all(r['passed'] for r in rows),rows=rows,apiCalls=0,elapsedSeconds=time.time()-started,
        notIndependentPhysics=True,notHumanReadabilityProof=True)
    write_json(OUT/'checks/selected-cases.json',result)
    print('CHECKED',len(rows),'FAILED',sum(not r['passed'] for r in rows),flush=True)


if __name__=='__main__':main()
