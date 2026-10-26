"""Uniform, unscored position cards for the existing public inspect-part action."""
from PIL import Image,ImageDraw,ImageFilter
import numpy as np
from render import FONT


def position_pages(session,public_part,view='isometric'):
    ep,packet=session.ep,session.packet
    actor=ep.actors[public_part]
    keys=sorted((k for k,r in ep.cert['candidates'].items() if r['actor']==actor),key=ep.pose_alias.get)
    assets=[]
    for offset in range(0,len(keys),12):
        group=keys[offset:offset+12]
        image=Image.new('RGB',(1600,((len(group)+3)//4)*312),'white');draw=ImageDraw.Draw(image)
        items=[]
        for i,key in enumerate(group):
            x,y=(i%4)*400,(i//4)*312
            frame=['_module_frame'] if '_module_frame' in packet.renderer.bounds else None
            card,mask=packet.renderer.rgb({**ep.state,actor:key},view,size=(400,284),supersample=1,frame_keys=frame)
            actor_mask=Image.fromarray(np.uint8(mask==packet.renderer.ids[actor])*255)
            expanded=np.asarray(actor_mask.filter(ImageFilter.MaxFilter(5))).astype(int)
            border=Image.fromarray(np.uint8(np.maximum(0,expanded-np.asarray(actor_mask).astype(int))))
            card.paste((0,151,164),(0,0),border)
            image.paste(card,(x,y+28))
            candidate=ep.pose_alias[key];draw.text((x+8,y+6),public_part+' / '+candidate,font=FONT,fill='#17283a')
            items.append(dict(candidate=candidate,rectangle=[x,y,x+400,y+312]))
        assets.append(packet.asset(image,'candidate-catalog',partId=public_part,view=view,
            page=offset//12+1,items=items,hypothetical=True,legalityOrCorrectnessShown=False))
    return assets
