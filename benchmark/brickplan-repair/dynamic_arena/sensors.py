"""Neutral, requested-only sensors shared by every dynamic source bank."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
from render import FONT as FALLBACK_FONT
FONT = ImageFont.truetype('/System/Library/Fonts/Supplemental/Comic Sans MS.ttf',16) if Path('/System/Library/Fonts/Supplemental/Comic Sans MS.ttf').exists() else FALLBACK_FONT
from dynamic_arena.plate_render import ArenaVision


class Sensors:
    def __init__(self, session):
        self.s = session
        self.ep = session.ep
        old = session.packet.renderer if session.packet else session.renderer
        # Module context is a real preassembly. Do not invent a physical plate
        # at its attachment plane; retain its full source geometry and renderer.
        self.renderer = (ArenaVision(old.cert, runtime=self.ep.runtime)
                         if hasattr(self.ep.runtime, 'baseplate') else old)
        self.renderer.bounds.update({k: v for k, v in old.bounds.items() if k.startswith('_')})
        self.aliases = getattr(self.ep, 'actor_alias', getattr(self.ep, 'alias', {}))
        self.reverse = {v: k for k, v in self.aliases.items()}
        self.poses = self.ep.pose_alias
        self.manual = getattr(session.packet, 'manual', None)
        self.full_manual_count = (len(self.manual['actions']) if self.manual else
            len(getattr(session.packet, 'module', {}).get('manual', [])))
        self.manual_count = self.full_manual_count
        self.target_stage = None
        if session.row['mode'] == 'static':
            # This is public task metadata, not a repair witness. Later build
            # steps describe another goal and must not appear in this task.
            self.target_stage = self.ep.case.get('completedInstructionStep')
            self.manual_count = (min(self.full_manual_count, self.target_stage)
                if type(self.target_stage) is int and self.target_stage >= 0 else 0)
        self.inventory_count = math.ceil(len(self.aliases) / 12)

    def keys(self, actor):
        if 'choices' in self.ep.case:
            return sorted(self.ep.case['choices'][actor], key=self.poses.get)
        return sorted((k for k, r in self.ep.cert['candidates'].items() if r['actor'] == actor), key=self.poses.get)

    def handles(self):
        return [dict(id=public, candidates=[self.poses[k] for k in self.keys(a)])
                for a, public in sorted(self.aliases.items(), key=lambda p: p[1])]

    def render(self, state, view='isometric', angles=None, focus='module', size=(800, 600)):
        frame = ['_module_frame'] if focus == 'module' and '_module_frame' in self.renderer.bounds else None
        return self.renderer.rgb(state, view, size=size, angles=angles, frame_keys=frame, supersample=1)[0]

    def availability(self,page=None):
        rows=(self.ep.inventory() if hasattr(self.ep,'inventory') and callable(self.ep.inventory) else
              [dict(partId=public,status='installed' if self.ep.state.get(a) else 'available') for a,public in self.aliases.items()])
        if page is None:return rows
        if not 1<=page<=self.inventory_count:raise ValueError('Unknown inventory page')
        group=set(sorted(self.aliases.values())[(page-1)*12:page*12])
        return [r for r in rows if r['partId'] in group]

    def inventory(self, page):
        if not 1 <= page <= self.inventory_count: raise ValueError('Unknown inventory page')
        group = sorted(self.aliases, key=self.aliases.get)[(page-1)*12:page*12]
        availability={r['partId']:r['status'] for r in self.availability(page)}
        im = Image.new('RGB', (1600, math.ceil(len(group)/4)*304), 'white'); draw = ImageDraw.Draw(im)
        for i, actor in enumerate(group):
            key = self.keys(actor)[0]; x, y = (i%4)*400, (i//4)*304
            tile = self.renderer.rgb({actor: key}, size=(400, 280), only=actor, frame_keys=[key], fixtures=False, supersample=1)[0]
            im.paste(tile, (x, y+24))
            label=self.aliases[actor]+' | '+availability[self.aliases[actor]]
            draw.text((x+8,y+4),label,font=FONT,fill='#17283a')
        return im

    def candidates(self, public, page, view, angles):
        actor = self.reverse[public]; keys = self.keys(actor)
        if not 1 <= page <= math.ceil(len(keys)/12): raise ValueError('Unknown candidate page')
        group = keys[(page-1)*12:page*12]
        im = Image.new('RGB', (1600, math.ceil(len(group)/4)*312), 'white'); draw = ImageDraw.Draw(im); items=[]
        frame = ['_module_frame'] if '_module_frame' in self.renderer.bounds else None
        for i, key in enumerate(group):
            x,y=(i%4)*400,(i//4)*312
            card,mask=self.renderer.rgb({**self.ep.state,actor:key},view,size=(400,284),angles=angles,supersample=1,frame_keys=frame)
            mask=Image.fromarray(np.uint8(mask==self.renderer.ids[actor])*255)
            border=Image.fromarray(np.uint8(np.maximum(0,np.asarray(mask.filter(ImageFilter.MaxFilter(5))).astype(int)-np.asarray(mask).astype(int))))
            card.paste((0,151,164),(0,0),border);im.paste(card,(x,y+28))
            candidate=self.poses[key];draw.text((x+8,y+6),public+' / '+candidate,font=FONT,fill='#17283a')
            items.append(dict(candidate=candidate,rectangle=[x,y,x+400,y+312]))
        return im, dict(partId=public,page=page,pages=math.ceil(len(keys)/12),items=items,hypothetical=True,legalityOrCorrectnessShown=False)

    def instruction(self, step):
        if not 1 <= step <= self.manual_count:
            raise ValueError('No such manual step for this task target; later construction stages are unavailable')
        asset = self.s.packet.manual_page(step)
        with Image.open(asset['file']) as im: return im.copy()

    def instruction_identity(self, step):
        """Identify the part pictured in an optional public manual step.

        No target pose ID, legality, fault or repair witness is returned.
        """
        actions = self.manual['actions'] if self.manual else getattr(self.s.packet,'module',{}).get('manual',[])
        actor = actions[step-1].get('actor') if 1 <= step <= self.manual_count else None
        return dict(referencePartId=self.aliases.get(actor),
            meaning='Handle of the part pictured in this optional construction step; not a required repair action or required order.')

    def _scene_mask(self, state, view, angles=None):
        frame=['_module_frame'] if '_module_frame' in self.renderer.bounds else None
        return self.renderer.rgb(state,view,size=(800,600),angles=angles,frame_keys=frame,supersample=1)

    def _outline(self, image, mask, actor):
        selection=Image.fromarray(np.uint8(mask==self.renderer.ids[actor])*255)
        border=Image.fromarray(np.uint8(np.maximum(0,np.asarray(selection.filter(ImageFilter.MaxFilter(5))).astype(int)-np.asarray(selection).astype(int))))
        image.paste((0,151,164),(0,0),border)
        return image

    def candidate_detail(self, public, candidate, view, angles=None):
        actor=self.reverse[public]
        key=next((k for k in self.keys(actor) if self.poses[k]==candidate),None)
        if key is None:raise ValueError('Candidate does not belong to this part; inspect its candidate catalogue first')
        current,_=self._scene_mask(self.ep.state,view,angles)
        proposed,mask=self._scene_mask({**self.ep.state,actor:key},view,angles)
        self._outline(proposed,mask,actor)
        image=Image.new('RGB',(1600,636),'white');draw=ImageDraw.Draw(image)
        image.paste(current,(0,36));image.paste(proposed,(800,36))
        draw.text((10,8),'CURRENT',font=FONT,fill='#17283a')
        draw.text((810,8),'HYPOTHETICAL '+public+' / '+candidate,font=FONT,fill='#17283a')
        return image,dict(partId=public,candidate=candidate,view=view,hypothetical=True,
            legalityOrCorrectnessShown=False,panels=[dict(role='current',rectangle=[0,36,800,636]),dict(role='hypothetical',rectangle=[800,36,1600,636])])

    def identify(self, point, view):
        image,mask=self._scene_mask(self.ep.state,view)
        picked=int(mask[min(599,int(point[1]*600)),min(799,int(point[0]*800))])
        actor=next((a for a,idx in self.renderer.ids.items() if idx==picked and a in self.aliases),None)
        if actor is not None:self._outline(image,mask,actor)
        return image,dict(view=view,point=point,partId=self.aliases.get(actor),
            visibleSurfaceOnly=True,noHiddenPartOrTargetLookup=True)
