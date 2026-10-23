"""Public JSON-lines adapter. Manuals are read on demand. Never calls an API."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import uuid
import numpy as np
from PIL import Image, ImageDraw
if __package__:
    from .core import OUT, ROOT, Episode, dump, render_certificate
else:
    from core import OUT, ROOT, Episode, dump, render_certificate
from render import PALETTE, FONT
from dynamic_v5.vision import DynamicVisionRenderer
from matched_canvas import comparison, panels


class ModulePacket:
    def __init__(self, ep, public_module, directory):
        self.ep, self.module, self.directory = ep, public_module, Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        config=(ROOT/'assets-source/ldraw-library/locked/LDConfig.ldr').read_text()
        PALETTE.update(dict(re.findall(r'CODE\s+(\d+)\s+VALUE\s+(#[0-9A-Fa-f]{6})',config)))
        self.renderer=DynamicVisionRenderer(render_certificate(ep.cert),runtime=ep.runtime)
        pts=np.concatenate([self.renderer.bounds[k] for k,r in ep.cert['candidates'].items() if r['kind']=='goal'])
        lo,hi=pts.min(0)-[20,28,20],pts.max(0)+[20,20,20]
        self.renderer.bounds['_module_frame']=np.array([[x,y,z] for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])
        self.inventory=self.inventory_pages()

    def asset(self,image,role,**meta):
        stream=io.BytesIO();image.save(stream,format='PNG');data=stream.getvalue()
        digest=hashlib.sha256(data).hexdigest();path=self.directory/(digest+'.png')
        if not path.exists():path.write_bytes(data)
        return dict(role=role,file=str(path),sha256=digest,width=image.width,height=image.height,**meta)

    def render(self,state,view='isometric',only=None,size=(1600,1200)):
        return self.renderer.rgb(state,view,size=size,supersample=1,only=only,
                                 frame_keys=None if only else ['_module_frame'])[0]

    def inventory_pages(self):
        actors=sorted(self.ep.actor_alias,key=self.ep.actor_alias.get);pages=[]
        for start in range(0,len(actors),12):
            group=actors[start:start+12];im=Image.new('RGB',(1600,((len(group)+3)//4)*304),'white')
            draw=ImageDraw.Draw(im)
            for i,actor in enumerate(group):
                key=next(k for k,r in self.ep.cert['candidates'].items() if r['actor']==actor)
                x,y=(i%4)*400,(i//4)*304
                im.paste(self.render({actor:key},only=actor,size=(400,280)),(x,y+24))
                draw.text((x+8,y+4),self.ep.actor_alias[actor],font=FONT,fill='#17283a')
            pages.append(self.asset(im,'inventory',page=len(pages)+1))
        return pages

    def manual_page(self,number):
        step=self.module['manual'][number-1]
        limit=self.ep.case['completedInstructionStep'] if self.ep.case['mode']=='static' else len(self.module['manual'])
        future=number>limit
        page=Image.new('RGB',(1600,1040),'white');draw=ImageDraw.Draw(page)
        caption=('FUTURE REFERENCE ONLY - NOT TARGET' if future else 'REFERENCE BUILD STEP - TARGET IS UNCHANGED')
        draw.text((16,8),f'STEP {number} | {caption}',font=FONT,fill='#17283a')
        sources=[('PART',OUT/step['partImage'])]+[(v.upper(),OUT/step['after'][v]) for v in ('isometric','rear','top')]
        for i,(label,path) in enumerate(sources):
            x,y=(i%2)*800,40+(i//2)*500
            with Image.open(path) as source:
                tile=source.convert('RGB');tile.thumbnail((800,472),Image.Resampling.LANCZOS)
                page.paste(tile,(x+(800-tile.width)//2,y+28+(472-tile.height)//2))
            draw.text((x+12,y+5),label,font=FONT,fill='#17283a')
        return self.asset(page,'future-instruction-reference' if future else 'instruction-reference',
                          step=number,isTarget=False,referenceOnly=True)

    def observation(self):
        ep=self.ep;obs=ep.observe();assets=[]
        for view in ('isometric','rear','top'):
            image=comparison(self.renderer,ep.state,ep.case['goal'],view,'CURRENT NOW','TARGET (required state)',frame_keys=['_module_frame'])
            assets.append(self.asset(image,'current-target',view=view,panels=panels('current-now','target')))
            if ep.previous is not None:
                image=comparison(self.renderer,ep.previous,ep.state,view,'BEFORE LAST ACTION','CURRENT NOW',frame_keys=['_module_frame'])
                assets.append(self.asset(image,'temporal-pair',view=view,panels=panels('before-last-action','current-now')))
        # All parts stay visible, grouped twelve per page instead of one image per part.
        assets.extend(self.inventory)
        total=len(self.module['manual']);stage=ep.case['completedInstructionStep'] if ep.case['mode']=='static' else total
        obs['manual']=dict(totalSteps=total,targetStage=stage,defaultImages=0,
            stepsForTarget=list(range(1,stage+1)),futureReferenceSteps=list(range(stage+1,total+1)),
            request=dict(type='inspect',manualStep=1),
            futureRequest=dict(type='inspect',manualStep=total,futureReference=True),
            policy='Optional reference order. Future steps are never required for TARGET and are shown only on explicit request.')
        obs['inventoryPages']=len(self.inventory)
        fb=ep.feedback or {}
        if fb.get('code')=='INSPECT':
            if 'manualStep' in fb:assets.append(self.manual_page(fb['manualStep']))
            elif 'inventoryPage' in fb:obs['requestedInventoryPage']=fb['inventoryPage']
            elif 'candidate' in fb:
                key=ep.poses[fb['candidate']];actor=ep.cert['candidates'][key]['actor']
                assets.append(self.asset(self.render({**ep.state,actor:key},fb['view']),
                                         'candidate-preview',view=fb['view'],candidate=fb['candidate']))
            elif 'partId' in fb:
                actor=ep.actors[fb['partId']]
                key=next(k for k,r in ep.cert['candidates'].items() if r['actor']==actor)
                assets.append(self.asset(self.render({actor:key},fb['view'],only=actor),
                                         'inventory-inspection',view=fb['view'],partId=fb['partId']))
            else:assets.append(self.asset(self.render(ep.state,fb['view']),'current-inspection',view=fb['view']))
        obs['images']=assets
        return obs


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--module',required=True)
    parser.add_argument('--condition',default='dynamic-missing',choices=[m+'-'+f for m in ('static','dynamic') for f in ('control','missing','wrong-color','extra-layer')])
    parser.add_argument('--seed',type=int,default=0);args=parser.parse_args()
    modules=json.loads((OUT/'gallery-data.js.json').read_text())
    module=next((m for m in modules if m['id']==args.module),None)
    if module is None:raise ValueError('Unknown module')
    base=OUT/args.module;cert=json.loads((base/'certificate.private.json').read_text())
    case=next(c for c in json.loads((base/'cases.private.json').read_text()) if c['id']==args.module+'-'+args.condition)
    ep=Episode(cert,case,args.seed);directory=OUT/'runs'/uuid.uuid4().hex
    packet=ModulePacket(ep,module,directory)
    print(json.dumps(packet.observation(),ensure_ascii=False),flush=True)
    for line in sys.stdin:
        try:ep.step(json.loads(line))
        except (ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
            ep.previous=dict(ep.state)
            ep.feedback=dict(code='INVALID_REQUEST',message=str(exc))
        print(json.dumps(packet.observation(),ensure_ascii=False),flush=True)
        if ep.done:break
    dump(directory/'record.private.json',dict(caseId=case['id'],seed=args.seed,score=ep.score(),history=ep.history,finalState=ep.state))


if __name__=='__main__':main()
