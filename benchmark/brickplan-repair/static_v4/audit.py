"""Offline oracle/validator audit. Never reports these as VLM accuracy."""
from pathlib import Path
from copy import deepcopy
import json,sys,random
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from baseplate import PlateAssembly
from static_v4.certify import TransitionIndex,FiniteGraph
from static_v4.metrics import RepairEpisode
from static_v4.build_suite import OUT,dump


def load(path):return json.loads(path.read_text())
def run():
    rows=[];parity=0;all_cases=[];mechanisms={};checks=[]
    for model in load(OUT/'library/index.json')['models']:
        folder=OUT/'library/models'/model['modelId'];rt=PlateAssembly(load(folder/'qualification.json'))
        cases=load(folder/'cases.json');first=next(iter(cases.values()))
        choices={a:[k for k,r in rt.candidates.items() if r['actor']==a] for a in rt.actors}
        index=TransitionIndex(rt,choices);graph=FiniteGraph(index).build(first['initial'])
        # Complete one small graph; seeded samples across every larger model.
        states=sorted(graph.states)
        sample=states if model['modelId']=='sr4-shared-1' else random.Random(214).sample(states,min(20,len(states)))
        for state in sample:
            for actor,key in zip(index.actors,state):
                options=[('detach',None)] if key else [('attach',k) for k in choices[actor]]
                for kind,pose in options:
                    expected=index.transition(state,actor,kind,pose)
                    after,feedback=rt.check(index.unpack(state),actor,kind,candidate=pose)
                    actual=index.state(after) if feedback['code']=='OK' else None
                    assert actual==expected,(model['modelId'],state,actor,kind,feedback)
                    parity+=1
        for case in cases.values():
            all_cases.append(case)
            proof=load(OUT/case['certificate']['file']);ep=RepairEpisode(rt,case,proof,graph)
            tampered=deepcopy(proof);tampered['optimalCost']+=1
            try:RepairEpisode(rt,case,tampered)
            except ValueError:pass
            else:raise AssertionError('Tampered certificate accepted')
            for action in proof['referencePlan']:assert ep.step(action)['code']=='OK'
            assert ep.step({'type':'finish'})['code']=='SUCCESS'
            score=ep.score();assert score['cost']['finiteLegalExcess']==0
            assert score['terminal']['physical']['f1']==1 and score['terminal']['connectionAdjacency']['f1']==1
            dump(OUT/'traces'/('oracle--'+case['id'].replace(':','--')+'.json'),ep.export())
            # Ground-truth privileged diagnostic: try editing ONLY erroneous
            # pieces; do not move correct covers. This is not an AI model.
            direct=RepairEpisode(rt,case,proof)
            for _ in range(len(rt.actors)*2):
                moved=False
                for actor,key in list(direct.state.items()):
                    goal=rt.goal[actor]
                    if key==goal:continue
                    action=dict(type='detach',partId=actor) if key else dict(type='attach',partId=actor,candidate=goal)
                    if not key and not goal:continue
                    if direct.step(action)['code']=='OK':moved=True
                if not moved or rt.complete(direct.state):break
            direct.step(dict(type='finish'))
            no_op=RepairEpisode(rt,case,proof);no_op.step(dict(type='finish'))
            rows.append(dict(caseId=case['id'],family=case['sourceFamily'],mechanism=case['mechanism'],
                finiteOracleSuccess=score['success'],directOnlySuccess=direct.score()['success'],
                finishOnlySuccess=no_op.score()['success'],cost=proof['optimalCost'],
                shortestPlans=proof['optimalPlanCount'],collateralSets=proof['allShortest']['collateralSets']))
        if model['modelId']=='sr4-alternative-release':
            case=cases[model['modelId']+':color'];proof=load(OUT/case['certificate']['file'])
            assert proof['allShortest']['mustRemove']==[]
            assert proof['allShortest']['collateralSets']==[['P006'],['P008']]
            assert proof['allValid']['unavoidableCorrectRemovals']==[]
            # Both alternatives must receive the same full success and cost.
            for cover in ['P006','P008']:
                ep=RepairEpisode(rt,case,proof,graph)
                for action in [dict(type='detach',partId=cover),dict(type='detach',partId='W007'),
                    dict(type='attach',partId='P007',candidate='P007:goal'),dict(type='attach',partId=cover,candidate=cover+':goal')]:
                    assert ep.step(action)['code']=='OK'
                ep.step(dict(type='finish'));assert ep.score()['success'] and ep.score()['cost']['finiteLegalExcess']==0
                dump(OUT/'traces'/f'alternative-{cover}.json',ep.export())
            checks.append('both alternative collateral sets accepted; neither cover individually mandatory')
            ep=RepairEpisode(rt,case,proof,graph)
            for action in [dict(type='detach',partId='P008'),dict(type='detach',partId='P006'),
                dict(type='detach',partId='W007'),dict(type='attach',partId='P006',candidate='P006:goal'),
                dict(type='attach',partId='P007',candidate='P007:goal'),dict(type='attach',partId='P008',candidate='P008:goal')]:
                assert ep.step(action)['code']=='OK'
            ep.step(dict(type='finish'))
            assert ep.score()['preservation']['additionalPiecesVsClosestShortestSet']==1
            checks.append('removing both alternative doors correctly costs an extra piece; union-of-paths is not treated as necessary')
            # Choosing a locally correct roof placement too early adds 2 moves.
            case=cases[model['modelId']+':order'];s=index.state(case['initial'])
            s=index.transition(s,'P006','detach');s=index.transition(s,'P006','attach','P006:goal')
            assert graph.distance[s]==4
            checks.append('premature roof correction: 2 moves spent, 4 remain versus initial optimum 4')
        if model['modelId']=='sr4-buried-1':
            case=cases[model['modelId']+':color'];proof=load(OUT/case['certificate']['file'])
            ep=RepairEpisode(rt,case,proof,graph)
            ep.step(dict(type='inspect',view='rear'))
            assert ep.step(dict(type='detach',partId='W001'))['code']=='PATH_BLOCKED'
            # A legal but avoidable detour on the irrelevant correct part.
            for action in [dict(type='detach',partId='P020'),dict(type='attach',partId='P020',candidate='P020:goal')]+proof['referencePlan']:
                assert ep.step(action)['code']=='OK'
            ep.step(dict(type='finish'));score=ep.score()
            assert score['success'] and score['cost']['finiteLegalExcess']==2 and score['cost']['finiteAttemptExcess']==3
            assert score['preservation']['additionalPiecesVsClosestShortestSet']==1
            assert score['execution']['observations']==1 and score['execution']['invalidMoves']==1
            dump(OUT/'traces'/'avoidable-detour.json',ep.export())
            checks.append('legal detour succeeds; invalid attempt, inspect, collateral, and cost scored separately')
            # A free, connector-aligned intermediate placement must drop the
            # finite-domain optimum claim, then still accept final correctness.
            ep=RepairEpisode(rt,case,proof)
            raw=[row[:] for row in rt.row('P020:goal')['part']['rawMatrix']];raw[0][3]+=40
            for action in [dict(type='detach',partId='P020'),dict(type='attach',partId='P020',rawMatrix=raw),
                           dict(type='detach',partId='P020'),dict(type='attach',partId='P020',candidate='P020:goal')]+proof['referencePlan']:
                assert ep.step(action)['code']=='OK'
            ep.step(dict(type='finish'));score=ep.score()
            assert score['success'] and score['cost']['finiteOptimum'] is None
            dump(OUT/'traces'/'free-pose-detour.json',ep.export())
            checks.append('arbitrary registered pose accepted; finite optimum suppressed outside certificate domain')
        limited=FiniteGraph(index,max_states=1).build(first['initial']).proof(first['initial'])
        assert limited['status']=='SEARCH_LIMIT' and limited['optimalCost'] is None
    checks+=['search limits never produce an optimum','all equivalent-instance and symmetry controls accepted at zero cost',
             'altered certificate costs rejected in every case']
    # Leave-one-family-out: paired cases, depths, and structural counterparts
    # never cross a fold. Four families is a pilot, not a broad held-out corpus.
    families=sorted({c['sourceFamily'] for c in all_cases})
    folds=[dict(testFamily=f,train=[c['id'] for c in all_cases if c['sourceFamily']!=f],
                test=[c['id'] for c in all_cases if c['sourceFamily']==f]) for f in families]
    dump(OUT/'splits.json',dict(schema='source-family-lofo/1',seed=214,families=families,folds=folds,
                              limitation='Four procedural families only; not evidence of broad generalization'))
    report=dict(kind='offline privileged reference and evaluator audit; NOT model accuracy',
                cases=len(rows),directTransitionParityChecks=parity,checks=checks,rows=rows,
                totals={k:sum(r[k] for r in rows) for k in ['finiteOracleSuccess','directOnlySuccess','finishOnlySuccess']})
    dump(OUT/'verification.json',report);print(json.dumps({k:v for k,v in report.items() if k!='rows'},ensure_ascii=False,indent=2))

if __name__=='__main__':run()
