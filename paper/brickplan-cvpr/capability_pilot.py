"""Small preselected current-interface demonstration, within the old $3 ledger.

No retry, no scripted action, no prompted fault identity. These selected cases
illustrate behavior; they do not estimate benchmark-wide ability.
"""
from pathlib import Path
from copy import deepcopy
import base64,fcntl,hashlib,json,time
from release_assets import HERE,ROOT,read,write,sha
from bench_design.session import Session,digest
from bench_design.run_episode import SYSTEM as STATIC_SYSTEM,valid
from bench_design.run_autonomous import image_blocks
from dynamic_arena import OUT
from dynamic_arena.tool_arena import ToolArena,PROTOCOL
from dynamic_arena.transport import Transport
from dynamic_arena.run import task_digest,gate

LEDGER=OUT/'normal-pilot-ledger.private.json'
REPORT=HERE/'evidence/capability-pilot.json'
CAR='D:obj-city-car--t5--removed_piece--v01'
PLAN=[dict(key='static-color',caseId='E7:v7::v7-long-bookshelf::static::wrong-color::t14',model='openai/gpt-6.1-sol',budget=12,kind='static'),
      dict(key='car-normal',caseId=CAR,model='anthropic/claude-sonnet-5.5',budget=36,kind='normal'),
      dict(key='car-incident',caseId=CAR,model='anthropic/claude-sonnet-5.5',budget=36,kind='incident'),
      dict(key='static-access',caseId='E7:v7::v7-long-bookshelf::static::buried-repair::t7',model='openai/gpt-6.1-sol',budget=16,kind='static')]

def money():
 d=read(LEDGER)
 return dict(capUSD=d['capUSD'],confirmedUSD=sum(c['actualUSD'] or 0 for c in d['charges']),
  upperUSD=sum(c['actualUSD'] if c['actualUSD'] is not None else c['reservedUSD'] for c in d['charges']))

class VisibleTransport(Transport):
 def __call__(self,payload):
  reply=super().__call__(payload)
  try:a=json.loads(reply)
  except ValueError:a={'format':'invalid'}
  print(json.dumps({'run':self.directory.name,'call':self.usage()['calls'],'action':a,'costUSD':self.usage()['costUSD']},ensure_ascii=False),flush=True)
  return reply

def static_run(s,t,cap):
 s.cap=cap;calls=[];history=[]
 for number in range(1,cap+1):
  try:
   obs=s.observe();blocks=image_blocks(obs)
   payload=dict(messages=[dict(role='system',content=STATIC_SYSTEM),*history,dict(role='user',content=blocks)])
  except Exception as e:
   s.terminal='harness_error';calls.append(dict(index=number,error=dict(type=type(e).__name__,message=str(e)[:160])));break
  public=deepcopy(obs)
  for im in public['images']:im['file']=str(Path(im['file']).relative_to(ROOT))
  try:reply=t(payload)
  except Exception as e:
   s.terminal='service_error';calls.append(dict(index=number,modelInput=public,error=dict(type=type(e).__name__,message=str(e)[:160])));break
  try:a=json.loads(reply)
  except ValueError:a={'type':'invalid'}
  fb=s.submit(a if isinstance(a,dict) else {'type':'invalid'},parse_error=not valid(a),request_evidence=dict(requestContextSha256=digest(payload)))
  calls.append(dict(index=number,modelInput=public,modelOutputRaw=reply,modelOutput=a,environmentOutput=fb,
    providerReceipt=dict(id=t.latest['result']['id'],requestBodySha256=t.latest['requestBodySha256'],costUSD=t.latest['result']['usage']['cost'])))
  history.extend([dict(role='user',content=[b for b in blocks if b['type']=='text']),
                  dict(role='assistant',content=reply),dict(role='user',content=json.dumps(dict(feedback=fb)))])
  if s.done:break
 if not s.done:s.terminal='model_budget_exhausted'
 s.save();result=s.result();result.update(apiCalls=t.usage()['calls'],providerUsage=t.usage(),
     controllerMetrics=dict(decisions=len(calls),budget=cap),staticAdapter='unchanged-Session.observe-and-direct-JSON')
 write(s.directory/'log.json',dict(protocol=result['inputVersion'],calls=calls,result=result))
 return result

def main():
 assert not REPORT.exists(),'The selected pilot already exists; do not silently rerun.'
 start=money();assert start['capUSD']==3 and start['upperUSD']<3
 report=dict(schema='brick-atlas-selected-capability-pilot/1',selection='Declared before execution; all planned outcomes retained.',
   plan=PLAN,startedAt=time.time(),initialLedger=start,runs=[],formalBenchmarkAggregate=False)
 write(REPORT,report)
 with (OUT/'run.lock').open('w') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  normal=None
  for item in PLAN:
   if item['kind']=='incident' and (normal is None or not normal['success']):
    report['runs'].append(dict(**item,status='not_run_normal_failed'));write(REPORT,report);continue
   if money()['upperUSD']>2.55:
    report['runs'].append(dict(**item,status='not_run_budget'));write(REPORT,report);continue
   runid='capability-'+item['key']+'-'+time.strftime('%Y%m%d-%H%M%S');directory=OUT/'runs'/runid
   s=Session.open(item['caseId'],directory,item['model'],control=item['kind']=='normal')
   if item['kind']=='incident':
    assert gate(normal,s,item['model'],item['budget'])
    s.normal_gate=dict(eligible=True,normalRunId=normal['arenaRunId'],sameCase=True,sameModel=True,sharedPrefixVerified=False)
   t=VisibleTransport(directory,cap=3.,model=item['model'],ledger_path=LEDGER)
   print('START '+item['key'],flush=True)
   if item['kind']=='static':result=static_run(s,t,item['budget'])
   else:
    result=ToolArena(s,t,item['budget']).run()
    result.update(arenaRunId=runid,arenaBranch=item['kind'],arenaProtocol=PROTOCOL,actor=item['model'],taskDigest=task_digest(s,item['budget']))
    if item['kind']=='normal':normal=result
   write(directory/'result.json',result)
   log=read(directory/'log.json');log['result']=result;write(directory/'log.json',log)
   if (directory/'spectator.json').exists():
    spec=read(directory/'spectator.json');spec['result']=result;write(directory/'spectator.json',spec)
   report['runs'].append(dict(**item,runId=runid,status=result['terminalStatus'],success=result['success'],result=result))
   report['finalLedger']=money();report['additionalConfirmedUSD']=report['finalLedger']['confirmedUSD']-start['confirmedUSD']
   report['additionalUpperUSD']=report['finalLedger']['upperUSD']-start['upperUSD'];write(REPORT,report)
   print('DONE '+item['key']+' '+str(result['success'])+' '+result['terminalStatus'],flush=True)
 report['finalLedger']=money();report['finishedAt']=time.time();write(REPORT,report)

if __name__=='__main__':main()
