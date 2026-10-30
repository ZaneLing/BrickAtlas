"""Targeted recheck of community cases affected by canonical 3023b symmetry."""
import gzip,json,time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
from dynamic_arena import ROOT
from unified_agent import OUT
from dynamic_arena.transport import write_json


def one(number):
    from expansion_v7.runtime import Episode,public_action
    from bench_design.source_expansion import guard_incidents
    folder=ROOT/'deliverables/brick-atlas-dataset-v1/private'/number
    cert=json.load(gzip.open(folder/'certificate.private.json.gz'));results=[]
    cases=json.load(gzip.open(folder/'cases.private.json.gz'))
    for case in cases:
        if case['mode']!='dynamic' or not any(e.get('family')=='rotated' for e in case.get('events',[])):continue
        ep=Episode(cert,case,41);guard_incidents(ep.runtime);codes=[]
        try:
            for action in case['referenceActions']:
                ep.step(public_action(ep,action));codes.append(ep.feedback['code'])
            ep.step(dict(type='finish'))
            passed=all(c=='OK' for c in codes) and ep.score()['success'] and len(ep.events)==len(ep.schedule)
            results.append(dict(caseId=case['id'],passed=passed,applied=len(ep.events),scheduled=len(ep.schedule),codes=codes))
        except Exception as exc:results.append(dict(caseId=case['id'],passed=False,error=repr(exc)))
    return results


def main():
    previous=json.loads((OUT/'checks/symmetry-scope-audit.json').read_text());rows=[];start=time.time()
    with ProcessPoolExecutor(max_workers=3) as pool:
        for future in as_completed([pool.submit(one,m) for m in previous['models']]):
            rows.extend(future.result())
    write_json(OUT/'checks/symmetry-dynamic-replay.json',dict(apiCalls=0,cases=len(rows),passed=all(r['passed'] for r in rows),
        elapsedSeconds=time.time()-start,runs=rows,scope='All community rotation-event reference traces in models containing 3023b; no model or human capability claim'))
    print(json.dumps(dict(cases=len(rows),failures=[r for r in rows if not r['passed']]),ensure_ascii=False))


if __name__=='__main__':main()
