"""Small, paid usage study; current S/D executors and exact D paired inputs.

No score is promoted to a formal benchmark result. Each model/case has one attempt.
The shared Node ledger authorizes at most ten USD over every model and branch.
"""
from pathlib import Path
from copy import deepcopy
import argparse,base64,hashlib,json,os,subprocess,sys,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'eval')]
from dynamic_v6.episode import DynamicEpisode,load_case,branch_before_action
from dynamic_v6.interface import packet,renderer_for,SYSTEM as D_SYSTEM,POINT_GUIDE
from dynamic_v6.run_paired import parse
from plate5_eval import load as load_static,evaluate as evaluate_static,SOURCE as STATIC_SOURCE
from static_v4.certify import digest
from dynamic_v5.run_api import request

OUT=ROOT/'deliverables/brickplan-budget-pilot-2026-10-23'
NODE=ROOT/'.tools/node-v22.23.2-darwin-arm64/bin/node'
MODELS=['openai/gpt-6.1-sol','google/gemini-3.8-flash','qwen/qwen3.5-27b','google/gemma-3-12b-it','anthropic/claude-sonnet-5.5','anthropic/claude-haiku-5.5','qwen/qwen3-vl-8b-instruct','qwen/qwen3.5-9b','qwen/qwen2.5-vl-72b-instruct']
S_SYSTEM='''Repair the CURRENT NOW LEGO assembly on its fixed white baseplate to match the separate FINAL TARGET images. This is a static task: the environment does not change. There are three labeled views, all inventory pages, and visual candidate catalogs available through inspect with partId. The same actor may be shown in several views: these are views of one assembly. Anonymous actor and candidate handles convey no answer. Inventory includes spare or distractor pieces. Choose any physically legal repair order; each attach or detach moves exactly one part. A rejected move leaves the state unchanged. Inspect is allowed at any time; inspect partId returns all its candidate pages uniformly in current-scene context, without correctness or legality labels. To identify a visible current part, inspect view and normalized point [x,y]. Candidate previews show the attempted placement, not an oracle. Attach needs partId and candidate (or catalogPage plus normalized catalogPoint). Detach needs partId. Finish ends the attempt, including if incomplete. Return exactly one JSON object with action, and an optional short note. No batch of actions. The BEFORE panel, when present, shows the same assembly immediately before your previous action; CURRENT NOW is the actual current state.'''
S_SYSTEM+=POINT_GUIDE

def dump(p,x):
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');t.replace(p)

class StaticEpisode(DynamicEpisode):
    def __init__(self,cid):
        rt,c=load_static(cid)
        fake=dict(id=cid,modelId=c['modelId'],kind='none',trigger=999999,targetParts=sum(bool(k) for k in c['goal'].values()),
                  protocol='brickplan-dynamic/6',manipulationProtocol=c['manipulationProtocol'],decisionBudget=max(40,6*sum(bool(k) for k in c['goal'].values())+20))
        source=json.loads((STATIC_SOURCE/c['qualificationFile']).read_text())
        super().__init__(source,fake,41)
        assert self.runtime.signature(self.runtime.goal)==rt.signature(c['goal'])
        self.source_case=c;self.state=dict(c['initial']);self.chain=digest(dict(caseId=cid,initial=self.state,seed=41))
    def observe(self):
        o=super().observe();o.update(protocol='visual-static-plate5-single-action-pilot/1',mode='static',
            task='Repair CURRENT NOW to match FINAL TARGET. The environment does not change.',decisionsUsed=len(self.records))
        o['responseSchema'].pop('unexpectedChange',None)
        return o

def initialize():
    OUT.mkdir(parents=True,exist_ok=True)
    if not (OUT/'catalogue.json').exists():
        (OUT/'catalogue.json').write_bytes((ROOT/'tem/budget-pilot-2026-10-23/catalogue.json').read_bytes())
    if not (OUT/'ledger.json').exists():dump(OUT/'ledger.json',dict(schema='brickplan-budget-pilot-ledger/1',capUSD=10,allowedModels=MODELS,charges=[]))
    dump(OUT/'authorization.json',dict(date='2026-10-23',capUSD=10,source='User explicitly authorized a ten-dollar static/dynamic model pilot in this conversation.',repetitions=1,scope='S static, D paired dynamic, M module pilot if budget allows; all models share one ledger.'))

def totals():
    x=json.loads((OUT/'ledger.json').read_text());return dict(spentUSD=sum(c['actualUSD'] or 0 for c in x['charges']),
      committedUSD=sum(c['actualUSD'] if c['actualUSD'] is not None else c['reservedUSD'] for c in x['charges']),requests=len(x['charges']),blocked=any(c['status']=='pending' for c in x['charges']))

def decide(ep,renderer,folder,extra,dialogue,model,system,report,branch,max_job):
    obs,imgs=packet(ep,renderer,folder,extra)
    if isinstance(ep,StaticEpisode):obs['track']='static-plate5-visual-pilot'
    if report['track']=='D-checkpoint':
        obs['track']='scripted-prefix-continuation-diagnostic'
        obs['task']='Continue from this already partially assembled scene; match the fixed final target. The setup actions were performed by the simulator, not by you.'
        obs['setupActions']=report['scriptedSetupActions']
    # Private evaluator fields may never enter the model's observation.
    for key in ['caseId','kind','trigger','privateEvent','current','target','buildGuide','legalActions','oraclePlan','roots']:
        assert key not in obs,key
    payload=request(model,obs,imgs,folder,system,dialogue)
    payload.update(campaign=str(OUT),run=report['runId'],branch=branch,decision=len(ep.records),max_tokens=4096,
                   remainingJobUSD=max_job-report['costUSD'],parserPolicy='one-explicit-json-object-with-optional-prose')
    if model=='openai/gpt-6.1-sol':payload['providerOnly']=['OpenAI']
    n=report['requests']+1
    dump(folder/f'input-{len(ep.records):03}.json',dict(system=system,observation=obs,images=imgs,priorTextHistory=dialogue))
    result=subprocess.run([str(NODE),str(HERE/'call.mjs')],input=json.dumps(payload),text=True,capture_output=True,cwd=ROOT,timeout=145)
    if result.returncode:raise RuntimeError('adapter_error: '+result.stderr[-200:])
    r=json.loads(result.stdout)
    if r['status']=='budget_stop':raise RuntimeError('reservation_budget_stop')
    report['requests']+=1;report['costUSD']+=r.get('costUSD',r.get('actualUSD')) or 0
    if r['status']!='returned':
        report.setdefault('errors',[]).append(r);dump(folder/f'error-{len(ep.records):03}.json',r);raise RuntimeError('api_error')
    a,note,change=parse(r['content'])
    print(json.dumps(dict(progress=report['runId'],branch=branch,decision=len(ep.records),costUSD=round(report['costUSD'],6),action=a,finishReason=r.get('finishReason')),ensure_ascii=False),flush=True)
    return dict(index=len(ep.records),observation=obs,images=imgs,response=r,action=a,note=note,reportedUnexpectedChange=change,
                priorDialogueSha256=digest(dialogue))

def history(dialogue,step,feedback):
    dialogue.append(dict(role='assistant',content=step['response']['content']))
    dialogue.append(dict(role='user',content=json.dumps(dict(toolFeedback=feedback,instruction='Continue using the fresh current images.'))))

def next_extra(action,fb):
    return ({'partId':fb['partId']} if 'partId' in fb else action) if action.get('type')=='inspect' and fb['code']=='OBSERVED' else None

def run(track,cid,model,max_decisions=32,max_job=2):
    initialize();rid=f'{track}--{cid}--'+model.replace('/','--');out=OUT/'runs'/rid
    if (out/'trace.json').exists():return json.loads((out/'trace.json').read_text())
    out.mkdir(parents=True,exist_ok=True)
    rep=dict(schema='brickplan-budget-pilot-run/1',runId=rid,track=track,caseId=cid,model=model,seed=41,repetitions=1,
             requests=0,costUSD=0,status='running',steps=[],branches={},pilotDecisionCap=max_decisions,perJobCapUSD=max_job,
             startedAt=time.time(),scope='Development usage estimate; not formal model ranking. Prior visual history is retained as text actions/feedback, with fresh full current image packet.')
    rep['parserPolicy']='one-explicit-json-object-with-optional-prose'
    save=lambda:dump(out/'trace.json',rep)
    if track=='S':ep=StaticEpisode(cid);system=S_SYSTEM;intervention=None
    else:
        cert,intervention=load_case(cid);cert,control=load_case(intervention['pairedGroup']+'--control');ep=DynamicEpisode(cert,control,41);system=D_SYSTEM
    rep['sourceCertificateSha256']=ep.cert['contentSha256'];rep['targetParts']=sum(bool(x) for x in ep.runtime.goal.values())
    renderer=renderer_for(ep);extra=None;dialogue=[];branches=None;save()
    try:
        while not ep.finished and len(ep.records)<max_decisions:
            step=decide(ep,renderer,out/'prefix',extra,dialogue,model,system,rep,'prefix',max_job)
            a=step['action'];change=step['reportedUnexpectedChange']
            if intervention and a.get('type') in ('attach','detach') and ep.manipulations>=intervention['trigger']-1:
                try:branches=branch_before_action(ep,intervention,a)
                except ValueError:branches=None
            if branches:
                for b in branches:b.judgments.append(change)
                fb=branches[0].history[-1]['feedback'];step['feedback']=fb;rep['steps'].append(step);history(dialogue,step,fb)
                rep['sharedPrefixVerified']=branches[0].expected_after_last_action==branches[1].expected_after_last_action
                rep['event']=branches[1].event;save();break
            fb=ep.submit(dict(action=a,unexpectedChange=change));step['feedback']=fb;rep['steps'].append(step);history(dialogue,step,fb)
            extra=next_extra(a,fb);save()
        if not branches:
            rep.update(status='complete' if ep.finished else 'decision_cap',episode=ep.export())
            if track=='S':
                actions=[]
                for s in rep['steps']:
                    action=ep.internal_action(s['action'])
                    if action.get('type')=='attach' and 'catalogPoint' in action:
                        action['candidate']=ep.catalog_click_candidate(s['action'])
                        action.pop('catalogPoint',None);action.pop('catalogPage',None)
                    actions.append(action)
                rep['replayScore']=evaluate_static(cid,actions)
                assert rep['replayScore']['success']==ep.score()['success']
            elif intervention:rep['status']='untriggered' if ep.finished else 'untriggered_decision_cap'
        else:
            for name,current in zip(('control','intervention'),branches):
                bd=deepcopy(dialogue);br=renderer_for(current);extra=None
                rep['branches'][name]=dict(status='running',steps=[]);save()
                try:
                    while not current.finished and len(current.records)<max_decisions:
                        s=decide(current,br,out/name,extra,bd,model,system,rep,name,max_job)
                        fb=current.submit(dict(action=s['action'],unexpectedChange=s['reportedUnexpectedChange']));s['feedback']=fb
                        rep['branches'][name]['steps'].append(s);history(bd,s,fb);extra=next_extra(s['action'],fb);save()
                    rep['branches'][name]['status']='complete' if current.finished else 'decision_cap'
                except RuntimeError as e:rep['branches'][name].update(status=str(e))
                rep['branches'][name]['episode']=current.export();save()
            rep['status']='complete' if all(b['status']=='complete' for b in rep['branches'].values()) else 'incomplete'
    except Exception as e:rep.update(status=str(e),episode=ep.export())
    rep['elapsedSeconds']=round(time.time()-rep['startedAt'],2);save()
    summary={k:v for k,v in rep.items() if k not in ('steps','branches','episode')};summary['score']=rep.get('replayScore',rep.get('episode',{}).get('score'))
    summary['branches']={n:dict(status=b['status'],score=b.get('episode',{}).get('score')) for n,b in rep['branches'].items()}
    print(json.dumps(summary,ensure_ascii=False),flush=True);return rep

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--track',choices=['S','D'],required=True);p.add_argument('--case',required=True);p.add_argument('--model',required=True);p.add_argument('--max-decisions',type=int,default=32);p.add_argument('--max-job',type=float,default=2)
    a=p.parse_args();run(a.track,a.case,a.model,a.max_decisions,a.max_job)
