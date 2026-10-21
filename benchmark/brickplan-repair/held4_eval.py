"""Offline scorer for the normalized held-subassembly static repair bank.

The scorer accepts public case IDs and action traces. It never uses the old
Domain optimum as a score and makes no external model calls.
"""
from collections import Counter
from pathlib import Path
import argparse
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assembly import Assembly
from static_v4.certify import digest

ROOT = Path(__file__).resolve().parents[2]
BANK = ROOT / 'deliverables/brickplan-static-held4/combined'
PROTOCOL = 'connector-workbench/4'


def read(path): return json.loads(path.read_text())


def load(public_id, bank=BANK):
    for line in (bank / 'cases.jsonl').open():
        case = json.loads(line)
        if case['publicId'] != public_id: continue
        if case['manipulationProtocol'] != PROTOCOL: raise ValueError('Wrong action protocol')
        cert_file = case.get('qualificationFile', 'models/' + case['modelId'] + '/qualification.json')
        cert = read(bank / cert_file)
        expected = digest(dict(caseId=case['id'], initial=case['initial'], goal=case['goal'],
                               plan=case['oraclePlan'], source=cert['contentSha256']))
        if expected != case['referenceValidation']['sha256']:
            raise ValueError('Stale or altered reference witness')
        return Assembly(cert), case
    raise KeyError(public_id)


def evaluate(public_id, actions, bank=BANK):
    runtime, case = load(public_id, bank)
    state = runtime.state(case['initial'])
    remaining = runtime.signature(runtime.state(case['goal'])).copy()
    initially_correct = set()
    for actor, key in state.items():
        if not key: continue
        signature = next(iter(runtime.signature({actor: key})))
        if remaining[signature]:
            initially_correct.add(actor)
            remaining[signature] -= 1
    feedback = []; finished = False; valid = 0; attempts = 0; observations = 0
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
    return dict(schema='brickplan-held4-score/1', publicId=public_id,
                manipulationProtocol=PROTOCOL, success=success, finished=finished,
                finalEquivalent=runtime.complete(state),
                legalMoves=valid, manipulationAttempts=attempts,
                invalidMoves=attempts-valid, observations=observations,
                correctPiecesRemoved=len(removed),
                correctRemovalEvents=sum(removed.values()),
                referenceWitnessLength=case['referenceCost'],
                exactOptimum=None, feedback=feedback)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('public_id')
    parser.add_argument('trace', type=Path,
                        help='JSON array of inspect/attach/detach/finish actions')
    args = parser.parse_args()
    print(json.dumps(evaluate(args.public_id, read(args.trace)), ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
