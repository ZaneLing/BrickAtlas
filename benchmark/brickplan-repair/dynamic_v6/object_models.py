"""Original complete objects; no recolor-only additions count as new designs."""
from copy import deepcopy
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from dynamic_v5.object_models import OBJECTS as OLD, certificate as old_certificate
from static_v4.certify import digest

BROWN='#a66b35'; DARK='#202326'; BLUE='#0055bf'; LIGHT='#6fa8dc'
RED='#c91a09'; YELLOW='#f2cd37'; WHITE='#eeeeee'; GRAY='#646464'; GREEN='#237841'
OBJECTS=deepcopy(OLD)
for key,s in OBJECTS.items():
    s['family']={'obj-chair':'seating','obj-table':'tables','obj-city-car':'road-vehicles','obj-crane':'lifting-machines'}[key]
    s['designNote']='Original v5 complete object retained; same geometry.'

class Design:
    def __init__(self,key,name,category,family):
        self.key='obj-'+key;self.s=dict(category=category,name=name,family=family,parts=[],designNote='Original stylized object assembled from registered LDraw parts.')
    def add(self,p,x,y,z,c=BROWN,r=0):
        # The local 3003 collision asset is open; use two closed 1x2 bricks.
        if p=='3003':
            self.add('3004',x,y,z-10,c).add('3004',x,y,z+10,c)
            return self
        i=len(self.s['parts']);self.s['parts'].append(('F001' if i==0 else f'P{i:03}',p,x,y,z,c,r));return self
    def column(self,p,x,z,levels,start=-24,c=BROWN,r=0):
        for i in range(levels):self.add(p,x,start-24*i,z,c,r)
        return self
    def finish(self):
        self.s.update(wrongColorActor=self.s['parts'][min(2,len(self.s['parts'])-1)][0],wrongColor='#9b59b6')
        OBJECTS[self.key]=self.s;return self

def chassis(d,color=BLUE,axle=40):
    return d.add('122c01',0,-16,-axle,DARK).add('122c01',0,-16,axle,DARK).add('3034',0,-24,0,color,1)

def models():
    d=Design('stool','小方凳','furniture','seating')
    for x in (-10,10):
        for z in (-10,10):d.add('3005',x,-24,z)
    d.add('3022',0,-32,0).add('3022',0,-40,0,RED).finish()
    d=Design('bench','长椅','furniture','seating')
    for x in (-50,50):
        for z in (-10,10):d.column('3005',x,z,2)
    d.add('3034',0,-56,0)
    for x in (-40,40):d.add('3010',x,-80,10)
    d.finish()
    d=Design('sofa','双人沙发','furniture','seating').add('3034',0,-8,0,DARK)
    for x in (-40,40):d.add('3001',x,-32,0,RED).add('3010',x,-56,10,RED)
    for x in (-70,70):d.add('3005',x,-56,-10,RED)
    d.finish()
    d=Design('desk','书桌','furniture','tables')
    for x in (-70,70):
        for z in (-30,30):d.column('3005',x,z,2)
    for z in (-20,20):d.add('3034',0,-56,z)
    d.add('3003',40,-80,0,BLUE).add('3022',40,-88,0,BLUE).finish()
    d=Design('bed','单人床','furniture','beds')
    for x in (-10,10):
        for z in (-50,50):d.add('3005',x,-24,z)
    d.add('3034',0,-32,0,WHITE,1).add('3001',0,-56,20,BLUE,1).add('3004',0,-56,-50,WHITE)
    d.column('3004',0,70,2,start=-56).finish()
    d=Design('bunk-bed','上下铺','furniture','beds').add('3034',0,-8,0,WHITE,1)
    for x in (-10,10):
        for z in (-70,70):d.column('3005',x,z,2,start=-32)
    d.add('3034',0,-64,0,BLUE,1).add('3004',0,-88,-50,WHITE).finish()
    d=Design('bookshelf','双层书架','furniture','storage').add('3034',0,-8,0)
    for x in (-70,70):d.column('3004',x,0,2,start=-32,r=1)
    d.add('3034',0,-64,0)
    for x in (-70,70):d.column('3004',x,0,2,start=-88,r=1)
    d.add('3034',0,-120,0).finish()
    d=Design('cabinet','矮柜','furniture','storage').add('3031',0,-8,0)
    for x in (-30,30):d.column('3010',x,0,2,start=-32,r=1)
    d.column('3004',0,-30,2,start=-32,c=WHITE).add('3031',0,-64,0).finish()
    d=Design('monitor','电脑显示器','household','screens').add('3031',0,-8,0,DARK).add('3003',0,-32,0,GRAY)
    d.column('3010',0,10,3,start=-56,c=DARK).add('3020',0,-112,0,GRAY).finish()
    d=Design('lamp','台灯','household','lighting').add('3022',0,-8,0,GRAY)
    d.column('3005',-10,-10,3,start=-32,c=GRAY).add('3003',0,-104,0,YELLOW).add('3022',0,-112,0,YELLOW).finish()
    d=Design('piano','立式钢琴','household','instruments').add('3034',0,-8,0,DARK)
    for x in (-40,40):
        d.add('3001',x,-32,0,DARK).column('3010',x,10,2,start=-56,c=DARK).add('3020',x,-40,-20,WHITE)
    d.add('3034',0,-88,0,DARK).finish()
    d=Design('cash-register','收银机','machine','counter-machines').add('3020',0,-8,0,GRAY).add('3001',0,-32,0,GRAY)
    d.add('3004',20,-56,10,DARK).add('3023',-20,-40,-10,WHITE).add('3023',20,-64,10,LIGHT).add('3024',-30,-48,-10,RED).finish()
    d=Design('coffee-machine','咖啡机','machine','counter-machines').add('3020',0,-8,0,DARK)
    for x in (-30,30):d.column('3005',x,10,2,start=-32,c=RED)
    d.add('3020',0,-64,0,RED).add('3004',0,-32,10,GRAY).add('3005',10,-32,-10,WHITE).add('3023',0,-72,-10,DARK).finish()
    d=Design('washing-machine','洗衣机','household','appliances').add('3031',0,-8,0,GRAY)
    for x in (-30,30):d.column('3004',x,0,2,start=-32,c=WHITE,r=1)
    d.column('3010',0,30,2,start=-32,c=WHITE).column('3004',0,-30,2,start=-32,c=BLUE).add('3031',0,-64,0,WHITE).finish()
    d=Design('refrigerator','冰箱','household','appliances').add('3031',0,-8,0,GRAY)
    for y in (-32,-56,-80,-104):
        d.add('3010',-30,y,0,WHITE,1).add('3010',30,y,0,WHITE,1).add('3004',0,y,-30,BLUE if y==-80 else WHITE)
    d.add('3031',0,-112,0,WHITE).finish()
    d=Design('fountain','喷泉','building','water-features').add('3031',0,-8,0,GRAY).add('3003',0,-32,0,GRAY)
    d.add('3031',0,-40,0,LIGHT).add('3003',0,-64,0,BLUE).add('3005',-10,-88,-10,LIGHT).add('3024',-10,-96,-10,WHITE).finish()
    d=Design('streetlight','路灯','building','lighting').add('3022',0,-8,0,GRAY)
    d.column('3005',-10,10,4,start=-32,c=GRAY).add('3010',20,-128,10,GRAY).add('3005',50,-104,10,YELLOW).finish()
    d=Design('traffic-light','红绿灯','building','signals').add('3022',0,-8,0,GRAY)
    d.column('3005',-10,10,3,start=-32,c=GRAY)
    for y,c in ((-104,GREEN),(-128,YELLOW),(-152,RED)):d.add('3004',-10,y,0,c,1)
    d.add('3023',-10,-160,0,DARK,1).finish()
    d=chassis(Design('pickup','皮卡车','vehicle','road-vehicles'),RED)
    d.add('3003',0,-48,-40,LIGHT).add('3022',0,-56,-40,RED)
    for x in (-10,10):d.add('3004',x,-48,40,RED,1)
    d.add('3004',0,-48,70,RED).finish()
    d=chassis(Design('bus','公共汽车','vehicle','road-vehicles'),YELLOW,60)
    for z in (-40,40):d.add('3001',0,-48,z,LIGHT,1)
    d.add('3034',0,-56,0,YELLOW,1)
    for z in (-70,70):d.add('3004',0,-80,z,YELLOW)
    d.finish()
    d=chassis(Design('cargo-truck','货车','vehicle','road-vehicles'),RED,60)
    d.add('3003',0,-48,-40,LIGHT).add('3022',0,-56,-40,RED).add('3001',0,-48,20,BROWN,1).add('3003',0,-72,20,BROWN).add('3022',0,-80,20,BROWN).finish()
    d=chassis(Design('ambulance','救护车','vehicle','road-vehicles'),WHITE,60)
    for z in (-40,40):d.column('3001',0,z,2,start=-48,c=WHITE,r=1)
    d.add('3034',0,-80,0,WHITE,1)
    for x,c in ((-10,RED),(10,BLUE)):d.add('3005',x,-104,-30,c)
    d.finish()
    d=chassis(Design('tractor','拖拉机','vehicle','utility-vehicles'),GREEN)
    d.add('3003',0,-48,-40,GREEN).add('3003',0,-48,40,GREEN).add('3005',-10,-72,30,DARK).add('3022',0,-80,40,YELLOW)
    d.column('3005',-10,-50,2,start=-72,c=DARK).finish()
    d=chassis(Design('forklift','叉车','vehicle','utility-vehicles'),YELLOW)
    d.add('3003',0,-48,40,YELLOW).add('3004',0,-48,70,DARK)
    for x in (-10,10):d.column('3005',x,-50,3,start=-48,c=DARK).add('3023',x,-32,-80,GRAY,1)
    d.add('3004',0,-120,-50,DARK).finish()
    d=chassis(Design('fire-engine','消防车','vehicle','road-vehicles'),RED,60)
    d.add('3003',0,-48,-40,LIGHT).add('3001',0,-48,20,RED,1)
    for x in (-10,10):d.add('3005',x,-72,50,GRAY)
    d.add('3034',0,-80,0,GRAY,1).add('3023',0,-88,-50,BLUE).finish()
    d=chassis(Design('locomotive','火车头','vehicle','rail-vehicles'),RED)
    d.add('3001',0,-48,20,DARK,1).column('3003',0,-40,2,start=-48,c=RED).add('3020',0,-80,-40,DARK,1)
    d.column('3005',-10,50,2,start=-72,c=DARK).finish()
    d=chassis(Design('rail-wagon','敞篷车厢','vehicle','rail-vehicles'),GREEN)
    for x in (-10,10):
        for z in (-40,40):d.add('3004',x,-48,z,GREEN,1)
    for z in (-70,70):d.add('3004',0,-48,z,GREEN)
    d.finish()
    d=Design('motorboat','小艇','vehicle','watercraft').add('3034',0,-8,0,WHITE)
    for x in (-40,40):d.add('3001',x,-32,0,WHITE)
    d.add('3003',-20,-56,0,LIGHT).add('3022',-20,-64,0,WHITE).column('3005',50,10,3,start=-56,c=DARK).add('3010',20,-128,10,DARK).finish()
    d=Design('airplane','飞机','vehicle','aircraft').add('3034',0,-8,0,WHITE,1)
    for z in (-40,40):d.add('3001',0,-32,z,WHITE,1)
    d.add('3034',0,-40,0,BLUE).add('3010',0,-56,70,BLUE).add('3003',0,-56,-40,LIGHT).add('3005',10,-80,70,RED).finish()
    d=Design('helicopter','直升机','vehicle','aircraft').add('3034',0,-8,0,RED,1)
    d.add('3001',0,-32,-20,LIGHT,1).add('3004',10,-32,40,RED,1).column('3005',-10,-30,2,start=-56,c=DARK).add('3034',0,-88,-20,DARK).finish()
    d=Design('press','压力机','machine','frame-machines').add('3031',0,-8,0,GRAY)
    for x in (-30,30):d.column('3005',x,10,3,start=-32,c=BLUE)
    d.add('3010',0,-104,10,BLUE).add('3005',-10,-80,10,GRAY).add('3004',0,-32,-10,GRAY).finish()
    d=Design('robot','机器人','machine','humanoid').add('3031',0,-8,0,GRAY)
    for x in (-10,10):d.add('3004',x,-32,0,BLUE,1)
    d.add('3001',0,-56,0,BLUE).add('3034',0,-64,0,BLUE)
    for x in (-50,50):d.add('3005',x,-56,10,YELLOW)
    d.add('3003',0,-88,0,YELLOW).add('3022',0,-96,0,DARK).finish()
    d=Design('clock-tower','钟楼','building','towers').add('3031',0,-8,0,GRAY)
    d.column('3003',0,0,4,start=-32).add('3031',0,-112,0,GRAY).add('3003',0,-136,0,WHITE).add('3031',0,-144,0,GRAY).finish()
    d=Design('bridge','小桥','building','spans')
    for x in (-50,50):
        for z in (-10,10):d.column('3005',x,z,3,c=GRAY)
    d.add('3034',0,-80,0,BROWN)
    for x in (-40,40):d.add('3010',x,-104,10,RED)
    d.finish()
    d=Design('house','小房子','building','buildings').add('3031',0,-8,0,GRAY)
    for x in (-30,30):d.column('3004',x,0,2,start=-32,c=WHITE,r=1)
    d.column('3010',0,30,2,start=-32,c=WHITE).add('3004',0,-32,-30,BROWN).add('3031',0,-64,0,RED)
    for x in (-20,20):d.add('3039',x,-88,10,RED)
    d.finish()
    d=Design('gateway','门楼','building','spans').add('3034',0,-8,0,GRAY)
    for x in (-60,60):d.column('3003',x,0,3,start=-32,c=GRAY)
    d.add('3034',0,-88,0,RED).add('3010',0,-112,10,RED).finish()
    d=Design('staircase','楼梯','building','stairs').add('3034',0,-8,0,GRAY,1)
    for n,z in enumerate((-50,-10,30,70),1):d.column('3004',0,z,n,start=-32,c=GRAY)
    d.finish()
    d=Design('rocket','火箭','vehicle','spacecraft').add('3031',0,-8,0,DARK)
    d.column('3003',0,0,4,start=-32,c=WHITE).add('3039',0,-128,10,RED)
    for z in (-30,30):d.add('3004',0,-32,z,RED)
    d.finish()
models()

def certificate(model_id,spec):
    cert=old_certificate(model_id,spec)
    cert['schema']='brickplan-geometry/procedural-object-v2'
    cert['source'].update(generator='dynamic_v6/object_models.py',designNote=spec['designNote'],sourceVersion='dynamic-v6')
    cert['contentSha256']=digest({k:v for k,v in cert.items() if k!='contentSha256'})
    return cert

if __name__=='__main__':
    print(len(OBJECTS),'distinct object designs')
