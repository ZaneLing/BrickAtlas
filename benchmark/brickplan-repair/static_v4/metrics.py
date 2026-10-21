"""Trajectory evaluation shared by human replays and visual agents.

Ground truth, graph distances and diagnostics stay evaluator-side. Success is
physical multiset equivalence, never reference-sequence or actor-ID equality.
"""
from collections import Counter
from copy import deepcopy
from static_v4.certify import digest,verify_certificate


def overlap(actual, target):
    correct=sum((actual & target).values()); n=sum(actual.values()); m=sum(target.values())
    precision=correct/n if n else float(not m)
    recall=correct/m if m else float(not n)
    return dict(correct=correct,actual=n,target=m,precision=precision,recall=recall,
                f1=2*precision*recall/(precision+recall) if precision+recall else 0.,
                extra=sum((actual-target).values()),missing=sum((target-actual).values()))


def residual(runtime,state):
    a,b=runtime.signature(state),runtime.signature(runtime.goal)
    return sum((a-b).values())+sum((b-a).values())


def connections(runtime,state):
    """Undirected piece-pair adjacency, NOT per-stud or force correctness."""
    graph,_=runtime.connections(state);signatures={a:next(iter(runtime.signature({a:k}))) for a,k in state.items() if k}
    signatures['@baseplate']=('environment','white-infinite-baseplate')
    result=Counter()
    for a,neighbors in graph.items():
        for b in neighbors:
            if a<b:result[tuple(sorted((digest(signatures[a]),digest(signatures[b]))))]+=1
    return result


class RepairEpisode:
    def __init__(self,runtime,case,certificate=None,graph=None):
        if certificate is not None:verify_certificate(runtime,case,certificate)
        self.runtime=runtime;self.case=case;self.state=runtime.state(case['initial'])
        self.initial=dict(self.state);self.certificate=certificate;self.graph=graph
        self.records=[];self.finished=False;self.success=False;self.visited=[dict(self.state)]
        remaining=runtime.signature(runtime.goal).copy();self.correct=set()
        for a,k in self.state.items():
            if not k:continue
            signature=next(iter(runtime.signature({a:k})))
            if remaining[signature]:self.correct.add(a);remaining[signature]-=1
        self.chain=digest(dict(caseId=case['id'],initial=self.initial,source=runtime.cert.get('contentSha256')))

    def step(self,action):
        action=deepcopy(action);before=dict(self.state);kind=action.get('type');actor=action.get('partId')
        if self.finished:raise ValueError('Episode is closed; reset requires a new episode')
        if kind=='finish':
            self.success=self.runtime.complete(self.state);self.finished=True
            feedback=dict(code='SUCCESS' if self.success else 'INCOMPLETE')
        elif kind=='inspect':feedback=dict(code='OBSERVED')
        elif kind in ('attach','detach'):
            try:
                self.state,feedback=self.runtime.check(self.state,actor,kind,raw=action.get('rawMatrix'),candidate=action.get('candidate'))
            except (ValueError,KeyError,TypeError):feedback=dict(code='INVALID_ACTION')
        else:feedback=dict(code='INVALID_ACTION')
        regret=None
        if self.graph is not None and kind in ('attach','detach'):
            x=self.graph.index.state(before);y=self.graph.index.state(self.state)
            if x in self.graph.distance and y in self.graph.distance:
                regret=1+self.graph.distance[y]-self.graph.distance[x]
        record=dict(index=len(self.records),action=action,code=feedback['code'],
                    beforeSha256=digest(before),afterSha256=digest(self.state),
                    residualEdits=residual(self.runtime,self.state),finiteDecisionRegret=regret)
        record['chainSha256']=digest(dict(previous=self.chain,record=record));self.chain=record['chainSha256']
        self.records.append(record);self.visited.append(dict(self.state))
        # No hidden distances, defect labels, optimal moves or certificate data.
        return dict(code=feedback['code'])

    def score(self):
        rt=self.runtime;actual=rt.signature(self.state);goal=rt.signature(rt.goal)
        physical=overlap(actual,goal)
        # Ablations of the same symmetry-aware physical multiset. These are
        # joint attribute projections, NOT independent object-detector scores.
        shape_pose=lambda c:Counter(k for s,n in c.items() for k in [(s[0],s[2])]*n)
        color_pose=lambda c:Counter(k for s,n in c.items() for k in [(s[1],s[2])]*n)
        manip=[r for r in self.records if r['action'].get('type') in ('attach','detach')]
        valid=[r for r in manip if r['code']=='OK'];invalid=[r for r in manip if r['code']!='OK']
        removed=Counter(r['action']['partId'] for r in valid if r['action']['type']=='detach' and r['action']['partId'] in self.correct)
        seq=[residual(rt,s) for s in self.visited]
        initial_residual=seq[0]
        certificate=self.certificate or {};finite=certificate.get('optimalCost')
        domain=certificate.get('domain',{}).get('choices',{})
        finite_eligible=bool(domain) and all(all(not k or k in domain.get(a,[]) for a,k in s.items()) for s in self.visited)
        legal_cost=len(valid);attempts=len(manip)
        witness=certificate.get('referencePlan',self.case.get('oraclePlan'))
        upper=len(witness) if witness is not None else None
        success=self.finished and self.success
        shortest=certificate.get('allShortest',{})
        collateral_options=shortest.get('collateralSets',[])
        # A union of all shortest masks is not a valid joint choice: compare
        # against each complete set so removing BOTH alternative doors counts.
        collateral_excess=min((len(set(removed)-set(s)) for s in collateral_options),default=None)
        return dict(schema='selective-repair-metrics/1',caseId=self.case['id'],
            success=success,finished=self.finished,finalEquivalent=rt.complete(self.state),
            terminal=dict(physical=physical,shapeAndPose=overlap(shape_pose(actual),shape_pose(goal)),
                          colorAndPose=overlap(color_pose(actual),color_pose(goal)),
                          connectionAdjacency=overlap(connections(rt,self.state),connections(rt,rt.goal))),
            execution=dict(manipulationAttempts=attempts,legalMoves=legal_cost,invalidMoves=len(invalid),
                           invalidByReason=dict(Counter(r['code'] for r in invalid)),
                           observations=sum(r['action'].get('type')=='inspect' for r in self.records),
                           otherInvalid=sum(r['code']=='INVALID_ACTION' and r not in manip for r in self.records),
                           prematureFinish=self.finished and not self.success),
            preservation=dict(initiallyCorrect=len(self.correct),correctPiecesRemoved=len(removed),
                              correctRemovalEvents=sum(removed.values()),repeatCorrectRemovals=sum(max(0,n-1) for n in removed.values()),
                              peakCorrectPiecesInRack=max(sum(not s[a] for a in self.correct) for s in self.visited),
                              additionalPiecesVsClosestShortestSet=collateral_excess if finite_eligible else None,
                              initialNoOp=initial_residual==0,falseRepair=initial_residual==0 and legal_cost>0),
            process=dict(initialEditResidual=initial_residual,finalEditResidual=seq[-1],
                         meanResidualPerDecision=sum(seq[1:])/max(1,len(seq)-1),
                         worsenings=sum(b>a for a,b in zip(seq,seq[1:])),
                         residualPerDecision=seq),
            cost=dict(finiteDomainEligible=finite_eligible,finiteOptimum=finite if finite_eligible else None,
                      finiteLegalExcess=legal_cost-finite if success and finite_eligible and finite is not None else None,
                      finiteAttemptExcess=attempts-finite if success and finite_eligible and finite is not None else None,
                      unrestrictedEditLowerBound=initial_residual,executableWitnessUpperBound=upper,
                      unrestrictedLegalExcessInterval=[max(0,legal_cost-upper),legal_cost-initial_residual]
                          if success and upper is not None else None,
                      globalContinuousOptimum=None),
            trace=dict(records=len(self.records),chainSha256=self.chain,protocol=rt.baseplate and 'connector-workbench/5-white-baseplate'))

    def export(self):
        return dict(score=self.score(),initial=self.initial,final=self.state,actions=self.records,
                    runtimePoses=self.runtime.extra)
