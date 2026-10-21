"""Offline regression gates for the visual-only protocol. No model API calls."""
import base64,hashlib,io,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
from protocol import Episode,load
from render import Renderer
from vision import VisionRenderer,observe,images,request_body,SIZE

class VisualProtocol(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert,cls.cases=load('10001');cls.case=cls.cases['10001:height_layer:a65ccf24']
        cls.renderer=VisionRenderer(cls.cert)
    def episode(self):
        ep=Episode(self.cert,self.case,protocol_version='v3');ep.vision_renderer=self.renderer;return ep
    def test_no_symbolic_input_or_hidden_geometry(self):
        ep=self.episode();o=ep.observe('visual')
        forbidden={'catalog','current','target','transform','supportAnyOf','pathMustBeEmpty','overlapMustBeEmpty','ldraw','description','color','oraclePlan','roots','initial','expectedOptimum','legalActions'}
        def walk(value):
            if isinstance(value,dict):
                self.assertFalse(set(value)&forbidden)
                for v in value.values():walk(v)
            elif isinstance(value,list):
                for v in value:walk(v)
        walk(o)
        with self.assertRaises(ValueError):ep.observe('symbolic')
        import run
        with self.assertRaises(ValueError):run.run_one({},'unused','symbolic')
        with self.assertRaises(ValueError):run.run_one({'protocolVersion':'v2'},'unused','visual')
        other=Episode(self.cert,next(c for c in self.cases.values() if c['kind']=='control'),protocol_version='v3')
        self.assertEqual(o['actionHandles'],other.observe('visual')['actionHandles'])
    def test_clean_native_scene_and_full_resolution_crop(self):
        ep=self.episode()
        with patch('PIL.ImageDraw.Draw',side_effect=AssertionError('Text drawing in scene')):
            im,mask=self.renderer.rgb(ep.assignments())
            zoom,_=self.renderer.rgb(ep.assignments(),crop=[.25,.25,.75,.75])
        self.assertEqual(im.size,SIZE);self.assertEqual(zoom.size,SIZE)
        self.assertGreater(np.count_nonzero(mask),200000)
        # New view fits the structure to the image; the old per-view raster did not.
        _,old=Renderer(self.cert).render(ep.assignments(),size=(384,288))
        oldx=np.where(old)[1];newx=np.where(mask)[1]
        self.assertGreater(np.ptp(newx)/np.ptp(oldx),4)
    def test_images_in_request_are_exact_native_png(self):
        ep=self.episode()
        with tempfile.TemporaryDirectory() as tmp:
            records=images(ep,self.renderer,tmp,extra={'view':'bottom','crop':[.25,.25,.75,.75]})
            req=request_body('test-vision-model',observe(ep),records,tmp)
            payload=[c for c in req['messages'][1]['content'] if c['type']=='image_url']
            self.assertEqual(len(payload),len(records));self.assertLessEqual(len(records),16)
            for item,record in zip(payload,records):
                data=base64.b64decode(item['image_url']['url'].split(',',1)[1])
                self.assertEqual(hashlib.sha256(data).hexdigest(),record['sha256'])
                self.assertEqual(item['image_url']['detail'],'high')
                self.assertEqual(Image.open(io.BytesIO(data)).format,'PNG')
                if record['role']!='inventory':self.assertEqual(Image.open(io.BytesIO(data)).size,SIZE)
    def test_point_selection_and_nonmutating_inspection(self):
        ep=self.episode();state=ep.state
        im,mask=self.renderer.rgb(ep.assignments(),supersample=1)
        actor=next(a for a in ep.actors if np.count_nonzero(mask==self.renderer.ids[a])>100)
        yy,xx=np.where(mask==self.renderer.ids[actor]);i=len(xx)//2
        result=ep.step({'type':'inspect','view':'isometric','point':[(int(xx[i])+.5)/SIZE[0],(int(yy[i])+.5)/SIZE[1]]})
        self.assertEqual(result,{'code':'OBSERVATION_READY','partId':ep.alias[actor]});self.assertEqual(ep.state,state)
        for action in [{'type':'inspect','view':'bottom'}, {'type':'inspect','azimuth':70,'elevation':-30},
                       {'type':'inspect','candidate':next(iter(ep.pose_reverse))},
                       {'type':'inspect','partId':ep.alias[actor]},
                       {'type':'inspect','crop':[.2,.2,.8,.8]}]:
            self.assertEqual(ep.step(action)['code'],'OBSERVATION_READY');self.assertEqual(ep.state,state)
        for bad in [{'type':'inspect','point':[2,0]}, {'type':'inspect','crop':[0,0,0,0]},
                    {'type':'inspect','candidate':'C_NOT_REAL'}, {'type':'attach','partId':ep.alias[actor]},
                    {'type':'inspect','azimuth':float('nan'),'elevation':0}, {'type':['inspect']}]:
            self.assertEqual(ep.step(bad)['code'],'INVALID_ACTION');self.assertEqual(ep.state,state)
    def test_oracle_actions_still_execute_without_prompt_truth(self):
        for case in self.cases.values():
            ep=Episode(self.cert,case,protocol_version='v3')
            for action in case['oraclePlan']:
                public={k:ep.alias[v] if k=='partId' else ep.pose(v) if k=='candidate' else v for k,v in action.items()}
                self.assertEqual(ep.step(public)['code'],'OK',case['id'])
            self.assertEqual(ep.step({'type':'finish'})['code'],'SUCCESS')

if __name__=='__main__':unittest.main(verbosity=2)
