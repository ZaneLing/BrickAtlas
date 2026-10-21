from pathlib import Path
import json,sys,time
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'eval')]
from dynamic_v6.object_models import OBJECTS,certificate
from baseplate import PlateAssembly
from dynamic_v5.build import write
OUT=HERE.parents[2]/'deliverables/brickplan-dynamic-v6'

def main():
    rows=[]
    for mid,s in OBJECTS.items():
        t=time.time()
        try:
            cert=certificate(mid,s);rt=PlateAssembly(cert);manual=rt.manual();g,_=rt.connections(rt.goal);g.pop('@baseplate',None)
            todo=[next(iter(g))];seen=set()
            while todo:
                a=todo.pop()
                if a in seen:continue
                seen.add(a);todo.extend(set(g[a])-seen-{'@baseplate'})
            row=dict(modelId=mid,parts=len(s['parts']),buildable=manual['pathVerified'],connected=len(seen)==len(g),passed=manual['pathVerified'] and len(seen)==len(g))
            if row['passed']:write(OUT/'object-sources'/mid/'qualification.json',cert)
            else:
                parts=list(rt.present(rt.goal).items())
                row['collisions']=[(a,b) for i,(a,p) in enumerate(parts) for b,q in parts[i+1:] if rt.q.endpoint(p,q)['status']!='CLEAR']
                row['groups']=rt.connections(rt.goal)[1]
        except Exception as e:row=dict(modelId=mid,passed=False,error=repr(e))
        row['seconds']=round(time.time()-t,2);rows.append(row);print(row,flush=True)
        write(OUT/'object-admission.json',rows)
    assert all(x['passed'] for x in rows), 'Fix rejected object designs before building episodes.'
    print('PASS',len(rows))
if __name__=='__main__':main()
