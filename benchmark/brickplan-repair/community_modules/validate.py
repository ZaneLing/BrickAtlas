"""Regression checks for flexible order, physical actions, and public adapter."""
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('community_build',HERE/'build.py')
b=importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def check_inspect_timing(cert,cases):
    case=next(c for c in cases if c['mode']=='static' and c['family']=='missing')
    ep=b.Episode(cert,case,seed=41)
    ep.step(b.public_action(ep,case['referenceActions'][0]))
    current=dict(ep.state)
    assert ep.previous!=current
    ep.step(dict(type='inspect',view='isometric'))
    assert ep.previous==current and ep.state==current
    ep.step(dict(type='inspect',view='top'))
    assert ep.previous==current and ep.state==current


def main():
    started=time.time()
    audit=json.loads((b.OUT/'audit.json').read_text())
    assert audit['status']=='PASS'
    modules=json.loads((b.OUT/'gallery-data.js.json').read_text())
    rows=[]
    for m in modules:
        d=b.OUT/m['id']
        cert=json.loads((d/'certificate.private.json').read_text())
        cases=json.loads((d/'cases.private.json').read_text())
        check_inspect_timing(cert,cases)
        normal=json.loads((d/'manual.private.json').read_text())['actions']
        evidence=b.order_checks(cert,cases,normal)
        m['orderChecks']=evidence
        b.dump(d/'order-checks.json',evidence)
        record=next(r for r in audit['results'] if r['module']==m['id'])
        record['orderChecks']=evidence
        moving=set(cert['source']['moduleSourceIndices'])
        fixed={p['sourceIndex'] for p in cert['fixed'].values()}
        unknown={p['part']['sourceIndex'] for p in cert['conservativeContext'].values()}
        assert moving.isdisjoint(fixed|unknown) and fixed.isdisjoint(unknown)
        assert moving|fixed|unknown==set(range(cert['source']['totalInstances']))
        assert b.sha256(d/'original.mpd')==cert['source']['originalSha256']
        assert cert['protocol']==b.PROTOCOL
        assert len(cases)==8 and len(m['cases'])==8
        for name,image in m['images'].items():
            assert b.sha256(b.OUT/image['file'])==image['sha256']
        rows.append(dict(module=m['id'],orderChecks='PASS',fullSourceCoverage='PASS',
                         imageHashes='PASS',differentPhysicalPrefixAtThreshold=evidence['differentPhysicalPrefixAtThreshold']))
        print('ORDER PASS',m['id'], 'different prefix',evidence['differentPhysicalPrefixAtThreshold'],flush=True)
    # Exercise the real line-oriented adapter, including an actual image preview.
    proc=subprocess.Popen([sys.executable,str(HERE/'run_episode.py'),'--module','repair-truck-cab',
                           '--condition','static-control','--seed','71'],
                          stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    line=proc.stdout.readline()
    if not line:
        raise AssertionError(proc.stderr.read())
    initial=json.loads(line)
    candidate=initial['handles'][0]['candidates'][0]
    remaining,err=proc.communicate(json.dumps(dict(type='inspect',view='rear',candidate=candidate))+'\n'+
                                   json.dumps(dict(type='finish'))+'\n',timeout=90)
    assert proc.returncode==0,err
    outputs=[initial]+[json.loads(line) for line in remaining.splitlines()]
    assert len(outputs)==3 and outputs[-1]['done'] and outputs[1]['feedback']['code']=='INSPECT'
    assert any(im['role']=='candidate-preview' for im in outputs[1]['images'])
    for obs in outputs:
        assert obs['protocol']==b.PROTOCOL and obs['intermediateGTMatching'] is False
        assert not set(obs).intersection({'event','family','goal','referenceActions','score'})
        for im in obs['images']:
            path=Path(im['file'])
            assert re.fullmatch(r'[0-9a-f]{64}\.png',path.name)
            assert path.is_file() and b.sha256(path)==im['sha256']
    record_path=Path(outputs[0]['images'][0]['file']).parent/'record.private.json'
    run=json.loads(record_path.read_text())
    assert run['score']['success']
    b.dump(b.OUT/'gallery-data.js.json',modules)
    audit.update(orderRegressionStatus='PASS',orderRegressionSeconds=round(time.time()-started,2),
                 differingPhysicalPrefixes=sum(r['differentPhysicalPrefixAtThreshold'] for r in rows))
    b.dump(b.OUT/'audit.json',audit)
    b.dump(b.OUT/'interface-checks.json',dict(status='PASS',protocol=b.PROTOCOL,modules=rows,
        localAdapter='PASS',firstObservationImages=len(initial['images']),candidatePreview='PASS',
        finalScore=run['score'],apiCalls=0,kind='automated-contract-check-not-human-or-model-evaluation'))
    docs_spec=importlib.util.spec_from_file_location('module_catalogue',HERE/'catalogue.py')
    docs=importlib.util.module_from_spec(docs_spec);docs_spec.loader.exec_module(docs);docs.main()
    shutil.copyfile(HERE/'index.html',b.OUT/'index.html')
    manifest=json.loads((b.OUT/'source-manifest.json').read_text())
    manifest[str((HERE/'validate.py').relative_to(b.ROOT))]=''
    for relative in ('benchmark/brickplan-repair/eval/matched_canvas.py',
                     'benchmark/brickplan-repair/evaluation_outcomes.py'):
        manifest[relative]=''
    b.dump(b.OUT/'source-manifest.json',{p:b.sha256(b.ROOT/p) for p in manifest})
    print('VALIDATION PASS',len(rows),round(time.time()-started,2),flush=True)


if __name__=='__main__':
    main()
