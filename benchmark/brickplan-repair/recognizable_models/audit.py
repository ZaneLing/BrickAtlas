"""Check completeness, physical witnesses and the actual public image packets."""
from collections import Counter
import hashlib
import json
import shutil
import numpy as np
import meshlib.mrmeshpy as mm
from meshlib import mrmeshnumpy
from recognizable_models import ROOT,OUT
from recognizable_models.run_episode import load_episode
from expansion_v7.build import read,write,states_for,run_witness
from expansion_v7.runtime import runtime,execute
from geometry import data_dir,mesh_for,xf


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    rows=[];case_counts=Counter()
    for meta in read(OUT/'admission-screen.json')['admitted']:
        mid=meta['id'];folder=OUT/'models'/mid
        cert=read(folder/'certificate.private.json.gz');rt=runtime(cert)
        manual=read(folder/'manual.private.json.gz');cases=read(folder/'cases.private.json.gz')
        mf=read(ROOT/'web/public/models'/meta['model']/'manifest.json')
        goals=[r for r in cert['candidates'].values() if r['kind']=='goal']
        assert len(goals)==len(mf['instances'])==meta['parts']
        assert not rt.cert['fixed'] and not any(manual['states'][0].values())
        assert not cert['conservativeContext']
        assert {r['part']['sourceIndex'] for r in goals}==set(range(meta['parts']))
        for r in goals:
            original=mf['instances'][r['part']['sourceIndex']]
            assert r['part']['originalMatrix']==original['originalMatrix']
            assert r['part']['partNumber']==original['partNumber']
            assert r['part']['colorCode']==original['colorCode']
        assert digest(ROOT/cert['source']['original'])==cert['source']['originalSha256']
        assert digest(ROOT/'web/public/models'/meta['model']/'manifest.json')==cert['source']['manifestSha256']
        for case in cases:
            case_counts[case['mode']]+=1
            if case['mode']=='dynamic':run_witness(cert,case,manual['actions'],rt.q)
            else:
                final,_=execute(rt,case['initial'],case['referenceActions'])
                assert rt.signature(final)==rt.signature(case['goal'])
        alternate=False
        control=next(c for c in cases if c['mode']=='dynamic' and c['family']=='control')
        for i in range(len(manual['actions'])-1):
            actions=list(manual['actions']);actions[i:i+2]=reversed(actions[i:i+2])
            try:run_witness(cert,control,actions,rt.q);alternate=True;break
            except AssertionError:continue
        rows.append(dict(id=mid,sourceParts=meta['parts'],sourcePartsDropped=0,
            noSourcePartInstalledInitially=True,allPosesAndColorsUnchanged=True,
            cases=len(cases),allReferenceReplaysPassed=True,alternateLegalOrderVerified=alternate))
    # The source explicitly includes the solid stud cap. Repair a single proxy
    # face, preserving vertex bytes and the original on-disk inset mesh.
    path=data_dir()/'inset/3003.ply';before_hash=digest(path)
    raw=mm.loadMesh(str(path));raw.transform(xf(np.diag([1.,1.,-1.,1.])))
    fixed=mesh_for('3003')[0]
    assert len(mrmeshnumpy.getNumpyFaces(fixed.topology))==len(mrmeshnumpy.getNumpyFaces(raw.topology))+1
    assert np.array_equal(mrmeshnumpy.getNumpyVerts(raw),mrmeshnumpy.getNumpyVerts(fixed))
    assert fixed.topology.isClosed() and before_hash==digest(path)
    evidence=['parts/3003.dat','parts/s/3003s01.dat','parts/s/3003s02.dat',
        'p/stug-2x2.dat','p/stud.dat','p/4-4disc.dat']
    proxy=dict(part='3003',addedFaces=1,verticesUnchanged=True,sourceMeshFileUnchanged=True,
        proxySha256=before_hash,sourceEvidence={p:digest(ROOT/'assets-source/ldraw-library/locked'/p) for p in evidence})
    packets=[];public=read(OUT/'public/models.json')
    sample_ids=[next(c['id'] for c in read(OUT/'case-index.json')['cases'] if c['module']==m['id'] and c['mode']=='dynamic' and c['family']=='control') for m in rows]
    sample_ids+=['cottage-roof-dynamic-control','racer-top-dynamic-control']
    sample_ids+=[next(c['id'] for c in read(OUT/'case-index.json')['cases'] if c['mode']=='static' and c['family']=='missing')]
    for cid in sample_ids:
        ep,packet=load_episode(cid,directory=OUT/'interface-evidence'/cid.replace('::','-'))
        obs=packet.observation()
        assert not {'family','events','goal','initial','referenceActions','eventApplied','score'}&set(obs)
        assert obs['intermediateGTMatching'] is False
        if ep.case['mode']=='static':assert '不是从空白底板重搭' in obs['task']
        assets=OUT/'public/native-inputs';assets.mkdir(exist_ok=True)
        for im in obs['images']:
            original=__import__('pathlib').Path(im['file']);assert digest(original)==im['sha256']
            target=assets/original.name;shutil.copyfile(original,target)
            im['file']=str(target.relative_to(OUT/'public'))
        obs['assetPathBase']='..'  # Paths resolve from the public output root.
        file=assets/(cid.replace('::','-')+'.json');write(file,obs)
        if ep.case['mode']=='dynamic':
            row=next(m for m in public['models'] if m['id']==ep.case['module'])
            row['nativeInput']=str(file.relative_to(OUT/'public'))
        packets.append(dict(caseId=cid,images=len(obs['images']),file=str(file.relative_to(OUT)),
            hiddenAnswerFieldsAbsent=True,fullObjectContext=True,
            contextType='preassembled-body' if ep.case['module'] in ('cottage-roof','racer-top') else 'complete-source-goal')))
    write(OUT/'public/models.json',public)
    write(OUT/'audit.json',dict(status='PASS',models=rows,newCaseCounts=dict(case_counts),
        collisionProxyRepair=proxy,nativePackets=packets,apiCalls=0,
        humanValidated=False,modelEvaluated=False,historicalReferenceDataRewritten=False))
    # Keep the historical source manifest unchanged: it describes its original
    # build. Record the code used by this extension and its native adapter here.
    paths=list((ROOT/'benchmark/brickplan-repair/recognizable_models').glob('*'))
    paths += [ROOT/'benchmark/brickplan-v1/geometry.py',ROOT/'benchmark/brickplan-repair/public_preview_server.py']
    write(OUT/'source-manifest.json',dict(files={str(p.relative_to(ROOT)):digest(p) for p in paths if p.is_file()},
        historicalCommunityManifest=dict(path='deliverables/brickplan-community-modules/source-manifest.json',
            sha256=digest(ROOT/'deliverables/brickplan-community-modules/source-manifest.json'),unchanged=True),
        change='Adds guarded, source-verified 3003 proxy stud cap. Historical case states and witnesses are unchanged; this is not a full historical replay.'))
    print('AUDIT PASS',len(rows),'complete models',dict(case_counts),len(packets),'native packets',flush=True)


if __name__=='__main__':main()
