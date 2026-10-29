from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse,subprocess,sys,time
from scaling_release import ROOT,OUT
from expansion_v7.build import write

def main():
 p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=4);p.add_argument('--limit',type=int,default=400);p.add_argument('--retry',action='store_true');p.add_argument('--timeout',type=int,default=240);a=p.parse_args()
 folders=[p.parent for p in sorted((OUT/'private').glob('*/metadata.json')) if not (p.parent/'cases.private.json.gz').exists() and (a.retry or not (p.parent/'status.json').exists())]
 def run(folder):
  n=folder.name;start=time.time()
  with (folder/'build.log').open('w') as log:
   try:
    proc=subprocess.run([sys.executable,'-m','scaling_release.build','--set',n],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=a.timeout)
    if proc.returncode:write(folder/'status.json',dict(status='withheld',phase='cases',reason='worker-exit-'+str(proc.returncode)))
   except subprocess.TimeoutExpired:write(folder/'status.json',dict(status='withheld',phase='cases',reason=f'case-generation-time-limit-{a.timeout}s'))
  return dict(setNumber=n,ready=(folder/'cases.private.json.gz').exists(),seconds=round(time.time()-start,2))
 with ThreadPoolExecutor(max_workers=a.workers) as ex:
  for f in as_completed([ex.submit(run,r) for r in folders[:a.limit]]):
   r=f.result();print('BUILT' if r['ready'] else 'WITHHELD',r['setNumber'],r['seconds'],flush=True)
if __name__=='__main__':main()
