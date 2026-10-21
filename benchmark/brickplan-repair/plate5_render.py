"""Render a static plate5 question's current and target scene on white board."""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE/'eval'),str(HERE/'dynamic_v5')]
from plate5_eval import load
from dynamic_v5.vision import DynamicVisionRenderer

ROOT=HERE.parents[1]
DEST=ROOT/'deliverables/brickplan-static-plate5/images'

def render(public_id,view='isometric',destination=DEST):
    runtime,case=load(public_id)
    renderer=DynamicVisionRenderer(runtime.cert,runtime)
    folder=destination/public_id;folder.mkdir(parents=True,exist_ok=True)
    result=[]
    for role,state in [('current',case['initial']),('target',case['goal'])]:
        image,_=renderer.rgb(state,view=view,supersample=1)
        path=folder/(role+'-'+view+'.png');image.save(path)
        result.append(dict(role=role,view=view,path=str(path.relative_to(ROOT)),
                           sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                           width=image.width,height=image.height))
    manifest=dict(publicId=public_id,protocol='visual-rgb-v5-plate5',images=result)
    (folder/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('public_id');parser.add_argument('--view',default='isometric')
    args=parser.parse_args();print(json.dumps(render(args.public_id,args.view),ensure_ascii=False))
