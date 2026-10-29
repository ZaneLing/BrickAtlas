"""Acquire a larger figure-free pool; task qualification remains a separate gate."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import argparse,re
from scaling_release import ROOT,OUT
from dynamic_arena import OUT as ARENA
from dynamic_arena.source_library import acquire,DEST
from dynamic_arena.curate_sources import FigureAudit,category,DIVERSITY_HOLD,refresh_index
from expansion_v7.build import read,write


def main():
 p=argparse.ArgumentParser();p.add_argument('--limit',type=int,default=240);p.add_argument('--refresh',action='store_true');p.add_argument('--retry',action='store_true');a=p.parse_args()
 baseline=OUT/'source-baseline.json'
 if not baseline.exists():write(baseline,read(ARENA/'source-library.json'))
 target=OUT/'source-pool.json';pool=read(target) if target.exists() else dict(models=read(baseline)['models'],rejected=[],withdrawn=[])
 candidates=refresh_index() if a.refresh else read(DEST/('source-candidates-current.json' if (DEST/'source-candidates-current.json').exists() else 'source-candidates.json'))
 pool['models']=[r for r in pool['models'] if r['setNumber']!='10018-1']
 figure=FigureAudit();oldcuration=read(ARENA/'source-curation.json')
 forbidden={r['setNumber'] for r in oldcuration['withdrawn'] if r['figureAudit']['status']=='contains-figure'}|set(DIVERSITY_HOLD)|{'21004-1','21007-1','10018-1'}
 seen={r['setNumber'] for r in pool['models']}|{r['setNumber'] for r in pool['withdrawn']}|set() if a.retry else {r['setNumber'] for r in pool['models']}|{r['setNumber'] for r in pool['withdrawn']}|{r['setNumber'] for r in pool['rejected']}
 choices=[r for r in candidates if r['setNumber'] not in seen|forbidden and not re.search(r'Brickheadz|Fabuland|Mixels|Duplo|Bionicle|Brick Sketches',r['theme'],re.I)]
 counts=Counter(category(r) for r in pool['models']);buckets={}
 for r in choices:buckets.setdefault(category(r),[]).append(r)
 for b in buckets.values():b.sort(key=lambda r:(not any(x in r['theme'] for x in ('Creator','Architecture','Technic','Botanicals','Basic','Model Team','Hobby','Boat')),r['setNumber']))
 choices=[]
 while any(buckets.values()):
  for c in sorted(buckets,key=lambda c:(c=='other',counts[c])):
   if buckets[c]:choices.append(buckets[c].pop(0))
 def save():
  pool.update(count=len(pool['models']),apiCalls=0,byCategory=dict(Counter(r['objectCategory'] for r in pool['models'])))
  write(target,pool)
 with ThreadPoolExecutor(max_workers=8) as ex:
  for start in range(0,min(a.limit,len(choices)),16):
   batch=[dict(r,maxSourceParts=3000) for r in choices[start:start+min(16,a.limit-start)]]
   for r in ex.map(acquire,batch):
    if 'rejected' in r:pool['rejected'].append(r);continue
    audit=figure.audit(r);r.update(figureAudit=audit,objectCategory=category(r),addedForScaling=True)
    if audit['status']!='no-figure-parts-found':pool['withdrawn'].append(r);continue
    if r.get('shapeHash') in {x.get('shapeHash') for x in pool['models']}:pool['rejected'].append(dict(setNumber=r['setNumber'],rejected='duplicate source geometry'));continue
    pool['models'].append(r);print('POOL',len(pool['models']),r['setNumber'],r['parts'],r['title'],flush=True)
   save()
 save()
if __name__=='__main__':main()
