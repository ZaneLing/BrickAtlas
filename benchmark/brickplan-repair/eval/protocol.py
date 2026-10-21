"""Leakage-separated static repair and from-empty dynamic episodes."""
from copy import deepcopy
import hashlib,json,math,random,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from static_bench import OUT,Domain,exact_plan,part_name


def load(model):
    p=OUT/'models'/model
    return json.loads((p/'qualification.json').read_text()),json.loads((p/'cases.json').read_text())


def from_empty_certificate(source):
    key=source['contentSha256']
    cache=HERE.parents[2]/'deliverables/brickplan-dynamic-v1/models'/key/'qualification.json'
    if cache.exists():return json.loads(cache.read_text())
    from library import Qualifier
    cert=deepcopy(source);fixed=cert['fixed'];mapping={k:k+':base' for k in fixed}
    for row in cert['candidates'].values():
        for field in ('support','pathBlocked','endpointBlocked'):
            row[field]=[mapping.get(k,k) for k in row[field]]
    for actor,part in fixed.items():
        cert['candidates'][mapping[actor]]={'actor':actor,'kind':'goal','label':'source piece','part':part}
    q=Qualifier()
    for actor,part in fixed.items():
        key2=mapping[actor]
        cert['candidates'][key2]=q.candidate(key2,part,{},cert['candidates'],cert['extractionLengthLDU'],'source piece','goal')
    cert['fixed']={'WORLD':{'virtual':True}}
    actors=sorted({r['actor'] for r in cert['candidates'].values()})
    goal={a:'' for a in actors};goal.update({r['actor']:k for k,r in cert['candidates'].items() if r['kind']=='goal'})
    case={'id':'construction-gate','actors':actors,'goal':goal,'choices':{a:[k for k,r in cert['candidates'].items() if r['actor']==a] for a in actors},'rackCapacity':len(actors)}
    # A static repair fixture can lie inside a structure. Choose a buildable
    # ground fixture explicitly; no real piece is preinstalled.
    for anchor in sorted(k for k in goal.values() if k):
        cert['candidates'][anchor]['support'].append('WORLD')
        domain=Domain(cert,{});state=domain.pack(case,goal);reverse=[]
        while any(state):
            moved=False
            for a,k in domain.unpack(case,state).items():
                if not k:continue
                after,check=domain.transition(case,state,{'type':'detach','partId':a})
                if check['code']=='OK':
                    reverse.append({'type':'attach','partId':a,'candidate':k});state=after;moved=True;break
            if not moved:break
        if not any(state):
            cert['constructionWitness']=list(reversed(reverse));cert['groundAnchor']=anchor
            cert['dynamicPrepared']=True;cert['sourceStaticCertificate']=source['contentSha256']
            cache.parent.mkdir(parents=True,exist_ok=True);cache.write_text(json.dumps(cert,ensure_ascii=False)+'\n')
            return cert
        cert['candidates'][anchor]['support'].remove('WORLD')
    raise ValueError('This static substructure has no qualified from-empty construction witness')


class Episode:
    def __init__(self,source,case,mode='static',event='none',seed=41,action_mask=False,protocol_version='v1'):
        self.cert=from_empty_certificate(source) if mode=='dynamic' else deepcopy(source)
        self.mode,self.event_kind,self.seed=mode,event,seed
        self.action_mask=action_mask
        self.protocol_version=protocol_version
        if protocol_version=='v3' and (mode!='static' or action_mask):
            raise ValueError('V3 currently accepts unassisted static visual episodes only')
        self.domain=Domain(self.cert,{})
        self.manipulator=None
        if protocol_version=='v3':
            from assembly import Assembly
            self.manipulator=Assembly(self.cert)
        self.actors=sorted({r['actor'] for r in self.cert['candidates'].values()})
        goals={a:'' for a in self.actors}
        goals.update({r['actor']:k for k,r in self.cert['candidates'].items() if r['kind']=='goal'})
        initial={a:'' for a in self.actors} if mode=='dynamic' else {**goals,**case['initial']}
        self.case={'id':case['id']+'-'+mode+'-'+event,'actors':self.actors,'initial':initial,'goal':goals,
                   'choices':{a:[k for k,r in self.cert['candidates'].items() if r['actor']==a] for a in self.actors},
                   'rackCapacity':len(self.actors)}
        self.state=self.domain.pack(self.case,initial)
        assert self.domain.valid(self.case,self.state)=='OK'
        self.target=self.domain.pack(self.case,goals)
        self.initial_errors={a for a in self.actors if initial[a]!=goals[a]}
        self.events=[];self.history=[];self.finished=False;self.success=False;self.manipulations=0;self.inspections=0;self.invalid=0
        self.trigger=max(2,sum(bool(v) for v in goals.values())//2)
        # Public IDs are permuted and carry no goal/fault/category suffixes.
        rng=random.Random(seed)
        actors=self.actors.copy();rng.shuffle(actors)
        self.alias={a:f'A{i+1:02}' for i,a in enumerate(actors)}
        for i,k in enumerate(sorted(self.cert['fixed'])):self.alias[k]=f'F{i+1:02}'
        keys=sorted(self.cert['candidates']);rng.shuffle(keys)
        self.pose_alias={k:f'C{i+1:03}' for i,k in enumerate(keys)}
        self.reverse={v:k for k,v in self.alias.items()};self.pose_reverse={v:k for k,v in self.pose_alias.items()}
        self.original_case=case

    def assignments(self):return self.domain.unpack(self.case,self.state)
    def pose(self,k):return self.pose_alias.get(k,self.alias.get(k,k)) if k else None
    def public_state(self,state):return {self.alias[a]:self.pose(k) for a,k in self.domain.unpack(self.case,state).items()}

    def catalog(self):
        result=[]
        for a in self.actors:
            rows=[(k,r) for k,r in self.cert['candidates'].items() if r['actor']==a]
            p=rows[0][1]['part']
            if self.protocol_version in ('v2','v3'):
                random.Random(str(self.seed)+':poses:'+self.alias[a]).shuffle(rows)
            result.append({'id':self.alias[a],'ldraw':p['partNumber'],'description':part_name(p['partNumber']),'color':p['colorHex'],
              'poses':[{'id':self.pose(k),'transform':[round(n,3) for row in r['part']['rawMatrix'][:3] for n in row],
                        'supportAnyOf':[self.pose(q) for q in r['support']],
                        'pathMustBeEmpty':[self.pose(q) for q in r['pathBlocked']],
                        'overlapMustBeEmpty':[self.pose(q) for q in r['endpointBlocked']]} for k,r in rows]})
        return sorted(result,key=lambda x:x['id'])

    def observe(self,track):
        if self.protocol_version=='v3':
            if track!='visual':raise ValueError('Text/symbolic evaluation is retired')
            from vision import observe
            return observe(self)
        value={'task':'Build and repair until the current assembly matches the target. All listed pieces are available.',
               'mode':self.mode,'track':track,'fixedFixtures':list(self.alias[k] for k in self.cert['fixed']),
               'catalog':self.catalog(),'manipulationsUsed':self.manipulations,'inspectionsUsed':self.inspections,
               'recentFeedback':self.history[-8:],'eventNotice':bool(self.events),
               'responseSchema':{'actions':[{'type':'attach','partId':'Axx','candidate':'Cxxx'},
                    {'type':'detach','partId':'Axx'},{'type':'inspect','view':'front'},
                    {'type':'inspect','partId':'Axx'}, {'type':'inspect','azimuth':45,'elevation':20}, {'type':'finish'}]},
               'maxActionsPerResponse':8}
        if track=='symbolic':
            value.update(current=self.public_state(self.state),target=self.public_state(self.target))
        else:
            value['imageContract']='Current and target seven-view sheets, plus uniform per-piece inspection atlas. IDs are printed only on visible surfaces. Atlas isolates EVERY registered piece in the same pose frame for current and target; it changes no assembly state. Empty cells mean absent. No fault highlights or oracle data.'
        if self.action_mask:
            legal=[]
            for actor,key in self.assignments().items():
                actions=[{'type':'detach','partId':actor}] if key else [{'type':'attach','partId':actor,'candidate':k} for k in self.case['choices'][actor]]
                for action in actions:
                    _,feedback=self.domain.transition(self.case,self.state,action)
                    if feedback['code']=='OK':
                        public={**action,'partId':self.alias[actor]}
                        if 'candidate' in public:public['candidate']=self.pose(public['candidate'])
                        legal.append(public)
            value.update(legalActions=legal,assistance='Diagnostic action mask: ALL currently legal manipulations, computed without target or oracle. Choose one action, then reobserve. This track exposes state feasibility and is scored separately.',maxActionsPerResponse=1)
        return value

    def internal_action(self,a):
        value=dict(a)
        if 'partId' in value:value['partId']=self.reverse.get(value['partId'],'UNKNOWN')
        if 'candidate' in value:value['candidate']=self.pose_reverse.get(value['candidate'],'UNKNOWN')
        return value

    def inject(self):
        if self.mode!='dynamic' or self.event_kind=='none' or self.events:return False
        current=self.assignments()
        if sum(bool(v) for v in current.values()) < self.trigger:return False
        options=[]
        for actor,key in current.items():
            if not key:continue
            row=self.cert['candidates'][key]
            if key.endswith(':base'):continue
            after,check=self.domain.transition(self.case,self.state,{'type':'detach','partId':actor})
            if check['code']!='OK':continue
            if self.event_kind=='remove':
                options.append((actor,after,[{'type':'detach','partId':actor}]))
            elif self.event_kind in ('color','pose'):
                for alt,r in self.cert['candidates'].items():
                    if self.event_kind=='color':
                        expected=r['kind']=='wrong_color' and r['part'].get('derivedFromSourceIndex')==row['part'].get('sourceIndex')
                    else:expected=r['actor']==actor and r['kind'] in ('offset','rotation')
                    if not expected or alt==key:continue
                    final,check2=self.domain.transition(self.case,after,{'type':'attach','partId':r['actor'],'candidate':alt})
                    if check2['code']=='OK' and final!=self.state:
                        options.append((actor,final,[{'type':'detach','partId':actor},{'type':'attach','partId':r['actor'],'candidate':alt}]))
        if self.event_kind=='closure':
            for actor,key in self.case['goal'].items():
                if not key or current[actor]:continue
                after,check=self.domain.transition(self.case,self.state,{'type':'attach','partId':actor,'candidate':key})
                if check['code']!='OK':continue
                blocked=[a for a,g in self.case['goal'].items() if g and not current[a] and key in self.cert['candidates'][g]['pathBlocked']]
                if blocked:options.append((actor,after,[{'type':'attach','partId':actor,'candidate':key}]))
        if not options:return False
        options.sort(key=lambda row:row[0]);chosen=random.Random(self.seed).choice(options)
        before=self.state;self.state=chosen[1]
        assert self.domain.valid(self.case,self.state)=='OK'
        self.events.append({'kind':self.event_kind,'atManipulation':self.manipulations,'before':self.domain.unpack(self.case,before),
                            'after':self.assignments(),'actions':chosen[2]})
        return True

    def step(self,public):
        if self.finished:return {'code':'TERMINATED'}
        if not isinstance(public,dict):public={'type':'invalid'}
        picked=None
        if self.protocol_version=='v3':
            from render import VIEWS
            def numbers(value, length):
                return isinstance(value,list) and len(value)==length and all(type(x) in (int,float) and math.isfinite(x) for x in value)
            kind=public.get('type')
            allowed={'detach':{'type','partId','view','point','crop','azimuth','elevation'},
                     'attach':{'type','partId','candidate'},
                     'inspect':{'type','partId','candidate','view','point','crop','azimuth','elevation'},
                     'finish':{'type'}}
            valid=isinstance(kind,str) and kind in allowed and not (set(public)-allowed[kind])
            valid=valid and (not ('point' in public and 'partId' in public))
            valid=valid and (not ('candidate' in public and kind=='inspect' and ('partId' in public or 'point' in public)))
            if 'view' in public:valid=valid and isinstance(public['view'],str) and public['view'] in VIEWS
            if 'point' in public:valid=valid and numbers(public['point'],2) and all(0<=x<=1 for x in public['point'])
            if 'crop' in public:
                rect=public['crop']
                valid=valid and numbers(rect,4) and all(0<=x<=1 for x in rect) and rect[2]-rect[0]>=.025 and rect[3]-rect[1]>=.025
            if 'azimuth' in public or 'elevation' in public:
                valid=valid and numbers([public.get('azimuth'),public.get('elevation')],2) and -90<=public['elevation']<=90
            if 'candidate' in public:valid=valid and isinstance(public['candidate'],str) and public['candidate'] in self.pose_reverse
            if 'partId' in public:valid=valid and isinstance(public['partId'],str) and self.reverse.get(public['partId']) in self.actors
            if not valid:
                self.invalid+=1;feedback={'code':'INVALID_ACTION'}
                self.history.append({'action':public,'feedback':feedback});return feedback
            if 'point' in public:
                from vision import VisionRenderer
                if not hasattr(self,'vision_renderer'):self.vision_renderer=VisionRenderer(self.cert)
                actor=self.vision_renderer.pick(self,public)
                if actor is None:
                    feedback={'code':'NO_VISIBLE_MOVABLE_PIECE'}
                    self.invalid+=1;self.history.append({'action':public,'feedback':feedback});return feedback
                picked=self.alias[actor]
                public={**public,'partId':picked};public.pop('point')
        if self.protocol_version in ('v2','v3'):
            kind=public.get('type')
            invalid=(not isinstance(kind,str) or kind not in ('attach','detach','inspect','finish')
                     or ('partId' in public and not isinstance(public['partId'],str))
                     or ('candidate' in public and not isinstance(public['candidate'],str))
                     or ('view' in public and not isinstance(public['view'],str))
                     or ('azimuth' in public and (not isinstance(public['azimuth'],(int,float)) or not math.isfinite(public['azimuth'])))
                     or ('elevation' in public and (not isinstance(public['elevation'],(int,float)) or not math.isfinite(public['elevation'])))
                     or (kind in ('attach','detach') and not isinstance(public.get('partId'),str))
                     or (kind=='attach' and not isinstance(public.get('candidate'),str)))
            if invalid:
                self.invalid+=1
                feedback={'code':'INVALID_ACTION','message':'attach requires explicit string partId and candidate; detach requires string partId.'}
                self.history.append({'action':public,'feedback':feedback})
                return feedback
        action=self.internal_action(public);kind=action.get('type')
        if kind=='finish':
            self.finished=True;self.success=self.manipulator.complete(self.assignments()) if self.manipulator else self.state==self.target
            feedback={'code':'SUCCESS' if self.success else 'GOAL_NOT_MET'}
        elif kind=='inspect':
            from render import VIEWS
            if 'partId' in action and action['partId'] not in self.actors:feedback={'code':'UNKNOWN_PIECE'}
            elif 'azimuth' in action and (not isinstance(action.get('azimuth'),(int,float)) or not isinstance(action.get('elevation'),(int,float)) or not math.isfinite(action['azimuth']) or not -90<=action['elevation']<=90):feedback={'code':'INVALID_CAMERA'}
            elif 'view' in action and action['view'] not in VIEWS:feedback={'code':'UNKNOWN_VIEW'}
            else:
                self.inspections+=1;feedback={'code':'OBSERVATION_READY'}
                if picked:feedback['partId']=picked
        elif kind in ('attach','detach'):
            self.manipulations+=1
            if self.manipulator:
                after, check = self.manipulator.check(self.assignments(), action['partId'], kind, candidate=action.get('candidate'))
                self.state=self.domain.pack(self.case,after)
                # Only neutral operation feedback crosses the observation boundary.
                feedback={'code':check['code'],'blockers':[self.alias.get(x,x) for x in check.get('blockers',[])]}
            else:
                self.state,feedback=self.domain.transition(self.case,self.state,action)
            # Blockers are action feedback, with IDs only and no goal hints.
            if 'blockers' in feedback:feedback['blockers']=[self.pose(x) for x in feedback['blockers']]
            if feedback['code']!='OK':self.invalid+=1
            if feedback['code']=='OK' and self.inject():feedback={'code':'ENVIRONMENT_CHANGED','message':'The state changed externally. Observe again; the rest of your queued actions was discarded.'}
        else:
            self.invalid+=1;feedback={'code':'INVALID_ACTION'}
        self.history.append({'action':public,'feedback':feedback})
        return feedback

    def score(self):
        errors=sum(x!=y for x,y in zip(self.state,self.target))
        matched=self.manipulator.complete(self.assignments()) if self.manipulator else self.state==self.target
        accuracy=1-errors/len(self.actors)
        recall=sum(bool(t) and s==t for s,t in zip(self.state,self.target))/sum(bool(t) for t in self.target)
        if self.manipulator:
            actual=self.manipulator.signature(self.assignments()); expected=self.manipulator.signature(self.case['goal'])
            overlap=sum((actual & expected).values()); union=sum((actual | expected).values())
            errors=sum((actual-expected).values())+sum((expected-actual).values())
            accuracy=overlap/union if union else 1
            recall=overlap/sum(expected.values()) if expected else 1
        return {'success':self.success,'targetMatched':matched,
                'manipulationProtocol':'connector-workbench/4' if self.manipulator else 'registered-fixed-fixture/legacy',
                'remainingMismatches':errors,'stateAccuracy':accuracy,'targetPartRecall':recall,
                'manipulations':self.manipulations,'invalidActions':self.invalid,
                'inspectCalls':self.inspections,'eventTriggered':bool(self.events),
                'postEventRecovery':self.success if self.events else None}
