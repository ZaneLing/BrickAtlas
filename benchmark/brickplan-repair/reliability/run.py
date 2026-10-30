"""Default static/dynamic tool runner. No provider or API key is chosen here."""
import argparse,json,subprocess,sys,uuid
from pathlib import Path
from bench_design.session import Session
from dynamic_arena.tool_arena import ToolArena,PROTOCOL
from reliability import OUT

class Offline:
 model='scripted:offline'
 latest=None
 def usage(self):return dict(calls=0,costUSD=0.,capUSD=0.)

class Command(Offline):
 def __init__(self,command,model):self.command,self.model=command,model
 def __call__(self,payload):
  result=subprocess.run(self.command,input=json.dumps(payload),text=True,capture_output=True,timeout=120,check=True)
  return result.stdout.strip()
 def usage(self):return dict(calls=0,costUSD=None,capUSD=None,externalBillingUnverified=True)

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--id',required=True);p.add_argument('--output',type=Path);p.add_argument('--actor',default='scripted:stdin')
 p.add_argument('--actions',type=Path);p.add_argument('--max-decisions',type=int,default=40)
 p.add_argument('--normal',action='store_true');p.add_argument('--diagnostic',action='store_true')
 p.add_argument('--policy-command',nargs=argparse.REMAINDER)
 a=p.parse_args();s=Session.open(a.id,a.output or OUT/'runs'/('preview-'+uuid.uuid4().hex),a.actor,diagnostic=a.diagnostic,control=a.normal)
 t=Command(a.policy_command,a.actor) if a.policy_command else Offline()
 arena=ToolArena(s,t,min(a.max_decisions,s.cap))
 if a.policy_command:
  print(json.dumps(arena.run(),ensure_ascii=False));return
 # Readable observation packets carry asset URLs and hashes. Models wrapping
 # this CLI use --policy-command to receive the actual serialized image bytes.
 source=a.actions.open() if a.actions else sys.stdin
 print(json.dumps(arena.request()[1],ensure_ascii=False),flush=True)
 for line in source:
  if not line.strip():continue
  output=arena.step(line.strip())
  print(json.dumps(dict(toolResult=output,nextInput=None if s.done else arena.request()[1]),ensure_ascii=False),flush=True)
  if s.done or len(arena.calls)>=arena.cap:break
 if not s.done:s.terminal='model_budget_exhausted' if len(arena.calls)>=arena.cap else 'harness_error'
 s.save();arena.phase='finished';arena.publish()
 from expansion_v7.build import write
 write(s.directory/'log.json',dict(protocol=PROTOCOL,calls=arena.calls,result=arena.result()))
 write(s.directory/'result.json',arena.result())

if __name__=='__main__':main()
