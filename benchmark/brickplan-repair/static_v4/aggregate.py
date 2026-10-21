"""Family-balanced aggregation; paired family bootstrap, never case-IID CIs."""
from collections import defaultdict
import random

def summarize(rows,metric='success',seed=214,repetitions=2000):
    groups=defaultdict(list)
    for row in rows:groups[row['sourceFamily']].append(float(row[metric]))
    if not groups:return dict(n=0,families=0,mean=None,ci95=None)
    means=[sum(v)/len(v) for _,v in sorted(groups.items())]
    rng=random.Random(seed)
    boots=sorted(sum(rng.choices(means,k=len(means)))/len(means) for _ in range(repetitions))
    return dict(n=len(rows),families=len(groups),familyMacroMean=sum(means)/len(means),
                caseMicroMean=sum(float(r[metric]) for r in rows)/len(rows),
                familyBootstrapCI95=[boots[int(.025*repetitions)],boots[min(repetitions-1,int(.975*repetitions))]],
                smallFamilyWarning=len(means)<10,seed=seed,repetitions=repetitions)

def paired(left,right,metric='success'):
    a={r['caseId']:r for r in left};b={r['caseId']:r for r in right}
    if a.keys()!=b.keys():raise ValueError('Paired comparison requires the exact same case IDs')
    if any(a[k]['sourceFamily']!=b[k]['sourceFamily'] for k in a):raise ValueError('Family mismatch')
    return summarize([dict(sourceFamily=a[k]['sourceFamily'],difference=float(a[k][metric])-float(b[k][metric])) for k in a],metric='difference')
