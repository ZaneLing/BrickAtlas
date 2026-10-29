"""Mesh export of ArenaVision's finite visible patch of its white stud plate.

Matches the existing sensor's grid, board transform, pitch, radius and height.
Publication geometry only; no changes to episode state or collision rules.
"""
import math
import numpy as np

def add_plate(renderer):
 if not hasattr(renderer,'stud_radius'):return
 key='_publication_white_stud_plate'
 if key in renderer.geometry:return
 xs,zs=list(renderer.grid_x),list(renderer.grid_z)
 xm,zm=max(1,len(xs)//4),max(1,len(zs)//4)
 x0,x1=xs[xm]-.5,xs[-1-xm]+.5;z0,z1=zs[zm]-.5,zs[-1-zm]+.5
 faces=[]
 def face(a,b,c,d):faces.extend([[a,b,c],[a,c,d]])
 top=[(x0*20,0,z0*20),(x1*20,0,z0*20),(x1*20,0,z1*20),(x0*20,0,z1*20)]
 low=[(x,8,z) for x,y,z in top]
 face(*top);face(*low)
 for i in range(4):j=(i+1)%4;face(top[i],top[j],low[j],low[i])
 radius=renderer.stud_radius*20;height=renderer.stud_height
 for x in xs:
  for z in zs:
   if not(x0<x<x1 and z0<z<z1):continue
   ring=[(x*20+radius*math.cos(i*math.tau/24),z*20+radius*math.sin(i*math.tau/24)) for i in range(24)]
   for i in range(24):
    j=(i+1)%24;a,b=ring[i],ring[j]
    face((a[0],0,a[1]),(b[0],0,b[1]),(b[0],-height,b[1]),(a[0],-height,a[1]))
    faces.append([(x*20,-height,z*20),(a[0],-height,a[1]),(b[0],-height,b[1])])
 v=np.array(faces,dtype=np.float32);ones=np.ones((*v.shape[:2],1))
 v=(np.concatenate([v,ones],axis=2)@renderer.board.T)[...,:3]*[1,-1,-1]
 n=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-8)
 light=np.array([.3,.8,.5]);light/=np.linalg.norm(light);shade=.6+.4*np.abs(n@light)
 c=np.repeat((shade*248)[:,None],3,axis=1).astype(np.uint8)
 renderer.geometry[key]=(v.astype(np.float32),c)
 renderer.bounds[key]=v.reshape(-1,3)
 renderer.cert={**renderer.cert,'fixed':{**renderer.cert['fixed'],key:dict(publicationPlate=True)}}
