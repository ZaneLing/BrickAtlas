"""Full-bank offline coverage and principle audit, independent of API spend."""
from pathlib import Path
from collections import Counter,defaultdict,deque
from copy import deepcopy
import json,sys,hashlib,time
import numpy as np
from protocol import Episode,load
from static_bench import exact_plan
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'deliverables/brickplan-static-audit-2026-10-14';BANK=ROOT/'deliverables/brickplan-repair-library'
index=json.loads((BANK/'index.json').read_text());allcases=[];structures=[];goalfirst=multifirst=multi=total=0;onepose=0
symmetry=Counter();evidence=Counter();graph=Counter();paths=Counter();types=Counter();duplicates=0
# A separate finite-state rule checker, implemented without Domain.valid/transition.
def independent_valid(cert,case,state):
 if len(state)!=len(case['actors']) or state.count('')>case['rackCapacity']:return False
 installed={k for k in state if k};present=installed|set(cert['fixed'])
 for actor,key in zip(case['actors'],state):
  if key and (key not in case['choices'][actor] or cert['candidates'][key]['actor']!=actor):return False
  if key and any(q in present for q in cert['candidates'][key]['endpointBlocked']):return False
 q=deque(cert['fixed']);reached=set(cert['fixed'])
 while q:
  n=q.popleft()
  for k in installed-reached:
   if n in cert['candidates'][k]['support']:reached.add(k);q.append(k)
 return installed<=reached

def independent_action(cert,case,state,action):
 actor=action['partId'];idx=case['actors'].index(actor);old=state[idx];kind=action['type'];key=old if kind=='detach' else action['candidate']
 if (kind=='detach' and not old) or (kind=='attach' and old):return state,False
 if key not in case['choices'][actor]:return state,False
 if (set(state)-{'',old}|set(cert['fixed']))&set(cert['candidates'][key]['pathBlocked']):return state,False
 new=list(state);new[idx]='' if kind=='detach' else key;new=tuple(new)
 return (new,True) if independent_valid(cert,case,new) else (state,False)

checks=0;negative=Counter();visualmin=[]
for m in index['models']:
 cert,cs=load(m['modelId']);allcases.extend(cs.values());actors={r['actor'] for r in cert['candidates'].values()}
 partcounts=Counter((r['part']['canonical'],r['part']['colorHex']) for r in cert['candidates'].values() if r['kind']=='goal')
 duplicates+=any(v>1 for v in partcounts.values())
 for actor in actors:
  rr=[r for r in cert['candidates'].values() if r['actor']==actor]
  if any(r['kind']=='goal' for r in rr):
   total+=1;goalfirst+=rr[0]['kind']=='goal';onepose+=len(rr)==1
   if len(rr)>1:multi+=1;multifirst+=rr[0]['kind']=='goal'
 for row in cert['candidates'].values():
  types[row['part']['canonical']]+=1
  for e in row.get('evidence',[]):
   evidence[e['endpoint']['status']]+=1;paths[e['path']['status']]+=1
   for con in e['connectors']:graph[con['family']]+=1
 for c in cs.values():
  state=tuple(c['initial'][a] for a in c['actors']);goal=tuple(c['goal'][a] for a in c['actors']);assert independent_valid(cert,c,state) and independent_valid(cert,c,goal)
  for a in c['oraclePlan']:
   state,ok=independent_action(cert,c,state,a);assert ok,c['id'];checks+=1
  assert state==goal
  for a in c['repairEvidence']['directRepairChecks']:negative[a['code']]+=1
  for r in c['observation'].get('actualStatePixelAudit',{}).get('roots',[]):visualmin.append(r['best']['changedPixels'])
 structures.append({'modelId':m['modelId'],'caseParts':m['caseParts'],'originalParts':m['originalParts'],'partFraction':m['caseParts']/m['originalParts'],'caseCount':len(cs),'primaryCounts':dict(Counter(c['kind'] for c in cs.values())),'structuralCounts':dict(Counter(k for c in cs.values() for k in c['structuralTypes'])),'maxCost':max(c['expectedOptimum'] for c in cs.values()),'sourceExact':m.get('targetProvenance',{}).get('kind')=='source_exact','identicalPartColorGroups':sum(v>1 for v in partcounts.values())})
# Re-solve the selected cases in the actual expanded API domain, capped explicitly.
expanded=[];selection=json.loads((OUT/'selection.json').read_text())
for s in selection['specs']:
 cert,cs=load(s['modelId']);ep=Episode(cert,cs[s['caseId']],seed=s['seed'],protocol_version='v2');start=time.time()
 try:
  plan,n=exact_plan(ep.domain,ep.case,max_expansions=30000)
  row={'caseId':s['caseId'],'solved':True,'expandedOptimum':len(plan),'expandedNodes':n,'restrictedOptimum':s['restrictedCost']}
 except ValueError as e:row={'caseId':s['caseId'],'solved':False,'reason':str(e),'restrictedOptimum':s['restrictedCost']}
 row['seconds']=time.time()-start;expanded.append(row);print(json.dumps(row),flush=True)
stat=lambda values:{'min':min(values),'median':float(np.median(values)),'max':max(values)}
summary={'caseCount':len(allcases),'structures':structures,'kindCounts':dict(Counter(c['kind'] for c in allcases)),'structuralTypeCounts':dict(Counter(k for c in allcases for k in c['structuralTypes'])),'difficultyCounts':dict(Counter(c['difficulty'] for c in allcases)),'rootCountDistribution':dict(Counter(len(c['roots']) for c in allcases if c['kind']=='compound')),'structureParts':stat([r['caseParts'] for r in structures]),'sourceFraction':stat([r['partFraction'] for r in structures]),'primaryKindsPerStructure':dict(Counter(len([k for k in r['primaryCounts'] if k!='control']) for r in structures)),'compoundSourceCount':len({c['modelId'] for c in allcases if len(c['roots'])==4}),'maxCost':max(c['expectedOptimum'] for c in allcases),'maxCollateral':max(len(c['repairEvidence']['oracleCollateralParts']) for c in allcases),'extraActionStats':stat([c['repairEvidence']['requiredExtraActions'] for c in allcases]),'requiresCollateralCases':sum(bool(c['repairEvidence']['oracleCollateralParts']) for c in allcases),'singlePoseGoalActors':onepose,'goalActors':total,'oldGoalFirstActors':goalfirst,'oldMultiPoseGoalFirstActors':multifirst,'multiPoseGoalActors':multi,'identicalPartColorStructures':duplicates,'uniquePartTypes':len(types),'connectorEvidenceCounts':dict(graph),'endpointEvidenceStatus':dict(evidence),'pathEvidenceStatus':dict(paths),'negativeDirectRepairCounts':dict(negative),'independentOracleReplayActions':checks,'expandedDomainOptima':expanded,'visualAdmissionMinimumRootBestPixels':min(visualmin),'newGeometryChecks':False,'geometryCaveat':'Replays use saved geometry certificates. Independent action/state checker validates logic, not an independent geometry engine.'}
(OUT/'bank-audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k not in ('structures','expandedDomainOptima')},ensure_ascii=False))
