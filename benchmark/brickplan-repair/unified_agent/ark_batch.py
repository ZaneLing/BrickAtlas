"""Authorized Ark + Aliyun Qwen pilot. One attempt per scheduled condition."""
import argparse,fcntl,json,time,os
from pathlib import Path
from unified_agent import ROOT,PROTOCOL
from dynamic_arena import OUT as ARENA
from dynamic_arena.transport import write_json
from unified_agent.readiness import probe
from unified_agent.run import execute
from unified_agent.providers import total,route,PaidTransport
from unified_agent.agent import VisualAgent

OUT=Path(os.environ.get('BRICK_ARK_PILOT_OUT',ROOT/'deliverables/brick-atlas-ark-pilot-v1')).expanduser().resolve()
LEDGER=OUT/'ledger.private.json'
MODELS=['ark/gpt-6-1-sol-260929','ark/doubao-seed-2-1-pro-260915','ark/deepseek-v4-1-flash-261017','qwen/qwen3.8-flash']

class PacedTransport:
 """Throttle before a request. Never resend an API call or alter its payload."""
 def __init__(self,*args,**kwargs):self.inner=PaidTransport(*args,**kwargs)
 def __getattr__(self,name):return getattr(self.inner,name)
 def __call__(self,payload):
  delay=0
  if self.model=='ark/doubao-seed-2-1-pro-260915' and self.ledger_path.exists():
   charges=json.loads(self.ledger_path.read_text())['charges']
   recent=[c['createdAt']+c.get('latencySeconds',0) for c in charges if c.get('model')==self.model]
   delay=max(0,65-(time.time()-max(recent))) if recent else 0
   if delay:print('TPM_PACING',self.model,round(delay,1),'seconds; no retry',flush=True);time.sleep(delay)
  try:return self.inner(payload)
  finally:
   if self.inner.latest:self.inner.latest['clientThrottleSeconds']=round(delay,3)

class IsolatedViewerAgent(VisualAgent):
 """Identical agent policy; publish only its own run, avoiding global latest races."""
 def publish(self):
  s=self.session
  state=dict(schema='brick-atlas-spectator-arena/2',protocol=PROTOCOL,runId=s.directory.name,
   title=s.row['title'],caseId=s.row['key'],model=self.model,phase=self.phase,startedAt=self.started,
   updatedAt=time.time(),frames=self.frames,calls=self.calls,usage=self.transport.usage(),
   targetParts=sum(bool(v) for v in s.goal.values()),maxDecisions=self.cap,result=self.result() if s.done else None,
   fullModelControl=True,scriptedPrefix=0,autoRepair=0,resets=0,formalBenchmarkResult=False,
   evaluationScope='per-task run; normal-qualified incident denominator',evidenceType='api-model',
   condition='static' if s.row['mode']=='static' else 'normal' if s.control else 'incident',
   track=s.row['evaluationMetadata']['track'],inputMode='initial three views + persistent visual memory + agent-requested observations',
   spectatorNotice='Spectator images, events and scores never enter model messages.',
   agentProfile=self.profile,experimentArm='static-checkpoint-shared-agent' if s.row['mode']=='static' else 'dynamic-visual-agent',
   initialImages=self.initial_images,agentMemory=dict(plan=self.plan,notes=self.notes),
   budgetCounters=dict(actions=self.action_attempts,observations=self.observation_attempts))
  write_json(s.directory/'spectator.json',state)

def combined_report():
 """Merge completed evidence for readers without touching active worker reports."""
 paths=[OUT/'pilot.json',*sorted((OUT/'workers').glob('*.json'))]
 reports=[json.loads(p.read_text()) for p in paths if p.exists()]
 if not reports:return {}
 report=dict(reports[0]);unique={};missing={};active=[]
 for d in reports:
  for r in d['runs']:unique[r['arenaRunId']]=r
  for r in d['notRun']:missing[(r['model'],r['caseId'],r['condition'])]=r
  if d.get('activeRun'):active.append(d['activeRun'])
 report['runs']=list(unique.values());report['notRun']=list(missing.values());report['activeRuns']=active
 report['pendingModels']=[m for m in MODELS if not any(r['model']==m for r in report['runs']+report['notRun'])]
 report['allWorkersFinished']=all(d.get('finishedAt') for d in reports) and not report['pendingModels']
 if LEDGER.exists():
  ledger=json.loads(LEDGER.read_text())
  report['ledger']=dict(accountedProvisionalCNY=total(ledger)/.2,accountingCapCNY=ledger['capUSD']/.2,
   usageEstimateCNY=sum(c.get('nativeCost',0) for c in ledger['charges']),
   pendingRequests=sum(c['status']=='pending' for c in ledger['charges']),
   uncertainRequests=sum(c['status']=='uncertain' for c in ledger['charges']),
   unresolvedRequests=sum(c['status'] in ('pending','uncertain') for c in ledger['charges']))
 report['apiStatus']=[]
 for model in MODELS:
  path=OUT/'preflight'/model.replace('/','--')/'certificate.json'
  if path.exists():
   c=json.loads(path.read_text());report['apiStatus'].append(dict(model=model,passed=c['passed'],inferenceModel=c.get('inferenceModel'),error=c.get('error',{}).get('code'),checkedAt=c['checkedAt']))
 if active:report['activeRun']=active[0]
 return report

def main():
 p=argparse.ArgumentParser();p.add_argument('--preflight-only',action='store_true');p.add_argument('--resume',action='store_true');p.add_argument('--refresh-preflight',action='store_true');p.add_argument('--models',nargs='+',choices=MODELS,default=MODELS);p.add_argument('--isolated-worker',action='store_true');a=p.parse_args()
 if (OUT/'completed.json').exists():
  raise ValueError('This pilot is archived. Use a new BRICK_ARK_PILOT_OUT directory and copied plan; do not overwrite or charge new probes to the completed pilot.')
 plan=json.loads((OUT/'plan.json').read_text());cap=plan['budget']['accountingCapCNY']*.2
 for model in MODELS:
  r=route(model)
  assert (r['provider']=='ark' and r['baseURL']=='https://ark.cn-beijing.volces.com/api/v3') or (model=='qwen/qwen3.8-flash' and r['provider']=='aliyun')
 checks={model:probe(model,cap,LEDGER,a.refresh_preflight,root=OUT,transport_factory=PacedTransport) for model in a.models}
 prior=json.loads((OUT/'api-preflight.json').read_text()) if (OUT/'api-preflight.json').exists() else {'rows':[]}
 combined={c['model']:c for c in prior['rows']};combined.update(checks)
 write_json(OUT/'api-preflight.json',dict(rows=list(combined.values()),passed=all(c['passed'] for c in combined.values()),purpose='interface only, no assembly scores'))
 if a.preflight_only:return
 if a.isolated_worker and len(a.models)!=1:raise ValueError('One model per isolated worker')
 lockpath=(OUT/(a.models[0].replace('/','--')+'.worker.lock')) if a.isolated_worker else ARENA/'run.lock'
 batch_lock=lockpath.open('w')
 print('WAIT_FOR_EXPERIMENT_LOCK',flush=True)
 fcntl.flock(batch_lock,fcntl.LOCK_EX)
 path=OUT/'workers'/(a.models[0].replace('/','--')+'.json') if a.isolated_worker else OUT/'pilot.json'
 if path.exists() and not a.resume:raise ValueError('Existing report; use --resume to keep completed attempts, never overwrite')
 report=json.loads(path.read_text()) if path.exists() else dict(schema='brick-atlas-ark-pilot/1',models=MODELS,protocol=PROTOCOL,startedAt=time.time(),runs=[],notRun=[],repeats=1,
  staticInterpretation='Static checkpoints use the SAME visual-agent controller to isolate task setting. These are not one-shot static model answers.',
  priceCaution='Sol Ark price unknown, explicitly authorized. CNY totals including Sol are provisional, not invoices or a guaranteed monetary cap.',
  incidentCondition='Same-case/backbone/profile successful normal run required; independently restarted incident episode, no matched-prefix causal estimate')
 if report.get('activeRun'):
  active=report['activeRun']
  if not any(r['arenaRunId']==active['arenaRunId'] for r in report['runs']):
   raise ValueError('A previously active run needs reconciliation before resume; it will not be silently repeated: '+active['arenaRunId'])
  report.pop('activeRun')
 other=combined_report()
 if any(r['model'] in a.models for r in other.get('activeRuns',[])):
  raise ValueError('Selected backbone already has an active run; do not start a duplicate worker')
 historical=other.get('runs',[])
 write_json(path,report)
 done={(r['model'],r['caseId'],r['arenaBranch']) for r in report['runs']}
 done.update((r['model'],r['caseId'],r['condition']) for r in report['notRun'])
 done.update((r['model'],r['caseId'],r['arenaBranch']) for r in historical)
 done.update((r['model'],r['caseId'],r['condition']) for r in other.get('notRun',[]))
 def run(cid,model,condition,obj,normal=None):
  key=(model,cid,condition)
  if key in done:return next((r for r in report['runs']+historical if (r['model'],r['caseId'],r['arenaBranch'])==key),None)
  if not checks[model]['passed']:
   report['notRun'].append(dict(model=model,caseId=cid,condition=condition,objectTitle=obj['title'],reason='api_preflight_failed'))
  elif condition=='incident' and (not normal or normal.get('success') is not True):
   report['notRun'].append(dict(model=model,caseId=cid,condition=condition,objectTitle=obj['title'],reason='normal_not_successful'))
  else:
   try:
    result=execute(cid,model,condition,cap,normal['agentProfile'] if normal else None,normal,
      ledger_path=LEDGER,report_path=path,certificate_root=OUT,transport_factory=PacedTransport,
      agent_factory=IsolatedViewerAgent if a.isolated_worker else VisualAgent)
    result.update(objectTitle=obj['title'],objectId=obj['model'],lengthGroup=obj['lengthGroup'],activeParts=obj['activeParts'])
    report['runs'].append(result);write_json(path,report);done.add(key)
    print('RESULT',model,obj['title'],condition,result['terminalStatus'],result['success'],flush=True)
    return result
   except ValueError as exc:
    report['notRun'].append(dict(model=model,caseId=cid,condition=condition,objectTitle=obj['title'],reason='case_or_certificate_failed',detail=str(exc)[:400]))
  done.add(key);write_json(path,report);return None
 if True:
  for i,obj in enumerate(plan['objects']):
   # Rotate order between objects. Every model receives the same task list.
   order=[m for m in MODELS[i%len(MODELS):]+MODELS[:i%len(MODELS)] if m in a.models]
   for cid in obj['staticCases']:
    for model in order:run(cid,model,'static',obj)
   normals={model:run(obj['dynamicCase'],model,'normal',obj) for model in order}
   for model in order:run(obj['dynamicCase'],model,'incident',obj,normals[model])
 ledger=json.loads(LEDGER.read_text());report['finishedAt']=time.time()
 report['ledger']=dict(accountedProvisionalCNY=total(ledger)/.2,accountingCapCNY=cap/.2,
  unresolvedRequests=sum(c['status'] in ('pending','uncertain') for c in ledger['charges']))
 report['pendingModels']=[m for m in MODELS if not any(r['model']==m for r in report['runs']+report['notRun'])]
 report.pop('activeRun',None);write_json(path,report)
 print('FINISHED',report['ledger'],flush=True)

if __name__=='__main__':main()
