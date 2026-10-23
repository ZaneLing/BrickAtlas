"""Same JSON-lines visual/action contract for the expanded cases. No paid calls."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
import uuid
import numpy as np
from PIL import Image,ImageDraw
from expansion_v7 import OUT, PROTOCOL
from expansion_v7.build import read,write
from expansion_v7.runtime import Episode
from community_modules.run_episode import ModulePacket as PreviousPacket
from render import FONT


def load_case(case_id):
    index=read(OUT/'index.json')
    row=next((r for r in index['cases'] if r['id']==case_id),None)
    if row is None:raise ValueError('Unknown case')
    folder=OUT/'models'/row['module']
    cert=read(folder/'certificate.private.json.gz')
    case=next(c for c in read(folder/'cases.private.json.gz') if c['id']==case_id)
    return cert,case,read(folder/'manual.private.json.gz')


class Packet(PreviousPacket):
    def __init__(self, ep, manual, directory):
        self.manual=manual
        # Plate scenes render the environment board, not the old implicit fixture.
        render_cert=ep.runtime.cert if ep.cert.get('environmentMode')=='white-baseplate' else ep.cert
        old=ep.cert;ep.cert=render_cert
        try:super().__init__(ep,{'manual':manual['actions']},directory)
        finally:ep.cert=old

    def manual_page(self, number):
        action=self.manual['actions'][number-1]
        limit=self.ep.case['completedInstructionStep'] if self.ep.case['mode']=='static' else len(self.manual['actions'])
        future=number>limit
        page=Image.new('RGB',(1600,1040),'white');draw=ImageDraw.Draw(page)
        title='FUTURE REFERENCE ONLY - NOT TARGET' if future else 'REFERENCE STEP - TARGET IS UNCHANGED'
        draw.text((16,8),f'STEP {number} | {title}',font=FONT,fill='#17283a')
        images=[('PART',self.render({action['actor']:action['candidate']},only=action['actor'],size=(800,472)))]
        images += [(view.upper(),self.render(self.manual['states'][number],view,size=(800,472)))
                   for view in ('isometric','rear','top')]
        for i,(label,im) in enumerate(images):
            x,y=i%2*800,40+i//2*500
            page.paste(im,(x,y+28));draw.text((x+12,y+5),label,font=FONT,fill='#17283a')
        return self.asset(page,'future-instruction-reference' if future else 'instruction-reference',
                          step=number,isTarget=False,referenceOnly=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case',required=True);parser.add_argument('--seed',type=int,default=41)
    args=parser.parse_args();cert,case,manual=load_case(args.case)
    ep=Episode(cert,case,args.seed);directory=OUT/'runs'/uuid.uuid4().hex
    packet=Packet(ep,manual,directory)
    print(json.dumps(packet.observation(),ensure_ascii=False),flush=True)
    for line in sys.stdin:
        try:action=json.loads(line)
        except json.JSONDecodeError:action={'type':'invalid'}
        ep.step(action)
        print(json.dumps(packet.observation(),ensure_ascii=False),flush=True)
        if ep.done:break
    write(directory/'record.private.json.gz',dict(caseId=case['id'],seed=args.seed,score=ep.score(),
        decisions=ep.decisions,history=ep.history,events=ep.events,finalState=ep.state))


if __name__=='__main__':main()
