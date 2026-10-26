"""Manifold Boolean spot checks, independent of MeshLib's collision/path verdict.

Same documented inset-mesh inputs, a different Boolean backend. The continuous
sweep is the union of the endpoints and the triangular-face translation prisms;
it is neither a bounding-box rejection nor a few sampled animation frames.
It does not certify real clutch forces, gravity, flexible joints, or mesh truth.
"""
from functools import lru_cache
import hashlib
import json
import importlib.metadata
import numpy as np
import manifold3d as m
from meshlib import mrmeshnumpy
from community_modules.core import ModuleAssembly  # initializes local geometry paths
from geometry import mesh_for

EPS_VOLUME=1e-4


@lru_cache(maxsize=256)
def canonical(name):
    mesh,*_,file_hash=mesh_for(name)
    vertices=np.asarray(mrmeshnumpy.getNumpyVerts(mesh),dtype=np.float32)
    faces=np.asarray(mrmeshnumpy.getNumpyFaces(mesh.topology),dtype=np.uint32)
    solid=m.Manifold(m.Mesh(vertices,faces))
    if solid.status()!=m.Error.NoError or solid.volume()<=0:
        raise ValueError('Independent backend cannot interpret solid '+name)
    return solid,vertices,faces,file_hash


def world(part):
    solid,vertices,faces,h=canonical(part['canonical'])
    matrix=np.asarray(part['matrix'])
    return solid.transform(matrix[:3,:].tolist()), vertices@matrix[:3,:3].T+matrix[:3,3], faces,h


def separate(a,b):
    return bool(np.any(a[1]<b[0]) or np.any(b[1]<a[0]))


def sweep(solid,vertices,faces,delta):
    delta=np.asarray(delta,dtype=float)
    translated=solid.translate(delta.tolist())
    pieces=[solid,translated]
    for tri in vertices[faces]:
        if abs(np.dot(np.cross(tri[1]-tri[0],tri[2]-tri[0]),delta))<1e-8:
            continue
        prism=m.Manifold.hull_points(np.vstack([tri,tri+delta]).tolist())
        if not prism.is_empty():pieces.append(prism)
    result=m.Manifold.batch_boolean(pieces,m.OpType.Add)
    if result.status()!=m.Error.NoError:raise ValueError('Independent sweep construction failed')
    return result


def check(rt,state,action,engine_result):
    actor=action['actor'];key=state.get(actor) if action['type']=='detach' else action['candidate']
    moving=rt.row(key)['part'];solid,vertices,faces,h=world(moving)
    endpoints=(vertices.min(0),vertices.max(0))
    others=rt.present({**state,actor:''})
    checks=[];unknown=[]
    def intersections(body,bounds):
        hits=[]
        for aid,part in others.items():
            try:
                other,v,_,_=world(part);box=(v.min(0),v.max(0))
                if separate(bounds,box):continue
                volume=(body^other).volume()
                if volume>EPS_VOLUME:hits.append(dict(actor=aid,intersectionVolumeLDU3=volume))
            except (ValueError,KeyError) as exc:unknown.append(dict(actor=aid,reason=str(exc)))
        for aid,p in rt.cert.get('conservativeContext',{}).items():
            box=tuple(np.asarray(x) for x in p['bounds'])
            if not separate(bounds,box):unknown.append(dict(actor=aid,reason='Unqualified visual-context mesh overlaps tested region'))
        return hits
    endpoint_hits=intersections(solid,endpoints)
    baseplane=False
    if rt.cert.get('environmentMode')=='white-baseplate' or hasattr(rt,'baseplate'):
        local=(np.c_[vertices,np.ones(len(vertices))]@np.asarray(rt.inverse_board).T)[:,:3]
        baseplane=bool(local[:,1].max()>.002)
    elif rt.cert.get('tableY') is not None:
        baseplane=bool(vertices[:,1].max()>rt.cert['tableY']+.002)
    if baseplane:endpoint_hits.append(dict(actor='environment-solid-plane',intersectionVolumeLDU3=None))
    directions=[]
    if engine_result.get('path'):
        directions.append((engine_result['path'],engine_result['pathLengthLDU']))
    else:
        mat=np.asarray(moving['matrix'])
        for i in range(3):
            for sign in [-1,1]:directions.append(((mat[:3,i]*sign).tolist(),rt.cert['extractionLengthLDU']))
    for direction,length in directions:
        d=np.asarray(direction,dtype=float);d=d/np.linalg.norm(d);delta=d*length
        bounds=(np.minimum(endpoints[0],endpoints[0]+delta),np.maximum(endpoints[1],endpoints[1]+delta))
        path_solid=sweep(solid,vertices,faces,delta)
        hits=intersections(path_solid,bounds)
        plane_hit=False
        if hasattr(rt,'inverse_board') and hasattr(rt,'baseplate'):
            inv=np.asarray(rt.inverse_board);local=(np.c_[vertices,np.ones(len(vertices))]@inv.T)[:,:3]
            end=local+(inv[:3,:3]@delta)
            plane_hit=max(local[:,1].max(),end[:,1].max())>.002
            # Independently instantiated stud tiles near the entire swept box.
            all_local=np.vstack([local,end]);lo,hi=all_local.min(0),all_local.max(0)
            if hi[1]>=-4.002 and not plane_hit:
                for x in range(int(np.ceil((lo[0]-10)/20)),int(np.floor((hi[0]+10)/20))+1):
                    for z in range(int(np.ceil((lo[2]-10)/20)),int(np.floor((hi[2]+10)/20))+1):
                        pose=np.eye(4);pose[:3,3]=[20*x,0,20*z]
                        tile=canonical('3024')[0].transform((np.asarray(rt.board)@pose)[:3].tolist())
                        volume=(path_solid^tile).volume()
                        if volume>EPS_VOLUME:hits.append(dict(actor='environment-stud',intersectionVolumeLDU3=volume))
        elif rt.cert.get('tableY') is not None:
            plane_hit=max(vertices[:,1].max(),(vertices+delta)[:,1].max())>rt.cert['tableY']+.002
        if plane_hit:hits.append(dict(actor='environment-solid-plane',intersectionVolumeLDU3=None))
        checks.append(dict(direction=d.tolist(),lengthLDU=float(length),hits=hits,
                           collisionFreeOnTestedSolids=not hits))
        if not hits:break
    clear=bool(not endpoint_hits and any(c['collisionFreeOnTestedSolids'] for c in checks) and not unknown)
    code=engine_result['code']
    status=('agrees-on-accepted-geometry' if clear and code=='OK' else
            'accepted-action-has-independent-collision' if code=='OK' and (endpoint_hits or checks and all(c['hits'] for c in checks)) else
            'rejected-endpoint-overlap-confirmed' if code=='ENDPOINT_COLLISION' and endpoint_hits else
            'rejected-path-blockage-on-tested-axes' if code=='PATH_BLOCKED' and checks and all(c['hits'] for c in checks) and not unknown else
            'needs-review')
    return dict(backend='manifold3d',backendVersion=importlib.metadata.version('manifold3d'),
        algorithm='closed-solid Boolean intersections; complete linear sweep from triangular face prisms',
        status=status,engineCode=code,endpointHits=endpoint_hits,pathChecks=checks,unresolved=unknown,
        inputMeshSha256=h,intersectionToleranceLDU3=EPS_VOLUME,
        realPhysicsQualified=False,connectorSemanticsIndependentlyQualified=False,
        scope='Independent volume/path spotcheck on shared inset meshes; same source-mesh defects or force assumptions are not independently resolved.')


def calibrate():
    # Thin obstacles between distant endpoints must be detected by the sweep.
    cube=m.Manifold.cube([2,2,2],True);mesh=cube.to_mesh();v=np.asarray(mesh.vert_properties)[:,:3]
    swept=sweep(cube,v,np.asarray(mesh.tri_verts),[20,0,0])
    obstacle=m.Manifold.cube([.1,4,4],True).translate([7.1,0,0])
    assert (cube^obstacle).volume()==0 and (cube.translate([20,0,0])^obstacle).volume()==0
    assert (swept^obstacle).volume()>.01
    clear=m.Manifold.cube([2,2,2],True).translate([7,8,0])
    assert (swept^clear).volume()==0
    return dict(thinMidPathObstacleDetected=True,clearPathAccepted=True,notFrameSampling=True)
