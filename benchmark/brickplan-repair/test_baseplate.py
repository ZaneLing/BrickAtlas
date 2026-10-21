"""Environment/interaction regressions for the infinite white baseplate."""
import json
from pathlib import Path
import sys
import unittest
import numpy as np
from baseplate import PlateAssembly, PLATE

ROOT = Path(__file__).resolve().parents[2]

def certificate(model='v23-3223--deep'):
    return json.loads((ROOT/'deliverables/brickplan-repair-library/models'/model/'qualification.json').read_text())


class WhiteBaseplateContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = PlateAssembly(certificate())

    def test_environment_is_not_a_model_part_and_source_is_immutable(self):
        source = certificate(); a = PlateAssembly(source)
        self.assertIn('F001', source['fixed']); self.assertNotIn('F001:goal', source['candidates'])
        self.assertEqual(a.cert['fixed'], {}); self.assertIn('F001', a.actors)
        self.assertNotIn(PLATE, a.actors); self.assertNotIn(PLATE, a.goal)
        state = dict(a.goal); state['F001'] = ''
        self.assertFalse(a.complete(state)); self.assertTrue(a.complete(a.goal))

    def test_all_parts_can_be_built_from_and_removed_to_an_empty_plate(self):
        a = self.a; manual = a.manual()
        self.assertTrue(manual['complete']); self.assertTrue(manual['pathVerified'])
        state = manual['states'][0]; self.assertFalse(any(state.values()))
        self.assertEqual(a.present(state), {})
        for actor, target in zip(manual['parts'], manual['states'][1:]):
            state, result = a.check(state, actor, 'attach', candidate=target[actor])
            self.assertEqual(result['code'], 'OK', (actor, result))
        self.assertTrue(a.complete(state))
        for actor in reversed(manual['parts']):
            state, result = a.check(state, actor, 'detach')
            self.assertEqual(result['code'], 'OK', (actor, result))
        self.assertFalse(any(state.values()))

    def test_plate_snap_far_from_model_and_former_fixture_is_removable(self):
        a = self.a; empty = {k: '' for k in a.actors}
        template = a.plate_snaps('F001', np.eye(3).tolist())[0]
        pose = np.asarray(template['rawMatrix']); pose[:3,3] += a.board[:3,:3] @ [2000,0,-1800]
        state, result = a.check(empty, 'F001', 'attach', raw=pose.tolist())
        self.assertEqual(result['code'], 'OK')
        self.assertIn(PLATE, result['components'][0])
        state, result = a.check(state, 'F001', 'detach')
        self.assertEqual(result['code'], 'OK'); self.assertEqual(state, empty)

    def test_misaligned_studs_and_below_plate_cannot_be_installed(self):
        a = self.a; empty = {k: '' for k in a.actors}
        template = np.asarray(a.plate_snaps('F001', np.eye(3).tolist())[0]['rawMatrix'])
        for shift in ([5,0,0], [0,8,0]):
            pose = template.copy(); pose[:3,3] += a.board[:3,:3] @ shift
            state, result = a.check(empty, 'F001', 'attach', raw=pose.tolist())
            self.assertEqual(result['code'], 'ENDPOINT_COLLISION'); self.assertIn(PLATE, result['blockers'])
            self.assertEqual(state, empty)

    def test_bottom_parts_have_multiple_valid_orders(self):
        for order in [('F001','P001','P002'), ('P002','P001','F001')]:
            state = {k: '' for k in self.a.actors}
            for actor in order:
                state, result = self.a.check(state, actor, 'attach', candidate=self.a.goal[actor])
                self.assertEqual(result['code'], 'OK')

    def test_flat_foot_model_does_not_intersect_studs(self):
        a = PlateAssembly(certificate('v23-3178'))
        self.assertEqual(a.baseplate['mounting'], 'resting')
        self.assertFalse(any(a.plate_collision(p) for p in a.present(a.goal).values()))
        self.assertTrue(any(a.on_plate(p) for p in a.present(a.goal).values()))

    def test_cached_scene_legacy_cases_and_incompatible_cases(self):
        sys.path.insert(0, str(ROOT/'benchmark/brickplan-v2.3'))
        from repair_workbench import RepairWorkbench
        api = RepairWorkbench(); model = 'v23-3223--deep'
        data = api.get('/models/'+model)
        self.assertEqual(data['scene']['fixed'], []); self.assertEqual(data['scene']['fixedIds'], {})
        self.assertTrue(data['scene']['baseplate']['infinite'])
        self.assertIn('F001', data['scene']['partIds'].values())
        self.assertEqual(len(data['scene']['mutable']), len(data['scene']['parts']))
        detail = api.get('/models/'+model+'/cases/'+data['cases'][0]['id'])
        self.assertEqual(detail['case']['initial']['F001'], 'F001:goal')
        self.assertTrue(all(s['F001']=='F001:goal' for s in detail['snapshots']))
        excluded = api.excluded_source_cases('v23-21018')
        self.assertTrue(excluded)
        self.assertFalse(set(excluded).intersection(api.cases('v23-21018')))

if __name__ == '__main__': unittest.main(verbosity=2)
