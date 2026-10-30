"""One model owns a complete episode; the harness never supplies build actions.

The policy command receives a multimodal request on stdin and returns one direct
action object on stdout. It can wrap an existing model transport. This module
does not choose an API service, authorize spending, or execute a GT action file.
"""
from copy import deepcopy
from pathlib import Path
import argparse,base64,hashlib,json,subprocess,uuid
from bench_design import OUT
from bench_design.session import Session,digest
from bench_design.run_episode import SYSTEM
from expansion_v7.build import write

PROTOCOL='continuous-model-controlled-assembly/1'
SYSTEM=SYSTEM+''' You control this ONE continuous episode from its starting state until you choose finish or exhaust the budget. Choose every operation yourself; the environment supplies no next-step action or recovery plan. An inspection does not reset the episode. You can request an earlier observed state with {"type":"inspect_history","step":0}; step is the number of environment decisions already executed in that observation. Earlier images are historical, never the actual current state. Your reasoning and action/feedback history continue across all decisions. No explicit error-detection answer is required. Decide yourself whether to continue building, inspect, undo earlier work, repair, or finish.'''
PRIVATE_FIELDS={'referenceActions','oraclePlan','referenceIncident','referenceEvents','recoveryWitness',
    'buildGuide','nextUnexecutedGuideAction','events','appliedEvents','family','score','initial','goal'}


def decode(reply):
    """Parse a single response; never replace malformed output with a GT move."""
    if isinstance(reply,str):
        try:return decode(json.loads(reply))
        except (ValueError,TypeError):return {'type':'invalid'}
    if isinstance(reply,dict) and 'choices' in reply:
        try:return decode(reply['choices'][0]['message']['content'])
        except (KeyError,TypeError,IndexError):return {'type':'invalid'}
    return reply if isinstance(reply,dict) else {'type':'invalid'}


def image_blocks(observation,label='CURRENT OBSERVATION'):
    blocks=[dict(type='text',text=label+'\n'+json.dumps(
        {k:v for k,v in observation.items() if k!='images'},ensure_ascii=False))]
    for asset in observation['images']:
        data=Path(asset['file']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==asset['sha256']
        blocks.append(dict(type='text',text=json.dumps({k:v for k,v in asset.items() if k not in ('file','sha256')},ensure_ascii=False)))
        blocks.append(dict(type='image_url',image_url=dict(url='data:image/png;base64,'+base64.b64encode(data).decode(),detail='high')))
    return blocks


class AutonomousRun:
    def __init__(self,session,decide,max_decisions=None,allow_module=False):
        self.session,self.decide=session,decide
        if session.row['mode']!='dynamic':raise ValueError('Select a dynamic episode.')
        self.whole=session.row['evaluationMetadata']['track']=='whole-object-dynamic'
        if not self.whole and not allow_module:raise ValueError('This task controls a finishing module; use --allow-module and report it separately.')
        if self.whole and (any(session.initial.values()) or session.ep.runtime.cert['fixed']):
            raise ValueError('Whole-object takeover requires an empty start and movable object parts; the environment baseplate is exempt.')
        if session.records:raise ValueError('Autonomous takeover begins at the task start, without a scripted prefix.')
        self.cap=max_decisions if max_decisions is not None else session.cap
        if type(self.cap) is not int or not 0<self.cap<=session.cap:raise ValueError('Invalid controller budget.')
        self.history=[];self.archive={};self.steps=[];self.query=None
        self.output=session.directory/'autonomous'
        self.output.mkdir(parents=True,exist_ok=True)

    def request(self):
        observation=self.session.observe()
        assert not PRIVATE_FIELDS.intersection(observation),'Private evaluator state in model input'
        step=len(self.session.records);self.archive.setdefault(step,deepcopy(observation))
        public=deepcopy(observation)
        public['baseInputVersion']=public['inputVersion']
        public['inputVersion']+='|'+PROTOCOL
        public['continuousEpisode']=dict(protocol=PROTOCOL,environmentStep=step,
            controllerDecision=len(self.steps)+1,controllerBudget=self.cap,
            recordedSteps=sorted(self.archive),
            historyRequest=dict(type='inspect_history',step=0),
            fullObjectControl=self.whole,episodeResetSinceStart=False)
        blocks=image_blocks(public)
        if self.query:
            public['historyFeedback']=deepcopy(self.query)
            blocks[0]['text']+='\nHISTORY LOOKUP: '+json.dumps(self.query,ensure_ascii=False)
            if self.query['code']=='HISTORY_AVAILABLE':
                blocks+=image_blocks(self.archive[self.query['step']],f'HISTORICAL STEP {self.query["step"]} - NOT CURRENT STATE')
        payload=dict(messages=[dict(role='system',content=SYSTEM),*deepcopy(self.history),dict(role='user',content=blocks)])
        return payload,public

    def run(self):
        while not self.session.done and len(self.steps)<self.cap:
            try:payload,public=self.request();sha=digest(payload)
            except Exception as exc:
                self.session.terminal='harness_error'
                self.steps.append(dict(index=len(self.steps)+1,harnessError=type(exc).__name__))
                break
            write(self.output/f'observation-{len(self.steps)+1:04}.json',public)
            try:reply=self.decide(payload)
            except Exception as exc:
                self.session.terminal='service_error'
                self.steps.append(dict(index=len(self.steps)+1,requestContextSha256=sha,transportError=type(exc).__name__))
                break
            action=decode(reply);before=deepcopy(self.session.ep.state)
            if action.get('type')=='inspect_history':
                number=action.get('step')
                valid=set(action)=={'type','step'} and type(number) is int and number in self.archive
                self.query=dict(code='HISTORY_AVAILABLE' if valid else 'UNKNOWN_HISTORY_STEP',step=number if type(number) is int else None)
                feedback=deepcopy(self.query)
                assert self.session.ep.state==before
            else:
                self.query=None
                feedback=self.session.submit(action,parse_error=action.get('type')=='invalid',
                    request_evidence=dict(requestContextSha256=sha))
            # Prior pictures remain in the archive and can be queried. Keep
            # text/action context, then send fresh pictures each decision.
            texts=[b for b in payload['messages'][-1]['content'] if b['type']=='text']
            self.history.extend([dict(role='user',content=texts),
                dict(role='assistant',content=reply if isinstance(reply,str) else json.dumps(reply,ensure_ascii=False)),
                dict(role='user',content=json.dumps(dict(toolFeedback=feedback),ensure_ascii=False))])
            self.steps.append(dict(index=len(self.steps)+1,requestContextSha256=sha,
                environmentStep=len(self.session.records),action=deepcopy(action),feedback=deepcopy(feedback)))
            self.save()
        if not self.session.done:self.session.terminal='model_budget_exhausted'
        self.session.save();self.save()
        return self.result()

    def result(self):
        normalized=self.session.result()
        normalized['baseInputVersion']=normalized['inputVersion'];normalized['inputVersion']+='|'+PROTOCOL
        normalized['controllerProtocol']=PROTOCOL
        normalized['controllerMetrics']=dict(decisions=len(self.steps),budget=self.cap,
            historyQueries=sum(s.get('action',{}).get('type')=='inspect_history' for s in self.steps),
            eventWindowDecisionUnit='environment decisions; archive lookups recorded separately')
        return dict(protocol=PROTOCOL,normalizedResult=normalized,
            controllerDecisions=len(self.steps),controllerBudget=self.cap,
            historyQueries=sum(s.get('action',{}).get('type')=='inspect_history' for s in self.steps),
            fullObjectControl=self.whole,scriptedPrefixActions=0,automaticRepairActions=0,
            stageResets=0,allAssemblyDecisionsFromPolicy=True,
            requestContextScope='Exact request assembled for the policy transport; provider forwarding must be audited separately.',
            observationArchiveSteps=sorted(self.archive))

    def save(self):
        write(self.output/'trace.private.json',dict(result=self.result(),steps=self.steps,
            publicObservationFiles=[p.name for p in sorted(self.output.glob('observation-*.json'))]))


def command_policy(command,timeout):
    def decide(payload):
        result=subprocess.run(command,input=json.dumps(payload,ensure_ascii=False),capture_output=True,text=True,timeout=timeout)
        if result.returncode:raise RuntimeError('Policy transport failed')
        return result.stdout.strip()
    return decide


def main():
    import sys
    if '--legacy-full-context' not in sys.argv:
        from reliability.run import main as paged_main
        return paged_main()
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--legacy-full-context',action='store_true')
    p.add_argument('--id',required=True);p.add_argument('--actor',required=True)
    p.add_argument('--output',type=Path);p.add_argument('--max-decisions',type=int)
    p.add_argument('--allow-module',action='store_true');p.add_argument('--timeout',type=float,default=120)
    p.add_argument('--policy-command',nargs=argparse.REMAINDER,required=True)
    a=p.parse_args()
    if not a.policy_command:raise SystemExit('Provide the model transport command after --policy-command.')
    s=Session.open(a.id,a.output or OUT/'autonomous-runs'/uuid.uuid4().hex,actor=a.actor)
    result=AutonomousRun(s,command_policy(a.policy_command,a.timeout),a.max_decisions,a.allow_module).run()
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
