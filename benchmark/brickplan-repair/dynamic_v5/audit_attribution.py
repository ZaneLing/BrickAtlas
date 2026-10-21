"""Separate failed detection from trigger, normal build, and interface failures.

This is an automated pilot gate. It cannot replace blinded human usability results.
"""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
BANK=HERE.parents[2]/'deliverables/brickplan-dynamic-v5'


def main():
    visibility={r['caseId']:r for r in json.loads((BANK/'temporal-interface-audit.json').read_text())['rows']}
    traces={}
    for path in (BANK/'pilot/runs').glob('*/trace.json'):
        run=json.loads(path.read_text())
        if run.get('track') in ('visual-v10','monitor-v4','monitor-v5'):
            traces[(run['caseId'],run['track'])]=run
    rows=[]
    for (case_id,track),run in sorted(traces.items()):
        if case_id.endswith('--control'):continue
        control_id=case_id.rsplit('--',1)[0]+'--control'
        control=traces.get((control_id,track))
        if control is None:continue
        report=run.get('detectionReport',{})
        control_report=control.get('detectionReport',{})
        event_index=report.get('eventDecisionIndex')
        event_step=next((s for s in run['steps'] if s['index']==event_index),None)
        declared=report.get('declaredAtEvent')
        # The diagnostic left panel is the normal post-action state, so its
        # visual difference is eventChangedPixels, even when the event undoes
        # the last move and before/current look identical.
        visible=(visibility[case_id]['eventChangedPixels']>=2000 if track=='monitor-v5'
                 else visibility[case_id]['primaryCandidate'])
        flags={
            'machineVisible':visible,
            'normalBuildCompleted':control.get('score',{}).get('success') is True,
            'normalBuildNoFalseAlarm':control_report.get('preEventFalseAlarms')==0,
            'sameSuccessfulPrefix':
                [s.get('action') for s in control['steps'][:event_index]]==
                [s.get('action') for s in run['steps'][:event_index]] if event_index is not None else False,
            'eventTriggered':run.get('score',{}).get('eventTriggered') is True,
            'eventDecisionObserved':event_step is not None and event_step.get('status')=='executed',
            'detectionAnswerPresent':type(declared) is bool,
            'noPreEventFalseAlarm':report.get('preEventFalseAlarms')==0,
        }
        technically_eligible=all(flags.values())
        rows.append(dict(caseId=case_id,track=track,controlId=control_id,
                         temporalCategory=visibility[case_id]['category'],checks=flags,
                         technicalAttributionEligible=technically_eligible,
                         humanUsabilityValidated=False,
                         paperClaimEligible=False,
                         detectionAtEvent=declared,
                         provisionalDetectionMiss=technically_eligible and declared is False,
                         provisionalRepairFailureAfterDetection=technically_eligible and declared is True and
                                                     run.get('score',{}).get('success') is False,
                         interventionSuccess=run.get('score',{}).get('success')))
    report=dict(schema='brickplan-dynamic-attribution-audit/1',exploratory=True,
                humanValidationStatus='No blinded reviewer answers received; no row supports a final paper claim.',
                rows=rows)
    (BANK/'pilot/attribution-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(pairs=len(rows),technicallyEligible=sum(r['technicalAttributionEligible'] for r in rows),
                          provisionalDetectionMisses=sum(r['provisionalDetectionMiss'] for r in rows)),ensure_ascii=False))


if __name__=='__main__':main()
