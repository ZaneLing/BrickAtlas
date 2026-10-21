"""Clean RGB observation audit and two reviewable input packs.

Uniform layer inspection is explicitly a digital assistance track. It is not
claimed to be external-camera-only perception or a real robot sensor stream.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent));sys.path.insert(0,str(HERE.parent/'eval'))
from baseplate import PlateAssembly
from vision import VisionRenderer
from static_v4.build_suite import OUT,dump


def run(only=None):
    rows=[];samples=['sr4-triple-2:mixed','sr4-alternative-release:color']
    if only and (OUT/'visual-audit.json').exists():
        rows=[r for r in json.loads((OUT/'visual-audit.json').read_text())['rows'] if not r['caseId'].startswith(only+':')]
    for model in json.loads((OUT/'library/index.json').read_text())['models']:
        if only and model['modelId']!=only:continue
        folder=OUT/'library/models'/model['modelId'];rt=PlateAssembly(json.loads((folder/'qualification.json').read_text()))
        renderer=VisionRenderer(rt.cert)
        # Layer bins are defined uniformly from the whole pose envelope; the
        # same fixed bins apply to every case and both current/target scenes.
        levels=sorted({round(float(r['part']['matrix'][1][3])/8) for r in rt.candidates.values()})
        for case in json.loads((folder/'cases.json').read_text()).values():
            masks=[];differences=[];images=[];counter=0
            pack=OUT/'visual-input'/hashlib.sha256(case['id'].encode()).hexdigest()[:12]
            def pair(label,current,target,view='isometric'):
                nonlocal counter
                a,ma=renderer.rgb(current,view=view);b,mb=renderer.rgb(target,view=view)
                delta=np.max(np.abs(np.asarray(a,dtype=np.int16)-np.asarray(b,dtype=np.int16)),axis=2)
                differences.append(dict(channel=label,changedPixels=int((delta>16).sum())))
                masks.append((ma,mb))
                if case['id'] in samples:
                    pack.mkdir(parents=True,exist_ok=True)
                    for scene,image in [('current',a),('target',b)]:
                        filename=f'{counter:03}.png';counter+=1;image.save(pack/filename)
                        images.append(dict(scene=scene,view=label,file=filename,width=1600,height=1200))
            for view in ['isometric','front','rear','left','right','top','bottom']:
                pair(view,case['initial'],rt.goal,view)
            for n,level in enumerate(levels):
                def section(state):return {a:k for a,k in state.items() if k and round(float(rt.row(k)['part']['matrix'][1][3])/8)==level}
                pair(f'layer-{n+1}',section(case['initial']),section(rt.goal))
            physical_change=not rt.complete(case['initial'])
            visible=max(d['changedPixels'] for d in differences)
            assert not physical_change or visible>=100,(case['id'],visible)
            # All pieces in current/target get at least a measurable footprint
            # in the uniform inspection channels. No root-conditioned crop.
            current_ids=set(np.unique(np.concatenate([m[0].ravel() for m in masks])))
            target_ids=set(np.unique(np.concatenate([m[1].ravel() for m in masks])))
            hidden_current=[a for a,k in case['initial'].items() if k and renderer.ids[a] not in current_ids]
            hidden_target=[a for a,k in rt.goal.items() if k and renderer.ids[a] not in target_ids]
            assert not hidden_current and not hidden_target
            rows.append(dict(caseId=case['id'],physicalChange=physical_change,maxChangedPixels=visible,
                             hiddenCurrent=hidden_current,hiddenTarget=hidden_target,differences=differences,
                             sampleDirectory=str(pack.relative_to(OUT)) if case['id'] in samples else None))
            if case['id'] in samples:
                dump(pack/'input.json',dict(protocol='visual-static-assisted/4-preview',
                    task='Repair the current assembly to match the target. Infer differences from RGB images.',
                    images=images,inspection='Uniform layer views are available for all layers in both scenes.',
                    status='Observation-only preview; action adapter/model trials not certified by this artifact'))
        print(model['modelId'],'visual check',flush=True)
    dump(OUT/'visual-audit.json',dict(schema='uniform-rgb-observability/1',resolution=[1600,1200],supersample=2,
        sceneLabels=False,selection='same seven views and all uniform 8-LDU layer bins, not fault-targeted',
        environment='diagram inspection: environmental plate omitted, including bottom/section views',
        limitation='Pixel footprint and visible differences are necessary checks, not semantic recognition or human validation.',rows=rows))

if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else None)
