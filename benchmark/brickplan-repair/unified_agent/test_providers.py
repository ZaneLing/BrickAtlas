"""No-network checks for permanent routes, native receipts and cost ceilings."""
import gzip,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from unified_agent.providers import PaidTransport,CostLimit,total
from dynamic_arena.transport import Transport


class ProviderChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.requests=[]

    def tearDown(self):self.tmp.cleanup()

    def http(self,url,secret=None,body=None,timeout=110):
        self.assertEqual(secret,'test-placeholder')
        if url.endswith('/models'):
            return dict(data=[dict(id='deepseek-flash',input_modalities=['text','image'])])
        if '/models?model=' in url:
            return dict(output=dict(models=[dict(model='qwen3.8-flash',inference_metadata=dict(request_modality=['Image','Text']),
                prices=[dict(prices=[dict(type='input_token',price=.8),dict(type='output_token',price=2.7)])])]))
        self.requests.append((url,json.loads(Path(body).read_text())))
        return dict(id='unit-receipt',usage=dict(prompt_tokens=100,completion_tokens=30,prompt_cache_hit_tokens=10),
            choices=[dict(finish_reason='stop',message=dict(content='{"tool":"finish","args":{},"plan":[],"notes":""}'))])

    def test_native_requests_and_billing_without_cost_field(self):
        with patch('unified_agent.providers.env',return_value='test-placeholder'),patch('unified_agent.providers.http',side_effect=self.http):
            for model,provider in [('qwen/qwen3.8-flash','aliyun'),('deepseek/deepseek-flash','deepseek')]:
                t=PaidTransport(self.root/provider,1,model,ledger_path=self.root/(provider+'.json'))
                t(dict(messages=[dict(role='user',content='Public task')]))
                url,body=self.requests[-1]
                self.assertNotIn('openrouter',url);self.assertNotIn('provider',body)
                self.assertEqual(body['model'],model.split('/')[1])
                if provider=='aliyun':
                    self.assertEqual(body['max_completion_tokens'],8192);self.assertNotIn('max_tokens',body)
                    self.assertFalse(body['preserve_thinking']);self.assertFalse(body['enable_thinking']);self.assertNotIn('reasoning_effort',body)
                    self.assertAlmostEqual(t.usage()['nativeCosts']['CNY'],.000161)
                else:self.assertAlmostEqual(t.usage()['nativeCosts']['USD'],.00006306)
                self.assertEqual(t.usage()['confirmedUSD'],0);self.assertTrue(t.usage()['settled'])
                self.assertEqual(t.ledger['charges'][0]['status'],'usage_estimated')
                self.assertNotIn('test-placeholder',gzip.decompress(next((t.directory/'api').glob('*.request.json.gz')).read_bytes()).decode())

    def test_legacy_entry_accounting_and_preflight_money_stop(self):
        old=dict(capUSD=.1,charges=[dict(status='settled',actualUSD=.0999,reservedUSD=.15,run='old')])
        self.assertEqual(total(old),.0999)
        ledger=self.root/'legacy.json';ledger.write_text(json.dumps(old))
        with patch('unified_agent.providers.env',return_value='test-placeholder'),patch('unified_agent.providers.http',side_effect=self.http):
            t=PaidTransport(self.root/'qwen',.1,'qwen/qwen3.8-flash',ledger_path=ledger)
            with self.assertRaises(CostLimit):t(dict(messages=[dict(role='user',content='x')]))
        self.assertEqual(self.requests,[]);self.assertEqual(len(t.ledger['charges']),1)

    def test_unresolved_same_provider_blocks_without_retry(self):
        ledger=self.root/'ledger.json';ledger.write_text(json.dumps(dict(capUSD=1,charges=[
            dict(status='pending',provider='aliyun',reservedUSD=.02,run='old')])))
        with patch('unified_agent.providers.env',return_value='test-placeholder'),patch('unified_agent.providers.http',side_effect=self.http):
            t=PaidTransport(self.root/'qwen',1,'qwen/qwen3.8-flash',ledger_path=ledger)
            with self.assertRaisesRegex(RuntimeError,'Unsettled'):t(dict(messages=[]))
        self.assertEqual(self.requests,[])

    def test_legacy_runner_cannot_route_native_family_through_openrouter(self):
        with patch('unified_agent.providers.PaidTransport') as native,patch('dynamic_arena.transport.catalogue') as router:
            native.return_value.return_value='reply'
            native.return_value.latest={'archiveId':'test'}
            native.return_value.usage.return_value={'calls':1}
            for model in ['qwen/qwen3.8-flash','qwen3.8-flash','deepseek/deepseek-flash']:
                t=Transport(self.root,model=model)
                self.assertEqual(t({}),'reply');self.assertEqual(t.usage(),{'calls':1})
                self.assertEqual(t.latest,{'archiveId':'test'})
                self.assertEqual(native.call_args.args[2],model)
            router.assert_not_called()


if __name__=='__main__':unittest.main()
