"""V3 visual-only observations: clean native RGB, separate visual action references.

Legacy render.py is intentionally retained for replaying recorded v1/v2 evidence.
No truth, segmentation, geometry catalogue or diagnostic label enters the request.
"""
import base64
import hashlib
import io
import json
import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from render import Renderer, VIEWS, C, FONT

VERSION = 'visual-rgb-v3'
SIZE = (1600, 1200)
INITIAL_VIEWS = ('isometric', 'rear', 'top')
SYSTEM = '''Repair the current LEGO assembly to match the target shown in the images, then finish.
Infer shape, color, position and assembly differences from the images. The scene images contain no printed identifiers. Inventory cards have anonymous action handles in margins; these handles convey no goal or error. All listed pieces exist, including distractors. Candidate handles are available discrete placements, not a list of correct placements.
Use inspect with view (isometric/front/rear/left/right/top/bottom), azimuth and elevation, or crop [left,top,right,bottom] in normalized 0..1 image coordinates. A crop rerenders the chosen view at full resolution. To identify a visible piece without labels, inspect with view and point [x,y] in normalized image coordinates; this picks the foremost current piece. All pieces can also be inspected by partId, which isolates that piece in current and target with a shared camera frame. This uniform inspection is an aid, not an external camera. Inspect candidate to see that placement in context; previews do not perform actions or reveal feasibility.
Return JSON {"actions":[...],"note":"short explanation"}. detach requires partId, or view and point. attach requires explicit partId and candidate. inspect accepts the fields above. finish needs only type. At most 8 actions per response. A rejection, inspection or finish discards remaining actions. Connector alignment, collisions and straight insertion/extraction paths are checked only after an attempted action. Connected subassemblies may be held by a hand/fixture; they do not need bottom support or a permanent connection to the original base. Any legal repair order is accepted. Success depends on final physical geometry and color, allowing interchangeable identical parts; extra actions still count as cost. Inspect changes no pieces. Never infer success from feedback other than SUCCESS.'''


def _camera(view, angles):
    az, el = np.deg2rad(angles if angles is not None else VIEWS[view])
    direction = np.array([np.sin(az)*np.cos(el), np.sin(el), np.cos(az)*np.cos(el)])
    right = np.array([np.cos(az), 0, -np.sin(az)])
    return np.stack([right, np.cross(direction, right), direction], axis=1)


class VisionRenderer(Renderer):
    def __init__(self, cert):
        super().__init__(cert)
        # The same, case-independent envelope for all candidate poses, both
        # current/target images, and all revisions. No automatic faulty-part crop.
        self.bounds = {}
        for key, (vertices, _) in self.geometry.items():
            points = vertices.reshape(-1, 3)
            lo, hi = points.min(0), points.max(0)
            self.bounds[key] = np.array([[x,y,z] for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])
        self.envelope = np.concatenate(list(self.bounds.values()))

    def rgb(self, state, view='isometric', size=SIZE, only=None, angles=None,
            crop=None, frame_keys=None, supersample=2, fixtures=True):
        camera = _camera(view, angles)
        parts = {**({a:a for a in self.cert['fixed']} if fixtures else {}), **state}
        entries = [(a,k) for a,k in parts.items() if k in self.geometry and (only is None or a==only)]
        if frame_keys is not None:
            envelope = np.concatenate([self.bounds[k] for k in frame_keys if k in self.bounds])
        elif only is not None:
            envelope = np.concatenate([self.bounds[k] for k,r in self.cert['candidates'].items() if r['actor']==only])
        else:
            envelope = self.envelope
        projected = envelope @ camera
        lo, hi = projected.min(0), projected.max(0)
        center = (lo+hi)/2
        w,h = size
        scale = min(w*.88/max(hi[0]-lo[0],1), h*.88/max(hi[1]-lo[1],1))
        # Recompute projection for the requested crop, retaining equal scale
        # and framing for paired images. It is a new render, never upsampling.
        left, top, right, bottom = crop or (0.,0.,1.,1.)
        crop_scale = min(1/(right-left), 1/(bottom-top))
        shift_x = ((left+right)/2-.5)*w
        shift_y = ((top+bottom)/2-.5)*h
        sw,sh = w*supersample,h*supersample
        pixels = np.full((sh,sw,3),246,dtype=np.uint8)
        depth = np.full((sh,sw),-1e20,dtype=np.float32)
        mask = np.zeros((sh,sw),dtype=np.int32)
        if entries:
            vertices=[];colors=[];ids=[]
            for actor,key in entries:
                v,c = self.geometry[key]
                vertices.append(v);colors.append(c);ids.append(np.full(len(v),self.ids[actor],np.int32))
            v = np.concatenate(vertices) @ camera
            v[:,:,0] = (((v[:,:,0]-center[0])*scale-shift_x)*crop_scale+w/2)*supersample
            v[:,:,1] = ((-(v[:,:,1]-center[1])*scale-shift_y)*crop_scale+h/2)*supersample
            v = np.ascontiguousarray(v,dtype=np.float32)
            colors=np.ascontiguousarray(np.concatenate(colors));ids=np.ascontiguousarray(np.concatenate(ids))
            C(len(v),v.ctypes.data,colors.ctypes.data,ids.ctypes.data,sw,sh,pixels.ctypes.data,depth.ctypes.data,mask.ctypes.data)
        im=Image.fromarray(pixels)
        if supersample>1:
            im=im.resize(size,Image.Resampling.LANCZOS)
            mask=mask[supersample//2::supersample,supersample//2::supersample].copy()
        return im,mask

    def inventory(self, ep):
        """Case-independent geometry cards; no current/target presence or pose."""
        actors=sorted(ep.actors,key=lambda a:ep.alias[a]);pages=[]
        for offset in range(0,len(actors),12):
            group=actors[offset:offset+12]
            image=Image.new('RGB',(1600,math.ceil(len(group)/4)*304),'white')
            draw=ImageDraw.Draw(image)
            for i,actor in enumerate(group):
                # Catalogue pose order is randomized and unrelated to the goal.
                keys=sorted(ep.case['choices'][actor],key=ep.pose)
                key=keys[0];x=(i%4)*400;y=(i//4)*304
                im,_=self.rgb({actor:key},size=(400,280),only=actor,frame_keys=[key],fixtures=False)
                image.paste(im,(x,y+24))
                draw.text((x+8,y+4),ep.alias[actor],font=FONT,fill='#17283a')
            pages.append(image)
        return pages

    def pick(self, ep, action):
        _,mask=self.rgb(ep.assignments(),view=action.get('view','isometric'),
                        angles=(action['azimuth'],action['elevation']) if 'azimuth' in action else None,
                        crop=action.get('crop'),supersample=1)
        x,y=action['point'];value=mask[min(SIZE[1]-1,int(y*SIZE[1])),min(SIZE[0]-1,int(x*SIZE[0]))]
        return next((a for a in ep.actors if self.ids[a]==value),None)


def observe(ep):
    # Only anonymous action handles; no shape names/colors/transforms/relations.
    handles=[{'id':ep.alias[a],'candidates':sorted(ep.pose(k) for k in ep.case['choices'][a])}
             for a in sorted(ep.actors,key=lambda a:ep.alias[a])]
    return {'task':'Repair current to match target, then finish.','mode':'static','track':'visual',
            'protocol':VERSION,'actionHandles':handles,'manipulationsUsed':ep.manipulations,
            'inspectionsUsed':ep.inspections,'recentFeedback':ep.history[-8:],
            'availableViews':list(VIEWS),'maxActionsPerResponse':8,
            'inspectionProtocol':'uniform-part-isolation-on-request',
            'responseSchema':{'actions':[{'type':'detach','view':'front','point':[.5,.5]},
                {'type':'attach','partId':'Axx','candidate':'Cxxx'},
                {'type':'inspect','view':'front','crop':[.25,.25,.75,.75]},
                {'type':'inspect','candidate':'Cxxx'}, {'type':'inspect','partId':'Axx'},
                {'type':'inspect','azimuth':45,'elevation':20},{'type':'finish'}]}}


def temporal_pair(renderer, previous_state, current_state, view, left_label=None):
    """One visibly labeled panel keeps the two compared states in a fixed order."""
    size=(800,600)
    current=renderer.rgb(current_state,view,size=size,supersample=1)[0]
    previous=(renderer.rgb(previous_state,view,size=size,supersample=1)[0]
              if previous_state is not None else Image.new('RGB',size,(238,241,244)))
    panel=Image.new('RGB',(1600,636),'white')
    panel.paste(previous,(0,36));panel.paste(current,(800,36))
    draw=ImageDraw.Draw(panel)
    draw.rectangle((0,0,1599,35),fill=(27,43,57))
    draw.text((18,8),left_label or ('BEFORE LAST ACTION' if previous_state is not None else 'NO PRIOR ACTION'),font=FONT,fill='white')
    draw.text((818,8),'ACTUAL NOW' if left_label else 'CURRENT NOW',font=FONT,fill='white')
    draw.line((800,0,800,636),fill=(27,43,57),width=3)
    return panel


def temporal_target(renderer, goal, view):
    scene=renderer.rgb(goal,view,size=(800,600),supersample=1)[0]
    panel=Image.new('RGB',(800,636),'white');panel.paste(scene,(0,36))
    draw=ImageDraw.Draw(panel)
    draw.rectangle((0,0,799,35),fill=(27,43,57))
    draw.text((18,8),'FINAL TARGET',font=FONT,fill='white')
    return panel


def images(ep, renderer, directory, extra=None, views=INITIAL_VIEWS, previous_state=None, paired_layout=False, expected_state=None, matched_layout=False):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    records=[]
    def save(image,role,**meta):
        stream=io.BytesIO();image.save(stream,format='PNG');data=stream.getvalue()
        digest=hashlib.sha256(data).hexdigest();name=f'images/{digest}.png'
        path=directory/name;path.parent.mkdir(exist_ok=True)
        if not path.exists():path.write_bytes(data)
        records.append({'file':name,'role':role,'width':image.width,'height':image.height,
                        'sha256':digest,'detail':'high',**meta})
    current,goal=ep.assignments(),ep.case['goal']
    for view in views:
        if matched_layout:
            from matched_canvas import comparison, panels
            save(comparison(renderer,current,goal,view,'CURRENT NOW','TARGET (required final state)'),
                 'current-target',view=view,panels=panels('current-now','target'))
            prior=expected_state if expected_state is not None else previous_state
            if prior is not None:
                expected_mode=expected_state is not None
                left='expected-after-action' if expected_mode else 'before-last-action'
                save(comparison(renderer,prior,current,view,
                     'EXPECTED AFTER YOUR ACTION' if expected_mode else 'BEFORE LAST ACTION','CURRENT NOW'),
                     'expected-current' if expected_mode else 'temporal-pair',view=view,
                     panels=panels(left,'current-now'))
        elif paired_layout:
            comparison=expected_state if expected_state is not None else previous_state
            expected_mode=expected_state is not None
            save(temporal_pair(renderer,comparison,current,view,
                 left_label='EXPECTED AFTER YOUR ACTION' if expected_mode else None),
                 'temporal-pair',view=view,
                 layout='left-expected-after-action/right-actual-now' if expected_mode else 'left-before-last-action/right-current-now')
            save(temporal_target(renderer,goal,view),'target',view=view)
        else:
            if previous_state is not None:
                save(renderer.rgb(previous_state,view)[0],'before-last-action',view=view)
            for role,state in [('current',current),('target',goal)]:
                save(renderer.rgb(state,view)[0],role,view=view)
    for i,page in enumerate(renderer.inventory(ep)):
        save(page,'inventory',page=i+1)
    if extra:
        a=ep.internal_action(extra)
        kwargs={'view':a.get('view','isometric'),'crop':a.get('crop')}
        if 'azimuth' in a:kwargs['angles']=(a['azimuth'],a['elevation'])
        if 'candidate' in a:
            k=a['candidate'];actor=ep.cert['candidates'][k]['actor']
            # All options have identical previews. No goal/current occupancy flag.
            preview={**current,actor:k}
            save(renderer.rgb(preview,**kwargs)[0],'candidate-preview',candidate=extra['candidate'])
        else:
            if 'partId' in a:kwargs['only']=a['partId']
            inspection_states=[('current',current)] if getattr(renderer,'no_target_isolation',False) else [('current',current),('target',goal)]
            for role,state in inspection_states:
                meta={'view':a.get('view','isometric')}
                for key in ('partId','crop','azimuth','elevation'):
                    if key in extra:meta[key]=extra[key]
                save(renderer.rgb(state,**kwargs)[0],role+'-inspection',**meta)
            if 'partId' in extra and hasattr(renderer,'catalog'):
                for page,image in enumerate(renderer.catalog(ep,extra['partId']),1):
                    save(image,'candidate-catalog',partId=extra['partId'],page=page)
    return records


def request_body(model, observation, records, directory):
    if observation.get('protocol')!=VERSION or not records:
        raise ValueError('Only V3 visual requests with images are accepted')
    content=[{'type':'text','text':json.dumps(observation,separators=(',',':'))}]
    for record in records:
        content.append({'type':'text','text':json.dumps({k:v for k,v in record.items() if k not in ('file','sha256','detail')},separators=(',',':'))})
        data=(Path(directory)/record['file']).read_bytes()
        if hashlib.sha256(data).hexdigest()!=record['sha256']:raise ValueError('Image checksum mismatch')
        content.append({'type':'image_url','image_url':{'url':'data:image/png;base64,'+base64.b64encode(data).decode(),'detail':'high'}})
    return {'model':model,'messages':[{'role':'system','content':SYSTEM},{'role':'user','content':content}]}


def qualify(ep, renderer):
    """Private admission gate. Never copy root-level evidence into the prompt."""
    current,goal=ep.assignments(),ep.case['goal'];rows=[];cache={}
    def pixels(actor,key,view):
        signature=(actor,key,view)
        if signature not in cache:
            cache[signature]=np.asarray(renderer.rgb({actor:key},view,only=actor)[0]).astype(np.int16)
        return cache[signature]
    for root in ep.original_case['roots']:
        best=0;tested=0
        for actor in root.get('affectedActors',[root['partId']]):
            for view in VIEWS:
                delta=np.abs(pixels(actor,current.get(actor,''),view)-pixels(actor,goal.get(actor,''),view))
                best=max(best,int(np.count_nonzero(np.max(delta,axis=2)>=24)));tested+=1
                if best>=128:break
            if best>=128:break
        rows.append({'observableWithUniformInspection':best>=128,'changedPixels':best,'viewsChecked':tested})
    return {'protocol':VERSION,'resolution':list(SIZE),'rgbThreshold':24,'minimumChangedPixels':128,
            'passed':all(r['observableWithUniformInspection'] for r in rows),'roots':rows,
            'scope':'Uniform isolated inspection; does not certify exterior-only visibility or VLM accuracy.'}
