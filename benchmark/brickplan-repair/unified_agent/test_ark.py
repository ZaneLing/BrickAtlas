"""Provider routing and generation settings: no network or paid requests."""
import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from unified_agent.providers import PaidTransport,route

class ArkChecks(unittest.TestCase):
 def test_exact_host_key_and_no_fallback(self):
  for model in ['gpt-6-1-sol-260929','doubao-seed-2-1-pro-260915','deepseek-v4-1-flash-261017']:
   self.assertEqual(route('ark/'+model),dict(provider='ark',model=model,baseURL='https://ark.cn-beijing.volces.com/api/v3',keyEnv='ARK_API_KEY'))
  self.assertEqual(route('qwen/qwen3.8-flash')['provider'],'aliyun')
 def test_payload_and_cny_accounting(self):
  for model in ['gpt-6-1-sol-260929','doubao-seed-2-1-pro-260915','deepseek-v4-1-flash-261017']:
   requests=[]
   def http(url,secret=None,body=None,timeout=180):
    self.assertTrue(url.startswith('https://ark.cn-beijing.volces.com/api/v3/'))
    if url.endswith('/models'):return {'data':[{'id':model}]}
    requests.append(json.loads(Path(body).read_text()))
    return dict(id='test',usage=dict(prompt_tokens=100,completion_tokens=20),choices=[dict(finish_reason='stop',message=dict(content='{"tool":"finish"}'))])
   with tempfile.TemporaryDirectory() as tmp,patch('unified_agent.providers.env',side_effect=lambda k: 'not-a-secret' if k=='ARK_API_KEY' else None),patch('unified_agent.providers.http',side_effect=http):
    t=PaidTransport(Path(tmp)/'run',8,'ark/'+model,ledger_path=Path(tmp)/'ledger.json')
    t(dict(messages=[dict(role='user',content='JSON action')]))
    body=requests[0]
    self.assertNotIn('provider',body)
    self.assertEqual(body['model'],model)
    self.assertAlmostEqual(t.usage()['costUSD'],t.usage()['nativeCosts']['CNY']*.2)
    if model.startswith('gpt'):
     self.assertEqual(body['reasoning_effort'],'low');self.assertEqual(body['max_completion_tokens'],8192)
     self.assertNotIn('temperature',body);self.assertFalse(t.price['arkPriceVerified'])
    else:self.assertEqual(body['thinking'],{'type':'disabled'})
    if model.startswith('deepseek'):self.assertNotIn('response_format',body)

if __name__=='__main__':unittest.main()
