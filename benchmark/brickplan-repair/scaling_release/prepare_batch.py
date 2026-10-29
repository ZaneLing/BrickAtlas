"""Bounded worker processes; no external model API calls."""
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse,subprocess,sys,time
from scaling_release import ROOT,OUT
from expansion_v7.build import read,write

def main():
 p=argparse.ArgumentParser();p.add_argument('--limit',type=int,default=400);p.add_argument('--workers',type=int,default=4);p.add_argument('--retry',action='store_true');p.add_argument('--timeout',type=int,default=180);p.add_argument('--retry-timeouts',action='store_true');a=p.parse_args()
 rows=read(OUT/'source-pool.json')['models']
 rows=[r for r in rows if not (OUT/'private'/r['setNumber']/'metadata.json').exists() and (a.retry or a.retry_timeouts or not (OUT/'private'/r['setNumber']/'status.json').exists())]
 if a.retry_timeouts:rows=[r for r in rows if (OUT/'private'/r['setNumber']/'status.json').exists() and 'time-limit' in read(OUT/'private'/r['setNumber']/'status.json').get('reason','')]
 # Work through recognizable small sources first; every outcome stays recorded.
 rows.sort(key=lambda r:(r['parts']>250,r['parts']))
 def run(r):
  n=r['setNumber'];folder=OUT/'private'/n;folder.mkdir(parents=True,exist_ok=True);start=time.time()
  with (folder/'prepare.log').open('w') as log:
   try:
    proc=subprocess.run([sys.executable,'-m','scaling_release.prepare','--set',n],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=a.timeout)
    if proc.returncode:write(folder/'status.json',dict(status='withheld',phase='prepare',reason='worker-exit-'+str(proc.returncode)))
   except subprocess.TimeoutExpired:write(folder/'status.json',dict(status='withheld',phase='prepare',reason=f'qualification-time-limit-{a.timeout}s'))
  ok=(folder/'metadata.json').exists();return dict(setNumber=n,ready=ok,seconds=round(time.time()-start,2))
 results=[]
 with ThreadPoolExecutor(max_workers=a.workers) as ex:
  for f in as_completed([ex.submit(run,r) for r in rows[:a.limit]]):
   r=f.result();results.append(r);print('PREPARED' if r['ready'] else 'WITHHELD',r['setNumber'],r['seconds'],flush=True)
 write(OUT/'last-prepare-batch.json',dict(results=results,apiCalls=0))
if __name__=='__main__':main()
