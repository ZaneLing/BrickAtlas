"""Normal-qualified recovery for independent Arena runs; no causal-fork claim."""

def normal_qualified_recovery(record):
 gate=record.get('repairPrerequisite') or {}
 reason=('normal_control' if not record.get('scheduledEvents') else
         'no_successful_matched_normal' if not gate.get('eligible') else
         'run_interrupted' if record.get('terminalStatus') not in ('completed','model_budget_exhausted') else
         'untriggered' if not record.get('appliedEvents') else
         'not_all_events_triggered' if record['appliedEvents']!=record['scheduledEvents'] else
         'incident_effect_unverified' if not record.get('effectiveIncidentVerified') else 'eligible')
 eligible=reason=='eligible'
 return dict(eligible=eligible,reason=reason,success=bool(record['success']) if eligible else None,normalRunId=gate.get('normalRunId'),sameTaskModelBudgetAndInputRequired=True,sharedPrefixVerified=bool(gate.get('sharedPrefixVerified')),causalEffectClaim=False)
