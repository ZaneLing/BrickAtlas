"""Check concrete UI-contract faults found in the previous paid pilot."""
import json,tempfile,unittest
from pathlib import Path
from dynamic_arena.contract import validate
from dynamic_arena.demo import create
from dynamic_arena.run import NoProvider
from unified_agent.agent import VisualAgent


class InterfaceV4Checks(unittest.TestCase):
    def test_complete_final_json_only(self):
        action={'tool':'finish','args':{}}
        for value in ['Explanation first.\n'+json.dumps(action),'```json\n'+json.dumps(action)+'\n```']:
            result=validate(value)
            self.assertTrue(result['valid']);self.assertEqual(result['action'],action)
            self.assertTrue(result['normalizations'])
        for value in ['{"tool":"finish"} {"tool":"detach"}',
                      'Explanation {"tool":"attach","args":',
                      'Explanation {"tool":"finish","tool":"detach"}',
                      'Explanation {"tool":"finish"} trailing command',
                      'Example {bad}; use {"tool":"finish"}']:
            self.assertFalse(validate(value)['valid'])

    def test_sensor_actions_do_not_install_or_reveal_correctness(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=create(Path(tmp),'scripted:interface',events=False);s.autosave=False
            a=VisualAgent(s,NoProvider());a.spectator_frame=lambda *args:None
            handle=a.sensors.handles()[0];before=json.dumps(s.ep.state,sort_keys=True)
            action=dict(tool='inspect',args=dict(partId=handle['id'],candidate=handle['candidates'][0],view='top'))
            self.assertTrue(validate(action)['valid'])
            output,images=a.execute(action,1)
            self.assertEqual(output['code'],'OBSERVED');self.assertEqual(len(images),1)
            self.assertEqual((images[0]['width'],images[0]['height']),(1600,636))
            self.assertFalse(output['inspection']['legalityOrCorrectnessShown'])
            self.assertEqual(before,json.dumps(s.ep.state,sort_keys=True))
            output,images=a.execute(dict(tool='inspect',args=dict(point=[0,0],view='top')),2)
            self.assertEqual(output['code'],'OBSERVED');self.assertIsNone(output['inspection']['partId'])
            self.assertEqual(before,json.dumps(s.ep.state,sort_keys=True))
            self.assertFalse(validate(dict(tool='inspect',args=dict(point=[2,0])))['valid'])
            self.assertFalse(validate(dict(tool='inspect',args=dict(partId=handle['id'],candidate=handle['candidates'][0],page=1)))['valid'])


if __name__=='__main__':unittest.main()
