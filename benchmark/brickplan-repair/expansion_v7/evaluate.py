"""Multi-incident eligibility; the existing single-incident gate is retained."""
from evaluation_outcomes import pair_assessment, service_error


def pair(control, intervention, control_status='complete', intervention_status='complete', shared_prefix=True):
    out=pair_assessment(control,intervention,control_status,intervention_status,shared_prefix=shared_prefix)
    scheduled=intervention.get('scheduledEvents',0)
    applied=intervention.get('appliedEvents',0)
    if control_status!='complete' or intervention_status!='complete':
        out.update(recoveryPairEligible=False,repairSuccess=None,repairEligibilityReason='run_interrupted',
                   detectionMiss=None,detectionPairMachineEligible=False)
    elif not scheduled:
        out.update(recoveryPairEligible=False,repairSuccess=None,repairEligibilityReason='normal_control')
    elif applied!=scheduled:
        out.update(recoveryPairEligible=False,repairSuccess=None,repairEligibilityReason='not_all_events_triggered',
                   detectionMiss=None,detectionPairMachineEligible=False)
    out.update(scheduledEvents=scheduled,appliedEvents=applied,
               perEventDetectionClaimEligible=False,paperDetectionClaimEligible=False)
    return out
