"""Evaluator-side accounting. Never put these fields into a model observation."""
import re
from collections import Counter


def service_error(error):
    """Accept structured adapter errors and legacy Python/HTTP exception messages."""
    data=error if isinstance(error,dict) else {}
    message=str(data.get('message',data.get('error',error)))
    status=data.get('httpStatus')
    if not status:
        match=re.search(r'(?:HTTP(?: Error)?\s*|status[=: ]+)(\d{3})',message,re.I)
        status=int(match.group(1)) if match else None
    try:status=int(status) if status is not None else None
    except (TypeError,ValueError):status=None
    if status is None or status<400:
        try:
            code=int(data.get('errorCode',0))
            if 400<=code<=599:status=code
        except (TypeError,ValueError):pass
    lowered=message.lower()
    if status==429:category='rate_limited'
    elif status in (408,504) or any(s in lowered for s in ('timeout','timed out','timeoutexpired')):category='timeout'
    elif status in (401,403):category='request_rejected'
    elif status and status>=500:category='provider_unavailable'
    elif status and status>=400:category='request_error'
    else:category='transport_or_adapter_error'
    return dict(category=category,httpStatus=status)


def event_triggered(event):
    if type(event.get('appliedEvents')) is int:return event['appliedEvents']>0
    return bool(event.get('eventTriggered',event.get('eventApplied',False)))


def pair_assessment(control,event,control_status,intervention_status,*,shared_prefix=True,visibility_gate=False):
    triggered=event_triggered(event)
    returned=control_status=='complete' and intervention_status=='complete'
    control_ok=bool(control.get('success',control.get('completionSuccess')))
    all_events=(event.get('appliedEvents')==event['scheduledEvents']) if 'scheduledEvents' in event else True
    eligible=bool(shared_prefix and returned and control_ok and triggered and all_events)
    declared=event.get('reportedAtEvent')
    detection_eligible=eligible and visibility_gate and type(declared) is bool and not control.get('preEventFalseAlarms',0)
    reason=('untriggered' if not triggered else 'run_interrupted' if not returned else
            'control_failed' if not control_ok else 'unmatched_prefix' if not shared_prefix else
            'not_all_events_triggered' if not all_events else 'eligible')
    return dict(recoveryPairEligible=eligible,repairEligibilityReason=reason,
        repairSuccess=bool(event.get('success',event.get('completionSuccess'))) if eligible else None,
        detectionPairMachineEligible=detection_eligible,
        detectionMiss=(not declared) if detection_eligible else None,
        humanValidated=False,paperDetectionClaimEligible=False)


def assess_run(trace):
    steps=trace.get('steps',trace.get('prefix',[]))+[s for b in trace.get('branches',{}).values() for s in b.get('steps',[])]
    format_count=sum(s.get('action',{}).get('type')=='invalid' for s in steps)
    schema_count=sum(s.get('action',{}).get('type')!='invalid' and s.get('feedback',{}).get('code') in ('INVALID_ACTION','INVALID_REQUEST') for s in steps)
    physical_rejections=Counter(s.get('feedback',{}).get('code') for s in steps
        if s.get('action',{}).get('type') in ('attach','detach') and s.get('feedback',{}).get('code') not in (None,'OK','INVALID_ACTION','INVALID_REQUEST'))
    errors=list(trace.get('errors',[]))
    errors.extend(a for a in trace.get('requestAudit',[]) if a.get('status')=='api_error')
    if not errors and trace.get('status')=='api_error':errors=[trace.get('error','API error')]
    service=Counter(service_error(e)['category'] for e in errors)
    status=trace.get('status','unknown')
    unrecovered=[e for e in errors if not (isinstance(e,dict) and e.get('recovered') is True)]
    interrupted=bool(unrecovered) or status in ('api_error','reservation_budget_stop','cost_budget','interface_update_stop','incomplete') or status.startswith('adapter_error')
    score=trace.get('moduleScore') or trace.get('replayScore') or trace.get('episode',trace.get('prefixEpisode',{})).get('score',{})
    dynamic=trace.get('track') in ('D','M-D','D-checkpoint','E7-D','O-D') or 'controlCaseId' in trace
    cid=trace.get('caseId','')
    normal=cid.endswith(('--control','-dynamic-control')) or '::dynamic::control::' in cid
    scheduled=trace.get('eventScheduled',bool(score['scheduledEvents']) if 'scheduledEvents' in score else not normal)
    triggered=event_triggered(score)
    completion=score.get('success') if not interrupted else None
    out=dict(serviceErrors=dict(service),serviceErrorCount=sum(service.values()),formatErrorResponses=format_count,
        actionSchemaErrorResponses=schema_count,physicalActionRejections=dict(physical_rejections),
        completionSuccess=completion,repairSuccess=None,detectionMiss=None,recoveryPairEligible=False,
        eventTriggered=triggered,success=completion if not dynamic or not scheduled else None,
        # A legal but unsuccessful move alone cannot distinguish perception from planning.
        visualFailure=None,placementFailure=None,failureCause='not_established',formatAffectedAttempt=False)
    branches=trace.get('branches',{})
    if dynamic and {'control','intervention'}<=set(branches):
        c,b=branches['control'],branches['intervention']
        event=b.get('episode',{}).get('score',{})
        pair=pair_assessment(c.get('episode',{}).get('score',{}),event,c.get('status'),b.get('status'),
                             shared_prefix=trace.get('sharedPrefixVerified',trace.get('branchStateVerified',False)),
                             visibility_gate=trace.get('attribution',{}).get('visibilityGate',False))
        out.update(pair);out['eventTriggered']=event_triggered(event)
        if interrupted:
            out.update(recoveryPairEligible=False,repairSuccess=None,detectionMiss=None,
                       detectionPairMachineEligible=False,repairEligibilityReason='run_interrupted')
        out['success']=out['repairSuccess']
        outcome='repair_completed' if out['repairSuccess'] else 'repair_incomplete' if out['recoveryPairEligible'] else out['repairEligibilityReason']
    elif dynamic and scheduled:
        out['observedCompletionAfterEvent']=completion if triggered else None
        outcome='unpaired_observation' if triggered else 'untriggered'
        out['repairEligibilityReason']='unpaired' if triggered else 'untriggered'
    else:
        outcome='completed' if completion else 'task_incomplete'
        if dynamic:out['repairEligibilityReason']='normal_control'
    if interrupted:
        outcome='service_error' if errors else 'evaluation_stopped'
    elif not out['success'] and format_count:
        # Preserve the task outcome separately; do not turn format rejects into vision errors.
        out['formatAffectedAttempt']=True
    else:out['formatAffectedAttempt']=False
    out['outcome']=outcome
    return out
