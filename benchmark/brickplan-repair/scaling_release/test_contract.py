import unittest
from scaling_release.arena_metrics import normal_qualified_recovery

class RecoveryContract(unittest.TestCase):
 def test_denominators_and_untriggered(self):
  base=dict(success=True,repairPrerequisite=dict(eligible=True,normalRunId='normal-proof'),terminalStatus='completed',scheduledEvents=2,appliedEvents=2,effectiveIncidentVerified=True)
  self.assertTrue(normal_qualified_recovery(base)['success'])
  self.assertFalse(normal_qualified_recovery(base)['causalEffectClaim'])
  for changes,reason in [({'appliedEvents':0},'untriggered'),({'appliedEvents':1},'not_all_events_triggered'),({'terminalStatus':'service_error'},'run_interrupted'),({'repairPrerequisite':None},'no_successful_matched_normal'),({'effectiveIncidentVerified':False},'incident_effect_unverified')]:
   value=normal_qualified_recovery({**base,**changes});self.assertIsNone(value['success']);self.assertEqual(value['reason'],reason)

if __name__=='__main__':unittest.main()
