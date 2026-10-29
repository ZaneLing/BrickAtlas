"""A billing error must retain evidence and keep the full budget reservation."""
import gzip,json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from dynamic_arena.transport import Transport

class ReceiptEvidence(unittest.TestCase):
 def check_response(self,response,ok):
  with tempfile.TemporaryDirectory() as tmp:
   t=Transport.__new__(Transport);t.directory=Path(tmp)/'run';t.model='test/model'
   t.ledger_path=Path(tmp)/'ledger.json';t.ledger=dict(capUSD=1,charges=[])
   t.secret='unit-test-not-a-real-key';t.input_price=1e-6;t.output_price=1e-6;t.latest=None
   wire=json.dumps(response)
   with patch('dynamic_arena.transport.subprocess.run',return_value=SimpleNamespace(returncode=0,stdout=wire+'\n200')):
    if ok:self.assertEqual(t({'messages':[]}),'{"tool":"finish","args":{}}')
    else:
     with self.assertRaisesRegex(RuntimeError,'verifiable charge'):t({'messages':[]})
   charge=json.loads(t.ledger_path.read_text())['charges'][0]
   archive=t.directory/charge['responseArchive']
   self.assertEqual(json.loads(gzip.decompress(archive.read_bytes())),response)
   self.assertEqual(charge['generationId'],'receipt-test')
   self.assertFalse(list((t.directory/'api').glob('*.pending')))
   self.assertEqual(charge['status'],'settled' if ok else 'uncertain')
   if not ok:
    self.assertIsNone(charge['actualUSD']);self.assertEqual(t.usage()['unsettledReservationsUSD'],charge['reservedUSD'])
   self.assertNotIn(t.secret,gzip.decompress(archive.read_bytes()).decode('utf-8'))
 def test_missing_cost_preserves_receipt(self):
  self.check_response(dict(id='receipt-test',usage={},choices=[dict(message=dict(content='unscored output'))]),False)
 def test_success_remains_settled(self):
  self.check_response(dict(id='receipt-test',usage=dict(cost=.001),choices=[dict(message=dict(content='{"tool":"finish","args":{}}'))]),True)

if __name__=='__main__':unittest.main()
