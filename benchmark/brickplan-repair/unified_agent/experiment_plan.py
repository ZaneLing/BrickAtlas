"""Select distinct objects across error families and length groups, before API calls."""
import hashlib,json,time
from collections import defaultdict,Counter
from unified_agent.experiment_batch import OUT,MODELS
from unified_agent import ROOT
from dynamic_arena.transport import write_json


def main():
    if (OUT/'plan.json').exists():raise ValueError('Do not overwrite a registered experiment plan')
    data=ROOT/'deliverables/brick-atlas-dataset-v1/questions'
    static=[json.loads(l) for l in (data/'static.jsonl').read_text().splitlines()]
    dynamic=[json.loads(l) for l in (data/'dynamic.jsonl').read_text().splitlines()]
    bymodel=defaultdict(list)
    for row in dynamic:
        if row['scheduledEvents']:bymodel[row['model']].append(row)
    old=json.loads((ROOT/'deliverables/brick-atlas-ark-pilot-v1/plan.json').read_text())
    old_models={o['model'] for o in old['objects']}
    families=['missing','wrong-color','offset','buried-repair','repeat-omission','rotated','extra-layer','repeated-step','early-cover','wrong-part','left-right-swap']
    used=set();sources=set();selected=[];family_counts=Counter();dynamic_counts=Counter()
    def tie(row):return hashlib.sha256(('brick-atlas-20261030-v4:'+row['id']).encode()).hexdigest()
    for i in range(50):
        family='control' if i%5==0 else families[(i-i//5-1)%len(families)]
        difficulty=['short','short','medium','medium','long'][i%5]
        eligible=[r for r in static if r['model'] not in used|old_models and r['model'] in bymodel and r['activeParts']<=28
            and not any(name in r['title'].lower() for name in ('museum','louvre','rockefeller'))]
        whole=i in {0,4,8,13,17,22,26,31,35,44}
        row=min(eligible,key=lambda r:(r['track'].startswith('whole')!=whole,r['family']!=family,r['difficulty']!=difficulty,
            r['sourceGroup'] in sources,family_counts[r['family']],tie(r)))
        used.add(row['model']);sources.add(row['sourceGroup']);family_counts[row['family']]+=1
        ds=bymodel[row['model']]
        desired=('multiple' if dynamic_counts['multiple']<6 and (i%5==0 or whole) and any(r['family']=='multiple' for r in ds) else row['family'])
        fault=min(ds,key=lambda r:(r['family']!=desired,dynamic_counts[r['family']],tie(r)))
        dynamic_counts[fault['family']]+=1
        selected.append(dict(index=i+1,static=row,dynamic=fault))
    def job(row,condition,group,index):
        return dict(caseId=row['id'],model=row['model'],title=row['title'],condition=condition,group=group,sampleIndex=index,
            difficulty=row['difficulty'],activeParts=row['activeParts'],family=row['family'],scheduledEvents=row['scheduledEvents'],
            sourceGroup=row['sourceGroup'],track=row['track'])
    common=[]
    for pair in selected:
        common.extend([job(pair['static'],'static','new-sample',pair['index']),job(pair['dynamic'],'normal','new-sample',pair['index'])])
    lookup={r['id']:r for r in static+dynamic}
    supplement={m:[] for m in MODELS}
    for i,obj in enumerate(old['objects']):
        for cid in obj['staticCases']:
            supplement[MODELS[0]].append(job(lookup[cid],'static','previous-missing',i+1))
        supplement[MODELS[0]].append(job(lookup[obj['dynamicCase']],'normal','previous-missing',i+1))
        supplement[MODELS[1]].append(job(lookup[obj['staticCases'][1]],'static','previous-interrupted',i+1))
        supplement[MODELS[1]].append(job(lookup[obj['dynamicCase']],'normal','previous-interrupted',i+1))
    plan=dict(schema='brick-atlas-expanded-experiment/1',createdAt=time.time(),selectionBeforePaidTaskCalls=True,
        countInterpretation='50 static + 50 normal-build tasks per backbone; conditional incidents are additional. Qwen receives the same 100 tasks.',
        repeats=1,models=MODELS,inputVersion='brick-atlas-unified-visual-agent/4',
        modelBudgetCNY=dict(zip(MODELS,[1000,350,150,100])),
        moneyCaution='Sol uses explicitly provisional Ark accounting. These caps are not a guaranteed actual invoice limit.',
        selected=selected,jobs={m:supplement[m]+common for m in MODELS},
        selectedStaticFamilies=dict(family_counts),selectedDynamicFamilies=dict(dynamic_counts),
        selectedLengths=dict(Counter(p['static']['difficulty'] for p in selected)),
        independentObjects=len(used),sourceGroups=len(sources),
        sourceFilesSha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [data/'static.jsonl',data/'dynamic.jsonl']},
        limitations=['Length group is not a validated difficulty scale.','Static uses the shared agent, not one-shot model answering.',
            'The static and dynamic targets may differ; no paired causal static/dynamic gap is claimed.',
            'Normal and incident are independent rollouts. Normal success gates incident execution.',
            'Available static/dynamic shared objects with manuals are sampled; not the full distribution of the dataset.'])
    write_json(OUT/'plan.json',plan)
    print('REGISTERED',len(common),'base tasks/model',len(used),'objects',len(sources),'source groups')
    print('STATIC',dict(family_counts),'DYNAMIC',dict(dynamic_counts),'LENGTH',plan['selectedLengths'])


if __name__=='__main__':main()
