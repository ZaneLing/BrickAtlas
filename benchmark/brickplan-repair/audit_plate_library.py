"""Replay every archived static repair case with the live white-plate rules.

This is an offline data audit. It never calls a model API. It records failures
instead of silently removing a case from the denominator.
"""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from baseplate import PlateAssembly, PROTOCOL
from assembly import Assembly

ROOT = Path(__file__).resolve().parents[2]
BANK = ROOT / 'deliverables/brickplan-repair-library'
OUT = ROOT / 'deliverables/brickplan-plate-audit-2026-10-16'


def read(path):
    return json.loads(path.read_text())


def audit_case(runtime, case, plate=True):
    issues = []
    try:
        initial = runtime.state(runtime.migrate_state(case['initial']) if plate else case['initial'])
        goal = runtime.state(runtime.migrate_state(case['goal']) if plate else case['goal'])
    except (ValueError, KeyError) as exc:
        return dict(caseId=case['id'], modelId=case['modelId'], status='INVALID_STATE',
                    issues=[str(exc)], actionsReplayed=0)
    if initial == goal and case['kind'] != 'control':
        issues.append('initial_equals_goal')
    if runtime.complete(initial) != (case['kind'] == 'control'):
        issues.append('initial_completion_disagrees_with_kind')
    if not runtime.complete(goal):
        issues.append('declared_goal_not_complete')
    for name, state in [('initial', initial), ('goal', goal)]:
        present = runtime.present(state)
        for actor, part in present.items():
            if plate and runtime.plate_collision(part):
                issues.append(name + ':plate_collision:' + actor)
        actors = list(present)
        for i, actor in enumerate(actors):
            if any(runtime.q.endpoint(present[actor], present[other])['status'] != 'CLEAR'
                   for other in actors[i + 1:]):
                issues.append(name + ':part_overlap:' + actor)
    state = initial
    replayed = 0
    for step, action in enumerate(case['oraclePlan']):
        try:
            state, feedback = runtime.check(state, action['partId'], action['type'],
                                            candidate=action.get('candidate'))
        except (ValueError, KeyError) as exc:
            issues.append(f'oracle_exception:{step}:{exc}')
            break
        if feedback['code'] != 'OK':
            issues.append(f"oracle_rejected:{step}:{feedback['code']}")
            break
        replayed += 1
    else:
        if not runtime.complete(state):
            issues.append('oracle_does_not_complete')
    return dict(caseId=case['id'], modelId=case['modelId'], kind=case['kind'],
                status='PASS' if not issues else 'FAIL', issues=issues,
                actionsReplayed=replayed, oracleLength=len(case['oraclePlan']),
                oldExpectedOptimum=case.get('expectedOptimum'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', action='append')
    parser.add_argument('--protocol', choices=['plate5', 'held4'], default='plate5')
    parser.add_argument('--bank', type=Path, default=BANK)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    bank = args.bank
    index = read(bank / 'index.json')
    rows = []
    started = time.time()
    for number, model in enumerate(index['models'], 1):
        model_id = model['modelId']
        if args.model and model_id not in args.model:
            continue
        folder = bank / 'models' / model_id
        plate = args.protocol == 'plate5'
        runtime = PlateAssembly(read(folder / 'qualification.json')) if plate else Assembly(read(folder / 'qualification.json'))
        cases = read(folder / 'cases.json')
        assert len(cases) == model['caseCount']
        for case in cases.values():
            rows.append(audit_case(runtime, case, plate))
        print(f'{number}/{len(index["models"])} {model_id} '
              f'{sum(r["status"] == "PASS" for r in rows if r["modelId"] == model_id)}/{len(cases)}',
              flush=True)
    if not args.model:
        exported = [json.loads(line) for line in (bank / 'cases.jsonl').read_text().splitlines()]
        assert len(exported) == index['caseCount'] == len(rows)
        assert {c['id'] for c in exported} == {r['caseId'] for r in rows}
    out = args.out or (OUT if args.protocol == 'plate5' else OUT / 'held4')
    out.mkdir(parents=True, exist_ok=True)
    counts = Counter(issue.split(':')[0] for r in rows for issue in r['issues'])
    report = dict(schema='brickplan-geometry-replay-audit/1', protocol=PROTOCOL if args.protocol == 'plate5' else 'connector-workbench/4',
                  bankSha256=hashlib.sha256((bank / 'cases.jsonl').read_bytes()).hexdigest(),
                  cases=len(rows), passed=sum(r['status'] == 'PASS' for r in rows),
                  failed=sum(r['status'] == 'FAIL' for r in rows),
                  actionsReplayed=sum(r['actionsReplayed'] for r in rows),
                  issueCounts=dict(counts), seconds=round(time.time() - started, 2))
    (out / 'rows.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
    (out / 'summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
