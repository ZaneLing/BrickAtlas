"""Fork a real post-incident state: continuing context versus fresh context.

This is a history treatment, not a no-incident counterfactual. No hidden state,
event identity or recovery instruction is exposed to either policy.
"""
from copy import deepcopy
import json
from bench_design.session import Session,disable_events,digest,alias_maps
from dynamic_arena.tool_arena import ToolArena,PROTOCOL
from expansion_v7.build import write
from reliability.run import Offline

def state_contract(arena):
 s=arena.session
 return dict(state=s.ep.state,target=s.goal,aliases=alias_maps(s.ep),certificate=s.ep.runtime.cert,
     inventory=arena.sensors.availability(),tools=arena.public_request()['availableTools'],
     camera=[arena.azimuth,arena.elevation],remainingDecisions=arena.cap,sensorProtocol=PROTOCOL,
     futureIncidentsEnabled=False)

def fork(origin,directory,transport_factory=None):
 """Call immediately after an effective incident, before the next policy call."""
 s=origin.session;directory=__import__('pathlib').Path(directory)
 effective=[e for e in s.events if e['effectiveIncidentVerified']]
 if not effective or effective[-1]['atDecision']!=len(s.records):
  raise ValueError('Checkpoint must be immediately after a verified effective incident')
 remaining=origin.cap-len(origin.calls)
 if remaining<1:raise ValueError('No decision budget left')
 branches={}
 for name in ('continuing','fresh'):
  clone=Session.open(s.row['key'],directory/name,s.actor);clone.autosave=False
  for rec in s.records:
   clone.submit(rec['action'],parse_error=rec['parseError'])
   for field in ('before','afterOwnActionBeforeExternalChange','after','feedback','newEventIndices'):
    assert clone.records[-1][field]==rec[field],('Checkpoint replay differs',name,field)
  assert clone.ep.state==s.ep.state and clone.goal==s.goal and alias_maps(clone.ep)==alias_maps(s.ep)
  disable_events(clone.ep)
  clone.initial=deepcopy(clone.ep.state);clone.records=[];clone.events=[];clone.observations=[]
  clone._pending_observation=None;clone.extra=None;clone.terminal=None;clone.cap=remaining
  # A fresh random run identifier must not become an experimental cue.
  clone.run_id='matched-'+digest([s.run_id,len(origin.calls)])[:20]
  t=transport_factory(name) if transport_factory else Offline()
  arena=ToolArena(clone,t,remaining);arena.azimuth,arena.elevation=origin.azimuth,origin.elevation
  if name=='continuing':
   arena.history=deepcopy(origin.history)
   # Prefix and continuation observation numbers are separate namespaces.
   # Explicit scope avoids collisions when continuation decisions restart at 1.
   arena.prior_archive=deepcopy(origin.archive)
  branches[name]=arena
 left,right=branches.values();assert digest(state_contract(left))==digest(state_contract(right))
 assert left.model==right.model
 assert left.public_request()==right.public_request()
 proof=dict(schema='brick-atlas-matched-state-pair/1',protocol=PROTOCOL,caseId=s.row['key'],
     sourceRun=s.directory.name,sourceActor=s.actor,prefixDecisions=len(origin.calls),remainingDecisions=remaining,
     stateContractSha256=digest(state_contract(left)),publicStartSha256=digest(left.public_request()),
     sharedStartVerified=True,historyIsOnlyDesignedTreatment=True,futureEventsDisabled=True,
     normalGate=getattr(s,'normal_gate',None),normalQualified=bool(getattr(s,'normal_gate',{}).get('eligible')),
     sourceEvidence='scripted-engine-check' if s.actor.startswith('scripted') else 'policy-run',
     prefixToolCalls=deepcopy(origin.calls),prefixEnvironmentRecords=deepcopy(s.records),
     prefixEvents=deepcopy(s.events),snapshot=deepcopy(state_contract(left)),
     notAnUnperturbedCounterfactual=True,notBenchmarkAggregate=True)
 write(directory/'pair.private.json',proof)
 return branches,proof

def score(branches,proof,directory):
 rows={name:a.result() for name,a in branches.items()}
 valid=all(r['terminalStatus'] in ('completed','model_budget_exhausted') for r in rows.values())
 output=dict(schema='brick-atlas-matched-state-result/1',pairContract=proof['stateContractSha256'],
     valid=valid,results=rows,completionDifference=(int(rows['continuing']['success'])-int(rows['fresh']['success'])) if valid else None,
     scope='Single paired continuation from identical fault state; history treatment, not causal fault cost.',
     normalQualified=proof['normalQualified'],sourceEvidence=proof['sourceEvidence'])
 write(__import__('pathlib').Path(directory)/'pair-result.json',output)
 return output

def main():
 import argparse
 from pathlib import Path
 from reliability import OUT
 from reliability.run import Command
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--id',required=True);p.add_argument('--actor',required=True);p.add_argument('--output',type=Path,default=OUT/'matched-policy-run')
 p.add_argument('--max-decisions',type=int,default=60);p.add_argument('--policy-command',nargs=argparse.REMAINDER,required=True)
 args=p.parse_args()
 if args.output.exists():raise ValueError('Use a new output directory; previous evidence is never overwritten')
 def opened(name,control=False):
  s=Session.open(args.id,args.output/name,args.actor,control=control)
  return ToolArena(s,Command(args.policy_command,args.actor),min(args.max_decisions,s.cap))
 normal=opened('normal',True);result=normal.run()
 if not result['success']:
  write(args.output/'status.json',dict(repairApplicable=False,reason='normal-not-successful',normal=result));return
 origin=opened('prefix');origin.session.normal_gate=dict(eligible=True,normalRunId=normal.session.directory.name,sameCase=True,sameModel=True,sharedPrefixVerified=False)
 origin.run(stop_after_incident=True)
 if not origin.session.events or origin.session.done:
  write(args.output/'status.json',dict(repairApplicable=False,reason='no-usable-incident-checkpoint',prefix=origin.result()));return
 branches,proof=fork(origin,args.output/'paired',lambda name:Command(args.policy_command,args.actor))
 for branch in branches.values():branch.run()
 print(json.dumps(score(branches,proof,args.output/'paired'),ensure_ascii=False))

if __name__=='__main__':main()
