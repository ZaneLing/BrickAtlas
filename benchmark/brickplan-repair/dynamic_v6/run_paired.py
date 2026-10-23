"""Run one shared policy prefix, then branch control/intervention with identical history.

Default --dry-run builds the exact input package without making a paid request.
Paid execution requires both --execute and an explicit --max-cost cap.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import argparse,hashlib,json,re,sys
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'eval')]
from dynamic_v6.episode import BANK,DynamicEpisode,load_case,branch_before_action
from dynamic_v6.interface import packet,renderer_for,SYSTEM
from dynamic_v5.run_api import request,call,parse as legacy_parse
from dynamic_v5.build import write

def decode_one_object(content):
    """Accept one explicit JSON object, optionally surrounded by prose/fences.

    Never invent, repair, merge, or select between multiple action objects.
    Native JSON arrays remain invalid, even if they contain only one object.
    """
    try:
        obj=json.loads(content)
    except (ValueError,TypeError):
        if not isinstance(content,str):raise ValueError('Expected text')
        decoder=json.JSONDecoder();objects=[];position=0
        while position<len(content):
            start=content.find('{',position)
            if start<0:break
            try:obj,end=decoder.raw_decode(content,start)
            except ValueError:position=start+1;continue
            objects.append(obj);position=end
        if len(objects)!=1:raise ValueError('Exactly one explicit JSON object is required')
        obj=objects[0]
    if not isinstance(obj,dict):raise ValueError('Expected one object')
    return obj

def parse(content):
    try:
        obj=decode_one_object(content)
        if not isinstance(obj,dict) or not set(obj)<={'action','unexpectedChange','note'}:
            raise ValueError('One action object is required')
    except (ValueError,TypeError):return {'type':'invalid'},'format_error',None
    return legacy_parse(json.dumps(obj))

def run(case_id,model,seed=41,execute=False,max_cost=None):
    cert,case=load_case(case_id)
    if case['kind']=='none':raise ValueError('Choose an intervention; its control is paired automatically')
    control_case=load_case(case['pairedGroup']+'--control')[1]
    ep=DynamicEpisode(cert,control_case,seed);renderer=renderer_for(ep)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out=BANK/'pilot-v6'/re.sub('[^A-Za-z0-9._-]','-',model)/(case_id+f'--s{seed}--{stamp}')
    out.mkdir(parents=True,exist_ok=True);obs,imgs=packet(ep,renderer,out)
    write(out/'initial-input.json',dict(system=SYSTEM,observation=obs,images=imgs))
    if not execute:
        report=dict(status='dry_run',paidRequests=0,costUSD=0,caseId=case_id,initialInput=str(out/'initial-input.json'),model=model)
        write(out/'trace.json',report);return report
    if max_cost is None or max_cost<=0:raise ValueError('--execute requires a positive --max-cost')
    report=dict(schema='brickplan-paired-run/6',caseId=case_id,controlCaseId=control_case['id'],model=model,seed=seed,
                systemPromptSha256=hashlib.sha256(SYSTEM.encode()).hexdigest(),decisionBudget=ep.decision_budget,
                imageInterface='visual-temporal-v6-three-views-all-pages',prefix=[],branches={},requestAudit=[],requests=0,costUSD=0,status='running',
                budgetNote='Check settled cost before each request; the last request may exceed the cap by its own charge.')
    def save():write(out/'trace.json',report)
    def decide(current,view_renderer,folder,extra,dialogue):
        if report['costUSD']>=max_cost:raise RuntimeError('cost_budget')
        observation,images=packet(current,view_renderer,folder,extra)
        payload=request(model,observation,images,folder,SYSTEM,dialogue)
        payload['seed']=seed
        attempt=dict(number=report['requests']+1,status='requesting',decision=len(current.records),branch=str(folder.relative_to(out)))
        report['requests']+=1;report['requestAudit'].append(attempt);save()
        try:result=call(payload)
        except Exception as e:
            attempt.update(status='api_error',error=str(e),costUSD=None);save();raise
        attempt.update(status='returned',costUSD=result['cost']);report['costUSD']+=result['cost']
        action,note,change=parse(result['content'])
        return dict(index=len(current.records),observation=observation,images=images,response=result,action=action,
                    reportedUnexpectedChange=change,note=note,priorDialogueSha256=hashlib.sha256(json.dumps(dialogue,sort_keys=True).encode()).hexdigest())
    def update_dialogue(dialogue,step,feedback):
        dialogue.append(dict(role='assistant',content=step['response']['content']))
        dialogue.append(dict(role='user',content=json.dumps(dict(toolFeedback=feedback,instruction='Continue this episode using the fresh current images.'))))
    def extra_for(action,fb):return ({'partId':fb['partId']} if 'partId' in fb else action) if action.get('type')=='inspect' and fb['code']=='OBSERVED' else None
    dialogue=[];extra=None;branches=None
    try:
        while not ep.finished:
            step=decide(ep,renderer,out/'prefix',extra,dialogue);action=step['action'];change=step['reportedUnexpectedChange']
            try:
                if action.get('type') in ('attach','detach') and ep.manipulations>=case['trigger']-1:
                    control,intervention=branch_before_action(ep,case,action);branches=(control,intervention)
                else:branches=None
            except ValueError:branches=None
            if branches:
                for branch in branches:branch.judgments.append(change)
                feedback=control.history[-1]['feedback'];step['feedback']=feedback;report['prefix'].append(step)
                update_dialogue(dialogue,step,feedback)
                report['sharedPrefixDecisions']=len(control.records);report['sharedPrefixActions']=control.history
                report['branchStateVerified']=control.expected_after_last_action==intervention.expected_after_last_action
                report['event']=intervention.event;save();break
            feedback=ep.submit(dict(action=action,unexpectedChange=change));step['feedback']=feedback;report['prefix'].append(step)
            update_dialogue(dialogue,step,feedback);extra=extra_for(action,feedback);save()
        if not branches:
            report.update(status='untriggered',prefixEpisode=ep.export());save();return report
        for name,current in zip(('control','intervention'),branches):
            branch_dialogue=deepcopy(dialogue);branch_renderer=renderer_for(current);extra=None
            report['branches'][name]=dict(steps=[],status='running')
            try:
                while not current.finished:
                    step=decide(current,branch_renderer,out/name,extra,branch_dialogue)
                    feedback=current.submit(dict(action=step['action'],unexpectedChange=step['reportedUnexpectedChange']))
                    step['feedback']=feedback;report['branches'][name]['steps'].append(step)
                    update_dialogue(branch_dialogue,step,feedback);extra=extra_for(step['action'],feedback)
                    report['branches'][name]['episode']=current.export();save()
                report['branches'][name].update(status='complete',episode=current.export())
            except Exception as e:report['branches'][name].update(status='cost_budget' if str(e)=='cost_budget' else 'api_error',error=str(e),episode=current.export())
            save()
        control_score=branches[0].score();event_score=branches[1].score()
        admission=next(r for r in json.loads((BANK/'audit.json').read_text())['rows'] if r['caseId']==case_id)
        visibility_gate=admission['primaryMachineCandidate'] and branches[1].event['provenance']=='precertified'
        report.update(status='complete' if all(b['status']=='complete' for b in report['branches'].values()) else 'incomplete',
            attribution=dict(sharedPrefix=True,controlSuccess=control_score['success'],controlFalseAlarms=control_score['preEventFalseAlarms'],
                             eventTriggered=event_score['eventTriggered'],interventionSuccess=event_score['success'],
                             declaredAtEvent=event_score['reportedAtEvent'],
                             recoveryPairEligible=control_score['success'] and event_score['eventTriggered'],
                             authoredTemporalClass=admission['temporalClass'],visibilityGate=visibility_gate,
                             detectionPairMachineEligible=control_score['success'] and not control_score['preEventFalseAlarms'] and event_score['reportedAtEvent'] is not None and visibility_gate,
                             humanValidated=False,paperDetectionClaimEligible=False))
    except Exception as e:report.update(status='cost_budget' if str(e)=='cost_budget' else 'api_error',error=str(e),prefixEpisode=ep.export())
    save();return {k:v for k,v in report.items() if k not in ('prefix','branches','sharedPrefixActions')}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',required=True);p.add_argument('--model',default='dry-run');p.add_argument('--seed',type=int,default=41)
    p.add_argument('--execute',action='store_true');p.add_argument('--max-cost',type=float)
    a=p.parse_args();print(json.dumps(run(a.case,a.model,a.seed,a.execute,a.max_cost),ensure_ascii=False,indent=2))
