"""Exhaustive finite-domain certificates, including ALL optimal repair paths.

Exactness is only for the explicitly enumerated actor/pose domain. It is never a
claim about all continuous poses, arbitrary robot paths, or physical forces.
"""
from collections import deque, defaultdict
from pathlib import Path
import hashlib
import json
import numpy as np

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

class TransitionIndex:
    """Compile the same geometry predicates as Assembly.check into finite guards.

    A path exists iff an available direction/length has no present blocker. No
    gravity/reachability heuristic or target predicate enters legal transitions.
    Direct replay of every reference witness independently checks compilation.
    """
    def __init__(self, runtime, choices):
        self.runtime=runtime; self.actors=tuple(sorted(choices)); self.choices=choices
        self.keys=tuple(sorted({k for values in choices.values() for k in values if k}))
        self.bit={k:1<<i for i,k in enumerate(self.keys)}; self.rows={}
        parts={k:runtime.row(k)['part'] for k in self.keys}
        for key,p in parts.items():
            actor=runtime.row(key)['actor']; peers={k:q for k,q in parts.items() if runtime.row(k)['actor']!=actor}
            endpoint=sum(self.bit[k] for k,q in peers.items() if runtime.q.endpoint(p,q)['status']!='CLEAR')
            links={k:runtime.q.connection(p,q) for k,q in peers.items()}
            environment=runtime.environment_connections(p)
            directions=[(np.asarray(p['direction']),0)]
            directions += [(np.asarray(p['matrix'])[:3,i]*sign,0) for i in range(3) for sign in (1,-1)]
            directions += [(np.asarray(c['axis'])*sign,0) for _,c in environment for sign in (1,-1)]
            directions += [(np.asarray(c['axis'])*sign,self.bit[k]) for k,cs in links.items() for c in cs for sign in (1,-1)]
            merged={}
            for d,guard in directions:
                d=d/np.linalg.norm(d); token=tuple(np.round(d,5))
                if token not in merged: merged[token]=[d,guard,guard==0]
                else: merged[token][1]|=guard; merged[token][2]|=guard==0
            paths=[]
            for d,guard,unconditional in merged.values():
                for length in runtime.path_lengths(p,d):
                    if runtime.environment_path_blockers(p,d,length):continue
                    blocked=sum(self.bit[k] for k,q in peers.items() if runtime.q.path({**p,'direction':d.tolist()},q,length)['status']!='CLEAR')
                    paths.append((0 if unconditional else guard,blocked))
            self.rows[key]=dict(endpoint=endpoint,environment=bool(runtime.environment_blockers(p)),
                                links=sum(self.bit[k] for k,v in links.items() if v),anchor=bool(environment),paths=paths)
        self.signatures={k:next(iter(runtime.signature({runtime.row(k)['actor']:k}))) for k in self.keys}
        self.goal=runtime.signature(runtime.goal)

    def state(self, assignments): return tuple(assignments.get(a,'') for a in self.actors)
    def unpack(self, state): return dict(zip(self.actors,state))
    def complete(self, state):
        from collections import Counter
        return self.goal==Counter(self.signatures[k] for k in state if k)
    def transition(self, state, actor, kind, key=None):
        i=self.actors.index(actor); key=state[i] if kind=='detach' else key
        if bool(state[i]) != (kind=='detach') or not key or key not in self.choices[actor]:return None
        row=self.rows[key]; present=sum(self.bit[k] for j,k in enumerate(state) if k and j!=i)
        if row['environment'] or row['endpoint']&present:return None
        if kind=='attach' and not row['anchor'] and not row['links']&present:return None
        if not any((not guard or guard&present) and not blockers&present for guard,blockers in row['paths']):return None
        result=list(state);result[i]='' if kind=='detach' else key
        return tuple(result)
    def actions(self, state):
        for actor,key in zip(self.actors,state):
            options=[dict(type='detach',partId=actor)] if key else [dict(type='attach',partId=actor,candidate=k) for k in self.choices[actor]]
            for action in options:
                after=self.transition(state,actor,action['type'],action.get('candidate'))
                if after is not None:yield after,action

class FiniteGraph:
    def __init__(self,index,max_states=20000):
        self.index=index; self.max_states=max_states
    def build(self,initial):
        self.initial=self.index.state(initial);queue=deque([self.initial]);self.states={self.initial}
        self.edges={};self.reverse=defaultdict(list);self.complete=True
        while queue:
            state=queue.popleft();edges=list(self.index.actions(state));self.edges[state]=edges
            for after,action in edges:
                self.reverse[after].append((state,action))
                if after in self.states:continue
                if len(self.states)>=self.max_states:self.complete=False;return self
                self.states.add(after);queue.append(after)
        goals=[s for s in self.states if self.index.complete(s)]
        self.distance={g:0 for g in goals};queue=deque(goals)
        while queue:
            s=queue.popleft()
            for before,_ in self.reverse[s]:
                if before not in self.distance:self.distance[before]=self.distance[s]+1;queue.append(before)
        return self
    def witness(self,start=None):
        node=self.initial if start is None else start;plan=[]
        while self.distance[node]:
            after,action=next((s,a) for s,a in self.edges[node] if self.distance.get(s)==self.distance[node]-1)
            plan.append(action);node=after
        return plan
    def proof(self,initial):
        domain=dict(actors=list(self.index.actors),choices=self.index.choices,goalRule='physical-multiset-with-declared-symmetries')
        result=dict(schema='selective-repair-certificate/1',domain=domain,domainSha256=digest(domain),
                    exactnessScope='ONLY declared finite placements, shared rigid connector/path validator',
                    sourceSha256=self.index.runtime.cert.get('contentSha256'),states=len(self.states),exhaustive=self.complete,
                    initialStateSha256=digest(self.index.unpack(self.initial)),goalStateSha256=digest(self.index.runtime.goal),
                    globalContinuousOptimum=None)
        here=Path(__file__).resolve().parents[1]
        files=[here/'assembly.py',here/'baseplate.py',here/'library.py',here.parent/'brickplan-v1/geometry.py',Path(__file__)]
        result['implementationSha256']={str(p.relative_to(here.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        from geometry import mesh_for
        result['collisionMeshSha256']={stem:mesh_for(stem)[3] for stem in sorted({self.index.runtime.row(k)['part']['canonical'] for k in self.index.keys}|{'3024'})}
        if not self.complete:return {**result,'status':'SEARCH_LIMIT','optimalCost':None}
        if self.initial not in self.distance:return {**result,'status':'UNREACHABLE','optimalCost':None}
        runtime=self.index.runtime;initial=runtime.state(initial);target=runtime.signature(runtime.goal)
        correct=[];remaining=target.copy()
        for a,k in initial.items():
            if not k:continue
            signature=self.index.signatures[k]
            if remaining[signature]>0:correct.append(a);remaining[signature]-=1
        masks={a:1<<i for i,a in enumerate(correct)}
        counts={};sets={}
        for state in sorted(self.distance,key=self.distance.get):
            if self.distance[state]==0:counts[state]=1;sets[state]={0};continue
            counts[state]=0;sets[state]=set()
            for after,action in self.edges[state]:
                if self.distance.get(after)!=self.distance[state]-1:continue
                counts[state]+=counts[after]
                flag=masks.get(action['partId'],0) if action['type']=='detach' else 0
                sets[state].update(s|flag for s in sets[after])
        options=sets[self.initial];union=0;intersection=(1<<len(correct))-1
        for mask in options:union|=mask;intersection&=mask
        decode=lambda mask:[a for a in correct if masks[a]&mask]
        # Unavoidability across ALL valid paths is a separate reachability test,
        # not the intersection of just one plan or even all shortest plans.
        unavoidable=[]
        for actor in correct:
            seen={self.initial};queue=deque(seen);reachable=False
            while queue:
                s=queue.popleft()
                if self.index.complete(s):reachable=True;break
                for after,action in self.edges[s]:
                    if action['type']=='detach' and action['partId']==actor:continue
                    if after not in seen:seen.add(after);queue.append(after)
            if not reachable:unavoidable.append(actor)
        plan=self.witness();state=runtime.state(initial)
        for action in plan:
            state,feedback=runtime.check(state,action['partId'],action['type'],candidate=action.get('candidate'))
            if feedback['code']!='OK':raise AssertionError(('compiled/direct mismatch',action,feedback))
        assert runtime.complete(state)
        result.update(status='CERTIFIED_FINITE',optimalCost=self.distance[self.initial],referencePlan=plan,
            optimalPlanCount=str(counts[self.initial]),initiallyCorrect=correct,
            allShortest=dict(mustRemove=decode(intersection),mayRemove=decode(union),
                             collateralSets=sorted([decode(s) for s in options]),
                             minimumCorrectRemoved=min(s.bit_count() for s in options),
                             maximumCorrectRemoved=max(s.bit_count() for s in options)),
            allValid=dict(unavoidableCorrectRemovals=unavoidable),
            witnessDirectlyReplayed=True,goalStates=sum(d==0 for d in self.distance.values()))
        result['certificateSha256']=digest(result)
        return result


def verify_certificate(runtime,case,certificate):
    """Fail closed on altered, misassigned, or stale finite certificates."""
    from geometry import mesh_for
    if certificate.get('status')!='CERTIFIED_FINITE' or not certificate.get('exhaustive'):
        raise ValueError('An exhaustive finite certificate is required')
    if digest({k:v for k,v in certificate.items() if k!='certificateSha256'})!=certificate.get('certificateSha256'):
        raise ValueError('Certificate digest mismatch')
    if case.get('certificate',{}).get('sha256',certificate['certificateSha256'])!=certificate['certificateSha256']:
        raise ValueError('Case/certificate mismatch')
    if certificate.get('initialStateSha256')!=digest(runtime.state(case['initial'])) or certificate.get('goalStateSha256')!=digest(runtime.goal):
        raise ValueError('Certificate initial/goal mismatch')
    if certificate.get('sourceSha256')!=runtime.cert.get('contentSha256'):
        raise ValueError('Certificate geometry source mismatch')
    root=Path(__file__).resolve().parents[2]
    for name,expected in certificate['implementationSha256'].items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=expected:raise ValueError('Stale validator certificate: '+name)
    for stem,expected in certificate['collisionMeshSha256'].items():
        if mesh_for(stem)[3]!=expected:raise ValueError('Stale geometry mesh: '+stem)
