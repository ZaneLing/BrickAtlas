"""Reproducible policy baselines, with privilege level stated in the output."""
from collections import Counter, defaultdict
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from dynamic_v5.episode import BANK, DynamicEpisode, load_case


def public(ep, action):
    result = dict(type=action['type'], partId=ep.alias[action['partId']])
    if 'candidate' in action:
        result['candidate'] = ep.pose(action['candidate'])
    return result


def run(case, cert, witness, policy):
    ep = DynamicEpisode(cert, case)
    for action in witness:
        ep.step(public(ep, action))
        if policy == 'privileged-reset' and ep.event:
            break
    if policy == 'privileged-reset' and ep.event:
        # This policy reads the private event boundary and exact state. Its
        # result is an inefficient feasibility baseline, never a visual score.
        while any(ep.state.values()):
            legal = []
            for actor in sorted(ep.actors):
                if not ep.state[actor]:
                    continue
                _, feedback = ep.runtime.check(ep.state, actor, 'detach')
                if feedback['code'] == 'OK':
                    legal.append(actor)
            if not legal:
                break
            ep.step(dict(type='detach', partId=ep.alias[legal[0]]))
        if not any(ep.state.values()):
            for action in witness:
                ep.step(public(ep, action))
    ep.step(dict(type='finish'))
    score = ep.score()
    return dict(caseId=case['id'], modelId=case['modelId'], sourceFamily=case['sourceFamily'],
                kind=case['kind'], pairedGroup=case['pairedGroup'], policy=policy,
                success=score['success'], eventTriggered=score['eventTriggered'],
                legalMoves=score['legalMoves'], invalidMoves=score['invalidMoves'],
                finalEquivalent=score['finalEquivalent'])


def main():
    cases = json.loads((BANK/'cases.private.json').read_text())['cases']
    results = []
    for case in cases:
        cert, _ = load_case(case['id'])
        witness = json.loads((BANK/'models'/case['modelId']/'evidence.json').read_text())['buildWitness']
        for policy in ('blind-manual', 'privileged-reset'):
            results.append(run(case, cert, witness, policy))
    summary = {}
    for policy in ('blind-manual', 'privileged-reset'):
        rows = [r for r in results if r['policy'] == policy]
        by_kind = defaultdict(list)
        for row in rows:
            by_kind[row['kind']].append(row)
        summary[policy] = dict(total=len(rows), success=sum(r['success'] for r in rows),
                               eventTriggered=sum(r['eventTriggered'] for r in rows),
                               byKind={k:dict(total=len(v),success=sum(r['success'] for r in v),
                                              triggered=sum(r['eventTriggered'] for r in v))
                                       for k,v in sorted(by_kind.items())},
                               totalLegalMoves=sum(r['legalMoves'] for r in rows),
                               totalInvalidMoves=sum(r['invalidMoves'] for r in rows))
    output = dict(schema='brickplan-dynamic-baselines/1',
                  policies={'blind-manual':'Follows the original build witness; ignores all observations and action errors.',
                            'privileged-reset':'Reads private event occurrence and exact installed actors; clears the assembly and rebuilds.'},
                  summary=summary, rows=results)
    (BANK/'baselines.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__ == '__main__':
    main()
