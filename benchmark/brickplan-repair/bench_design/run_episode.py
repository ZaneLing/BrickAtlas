"""A single direct-action envelope; existing physical engines remain authoritative.

Full scene context for named modules. Diagnostic historical dynamic crops require
an explicit flag. This runner does not contact any model API.
"""
from copy import deepcopy
from functools import lru_cache
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
SYSTEM+=''' Follow the observation's targetContract. When alternative decompositions are explicitly allowed, the target picture illustrates the required colored volume and height; different internal seams and part counts are allowed, with legal connections still required. Use only actual available inventory; each handle is one finite physical part. Multiple views show the same object at the same time. Default current-target views arrive automatically; inspect requests additional views, part/position previews or optional manual pages.'''


@lru_cache(maxsize=1)
def source_rows():
    return {r['key']:r for r in rows_with_cases()}


@lru_cache(maxsize=1)
def public_rows():
    return {r['id']:r for r in map(json.loads,(OUT/'questions.jsonl').read_text().splitlines())}


def load(case_id,directory,diagnostic=False):
    from bench_design.reference_revisions import apply
    from bench_design.selection import require_active
    require_active(case_id)
    row,ep,packet,renderer=_load(case_id,directory,diagnostic)
    require_active(case_id,row['model'],row.get('evaluationMetadata',{}).get('source'))
    apply(row,ep)
    return row,ep,packet,renderer


def _load(case_id,directory,diagnostic=False):
    if case_id.startswith('SC:'):
        from scaling_release.load import load as load_scaling
        return load_scaling(case_id,directory)
    if case_id.startswith('A4:'):
        from dynamic_arena.qualify_sources import load as load_arena_source
        return load_arena_source(case_id,directory)
    if case_id.startswith('QI:'):
        from bench_design.inventory_tasks import load as load_inventory
        return load_inventory(case_id,directory)
    if case_id.startswith('QN:'):
        from bench_design.source_expansion import load as load_source_extension
        return load_source_extension(case_id,directory)
    if case_id.startswith('QX:'):
        from bench_design.challenges import load_challenge
        return load_challenge(case_id,directory)
    if case_id.startswith(('E7:','D:')):
        from reliability.active_load import index,load as active_load
        if case_id in index():return active_load(case_id,directory)
    row=deepcopy(source_rows()[case_id])
    public=public_rows()[case_id]
    if public['track'] in ('archived-crop-dynamic','dynamic-structure-diagnostic') and not diagnostic:
        raise ValueError('This historical dynamic structure is diagnostic only; use --diagnostic explicitly.')
    row['evaluationMetadata']={k:public[k] for k in ('canonicalId','taskType','track','source','model')}
    normal=next((r for r in public_rows().values() if r['model']==public['model'] and r['taskType']=='D0'),None)
    if normal:row['evaluationMetadata']['normalCanonicalId']=normal['canonicalId']
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
    if row['bank'] in ('E7','QN') and ep.cert.get('environmentMode')!='white-baseplate':
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
    return kind=='inspect' and fields<={'type','view','partId','candidate','point','manualStep','inventoryPage','futureReference'} and len(fields)>1


def main():
    from bench_design.session import Session
    import sys
    # The full-context image bundle is retained only for historical replay.
    if '--legacy-full-context' not in sys.argv:
        from reliability.run import main as paged_main
        return paged_main()
    parser=argparse.ArgumentParser()
    parser.add_argument('--legacy-full-context',action='store_true')
    parser.add_argument('--id',required=True)
    parser.add_argument('--diagnostic',action='store_true')
    parser.add_argument('--actions',type=Path,help='Optional JSONL action script; otherwise read stdin')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--actor',default='scripted-cli')
    args=parser.parse_args()
    directory=(args.output or OUT/'runs'/uuid.uuid4().hex).resolve()
    session=Session.open(args.id,directory,args.actor,args.diagnostic)
    print(json.dumps(session.observe(),ensure_ascii=False),flush=True)
    stream=args.actions.open() if args.actions else sys.stdin
    try:
        for line in stream:
            try: action=json.loads(line);parse_error=False
            except json.JSONDecodeError: action={'type':'invalid'};parse_error=True
            session.submit(action,parse_error)
            print(json.dumps(session.observe(),ensure_ascii=False),flush=True)
            if session.done:break
    finally:
        if args.actions:stream.close()
        session.save()


if __name__=='__main__':main()
