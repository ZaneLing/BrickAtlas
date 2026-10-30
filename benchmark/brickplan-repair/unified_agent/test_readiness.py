"""Regression cases drawn from the actual pilot failures; no paid requests."""
import json,tempfile,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from dynamic_arena.contract import validate
from dynamic_arena.demo import create
from dynamic_arena.run import NoProvider
from unified_agent.agent import VisualAgent
from unified_agent.providers import PaidTransport,http
from unified_agent.failures import GenerationError,ProviderError
from unified_agent import test_providers as provider_checks
from unified_agent.readiness import require
from unified_agent.profile import profile


class ContractRegression(unittest.TestCase):
 def test_observed_pilot_omissions_have_declared_meaning(self):
  for args in [{},{'view':'top','show':['current']},{'view':'isometric','rotateDegrees':'270'}]:
   r=validate(dict(tool='observe',args=args),memory=True)
   self.assertTrue(r['valid']);self.assertTrue(r['normalizations'])
  r=validate(dict(tool='inspect',args={'manualStep':'1'}));self.assertTrue(r['valid']);self.assertEqual(r['action']['args']['manualStep'],1)
 def test_ambiguous_or_dangerous_json_is_not_repaired(self):
  for obj in ['{"tool":"attach"','{"tool":"finish","tool":"attach"}',
      '{"tool":"observe","args":{"rotateDegrees":NaN}}',{'tool':['finish']},
      {'tool':'attach','args':{'partId':'A1'}},{'tool':'observe','args':{'rotateDegrees':45}},
      {'tool':'inspect','args':{'partId':'A1','manualStep':1}}]:
   self.assertFalse(validate(obj)['valid'])
 def test_memory_optional_and_bad_inventory_observation_atomic(self):
  with tempfile.TemporaryDirectory() as tmp:
   t=NoProvider();t.model='scripted:test';s=create(Path(tmp),t.model,events=False);s.control=True;s.autosave=False
   a=VisualAgent(s,t);a.spectator_frame=lambda *args:None
   a.step(dict(tool='observe',args={},notes='keep this',plan=['watch']))
   a.step(dict(tool='observe',args={}))
   self.assertEqual(a.notes,'keep this');self.assertEqual(a.plan,['watch'])
   before=deepcopy(s.ep.state);angle=a.azimuth
   output=a.step(dict(tool='observe',args=dict(rotateDegrees=90,show=['inventory'],inventoryPage=999)))
   self.assertEqual(output['code'],'INVALID_SENSOR_REQUEST');self.assertEqual(a.azimuth,angle);self.assertEqual(s.ep.state,before)
 def test_truncated_complete_json_never_executes_and_never_scores_failure(self):
  class Truncated:
   model='test';latest=None
   def usage(self):return dict(calls=1,costUSD=0,completionTokens=8192)
   def __call__(self,payload):raise GenerationError('OUTPUT_TRUNCATED','Token ceiling')
  with tempfile.TemporaryDirectory() as tmp:
   s=create(Path(tmp),'test',events=False);s.control=True;s.autosave=False
   a=VisualAgent(s,Truncated());a.spectator_frame=lambda *args:None;a.publish=lambda:None
   before=deepcopy(s.ep.state);r=a.run()
   self.assertEqual(r['terminalStatus'],'output_truncated');self.assertIsNone(r['success'])
   self.assertFalse(s.records);self.assertEqual(s.ep.state,before);self.assertFalse(r['assemblyScoreEligible'])
 def test_no_preflight_certificate_blocks_before_api(self):
  with patch('unified_agent.readiness.certificate_path',return_value=Path('/nonexistent/certificate.json')):
   with self.assertRaisesRegex(ValueError,'Missing API preflight'):require('qwen/qwen3.8-flash',profile())


class ProviderRegression(unittest.TestCase):
 setUp=provider_checks.ProviderChecks.setUp
 tearDown=provider_checks.ProviderChecks.tearDown
 http=provider_checks.ProviderChecks.http
 def test_length_archived_charged_but_not_returned_as_action(self):
  original=self.http
  def truncated(*args,**kwargs):
   r=original(*args,**kwargs)
   if 'choices' in r:r['choices'][0]['finish_reason']='length'
   return r
  with patch('unified_agent.providers.env',return_value='test-placeholder'),patch('unified_agent.providers.http',side_effect=truncated):
   t=PaidTransport(self.root/'qwen',1,'qwen/qwen3.8-flash',ledger_path=self.root/'ledger.json')
   with self.assertRaises(GenerationError):t(dict(messages=[]))
   self.assertEqual(t.usage()['calls'],1);self.assertTrue(t.latest_attempt['responseAvailable']);self.assertTrue(t.usage()['settled'])
 def test_rate_limit_and_timeout_are_separate_without_automatic_resend(self):
  original=self.http
  for code,status,response in [('API_RATE_LIMIT',429,{'error':{'message':'limited'}}),('API_TIMEOUT',None,None)]:
   def error(*args,**kwargs):
    if args[0].endswith('/chat/completions'):raise ProviderError(code,code,status=status,response=response)
    return original(*args,**kwargs)
   with patch('unified_agent.providers.env',return_value='test-placeholder'),patch('unified_agent.providers.http',side_effect=error):
    t=PaidTransport(self.root/code,1,'qwen/qwen3.8-flash',ledger_path=self.root/(code+'.json'))
    with self.assertRaises(ProviderError):t(dict(messages=[]))
    self.assertEqual(t.usage()['calls'],1)
    self.assertEqual(t.ledger['charges'][0]['status'],'rejected_before_generation' if status==429 else 'uncertain')
    self.assertEqual(t.ledger['charges'][0]['errorCode'],code)


if __name__=='__main__':unittest.main()
