"""Version-six episode: strict actions, bounded live certification and complete accounting."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from functools import lru_cache
import json,sys,math
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'eval')]
from dynamic_v5.episode import DynamicEpisode as PreviousEpisode
from dynamic_v6 import VERSION
from dynamic_v6.build import event_candidates,replay,perform
from static_v4.certify import digest
from static_v4.metrics import residual
BANK=HERE.parents[2]/'deliverables/brickplan-dynamic-v6'

@lru_cache(maxsize=1)
def bank_cases():return {c['id']:c for c in json.loads((BANK/'cases.private.json').read_text())['cases']}
@lru_cache(maxsize=128)
def model_cert(mid):return json.loads((BANK/'models'/mid/'qualification.json').read_text())
def load_case(case_id):
    case=deepcopy(bank_cases()[case_id]);return deepcopy(model_cert(case['modelId'])),case

def continuation(rt,state,limit=2000):
    failed=set();visited=0
    def solve(s,remaining):
        nonlocal visited
        if not remaining:return []
        token=tuple(remaining)
        if token in failed:return None
        visited+=1
        if visited>limit:return None
        for a in remaining:
            move=dict(type='attach',partId=a,candidate=rt.goal[a]);after=perform(rt,s,move)
            if after is None:continue
            tail=solve(after,[b for b in remaining if b!=a])
            if tail is not None:return [move]+tail
        failed.add(token);return None
    return solve(state,[a for a,k in rt.goal.items() if k and not state.get(a)])

class DynamicEpisode(PreviousEpisode):
    def __init__(self,cert,case,seed=41):
        assert case['protocol']==VERSION
        self.input_certificate=deepcopy(cert)
        super().__init__(cert,{**case,'protocol':'brickplan-dynamic/5'},seed)
        self.case['protocol']=VERSION
        self.chain=digest(dict(caseId=case['id'],source=cert['contentSha256'],seed=seed,initial=self.state,protocol=VERSION))
        self.trigger_attempts=[];self.judgments=[];self.previous_state=None
        self.decision_budget=case.get('decisionBudget',max(40,6*case['targetParts']+20))
        self.budget_exhausted=False

    def observe(self):
        obs=super().observe();obs['protocol']=VERSION
        for handle in obs['actionHandles']:handle['candidates']=sorted(handle['candidates'])
        obs.update(decisionsUsed=len(self.records),decisionBudget=self.decision_budget,
                   visualTiming=dict(firstDecision=not self.records,left='Immediately before your previous action; no prior scene at the first decision.',right='Actual scene now, after the previous action and any external change.',target='Fixed final target; identical camera and scale.'),
                   previousAction=self.history[-1] if self.history else None)
        obs['responseSchema']['unexpectedChange']='boolean: did something change beyond the effect of your own previous action? false at the first decision.'
        obs['responseSchema']['note']='optional; no explanation is required'
        obs['note']='One attach or detach changes one movable part. The white baseplate is fixed. Inspect is always allowed. Before and current are two times of the same scene; do not add their pieces together. All catalog pages and all inventory pages are available. Inspect does not change the build. Finish ends this attempt, including an incomplete submission.'
        return obs

    def _event(self):
        event=self.case.get('privateEvent')
        if not event or self.event or self.manipulations<self.case['trigger']:return
        before=dict(self.state)
        def correct_placement(a,k):
            target=self.runtime.goal.get(a)
            return bool(k and target and self.runtime.signature({a:k})==self.runtime.signature({a:target}))
        correct=sum(correct_placement(a,k) for a,k in before.items())
        if correct<self.case['trigger']:return
        selected=event;provenance='precertified'
        if digest(before)!=event['beforeSha256']:
            if any(k and not correct_placement(a,k) for a,k in before.items()):
                self.trigger_attempts.append(dict(at=len(self.records),reason='non-goal-prefix'));return
            tail=continuation(self.runtime,before)
            if tail is None:
                self.trigger_attempts.append(dict(at=len(self.records),reason='continuation-not-certified'));return
            options=event_candidates(self.runtime,before,[a['partId'] for a in tail])
            if self.case['kind']=='compound_fault':
                simple=[]
                for kind,change,restore in options:
                    if kind not in ('wrong_color','shifted_piece','extra_layer','removed_piece'):continue
                    after=replay(self.runtime,before,change)
                    if after is not None and replay(self.runtime,after,restore)==before:
                        simple.append((kind,change,restore))
                    if len(simple)>=40:break
                compound=[]
                for i,(ka,ca,ra) in enumerate(simple):
                    for kb,cb,rb in simple[i+1:]:
                        if ka==kb or {a['partId'] for a in ca}&{a['partId'] for a in cb}:continue
                        compound.append(('compound_fault',ca+cb,rb+ra))
                options=compound
            selected=None
            for kind,change,restore in options:
                if kind!=self.case['kind']:continue
                after=replay(self.runtime,before,change)
                if after is None or self.runtime.signature(after)==self.runtime.signature(before):continue
                if replay(self.runtime,after,restore)!=before:continue
                final=replay(self.runtime,after,restore+tail)
                if final is None or not self.runtime.complete(final):continue
                selected=dict(kind=kind,transaction=change,recoveryWitness=restore+tail,beforeSha256=digest(before),afterSha256=digest(after));break
            if selected is None:
                self.trigger_attempts.append(dict(at=len(self.records),reason='no-certified-live-event'));return
            provenance='adaptive-certified'
        shadow=replay(self.runtime,before,selected['transaction'])
        assert shadow is not None and digest(shadow)==selected['afterSha256']
        self.state=shadow
        self.event=dict(kind=selected['kind'],atManipulation=self.manipulations,beforeSha256=digest(before),afterSha256=digest(shadow),transaction=deepcopy(selected['transaction']),recoveryWitness=deepcopy(selected['recoveryWitness']),provenance=provenance,atRecord=len(self.records),beforeResidual=residual(self.runtime,before),afterResidual=residual(self.runtime,shadow))

    def valid_action_shape(self,action):
        if not isinstance(action,dict):return False
        kind=action.get('type')
        fields={'finish':{'type'},'detach':{'type','partId'},'attach':{'type','partId','candidate','catalogPage','catalogPoint'},'inspect':{'type','partId','candidate','point','crop','view','azimuth','elevation'}}
        if not isinstance(kind,str) or kind not in fields or not set(action)<=fields[kind]:return False
        if kind in ('attach','detach') and not isinstance(action.get('partId'),str):return False
        if kind=='attach':
            direct='candidate' in action;click='catalogPage' in action or 'catalogPoint' in action
            if direct==click:return False
            if direct and not isinstance(action['candidate'],str):return False
        return True

    def step(self,public):
        if self.finished:raise ValueError('Episode already ended')
        if len(self.records)>=self.decision_budget:raise ValueError('Decision budget exhausted')
        self.previous_state=self.assignments()
        malformed=not self.valid_action_shape(public)
        submitted=deepcopy(public)
        prior_chain=self.chain
        actor=self.reverse.get(public.get('partId')) if isinstance(public,dict) and isinstance(public.get('partId'),str) else None
        removed_correct=bool(isinstance(public,dict) and public.get('type')=='detach' and actor and self.state.get(actor) and self.runtime.goal.get(actor) and self.runtime.signature({actor:self.state[actor]})==self.runtime.signature({actor:self.runtime.goal[actor]}))
        feedback=super().step({'type':'invalid'} if malformed else public)
        # Preserve malformed responses outside the state hash chain; the
        # normalized INVALID_ACTION record remains fully replayable.
        self.records[-1]['submittedAction']=submitted
        self.records[-1]['detachedCorrectPiece']=removed_correct and feedback['code']=='OK'
        record={k:v for k,v in self.records[-1].items() if k!='chainSha256'}
        self.chain=digest(dict(previous=prior_chain,record=record))
        self.records[-1]['chainSha256']=self.chain
        if len(self.records)>=self.decision_budget and not self.finished:
            self.budget_exhausted=True;self.finished=True
        return feedback

    def submit(self,payload):
        if not isinstance(payload,dict) or 'action' not in payload or not set(payload)<={'action','unexpectedChange','note'}:
            payload={'action':{'type':'invalid'}}
        judgment=payload.get('unexpectedChange')
        self.judgments.append(judgment if type(judgment) is bool else None)
        return self.step(payload['action'])

    def score(self):
        out=super().score();event_index=self.event['atRecord']+1 if self.event else None
        invalid=[r for r in self.records if r['feedback']['code']=='INVALID_ACTION']
        post=[r for r in self.records if self.event and r['index']>self.event['atRecord']]
        prior_residual=self.event['afterResidual'] if self.event else None
        first_reducing=None
        for i,r in enumerate(post,1):
            if first_reducing is None and r['feedback']['code']=='OK' and r['afterResidual']<prior_residual:first_reducing=i
            prior_residual=r['afterResidual']
        out.update(protocol=VERSION,decisions=len(self.records),decisionBudget=self.decision_budget,budgetExhausted=self.budget_exhausted,
                   invalidOutputs=len(invalid),allRejectedActions=sum(r['feedback']['code'] not in ('OK','OBSERVED','SUCCESS','INCOMPLETE') for r in self.records),
                   reportedAtEvent=self.judgments[event_index] if event_index is not None and event_index<len(self.judgments) else None,
                   missingChangeJudgments=sum(v is None for v in self.judgments),
                   preEventFalseAlarms=sum(v is True for i,v in enumerate(self.judgments) if event_index is None or i<event_index),
                   triggerFailureReason=self.trigger_attempts[-1]['reason'] if not self.event and self.trigger_attempts else None,
                   firstResidualReducingMoveDecision=first_reducing,
                   postEventCorrectPieceDetaches=sum(r['detachedCorrectPiece'] for r in post),
                   detectionClaimEligible=False)
        return out

    def export(self):
        out=super().export();out.update(protocol=VERSION,changeJudgments=self.judgments,triggerAttempts=self.trigger_attempts)
        if hasattr(self,'branch_origin'):out['branchOrigin']=self.branch_origin
        return out

def branch_before_action(prefix,intervention_case,action):
    """The policy runs once before the trigger; both branches receive that exact prefix."""
    if prefix.case['kind']!='none' or prefix.case['pairedGroup']!=intervention_case['pairedGroup']:
        raise ValueError('Need the paired control prefix')
    def clone():
        result=DynamicEpisode(prefix.input_certificate,prefix.case,prefix.seed)
        for record in prefix.records:result.step(deepcopy(record.get('submittedAction',record['action'])))
        result.judgments=deepcopy(prefix.judgments)
        assert result.state==prefix.state and result.history==prefix.history
        return result
    control=clone();changed=clone()
    changed.case={**changed.case,**deepcopy(intervention_case)}
    changed.branch_origin=dict(controlCaseId=prefix.case['id'],sharedPrefixHash=prefix.chain,sharedDecisions=len(prefix.records))
    control.step(deepcopy(action));changed.step(deepcopy(action))
    if not changed.event:raise ValueError('This action did not reach a certified trigger; keep the prefix running')
    assert control.expected_after_last_action==changed.expected_after_last_action
    assert control.alias==changed.alias and control.pose_alias==changed.pose_alias
    assert control.history==changed.history
    assert control.event is None
    return control,changed
