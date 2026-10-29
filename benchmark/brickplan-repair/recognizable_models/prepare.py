"""Preserve every source instance for complete objects; reject unsupported ones."""
from copy import deepcopy
from pathlib import Path
import argparse
import json
import sys
import numpy as np

from recognizable_models import ROOT, OUT
from recognizable_models.specs import WHOLE
from community_modules.core import source_certificate
from expansion_v7.prepare import find_order
from expansion_v7.runtime import runtime
from expansion_v7.build import write, read


def complete_certificate(spec):
    path = ROOT / 'web/public/models' / spec['model'] / 'manifest.json'
    mf = read(path)
    if len(mf['instances']) > 50:
        raise ValueError(f"{len(mf['instances'])} source parts exceeds the 50-part complete-object selection limit; use a named finishing module")
    md = mf['model']; source = mf.get('sourceFile')
    if not source:
        prov = read(path.with_name('provenance.json'))
        source = prov.get('source', {}).get('path')
    if not source:
        source = 'assets-source/brickplan-v23/original/' + md['setNumber'] + '.mpd'
    chosen = dict(**spec, indices=list(range(len(mf['instances']))), original=source,
        author=md['author'], url=md['sourceUrl'])
    cert = source_certificate(chosen)
    goals = {k:r for k,r in cert['candidates'].items() if r['kind']=='goal'}
    assert len(goals) == len(mf['instances']) and not cert['conservativeContext']
    # This is only the mounting frame used to derive the white plate. The part
    # is promoted to a normal movable piece by PlateAssembly, not left installed.
    eligible = [k for k,r in goals.items() if np.asarray(r['part']['rawMatrix'])[1,1] > .999]
    seed = (eligible or list(goals))[0]
    cert['fixed'] = {goals[seed]['actor']:deepcopy(goals[seed]['part'])}
    cert['environmentMode']='white-baseplate'
    cert['source'].update(selectionKind='complete-source-model', sourceSetId=md['setNumber'],
        completeSourceRetained=True, sourceInstancesDropped=0,
        moduleSourceIndices=list(range(len(mf['instances']))),
        initialInstalledSourceParts=0, retailInventoryVerified=False,
        sourceGeometryModified=False,
        contextRole='No preassembled source parts. Only the white environment baseplate is present initially.',
        scope='Every leaf part in the original LDraw model is an operable goal part. No unsupported source part is dropped.')
    if any(r['part']['canonical'] in ('3003','3003pe2') for r in goals.values()):
        cert['source']['collisionProxyRepairs']=[dict(part='3003',operation='Close one source-verified triangular stud cap; no vertex changes.',
            sourceEvidence=['parts/3003pe2.dat','parts/3003.dat','parts/s/3003s01.dat','parts/s/3003s02.dat','p/stug-2x2.dat','p/stud.dat','p/4-4disc.dat'])]
    cert['boundary']='One rigid source part per action; connector, endpoint and straight-path qualification; no force or articulation claim.'
    return cert, mf


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--only');args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    admitted=[];rejected=[]
    if args.only and (OUT/'admission-screen.json').exists():
        previous=read(OUT/'admission-screen.json')
        admitted=[r for r in previous['admitted'] if r['id']!=args.only]
        rejected=[r for r in previous['rejected'] if r['id']!=args.only]
    for spec in WHOLE:
        if args.only and spec['id']!=args.only:continue
        print('SCREEN',spec['id'],flush=True)
        if not (ROOT/'web/public/models'/spec['model']/'manifest.json').exists():
            rejected.append(dict(**spec,reason='Original source not acquired'));continue
        try:
            cert,mf=complete_certificate(spec)
            rt=runtime(cert)
            assert not rt.cert['fixed']
            assert len(rt.actors)==len(mf['instances'])
            actions=find_order(rt)
            if not actions:raise ValueError('No complete, anchored, legal build witness found with the current executor')
            assert len(actions)==len(mf['instances'])
            folder=OUT/'models'/spec['id']
            write(folder/'base-certificate.private.json.gz',cert)
            write(folder/'base-manual.private.json.gz',dict(actions=actions))
            meta=dict(**spec,kind='complete',parts=len(actions),sourceParts=len(mf['instances']),
                sourceInstancesDropped=0,sourceGeometryModified=False,
                source=cert['source'],status='REFERENCE_BUILD_VERIFIED',humanValidated=False)
            write(folder/'metadata.json',meta);admitted.append(meta)
            print('ADMITTED WHOLE',spec['id'],len(actions),flush=True)
        except Exception as exc:
            cause=exc
            while cause.__cause__ is not None:cause=cause.__cause__
            reason=str(exc)+'; '+str(cause) if cause is not exc else str(exc)
            rejected.append(dict(**spec,reason=reason[:500]));print('REJECTED',spec['id'],reason[:250],flush=True)
        write(OUT/'admission-screen.json',dict(admitted=admitted,rejected=rejected,apiModelCalls=0))
    write(OUT/'admission-screen.json',dict(admitted=admitted,rejected=rejected,apiModelCalls=0))


if __name__=='__main__':main()
