"""Repair only small collision-mesh holes backed by original LDraw surfaces.

The new triangles must stay within the existing 0.25-LDU inset tolerance of a
parallel original surface at dense barycentric samples. No vertices are moved;
large holes, unmatched surfaces, non-triangular facets after filling, or still
open outputs remain unsupported. This is a representation repair, not a change
of the source model or a substitute for physical validation.
"""
from pathlib import Path
import argparse,hashlib,json,re
import numpy as np
import meshlib.mrmeshpy as mm
import meshlib.mrmeshnumpy as mn
from scaling_release import ROOT,OUT
from expansion_v7.build import read,write
from community_modules.core import raw_part
from geometry import data_dir,xf
from render import ldraw
DEST=ROOT/'assets-source/qualified-collision'


def repair(stem):
 src=data_dir()/'inset'/f'{stem}.ply'
 if not src.exists():return dict(part=stem,status='missing-mesh')
 mesh=mm.loadMesh(str(src));mesh.transform(xf(np.diag([1.,1.,-1.,1.])))
 if mesh.volume()<0:mesh.topology.flipOrientation()
 holes=mesh.topology.findHoleRepresentiveEdges()
 if not holes:return dict(part=stem,status='already-closed')
 if len(holes)>24:return dict(part=stem,status='too-many-holes',holes=len(holes))
 vertices=mn.getNumpyVerts(mesh);before=mn.getNumpyFaces(mesh.topology);original_faces={tuple(sorted(f)) for f in before}
 for h in holes:
  ring=mesh.topology.getLeftRing(h)
  if not 3<=len(ring)<=12:return dict(part=stem,status='large-hole',boundary=len(ring))
  mm.fillHole(mesh,h)
 if not mesh.topology.isClosed():return dict(part=stem,status='still-open')
 if not np.array_equal(vertices,mn.getNumpyVerts(mesh)):return dict(part=stem,status='vertices-changed')
 after=mn.getNumpyFaces(mesh.topology);new=np.array([f for f in after if tuple(sorted(f)) not in original_faces]);triangles=vertices[new]
 raw=ldraw.triangles(stem+'.dat')[0];t=np.concatenate([np.asarray(v,dtype=np.float64).reshape(-1,3,3) for v in raw.values()])
 rawmesh=mn.meshFromFacesVerts(np.arange(t.size//3,dtype=np.int32).reshape(-1,3),t.reshape(-1,3))
 rawfaces=mn.getNumpyFaces(rawmesh.topology);rawverts=mn.getNumpyVerts(rawmesh)
 distances=[];min_normal=1.
 for tri in triangles:
  normal=np.cross(tri[1]-tri[0],tri[2]-tri[0]);norm=np.linalg.norm(normal)
  if norm<1e-8:continue
  normal/=norm
  # Include boundary and interior samples; interpolation spacing <= 1 LDU.
  steps=max(8,min(64,int(np.ceil(max(np.linalg.norm(tri[i]-tri[j]) for i in range(3) for j in range(3))))))
  for i in range(steps+1):
   for j in range(steps+1-i):
    pos=tri[0]+(tri[1]-tri[0])*i/steps+(tri[2]-tri[0])*j/steps
    proj=mm.findProjection(mm.Vector3f(*pos),rawmesh)
    distance=float(np.sqrt(proj.distSq));distances.append(distance)
    if distance>np.sqrt(3)*.25+.005:return dict(part=stem,status='no-source-surface',distance=distance)
    # Closest surface normal at an edge may be orthogonal. Interior samples
    # must have a corresponding plane normal, never just be near an edge.
    if min(i,j,steps-i-j)>0:
     nv=rawmesh.normal(proj.proj.face);rn=np.array([nv.x,nv.y,nv.z]);rn/=max(np.linalg.norm(rn),1e-12)
     aligned=abs(float(rn@normal));min_normal=min(min_normal,aligned)
     if aligned<.94:return dict(part=stem,status='source-normal-mismatch',alignment=aligned)
 record=dict(part=stem,status='verified',holes=len(holes),addedTriangles=len(new),originalMeshSha256=hashlib.sha256(src.read_bytes()).hexdigest(),sourcePartSha256=hashlib.sha256((ROOT/'assets-source/ldraw-library/locked/parts'/f'{stem}.dat').read_bytes()).hexdigest(),verticesMoved=0,maxSourceSurfaceDistanceLDU=max(distances,default=0),minInteriorNormalAgreement=min_normal,samples=len(distances),closed=True,method='sampled-source-surface-backed-hole-repair/1')
 # Store in the same convention as the upstream inset library.
 mesh.transform(xf(np.diag([1.,1.,-1.,1.])));mesh.topology.flipOrientation();DEST.mkdir(exist_ok=True)
 path=DEST/f'{stem}.ply';mm.saveMesh(mesh,str(path));record['repairedMeshSha256']=hashlib.sha256(path.read_bytes()).hexdigest();write(DEST/f'{stem}.json',record)
 return record


def main():
 p=argparse.ArgumentParser();p.add_argument('--parts',nargs='*');a=p.parse_args()
 if a.parts:parts=a.parts
 else:
  parts=set()
  for f in (OUT/'private').glob('*/prepare-failure.json'):
   text=f.read_text();parts.update(re.findall(r'Open collision mesh cannot be qualified: ([A-Za-z0-9_\-]+)',text))
  # Unsupported context reasons are in prepared certificate records as well.
  for f in (OUT/'private').glob('*/base-certificate.private.json.gz'):
   parts.update(re.findall(r'Open collision mesh cannot be qualified: ([A-Za-z0-9_\-]+)',json.dumps(read(f))))
  parts=sorted(parts)
 report=[]
 for stem in parts:
  try:r=repair(stem)
  except Exception as e:r=dict(part=stem,status='error',reason=str(e)[:200])
  report.append(r);print(stem,r['status'],flush=True)
 write(OUT/'collision-repair-audit.json',dict(parts=report,apiCalls=0))
if __name__=='__main__':main()
