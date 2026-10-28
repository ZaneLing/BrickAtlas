"""One entry point for every dynamic task; normal success gates repair runs."""
import argparse,fcntl,json,re,time,uuid
from pathlib import Path
from bench_design.session import Session,scheduled_of,digest
from dynamic_arena import OUT
from dynamic_arena.catalogue import entry
from dynamic_arena.tool_arena import ToolArena,PROTOCOL,SYSTEM,TOOLS
from dynamic_arena.transport import Transport,write_json


class NoProvider:
    model='未调用 API · 题目预览'
    def usage(self):return dict(calls=0,costUSD=0.,capUSD=0.)


def open_session(cid,directory,actor,normal):
    r=entry(cid)
    s=Session.open(cid,directory,actor,diagnostic=r['diagnostic'],control=normal)
    s.row.setdefault('title',r['title']);return s


def preview(cid,normal=True):
    runid='preview-'+digest([cid,normal,PROTOCOL])[:20];directory=OUT/'runs'/runid
    path=directory/'spectator.json'
    if not path.exists():
        s=open_session(cid,directory,'scripted:preview',normal)
        arena=ToolArena(s,NoProvider(),min(60,s.cap));arena.spectator_frame()
    return runid


def task_digest(s,budget):
    from hashlib import sha256
    implementation={name:sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                    for name in ['tool_arena.py','sensors.py','plate_render.py']}
    return digest(dict(initial=s.initial,goal=s.goal,certificate=s.ep.runtime.cert,
        inventory=sorted(getattr(s.ep.runtime,'available',[])),budget=budget,
        protocol=PROTOCOL,system=SYSTEM,tools=TOOLS,implementation=implementation))


def gate(normal,s,model,budget):
    return bool(normal.get('success') and normal.get('caseId')==s.row['key'] and
        normal.get('actor')==model and normal.get('arenaProtocol')==PROTOCOL and
        normal.get('arenaBranch')=='normal' and normal.get('taskDigest')==task_digest(s,budget))


def execute(cid,model,condition,cap,max_decisions,normal=None):
    runid='arena-'+condition+'-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6]
    directory=OUT/'runs'/runid;s=open_session(cid,directory,model,condition=='normal')
    budget=min(max_decisions or s.cap,s.cap)
    if not 1<=budget<=s.cap:raise ValueError('Decision budget must be positive')
    contract_digest=task_digest(s,budget)
    if condition=='incident':
        if not normal or not gate(normal,s,model,budget):raise ValueError('Repair requires successful SAME case/model/input/budget normal result; run --condition pair first.')
        if not scheduled_of(s.ep):raise ValueError('This task has no intervention schedule; use normal.')
        s.normal_gate=dict(eligible=True,normalRunId=normal['arenaRunId'],sameCase=True,sameModel=True,sharedPrefixVerified=False)
    try:
        t=Transport(directory,cap=cap,model=model,ledger_path=OUT/'unified-ledger.private.json')
    except Exception as exc:
        t=NoProvider();t.model=model
        runner=ToolArena(s,t,min(max_decisions or s.cap,s.cap))
        s.terminal='service_error';runner.phase='finished';runner.spectator_frame()
        result=runner.result();result['setupError']=dict(type=type(exc).__name__,message=str(exc)[:160])
        write_json(directory/'log.json',dict(protocol=PROTOCOL,calls=[],result=result))
        s.save()
    else:
        result=ToolArena(s,t,min(max_decisions or s.cap,s.cap)).run()
    result.update(arenaProtocol=PROTOCOL,arenaBranch=condition,arenaRunId=runid,taskDigest=contract_digest,actor=model)
    write_json(directory/'result.json',result)
    # Preserve the gate in the replay's final metric panel as well.
    state=json.loads((directory/'spectator.json').read_text());state['result']=result;write_json(directory/'spectator.json',state)
    log=json.loads((directory/'log.json').read_text());log['result']=result;write_json(directory/'log.json',log)
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--id',required=True);p.add_argument('--model');p.add_argument('--condition',choices=['normal','incident','pair','preview'],default='pair');p.add_argument('--normal-run');p.add_argument('--cap-usd',type=float,default=1.);p.add_argument('--max-decisions',type=int)
    a=p.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    if a.condition=='preview':print(preview(a.id));return
    if not a.model:p.error('--model is required')
    with (OUT/'run.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        normal=None
        if a.normal_run:
            if not re.fullmatch(r'[a-zA-Z0-9_-]+',a.normal_run):p.error('Invalid run ID')
            normal=json.loads((OUT/'runs'/a.normal_run/'result.json').read_text())
        if a.condition in ('normal','pair'):
            normal=execute(a.id,a.model,'normal',a.cap_usd,a.max_decisions)
            print(json.dumps(normal,ensure_ascii=False),flush=True)
        if a.condition=='incident' or (a.condition=='pair' and normal['success'] and entry(a.id)['incidentBranch']):
            result=execute(a.id,a.model,'incident',a.cap_usd,a.max_decisions,normal)
            print(json.dumps(result,ensure_ascii=False),flush=True)
        elif a.condition=='pair':print(json.dumps(dict(repairStatus='not_applicable',reason='normal-not-successful' if not normal['success'] else 'normal-only-task')))


# Historical automatic-image recordings retain their original reader.
from dynamic_arena.legacy_run import ArenaRun

if __name__=='__main__':main()
