"""Longer recognizable original designs, using the same registered parts."""
from copy import deepcopy
from dynamic_v5.object_models import certificate as make_certificate

BROWN, GRAY, RED, WHITE, BLUE, DARK = '#a66b35', '#646464', '#c91a09', '#eeeeee', '#0055bf', '#202326'


class Design:
    def __init__(self, key, title, family, category):
        self.key = key
        self.spec = dict(name=title, family=family, category=category, parts=[], wrongColor='#9b59b6')

    def add(self, part, x, y, z, color=BROWN, turn=0):
        n = len(self.spec['parts'])
        self.spec['parts'].append(('F001' if n == 0 else f'P{n:03}', part, x, y, z, color, turn))
        return self

    def column(self, part, x, z, levels, y=-32, color=BROWN, turn=0):
        for i in range(levels):
            self.add(part, x, y-24*i, z, color, turn)
        return self

    def finish(self):
        self.spec['wrongColorActor'] = self.spec['parts'][2][0]
        return self.key, self.spec


def designs():
    rows = []
    d = Design('long-bookshelf', '四层书架', 'storage-long', 'furniture').add('3034', 0, -8, 0)
    for floor in range(4):
        y = -32-56*floor
        for x in (-70, 70):
            d.column('3004', x, 0, 2, y=y, turn=1)
        d.add('3034', 0, y-32, 0, BROWN)
    rows.append(d.finish())
    d = Design('long-city-bus', '带多排车窗的公共汽车', 'road-vehicle-long', 'vehicle')
    d.add('122c01', 0, -16, -60, DARK).add('122c01', 0, -16, 60, DARK).add('3034', 0, -24, 0, BLUE, 1)
    for level, color in enumerate((BLUE, '#6fa8dc', BLUE)):
        for x in (-10, 10):
            for z in (-70, -30, 10, 50):
                d.add('3005', x, -48-24*level, z, color)
    d.add('3034', 0, -104, 0, WHITE, 1)
    for x in (-10, 10):
        for z in (-70, 70):
            d.add('3024', x, -112, z, RED if z > 0 else '#f2cd37')
    rows.append(d.finish())
    d = Design('long-stone-bridge', '高桥墩步行桥', 'span-long', 'building')
    for x in (-50, 50):
        for z in (-10, 10):
            d.column('3005', x, z, 5, y=-24, color=GRAY)
    d.add('3034', 0, -128, 0, BROWN)
    for x in (-40, 40):
        d.add('3010', x, -152, 10, RED).add('3710', x, -160, 10, WHITE)
    rows.append(d.finish())
    d = Design('long-gantry-press', '四柱冲压机', 'industrial-frame-long', 'machine').add('3031', 0, -8, 0, GRAY)
    for x in (-30, 30):
        for z in (-30, 30):
            d.column('3005', x, z, 4, color=BLUE)
    for z in (-30, 30):
        d.add('3010', 0, -128, z, BLUE)
    d.add('3031', 0, -136, 0, GRAY).add('3004', 0, -32, -10, GRAY)
    d.column('3005', -10, 10, 3, y=-32, color=GRAY)
    rows.append(d.finish())
    d = Design('long-cottage', '小屋：墙体与屋面', 'building-long', 'building').add('3031', 0, -8, 0, GRAY)
    for level in range(4):
        y = -32-24*level
        for x in (-30, 30):
            d.add('3004', x, y, 0, WHITE, 1).add('3005', x, y, -30, WHITE)
        d.add('3010', 0, y, 30, WHITE)
    d.add('3031', 0, -112, 0, RED)
    for x in (-20, 20):
        d.add('3039', x, -136, 10, RED)
    rows.append(d.finish())
    return dict(rows)


def certificate(key, spec):
    cert = make_certificate('v7-'+key, spec)
    cert.update(id='v7-'+key, protocol='brickplan-expansion/7', checkpoint=3,
                environmentMode='white-baseplate', conservativeContext={}, tableY=.1)
    cert['source'].update(moduleSourceIndices=list(range(len(spec['parts']))),
        sourceSetId='original:v7:'+key, totalInstances=len(spec['parts']),
        generator='expansion_v7/designs.py', originalDesign=True,
        longProcess=True, sourceGeometryModified=False)
    for part in [*cert['fixed'].values(), *[r['part'] for r in cert['candidates'].values()]]:
        part.setdefault('sourceInstanceId',f'original:{key}:{part.get("sourceIndex")}')
    # PlateAssembly makes the former fixture movable as an ordinary goal part.
    for actor, part in cert['fixed'].items():
        cert['candidates'][actor+':goal'] = dict(actor=actor, kind='goal', part=deepcopy(part))
    return cert
