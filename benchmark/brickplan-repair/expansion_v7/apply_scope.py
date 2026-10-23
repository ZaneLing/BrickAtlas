"""Remove user-excluded conditions from active exports; retain an audit archive.

No source geometry, remaining task state or reference action is changed. Legacy
S/D/M raw banks stay historical; the shared manifest and runner gates set scope.
"""
from collections import Counter
import hashlib
import json
from expansion_v7 import ROOT,OUT
from expansion_v7.build import read,write,digest
from expansion_v7.scope import POLICY,APPROVED,EXCLUDED,DEFERRED,allowed,exclusion_reason


def main():
    archive=OUT/'excluded-by-user.private.json.gz'
    archived={c['id']:c for c in read(archive)['cases']} if archive.exists() else {}
    index=read(OUT/'index.json');active=[];unchanged={}
    for meta in index['models']:
        folder=OUT/'models'/meta['id'];path=folder/'cases.private.json.gz';cases=read(path)
        kept=[]
        for c in cases:
            if not allowed(c):archived[c['id']]=c
            else:kept.append(c);unchanged[c['id']]=digest(c)
        write(path,kept);active+=kept
        admission=read(folder/'admission.json');admission.update(cases=len(kept),scopePolicy=POLICY)
        admission['feasibleCheckpoints']={k:v for k,v in admission['feasibleCheckpoints'].items() if 'cascade' not in k}
        admission['rejected']=[r for r in admission['rejected'] if 'cascade' not in r.get('family','')]
        write(folder/'admission.json',admission)
    write(archive,dict(policy=POLICY,reason='User excluded H12',cases=list(archived.values()),notForEvaluation=True))
    ids={c['id'] for c in active};index['cases']=[c for c in index['cases'] if c['id'] in ids]
    index.update(counts=dict(Counter(c['family'] for c in active)),scopePolicy=POLICY)
    write(OUT/'index.json',index)
    gallery=read(OUT/'gallery.json')
    for m in gallery:m['cases']=[c for c in m['cases'] if c['id'] in ids]
    write(OUT/'gallery.json',gallery)
    (OUT/'gallery-data.js').write_text('window.EXPANSION='+json.dumps(gallery,ensure_ascii=False)+';\n')
    visual=read(OUT/'visibility.json');visual['rows']=[r for r in visual['rows'] if r['caseId'] in ids]
    visual.update(events=len(visual['rows']),passed=sum(r['passed'] for r in visual['rows']),scopePolicy=POLICY)
    write(OUT/'visibility.json',visual)
    diff=read(OUT/'difficulty.json');diff['cases']=[r for r in diff['cases'] if r['caseId'] in ids]
    diff.update(processGroups=dict(Counter(r['processLength'] for r in diff['cases'])),
                structuralGroups=dict(Counter(r['structuralGroup'] for r in diff['cases'])),scopePolicy=POLICY)
    write(OUT/'difficulty.json',diff)
    parent=OUT/'validation-before-scope.json'
    if not parent.exists():parent.write_bytes((OUT/'validation.json').read_bytes())
    validation=read(parent)
    counts=Counter(c['module'] for c in active)
    for row in validation['rows']:row['cases']=counts[row['module']]
    validation.update(cases=len(active),scopePolicy=POLICY,certificationMethod='Unchanged certified subset of prior independently replayed bank',
        parentValidationSha256=hashlib.sha256(parent.read_bytes()).hexdigest(),retainedCaseDigests=unchanged)
    write(OUT/'validation.json',validation)
    historical=read(ROOT/'deliverables/brickplan-dynamic-v6/cases.private.json')['cases']
    excluded_d=[dict(id=c['id'],reason=exclusion_reason(c)) for c in historical if not allowed(c)]
    report=dict(policy=POLICY,approvedHumanErrorIds=APPROVED,excludedHumanErrorIds=EXCLUDED,deferredHumanErrorIds=DEFERRED,
        extensionHistoricalConditions=len(active)+len(archived),extensionActiveConditions=len(active),extensionExcludedConditions=len(archived),
        legacyDynamicHistoricalCases=len(historical),legacyDynamicActiveCases=len(historical)-len(excluded_d),
        legacyDynamicExcludedCases=excluded_d,normalControlsRetainedIndependentlyOfH18=True,
        dynamicRemainingInventoryNotImplemented=True,retainedStatesAndGTUnchanged=True,apiModelCalls=0)
    write(OUT/'human-error-scope.json',report)
    manifest=ROOT/'deliverables/brickplan-dynamic-v6/source-manifest.json'
    previous=read(manifest)
    for name in ('episode.py','human_server.py','test_contracts.py'):
        key='benchmark/brickplan-repair/dynamic_v6/'+name
        previous['files'][key]=hashlib.sha256((ROOT/key).read_bytes()).hexdigest()
    key='benchmark/brickplan-repair/expansion_v7/scope.py';previous['files'][key]=hashlib.sha256((ROOT/key).read_bytes()).hexdigest()
    write(manifest,previous)
    print('SCOPE',len(active),'active extension conditions;',len(excluded_d),'legacy dynamic cases excluded',flush=True)


if __name__=='__main__':main()
