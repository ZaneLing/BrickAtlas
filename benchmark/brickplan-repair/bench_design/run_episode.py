"""A single direct-action envelope; existing physical engines remain authoritative.

Full scene context for named modules. Diagnostic historical dynamic crops require
an explicit flag. This runner does not contact any model API.
"""
from copy import deepcopy
from pathlib import Path
import argparse,json,uuid
import numpy as np
from bench_design import ROOT,OUT
from bench_design.catalogue import rows_with_cases
from bench_design.metrics import state_metrics,execution_metrics
from bench_design.policy import INPUT_VERSION
from expansion_v7.build import read,write
from expansion_v7.runtime import Episode as ExpandedEpisode
from expansion_v7.run_episode import Packet
from recognizable_models.run_episode import load_episode as load_object_episode
from dynamic_v6.episode import DynamicEpisode
from dynamic_v6.interface import renderer_for,packet as legacy_packet
from budget_pilot.run import StaticEpisode

VERSION=INPUT_VERSION
SYSTEM='''Match the sole TARGET using the current images. For static tasks repair the current stage; for dynamic tasks complete the whole required target. One action per response: attach, detach, inspect, or finish. Return one direct JSON object, for example {"type":"attach","partId":"anonymous handle","candidate":"anonymous position"}. Every attach/detach moves one part. Any physically legal order is accepted. You may inspect throughout. Inventory contains spare parts. No changes are announced in dynamic episodes. Do not assume a change occurred merely because an episode is being evaluated. Finish only when the required target is complete.'''


def load(case_id,directory,diagnostic=False):
    row=next(r for r in rows_with_cases() if r['key']==case_id)
    public=next(json.loads(l) for l in (OUT/'questions.jsonl').read_text().splitlines() if json.loads(l)['id']==case_id)
    if public['track'] in ('archived-crop-dynamic','dynamic-structure-diagnostic') and not diagnostic:
        raise ValueError('This historical dynamic structure is diagnostic only; use --diagnostic explicitly.')
    row['evaluationMetadata']={k:public[k] for k in ('canonicalId','taskType','track','source','model')}
    bank,mid,c=row['bank'],row['model'],row['case']
    if bank in ('M','O'):
        ep,packet=load_object_episode(c['id'],directory=directory)
        return row,ep,packet,None
    if bank=='E7':
        folder=ROOT/'deliverables/brickplan-expansion-v7/models'/mid
        ep=ExpandedEpisode(read(folder/'certificate.private.json.gz'),c,41)
        packet=Packet(ep,read(folder/'manual.private.json.gz'),directory)
        if ep.cert.get('environmentMode')!='white-baseplate':
            keys=list(packet.renderer.cert['fixed'])+[k for k,r in ep.cert['candidates'].items() if r['kind']=='goal']
            packet.renderer.bounds['_module_frame']=np.concatenate([packet.renderer.bounds[k] for k in keys])
        return row,ep,packet,None
    if bank=='S':ep=StaticEpisode(c['publicId'])
    else:ep=DynamicEpisode(read(ROOT/'deliverables/brickplan-dynamic-v6/models'/mid/'qualification.json'),c,41)
    return row,ep,None,renderer_for(ep)


def observation(row,ep,packet,renderer,directory,extra=None):
    if packet:obs=packet.observation()
    else:
        obs,images=legacy_packet(ep,renderer,directory,extra)
        for im in images:
            path=Path(im['file'])
            if not path.is_absolute():im['file']=str(directory/path)
        obs['images']=images
    obs['inputVersion']=VERSION
    obs['done']=bool(getattr(ep,'done',getattr(ep,'finished',False)))
    obs['responseEnvelope']='one direct action object, with no outer action field'
    obs['responseSchema']=dict(attach=['type','partId','candidate'],detach=['type','partId'],
        inspect='type plus view, partId, candidate, manualStep or inventoryPage as available',finish=['type'])
    if row['bank']=='E7' and ep.cert.get('environmentMode')!='white-baseplate':
        obs['startingStateDescription']='完整主体已经装好，本次只补指定部分；当前／目标图保留完整物件背景。'
    forbidden={'family','events','initial','goal','humanErrorIds','referenceActions','score','scheduledEvents','appliedEvents','taskType'}
    assert not forbidden.intersection(obs)
    return obs


def valid(action):
    if not isinstance(action,dict):return False
    kind=action.get('type');fields=set(action)
    if kind=='attach':return fields=={'type','partId','candidate'}
    if kind=='detach':return fields=={'type','partId'}
    if kind=='finish':return fields=={'type'}
    return kind=='inspect' and fields<={'type','view','partId','candidate','manualStep','inventoryPage','futureReference'} and len(fields)>1


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--id',required=True);parser.add_argument('--diagnostic',action='store_true')
    args=parser.parse_args();directory=(OUT/'runs'/uuid.uuid4().hex).resolve()
    directory.mkdir(parents=True,exist_ok=True)
    row,ep,packet,renderer=load(args.id,directory,args.diagnostic)
    initial=deepcopy(ep.state);records=[];states=[deepcopy(initial)]
    print(json.dumps(observation(row,ep,packet,renderer,directory),ensure_ascii=False),flush=True)
    import sys
    for line in sys.stdin:
        try:action=json.loads(line);parse_error=False
        except json.JSONDecodeError:action={'type':'invalid'};parse_error=True
        supplied=deepcopy(action);action=action if valid(action) else {'type':'invalid'}
        before=deepcopy(ep.state)
        try:
            result=ep.step(action)
            fb=ep.feedback if hasattr(ep,'feedback') else result
        except (ValueError,KeyError,TypeError) as exc:
            fb=dict(code='INVALID_REQUEST',message=str(exc))
        if not valid(supplied):fb=dict(code='INVALID_REQUEST')
        records.append(dict(action=supplied if isinstance(supplied,dict) else {'type':'invalid'},
            parseError=parse_error,feedback=fb,before=before,after=deepcopy(ep.state)))
        if action.get('type') in ('attach','detach') and fb.get('code')=='OK' and hasattr(ep,'expected_after_last_action'):
            records[-1]['afterOwnActionBeforeExternalChange']=deepcopy(ep.expected_after_last_action)
        states.append(deepcopy(ep.state))
        extra=action if action.get('type')=='inspect' and fb.get('code') in ('INSPECT','OBSERVED') else None
        print(json.dumps(observation(row,ep,packet,renderer,directory,extra),ensure_ascii=False),flush=True)
        if getattr(ep,'done',getattr(ep,'finished',False)):break
    done=getattr(ep,'done',getattr(ep,'finished',False));goal=row['case'].get('goal',ep.runtime.goal)
    explicit_finish=bool(records and valid(records[-1]['action']) and records[-1]['action']['type']=='finish'
        and records[-1]['feedback'].get('code') in ('FINISHED','SUCCESS','INCOMPLETE'))
    metrics=state_metrics(ep.runtime,initial,ep.state,goal,finished=explicit_finish)
    case=row['case'];reference=case.get('oraclePlan',case.get('referenceActions'))
    if reference is not None:reference_moves=len(reference)
    elif row['bank']=='D':reference_moves=case['trigger']+len(case['privateEvent']['recoveryWitness']) if case.get('privateEvent') else case['targetParts']
    else:reference_moves=None
    native_events=getattr(ep,'events',None)
    if native_events is None:
        single=getattr(ep,'event',None) or getattr(ep,'last_event',None)
        native_events=[deepcopy(single)] if single else []
    write(directory/'record.private.json.gz',dict(caseId=args.id,inputVersion=VERSION,
        evaluationMetadata=row['evaluationMetadata'],
        terminalStatus='completed' if explicit_finish else 'model_budget_exhausted' if done else 'external_stop',records=records,states=states,
        stateMetrics=metrics,executionMetrics=execution_metrics(records,initial_was_correct=metrics['initialWasCorrect'],reference_moves=reference_moves),
        nativeEvents=native_events,nativeHistory=getattr(ep,'history',[]),
        nativeScore=ep.score(),apiCalls=0))


if __name__=='__main__':main()
