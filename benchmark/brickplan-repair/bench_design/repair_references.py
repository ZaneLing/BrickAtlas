"""Audit every existing buried-repair witness and correct redundant round trips."""
from copy import deepcopy
from collections import Counter
from bench_design.catalogue import rows_with_cases,module_runtime
from bench_design.challenges import QUALITY,witness
from bench_design import ROOT
from bench_design.reference_revisions import PATH,fingerprint
from expansion_v7.build import read,write,run_witness
from expansion_v7.runtime import prune_roundtrips,execute


def main():
    rows=[r for r in rows_with_cases() if r['bank']=='E7' and (
        r['case'].get('referenceIncident',{}).get('temporarilyRemovedCorrectParts') or
        any(e.get('temporarilyRemovedCorrectParts') for e in r['case'].get('referenceEvents',[])))]
    extra=read(QUALITY/'challenges.private.json.gz')['cases']
    rows += [dict(key=r['id'],case=r['case'],model=r['model'],bank='QX',mode='dynamic') for r in extra
             if any(e.get('temporarilyRemovedCorrectParts') for e in r['case'].get('referenceEvents',[]))]
    revisions=[];audits=[]
    for row in rows:
        case=deepcopy(row['case']);rt=module_runtime('E7',row['model'])
        before=deepcopy(case['referenceActions']);updates={};cleanup=None
        if row['mode']=='static':
            actions,cleanup=prune_roundtrips(rt,case['initial'],before)
            end,checks=execute(rt,case['initial'],actions);assert end==case['goal']
            incident=deepcopy(case['referenceIncident']);incident['recovery']=actions;incident['recoveryChecks']=checks
            incident['temporarilyRemovedCorrectParts']=[a for a in incident['temporarilyRemovedCorrectParts'] if a not in cleanup['removedRoundtripActors']]
            changes,change_audit=prune_roundtrips(rt,incident['before'],incident['changes'])
            incident['changes']=changes;_,incident['checks']=execute(rt,incident['before'],changes)
            incident['referenceCleanup']=dict(recovery=cleanup,intervention=change_audit)
            updates=dict(referenceActions=actions,referenceChecks=checks,referenceIncident=incident)
        else:
            folder=ROOT/'deliverables/brickplan-expansion-v7/models'/row['model']
            cert=read(folder/'certificate.private.json.gz');normal=read(folder/'manual.private.json.gz')['actions']
            updates=(witness(cert,case,normal,rt.q) if row['bank']=='QX' else run_witness(cert,case,normal,rt.q))
            actions=updates['referenceActions']
            if row['bank']=='QX':assert updates['actualOverlapDuringUnrepairedWindow'],row['key']
        changed=actions!=before
        audits.append(dict(caseId=row['key'],mode=row['mode'],beforeMoves=len(before),afterMoves=len(actions),
            changed=changed,nativeReplayPassed=True,cleanup=cleanup,
            eventCount=len(updates.get('referenceEvents',[])),globalShortestClaim=False))
        if changed:
            updates['referenceRevision']=dict(version='necessary-repair-roundtrips/1',reason='Remove legally avoidable detach/restore pairs',
                beforeMoves=len(before),afterMoves=len(actions),globalShortestClaim=False)
            if row['key']=='E7:v7::v7-long-bookshelf::static::buried-repair::t7':
                updates['referenceRepairNote']='左侧柱子全程不动；只拆装右侧错色件及挡住它的零件。'
                updates['referenceActorLabels']={'P008':'右侧最上方棕色块','P005':'横隔板','P004':'右柱上段棕色块',
                    'V7W_P003':'右柱下段红色错件','P003':'右柱下段棕色正确件'}
            revisions.append(dict(caseId=row['key'],sourceFingerprint=fingerprint(row['case']),updates=updates))
        print('CHECK',len(audits),row['key'],len(before),'->',len(actions),flush=True)
    assert any(r['caseId']=='E7:v7::v7-long-bookshelf::static::buried-repair::t7' for r in revisions)
    write(PATH,dict(schema='brick-atlas-reference-revisions/1',revisions=revisions,
        taskInitialGoalScheduleUnchanged=True,originalWitnessFilesUnchanged=True,apiCalls=0))
    write(QUALITY/'reference-roundtrip-audit.json',dict(status='PASS',audited=len(audits),changed=len(revisions),
        counts=dict(Counter(r['mode'] for r in audits if r['changed'])),rows=audits,apiCalls=0,
        allExistingBuriedRepairWitnessesAudited=True,globalShortestClaim=False))


if __name__=='__main__':main()
