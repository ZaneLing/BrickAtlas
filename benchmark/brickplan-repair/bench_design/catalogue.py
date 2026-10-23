"""A new authoritative view; historical case files and paired controls remain intact."""
from collections import Counter,defaultdict
from functools import lru_cache
import csv
import hashlib
import json
import numpy as np
from bench_design import ROOT,OUT
from bench_design.policy import tags,descriptors,INPUT_VERSION
from question_showcase import dataset
from expansion_v7.build import read,write,digest
from expansion_v7.runtime import runtime
from expansion_v7.scope import allowed
from community_modules.core import ModuleAssembly,render_certificate
from plate5_eval import load as load_static


def rows_with_cases():
    rows,_,_=dataset()
    for meta in read(ROOT/'deliverables/brickplan-recognizable-models/admission-screen.json')['admitted']:
        folder=ROOT/'deliverables/brickplan-recognizable-models/models'/meta['id']
        for c in read(folder/'cases.private.json.gz'):
            incident=c.get('referenceIncident') or {}
            events=c.get('referenceEvents') or []
            profile=dict(targetParts=sum(bool(k) for k in c['goal'].values()),
                witnessRepairMoves=max((len(e['recovery']) for e in events),default=len(incident.get('recovery',[]))),
                witnessCoverRemovals=max((len(e.get('temporarilyRemovedCorrectParts',[])) for e in events),default=0),
                scheduledEvents=len(c['events']),source='set:'+c['sourceSetId'].split('-')[0],split='development-public')
            rows.append(dict(key='O:'+c['id'],bank='O',case=c,mode=c['mode'],family=c['family'],
                model=meta['id'],title=meta['title'],profile=profile,level=None,visibility=None))
    return rows


@lru_cache(maxsize=128)
def module_runtime(bank,mid):
    names={'M':'brickplan-community-modules','E7':'brickplan-expansion-v7','O':'brickplan-recognizable-models/models'}
    folder=ROOT/'deliverables'/names[bank]
    if bank=='E7':folder=folder/'models'
    path=folder/mid/('certificate.private.json' if bank=='M' else 'certificate.private.json.gz')
    cert=read(path)
    return ModuleAssembly(cert) if bank=='M' else runtime(cert)


def state_key(rt,state):return sorted((repr(k),v) for k,v in rt.signature(state).items())


def static_error_tags(rt,c):
    """Resolve replacement/compound labels from qualified physical candidates.

    First cancel all physically correct placements, regardless of actor ID.
    A wrong-color/type/pose replacement is not also called a missing brick.
    """
    remaining=rt.signature(c['goal']).copy();bad=[]
    for actor,key in c['initial'].items():
        if not key:continue
        sig=next(iter(rt.signature({actor:key})))
        if remaining[sig]:remaining[sig]-=1
        else:bad.append(rt.row(key)['kind'])
    mapping={'wrong_color':'E03','wrong_type':'E04','wrong_size':'E04','offset':'E05',
        'height_layer':'E05','rotation':'E06','swapped_positions':'E07','swap':'E07',
        'extra':'E02','goal':'E02'}
    assert not set(bad)-set(mapping),set(bad)-set(mapping)
    codes={mapping[k] for k in bad};extra=sum(mapping[k]=='E02' for k in bad)
    replacements=len(bad)-extra;missing=max(0,sum(remaining.values())-replacements)
    if missing:codes.add('E01')
    return sorted(codes) or ['OK'],missing+extra+replacements


def task_key(row):
    """Conservative de-duplication within one source/configuration/task contract.

    Historical M/E7 cross-adapter aliases were already removed by global-splits.
    Preserve all execution conditions for prefix-matched pairing.
    """
    c=row['case'];bank=row['bank'];mid=row['model']
    if bank=='D':
        # Empty-to-whole normal runs are identical despite pairedGroup/trigger labels.
        value=['normal-control'] if row['family']=='none' else [c['kind'],c['trigger'],c.get('privateEvent')]
        return digest([bank,mid,row['mode'],value])
    rt=load_static(c['publicId'])[0] if bank=='S' else module_runtime(bank,mid)
    events=c.get('events',[]) or ([c['event']] if c.get('event') else [])
    return digest([bank,mid,row['mode'],state_key(rt,c['initial']),state_key(rt,c['goal']),events])


def track(row,crops):
    bank,mid,mode=row['bank'],row['model'],row['mode']
    if bank=='S' or mid in crops:return 'static-structure-diagnostic' if mode=='static' else 'archived-crop-dynamic'
    if bank=='D' and not mid.startswith('obj-'):return 'dynamic-structure-diagnostic'
    if bank=='D' or bank=='O' or mid.startswith('v7-long-'):
        return 'whole-object-'+mode
    return 'named-module-'+mode


def main():
    OUT.mkdir(parents=True,exist_ok=True);rows=rows_with_cases()
    policy=read(ROOT/'benchmark/brickplan-repair/recognizable_models/selection-policy.json')
    crops=set(policy['unreviewedSpatialCrops'])
    public_sources={read(p)['profile']['source'] for p in (ROOT/'deliverables/brickplan-question-showcase/examples').glob('Q*.json')}
    public_sources.update(r['profile']['source'] for r in rows if r['bank'] in ('M','O'))
    inherited=read(ROOT/'deliverables/brickplan-expansion-v7/global-splits.json')['sources']
    dv={r['caseId']:r for r in read(ROOT/'deliverables/brickplan-dynamic-v6/audit.json')['rows']}
    ev={r['caseId']:r for r in read(ROOT/'deliverables/brickplan-expansion-v7/difficulty.json')['cases']}
    ov={r['id']:r['status'] for r in read(OUT/'new-object-visibility.json')['rows']} if (OUT/'new-object-visibility.json').exists() else {}
    seen={};catalogue=[];aliases=[];issues=[]
    for row in rows:
        c=row['case'];bank=row['bank'];mid=row['model'];p=row['profile'];mode=row['mode']
        assert allowed(c),row['key']
        scope=track(row,crops);codes,name=tags(row['family']);events=int(p.get('scheduledEvents',0))
        parts=(p.get('activeParts') or p.get('moduleParts') or p['targetParts'])
        if bank=='M':parts=len(module_runtime(bank,mid).cert['source']['moduleSourceIndices'])
        if bank=='S':parts=sum(bool(k) for k in c['goal'].values())
        moves=p.get('witnessRepairMoves');covers=p.get('witnessCorrectCoverRemovals',p.get('witnessCoverRemovals',0))
        vis=('control' if row['family'] in ('none','control') else
            dv[c['id']]['temporalClass'] if bank=='D' else
            ('machine-visible' if ev[c['id']]['machineVisible'] else 'low-visibility') if bank=='E7' else 'not-rechecked-on-current-interface')
        legacy_vis=vis
        if bank=='O':vis=ov.get(row['key'],'not-rechecked-on-current-interface')
        if bank=='E7' and scope.startswith('named-module') and vis!='control':vis='current-full-context-review-pending'
        source=p['source'];split='development-public' if source in public_sources else inherited.get(source,'development-public')
        key=task_key(row);canonical=seen.setdefault(key,row['key'])
        if canonical!=row['key']:aliases.append(dict(id=row['key'],canonicalId=canonical,reason='Same task state/goal or identical normal control; physical equivalence ignores interchangeable actor IDs.'))
        if mode=='static':
            rt=load_static(c['publicId'])[0] if bank=='S' else module_runtime(bank,mid)
            if row['family'] not in ('none','control') and rt.signature(c['initial'])==rt.signature(c['goal']):
                issues.append(dict(id=row['key'],reason='Labelled error is physically equivalent to target'))
            if bank=='S':
                codes,fault_units=static_error_tags(rt,c)
                names={'E01':'少件','E02':'多件','E03':'错色','E04':'错零件','E05':'位置／高度偏移','E06':'方向错误','E07':'位置互换','OK':'正常验收'}
                name='＋'.join(names[k] for k in codes)
            else:fault_units=None
        else:fault_units=None
        kind=('S0' if mode=='static' and codes==['OK'] else 'S1' if mode=='static' else
              'D0' if codes==['OK'] else 'D2' if events>=2 else 'D1')
        process_tags=[]
        if row['family'] in ('early-cover','early_cover'):process_tags.append('P01')
        if row['family'] in ('buried-repair','buried_wrong_color'):process_tags.append('P02')
        if events>=2:process_tags.append('P03')
        if row['family'] in ('compound','compound_fault') and (fault_units is None or fault_units>=2 or len(codes)>=2):process_tags.append('simultaneous-errors')
        if row['family']=='repeat-omission':process_tags.append('repeat-count-omission')
        candidate=scope not in ('archived-crop-dynamic','dynamic-structure-diagnostic')
        record=dict(id=row['key'],canonicalId=canonical,isAlias=canonical!=row['key'],
            bank=bank,model=mid,title=row['title'],source=source,mode=mode,taskType=kind,track=scope,
            family=row['family'],errorCodes=codes,processTags=process_tags,errorName=name,legacyLevel=row['level'],
            errorLabelBasis='qualified-candidate-kinds-after-physical-matching' if bank=='S' else 'source-event-design',
            **descriptors(parts,moves,covers,events,row['family'],mode,p['targetParts']),
            visibility=vis,legacyVisibility=legacy_vis,inputVersion=INPUT_VERSION,modelInput='vision-with-neutral-text-and-anonymous-action-handles',
            mainTaskCandidate=candidate,formalPerceptionClaimEligible=False,
            currentInterfaceHumanValidated=False,sourceSplit=split,legacySplit=p.get('split'),
            splitReason='Shown illustrative source; all variants assigned to development' if source in public_sources else 'Inherited source grouping',
            referenceOrderRequired=False,finalTargetParts=p['targetParts'])
        catalogue.append(record)
    unique=[r for r in catalogue if not r['isAlias']]
    by_source=defaultdict(set)
    for r in catalogue:by_source[r['source']].add(r['sourceSplit'])
    assert all(len(s)==1 for s in by_source.values())
    assert not issues,issues
    with (OUT/'questions.jsonl').open('w') as f:
        for r in catalogue:f.write(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n')
    with (OUT/'questions.csv').open('w',newline='') as f:
        fields=['id','canonicalId','isAlias','bank','model','source','mode','taskType','track','family','errorCodes','processTags','errorName','planningLevel','buildLength','rework','eventLevel','gradingParts','lengthBasis','visibility','sourceSplit','mainTaskCandidate']
        w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(catalogue)
    models={}
    for r in catalogue:
        k=(r['bank'],r['model']);models.setdefault(k,dict(bank=r['bank'],id=r['model'],title=r['title'],track=r['track'],conditions=0,distinctTasks=0))
        models[k]['conditions']+=1;models[k]['distinctTasks']+=not r['isAlias']
    write(OUT/'models.json',list(models.values()))
    write(OUT/'duplicates.json',dict(withinBankAliases=aliases,
        historicalCrossAdapterAliases=read(ROOT/'deliverables/brickplan-expansion-v7/global-splits.json')['adapterAliases'],
        scope='Conservative source/configuration/contract de-duplication. Different sensor, action or event-policy conditions remain recorded.'))
    summary=dict(schema='brick-atlas-organized-benchmark/1',rawRetainedConditions=len(catalogue),
        historicalCatalogueRecords=5793,newWholeObjectConditions=46,
        distinctTaskRecords=len(unique),withinBankAliasRecords=len(aliases),historicalCrossAdapterAliases=83,
        perBank=dict(Counter(r['bank'] for r in unique)),perTrack=dict(Counter(r['track'] for r in unique)),
        perTaskType=dict(Counter(r['taskType'] for r in unique)),
        structuralBuildLength=dict(Counter(r['buildLength'] for r in unique)),
        planningLevels=dict(Counter(r['planningLevel'] for r in unique)),
        structuralRework=dict(Counter(r['rework'] for r in unique)),eventLevels=dict(Counter(r['eventLevel'] for r in unique)),
        sourceGroups=len(by_source),sourcesCrossingSplits=0,splitCounts=dict(Counter(r['sourceSplit'] for r in unique)),
        promotedPublicSources=len(public_sources),
        atomicErrorClasses=7,approvedHumanErrorCategories=12,humanCaseValidationPending=True,
        forbiddenHumanCategoriesPresent=0,labelledStaticErrorsEquivalentToGoal=0,
        mainTaskCandidates=sum(r['mainTaskCandidate'] for r in unique),
        pendingImageAndHumanReview=True,apiCalls=0)
    write(OUT/'summary.json',summary)
    write(OUT/'classification-audit.json',dict(status='PASS',rows=len(catalogue),
        uniqueIds=len({r['id'] for r in catalogue}),allFamiliesClassified=True,
        referenceTargetsChecked=True,falseStaticErrors=issues,sourceSplitLeakage=0,
        note='Does not claim that every input image has been reviewed by a human.'))
    print('ORGANIZED',json.dumps(summary,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
