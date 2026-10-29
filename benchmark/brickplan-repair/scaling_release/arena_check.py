"""Real Arena tool I/O and images with scripted witnesses, never an API model."""
from bench_design.session import Session
from dynamic_arena import OUT as ARENA
from dynamic_arena.tool_arena import ToolArena
from dynamic_arena.validate_replays import Witness
from scaling_release import OUT
from expansion_v7.build import read,write

def main():
 results=[]
 for number in ['2132-1','7223-1-alt-831','21035-1']:
  cases=read(OUT/'private'/number/'cases.private.json.gz')
  c=next(c for c in cases if c['mode']=='dynamic' and len(c['events'])>1) if any(c['mode']=='dynamic' and len(c['events'])>1 for c in cases) else next(c for c in cases if c['mode']=='dynamic' and c['events'])
  previous=None
  for normal in [True,False]:
   tag='normal' if normal else 'incident';runid=f'release-check-{number}-{tag}';directory=ARENA/'runs'/runid
   s=Session.open(c['id'],directory,'scripted:release-check',control=normal);s.autosave=False
   if not normal:s.normal_gate=dict(eligible=previous['success'],normalRunId=previous['runId'],sameCase=True,sameModel=True,sharedPrefixVerified=False)
   out=ToolArena(s,Witness(s),s.cap).run();assert out['success'],(runid,out)
   assert out['appliedEvents']==(0 if normal else len(c['events']))
   if not normal:assert out['normalQualifiedRecovery']['success'] is True
   record=dict(runId=runid,caseId=c['id'],normal=normal,success=True,appliedEvents=out['appliedEvents'],metrics=out)
   results.append(record);previous=record;print('ARENA PASS',runid,out['controllerMetrics'],flush=True)
 write(OUT/'checks/arena-replays.json',dict(passed=True,runs=results,apiCalls=0,notModelPerformance=True))

if __name__=='__main__':main()
