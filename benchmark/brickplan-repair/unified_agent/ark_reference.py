"""Evaluator-only legal reference frames. Never supplied to API models."""
import hashlib,json,time
from bench_design.session import Session
from dynamic_arena.sensors import Sensors
from dynamic_arena.validate_replays import Witness
from dynamic_arena.transport import write_json
from unified_agent.ark_batch import OUT

def main():
 plan=json.loads((OUT/'plan.json').read_text());rows=[]
 for obj in plan['objects']:
  for cid,arm in [(c,'static') for c in obj['staticCases']]+[(obj['dynamicCase'],'normal'),(obj['dynamicCase'],'incident')]:
   tag=hashlib.sha256((cid+arm).encode()).hexdigest()[:12];folder=OUT/'reference'/tag
   if (folder/'reference.json').exists():rows.append(json.loads((folder/'reference.json').read_text()));continue
   folder.mkdir(parents=True,exist_ok=True);s=Session.open(cid,folder,'scripted:evaluator-reference',control=arm=='normal');s.autosave=False
   sensor=Sensors(s);w=Witness(s);frames=[]
   def frame(action=None):
    path=folder/f"step-{len(frames):03}.png";sensor.render(s.ep.state).save(path)
    frames.append(dict(index=len(frames),environmentDecision=len(s.records),action=action,image=str(path.relative_to(OUT))))
   frame()
   for _ in range(s.cap*2+4):
    a=json.loads(w({}));tool,args=a['tool'],a['args']
    if tool=='observe':continue
    f=s.submit(dict(type=tool,**args));assert f['code'] in ('OK','FINISHED','SUCCESS'),f
    if tool in ('attach','detach'):frame(a)
    if s.done:break
   result=s.result();assert result['success'],(cid,arm)
   row=dict(caseId=cid,arm=arm,object=obj['title'],frames=frames,result=result,
    evidenceType='scripted-reference-not-model',shortestPathClaim=False,providedToModel=False)
   write_json(folder/'reference.json',row);rows.append(row);print('REFERENCE',obj['title'],arm,len(frames)-1,flush=True)
 write_json(OUT/'reference/index.json',dict(rows=rows,apiCalls=0,providedToModel=False,createdAt=time.time()))

if __name__=='__main__':main()
