"""Regression gates for evidence-critical adapter changes (no API calls)."""
from pathlib import Path
import json,sys
from protocol import Episode,load
from static_bench import Domain,exact_plan
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'deliverables/brickplan-static-audit-2026-10-14'
selection=json.loads((OUT/'selection.json').read_text());records=[];first=total=0;multi_first=multi_total=0
for spec in selection['specs']:
 cert,cs=load(spec['modelId']);case=cs[spec['caseId']]
 ep=Episode(cert,case,seed=spec['seed'],protocol_version='v2')
 goalposes=set(ep.public_state(ep.target).values())
 for item in ep.catalog():
  if any(p['id'] in goalposes for p in item['poses']):
   total+=1;first+=item['poses'][0]['id'] in goalposes
   if len(item['poses'])>1:multi_total+=1;multi_first+=item['poses'][0]['id'] in goalposes
 # Exact original oracle remains a valid certificate in the larger action domain.
 for action in case['oraclePlan']:
  public={k:ep.alias[v] if k=='partId' else ep.pose(v) if k=='candidate' else v for k,v in action.items()}
  feedback=ep.step(public);assert feedback['code']=='OK',(case['id'],feedback)
 assert ep.step({'type':'finish'})['code']=='SUCCESS'
 # Catalogue has no case-conditioned ordering or availability filter.
 control=next(c for c in cs.values() if c['kind']=='control')
 a=Episode(cert,case,seed=spec['seed'],protocol_version='v2');b=Episode(cert,control,seed=spec['seed'],protocol_version='v2');assert a.catalog()==b.catalog()
 assert a.catalog()==Episode(cert,case,seed=spec['seed'],protocol_version='v2').catalog()
 initial=a.state
 for action in [{'type':'attach','partId':next(iter(a.reverse))},{'type':'attach','partId':[],'candidate':{}},{'type':[]},{'type':'inspect','view':[]},{'type':'inspect','azimuth':float('nan'),'elevation':0},None]:
  assert a.step(action)['code']=='INVALID_ACTION';assert a.state==initial
 obs=a.observe('visual');assert 'current' not in obs and 'target' not in obs and 'legalActions' not in obs
 assert all(x not in json.dumps(obs) for x in ('oraclePlan','expectedOptimum',':goal',':wrong'))
 records.append({'caseId':case['id'],'oracleLength':len(case['oraclePlan']),'oracleReplayPassed':True,'catalogCaseIndependent':True})
# Demonstrate old omitted-candidate bug with the smallest admitted missing case.
for m in json.loads((ROOT/'deliverables/brickplan-repair-library/index.json').read_text())['models']:
 cert,cs=load(m['modelId']);case=next((c for c in cs.values() if c['kind']=='missing' and c['expectedOptimum']==1),None)
 if case:
  old=Episode(cert,case);actor=next(a for a,k in old.assignments().items() if not k and old.case['goal'][a]);action={'type':'attach','partId':old.alias[actor]};feedback=old.step(action)
  assert feedback['code']=='OK' and old.state==old.target
  bug={'caseId':case['id'],'action':action,'oldFeedback':feedback,'oldTargetMatched':True,'v2RejectsOmittedCandidate':True};break
result={'passed':True,'cases':len(records),'checks':records,'oldImplicitGoalReproduction':bug,'shuffledGoalFirst':first,'goalActors':total,'multiPoseGoalFirst':multi_first,'multiPoseGoalActors':multi_total}
(OUT/'protocol-audit.json').write_text(json.dumps(result,indent=2));print({k:v for k,v in result.items() if k!='checks'})
