"""Small complete objects with a recognizable silhouette.

These are original stylized LEGO designs, not excerpts from commercial kits.
The same /5 assembly engine must prove a from-empty build before admission.
"""
from copy import deepcopy
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
from static_v4.build_suite import part
from static_v4.certify import digest

OUT = ROOT/'deliverables/brickplan-dynamic-v5/object-sources'

# actor, part number, x, y, z, color, quarter turns around the vertical axis
OBJECTS = {
    'obj-chair': dict(category='furniture', name='餐椅', family='complete-chair',
                      wrongColorActor='P003', wrongColor='#9b59b6', parts=[
        ('F001','3005',-30,-24,-10,'#8b5a2b',0),
        ('P001','3005', 30,-24,-10,'#8b5a2b',0),
        ('P002','3005',-30,-24, 10,'#8b5a2b',0),
        ('P003','3005', 30,-24, 10,'#8b5a2b',0),
        ('P004','3020',  0,-32,  0,'#a66b35',0),
        ('P005','3010',  0,-56, 10,'#a66b35',0),
        ('P006','3010',  0,-80, 10,'#a66b35',0),
    ]),
    'obj-table': dict(category='furniture', name='方桌', family='complete-table',
                      wrongColorActor='P007', wrongColor='#0055bf', parts=[
        ('F001','3005',-30,-24,-30,'#795333',0),
        ('P001','3005', 30,-24,-30,'#795333',0),
        ('P002','3005',-30,-24, 30,'#795333',0),
        ('P003','3005', 30,-24, 30,'#795333',0),
        ('P004','3005',-30,-48,-30,'#795333',0),
        ('P005','3005', 30,-48,-30,'#795333',0),
        ('P006','3005',-30,-48, 30,'#795333',0),
        ('P007','3005', 30,-48, 30,'#795333',0),
        ('P008','3031',  0,-56,  0,'#b48858',0),
    ]),
    'obj-city-car': dict(category='vehicle', name='小汽车', family='complete-city-car',
                         wrongColorActor='P002', wrongColor='#c91a09', parts=[
        ('F001','122c01',0,-16,-40,'#202326',0),
        ('P001','122c01',0,-16, 40,'#202326',0),
        ('P002','3034',  0,-24,  0,'#0055bf',1),
        ('P003','3039',  0,-48,-30,'#0055bf',0),
        ('P004','3001',  0,-48, 20,'#6fa8dc',1),
        ('P005','3020',  0,-56, 20,'#0055bf',1),
    ]),
    'obj-crane': dict(category='machine', name='小吊机', family='complete-crane',
                      wrongColorActor='P002', wrongColor='#f57d20', parts=[
        ('F001','3034',  0,  -8,0,'#646464',0),
        ('P001','3005',-50, -32,10,'#f2cd37',0),
        ('P002','3005',-50, -56,10,'#f2cd37',0),
        ('P003','3005',-50, -80,10,'#f2cd37',0),
        ('P004','3005',-50,-104,10,'#f2cd37',0),
        ('P005','3034', 20,-112,0,'#f2cd37',0),
        ('P006','3004',-20, -32,-10,'#0055bf',0),
        ('P007','3005', 90,-104,10,'#202326',0),
        ('P008','3024', 90, -80,10,'#202326',0),
    ]),
}


def certificate(model_id, spec):
    fixed, candidates = {}, {}
    for index,(actor,stem,x,y,z,color,turn) in enumerate(spec['parts']):
        p = part(stem,x,y,z,index=index,quarter=turn)
        p['colorHex'] = color
        p['name'] = stem+' in '+spec['name']
        if actor == 'F001':
            fixed[actor] = p
        else:
            candidates[actor+':goal'] = dict(actor=actor,kind='goal',label='模型零件',
                                             part=p,support=[],pathBlocked=[])
    actor = spec['wrongColorActor']
    replacement = deepcopy(candidates[actor+':goal']['part'])
    replacement['derivedFromSourceIndex'] = replacement['sourceIndex']
    replacement['colorHex'] = spec['wrongColor']
    wrong_actor = 'W'+actor[1:]
    candidates[wrong_actor+':wrong_color'] = dict(actor=wrong_actor,kind='wrong_color',
        label='备选颜色',part=replacement,support=[],pathBlocked=[])
    cert = dict(schema='brickplan-geometry/procedural-object-v1',modelId=model_id,
                fixed=fixed,candidates=candidates,extractionLengthLDU=320,
                scaleMetresPerLDU=.0004,
                source=dict(modelId=spec['family'],kind='stylized-complete-object',
                            objectCategory=spec['category'],objectNameZh=spec['name'],
                            generator='dynamic_v5/object_models.py'),
                boundary='Stylized complete rigid object; ideal connectors, collisions and straight paths.')
    cert['contentSha256'] = digest(cert)
    return cert


def main():
    for model_id,spec in OBJECTS.items():
        value=certificate(model_id,spec)
        folder=OUT/model_id;folder.mkdir(parents=True,exist_ok=True)
        (folder/'qualification.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
        print(model_id,len(spec['parts']),flush=True)


if __name__=='__main__':
    main()
