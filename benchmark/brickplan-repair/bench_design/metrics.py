"""Evaluator-only metrics. Final geometry, not actor IDs or a reference sequence.

No hidden state or metric output may be sent back to the acting model.
"""
from collections import Counter,defaultdict


def rate(a,b):return a/b if b else None


def overlap(a,b):
    tp=sum((a&b).values());fp=sum((a-b).values());fn=sum((b-a).values())
    return dict(tp=tp,fp=fp,fn=fn,precision=tp/(tp+fp) if tp+fp else float(not fn),
        recall=tp/(tp+fn) if tp+fn else float(not fp),
        f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 1.)


def state_metrics(rt,initial,final,goal,*,finished):
    i,f,g=(rt.signature(s) for s in (initial,final,goal))
    quality=overlap(f,g);base=i&g;missing=g-i;extra=i-g
    e0=sum(missing.values())+sum(extra.values());et=quality['fp']+quality['fn']
    type_color=lambda x:_project(x,lambda k:(k[0],k[1]))
    restored=(f-base)&missing
    still_bad=(f-g)&extra
    constraints=rt.final_constraints(final) if hasattr(rt,'final_constraints') else True
    return dict(finished=bool(finished),success=bool(finished and f==g and constraints),finalEquivalent=f==g,
        finalConstraintsSatisfied=bool(constraints),
        fullPlacement=quality,partTypeColor=overlap(type_color(f),type_color(g)),
        shapeAndPose=overlap(_project(f,lambda k:(k[0],k[2])),_project(g,lambda k:(k[0],k[2]))),
        colorAndPose=overlap(_project(f,lambda k:(k[1],k[2])),_project(g,lambda k:(k[1],k[2]))),
        initialEditResidual=e0,finalEditResidual=et,
        errorReduction=1-et/e0 if e0 else None,
        missingTargetRecovered=rate(sum(restored.values()),sum(missing.values())),
        originalExcessCleared=rate(sum(extra.values())-sum(still_bad.values()),sum(extra.values())),
        initiallyCorrectPlacements=sum(base.values()),
        finalDamageCount=sum((base-f).values()),finalDamageRate=rate(sum((base-f).values()),sum(base.values())),
        initialWasCorrect=i==g,scope='Operable target placements only; unchanged scenery cannot inflate the score.',
        residualIsNotShortestRepairLength=True)


def _project(counter,fn):
    out=Counter()
    for k,n in counter.items():out[fn(k)]+=n
    return out


def execution_metrics(records,*,initial_was_correct=False,reference_moves=None):
    attempts=well_formed=accepted=inspections=parse_errors=schema_errors=budget_rejections=0;rejections=Counter();resource=Counter()
    for r in records:
        action=r.get('action',{});kind=action.get('type')
        feedback=r.get('feedback',r.get('result',{})) or {}
        code=r.get('code',feedback.get('code'))
        parse=bool(r['parseError']) if 'parseError' in r else kind=='invalid'
        schema=not parse and code in ('INVALID_ACTION','INVALID_REQUEST')
        parse_errors+=parse;schema_errors+=schema;inspections+=kind=='inspect'
        budget_rejections+=code=='BUDGET_EXHAUSTED'
        if kind in ('attach','detach'):attempts+=1
        if kind in ('attach','detach') and not schema and not parse and code!='BUDGET_EXHAUSTED':
            well_formed+=1
            if code=='OK':accepted+=1
            elif code is None:raise ValueError('Manipulation feedback missing; cannot score legality')
            elif code=='OUT_OF_STOCK':resource[code]+=1
            else:rejections[code]+=1
    return dict(decisions=len(records),manipulationAttempts=attempts,acceptedMoves=accepted,
        wellFormedManipulationAttempts=well_formed,
        physicalRejections=dict(rejections),resourceRejections=dict(resource),legalActionRate=rate(accepted,well_formed),
        formatErrorResponses=parse_errors,schemaErrorResponses=schema_errors,
        inspectionCalls=inspections,budgetRejectedResponses=budget_rejections,falseRepair=bool(initial_was_correct and accepted),
        movesRelativeToWitness=rate(attempts,reference_moves) if reference_moves is not None else None,
        referenceIsNotOptimal=True,optimalityScore=None)


VALID_TERMINAL={'completed','model_budget_exhausted'}
ALL_TERMINAL=VALID_TERMINAL|{'service_error','harness_error','external_stop'}


def run_status(record):
    terminal=record['terminalStatus']
    if terminal not in ALL_TERMINAL:raise ValueError('Unknown terminalStatus')
    if terminal=='completed' and type(record.get('success')) is not bool:
        raise ValueError('Completed runs require an explicit boolean success; missing outcomes are not failures')
    return dict(abilityEligible=terminal in VALID_TERMINAL,
        success=(bool(record.get('success')) if terminal=='completed' else False) if terminal in VALID_TERMINAL else None,
        terminalStatus=terminal)


def pair_metrics(control,event,*,shared_prefix_verified=False):
    a,b=run_status(control),run_status(event)
    scheduled=event.get('scheduledEvents');applied=event.get('appliedEvents')
    if type(scheduled) is not int or type(applied) is not int or not 0<=applied<=scheduled:
        raise ValueError('Explicit valid scheduled/applied counts required')
    reason=('normal_control' if scheduled==0 else
        'run_interrupted' if not a['abilityEligible'] or not b['abilityEligible'] else
        'control_failed' if not a['success'] else 'unmatched_prefix' if not shared_prefix_verified else
        'untriggered' if applied==0 else 'not_all_events_triggered' if applied!=scheduled else
        'incident_effect_unverified' if event.get('effectiveIncidentVerified') is not True else 'eligible')
    eligible=reason=='eligible'
    comparable=bool(scheduled and a['abilityEligible'] and b['abilityEligible'] and shared_prefix_verified
        and applied==scheduled and event.get('effectiveIncidentVerified') is True)
    exclusions=[]
    for condition,label in [(scheduled==0,'normal_control'),
        (not a['abilityEligible'] or not b['abilityEligible'],'run_interrupted'),
        (a['abilityEligible'] and a['success'] is False,'control_failed'),(not shared_prefix_verified,'unmatched_prefix'),
        (bool(scheduled and applied==0),'untriggered'),
        (bool(scheduled and 0<applied<scheduled),'not_all_events_triggered'),
        (bool(scheduled and event.get('effectiveIncidentVerified') is not True),'incident_effect_unverified')]:
        if condition:exclusions.append(label)
    return dict(recoveryPairEligible=eligible,reason=reason,exclusionReasons=exclusions,
        repairJudgment='not_applicable' if not eligible else 'recovered' if b['success'] else 'not_recovered',
        conditionalRecoverySuccess=bool(b['success']) if eligible else None,
        rawInterventionCompletion=b['success'],triggerCoverage=rate(applied,scheduled),
        pairedComparisonEligible=comparable,
        pairedCompletionDrop=int(a['success'])-int(b['success']) if comparable else None,
        detectionSuccess=None,scheduledEvents=scheduled,appliedEvents=applied)


def event_recovery(rt,before,after,goal,window,*,minimum_retention_decisions=2,process_incident=False,resource_incident=False):
    """Each window entry is a POST-event/post-model-decision state.

    Window ends immediately before the NEXT external event. New correct build
    progress is allowed: never require equality to the old reference prefix.
    Identity swaps of equivalent physical parts are accepted by rt.signature.
    """
    b,a,g=(rt.signature(s) for s in (before,after,goal));base=b&g
    if resource_incident:
        values=[rt.complete(s) for s in window]
        first=next((i+1 for i,v in enumerate(values) if v),None)
        remaining=values[first:] if first is not None else []
        return dict(repairApplicable=True,observedRecovery=bool(values[-1]) if values else None,
            firstRecoveryDecision=first,retainedAfterRecovery=False if remaining and not all(remaining) else True if len(remaining)>=minimum_retention_decisions else None,
            windowDecisions=len(window),reason='inventory-change-use-legally-completed-equivalent-target',
            detectionSuccess=None,referencePrefixEqualityRequired=False)
    lost=base-a;new_bad=(a-g)-(b-g)
    required={k:base[k] for k in lost};excess_before=b-g
    applicable=bool(lost or new_bad)
    if not applicable:
        return dict(repairApplicable=False,observedRecovery=None,firstRecoveryDecision=None,
            retainedAfterRecovery=None,reason='process-obstruction-use-completion' if process_incident else 'no-new-target-defect',
            detectionSuccess=None)
    def restored(state):
        current=rt.signature(state);excess=current-g
        return all(current[k]>=n for k,n in required.items()) and all(excess[k]<=excess_before[k] for k in new_bad)
    values=[restored(s) for s in window]
    first=next((i+1 for i,v in enumerate(values) if v),None)
    remaining=values[first:] if first is not None else []
    retention=(False if remaining and not all(remaining) else
               True if len(remaining)>=minimum_retention_decisions else None)
    return dict(repairApplicable=True,observedRecovery=bool(values[-1]) if values else None,
        firstRecoveryDecision=first,retainedAfterRecovery=retention,windowDecisions=len(window),
        newlyMissingCorrectPlacements=sum(lost.values()),newExcessPlacements=sum(new_bad.values()),
        detectionSuccess=None,referencePrefixEqualityRequired=False)


def aggregate(records):
    """One record per model/condition/input version. Alias tasks cannot inflate SR.

    Pair metrics are aggregated separately over eligible pairs; never mix them
    with static SR. Bootstrap units should be canonical original source groups.
    """
    groups=defaultdict(list);seen=set()
    for r in records:
        token=(r['model'],r['inputVersion'],r['conditionId'],r.get('sensorVersion','archived'),r.get('targetContract','exact-physical-parts-and-poses'))
        if token in seen:raise ValueError('Duplicate attempt for a model/condition/input version')
        seen.add(token);run_status(r)
        groups[r['model'],r['inputVersion'],r['track'],r['taskType'],r.get('sensorVersion','archived'),r.get('targetContract','exact-physical-parts-and-poses')].append(r)
    out=[]
    for (model,version,track,task_type,sensor,contract),rows in groups.items():
        valid=[r for r in rows if run_status(r)['abilityEligible']]
        tasks=defaultdict(list)
        for r in valid:tasks[r['canonicalTaskId']].append(run_status(r)['success'])
        # Multiple paired-prefix controls remain conditions. Their task weight
        # is normalized; they do not become independent extra tasks.
        task_scores={k:sum(v)/len(v) for k,v in tasks.items()}
        objects=defaultdict(list);sources=defaultdict(list)
        for tid,score in task_scores.items():
            sample=next(r for r in valid if r['canonicalTaskId']==tid)
            objects[sample['objectId']].append(score);sources[sample['sourceGroup']].append(score)
        statuses=Counter(r['terminalStatus'] for r in rows)
        out.append(dict(model=model,inputVersion=version,sensorVersion=sensor,targetContract=contract,track=track,taskType=task_type,plannedConditions=len(rows),
            validConditions=len(valid),validDistinctTasks=len(tasks),terminalStatuses=dict(statuses),
            conditionSuccessRate=rate(sum(run_status(r)['success'] for r in valid),len(valid)),
            distinctTaskSuccessRate=rate(sum(task_scores.values()),len(task_scores)),
            objectMacroSuccessRate=rate(sum(sum(v)/len(v) for v in objects.values()),len(objects)),
            sourceMacroSuccessRate=rate(sum(sum(v)/len(v) for v in sources.values()),len(sources)),
            validRunCoverage=rate(len(valid),len(rows)),
            operationalCompletion=rate(sum(run_status(r)['success'] for r in valid),len(rows)),
            populationSuccessCI=None,modelRepeatabilityMeasured=False))
    return out


def aggregate_pairs(pairs):
    """Aggregate qualified pair outcomes with both denominators and exclusions."""
    groups=defaultdict(list);seen=set()
    for pair in pairs:
        c,e=pair['control'],pair['intervention']
        token=(e['model'],e['inputVersion'],e['conditionId'],e.get('sensorVersion','archived'),e.get('targetContract','exact-physical-parts-and-poses'))
        if token in seen:raise ValueError('Duplicate paired condition')
        seen.add(token)
        proof=pair.get('sharedPrefixProof',{})
        measured=pair_metrics(c,e,shared_prefix_verified=proof.get('verified') is True)
        groups[e['model'],e['inputVersion'],e['track'],e['taskType'],e.get('sensorVersion','archived'),e.get('targetContract','exact-physical-parts-and-poses')].append(measured)
    out=[]
    for (model,version,track,kind,sensor,contract),rows in groups.items():
        eligible=[r for r in rows if r['recoveryPairEligible']]
        comparable=[r for r in rows if r['pairedComparisonEligible']]
        out.append(dict(model=model,inputVersion=version,sensorVersion=sensor,targetContract=contract,track=track,taskType=kind,
            plannedPairs=len(rows),conditionalRecoveryEligibleN=len(eligible),pairedComparisonN=len(comparable),
            conditionalRecoveryRate=rate(sum(r['conditionalRecoverySuccess'] for r in eligible),len(eligible)),
            pairedCompletionDrop=rate(sum(r['pairedCompletionDrop'] for r in comparable),len(comparable)),
            reasons=dict(Counter(r['reason'] for r in rows)),
            exclusionReasons=dict(Counter(k for r in rows for k in r['exclusionReasons'])),
            scheduledEvents=sum(r['scheduledEvents'] for r in rows),appliedEvents=sum(r['appliedEvents'] for r in rows),
            triggerCoverage=rate(sum(r['appliedEvents'] for r in rows),sum(r['scheduledEvents'] for r in rows))))
    return out
