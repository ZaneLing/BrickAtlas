"""Measure the shipped M JSON-lines image protocol without dropping manual pages."""
from pathlib import Path
import hashlib,json,subprocess,sys,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import run as pilot

SYSTEM='''Complete or repair the specified LEGO module using the current scene, acceptance-target images, inventory, and numbered instruction images. The surrounding context is already assembled and locked. The acceptance target is the required final state for this episode; in static cases it can be an earlier instruction stage than the full-completion reference. The instruction images describe one valid original build order; any physically legal order reaching the acceptance target is allowed. In a dynamic episode the actual assembly can change without a notification. Account for your own previous action and repair unexpected changes. Every attach/detach moves exactly one part. Anonymous handles do not identify correct parts or poses. Inspect with view and candidate previews that candidate; inspect with view and partId shows the part. Use the exact schema in the observation. Return one JSON object {"action":{"type":"inspect","view":"isometric","candidate":"C001"},"note":"optional short note"}. No batch. Finish ends this attempt, including if incomplete. All supplied image roles and step numbers are provided in text immediately before each image.'''

def launch(module,condition):
    env=dict(__import__('os').environ)
    proc=subprocess.Popen([str(pilot.ROOT/'benchmark/.runtime/mlx-env/bin/python'),str(HERE.parent/'community_modules/run_episode.py'),
        '--module',module,'--condition',condition,'--seed','41'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,cwd=pilot.ROOT,env=env)
    line=proc.stdout.readline()
    if not line:raise RuntimeError('Module image adapter failed: '+proc.stderr.read()[-200:])
    return proc,json.loads(line)

def run(module,condition,model,max_decisions=20,max_job=3):
    pilot.initialize();cid=module+'-'+condition;rid='M--'+cid+'--'+model.replace('/','--');out=pilot.OUT/'runs'/rid
    if (out/'trace.json').exists():return json.loads((out/'trace.json').read_text())
    out.mkdir(parents=True,exist_ok=True);proc,obs=launch(module,condition)
    rep=dict(schema='brickplan-budget-pilot-run/1',runId=rid,track='M-S' if condition.startswith('static') else 'M-D',caseId=cid,
        model=model,seed=41,repetitions=1,requests=0,costUSD=0,status='running',steps=[],branches={},pilotDecisionCap=max_decisions,
        perJobCapUSD=max_job,startedAt=time.time(),scope='Exact shipped module JSON-lines adapter, all instruction and inventory images. Single qualitative episode, not a matched-prefix causal pair.')
    rep['parserPolicy']='one-explicit-json-object-with-optional-prose'
    save=lambda:pilot.dump(out/'trace.json',rep)
    dialogue=[];save()
    record_paths=set()
    try:
        for i in range(max_decisions):
            records=[]
            for item in obs['images']:
                source=Path(item['file']);record_paths.add(source.parent/'record.private.json')
                name='images/'+item['sha256']+'.png';target=out/name;target.parent.mkdir(exist_ok=True)
                if not target.exists():target.write_bytes(source.read_bytes())
                assert hashlib.sha256(target.read_bytes()).hexdigest()==item['sha256']
                records.append({**item,'file':name})
            public={k:v for k,v in obs.items() if k!='images'}
            payload=pilot.request(model,public,records,out,SYSTEM,dialogue)
            payload.update(campaign=str(pilot.OUT),run=rid,branch='single',decision=i,max_tokens=4096,remainingJobUSD=max_job-rep['costUSD'])
            if model=='openai/gpt-6.1-sol':payload['providerOnly']=['OpenAI']
            pilot.dump(out/f'input-{i:03}.json',dict(system=SYSTEM,observation=public,images=records,priorTextHistory=dialogue))
            response=subprocess.run([str(pilot.NODE),str(HERE/'call.mjs')],input=json.dumps(payload),text=True,capture_output=True,cwd=pilot.ROOT,timeout=145)
            if response.returncode:raise RuntimeError('adapter_error: '+response.stderr[-200:])
            r=json.loads(response.stdout)
            if r['status']=='budget_stop':raise RuntimeError('reservation_budget_stop')
            rep['requests']+=1;rep['costUSD']+=r.get('costUSD',r.get('actualUSD')) or 0
            if r['status']!='returned':rep.setdefault('errors',[]).append(r);raise RuntimeError('api_error')
            action,note,_=pilot.parse(r['content'])
            before=obs
            proc.stdin.write(json.dumps(action)+'\n');proc.stdin.flush();line=proc.stdout.readline()
            if not line:raise RuntimeError('Module adapter ended before returning observation')
            obs=json.loads(line)
            fb=obs.get('feedback') or {k:v for k,v in obs.items() if k in ('code','message')}
            step=dict(index=i,observation=public,images=records,response=r,action=action,note=note,feedback=fb)
            rep['steps'].append(step);pilot.history(dialogue,step,fb);save()
            print(json.dumps(dict(progress=rid,decision=i,costUSD=round(rep['costUSD'],6),action=action,feedback=fb),ensure_ascii=False),flush=True)
            if obs.get('done'):rep['status']='complete';break
            if 'images' not in obs:
                # Invalid requests leave the prior visible state in place; feedback is retained.
                obs={**before,'feedback':fb}
        else:rep['status']='decision_cap'
    except Exception as e:rep['status']=str(e)
    finally:
        try:proc.stdin.close();proc.wait(timeout=20)
        except (BrokenPipeError,subprocess.TimeoutExpired):proc.terminate();proc.wait(timeout=5)
    for p in record_paths:
        if p.exists():
            raw=json.loads(p.read_text());pilot.dump(out/'episode.private.json',raw);rep['moduleScore']=raw['score'];break
    rep['elapsedSeconds']=round(time.time()-rep['startedAt'],2);save()
    print(json.dumps({k:v for k,v in rep.items() if k not in ('steps','branches')},ensure_ascii=False),flush=True);return rep

if __name__=='__main__':run(*sys.argv[1:4])
