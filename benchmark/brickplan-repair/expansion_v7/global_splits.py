"""One source allocation across S, D, M and the additive extension.

Historical splits/results are preserved. This is a new experiment manifest, not
a relabeling of previously measured test results.
"""
from collections import Counter,defaultdict
from copy import deepcopy
import csv
import hashlib
import json
import re
from expansion_v7 import ROOT,OUT
from expansion_v7.build import read,write,signature_key,digest
from expansion_v7.runtime import runtime
from community_modules.core import ModuleAssembly
from dynamic_v6.object_models import OBJECTS

FAMILIES={'storage-long':'storage','road-vehicle-long':'road-vehicles',
          'span-long':'spans','industrial-frame-long':'frame-machines','building-long':'buildings'}


def group(model,source=None):
    if model in OBJECTS:return 'procedural-family:'+OBJECTS[model]['family']
    if source and source.get('kind')=='stylized-complete-object':
        return 'procedural-family:'+FAMILIES.get(source['modelId'],source['modelId'])
    value=re.sub(r'^(v7-omr-|v23-|omr-|new-)','',model)
    match=re.match(r'(\d{3,6})(?:\D|$)',value)
    if match:return 'set:'+match.group(1)
    if source and source.get('kind')=='procedural-mechanism':
        return 'mechanism-family:'+source['modelId']
    return 'source:'+model.split('--')[0]


def fingerprint(rt,case):
    return digest([signature_key(rt,case),sorted(rt.cert['source'].get('moduleSourceIndices',[]))])


def main():
    records=[];baseline={};counts=Counter();public_groups=set()
    s_path=ROOT/'deliverables/brickplan-static-plate5/cases.jsonl'
    for line in s_path.read_text().splitlines():
        c=json.loads(line);records.append(dict(id='S:'+c['id'],track='S',source=group(c['modelId']),originalId=c['id']))
    d=read(ROOT/'deliverables/brickplan-dynamic-v6/index.json')
    dcerts={}
    for c in d['cases']:
        mid=c['modelId']
        if mid not in dcerts:
            dcerts[mid]=read(ROOT/'deliverables/brickplan-dynamic-v6/models'/mid/'qualification.json')['source']
        records.append(dict(id='D:'+c['id'],track='D',source=group(mid,dcerts[mid]),originalId=c['id']))
    modules=read(ROOT/'deliverables/brickplan-community-modules/gallery-data.js.json')
    for m in modules:
        folder=ROOT/'deliverables/brickplan-community-modules'/m['id']
        cert=read(folder/'certificate.private.json');rt=ModuleAssembly(cert)
        family=group(cert['source']['modelId']);public_groups.add(family)
        for c in read(folder/'cases.private.json'):
            rid='M:'+c['id'];records.append(dict(id=rid,track='M',source=family,originalId=c['id']))
            converted={**c,'events':[],'referenceEvents':[]}
            if c.get('event'):
                converted['events']=[dict(minimumInstalled=c['event']['minimumInstalled'])]
                converted['referenceEvents']=[c['referenceIncident']]
            baseline[fingerprint(rt,converted)]=rid
    index=read(OUT/'index.json');aliases=[];new_rows=[]
    for meta in index['models']:
        mid=meta['id'];folder=OUT/'models'/mid
        if not (folder/'cases.private.json.gz').exists():continue
        cert=read(folder/'certificate.private.json.gz');rt=runtime(cert)
        family=group(cert['source'].get('modelId',meta['sourceSetId']),cert['source'])
        for c in read(folder/'cases.private.json.gz'):
            matched=baseline.get(fingerprint(rt,c));rid='E7:'+c['id']
            row=dict(id=rid,track=meta['track'],source=family,originalId=c['id'],module=mid)
            if matched:
                aliases.append(dict(**row,samePhysicalTaskAs=matched,reason='Same source, mutable scope, states and reference incident effects; new adapter condition'))
            else:
                records.append(row);new_rows.append(row)
    sources=sorted({r['source'] for r in records})
    # Already shown community objects are development material. New sources
    # were selected before any model execution and are reserved for evaluation.
    new_holdout={'set:10013','set:10015','set:10016'}
    assignments={}
    for source in sources:
        if source in new_holdout:split='test-new-source'
        elif source in public_groups:split='development-public'
        else:
            bucket=int(hashlib.sha256(('brickplan-global-v7:41:'+source).encode()).hexdigest()[:12],16)%100
            split='train' if bucket<70 else 'development' if bucket<85 else 'test-existing-source'
        assignments[source]=split
    for r in records+aliases:r['split']=assignments[r['source']]
    assert len({r['id'] for r in records})==len(records)
    by_source=defaultdict(set)
    for r in records:by_source[r['source']].add(r['split'])
    assert all(len(s)==1 for s in by_source.values())
    write(OUT/'global-splits.json',dict(schema='brickplan-global-source-splits/7',seed=41,
        historicalSplitsModified=False,independenceUnit='Canonical original set; related procedural designs share a design family',
        sources=assignments,cases=records,adapterAliases=aliases,newSourceEvaluation=sorted(new_holdout),
        leakageCheck=dict(status='PASS',sourcesCrossingSplits=0),
        counts=dict(Counter(r['split'] for r in records)),
        baselineCases=5260,newPhysicalTasks=len(new_rows),extensionAdapterConditions=len(index['cases']),
        adapterConditionsReusingBaselineTasks=len(aliases),combinedPhysicalTasks=len(records),
        publicSourcesAreNotUnseen=True,modelEvaluationCount=0,
        limitation='Unseen means held out from project prompt/model tuning, not guaranteed absent from pretraining or public sources.'))
    write(OUT/'release-summary.json',dict(baselineCases=5260,extensionConditions=len(index['cases']),
        newPhysicalTasks=len(new_rows),reusedBaselineTasks=len(aliases),combinedPhysicalTasks=len(records),
        modelConfigurations=len(index['models']),newLongObjects=sum(m['track']=='D-long' for m in index['models']),
        longerCommunityModules=sum(m['track']=='M-long' or (m['track']=='M-new-source' and m['activeParts']>12) for m in index['models']),
        newCommunitySources=sum(m['track']=='M-new-source' for m in index['models']),
        maximumActiveParts=max(m['activeParts'] for m in index['models']),
        multipleIncidentConditions=sum(c['eventCount']>=2 for c in index['cases']),
        threeIncidentConditions=sum(c['eventCount']==3 for c in index['cases']),
        tracks=dict(Counter(r['track'] for r in new_rows)),
        extensionModes=dict(Counter(r['mode'] for r in index['cases'])),
        newPhysicalModes=dict(Counter(next(c['mode'] for c in index['cases'] if c['id']==r['originalId']) for r in new_rows)),
        apiModelCalls=0,humanValidationCount=0,difficultyEmpiricallyValidated=False))
    with (OUT/'global-splits.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['id','track','source','split','originalId'],extrasaction='ignore',lineterminator='\n')
        writer.writeheader();writer.writerows(records)
    print('GLOBAL',len(records),'physical tasks',len(new_rows),'new',len(aliases),'adapter aliases',len(sources),'sources',flush=True)


if __name__=='__main__':main()
