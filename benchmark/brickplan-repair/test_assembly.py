"""Regression checks of physical transition/evaluation contracts; no model API."""
import json
from pathlib import Path
import sys
import unittest
import numpy as np
from assembly import Assembly, PROTOCOL
from engine import Domain
ROOT = Path(__file__).resolve().parents[2]
FOLDER = ROOT/'deliverables/brickplan-repair-library/models/v23-3223--deep'

class AssemblyContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert=json.loads((FOLDER/'qualification.json').read_text())
        cls.a=Assembly(cls.cert)
        cls.cases=json.loads((FOLDER/'cases.json').read_text())

    def test_nonconvex_collision_is_symmetric_and_containment_still_rejected(self):
        from geometry import endpoint_pair, mm, xf, contains_surface_component
        cert=json.loads((ROOT/'deliverables/brickplan-repair-library/models/v23-30285/qualification.json').read_text())
        a=cert['candidates']['P004:goal']['part'];b=cert['fixed']['F001']
        self.assertEqual(endpoint_pair(a,b)['status'],'CLEAR')
        self.assertEqual(endpoint_pair(b,a)['status'],'CLEAR')
        # Genuine full containment must still be rejected without intersections.
        outer=mm.makeCube(mm.Vector3f(10,10,10),mm.Vector3f(0,0,0))
        inner=mm.makeCube(mm.Vector3f(1,1,1),mm.Vector3f(4,4,4))
        self.assertTrue(contains_surface_component(inner,outer,xf(np.eye(4)),mm.getAllComponents(inner)))
        self.assertFalse(contains_surface_component(outer,inner,xf(np.eye(4)),mm.getAllComponents(outer)))

    def test_all_reference_additions_are_executable(self):
        manual=self.a.manual(); self.assertTrue(manual['complete']); self.assertFalse(any(manual['states'][0].values()))
        state=manual['states'][0]
        for actor,next_state in zip(manual['parts'],manual['states'][1:]):
            state,check=self.a.check(state,actor,'attach',candidate=next_state[actor])
            self.assertEqual(check['code'],'OK'); self.assertEqual(state,next_state)
        self.assertTrue(self.a.complete(state))

    def test_every_existing_case_plan_and_nonoptimal_detour(self):
        for case in self.cases.values():
            state=self.a.state(case['initial'])
            for action in case['oraclePlan']:
                state,check=self.a.check(state,action['partId'],action['type'],candidate=action.get('candidate'))
                self.assertEqual(check['code'],'OK',(case['id'],action,check))
            self.assertTrue(self.a.complete(state),case['id'])
        # An unnecessary detach/attach cycle still ends successfully.
        state,check=self.a.check(self.a.goal,'P015','detach');self.assertEqual(check['code'],'OK')
        state,check=self.a.check(state,'P015','attach',candidate=self.a.goal['P015']);self.assertEqual(check['code'],'OK')
        self.assertTrue(self.a.complete(state))

    def test_handheld_components_are_not_rejected_as_unsupported(self):
        folder=ROOT/'deliverables/brickplan-repair-library/models/31027'
        cert=json.loads((folder/'qualification.json').read_text()); a=Assembly(cert); domain=Domain(cert,{})
        source=json.loads((folder/'cases.json').read_text())['31027:offset:273da8dd']
        case=dict(actors=a.actors,rackCapacity=len(a.actors),choices={actor:[k for k,r in cert['candidates'].items() if r['actor']==actor] for actor in a.actors})
        state=a.state(source['initial'])
        _,old=domain.transition(case,domain.pack(case,state),{'type':'detach','partId':'P005'})
        self.assertEqual(old['code'],'DISCONNECTED_ASSEMBLY')
        after,check=a.check(state,'P005','detach')
        self.assertEqual(check['code'],'OK'); self.assertIn(['P002','P003'],check['components'])
        graph,_=a.connections(after);self.assertIn('P003',graph['P002'])

    def test_snap_generation_has_no_dependency_on_goal(self):
        state=dict(self.a.goal);state['P015']=''
        before=self.a.snaps(state,'P015',np.eye(3).tolist())
        original=self.a.goal;self.a.goal={a:'' for a in self.a.actors}
        try:self.assertEqual(before,self.a.snaps(state,'P015',np.eye(3).tolist()))
        finally:self.a.goal=original
        self.assertGreater(len(before),20)
        self.assertTrue(any(not any(np.allclose(s['rawMatrix'],r['part']['rawMatrix']) for r in self.cert['candidates'].values() if r['actor']=='P015') for s in before))

    def test_snapping_on_tilted_assembly(self):
        cert=json.loads((ROOT/'deliverables/brickplan-repair-library/models/v23-30285/qualification.json').read_text())
        a=Assembly(cert);state=dict(a.goal);state['P004']=''
        snaps=[]
        for quarter in range(4):
            co=round(np.cos(quarter*np.pi/2));si=round(np.sin(quarter*np.pi/2))
            snaps.extend(a.snaps(state,'P004',[[co,0,si],[0,1,0],[-si,0,co]]))
        self.assertGreater(len(snaps),0)
        self.assertTrue(any(np.allclose(s['rawMatrix'],cert['candidates']['P004:goal']['part']['rawMatrix'],atol=.001) for s in snaps))

    def test_free_pose_authoring_survives_restart(self):
        import tempfile
        sys.path.insert(0,str(ROOT/'benchmark/brickplan-v2.3'))
        from repair_workbench import RepairWorkbench, OUT
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            for name in ['index.json','cases.jsonl','models']:(root/name).symlink_to(OUT/name)
            api=RepairWorkbench(root);model='v23-3223--deep';a=api.assembly(model)
            state=dict(a.goal);state['P014']='';raw=np.eye(4);raw[:3,3]=[20,-88,-80]
            result=api.post('/action',dict(modelId=model,assignments=state,action=dict(type='attach',partId='P014',rawMatrix=raw.tolist())))
            self.assertEqual(result['code'],'OK')
            case=api.post('/save',dict(modelId=model,assignments=result['assignments'],title='regression'))['case']
            self.assertIsNone(case['expectedOptimum']);self.assertFalse(case['referenceIsOptimal'])
            self.assertEqual(case['kind'],'offset');self.assertEqual(case['referenceCost'],2)
            other=RepairWorkbench(root)
            snapshots=other.get(f'/models/{model}/cases/{case["id"]}')['snapshots']
            self.assertTrue(other.assembly(model).complete(snapshots[-1]))

    def test_collision_rejected_without_mutating_state(self):
        state=dict(self.a.goal);state['P015']=''
        raw=self.cert['candidates']['P014:goal']['part']['rawMatrix']
        after,check=self.a.check(state,'P015','attach',raw=raw)
        self.assertEqual(check['code'],'ENDPOINT_COLLISION');self.assertEqual(state,after)
        raw=np.eye(4);raw[:3,3]=[1000,1000,1000]
        after,check=self.a.check(state,'P015','attach',raw=raw.tolist())
        self.assertEqual(check['code'],'NO_CONNECTION');self.assertEqual(state,after)

    def test_equivalent_parts_and_rotations(self):
        state=dict(self.a.goal)
        # The two orange 3298 pieces are physically interchangeable.
        p=self.cert['candidates']['P014:goal']['part'];q=self.cert['candidates']['P015:goal']['part']
        self.assertEqual(p['colorHex'],q['colorHex'])
        state['P014']=self.a.register('P014',q['rawMatrix']);state['P015']=self.a.register('P015',p['rawMatrix'])
        self.assertTrue(self.a.complete(state))
        m=np.asarray(self.cert['candidates']['P003:goal']['part']['rawMatrix'])@np.diag([-1,1,-1,1])
        state['P003']=self.a.register('P003',m.tolist());self.assertTrue(self.a.complete(state))
        state['P003']='';self.assertFalse(self.a.complete(state))

    def test_vlm_uses_same_transition_and_final_state_evaluation(self):
        sys.path.insert(0,str(Path(__file__).parent/'eval'))
        from protocol import Episode
        case=next(c for c in self.cases.values() if c['kind']=='control')
        ep=Episode(self.cert,case,protocol_version='v3')
        self.assertEqual(ep.step({'type':'detach','partId':ep.alias['P015']})['code'],'OK')
        self.assertEqual(ep.step({'type':'attach','partId':ep.alias['P015'],'candidate':ep.pose_alias['P015:goal']})['code'],'OK')
        self.assertEqual(ep.step({'type':'finish'})['code'],'SUCCESS')
        score=ep.score();self.assertEqual(score['manipulations'],2);self.assertEqual(score['manipulationProtocol'],PROTOCOL)

if __name__=='__main__': unittest.main(verbosity=2)
