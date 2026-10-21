"""Prevent anonymous action lists from leaking target membership through order/count."""
from pathlib import Path
from copy import deepcopy
from collections import Counter,defaultdict
import json,sys,math
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from dynamic_v5.build import write
from static_v4.certify import digest

def pad(cert):
    cert=deepcopy(cert)
    cert['candidates']={k:r for k,r in cert['candidates'].items() if r['kind']!='catalog_distractor'}
    for a,p in cert['fixed'].items():
        cert['candidates'][a+':goal']=dict(actor=a,kind='goal',part=deepcopy(p),label='part',support=[],pathBlocked=[])
    groups=defaultdict(list)
    for k,r in cert['candidates'].items():groups[r['actor']].append(k)
    count=max(12,math.ceil(max(map(len,groups.values()))/12)*12)
    for actor,keys in sorted(groups.items()):
        base=cert['candidates'][sorted(keys)[0]]['part'];seen={tuple(np.round(np.asarray(cert['candidates'][k]['part']['rawMatrix']).ravel(),4)) for k in keys}
        for turn in range(4):
            c,s=round(np.cos(turn*np.pi/2)),round(np.sin(turn*np.pi/2));rot=np.asarray([[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]])
            for dx,dz in ((x,z) for x in (0,20,-20,40,-40) for z in (0,20,-20,40,-40)):
                if len(keys)>=count:break
                p=deepcopy(base)
                for field in ('rawMatrix','matrix'):
                    m=np.asarray(p[field]);r=m@rot;r[:3,3]+=m[:3,:3]@np.asarray([dx,0,dz]);p[field]=r.tolist()
                token=tuple(np.round(np.asarray(p['rawMatrix']).ravel(),4))
                if token in seen:continue
                key=f'{actor}:catalog-{len(keys):03}';cert['candidates'][key]=dict(actor=actor,kind='catalog_distractor',part=p,label='grid placement',support=[],pathBlocked=[])
                keys.append(key);seen.add(token)
            if len(keys)>=count:break
        assert len(keys)==count,(actor,len(keys),count)
    cert['catalogPolicy']=dict(version=1,candidatesPerActor=count,ordering='Sort only by randomized public pose alias',padding='Same local translations/rotations for every inventory actor; independent of target membership and episode fault.')
    cert['contentSha256']=digest({k:v for k,v in cert.items() if k!='contentSha256'})
    return cert

def seal(bank):
    index=json.loads((bank/'index.json').read_text());rows=[]
    for mid in sorted({c['modelId'] for c in index['cases']}):
        path=bank/'models'/mid/'qualification.json';cert=pad(json.loads(path.read_text()));write(path,cert)
        epath=path.parent/'evidence.json';e=json.loads(epath.read_text());e['runtimeCertificateSha256']=cert['contentSha256'];e['catalogPolicy']=cert['catalogPolicy'];write(epath,e)
        for a in index['modelAudits']:
            if a['modelId']==mid:a['runtimeCertificateSha256']=cert['contentSha256'];a['catalogPolicy']=cert['catalogPolicy']
        counts=Counter(r['actor'] for r in cert['candidates'].values());assert len(set(counts.values()))==1
        rows.append(dict(modelId=mid,inventoryActors=len(counts),candidatesPerActor=cert['catalogPolicy']['candidatesPerActor']))
    write(bank/'index.json',index);write(bank/'catalog-audit.json',dict(status='PASS',models=len(rows),rows=rows))
    return rows
if __name__=='__main__':
    bank=HERE.parents[2]/'deliverables/brickplan-dynamic-v6';print('sealed',len(seal(bank)))
