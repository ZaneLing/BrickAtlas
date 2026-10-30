"""The optional manual must describe the same goal as the static target."""
import json
import tempfile
import unittest
from bench_design.session import Session
from dynamic_arena.sensors import Sensors
from dynamic_arena.tool_arena import ToolArena
from dynamic_arena.run import NoProvider
from unified_agent.ark_batch import OUT


class TargetScopeChecks(unittest.TestCase):
    def test_static_reference_stops_at_public_target_stage(self):
        plan = json.loads((OUT / 'plan.json').read_text())
        for obj in plan['objects']:
            for case_id in obj['staticCases']:
                with self.subTest(case=case_id), tempfile.TemporaryDirectory() as tmp:
                    session = Session.open(case_id, tmp)
                    sensor = Sensors(session)
                    stage = session.ep.case['completedInstructionStep']
                    self.assertEqual(sensor.manual_count, stage)
                    self.assertGreater(sensor.full_manual_count, stage)
                    # This pilot's public stage corresponds exactly to its
                    # acceptance target, not just to the number of its parts.
                    self.assertEqual(sensor.manual['states'][stage], session.goal)
                    with self.assertRaisesRegex(ValueError, 'later construction stages'):
                        sensor.instruction(stage + 1)
                    arena = ToolArena(session, NoProvider())
                    request = arena.public_request()
                    self.assertEqual(request['manualSteps'], stage)
                    self.assertEqual(request['targetScope']['kind'], 'static-stage')
                    self.assertIn('If CURRENT already matches TARGET, call finish', request['task'])

    def test_dynamic_keeps_complete_requested_manual(self):
        obj = json.loads((OUT / 'plan.json').read_text())['objects'][0]
        with tempfile.TemporaryDirectory() as tmp:
            session = Session.open(obj['dynamicCase'], tmp, control=True)
            sensor = Sensors(session)
            self.assertEqual(sensor.manual_count, obj['activeParts'])
            self.assertEqual(sensor.manual_count, sensor.full_manual_count)
            self.assertIsNone(sensor.target_stage)


if __name__ == '__main__':
    unittest.main()
