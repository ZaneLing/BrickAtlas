"""All active dynamic task IDs share the pull-observation Arena entry point."""
from collections import Counter
import json
from dynamic_arena import ROOT, OUT
from bench_design import OUT as SPEC
from bench_design.selection import retired
from expansion_v7.build import read,write


def build():
    rows=[]
    for line in (SPEC/'questions.jsonl').read_text().splitlines():
        r=json.loads(line)
        if r['mode']=='dynamic':rows.append(dict(caseId=r['id'],model=r['model'],title=r.get('title',r['model']),track=r['track'],source=r.get('source'),taskType=r['taskType'],family=r.get('family'),canonicalId=r['canonicalId'],difficulty=r.get('difficulty',r.get('planningLevel')),origin='published'))
    quality=ROOT/'deliverables/brickplan-quality-round'
    for r in read(quality/'challenge-catalogue.json')['cases']:
        meta=r['evaluationMetadata'];rows.append(dict(caseId=r['id'],model=r['model'],title=r.get('title',r.get('description',r['model'])),track=meta['track'],source=meta.get('source'),taskType=meta['taskType'],family=r.get('family',r.get('category')),canonicalId=r['id'],origin='review-extension'))
    for r in read(quality/'source-expansion/index.json')['cases']:
        if r['mode']=='dynamic':rows.append(dict(caseId=r['id'],model=r['model'],title=r['title'],track='named-module-dynamic',source='set:'+next(m['sourceSetId'].split('-')[0] for m in read(quality/'source-expansion/index.json')['models'] if m['id']==r['model']),taskType='D0' if r['family']=='control' else 'D1',family=r['family'],canonicalId=r['id'],origin='review-extension'))
    for r in read(quality/'inventory-equivalence/index.json')['cases']:
        if r['mode']=='dynamic':rows.append(dict(caseId=r['id'],model=r['model'],title=r['title'],track='inventory-equivalent-dynamic',source='original:inventory:'+r['axis'],taskType='D3',family='inventory-shortage',canonicalId=r['id'],origin='review-extension'))
    if (OUT/'new-objects/index.json').exists():
        for m in read(OUT/'new-objects/index.json')['models']:
            for c in read(OUT/'new-objects'/m['id']/'cases.private.json.gz'):
                if c['mode']!='dynamic':continue
                rows.append(dict(caseId=c['id'],model=m['id'],title=m['title'],track='whole-object-dynamic',source='set:'+m['setNumber'].split('-')[0],taskType='D0' if not c['events'] else 'D1',family=c['family'],canonicalId=c['id'],origin='new-source-machine-checked'))
    rows=[r for r in rows if not retired(r['caseId'],r['model'],r.get('source'))]
    assert len(rows)==len({r['caseId'] for r in rows})
    new_sets={'set:'+m['setNumber'].split('-')[0] for m in read(OUT/'source-library.json')['models'] if m.get('addedAfterFigureCuration')}
    for r in rows:
        r['addedAfterFigureCuration']=r.get('source') in new_sets
        r.update(arenaProtocol='brick-atlas-tool-arena/3',normalBranch=dict(caseId=r['caseId'],control=True),incidentBranch=None if r['taskType']=='D0' else dict(caseId=r['caseId'],control=False),diagnostic=r['track'] in ('archived-crop-dynamic','dynamic-structure-diagnostic'),normalPrerequisite='same-case, same-model successful no-event run required',humanQualified=False)
    out=dict(schema='brick-atlas-arena-catalogue/1',totalDynamic=len(rows),distinctTasks=len({r['canonicalId'] for r in rows}),models=len({r['model'] for r in rows}),byTrack=dict(Counter(r['track'] for r in rows)),byType=dict(Counter(r['taskType'] for r in rows)),cases=rows,entryPoint='python -m dynamic_arena.run --id CASE --model PROVIDER_MODEL --condition pair',apiCalls=0)
    write(OUT/'catalogue.json',out);print(json.dumps({k:v for k,v in out.items() if k!='cases'},ensure_ascii=False));return out


def entry(cid):
    return next(r for r in read(OUT/'catalogue.json')['cases'] if r['caseId']==cid)


if __name__=='__main__':build()
