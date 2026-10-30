"""No-API integration checks for evidence, memory, budgets and repair scoring."""
import json,tempfile,unittest
from pathlib import Path
from copy import deepcopy
from dynamic_arena.demo import create
from dynamic_arena.run import NoProvider
from bench_design.session import internal_action
from unified_agent.agent import VisualAgent,parse_agent
from unified_agent.profile import profile
from unified_agent.run import gate
from unified_agent.providers import route


class AgentChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)

    def tearDown(self):self.tmp.cleanup()

    def agent(self,name='a',events=False,configuration=None):
        t=NoProvider();t.model='scripted:test'
        s=create(self.root/name,t.model,events=events);s.control=not events;s.autosave=False
        a=VisualAgent(s,t,configuration);a.spectator_frame=lambda *args:None
        return a

    def send(self,a,tool,args=None):
        return a.step(dict(tool=tool,args=args or {},plan=['Verify the current assembly'],notes='Test-authored public notes'))

    def move(self,a,action):
        v=internal_action(a.session.ep,action);tool=v.pop('type');return self.send(a,tool,v)

    def test_routes(self):
        for name in ['qwen/qwen3-vl-235b-a22b-instruct','qwen3-vl-235b-a22b-instruct']:
            self.assertEqual(route(name)['provider'],'aliyun')
        self.assertEqual(route('deepseek/deepseek-flash')['keyEnv'],'DEEPSEEK_API_KEY')
        self.assertEqual(route('google/gemini-2.5-flash')['provider'],'openrouter')

    def test_strict_output(self):
        p=profile();self.assertFalse(parse_agent('```json\n{}\n```',p)[1])
        self.assertEqual(len(parse_agent(dict(tool='finish',args={},plan=[],notes='x'*1201),p)[0]['notes']),1200)
        self.assertTrue(parse_agent(dict(tool='finish',args={},plan=[],notes=''),p)[1])

    def test_json_and_argument_errors_are_separate(self):
        a=self.agent()
        a.step('{"tool":')
        a.step(dict(tool='observe',args=dict(view='diagonal-unknown',show=['current']),plan=[],notes=''))
        self.assertTrue(a.session.records[0]['parseError'])
        self.assertFalse(a.session.records[1]['parseError'])
        metrics=a.result()['executionMetrics']
        self.assertEqual(metrics['formatErrorResponses'],1)
        self.assertEqual(metrics['schemaErrorResponses'],1)

    def test_persistent_memory_no_unrequested_refresh(self):
        a=self.agent();before=a.request();self.assertEqual(len(before[3]),7)
        targets=[i['sha256'] for i in before[3] if i['role']=='target']
        action=a.session.row['case']['normalReferenceActions'][0];self.move(a,action)
        after=a.request();self.assertEqual(targets,[i['sha256'] for i in after[3] if i['role']=='target'])
        old=[i for i in after[3] if i['role']=='current'];self.assertTrue(all(i['historicalNotLive'] for i in old))
        self.assertEqual([i['sha256'] for i in old],[i['sha256'] for i in before[3] if i['role']=='current'])
        self.assertEqual(after[2]['memory']['notes'],'Test-authored public notes')
        self.send(a,'observe',dict(view='angled',rotateDegrees=90,show=['current','target','inventory']))
        later=a.request();self.assertTrue(any(i['role']=='current' and not i['historicalNotLive'] for i in later[3]))
        self.assertEqual(a.action_attempts,1);self.assertEqual(a.observation_attempts,1)
        self.assertTrue(any(i['role']=='target' and i.get('camera',{}).get('azimuthDegrees')==125 for i in later[3]))
        public=json.dumps(later[2]);self.assertNotIn('recoveryWitness',public);self.assertNotIn('privateEvent',public)

    def test_alternative_order_and_gate(self):
        a=self.agent();moves=a.session.row['case']['normalReferenceActions']
        for move in list(reversed(moves[:-1]))+moves[-1:]:self.assertEqual(self.move(a,move)['code'],'OK')
        self.send(a,'finish');r=a.result();self.assertTrue(r['success']);self.assertFalse(r['repairApplicable'])
        r.update(arenaBranch='normal',arenaRunId='scripted-proof')
        b=self.agent('b',events=True);self.assertTrue(gate(r,b))
        b.profile['maxActions']+=1;b.contract_sha='changed';self.assertFalse(gate(r,b))

    def test_untriggered_and_effective_incident(self):
        empty=self.agent('untriggered',events=True);self.send(empty,'finish')
        self.assertEqual(empty.result()['incidentExposure'],'untriggered');self.assertIsNone(empty.result()['normalQualifiedRecovery']['success'])
        a=self.agent(events=True)
        for move in a.session.row['case']['normalReferenceActions']:self.move(a,move)
        self.assertEqual(len(a.session.events),1)
        # A missing foot is now under the tabletop. Remove the top first;
        # otherwise the real straight-path checker correctly rejects repair.
        top=a.session.row['case']['normalReferenceActions'][-1]
        self.assertEqual(self.move(a,dict(type='detach',actor=top['actor']))['code'],'OK')
        missing=[(actor,k) for actor,k in a.session.goal.items() if k and a.session.ep.state.get(actor)!=k]
        for actor,k in sorted(missing,key=lambda item:item[0]==top['actor']):self.assertEqual(self.move(a,dict(type='attach',actor=actor,candidate=k))['code'],'OK')
        self.send(a,'finish');r=a.result();self.assertTrue(r['success']);self.assertTrue(r['repairApplicable'])
        self.assertTrue(r['allWindowsRecovered'])

    def test_separate_budgets(self):
        a=self.agent(configuration=profile(maxActions=1,maxObservations=1))
        moves=a.session.row['case']['normalReferenceActions'];self.move(a,moves[0])
        self.assertEqual(self.move(a,moves[1])['code'],'RESOURCE_BUDGET_EXHAUSTED')
        self.assertEqual(a.result()['executionMetrics']['schemaErrorResponses'],0)
        self.assertEqual(a.result()['executionMetrics']['budgetRejectedResponses'],1)
        self.assertEqual(self.send(a,'observe',dict(view='top',rotateDegrees=0,show=['current']))['code'],'OBSERVED')
        self.assertEqual(a.observation_attempts,1)
        self.send(a,'finish');self.assertEqual(a.session.terminal,'completed')


if __name__=='__main__':unittest.main()
