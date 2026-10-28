"""Replay revised references through the real runner; independently check Q003."""
from pathlib import Path
from bench_design.session import Session,internal_action
from bench_design.reference_revisions import PATH
from bench_design.challenges import QUALITY
from bench_design.independent_geometry import check
from expansion_v7.build import read,write
from expansion_v7.runtime import prune_roundtrips

Q003='E7:v7::v7-long-bookshelf::static::buried-repair::t7'


def main():
    results=[];q003=None
    for n,row in enumerate(read(PATH)['revisions']):
        cid=row['caseId'];s=Session.open(cid,Path('/tmp/brick-reference-revision-check')/str(n),diagnostic=True);s.autosave=False
        actions=s.row['case']['referenceActions'];initial=dict(s.ep.state);independent=[]
        if cid==Q003:
            assert len(actions)==8 and not {'P001','P002'}&{a['actor'] for a in actions}
            shortened,audit=prune_roundtrips(s.ep.runtime,initial,actions)
            assert shortened==actions and not audit['removedRoundtripActors']
        for action in actions:
            if cid==Q003:
                _,v=s.ep.runtime.check(s.ep.state,action['actor'],action['type'],candidate=action.get('candidate'))
                evidence=check(s.ep.runtime,s.ep.state,action,v)
                assert evidence['status']=='agrees-on-accepted-geometry'
                independent.append(dict(action=action,evidence=evidence))
            assert s.submit(internal_action(s.ep,action))['code']=='OK',cid
            if cid==Q003:
                assert all(s.ep.state[a]==initial[a] for a in ('P001','P002'))
        s.submit(dict(type='finish'));result=s.result()
        assert result['success'] and len(s.events)==len(s.row['case']['events']),cid
        assert result['executionMetrics']['movesRelativeToWitness']==1.,cid
        results.append(dict(caseId=cid,moves=len(actions),events=len(s.events),success=True,track=s.row['evaluationMetadata']['track']))
        if cid==Q003:
            q003=dict(status='PASS',caseId=cid,oldMoves=10,newMoves=8,removedRoundtripActor='P002',
                leftColumnNeverChanged=True,noFurtherRemovableRoundtrip=True,independentChecks=independent,
                globalShortestClaim=False,referenceOrderRequired=False,apiCalls=0)
        print('PASS',n+1,cid,len(actions),flush=True)
    assert q003
    write(QUALITY/'q003-reference-correction-check.json',q003)
    write(QUALITY/'reference-revision-replay-check.json',dict(status='PASS',runs=results,apiCalls=0))


if __name__=='__main__':main()
