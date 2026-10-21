"""Replay a human practice round without trusting client scores or outcomes."""
from copy import deepcopy
import math
from static_v4.metrics import RepairEpisode
from static_v4.certify import digest


def evaluate_practice(runtime,case,events,final_state,certificate=None,elapsed_seconds=None):
    if not isinstance(events,list) or len(events)>5000:
        raise ValueError('本轮操作记录无效或超过 5000 条')
    ep=RepairEpisode(runtime,case,certificate);undo_stack=[];undos=0;reference=False
    for action in events:
        if not isinstance(action,dict) or action.get('type') not in ('attach','detach','inspect','undo'):
            raise ValueError('本轮包含未知操作，请重新开始')
        kind=action['type'];before=dict(ep.state)
        if kind=='undo':
            if not undo_stack:raise ValueError('撤销记录与本轮操作不一致')
            ep.state=undo_stack.pop();undos+=1
            from static_v4.metrics import residual
            record=dict(index=len(ep.records),action=deepcopy(action),code='PRACTICE_UNDO',
                        beforeSha256=digest(before),afterSha256=digest(ep.state),
                        residualEdits=residual(runtime,ep.state),finiteDecisionRegret=None)
            record['chainSha256']=digest(dict(previous=ep.chain,record=record));ep.chain=record['chainSha256']
            ep.records.append(record);ep.visited.append(dict(ep.state))
        else:
            feedback=ep.step(action)
            if kind in ('attach','detach') and feedback['code']=='OK':undo_stack.append(before)
            if kind=='inspect' and action.get('source')=='reference-replay':reference=True
    if runtime.state(final_state)!=ep.state:
        raise ValueError('本轮记录与页面状态不一致，请重新开始后提交')
    ep.step(dict(type='finish'));result=ep.export();score=result['score']
    if undos:
        # Undo is a practice state restoration, not a legal manipulation edge.
        # Keep every actual attempt in the record, but suppress path optimality.
        score['cost'].update(finiteDomainEligible=False,finiteOptimum=None,finiteLegalExcess=None,
                             finiteAttemptExcess=None,unrestrictedLegalExcessInterval=None)
        score['preservation']['additionalPiecesVsClosestShortestSet']=None
    if not isinstance(elapsed_seconds,(int,float)) or not math.isfinite(elapsed_seconds) or elapsed_seconds<0:
        elapsed_seconds=None
    score['practice']=dict(undoCount=undos,referenceReplayUsed=reference,assisted=bool(undos or reference),
                          elapsedSeconds=elapsed_seconds,timeSource='client elapsed time',
                          observationScope='explicit view, guide and target controls; excludes continuous camera dragging',
                          rankedBenchmarkRun=False)
    return result
