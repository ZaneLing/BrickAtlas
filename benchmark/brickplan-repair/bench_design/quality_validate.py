"""Replay every new condition through the actual unified judge and event logger."""
from collections import Counter
from bench_design.challenges import QUALITY
from bench_design.catalogue import module_runtime
from bench_design.session import Session,internal_action
from expansion_v7.build import read,write


def main():
    rows=[];failures=[]
    for item in read(QUALITY/'challenges.private.json.gz')['cases']:
        session=Session.open(item['id'],QUALITY/'targeted-replay'/item['conditionSha256'][:16],
                             actor='scripted:targeted-replay')
        session.ep.runtime.q=module_runtime('E7',item['model']).q
        try:
            for action in item['case']['referenceActions']:
                feedback=session.submit(internal_action(session.ep,action))
                assert feedback['code']=='OK',feedback
            session.submit({'type':'finish'});result=session.result()
            assert result['success'],'Not complete'
            assert result['scheduledEvents']==result['appliedEvents'],'Partial trigger'
            assert result['effectiveIncidentVerified'],'An incident helped or had no verified harmful/access effect'
            assert len(result['eventWindows'])==result['appliedEvents'],'Missing window'
            if item['category'] in ('repair-overlap','buried-overlap'):
                assert result['eventWindows'][0]['observedRecovery'] is False
            rows.append(dict(id=item['id'],category=item['category'],model=item['model'],
                success=True,events=result['appliedEvents'],windowRecovery=[w['observedRecovery'] for w in result['eventWindows']],
                effectiveIncidents=result['effectiveIncidentVerified']))
            print('JUDGE PASS',len(rows),item['model'],item['category'],flush=True)
        except (AssertionError,ValueError) as exc:
            failures.append(dict(id=item['id'],reason=str(exc),result=session.result()))
            print('JUDGE NEEDS FIX',item['id'],str(exc),flush=True)
    write(QUALITY/'targeted-judge-check.json',dict(status='PASS' if not failures else 'NEEDS_FIX',
        conditions=len(rows)+len(failures),passed=len(rows),events=sum(r['events'] for r in rows),
        categories=dict(Counter(r['category'] for r in rows)),rows=rows,failures=failures,
        apiCalls=0,humanSubmissions=0,scope='Actual Session execution and normalized event windows; written privileged witnesses, not model performance.'))
    assert not failures,[(x['id'],x['reason']) for x in failures]


if __name__=='__main__':main()
