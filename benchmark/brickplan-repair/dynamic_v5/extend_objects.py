"""Add complete recognizable objects after procedural and source extensions."""
from collections import Counter
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from dynamic_v5 import VERSION
from dynamic_v5.build import OUT, build_one, write
from dynamic_v5.extend_sources import verify
from dynamic_v5.object_models import OBJECTS, OUT as OBJECT_SOURCE, certificate
from baseplate import PlateAssembly


def main():
    selected = tuple(sorted(OBJECTS))
    current = json.loads((OUT/'cases.private.json').read_text())
    originals = [case for case in current['cases'] if case['modelId'] not in selected]
    extension = []
    decisions = []
    for model_id in selected:
        source_path = OBJECT_SOURCE/model_id/'qualification.json'
        assert source_path.exists(), f'Run object_models.py first: {source_path}'
        source = json.loads(source_path.read_text())
        assert source['contentSha256'] == certificate(model_id,OBJECTS[model_id])['contentSha256']
        original_rt = PlateAssembly(source)
        graph,_ = original_rt.connections(original_rt.goal)
        graph.pop('@baseplate',None)
        for neighbors in graph.values():
            neighbors.discard('@baseplate')
        seen=set();todo=[next(iter(graph))]
        while todo:
            actor=todo.pop()
            if actor in seen:
                continue
            seen.add(actor);todo.extend(graph[actor]-seen)
        assert len(seen)==sum(bool(k) for k in original_rt.goal.values()), (model_id,'disconnected object')
        cases, evidence = build_one(source_path)
        assert cases and any(c['kind']=='none' for c in cases) and any(c['kind']!='none' for c in cases), model_id
        cert = json.loads((OUT/'models'/model_id/'qualification.json').read_text())
        for case in cases:
            case['objectCategory'] = source['source']['objectCategory']
            case['objectNameZh'] = source['source']['objectNameZh']
            verify(cert,case,evidence['buildWitness'])
        evidence['objectCategory'] = source['source']['objectCategory']
        evidence['objectNameZh'] = source['source']['objectNameZh']
        write(OUT/'models'/model_id/'evidence.json',evidence)
        decisions.append(dict(modelId=model_id,objectCategory=evidence['objectCategory'],
                              objectNameZh=evidence['objectNameZh'],admittedCases=len(cases),
                              kinds=dict(Counter(c['kind'] for c in cases))))
        extension += cases
        print(model_id,len(cases),decisions[-1]['kinds'],flush=True)
    combined = originals+extension
    assert len({c['id'] for c in combined})==len(combined)
    prior = json.loads((OUT/'index.json').read_text())
    audits = [a for a in prior['modelAudits'] if a['modelId'] not in selected]
    audits += [json.loads((OUT/'models'/m/'evidence.json').read_text()) for m in selected]
    write(OUT/'cases.private.json',dict(schema=VERSION,cases=combined))
    write(OUT/'index.json',dict(schema=VERSION,
          cases=[{k:v for k,v in c.items() if k!='privateEvent'} for c in combined],
          modelAudits=audits,counts=dict(Counter(c['kind'] for c in combined))))
    write(OUT/'object-extension.json',dict(schema='brickplan-dynamic-objects/1',
          models=len(selected),cases=len(extension),kinds=dict(Counter(c['kind'] for c in extension)),
          decisions=decisions,scope='Original stylized complete objects, not commercial kits.'))
    write(OUT/'object-track.json',dict(schema='brickplan-dynamic-object-track/1',
          status='prototype; human recognizability review pending',
          modelIds=list(selected),cases=[{k:v for k,v in c.items() if k!='privateEvent'} for c in extension],
          counts=dict(Counter(c['kind'] for c in extension))))
    print('object extension',len(extension),'combined',len(combined),flush=True)


if __name__=='__main__':
    main()
