"""Real, bounded OpenRouter pilot with durable inputs, outputs, images and traces."""
from pathlib import Path
import argparse,base64,hashlib,json,os,re,shutil,subprocess,sys,time
from copy import deepcopy
from datetime import datetime,timezone
import numpy as np
from protocol import Episode,load
from render import Renderer
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/os.environ.get('BRICKPLAN_EVAL_OUT','deliverables/brickplan-visual-v3')
NODE=Path(os.environ.get('BRICKPLAN_NODE') or shutil.which('node') or ROOT/'.tools/node-v22.23.2-darwin-arm64/bin/node')
MODELS=[]  # Live model IDs must be explicitly selected; no text or obsolete defaults.
from vision import SYSTEM

def dump(path,value):
    path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');tmp.replace(path)


def image_file(image, directory=None):
    import io
    buf=io.BytesIO();image.save(buf,format='PNG');data=buf.getvalue();name=hashlib.sha256(data).hexdigest()+'.png'
    p=(directory or OUT)/'images'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data) if not p.exists() else None
    return 'images/'+name


def images(ep,renderer,extra=None,directory=None):
    # Historical evidence replay only. The live runner uses vision.images.
    save=lambda image:image_file(image,directory)
    state=ep.assignments();goal=ep.case['goal']
    results=[save(renderer.sheet(state,ep.alias,'CURRENT')),save(renderer.sheet(goal,ep.alias,'TARGET')),
             save(renderer.atlas(state,goal,ep.alias))]
    if extra:
        action=ep.internal_action(extra)
        if action.get('partId') in ep.actors:results.append(save(renderer.pair(state,goal,action['partId'],ep.alias)))
        elif 'azimuth' in action:
            results.extend(save(renderer.render(s,size=(640,480),labels=ep.alias,angles=(action['azimuth'],action['elevation']))[0]) for s in (state,goal))
        elif 'view' in action:
            results.extend(save(renderer.render(s,action['view'],size=(640,480),labels=ep.alias)[0]) for s in (state,goal))
    return results


def call(model,observation,paths):
    from vision import request_body
    payload=request_body(model,observation,paths,OUT)
    return send_request(payload)


def send_request(payload):
    # Calls always receive a V3 visual request assembled by request_body.
    proc=subprocess.run([str(NODE),'--import','tsx',str(ROOT/'benchmark/brickplan-repair/eval/call_api.ts')],input=json.dumps(payload),text=True,capture_output=True,cwd=ROOT,timeout=110)
    if proc.returncode:
        diagnostic=re.search(r'OpenRouter HTTP \d{3}|TimeoutError|Provider exceeded reservation|Missing usage cost',proc.stderr)
        reason='budget cap' if 'Budget limit reached' in proc.stderr else 'unsettled charge' if 'Unsettled' in proc.stderr else diagnostic.group(0) if diagnostic else 'API adapter failed'
        raise RuntimeError(reason)
    return json.loads(proc.stdout)


def run_one(spec,model,track,max_calls=8):
    if track!='visual' or spec.get('protocolVersion')!='v3':
        raise ValueError('Text and v1/v2 views are retired. Use visual protocolVersion=v3.')
    from vision import VisionRenderer, images as visual_images, SYSTEM as visual_system, VERSION, qualify
    cert,cases=load(spec['modelId']);case=cases[spec['caseId']]
    ep=Episode(cert,case,spec['mode'],spec.get('event','none'),seed=spec.get('seed',41),action_mask=spec.get('actionMask',False),protocol_version=spec.get('protocolVersion','v1'))
    slug=hashlib.sha256(json.dumps([spec,model,track,'connector-workbench/4'],sort_keys=True).encode()).hexdigest()[:16]
    file=OUT/'runs'/f'{slug}.json'
    resume=None
    if file.exists():
        old=json.loads(file.read_text())
        if old.get('status') in ('complete','budget_exhausted','error'):return old
        if old.get('status')=='scheduler_paused':
            resume=old
            for step in old['steps']:
                assert ep.assignments()==step['before']
                assert ep.observe(track)==step['observation']
                for execution in step.get('executions',[]):
                    assert ep.step(execution['action'])==execution['feedback']
                    assert ep.assignments()==execution['after']
        else:raise RuntimeError('Existing interrupted run needs review; refusing silent replay')
    renderer=VisionRenderer(ep.cert);ep.vision_renderer=renderer
    admission=qualify(ep,renderer)
    if not admission['passed']:raise ValueError('V3 actual-state visual admission failed before any model call')
    result={'id':slug,'spec':spec,'model':model,'track':track,'startedAt':datetime.now(timezone.utc).isoformat(),
            'visualAdmission':admission,'status':'running','steps':[],'maxCalls':max_calls,'systemPrompt':visual_system,
            'protocol':VERSION,'manipulationProtocol':'connector-workbench/4','originalRestrictedOptimum':case['expectedOptimum'] if spec['mode']=='static' else None,
            'referenceCostScope':'Original bank optimum is NOT claimed optimal in the expanded, case-independent action catalogue.'}
    if resume:
        result=resume;result['status']='running';result.pop('error',None)
    dump(file,result);extra=None
    if resume and resume['steps']:
        for execution in resume['steps'][-1].get('executions',[]):
            if execution['action'].get('type')=='inspect' and execution['feedback']['code']=='OBSERVATION_READY':extra={'partId':execution['feedback']['partId']} if 'partId' in execution['feedback'] else execution['action']
    for i in range(len(result['steps']),max_calls):
        observation=ep.observe(track);paths=visual_images(ep,renderer,OUT,extra)
        step={'callIndex':i,'observation':observation,'images':paths,'before':ep.assignments(),'state':'requesting'}
        result['steps'].append(step);dump(file,result)
        try:response=call(model,observation,paths)
        except Exception as exc:
            result.update(status='budget_exhausted' if str(exc)=='budget cap' else 'error',error=str(exc),metrics=ep.score(),events=ep.events);dump(file,result);raise
        step['response']=response;step['state']='responded';dump(file,result)
        try:
            parsed=json.loads(response['content']);actions=parsed.get('actions')
            if not isinstance(actions,list) or not 1<=len(actions)<=8:raise ValueError()
        except (ValueError,AttributeError,TypeError):actions=[{'type':'invalid'}]
        if spec.get('actionMask'):actions=actions[:1]
        step['executions']=[];extra=None
        for action in actions:
            feedback=ep.step(action);step['executions'].append({'action':action,'feedback':feedback,'after':ep.assignments()})
            if isinstance(action,dict) and action.get('type')=='inspect' and feedback['code']=='OBSERVATION_READY':extra={'partId':feedback['partId']} if 'partId' in feedback else action
            if feedback['code']!='OK':break
        step['state']='executed';result.update(metrics=ep.score(),events=ep.events);dump(file,result)
        if ep.finished:break
    result.update(status='complete',stopReason='model_finish' if ep.finished else 'call_budget',metrics=ep.score(),events=ep.events,
                  costUSD=sum(s['response']['cost'] for s in result['steps'] if 'response' in s))
    dump(file,result)
    print(json.dumps({'id':slug,'mode':spec['mode'],'event':spec.get('event'),'kind':case['kind'],'model':model,'track':track,**result['metrics'],'cost':result['costUSD']},ensure_ascii=False),flush=True)
    return result


def select():
    rows=[]
    from static_bench import OUT as BANK
    index=json.loads((BANK/'index.json').read_text())
    for m in index['models']:
        _,cs=load(m['modelId']);rows.extend(cs.values())
    chosen=[]
    for kind in ['control','wrong_color','missing','wrong_type','wrong_size','offset','rotation','height_layer','swapped_positions','compound']:
        pool=[c for c in rows if c['kind']==kind and c['observation']['visualEligibility']=='verified']
        # Frozen hard pilot: one representative per kind, no population claim.
        pool.sort(key=lambda c:(c.get('challengeVariant')=='four_fault_coupling',c['expectedOptimum'],c['id']),reverse=True)
        if kind=='control':pool.sort(key=lambda c:(c['modelId']!='v23-30181',c['id']))
        c=pool[0];chosen.append({'mode':'static','modelId':c['modelId'],'caseId':c['id'],'kind':kind,'difficulty':c['difficulty'],'restrictedCost':c['expectedOptimum']})
    for spec in chosen:spec['protocolVersion']='v3'
    dump(OUT/'selection.json',{'selection':'deterministic hard-stratified pilot, not random bank sample','seed':41,'specs':chosen,'models':MODELS,'tracks':['visual']})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--select',action='store_true');p.add_argument('--models',nargs='+',required=True);p.add_argument('--calls',type=int,default=8);p.add_argument('--limit',type=int);p.add_argument('--mode',choices=['static'],default='static');args=p.parse_args()
    MODELS=args.models;OUT.mkdir(parents=True,exist_ok=True)
    if args.select:select()
    else:
        specs=json.loads((OUT/'selection.json').read_text())['specs']
        if args.mode:specs=[s for s in specs if s['mode']==args.mode]
        if args.limit:specs=specs[:args.limit]
        specs.sort(key=lambda s:s.get('kind',''))
        for spec in specs:
            for track in ['visual']:
                for model in MODELS:run_one(spec,model,track,args.calls)
