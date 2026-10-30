"""Regression for the real API plate half-turn falsely rejected as an error."""
import gzip,json,tempfile,unittest
from pathlib import Path
from copy import deepcopy
from collections import Counter
import numpy as np
from assembly import Assembly,info
from library import load_aliases
from dynamic_arena.run import open_session
from dynamic_arena.sensors import Sensors
from bench_design.metrics import state_metrics


class PlateSymmetry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.s=open_session('SC:4096-1-alt-1488:dynamic:buried-repair',cls.tmp.name,'scripted:symmetry',True)
        cls.rt=cls.s.ep.runtime

    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()

    def test_verified_plain_alias_and_connector_set(self):
        canonical,transform=load_aliases()['3023'];self.assertEqual(canonical,'3023b')
        np.testing.assert_allclose(transform,np.eye(4))
        part=info(canonical);rotation=np.diag([-1,1,-1,1])
        # Port positions and axes are preserved as a multiset. Index labels
        # of the two identical studs/holes are not physical distinctions.
        def ports(frames):
            return Counter((c[0],c[1],c[2],tuple(np.round(f[:3,3],5)),tuple(np.round(f[:3,1],5))) for c,f in zip(part.conns,frames))
        self.assertEqual(ports(part.frames),ports(rotation@part.frames))

    def test_same_image_connections_and_success(self):
        goal=deepcopy(self.s.goal);half={**goal,'P12':'P12:v7-turn2-0'}
        self.assertEqual(self.rt.connections(goal),self.rt.connections(half))
        sensor=Sensors(self.s)
        for view in ('isometric','rear','top'):
            self.assertEqual(sensor.render(goal,view).tobytes(),sensor.render(half,view).tobytes())
        self.assertTrue(self.rt.complete(half))
        self.assertTrue(state_metrics(self.rt,self.s.initial,half,goal,finished=True)['success'])

    def test_wrong_color_missing_shift_and_quarter_turn_still_fail(self):
        goal=deepcopy(self.s.goal);self.assertFalse(self.rt.complete({**goal,'P12':''}))
        p=deepcopy(self.rt.row(goal['P12'])['part'])
        for kind in ['color','shift','quarter']:
            q=deepcopy(p);m=np.array(q['matrix'])
            if kind=='color':q['colorHex']='#ff0000'
            elif kind=='shift':m[0,3]+=20
            else:m=m@np.array([[0,0,1,0],[0,1,0,0],[-1,0,0,0],[0,0,0,1]])
            q['matrix']=m.tolist();key='test-'+kind
            self.rt.extra[key]=dict(actor='P12',part=q)
            self.assertFalse(self.rt.complete({**goal,'P12':key}),kind)


if __name__=='__main__':unittest.main()
