"""Deterministic original-LDraw RGB/depth renderer; no physics simulation."""
from pathlib import Path
from functools import lru_cache
import ctypes, hashlib, importlib.util, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
LIB=HERE/'raster.so'
if not LIB.exists() or LIB.stat().st_mtime < (HERE/'raster.c').stat().st_mtime:
    subprocess.run(['cc','-O3','-shared','-fPIC',str(HERE/'raster.c'),'-o',str(LIB),'-lm'],check=True)
C=ctypes.CDLL(str(LIB)).raster
C.argtypes=[ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
spec=importlib.util.spec_from_file_location('ldraw_pixels',ROOT/'benchmark/brickplan-v1/render_assets.py')
ldraw=importlib.util.module_from_spec(spec);spec.loader.exec_module(ldraw)
VIEWS={'isometric':(35,30),'front':(0,0),'rear':(180,0),'left':(-90,0),'right':(90,0),'top':(0,90),'bottom':(0,-90)}
PALETTE={'0':'#202326','1':'#0055bf','4':'#c91a09','7':'#9ba19d','14':'#f2cd37','15':'#ffffff','71':'#a0a5a9','72':'#6c6e68'}
FONT=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',14) if Path('/System/Library/Fonts/Helvetica.ttc').exists() else ImageFont.load_default(size=14)

def rgb(h):return np.array([int(h.lstrip('#')[i:i+2],16) for i in (0,2,4)],dtype=float)

@lru_cache(maxsize=2048)
def triangles(part_json):
    part=json.loads(part_json);matrix=np.array(part['rawMatrix']);verts=[];colors=[]
    for color,values in ldraw.triangles(part['partNumber']+'.dat')[0].items():
        v=np.array(values).reshape(-1,3) @ matrix[:3,:3].T+matrix[:3,3]
        v*=np.array([1,-1,-1]);v=v.reshape(-1,3,3)
        normal=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-8)
        light=np.array([.3,.8,.5]);light/=np.linalg.norm(light)
        shade=.6+.4*np.abs(normal@light)
        colors.append(np.clip(rgb(part['colorHex'] if color=='16' else PALETTE.get(color,part['colorHex']))[None,:]*shade[:,None],0,255).astype('uint8'))
        verts.append(v)
    return np.concatenate(verts).astype('float32'),np.concatenate(colors)

class Renderer:
    def __init__(self,cert):
        self.cert=cert
        self.parts={**{k:v for k,v in cert['fixed'].items() if not v.get('virtual')},**{k:r['part'] for k,r in cert['candidates'].items()}}
        self.geometry={k:triangles(json.dumps(p,sort_keys=True)) for k,p in self.parts.items()}
        goalkeys=[k for k in cert['fixed'] if k in self.parts]+[k for k,r in cert['candidates'].items() if r['kind']=='goal']
        points=np.concatenate([self.geometry[k][0].reshape(-1,3) for k in goalkeys])
        self.center=(points.min(0)+points.max(0))/2
        self.extent=max(20,float(np.linalg.norm(points.max(0)-points.min(0))))
        self.ids={a:i+1 for i,a in enumerate(sorted(set(cert['fixed'])|{r['actor'] for r in cert['candidates'].values()}))}

    def render(self,state,view='isometric',size=(480,360),labels=None,only=None,angles=None):
        az,el=angles if angles is not None else VIEWS[view]
        az,el=np.deg2rad([az,el]);direction=np.array([np.sin(az)*np.cos(el),np.sin(el),np.cos(az)*np.cos(el)])
        right=np.array([np.cos(az),0,-np.sin(az)]);up=np.cross(direction,right)
        camera=np.stack([right,up,direction],axis=1)
        entries=[(a,k) for a,k in {**{a:a for a in self.cert['fixed']},**state}.items() if k and k in self.geometry and (only is None or a==only)]
        w,h=size;im=np.full((h,w,3),246,dtype=np.uint8);depth=np.full((h,w),-1e20,dtype=np.float32);mask=np.zeros((h,w),dtype=np.int32)
        if entries:
            vertices=[];colors=[];ids=[]
            for actor,key in entries:
                v,c=self.geometry[key];vertices.append(v);colors.append(c);ids.append(np.full(len(v),self.ids[actor],np.int32))
            center,extent=self.center,self.extent
            if only:
                keys=[k for k,r in self.cert['candidates'].items() if r['actor']==only]
                if keys:
                    pts=np.concatenate([self.geometry[k][0].reshape(-1,3) for k in keys]);center=(pts.min(0)+pts.max(0))/2;extent=max(20,float(np.linalg.norm(pts.max(0)-pts.min(0))))
            v=(np.concatenate(vertices)-center)@camera
            scale=min(w,h)*.86/extent
            v[:,:,0]=v[:,:,0]*scale+w/2;v[:,:,1]=-v[:,:,1]*scale+h/2
            v=np.ascontiguousarray(v,dtype=np.float32);col=np.ascontiguousarray(np.concatenate(colors));actorids=np.ascontiguousarray(np.concatenate(ids))
            C(len(v),v.ctypes.data,col.ctypes.data,actorids.ctypes.data,w,h,im.ctypes.data,depth.ctypes.data,mask.ctypes.data)
        image=Image.fromarray(im)
        if labels:
            draw=ImageDraw.Draw(image)
            for actor,_ in entries:
                yy,xx=np.where(mask==self.ids[actor])
                if len(xx)<18:continue
                # Place IDs only on visible surfaces: no x-ray outlines.
                index=len(xx)//2;x,y=int(xx[index]),int(yy[index]);label=labels.get(actor,actor)
                box=draw.textbbox((x,y),label,font=FONT);draw.rectangle(box,fill='white');draw.text((x,y),label,fill='#17283a',font=FONT)
        return image,mask

    def sheet(self,state,labels,title,size=(384,288)):
        sheet=Image.new('RGB',(size[0]*4,(size[1]+24)*2),'white');draw=ImageDraw.Draw(sheet)
        for i,view in enumerate(VIEWS):
            x=(i%4)*size[0];y=(i//4)*(size[1]+24)
            image,_=self.render(state,view,size,labels)
            sheet.paste(image,(x,y+24));draw.text((x+6,y+4),title+' / '+view,font=FONT,fill='#17283a')
        return sheet

    def pair(self,current,goal,actor,labels=None):
        sheet=Image.new('RGB',(960,768),'white');draw=ImageDraw.Draw(sheet)
        for i,view in enumerate(('isometric','front')):
            for j,(state,title) in enumerate(((current,'CURRENT'),(goal,'TARGET'))):
                im,_=self.render(state,view,(480,360),labels,actor)
                sheet.paste(im,(j*480,i*384+24));draw.text((j*480+8,i*384+4),f'{title} / {labels.get(actor,actor) if labels else actor} / {view}',font=FONT,fill='black')
        return sheet

    def atlas(self,current,goal,labels):
        actors=sorted(current,key=lambda a:labels[a]);tile=(128,112);stride=256;rowh=140
        sheet=Image.new('RGB',(stride*4,math.ceil(len(actors)/4)*rowh),'white');draw=ImageDraw.Draw(sheet)
        for i,a in enumerate(actors):
            x=(i%4)*stride;y=(i//4)*rowh
            for j,(state,title) in enumerate(((current,'current'),(goal,'target'))):
                im,_=self.render(state,'isometric',tile,only=a)
                sheet.paste(im,(x+j*128,y+24));draw.text((x+j*128+3,y+3),labels[a]+' / '+title,font=FONT,fill='black')
        return sheet
