"""Shared transport keeps provider evidence even when billing is incomplete."""
import gzip,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from dynamic_arena.transport import Transport


class ReceiptEvidence(unittest.TestCase):
 def check_response(self,response,ok):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)
   catalogue=dict(data=[dict(id='test/model',architecture=dict(input_modalities=['image']),
       pricing=dict(prompt='0.000001',completion='0.000001'),supported_parameters=['response_format'])])
   def fake(url,secret=None,body=None,timeout=None):return catalogue if url.endswith('/models') else response
   with patch('unified_agent.providers.http',side_effect=fake),patch('unified_agent.providers.env',return_value='test-placeholder'):
    t=Transport(root/'run',model='test/model',ledger_path=root/'ledger.json')
    if ok:self.assertEqual(t(dict(messages=[])),'{"tool":"finish","args":{}}')
    else:
     with self.assertRaisesRegex(RuntimeError,'verifiable charge'):t(dict(messages=[]))
   charge=json.loads((root/'ledger.json').read_text())['charges'][0]
   self.assertEqual(json.loads(gzip.decompress((root/'run'/charge['responseArchive']).read_bytes())),response)
   self.assertEqual(charge['generationId'],'receipt-test')
   self.assertEqual(charge['status'],'settled' if ok else 'uncertain')
   if not ok:self.assertEqual(t.usage()['unsettledReservationsUSD'],charge['reservedUSD'])
   self.assertFalse(list((root/'run/api').glob('*.pending')))
 def test_missing_cost_preserves_receipt(self):
  self.check_response(dict(id='receipt-test',usage=dict(prompt_tokens=10,completion_tokens=4),choices=[]),False)
 def test_success_remains_settled(self):
  self.check_response(dict(id='receipt-test',usage=dict(cost=.001,prompt_tokens=10,completion_tokens=4),
      choices=[dict(finish_reason='stop',message=dict(content='{"tool":"finish","args":{}}'))]),True)


if __name__=='__main__':unittest.main()
