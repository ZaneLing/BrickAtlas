"""Render legal references for representative completed trials; never model input."""
import argparse,hashlib,json,time
from bench_design.session import Session
from dynamic_arena.sensors import Sensors
from dynamic_arena.validate_replays import Witness
from dynamic_arena.transport import write_json
from unified_agent.experiment_batch import OUT,merged


def main():
    p=argparse.ArgumentParser();p.add_argument('--all',action='store_true');a=p.parse_args()
    report=merged();selected={}
    for r in report['runs']:
        key=(r['caseId'],r['arenaBranch'])
        if a.all or r['sampleIndex'] in (1,2,3,5):selected[key]=r
    rows=[]
    for (cid,arm),r in selected.items():
        folder=OUT/'reference'/hashlib.sha256((cid+arm).encode()).hexdigest()[:12]
        if (folder/'reference.json').exists():rows.append(json.loads((folder/'reference.json').read_text()));continue
        folder.mkdir(parents=True,exist_ok=True);s=Session.open(cid,folder,'scripted:evaluator-reference',control=arm=='normal');s.autosave=False
        sensor=Sensors(s);w=Witness(s);frames=[]
        def frame(action=None):
            path=folder/f"step-{len(frames):03}.png";sensor.render(s.ep.state).save(path)
            frames.append(dict(index=len(frames),environmentDecision=len(s.records),action=action,image=str(path.relative_to(OUT))))
        frame()
        for _ in range(s.cap*2+4):
            action=json.loads(w({}));tool,args=action['tool'],action['args']
            if tool=='observe':continue
            feedback=s.submit(dict(type=tool,**args));assert feedback['code'] in ('OK','FINISHED','SUCCESS'),feedback
            if tool in ('attach','detach'):frame(action)
            if s.done:break
        result=s.result();assert result['success'],(cid,arm)
        row=dict(caseId=cid,arm=arm,object=r['objectTitle'],sampleIndex=r['sampleIndex'],frames=frames,result=result,
            evidenceType='scripted-reference-not-model',shortestPathClaim=False,providedToModel=False)
        write_json(folder/'reference.json',row);rows.append(row);print('REFERENCE',r['objectTitle'],arm,len(frames)-1,flush=True)
    write_json(OUT/'reference/index.json',dict(rows=rows,apiCalls=0,providedToModel=False,createdAt=time.time()))


if __name__=='__main__':main()
