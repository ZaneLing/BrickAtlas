"""Paid interface probes, not capability trials. A current pass gates experiments."""
import argparse,hashlib,json,time,tempfile,uuid
from pathlib import Path
from dynamic_arena.run import open_session
from dynamic_arena.transport import write_json
from dynamic_arena.contract import validate
from unified_agent import ROOT,RUN_OUT,PROTOCOL
from unified_agent.agent import VisualAgent
from unified_agent.profile import for_session
from unified_agent.providers import PaidTransport,MODELS,total
from unified_agent.failures import describe

FILES=['unified_agent/agent.py','unified_agent/profile.py','unified_agent/providers.py','unified_agent/failures.py',
       'dynamic_arena/contract.py','dynamic_arena/tool_arena.py','dynamic_arena/sensors.py','dynamic_arena/transport.py','assembly.py','bench_design/session.py','bench_design/metrics.py']
CHECK_CASE='SC:4096-1-alt-1488:dynamic:buried-repair'


def source_digest():
    base=ROOT/'benchmark/brickplan-repair'
    return hashlib.sha256(b''.join((base/n).read_bytes() for n in FILES)).hexdigest()


def certificate_path(model):return RUN_OUT/'preflight'/model.replace('/','--')/'certificate.json'


def require(model,config):
    path=certificate_path(model)
    if not path.exists():raise ValueError('Missing API preflight; run python -m unified_agent.readiness --models '+model)
    c=json.loads(path.read_text())
    if not c.get('passed') or c['sourceSha256']!=source_digest() or not 0<=time.time()-c['checkedAt']<=86400:
        raise ValueError('API preflight failed, expired or code changed; rerun interface check')
    for field in ('maxOutputTokensPerDecision','reasoningMode','requestTimeoutSeconds'):
        if c['profile'][field]!=config[field]:raise ValueError('API generation configuration differs from preflight: '+field)
    return dict(certificate=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),checkedAt=c['checkedAt'])


def probe(model,cap,ledger,refresh=False):
    certificate=certificate_path(model);base=certificate.parent
    if certificate.exists():
        previous=json.loads(certificate.read_text())
        if not refresh:
            if previous.get('passed') and previous['sourceSha256']==source_digest() and 0<=time.time()-previous['checkedAt']<=86400:
                print(model,'CACHED PASS (no API call)',flush=True);return previous
            raise ValueError('Preflight failed/expired/changed; use --refresh to archive and recheck')
        write_json(base/'history'/(str(int(previous['checkedAt']))+'-'+uuid.uuid4().hex[:6]+'.json'),previous)
    directory=base/('attempt-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6])
    directory.mkdir(parents=True,exist_ok=True)
    result=dict(model=model,protocol=PROTOCOL,sourceSha256=source_digest(),checkedAt=time.time(),passed=False,
        purpose='API/schema/image receipt checks; no assembly competence claim',probes=[],apiConfigurationPinned=True,archiveDirectory=str(directory.relative_to(ROOT)))
    try:
        s=open_session(CHECK_CASE,directory,model,True);s.autosave=False
        config=for_session(s);result['profile']=config
        transport=PaidTransport(directory,cap,model,ledger_path=ledger,max_output=config['maxOutputTokensPerDecision'],
            reasoning_mode=config['reasoningMode'],timeout=config['requestTimeoutSeconds'])
        a=VisualAgent(s,transport,config);a.spectator_frame=lambda *args:None
        for i in range(2):
            if i:
                # Explicit scripted sensor setup for the API check; no physical
                # actions, no private witness, and never benchmark evidence.
                a.execute(dict(tool='observe',args=dict(view='angled',rotateDegrees=90,show=['current'])),100)
                a.execute(dict(tool='observe',args=dict(view='top',rotateDegrees=0,show=['current','inventory'])),101)
                first=a.sensors.handles()[0]['id']
                a.execute(dict(tool='inspect',args=dict(partId=first,page=1)),102)
            provider,readable,visible,images=a.request()
            wanted=dict(tool='observe',args=dict(view='angled',rotateDegrees=90,show=['current','inventory'])) if i==0 else dict(tool='observe',args=dict(view='top',rotateDegrees=0,show=['current']))
            instruction='API INTERFACE CHECK ONLY, not an assembly trial. Read the supplied images and tool contract. Return exactly this tool call as JSON, optionally adding short plan/notes: '+json.dumps(wanted)+'. Do not solve or install anything.'
            provider['messages'][-1]['content'].append(dict(type='text',text=instruction))
            readable['messages'][-1]['content'].append(dict(type='text',value=instruction))
            before=json.dumps(s.ep.state,sort_keys=True)
            reply=transport(provider);validation=validate(reply,memory=True,limits=config)
            assert validation['valid'],validation['errors']
            assert {k:validation['action'][k] for k in ('tool','args')}==wanted,'Model did not follow the interface probe'
            assert json.dumps(s.ep.state,sort_keys=True)==before
            receipt=transport.latest
            result['probes'].append(dict(index=i+1,passed=True,input=readable,inputImages=len(images),
                rawOutput=reply,validation=validation,receipt={k:v for k,v in receipt.items() if k!='result'},
                finishReason=receipt['result']['choices'][0]['finish_reason'],usage=receipt['result']['usage']))
            if i==0:a.step(reply,(provider,readable,visible,images))
        result['passed']=True;result['usage']=transport.usage()
    except Exception as exc:
        result['error']=describe(exc)
        if 'transport' in locals():result['usage']=transport.usage()
    result['checkedAt']=time.time();write_json(directory/'certificate.json',result);write_json(certificate,result)
    print(model,'PASS' if result['passed'] else 'BLOCKED',result.get('error',{}).get('message',''),flush=True)
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--models',nargs='+',default=list(reversed(MODELS)))
    p.add_argument('--cap-usd',type=float,default=.4);p.add_argument('--ledger',type=Path,default=RUN_OUT/'preflight-ledger.private.json')
    p.add_argument('--refresh',action='store_true',help='Keep prior evidence and rerun paid checks in new attempt directories')
    a=p.parse_args();rows=[]
    for model in a.models:rows.append(probe(model,a.cap_usd,a.ledger,a.refresh))
    ledger=json.loads(a.ledger.read_text()) if a.ledger.exists() else {'charges':[]}
    write_json(RUN_OUT/'api-preflight.json',dict(passed=all(r['passed'] for r in rows),rows=rows,capUSD=a.cap_usd,
        budgetAccountedUpperUSD=total(ledger),retries=0,purpose='Interface acceptance only; not benchmark scores'))


if __name__=='__main__':main()
