"""Compare recorded same-condition inputs; never substitute current defaults."""
import json
import time
from collections import defaultdict
from dynamic_arena import OUT as ARENA
from dynamic_arena.transport import write_json
from unified_agent.ark_batch import OUT, combined_report


def main():
    groups = defaultdict(list)
    for run in combined_report()['runs']:
        log = json.loads((ARENA / 'runs' / run['arenaRunId'] / 'log.json').read_text())
        groups[run['caseId'], run['arenaBranch']].append(dict(
            model=run['model'], contract=run['agentContractSha256'],
            images=[image['sha256'] for image in log['initialImages']],
            profile=run['agentProfile']))
    rows = []
    for (case_id, condition), group in groups.items():
        rows.append(dict(caseId=case_id, condition=condition,
            models=[r['model'] for r in group],
            sameContract=len({r['contract'] for r in group}) == 1,
            sameInitialImages=len({tuple(r['images']) for r in group}) == 1,
            sameBudget=len({json.dumps(r['profile'], sort_keys=True) for r in group}) == 1))
    result = dict(passed=all(r['sameContract'] and r['sameInitialImages'] and r['sameBudget'] for r in rows),
        checkedAt=time.time(), rows=rows, apiCalls=0,
        scope='Same case and condition only. Does not establish static/dynamic matched-state equivalence or equal backend compute.')
    write_json(OUT / 'checks/fairness-audit.json', result)
    print('FAIRNESS', len(rows), 'groups', result['passed'])


if __name__ == '__main__':
    main()
