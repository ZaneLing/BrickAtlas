"""Regression checks for figure exclusion, physical mesh repair and active tasks."""
import json
import numpy as np
from dynamic_arena import ROOT,OUT
from dynamic_arena.curate_sources import FigureAudit,BODY
from expansion_v7.build import read
from bench_design.selection import retired,require_active
from geometry import mesh_for,xf,data_dir
import meshlib.mrmeshpy as mm

for name in ['Minifig Torso','~Minifig Leg Right (Obsolete)','Figure Friends Female Head with Pattern','Figure Friends Girl Torso','Minifig Statuette','Technic Figure Torso']:
    assert BODY.search(name),name
for name in ['Minifig Seat 2 x 2','Minifig Cup','Minifig Hand Truck','Brick 1 x 1 with Headlight','Minifig Mechanical Arm with Clips Parallel','Figure Friends Cutlery Fork']:
    assert not BODY.search(name),name
A=FigureAudit();data=read(OUT/'source-library.json');rows=data['models']
assert len(rows)==len({r['setNumber'] for r in rows})==data['count']
assert all(A.audit(r)['status']=='no-figure-parts-found' for r in rows)
withdrawn=read(OUT/'source-curation.json')['withdrawn'];assert not ({r['setNumber'] for r in rows}&{r['setNumber'] for r in withdrawn})
for r in withdrawn:
    assert retired(model=r['id'],source='set:'+r['setNumber'].split('-')[0])
for c in read(OUT/'catalogue.json')['cases']:assert not retired(c['caseId'],c['model'],c['source'])
raw=mm.loadMesh(str(data_dir()/'inset/3003pe2.ply'));raw.transform(xf(np.diag([1.,1.,-1.,1.])))
if raw.volume()<0:raw.topology.flipOrientation()
assert len(raw.topology.findHoleRepresentiveEdges())==1
before=[(p.x,p.y,p.z) for p in raw.points]
fixed,*_=mesh_for('3003pe2');assert fixed.topology.isClosed()
assert before==[(p.x,p.y,p.z) for p in fixed.points], 'Collision fix must not move source vertices'
assert fixed.topology.numValidFaces()==raw.topology.numValidFaces()+1
print('PASS figure bodies/accessories, all active inventories, withdrawn task filtering, exact one-triangle stud repair')
