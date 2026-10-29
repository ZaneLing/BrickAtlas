import unittest
from scaling_release.arena_metrics import normal_qualified_recovery

class RecoveryContract(unittest.TestCase):
 def test_correct_intermediate_stage_stops_without_finishing_whole_object(self):
  import json,tempfile
  from bench_design.session import Session
  from dynamic_arena.validate_replays import Witness
  with tempfile.TemporaryDirectory() as directory:
   session=Session.open('E7:v7::v7-long-bookshelf::static::control::t4',directory,'scripted:regression')
   session.autosave=False
   self.assertLess(sum(bool(v) for v in session.goal.values()),len(session.packet.manual['actions']))
   witness=Witness(session)
   self.assertEqual(json.loads(witness({}))['tool'],'observe')
   action=json.loads(witness({}));self.assertEqual(action['tool'],'finish')
   session.submit({'type':'finish'})
   self.assertTrue(session.result()['success'])
 def test_denominators_and_untriggered(self):
  base=dict(success=True,repairPrerequisite=dict(eligible=True,normalRunId='normal-proof'),terminalStatus='completed',scheduledEvents=2,appliedEvents=2,effectiveIncidentVerified=True)
  self.assertTrue(normal_qualified_recovery(base)['success'])
  self.assertFalse(normal_qualified_recovery(base)['causalEffectClaim'])
  for changes,reason in [({'appliedEvents':0},'untriggered'),({'appliedEvents':1},'not_all_events_triggered'),({'terminalStatus':'service_error'},'run_interrupted'),({'repairPrerequisite':None},'no_successful_matched_normal'),({'effectiveIncidentVerified':False},'incident_effect_unverified')]:
   value=normal_qualified_recovery({**base,**changes});self.assertIsNone(value['success']);self.assertEqual(value['reason'],reason)

if __name__=='__main__':unittest.main()
