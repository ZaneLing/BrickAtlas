"""Fresh, no-API feasibility and public-handle checks for selected/all cases."""
import argparse,hashlib,json,tempfile,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
from bench_design.session import Session
from dynamic_arena.validate_replays import Witness
from dynamic_arena.sensors import Sensors
from dynamic_arena.transport import write_json
from unified_agent import ROOT,RUN_OUT
from unified_agent.profile import for_session


def one(cid,normal=False,images=False):
    with tempfile.TemporaryDirectory() as tmp:
        s=Session.open(cid,tmp,'scripted:readiness',control=normal);s.autosave=False
        config=for_session(s);sensors=Sensors(s);handles=sensors.handles()
        ids={h['id']:set(h['candidates']) for h in handles}
        assert len(ids)==len(handles) and all(ids.values()),'Empty or duplicate public handle'
        initial_correct=s.ep.runtime.signature(s.initial)==s.ep.runtime.signature(s.goal)
        kind='D0' if normal else s.row['evaluationMetadata']['taskType']
        if kind=='S0':assert initial_correct,'S0 is not correct'
        if kind=='S1':assert not initial_correct,'Static fault is already correct'
        witness=Witness(s);moves=0
        for _ in range(2*s.cap+4):
            a=json.loads(witness({}));tool,args=a['tool'],a['args']
            if tool=='observe':continue
            if tool in ('attach','detach'):
                assert args['partId'] in ids,'Missing part handle'
                if tool=='attach':assert args['candidate'] in ids[args['partId']],'Candidate belongs to another part'
                moves+=1
            feedback=s.submit(dict(type=tool,**args))
            # Native D episodes name a successful finish SUCCESS; the newer
            # community engine uses FINISHED. Neither spelling implies a move.
            assert feedback['code']=='OK' or (tool=='finish' and feedback['code'] in ('FINISHED','SUCCESS')),str(feedback['code'])
            if s.done:break
        r=s.result();assert r['success'],'Reference failed'
        assert moves<=config['maxActions'] and len(s.records)<=config['maxDecisions'],'Configured agent budget cannot execute a feasible witness'
        if r['scheduledEvents']:assert r['repairApplicable'],'Reference failed to trigger effective scheduled incidents'
        if images:
            pairs=[(sensors.render(s.initial,v),sensors.render(s.goal,v)) for v in ('isometric','rear','top')]
            assert all(a.size==b.size==(800,600) for a,b in pairs)
            if kind=='S1':assert any(a.tobytes()!=b.tobytes() for a,b in pairs),'Fault invisible in three views'
        fingerprint=hashlib.sha256(json.dumps([s.ep.case,s.ep.runtime.cert],sort_keys=True,default=str).encode()).hexdigest()
        return dict(caseId=cid,normal=normal,passed=True,taskType=kind,moves=moves,
            applied=r['appliedEvents'],scheduled=r['scheduledEvents'],config=config,physicalTaskSha256=fingerprint)


def checked(cid,normal=False,images=False):
    try:return one(cid,normal,images)
    except Exception as exc:return dict(caseId=cid,normal=normal,passed=False,error=str(exc)[:400])


def main():
    p=argparse.ArgumentParser();p.add_argument('--all',action='store_true');p.add_argument('--cases',nargs='+');p.add_argument('--workers',type=int,default=3)
    p.add_argument('--recheck-failed',type=Path,help='Replay every failed row; preserve the prior audit and merge fresh results')
    a=p.parse_args();data=ROOT/'deliverables/brick-atlas-dataset-v1';started=time.time()
    questions=[json.loads(l) for mode in ('static','dynamic') for l in (data/'questions'/f'{mode}.jsonl').read_text().splitlines()]
    previous=json.loads(a.recheck_failed.read_text()) if a.recheck_failed else None
    ids=[r['caseId'] for r in previous['rows'] if not r['passed']] if previous else [q['id'] for q in questions] if a.all else a.cases
    if not ids:raise ValueError('Specify --all or --cases')
    rows=[]
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        futures={pool.submit(checked,cid,False,False):cid for cid in ids}
        for f in as_completed(futures):
            r=f.result();rows.append(r)
            if not r['passed'] or len(rows)%100==0:print('CHECK',len(rows),'/',len(ids),r['caseId'],r.get('error','PASS'),flush=True)
    if previous:
        write_json(a.recheck_failed.with_name(a.recheck_failed.stem+'-before-recheck.json'),previous)
        rows=[r for r in previous['rows'] if r['passed']]+rows
    write_json(a.recheck_failed or RUN_OUT/'checks'/('all-cases.json' if a.all else 'selected-cases.json'),dict(passed=all(r['passed'] for r in rows),
        checked=len(rows),elapsedSeconds=time.time()-started,apiCalls=0,cachedReplayUsed=False,
        priorCheckElapsedSeconds=previous.get('elapsedSeconds') if previous else None,recheckedCases=len(ids) if previous else 0,
        independentPhysicsEngine=False,notHumanReadabilityProof=True,rows=rows))
    print('DONE',len(rows),'failed',sum(not r['passed'] for r in rows),flush=True)


if __name__=='__main__':main()
