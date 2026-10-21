"""Offline scorer and witness audit for the white-baseplate static bank."""
from collections import Counter
from functools import lru_cache
from pathlib import Path
import argparse
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from baseplate import PlateAssembly, PROTOCOL
from static_v4.certify import digest

ROOT = Path(__file__).resolve().parents[2]
BANK = ROOT / 'deliverables/brickplan-static-plate5'
SOURCE = ROOT / 'deliverables/brickplan-static-held4/combined'


def rows(path):
    with path.open() as f:
        for line in f:
            yield json.loads(line)


@lru_cache(maxsize=1)
def cases():
    result = {case['publicId']: case for case in rows(BANK / 'cases.jsonl')}
    if len(result) != len(list(rows(BANK / 'cases.jsonl'))):
        raise ValueError('Duplicate public ID')
    return result


@lru_cache(maxsize=256)
def runtime_for(path):
    return PlateAssembly(json.loads((SOURCE / path).read_text()))


def load(public_id):
    case = cases()[public_id]
    if case['manipulationProtocol'] != PROTOCOL:
        raise ValueError('Wrong action protocol')
    runtime = runtime_for(case['qualificationFile'])
    expected = digest(dict(caseId=case['id'], initial=case['initial'], goal=case['goal'],
                           plan=case['oraclePlan'], source=runtime.cert['contentSha256']))
    if expected != case['referenceValidation']['sha256']:
        raise ValueError('Stale reference witness')
    return runtime, case


def evaluate(public_id, actions):
    runtime, case = load(public_id)
    state = runtime.state(case['initial'])
    if any(runtime.plate_collision(p) for p in runtime.present(state).values()):
        raise ValueError('Initial state intersects baseplate')
    remaining = runtime.signature(runtime.state(case['goal'])).copy()
    initially_correct = set()
    for actor, key in state.items():
        if not key: continue
        signature = next(iter(runtime.signature({actor: key})))
        if remaining[signature]:
            initially_correct.add(actor)
            remaining[signature] -= 1
    feedback = []; finished = False; valid = attempts = observations = 0
    removed = Counter()
    for action in actions:
        if finished: raise ValueError('Actions after finish')
        kind = action.get('type')
        if kind == 'finish':
            finished = True
            code = 'SUCCESS' if runtime.complete(state) else 'INCOMPLETE'
        elif kind == 'inspect':
            observations += 1; code = 'OBSERVED'
        elif kind in ('attach', 'detach'):
            attempts += 1
            actor = action.get('partId')
            try:
                after, result = runtime.check(state, actor, kind,
                                              raw=action.get('rawMatrix'),
                                              candidate=action.get('candidate'))
                code = result['code']
            except (ValueError, KeyError, TypeError):
                code = 'INVALID_ACTION'
            if code == 'OK':
                state = after; valid += 1
                if kind == 'detach' and actor in initially_correct: removed[actor] += 1
        else:
            code = 'INVALID_ACTION'
        feedback.append(dict(index=len(feedback), code=code))
    success = finished and runtime.complete(state)
    return dict(schema='brickplan-plate5-score/1', publicId=public_id,
                manipulationProtocol=PROTOCOL, success=success, finished=finished,
                finalEquivalent=runtime.complete(state), legalMoves=valid,
                manipulationAttempts=attempts, invalidMoves=attempts-valid,
                observations=observations, correctPiecesRemoved=len(removed),
                correctRemovalEvents=sum(removed.values()),
                referenceWitnessLength=len(case['oraclePlan']), exactOptimum=None,
                feedback=feedback)


def audit_all():
    failure=[]; counts=Counter(); total=0
    for case in cases().values():
        total += 1
        actions=[*case['oraclePlan'], {'type':'finish'}]
        try:
            result=evaluate(case['publicId'],actions)
            if not result['success'] or result['invalidMoves']:
                failure.append(dict(publicId=case['publicId'],feedback=result['feedback']))
            else: counts[case['migrationMethod']]+=1
        except Exception as exc:
            failure.append(dict(publicId=case['publicId'],error=str(exc)))
    return dict(total=total,passed=total-len(failure),failed=len(failure),methods=dict(counts),failures=failure)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('public_id',nargs='?')
    parser.add_argument('trace',type=Path,nargs='?')
    parser.add_argument('--audit-all',action='store_true')
    args=parser.parse_args()
    result=audit_all() if args.audit_all else evaluate(args.public_id,json.loads(args.trace.read_text()))
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
