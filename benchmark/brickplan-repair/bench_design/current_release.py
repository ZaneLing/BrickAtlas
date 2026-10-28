"""Export the active selection and explicit pending additions, without rewriting archives."""
from collections import Counter
import hashlib,json
from bench_design import ROOT,OUT as SPEC
from bench_design.challenges import QUALITY
from bench_design.selection import retired,RETIRED_MODELS
from bench_design.inventory_tasks import index as inventory_index,source_row as inventory_row
from bench_design.source_expansion import index as source_index,source_row
from bench_design.reference_revisions import revisions
from bench_design.policy import tags,descriptors
from expansion_v7.build import read,write

OUT=QUALITY/'current-release'


def main():
    archived=list(map(json.loads,(SPEC/'questions.jsonl').read_text().splitlines()))
    active=[r for r in archived if not retired(r['id'],r['model'],r['source'])]
    removed=[r for r in archived if retired(r['id'],r['model'],r['source'])]
    corrections=revisions()
    for row in active:
        correction=corrections.get(row['id'])
        if correction:
            u=correction['updates'];events=u.get('referenceEvents',[]);incident=u.get('referenceIncident',{})
            row['referenceRepairMoves']=max((len(e['recovery']) for e in events),default=len(u['referenceActions']))
            row['referenceCorrectCoverRemovals']=max((len(e.get('temporarilyRemovedCorrectParts',[])) for e in events),default=len(incident.get('temporarilyRemovedCorrectParts',[])))
            row['referenceTotalMoves']=len(u['referenceActions']);row['referenceRevision']=u['referenceRevision']
    appended=[]
    for bank,rows,getrow in [('QN',source_index()['cases'],source_row),('QI',inventory_index()['cases'],inventory_row)]:
        for item in rows:
            row=getrow(item['id']);m=row['evaluationMetadata'];case=row['case']
            appended.append(dict(id=row['key'],canonicalId=row['key'],isAlias=False,bank=bank,model=row['model'],
                title=row['title'],source=m['source'],mode=row['mode'],taskType=m['taskType'],track=m['track'],
                family=row['family'],mainTaskCandidate=False,currentInterfaceHumanValidated=False,
                qualification='pending-human-review',sourceSplit='development-public',
                targetContract=case.get('targetContract','exact-physical-parts-and-poses'),referenceOrderRequired=False))
            codes,name=tags(row['family']);appended[-1].update(errorCodes=codes,errorName=name,
                difficultyStatus='STRUCTURAL_DESCRIPTORS_ONLY',empiricalDifficulty=None,
                referenceTotalMoves=len(case['referenceActions']))
            if bank=='QI':appended[-1].update(capabilityAxis='inventory-feasibility-and-replanning',
                buildLength='B1',planningLevel='G2' if case['family']!='inventory-allocation' else 'G1',
                rework='R2' if case['family']!='inventory-allocation' else 'R0',eventLevel='T'+str(len(case['events'])),
                alternateDecompositionsAccepted=True)
    OUT.mkdir(parents=True,exist_ok=True)
    for name,rows in [('active-questions.jsonl',active),('pending-additions.jsonl',appended)]:
        (OUT/name).write_text(''.join(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n' for r in rows))
    challenges=[r for r in read(QUALITY/'challenges.private.json.gz')['cases'] if not retired(r['id'],r['model'])]
    write(OUT/'selection.json',dict(schema='brick-atlas-current-selection/2026-10-28',
        retiredModels=RETIRED_MODELS,withdrawnArchiveConditions=len(removed),
        withdrawnArchiveDistinctTasks=sum(not r['isAlias'] for r in removed),
        activeArchiveConditions=len(active),activeArchiveDistinctTasks=sum(not r['isAlias'] for r in active),
        activeMainCandidates=sum(r['mainTaskCandidate'] and not r['isAlias'] for r in active),
        activeDiagnosticTasks=sum(not r['mainTaskCandidate'] and not r['isAlias'] for r in active),
        pendingAdditions=dict(Counter(r['bank'] for r in appended)),activeStressChallenges=len(challenges),
        noRetiredTasksInActiveSelection=True,humanReviewStillRequired=True,apiCalls=0,
        referenceCorrectionsApplied=sum(r['id'] in corrections for r in active),
        archive='deliverables/brickplan-benchmark-spec/questions.jsonl',
        archiveSha256=hashlib.sha256((SPEC/'questions.jsonl').read_bytes()).hexdigest(),
        runtimeSelectionCode='benchmark/brickplan-repair/bench_design/selection.py'))
    print(json.dumps(read(OUT/'selection.json'),ensure_ascii=False,indent=2))


if __name__=='__main__':main()
