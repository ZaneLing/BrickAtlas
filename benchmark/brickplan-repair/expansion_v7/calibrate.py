"""Import real outcomes without inventing human/model difficulty labels.

Every input condition gets one attempt per participant/model. Service failures
are reported separately, and structural groups are never redefined from results.
"""
from collections import defaultdict,Counter
import argparse
import csv
from expansion_v7 import OUT
from expansion_v7.build import read,write

COLUMNS=['caseId','kind','participantOrModel','inputVersion','status','success']


def main():
    p=argparse.ArgumentParser();p.add_argument('--results');args=p.parse_args()
    template=OUT/'empirical-results-template.csv'
    if not template.exists():
        with template.open('w',newline='') as f:csv.writer(f,lineterminator='\n').writerow(COLUMNS)
    if not args.results:
        print('Template only; no human/model outcomes collected.');return
    known={r['id'] for r in read(OUT/'index.json')['cases']}
    rows=list(csv.DictReader(open(args.results,newline='')));seen=set();groups=defaultdict(list);errors=Counter()
    for row in rows:
        if not set(COLUMNS)<=set(row):raise ValueError('Missing result columns')
        if row['caseId'] not in known or row['kind'] not in ('human','model'):raise ValueError('Unknown case or participant kind')
        if not row['participantOrModel'] or not row['inputVersion']:raise ValueError('Need participant/model and input version')
        token=tuple(row[k] for k in ('caseId','kind','participantOrModel','inputVersion'))
        if token in seen:raise ValueError('Repeated attempt cannot replace an earlier result')
        seen.add(token)
        if row['status']!='complete':errors[row['status']]+=1;continue
        if row['success'] not in ('true','false'):raise ValueError('Completed success must be true or false')
        groups[(row['caseId'],row['kind'],row['inputVersion'])].append(row['success']=='true')
    results=[dict(caseId=case,kind=kind,inputVersion=version,attempts=len(values),successes=sum(values),
        successRate=sum(values)/len(values),independentParticipantCount=len(values),
        interpretation='Observed performance; structural difficulty labels unchanged')
        for (case,kind,version),values in groups.items()]
    write(OUT/'empirical-difficulty.json',dict(status='OBSERVED' if results else 'NO_VALID_RESULTS',
        rows=results,excludedStatuses=dict(errors),structuralLabelsChanged=False,
        generalHumanPopulationEstimate=False,modelRepeatabilityMeasured=False))


if __name__=='__main__':main()
