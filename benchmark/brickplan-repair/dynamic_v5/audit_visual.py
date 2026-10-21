"""Image-delta admission check; visibility to a VLM still needs human review."""
from collections import Counter
from pathlib import Path
import json
import sys
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
sys.path.insert(0,str(HERE.parent/'eval'))
from dynamic_v5.episode import BANK, DynamicEpisode, load_case
from dynamic_v5.vision import DynamicVisionRenderer

def main():
    cases=json.loads((BANK/'index.json').read_text())['cases']
    results=[];cache={}
    for case in cases:
        cert,private=load_case(case['id'])
        ep=DynamicEpisode(cert,private)
        model=case['modelId']
        if model not in cache:cache[model]=DynamicVisionRenderer(ep.cert,ep.runtime)
        renderer=cache[model]
        prefix=ep.runtime.manual()['states'][case['trigger']]
        after=dict(prefix)
        for action in private.get('privateEvent',{}).get('transaction',[]):
            after,feedback=ep.runtime.check(after,action['partId'],action['type'],candidate=action.get('candidate'))
            assert feedback['code']=='OK'
        counts={}
        for view in ('isometric','top','rear'):
            before_image=np.asarray(renderer.rgb(prefix,view,size=(800,600),supersample=1)[0]).astype(np.int16)
            after_image=np.asarray(renderer.rgb(after,view,size=(800,600),supersample=1)[0]).astype(np.int16)
            counts[view]=int(np.count_nonzero(np.max(np.abs(before_image-after_image),axis=2)>=24))
        results.append(dict(caseId=case['id'],kind=case['kind'],changedPixels=counts,maxChangedPixels=max(counts.values()),
                            passesPixelGate=case['kind']=='none' or max(counts.values())>=128))
        print(case['id'],counts,flush=True)
    report=dict(schema='brickplan-dynamic-visual-audit/2',interface='visual-v5-grid-and-catalog',resolution=[800,600],views=['isometric','top','rear'],
                rgbThreshold=24,minimumChangedPixels=128,scope='Machine pixel delta only; not human or VLM semantic observability.',
                total=len(results),passed=sum(r['passesPixelGate'] for r in results),
                failedByKind=dict(Counter(r['kind'] for r in results if not r['passesPixelGate'])),rows=results)
    (BANK/'visual-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('total','passed','failedByKind')},ensure_ascii=False))

if __name__=='__main__':main()
