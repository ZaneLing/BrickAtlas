"""Make a no-intervention prerequisite explicit for every published dynamic task.

The control for an incident is the SAME case loaded with control=True, which
suppresses only external events. This preserves its start, goal, inventory,
camera contract and difficulty; a generic control from the same object is not
substituted. API runs must still populate normalSuccess before repair claims.
"""
from collections import Counter
import json
from bench_design import OUT
from bench_design.selection import retired
from expansion_v7.build import write


def main():
    rows = [json.loads(line) for line in (OUT / 'questions.jsonl').read_text().splitlines()]
    dynamic = [r for r in rows if r['mode'] == 'dynamic' and
               not retired(r['id'], r['model'], r.get('source'))]
    controls = {(r['track'], r['model']) for r in dynamic if r['taskType'] == 'D0'}
    entries = []
    for r in dynamic:
        key = (r['track'], r['model'])
        assert key in controls, ('No published normal control for', r['id'])
        entries.append(dict(caseId=r['id'], canonicalId=r['canonicalId'],
            track=r['track'], model=r['model'], source=r.get('source'),
            taskType=r['taskType'], controlCaseId=r['id'],
            controlLaunch='Session.open(caseId, ..., control=True)',
            exactSameCase=True, eventScheduleSuppressed=True,
            prerequisite='Evaluate normal completion before interpreting any incident repair',
            repairEligibleOnlyIfNormalSucceeded=r['taskType'] != 'D0'))
    out = dict(schema='brick-atlas-normal-gate/1', totalDynamic=len(entries),
        byType=dict(Counter(e['taskType'] for e in entries)),
        byTrack=dict(Counter(e['track'] for e in entries)),
        uniqueModels=len({(e['track'], e['model']) for e in entries}),
        incidentTasks=sum(e['taskType'] != 'D0' for e in entries),
        rule='For every incident task, first run its exact no-event control with the same model and input protocol. Service errors and untriggered events are excluded from repair failure. Independent normal success is necessary; a matched shared-prefix branch is additionally required for causal recovery claims.',
        entries=entries)
    write(OUT / 'normal-gate.json', out)
    print(json.dumps({k: out[k] for k in ('totalDynamic','byType','byTrack','uniqueModels','incidentTasks')}, ensure_ascii=False))


if __name__ == '__main__': main()
