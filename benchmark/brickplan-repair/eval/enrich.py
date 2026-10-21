"""Admit hard four-defect static cases from already qualified finite placements."""
import sys,json
from pathlib import Path
from copy import deepcopy
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from static_bench import OUT,Domain,make_case,groups_for,annotate_static,normalized_state,visual_reference,dump,aggregate
changes=[]
for model in ['v23-3223--deep','10001--deep','v23-6678--deep','v23-30571--deep']:
    p=OUT/'models'/model;cert=json.loads((p/'qualification.json').read_text());cases=json.loads((p/'cases.json').read_text());record=json.loads((p/'record.json').read_text())
    domain=Domain(cert,{});seen={normalized_state(c,cert) for c in cases.values()}
    singles=[c for c in cases.values() if len(c['roots'])==1]
    triples=[c for c in cases.values() if len(c['roots'])>=3]
    new=[]
    for a in sorted(triples,key=lambda c:-c['expectedOptimum']):
        used={x for r in a['roots'] for x in r['affectedActors']}
        for b in sorted(singles,key=lambda c:-c['expectedOptimum']):
            if used&{x for r in b['roots'] for x in r['affectedActors']}:continue
            edits={x:k for c in (a,b) for x,k in c['initial'].items() if k!=c['goal'].get(x,'')}
            if len(edits)>8:continue
            c=make_case(cert,model,edits,groups_for(cert,edits))
            if normalized_state(c,cert) in seen:continue
            try:c=annotate_static(c,domain)
            except ValueError:continue
            if c['expectedOptimum']<10 or c['repairEvidence']['requiredExtraActions']<2:continue
            c['qualificationSha256']=cert['contentSha256'];c['targetProvenance']=record['targetProvenance'];c['challengeVariant']='four_fault_coupling'
            c['tags'].append('four_fault_coupling');visual_reference(c,{})
            new.append(c);seen.add(normalized_state(c,cert))
            if len(new)>=2:break
        if len(new)>=2:break
    for c in new:cases[c['id']]=c;changes.append({'id':c['id'],'roots':len(c['roots']),'cost':c['expectedOptimum'],'extra':c['repairEvidence']['requiredExtraActions']})
    record['caseCount']=len(cases);record['kinds']=dict(Counter(c['kind'] for c in cases.values()));record['difficulty']=dict(Counter(c['difficulty'] for c in cases.values()))
    record['cases']=[{k:c[k] for k in ('id','title','kind','difficulty','expectedOptimum')} for c in cases.values()]
    dump(p/'cases.json',cases);dump(p/'record.json',record)
aggregate();dump(OUT/'four-fault-expansion.json',changes);print(json.dumps(changes,ensure_ascii=False))
