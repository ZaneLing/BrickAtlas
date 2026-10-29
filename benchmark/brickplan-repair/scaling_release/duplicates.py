"""Find identical source structures after color, translation and 24 axis rotations."""
from collections import defaultdict
from itertools import permutations,product
import hashlib,json
import numpy as np
from scaling_release import ROOT,OUT
from expansion_v7.build import read,write

def fingerprint(instances):
 matrices=np.array([np.asarray(p['originalMatrix']).reshape(4,4).T for p in instances]);matrices[:,:3,3]-=matrices[:,:3,3].mean(0)
 parts=[p['partNumber'].lower().removeprefix('p/') for p in instances];variants=[]
 for order in permutations(range(3)):
  for signs in product([-1,1],repeat=3):
   rot=np.eye(3)[list(order)]*np.array(signs)[:,None]
   if np.linalg.det(rot)<.5:continue
   transformed=rot@matrices[:,:3,:]
   rows=sorted((p,tuple(np.round(m,5).ravel())) for p,m in zip(parts,transformed))
   variants.append(hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest())
 return min(variants)

def main():
 groups=defaultdict(list);records=[]
 for row in read(OUT/'source-pool.json')['models']:
  mf=read(ROOT/row['manifest']);sha=fingerprint(mf['instances']);groups[sha].append(row['setNumber']);records.append(dict(model=row['setNumber'],structureSha256=sha))
 from scaling_release.legacy import collect
 for m in collect()[0]:
  mid=m['id'];path=ROOT/'deliverables/brickplan-expansion-v7/models'/mid/'certificate.private.json.gz' if mid.startswith('v7-') else ROOT/'deliverables/brickplan-dynamic-v6/models'/mid/'qualification.json'
  cert=read(path);parts=list(cert['fixed'].values())+[r['part'] for r in cert['candidates'].values() if r['kind']=='goal'];seen=set();instances=[]
  for p in parts:
   key=(p['partNumber'],tuple(np.asarray(p['rawMatrix']).ravel()))
   if key in seen:continue
   seen.add(key);matrix=np.diag([.4,-.4,-.4,1.])@np.asarray(p['rawMatrix']);instances.append(dict(partNumber=p['partNumber'],originalMatrix=matrix.T.ravel().tolist()))
  sha=fingerprint(instances);groups[sha].append(mid);records.append(dict(model=mid,structureSha256=sha,legacy=True))
 duplicates=[dict(structureSha256=k,models=v) for k,v in groups.items() if len(v)>1]
 write(OUT/'checks/source-duplicates.json',dict(checked=len(records),records=records,duplicates=duplicates,colorIgnored=True,translationIgnored=True,globalAxisRotations=24,arbitraryShapeSymmetryProven=False));print('DUPLICATE GROUPS',duplicates,flush=True)

if __name__=='__main__':main()
