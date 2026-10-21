"""One uninterrupted actor loop; hidden event commits after a successful move."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import math
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent/'eval'))
from baseplate import PlateAssembly, PROTOCOL
from static_v4.certify import digest
from static_v4.metrics import residual
from dynamic_v5 import VERSION

BANK = ROOT/'deliverables/brickplan-dynamic-v5'

def load_case(case_id):
    rows = json.loads((BANK/'cases.private.json').read_text())['cases']
    case = next(c for c in rows if c['id'] == case_id)
    cert = json.loads((BANK/'models'/case['modelId']/'qualification.json').read_text())
    return cert, case

class DynamicEpisode:
    def __init__(self, cert, case, seed=41):
        if case['protocol'] != VERSION or case['manipulationProtocol'] != PROTOCOL:
            raise ValueError('Wrong dynamic execution protocol')
        self.case, self.seed = case, seed
        self.runtime = PlateAssembly(cert)
        self.cert = self.runtime.cert
        self.actors = self.runtime.actors
        self.state = {a:'' for a in self.actors}
        self.case_view = dict(goal=self.runtime.goal, choices={a: sorted(k for k,r in self.cert['candidates'].items() if r['actor']==a) for a in self.actors})
        rng = random.Random(seed)
        actors = list(self.actors); rng.shuffle(actors)
        keys = sorted(self.cert['candidates']); rng.shuffle(keys)
        self.alias = {a:f'A{i+1:02}' for i,a in enumerate(actors)}
        self.reverse = {v:k for k,v in self.alias.items()}
        self.pose_alias = {k:f'C{i+1:03}' for i,k in enumerate(keys)}
        self.pose_reverse = {v:k for k,v in self.pose_alias.items()}
        self.case_for_vision = dict(goal=self.runtime.goal,choices=self.case_view['choices'])
        self.case = {**case,'goal':self.runtime.goal,'choices':self.case_view['choices']}
        self.history=[]; self.records=[]; self.event=None; self.manipulations=0
        self.inspections=0; self.finished=False; self.success=False
        self.expected_after_last_action=None
        self.chain=digest(dict(caseId=case['id'],source=cert['contentSha256'],seed=seed,initial=self.state))

    def assignments(self):
        return dict(self.state)

    def pose(self, key):
        return self.pose_alias.get(key)

    def internal_action(self, action):
        result=dict(action)
        if 'partId' in result: result['partId']=self.reverse.get(result['partId'],'UNKNOWN')
        if 'candidate' in result: result['candidate']=self.pose_reverse.get(result['candidate'],'UNKNOWN')
        return result

    def catalog_click_candidate(self, public):
        """Resolve a click on a uniformly laid out candidate card, not a goal pose."""
        part_id = public.get('partId')
        actor = self.reverse.get(part_id) if isinstance(part_id,str) else None
        page, point = public.get('catalogPage'), public.get('catalogPoint')
        if actor is None or type(page) is not int or page < 1:
            return None
        if (not isinstance(point, list) or len(point) != 2 or
            not all(type(x) in (int, float) and math.isfinite(x) and 0 <= x < 1 for x in point)):
            return None
        keys = sorted(self.case['choices'][actor], key=self.pose)
        group = keys[(page-1)*12:page*12]
        if not group:
            return None
        rows = math.ceil(len(group)/4)
        col, row = int(point[0]*4), int(point[1]*rows)
        index = row*4+col
        return group[index] if index < len(group) else None

    def observe(self):
        handles=[dict(id=self.alias[a],candidates=[self.pose(k) for k in self.case['choices'][a]])
                 for a in sorted(self.actors,key=lambda x:self.alias[x])]
        return dict(task='Build the target from an empty white baseplate. Observe the latest current image after every action. Repair any discrepancy and finish.',
                    mode='dynamic',track='visual',protocol=VERSION,manipulationProtocol=PROTOCOL,
                    actionHandles=handles,manipulationsUsed=self.manipulations,inspectionsUsed=self.inspections,
                    recentFeedback=self.history[-8:],availableViews=['isometric','front','rear','left','right','top','bottom'],
                    maxActionsPerResponse=1,
                    responseSchema={'action':{'type':'attach|detach|inspect|finish','partId':'Axx if needed','candidate':'Cxxx if attaching, or catalogPage plus catalogPoint',
                                              'catalogPage':'optional 1-based candidate-catalog page for attach',
                                              'catalogPoint':'optional normalized [x,y] click within candidate-catalog image for attach',
                                              'view':'optional view for inspect','point':'optional [x,y] for inspecting a visible piece'}},
                    note='A move is followed by a fresh observation. Environment changes, if any, are visible only through the next ordinary observation. Candidate IDs are placement handles, not correct-answer labels.')

    def _event(self):
        event=self.case.get('privateEvent')
        if not event or self.event or self.manipulations < self.case['trigger']:
            return
        before=dict(self.state)
        correct=sum(bool(key) and key==self.runtime.goal[actor] for actor,key in before.items())
        if correct < self.case['trigger']:
            return
        selected=event
        provenance='precertified'
        if digest(before)!=event['beforeSha256']:
            # A free agent may build in another valid order. Select an event
            # of the pre-registered category only if the live state has a
            # directly replayed route to the same target.
            from dynamic_v5.build import candidates, replay
            if any(key and key!=self.runtime.goal[actor] for actor,key in before.items()):
                return
            def suffix(state, remaining):
                if not remaining:return []
                for actor in remaining:
                    action=dict(type='attach',partId=actor,candidate=self.runtime.goal[actor])
                    after,feedback=self.runtime.check(state,actor,'attach',candidate=action['candidate'])
                    if feedback['code']!='OK':continue
                    tail=suffix(after,[a for a in remaining if a!=actor])
                    if tail is not None:return [action]+tail
                return None
            remaining=[a for a,k in self.runtime.goal.items() if k and not before[a]]
            continuation=suffix(before,remaining)
            if continuation is None:return
            options=candidates(self.runtime,before,[a['partId'] for a in continuation])
            selected=None
            for kind,change,restore in options:
                if kind!=self.case['kind']:continue
                after=replay(self.runtime,before,change)
                if after is None or replay(self.runtime,after,restore)!=before:continue
                final=replay(self.runtime,before,continuation)
                if final is None or not self.runtime.complete(final):continue
                selected=dict(kind=kind,transaction=change,recoveryWitness=restore+continuation,
                              beforeSha256=digest(before),afterSha256=digest(after))
                break
            if selected is None:return
            provenance='adaptive-certified'
        shadow=dict(before)
        for action in selected['transaction']:
            shadow, result=self.runtime.check(shadow,action['partId'],action['type'],candidate=action.get('candidate'))
            if result['code']!='OK':
                raise AssertionError((self.case['id'],'event failed',action,result))
        if digest(shadow)!=selected['afterSha256']:
            raise AssertionError((self.case['id'],'event prefix drift'))
        self.state=shadow
        self.event=dict(kind=selected['kind'],atManipulation=self.manipulations,
                        beforeSha256=digest(before),afterSha256=digest(shadow),transaction=deepcopy(selected['transaction']),
                        recoveryWitness=deepcopy(selected['recoveryWitness']),provenance=provenance,
                        atRecord=len(self.records),beforeResidual=residual(self.runtime,before),
                        afterResidual=residual(self.runtime,shadow))

    def step(self, public):
        if self.finished: raise ValueError('Episode already ended')
        before=dict(self.state)
        if not isinstance(public,dict):public={'type':'invalid'}
        self.expected_after_last_action=dict(before)
        kind=public.get('type');part_id=public.get('partId')
        actor=self.reverse.get(part_id) if isinstance(part_id,str) else None
        if kind=='finish':
            self.finished=True;self.success=self.runtime.complete(self.state)
            feedback={'code':'SUCCESS' if self.success else 'INCOMPLETE'}
        elif kind=='inspect':
            from render import VIEWS
            allowed={'type','view','partId','candidate','point','crop','azimuth','elevation'}
            valid=set(public)<=allowed
            valid=valid and not ('partId' in public and ('candidate' in public or 'point' in public))
            valid=valid and not ('candidate' in public and 'point' in public)
            valid=valid and ('partId' not in public or isinstance(public['partId'],str) and public['partId'] in self.reverse)
            valid=valid and ('candidate' not in public or isinstance(public['candidate'],str) and public['candidate'] in self.pose_reverse)
            valid=valid and ('view' not in public or isinstance(public['view'],str) and public['view'] in VIEWS)
            if 'point' in public:
                point=public['point'];valid=valid and isinstance(point,list) and len(point)==2 and all(type(x) in (int,float) and math.isfinite(x) and 0<=x<=1 for x in point)
            if 'crop' in public:
                crop=public['crop'];valid=valid and isinstance(crop,list) and len(crop)==4 and all(type(x) in (int,float) and math.isfinite(x) and 0<=x<=1 for x in crop)
                valid=valid and crop[2]-crop[0]>=.025 and crop[3]-crop[1]>=.025
            if 'azimuth' in public or 'elevation' in public:
                valid=valid and all(type(public.get(x)) in (int,float) and math.isfinite(public[x]) for x in ('azimuth','elevation'))
                valid=valid and -90<=public.get('elevation',999)<=90
            if not valid:
                feedback={'code':'INVALID_ACTION'}
            elif 'point' in public:
                from vision import VisionRenderer
                renderer=getattr(self,'vision_renderer',None) or VisionRenderer(self.cert)
                actor=renderer.pick(self,public)
                if actor is None:feedback={'code':'NO_VISIBLE_MOVABLE_PIECE'}
                else:
                    self.inspections+=1;feedback={'code':'OBSERVED','partId':self.alias[actor]}
            else:
                self.inspections+=1;feedback={'code':'OBSERVED'}
        elif kind in ('attach','detach'):
            click_requested='catalogPage' in public or 'catalogPoint' in public
            malformed=click_requested and ('candidate' in public or kind!='attach' or
                                           'catalogPage' not in public or 'catalogPoint' not in public)
            candidate=(self.catalog_click_candidate(public) if click_requested
                       else self.pose_reverse.get(public.get('candidate'))) if kind=='attach' else None
            if malformed or (click_requested and candidate is None):
                result={'code':'INVALID_ACTION','blockers':[]}
            else:
                try:self.state,result=self.runtime.check(self.state,actor,kind,candidate=candidate)
                except (KeyError,TypeError,ValueError):result={'code':'INVALID_ACTION','blockers':[]}
            feedback={'code':result['code']}
            if result['code']!='OK':
                feedback['blockers']=[self.alias.get(a,a) for a in result.get('blockers',[]) if a!='@baseplate']
            else:
                self.manipulations+=1
                self.expected_after_last_action=dict(self.state)
                self._event()
        else:feedback={'code':'INVALID_ACTION'}
        # The public feedback never names the event, actor, location or class.
        entry=dict(index=len(self.records),action=deepcopy(public),feedback=feedback,
                   beforeSha256=digest(before),afterSha256=digest(self.state),eventOccurred=bool(self.event and self.event['atManipulation']==self.manipulations and not any(r.get('eventOccurred') for r in self.records)))
        entry['afterResidual']=residual(self.runtime,self.state)
        entry['chainSha256']=digest(dict(previous=self.chain,record=entry));self.chain=entry['chainSha256']
        self.records.append(entry)
        self.history.append(dict(action=public,feedback=feedback))
        return feedback

    def score(self):
        valid=[r for r in self.records if r['feedback']['code']=='OK']
        invalid=[r for r in self.records if r['action'].get('type') in ('attach','detach') and r['feedback']['code']!='OK']
        event_at=self.event['atManipulation'] if self.event else None
        post=[r for r in self.records if self.event and r['index']>self.event['atRecord']]
        first_fix=next((i for i,r in enumerate(post,1) if r['feedback']['code']=='OK' and r['action'].get('type') in ('attach','detach')),None)
        post_manip=[r for r in post if r['action'].get('type') in ('attach','detach')]
        target_detaches=sum(r['action'].get('type')=='detach' and r['feedback']['code']=='OK'
                             and bool(self.runtime.goal.get(self.reverse.get(r['action'].get('partId')))) and
                             r['beforeSha256']!=r['afterSha256'] for r in post)
        return dict(caseId=self.case['id'],success=self.success,finalEquivalent=self.runtime.complete(self.state),
                    finished=self.finished,eventScheduled=self.case['kind']!='none',eventTriggered=bool(self.event),
                    eventAtManipulation=event_at,legalMoves=len(valid),invalidMoves=len(invalid),
                    invalidByReason=dict(Counter(r['feedback']['code'] for r in invalid)),
                    inspections=self.inspections,postEventDecisions=len(post),firstPostEventMoveDecision=first_fix,
                    postEventLegalMoves=sum(r['feedback']['code']=='OK' for r in post_manip),
                    postEventInvalidMoves=sum(r['feedback']['code']!='OK' for r in post_manip),
                    postEventInspections=sum(r['action'].get('type')=='inspect' for r in post),
                    postEventTargetActorDetaches=target_detaches,
                    eventResidual=self.event['afterResidual'] if self.event else None,
                    finalResidual=residual(self.runtime,self.state),chainSha256=self.chain)

    def export(self):
        return dict(caseId=self.case['id'],protocol=VERSION,sourceCertificateSha256=self.cert['contentSha256'],
                    seed=self.seed,finalState=self.state,event=self.event,records=self.records,score=self.score())
