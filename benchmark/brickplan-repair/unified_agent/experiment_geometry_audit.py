"""Look for visually indistinguishable states with different geometric scores.

Uses the existing renderer/checker, so flags need independent review and a pass
does not establish real-world physical validity. No API requests are made.
"""
import gzip,json,tempfile,time
from collections import Counter
from bench_design.session import Session
from dynamic_arena.sensors import Sensors
from dynamic_arena import OUT as ARENA
from dynamic_arena.transport import write_json
from unified_agent.experiment_batch import OUT,merged


def check(run):
    saved=json.loads(gzip.decompress((ARENA/'runs'/run['arenaRunId']/'record.private.json.gz').read_bytes()))
    with tempfile.TemporaryDirectory() as tmp:
        s=Session.open(run['caseId'],tmp,'scripted:visual-consistency',control=run['arenaBranch']=='normal');sensor=Sensors(s)
        matches={v:sensor.render(saved['final'],v).tobytes()==sensor.render(saved['goal'],v).tobytes() for v in ('isometric','rear','top')}
        parts={v:k for k,v in saved['aliasMaps']['parts'].items()};poses={v:k for k,v in saved['aliasMaps']['poses'].items()}
        candidates=[];seen=set()
        attempts=[r for r in saved['records'] if r['action'].get('type')=='attach' and r['feedback'].get('code') in ('NO_CONNECTION','ENDPOINT_COLLISION','PATH_BLOCKED')]
        counts=Counter((r['action'].get('partId'),r['action'].get('candidate')) for r in attempts)
        for record in sorted(attempts,key=lambda r:-counts[r['action'].get('partId'),r['action'].get('candidate')]):
            action=record['action'];token=(action.get('partId'),action.get('candidate'))
            if token in seen:continue
            seen.add(token);actor=parts.get(token[0]);candidate=poses.get(token[1]);goal=saved['goal'].get(actor)
            if not goal or not candidate:continue
            proposed={**record['before'],actor:candidate};reference={**record['before'],actor:goal}
            equivalent=s.ep.runtime.signature(proposed)==s.ep.runtime.signature(reference)
            views={v:sensor.render(proposed,v).tobytes()==sensor.render(reference,v).tobytes() for v in ('isometric','rear','top')}
            extra={}
            if all(views.values()) and not equivalent:
                extra={str(angle):sensor.render(proposed,angles=(angle,30)).tobytes()==sensor.render(reference,angles=(angle,30)).tobytes() for angle in (35,125,215,305)}
            candidates.append(dict(partId=token[0],candidate=token[1],repeatedAttempts=counts[token],samePhysicalPlacement=equivalent,
                standardViewMatches=views,additionalViewMatches=extra,needsReview=not equivalent and all(views.values()) and all(extra.values())))
            if len(candidates)>=5:break
        return dict(runId=run['arenaRunId'],caseId=run['caseId'],model=run['model'],finalViewMatches=matches,
            finalEquivalent=run['stateMetrics']['finalEquivalent'],finalReviewRequired=all(matches.values()) and not run['stateMetrics']['finalEquivalent'],
            candidates=candidates,candidateReviewRequired=any(r['needsReview'] for r in candidates))


def main():
    path=OUT/'checks/visual-consistency.json';previous=json.loads(path.read_text()) if path.exists() else {'rows':[]}
    rows={r['runId']:r for r in previous['rows']}
    for run in merged()['runs']:
        if run['arenaRunId'] in rows:continue
        row=check(run);rows[row['runId']]=row
        write_json(path,dict(checkedAt=time.time(),rows=list(rows.values()),apiCalls=0,
            flagged=sum(r['finalReviewRequired'] or r['candidateReviewRequired'] for r in rows.values()),
            scope='Final standard views and at most five repeated rejected placements per run. Not an independent physics or human-readability proof.'))
        print('VISUAL',len(rows),row['runId'],row['finalReviewRequired'],row['candidateReviewRequired'],flush=True)


if __name__=='__main__':main()
