"""A source-backed Markdown example for every populated bank/mode/type/level cell.

Uses existing input adapters and executors. No model client is invoked. Reference
actions are one feasible witness, never a required order or empirical AI result.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
import argparse
import hashlib
import io
import json
import os
import sys

HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE/'eval'),str(HERE.parent/'brickplan-v1')]
from expansion_v7 import ROOT
from expansion_v7.build import read
from expansion_v7.runtime import Episode as NewEpisode, public_action
from expansion_v7.run_episode import Packet as NewPacket
from community_modules.core import Episode as ModuleEpisode
from community_modules.run_episode import ModulePacket
from dynamic_v6.episode import DynamicEpisode
from dynamic_v6.interface import packet as old_packet, renderer_for, SYSTEM as D_SYSTEM
from dynamic_v6.object_models import OBJECTS
from budget_pilot.run import StaticEpisode, S_SYSTEM
from plate5_eval import evaluate as static_evaluate
from matched_canvas import comparison
from PIL import Image,ImageDraw
from render import FONT

OUT=ROOT/'deliverables/brickplan-question-showcase'
EXT=ROOT/'deliverables/brickplan-expansion-v7'
VIEWS=('isometric','rear','top')
BANKS={'S':'原静态题库 S','D':'原动态题库 D','M':'原社区模块 M','E7':'本轮扩展 E7'}
LEVELS={'L1':'基础组合（暂定）','L2':'增加一项结构负担（暂定）','L3':'叠加多项结构负担（暂定）'}
NAMES={'control':'正常对照','none':'正常对照','missing':'少件','removed_piece':'少件',
 'wrong_color':'错色','wrong-color':'错色','extra':'多余零件','extra_layer':'局部多装一层',
 'extra-layer':'局部多装一层／重复加件','offset':'偏移一格','shifted_piece':'偏移一格',
 'rotation':'方向装反','rotated':'方向装反','rotated_piece':'方向装反',
 'wrong_type':'零件类型错误','wrong-part':'错零件／厚度','wrong_part':'零件类型错误',
 'wrong_size':'零件尺寸错误','height_layer':'高度／层数错误','swapped_positions':'两件位置互换',
 'left-right-swap':'左右位置互换','compound':'同时存在多种错误','compound_fault':'同时存在多种错误',
 'repair_state':'从已验证修复路线中截取的替换题','early_cover':'提前封口挡住安装通路',
 'early-cover':'提前封口挡住安装通路','buried_wrong_color':'内部错色，需拆上层返修',
 'buried-repair':'内部错误，需拆上层返修','repeat-omission':'重复组件漏做一份',
 'cascade_removal':'连带掉件','cascade-removal':'连带掉件'}
DESCRIPTIONS={'control':'结构已经符合本题阶段目标，直接结束即可；库存有备用件不代表必须继续安装。',
 'none':'没有后台干扰；按任意合法顺序拼到最终目标。',
 'missing':'应有的零件缺失，需要补回。','removed_piece':'中途移走了原本装上的零件，需要恢复并继续。',
 'wrong_color':'实际零件颜色与目标不符，需换成正确颜色。','wrong-color':'实际零件颜色与目标不符，需换成正确颜色。',
 'extra':'当前结构有目标之外的零件，应移除多余件。',
 'extra_layer':'中途多装了局部零件／一层，应拆掉多装部分并继续。',
 'extra-layer':'多装了局部零件，用来模拟重复加件／铺层；不是整套模型每层都重复。',
 'offset':'零件位置偏移一颗凸点，需要拆下并改到正确候选位置。',
 'shifted_piece':'中途改变了某件的位置，需要改回并继续。',
 'rotation':'零件朝向与目标不同，需要拆下重新定向。',
 'rotated':'零件朝向与目标不同；对称等价朝向不会被当成错误。',
 'rotated_piece':'中途改变了非等价朝向，需要重新安装。',
 'wrong_type':'用了错误类型的零件，需要取下并换件。',
 'wrong_part':'中途换成了错误类型的零件，需要换回并继续。',
 'wrong-part':'用了错误类型／厚度的实物，需要换件；不会让同一块零件凭空变形。',
 'wrong_size':'使用了尺寸不对的零件，需要换成目标规定的尺寸。',
 'height_layer':'高度或层数与目标不同，以右侧目标和真实几何为准。',
 'swapped_positions':'两件在错误的位置，需要合法地拆换；同形同色零件可互换。',
 'left-right-swap':'不同颜色的同形零件互换了位置；这里只模拟合法刚体的位置互换。',
 'compound':'同一初始状态同时存在多项错误。',
 'compound_fault':'一次后台事件同时造成多项错误，不等于前后两次事故。',
 'repair_state':'这题来自白底板迁移时的替换记录，是可验证修复中途状态，不是新的基本错误类别。',
 'early_cover':'盖件本身能合法安装，但提前挡住了后续零件的进入通路。',
 'early-cover':'盖件本身能合法安装，但提前挡住了后续零件的进入通路。',
 'buried_wrong_color':'下层有错色，需要临时拆开本来正确的盖件，换好再恢复。',
 'buried-repair':'内部有错误，需要临时拆开本来正确的盖件，换好再恢复。',
 'repeat-omission':'两个相同类型／颜色的位置缺件，近似模拟漏看重复次数；不声称还原了注意过程。',
 'cascade_removal':'多件连带移除，需逐块补回；不模拟真实跌落时的受力过程。',
 'cascade-removal':'多件连带移除，需逐块补回；不模拟真实跌落时的受力过程。'}
PARTS={'3001':'2×4砖','3002':'2×3砖','3003':'2×2砖','3004':'1×2砖','3005':'1×1砖',
 '3010':'1×4砖','3008':'1×8砖','3009':'1×6砖','3020':'2×4薄板','3021':'2×3薄板',
 '3022':'2×2薄板','3023':'1×2薄板','3024':'1×1薄板','3031':'4×4薄板','3034':'2×8薄板',
 '3710':'1×4薄板','3039':'斜坡砖','122c01':'轮轴组件'}


def dump(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def label(f):
    return NAMES.get(f,'连续：'+' → '.join(NAMES.get(x,x) for x in f.removeprefix('multiple-').split('then-')))


def family_note(f):
    return DESCRIPTIONS.get(f,'前后分时发生多次干扰；修好一次后还要继续观察后续状态。')


def dataset():
    master=read(EXT/'global-splits.json');features={r['caseId']:r for r in read(EXT/'difficulty-all.json')['cases']}
    active={r['id'] for r in master['cases']};rows=[]
    old_modules={m['id']:m for m in read(ROOT/'deliverables/brickplan-community-modules/gallery-data.js.json')}
    new_models={m['id']:m for m in read(EXT/'index.json')['models']}
    source_titles={}
    def source_title(model):
        base=model.split('--')[0]
        if base not in source_titles:
            path=ROOT/'web/public/models'/base/'manifest.json'
            title=read(path).get('model',{}).get('title',base) if path.exists() else base
            translations={'Jet':'喷气飞机','Metroliner':'都市列车','Caboose':'铁路守车','Pizza To Go':'披萨外卖店',
                'Train Level Crossing':'铁路道口','LEGO Truck':'卡车','Shuttle Adventure':'航天飞机','Tower Bridge':'伦敦塔桥',
                'Small Cottage':'小屋','Kart':'卡丁车','Pelican':'鹈鹕','Town Bank':'城市银行'}
            source_titles[base]=translations.get(title,title)
        return source_titles[base]+'的局部结构（'+model+'）'
    audits={r['caseId']:r for r in read(ROOT/'deliverables/brickplan-dynamic-v6/audit.json')['rows']}
    def add(bank,c,mode,family,model,title):
        key=bank+':'+c['id']
        if key not in active:return
        p=features[key]
        visibility=(p.get('machineVisible') if bank=='E7' else
                    audits.get(c['id'],{}).get('temporalClass') if bank=='D' else None)
        rows.append(dict(key=key,bank=bank,case=c,mode=mode,family=family,model=model,title=title,
            level=p['structuralGroup'],profile=p,visibility=visibility))
    for line in (ROOT/'deliverables/brickplan-static-plate5/cases.jsonl').read_text().splitlines():
        c=json.loads(line);add('S',c,'static',c['kind'],c['modelId'],source_title(c['modelId']))
    for c in read(ROOT/'deliverables/brickplan-dynamic-v6/cases.private.json')['cases']:
        add('D',c,'dynamic',c['kind'],c['modelId'],OBJECTS.get(c['modelId'],{}).get('name','机制结构 '+c['modelId']))
    for line in (ROOT/'deliverables/brickplan-community-modules/cases.private.jsonl').read_text().splitlines():
        c=json.loads(line);add('M',c,c['mode'],c['family'],c['module'],old_modules[c['module']]['title'])
    for m in new_models.values():
        for c in read(EXT/'models'/m['id']/'cases.private.json.gz'):
            add('E7',c,c['mode'],c['family'],m['id'],m['title'])
    assert len(rows)==5975
    return rows,old_modules,new_models


def cell(row):return row['bank'],row['mode'],row['family'],row['level']


def select(rows):
    groups=defaultdict(list)
    for r in rows:groups[cell(r)].append(r)
    selected={};usage=Counter();models=sorted({r['model'] for r in rows if r['bank']=='E7'})
    possibilities={m:sorted([k for k,v in groups.items() if k[0]=='E7' and any(r['model']==m for r in v)],
                          key=lambda k:(len({r['model'] for r in groups[k]}),k)) for m in models}
    assigned={}
    def match(model,seen):
        for key in possibilities[model]:
            if key in seen:continue
            seen.add(key)
            if key not in assigned or match(assigned[key],seen):assigned[key]=model;return True
        return False
    for model in sorted(models,key=lambda m:(len(possibilities[m]),m)):assert match(model,set())
    def preference(r):
        visible=0 if r['visibility'] is True or r['visibility']=='machine-visible' else 1 if r['visibility'] is None or r['visibility']=='control' else 2
        return (visible,usage[r['bank'],r['model']],not r['model'].startswith('obj-') if r['bank']=='D' else False,
                abs(r['profile']['targetParts']-10),r['key'])
    order={'S':0,'D':1,'M':2,'E7':3}
    for key in sorted(groups,key=lambda k:(order[k[0]],k[1],k[2],k[3])):
        candidates=groups[key]
        if key in assigned:candidates=[r for r in candidates if r['model']==assigned[key]]
        chosen=min(candidates,key=preference);selected[key]=chosen;usage[chosen['bank'],chosen['model']]+=1
    examples=[dict(r,purpose='coverage',cellCount=len(groups[k])) for k,r in selected.items()]
    used={r['key'] for r in examples}
    for bank,visibility,purpose in [('D','action-cancellation','自己的动作被抵消'),('D','low-contrast','动态低对比诊断'),('E7',False,'扩展低可见诊断')]:
        pool=[r for r in rows if r['bank']==bank and r['visibility']==visibility and r['key'] not in used]
        if bank=='E7':pool.sort(key=lambda r:(r['family']!='buried-repair',r['mode']!='dynamic',r['key']))
        else:pool.sort(key=preference)
        chosen=pool[0];used.add(chosen['key']);examples.append(dict(chosen,purpose=purpose,cellCount=len(groups[cell(chosen)])))
    for i,r in enumerate(examples,1):r['example']='Q'+str(i).zfill(3)
    assert len(groups)==96 and len(examples)==99
    assert {r['model'] for r in examples if r['bank']=='E7'}==set(models)
    return examples,groups


def asset(image,role,**meta):
    stream=io.BytesIO();image.save(stream,format='PNG');data=stream.getvalue();sha=hashlib.sha256(data).hexdigest()
    path=OUT/'assets'/(sha+'.png');path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists():path.write_bytes(data)
    return dict(file=path.relative_to(OUT).as_posix(),role=role,sha256=sha,width=image.width,height=image.height,**meta)


def normalize(record,directory=None):
    source=Path(record['file'])
    if not source.is_absolute():source=directory/source
    target=OUT/'assets'/source.name;target.parent.mkdir(parents=True,exist_ok=True)
    if source!=target:
        if not target.exists():source.replace(target)
        elif source.exists():source.unlink()
    return {**record,'file':target.relative_to(OUT).as_posix()}


def context(row,old_modules):
    bank,mid=row['bank'],row['model']
    if bank in ('S','D'):
        if bank=='S':ep=StaticEpisode(row['case']['publicId'])
        else:ep=DynamicEpisode(read(ROOT/'deliverables/brickplan-dynamic-v6/models'/mid/'qualification.json'),row['case'],41)
        renderer=renderer_for(ep);inventory=renderer.inventory(ep)
        renderer.inventory=lambda unused:inventory
        return dict(renderer=renderer,q=ep.runtime.q)
    folder=(EXT/'models'/mid if bank=='E7' else ROOT/'deliverables/brickplan-community-modules'/mid)
    cert=read(folder/('certificate.private.json.gz' if bank=='E7' else 'certificate.private.json'))
    ep=(NewEpisode if bank=='E7' else ModuleEpisode)(cert,row['case'],41)
    manual=read(folder/('manual.private.json.gz' if bank=='E7' else 'manual.private.json'))
    packet=(NewPacket(ep,manual,OUT/'assets') if bank=='E7' else ModulePacket(ep,old_modules[mid],OUT/'assets'))
    return dict(cert=cert,packet=packet,renderer=packet.renderer,q=ep.runtime.q,manual=manual)


def scene(renderer,state,view='isometric',size=(400,300)):
    kwargs={'frame_keys':['_module_frame']} if '_module_frame' in renderer.bounds else {}
    return renderer.rgb(state,view,size=size,supersample=1,**kwargs)[0]


def part_description(rt,key):
    if not key:return '未装在结构上'
    p=rt.row(key)['part'];h=p['colorHex'].lower()
    known={'#c91a09':'红色','#0055bf':'蓝色','#a66b35':'棕色','#eeeeee':'白色','#ffffff':'白色',
           '#202326':'黑色','#05131d':'黑色','#646464':'灰色','#6fa8dc':'浅蓝','#237841':'绿色',
           '#00852b':'绿色','#19325a':'深蓝','#f2cd37':'黄色','#9b59b6':'紫色','#a0a5a9':'浅灰',
           '#6c6e68':'深灰','#9ba19d':'灰色'}
    return known.get(h,'颜色'+h)+' '+PARTS.get(p.get('canonical'),p['partNumber']+'零件')


def capture(ctx,ep,row,stage):
    if row['bank'] in ('S','D'):
        directory=OUT/'scratch'/row['example']/stage
        obs,records=old_packet(ep,ctx['renderer'],directory)
        records=[normalize(r,directory) for r in records]
    else:
        ctx['packet'].ep=ep;obs=ctx['packet'].observation()
        records=[normalize(r) for r in obs.pop('images')]
    forbidden={'initial','goal','oraclePlan','privateEvent','referenceActions','humanErrorIds','family','events'}
    assert not forbidden.intersection(obs)
    path=OUT/'inputs'/row['example']/(stage+'.json')
    dump(path,dict(observation=obs,images=records,assetPathBase='deliverables/brickplan-question-showcase',
        **({'system':S_SYSTEM if row['bank']=='S' else D_SYSTEM} if row['bank'] in ('S','D') else {})))
    return dict(input=path.relative_to(OUT).as_posix(),images=records)


def build_example(row,ctx):
    bank,c=row['bank'],row['case'];module=bank in ('M','E7')
    if bank=='S':ep=StaticEpisode(c['publicId']);actions=[dict(a) for a in c['oraclePlan']]
    elif bank=='D':
        cert=read(ROOT/'deliverables/brickplan-dynamic-v6/models'/row['model']/'qualification.json')
        ep=DynamicEpisode(cert,c,41);normal=read(ROOT/'deliverables/brickplan-dynamic-v6/models'/row['model']/'evidence.json')['buildWitness']
        actions=normal if not c.get('privateEvent') else normal[:c['trigger']]+c['privateEvent']['recoveryWitness']
    else:
        ep=(NewEpisode if bank=='E7' else ModuleEpisode)(ctx['cert'],c,41)
        actions=[dict(a) for a in c['referenceActions']]
    ep.runtime.q=ctx['q'];rt=ep.runtime;initial=dict(ep.state);initial_packet=capture(ctx,ep,row,'initial')
    aliases=ep.actor_alias if module else ep.alias
    def pub(action):
        if module:return public_action(ep,action)
        result=dict(type=action['type'],partId=ep.alias[action['partId']])
        if action['type']=='attach':result['candidate']=ep.pose(action['candidate'])
        return result
    def wire(public,changed=False):
        return public if module else dict(action=public,**({'unexpectedChange':changed} if bank=='D' else {}))
    gt=[];states=[dict(ep.state)];events=[];changed=False
    for number,action in enumerate(actions,1):
        public=pub(action);payload=wire(public,changed);before=dict(ep.state)
        actor=action.get('actor',action.get('partId'));key=action.get('candidate') or before.get(actor)
        description=part_description(rt,key)
        prior=len(ep.events) if bank=='E7' else int(bool(ep.event_applied)) if bank=='M' else int(bool(ep.event))
        if module:ep.step(public);feedback=ep.feedback
        else:feedback=ep.submit(payload)
        assert feedback['code']=='OK',(row['key'],number,feedback)
        now=len(ep.events) if bank=='E7' else int(bool(ep.event_applied)) if bank=='M' else int(bool(ep.event))
        changed=now>prior;states.append(dict(ep.state))
        gt.append(dict(step=number,output=payload,publicAction=public,description=description,
                       feedback=feedback['code'],eventAfterThisAction=changed,after=dict(ep.state)))
        if changed:
            event=ep.events[-1] if bank=='E7' else ep.last_event if bank=='M' else ep.event
            if bank=='D':
                event_before=dict(ep.expected_after_last_action);event_after=dict(ep.state)
                family=c['kind'];changes=event['transaction'];recovery=event['recoveryWitness']
            else:
                event_before=event['before'];event_after=event['after'];family=event['family']
                changes=event['changes'];recovery=event['recovery']
            kwargs={'frame_keys':['_module_frame']} if module else {}
            truth=asset(comparison(ctx['renderer'],event_before,event_after,'isometric',
                'GT ONLY: AFTER YOUR ACTION, BEFORE EVENT','GT ONLY: AFTER HIDDEN EVENT',**kwargs),'private-event-explanation')
            packet=capture(ctx,ep,row,'event-'+str(now))
            changes_public=[]
            for a in changes:
                internal=a.get('actor',a.get('partId'));k=a.get('candidate') or event_before.get(internal)
                changes_public.append(dict(type=a['type'],partId=aliases[internal],description=part_description(rt,k)))
            events.append(dict(number=now,afterStep=number,family=family,truthImage=truth,
                               packet=packet,changes=changes_public,recoveryWitnessMoves=len(recovery)))
    finish=wire({'type':'finish'},changed)
    if module:ep.step({'type':'finish'});score=ep.score()
    else:ep.submit(finish);score=ep.score()
    assert score['success'] and rt.complete(ep.state),(row['key'],score)
    if bank=='S':assert static_evaluate(c['publicId'],actions+[{'type':'finish'}])['success']
    expected=len(c.get('events',[])) if bank=='E7' else int(bool(c.get('event'))) if bank=='M' else int(bool(c.get('privateEvent'))) if bank=='D' else 0
    assert len(events)==expected,(row['key'],'event count')
    # Every action is tabulated. A compact strip samples at most eight states.
    chosen={0,len(actions)}|{e['afterStep'] for e in events}
    for k in [round(i*len(actions)/7) for i in range(1,7)]:
        if len(chosen)<8:chosen.add(k)
    chosen=sorted(chosen);tiles=Image.new('RGB',(400*len(chosen),330),'white');draw=ImageDraw.Draw(tiles)
    for col,k in enumerate(chosen):
        tiles.paste(scene(ctx['renderer'],states[k]),(col*400,30))
        caption='0 START' if k==0 else f'{k} '+('AFTER EVENT' if k in {e['afterStep'] for e in events} else 'AFTER ACTION')
        draw.text((col*400+12,7),caption,font=FONT,fill='#17283a')
    strip=asset(tiles,'gt-keyframes',actionIndices=chosen)
    first_attach=next((g for g in gt if g['publicAction']['type']=='attach'),None)
    preview=None
    if first_attach:
        public=first_attach['publicAction'];pose=public['candidate']
        internal_key=(ep.poses[pose] if module else ep.pose_reverse[pose]);actor=rt.row(internal_key)['actor']
        if module:
            page=scene(ctx['renderer'],{**initial,actor:internal_key},size=(1600,1200))
            pages=[asset(page,'candidate-preview',candidate=pose)]
            request=dict(type='inspect',candidate=pose,view='isometric')
        else:
            current=ep.state;ep.state=initial
            try:pages=[asset(im,'candidate-catalog',page=i+1) for i,im in enumerate(ctx['renderer'].catalog(ep,public['partId']))]
            finally:ep.state=current
            request=dict(action=dict(type='inspect',partId=public['partId']),**({'unexpectedChange':False} if bank=='D' else {}))
        preview=dict(request=request,images=pages,correctCandidateInGT=pose)
    final_pair=asset(comparison(ctx['renderer'],ep.state,c.get('goal',rt.goal),'isometric',
        'GT REPLAY FINAL STATE','REQUIRED TARGET',**({'frame_keys':['_module_frame']} if module else {})),'gt-final-versus-target')
    manual=None
    if module:
        instruction=1 if c['mode']=='dynamic' else min(1,c['completedInstructionStep'])
        manual=normalize(ctx['packet'].manual_page(max(1,instruction)))
    truth_path=OUT/'gt'/(row['example']+'.json')
    dump(truth_path,dict(caseKey=row['key'],seed=41,initial=initial,goal=c.get('goal',rt.goal),
        referenceActions=gt,finishOutput=finish,events=events,final=dict(ep.state),
        referenceWitnessPassed=True,requiredReferenceOrder=False,referenceIsShortest=None,optimalityCertified=False,
        apiModelCalls=0,humanOrModelPerformance=False))
    result={k:v for k,v in row.items() if k!='case'}
    result.update(originalId=c['id'],publicId=c.get('publicId'),initial=initial_packet,events=events,
        gt=gt,finish=finish,gtFile=truth_path.relative_to(OUT).as_posix(),gtStrip=strip,finalImage=final_pair,
        candidateExample=preview,manual=manual,inventoryParts=len(aliases),referenceActions=len(actions),
        targetParts=sum(bool(k) for k in c.get('goal',rt.goal).values()),
        moduleParts=len(ctx['cert']['source']['moduleSourceIndices']) if module else None,
        contextLocked=module and ctx['cert'].get('environmentMode')!='white-baseplate',referenceWitnessPassed=True)
    dump(OUT/'examples'/(row['example']+'.json'),result)
    return result


def image(record,alt):return f'![{alt}]({record["file"]})'


def image_table(records,roles=None):
    if roles:records=[r for r in records if r['role'] in roles]
    if not records:return []
    names={'isometric':'斜视','rear':'背面','top':'俯视'}
    headers=[names.get(r.get('view'),f'第{r.get("page",i+1)}页') for i,r in enumerate(records)]
    return ['| '+' | '.join(headers)+' |','|'+'---|'*len(records),
            '| '+' | '.join(image(r,h) for r,h in zip(records,headers))+' |','']


def write_markdown(examples,groups,rows):
    lines=['# 全类别、全难度组题目图解：输入、输出与GT','',
        '更新：2026-10-23。**GT就是参考正确答案。** 这份文件供你审题，含错误名称、后台事件和参考修法，不能整份发给被测模型。','',
        '本文件覆盖现有 **5,975道物理任务**中全部 **96种实际存在的“题库 × 静态或动态 × 错误类别 × 结构难度组”组合**，每种选一道；另加3道特殊诊断题，共 **99个完整图解例子**。本轮扩展的21个物件配置全部至少出现一次。不是把5,975道题逐题展开，也没有为不存在的难度组合编题。','',
        '下面所有操作与图片都来自实际题目和现有执行器。程序已重放这些参考操作；没有调用模型API，没有把程序答案当作模型成绩。','',
        '## 先看懂一题','',
        '1. **看左边当前状态，右边是本题唯一目标。** 静态题可能只要求恢复某个中途阶段，不一定要求完整成品。',
        '2. **每次只装一块或拆一块。** 也可以查看图片、零件或候选位置；查看不改变积木。',
        '3. **安装时选零件和候选位置。** A开头是零件编号，C开头是候选摆放编号；编号随机，不代表正确答案。',
        '4. **拼法不唯一。** 下文GT只展示一条走得通的路线。其他合法路线，只要最后结构、零件和颜色等价，也能通过。',
        '5. **达到目标后还要提交结束。** 正常静态题左右相同时，可以直接结束；正常动态题则仍要从起点拼完。','',
        '## 各部分给什么、回什么','',
        '| 部分 | 开始时看到什么 | 中间看到什么 | 每次输出 | 最后要求 |',
        '|---|---|---|---|---|',
        '| 原静态 S | 当前／唯一目标三视图、全部零件库存、匿名操作编号 | 新的当前图；上次操作前与现在的对照；可查看全部候选页 | 一个装、拆、查看或结束动作，外层有`action` | 修到本题目标；环境不再暗中改动 |',
        '| 原动态 D | 空白底板／最终目标三视图、全部库存；没有说明书 | 每步实际状态、上次操作前与现在的对照 | `action`加`unexpectedChange`布尔值；不要求解释文字 | 遇到变化后仍继续拼到最终目标 |',
        '| 社区模块 M | 主体已装好，只操作指定模块；阶段目标或最终模块目标、全部库存 | 每步状态和时间对照；说明书按需查看 | 直接提交一个动作对象，没有`action`外壳 | 固定主体不拆；达到本题右侧目标 |',
        '| 扩展 E7 | 长流程从空底板开始，或社区模块从预装主体开始；目标、库存 | 每步状态、时间对照；可按需看逐块说明 | 同M，直接一个动作对象；没有强制检测问答 | 合法拼完目标；动态题可能有多次干扰 |','',
        '**这些接口目前确实有差别。** 本文的JSON示例按各自当前接口生成，没有把计划中的统一接口写成已实现。真人在操作页面点击即可；JSON只用来说明模型接口。','',
        '这里的输入JSON是程序参考路线导出的原生观察与图片清单，不是某个API模型的真实调用日志。S／D文件另附当前system提示词；M／E7目前直接导出JSONL观察。后续API运行还要由调用器保留之前的动作／反馈对话，不能把一张中途截图当成有完整历史的动态测试。','',
        '**图片是什么：**每张当前／目标图为1600×636，左右场景都是800×600；多视角是同一套积木，不能把三个视角的零件数相加。首轮没有“上一步”时间图；之后才有。零件库存包含备用件，剩件不必全部装上。候选预览只是预览，不保证当前可安装；是否可安装由执行器检查。','',
        '### 输出格式示例（具体编号以每题为准）','',
        '```json',
        '{"action":{"type":"attach","partId":"A03","candidate":"C017"}}',
        '```','',
        '上面是S。D额外提交`"unexpectedChange": false`，表示本轮是否发现超出自己上一步动作的变化；首次为false。M／E7直接提交下面这样的对象：','',
        '```json','{"type":"attach","partId":"A003","candidate":"C00017"}','```','',
        '装错或装不进去时返回拒绝信息，真实状态不改变；下一轮继续看新图。API拒绝、限流、超时与模型格式错误另外统计。','',
        '## 难度怎么读','',
        '**这些是暂定的结构分组，尚未用真人或模型成功率验证。** 不把L1直接说成“人一定觉得简单”。','',
        '| 暂定组 | 白话说明 | 本文件如何展示 |','|---|---|---|',
        '| L1：基础组合 | 当前记录中，没有20块及以上目标／拼装、参考路线临时拆正确件、多次事故这三项负担 | 每个已有类别都展示对应例子 |',
        '| L2：增加一项结构负担 | 上述三项里出现一项 | 可能是长一些，也可能是短模型的参考修法要先拆开返修 |',
        '| L3：叠加多项结构负担 | 上述三项里同时出现至少两项 | 例如长流程加连续事故；没有该组合的旧题库不虚填L3 |','',
        '“短／中／长”是另一条轴：本题规模≤12块、13–24块、≥25块。静态按本题目标件数，动态按要拼的模块／物件全长；整套社区套装的总零件数不是本题要操作的块数。遮挡与低对比另列，不自动把不可见的信息叫“困难”。参考修复长度也不等于最短解。','',
        '| 题库 | 全库物理题数 | L1 | L2 | L3 | 本文件覆盖组合数 |','|---|---:|---:|---:|---:|---:|']
    for bank in BANKS:
        rr=[r for r in rows if r['bank']==bank];counts=Counter(r['level'] for r in rr)
        lines.append(f'| {BANKS[bank]} | {len(rr)} | {counts["L1"]} | {counts["L2"]} | {counts["L3"]} | {sum(k[0]==bank for k in groups)} |')
    lines+=['','E7这里只计715道新增物理任务；另外83条复用旧题的接口条件不重复计数。M有96题，包含静态与动态各48题。','',
        '## 先认物件：完整外观参考','',
        '下图只帮助你认出是什么物件，属于审题说明，不是额外发送给模型的目标。具体该拼到哪一步，仍以每道题的右侧唯一目标为准。原S题是从套装中抽取的局部结构，不是整套模型复原任务。','',
        '原D中的42个简化完整物件：','',
        '![原动态题的42个完整物件，另有26个机制结构](../brickplan-dynamic-v6/object-gallery.png)','',
        '本轮扩展的21个配置，完整外观如下；同一套博物馆的两个操作范围不算两个独立来源。','']
    gallery=read(EXT/'gallery.json')
    for start in range(0,len(gallery),4):
        batch=gallery[start:start+4]
        headers=[m['title'] for m in batch]+['—']*(4-len(batch))
        pictures=['!['+m['title']+'](../brickplan-expansion-v7/'+m['fullImage']['file']+')' for m in batch]+['']*(4-len(batch))
        lines+=['| '+' | '.join(headers)+' |','|'+'---|'*4,'| '+' | '.join(pictures)+' |','']
    lines+=[
        '## 按类别和难度找题','',
        '表格每行都是一个真实存在的组合。点击Q编号跳到配图、实际输入输出和完整GT操作表。','',
        '| 例子 | 题库／任务 | 类别 | 暂定难度 | 该组合全库题数 | 物件 |','|---|---|---|---|---:|---|']
    for e in examples:
        if e['purpose']!='coverage':continue
        lines.append(f'| [{e["example"]}](#{e["example"].lower()}) | {e["bank"]}／{"静态" if e["mode"]=="static" else "动态"} | {label(e["family"])} | {e["level"]} | {e["cellCount"]} | {e["title"]} |')
    lines+=['','### 特殊诊断题','']
    for e in examples:
        if e['purpose']!='coverage':lines.append(f'- [{e["example"]}：{e["purpose"]}](#{e["example"].lower()})。')
    lines+=['','## 各题的图片、输入输出与GT','',
        '**动态题特别注意：**“上次动作前→现在”才是模型真正拿到的时间对照。“自己的安装完成后、后台改动前→后台改动后”是出题者用于解释GT的额外画面，不是默认给模型的输入。下面两种图分开标注。','']
    for e in examples:
        q=e['example'];p=e['profile'];dynamic=e['mode']=='dynamic';bank=e['bank'];n=e['targetParts']
        length=(e.get('moduleParts') or n) if dynamic else n
        process='短（≤12块）' if length<=12 else '中（13–24块）' if length<=24 else '长（≥25块）'
        covers=p.get('witnessCoverRemovals',p.get('witnessCorrectCoverRemovals',0)) or 0
        reasons=[]
        if length>=20:reasons.append('本题目标／拼装过程至少20块')
        if covers:reasons.append(f'这条参考修法临时拆下{covers}块本来正确的件')
        if len(e['events'])>=2:reasons.append(f'前后{len(e["events"])}次后台事件')
        visibility=('参考状态达到机器像素差异门槛，真人可读性待确认' if e['visibility'] is True or e['visibility']=='machine-visible'
                    else '动作被抵消，单列诊断' if e['visibility']=='action-cancellation'
                    else '低变化／遮挡，单列诊断' if e['visibility'] is False or e['visibility']=='low-contrast'
                    else '正常对照，无需识别后台错误' if e['family'] in ('none','control')
                    else '本例有实际渲染，尚未做独立真人可读性认证')
        lines += [f'<a id="{q.lower()}"></a>','',f'### {q} · {e["title"]} · {label(e["family"])} · {e["level"]}','',
            f'| 项目 | 内容 |','|---|---|',
            f'| 题目身份 | `{e["key"]}`'+(f'；公开题号 `{e["publicId"]}`' if e.get('publicId') else '')+' |',
            f'| 类别与任务 | {BANKS[bank]}；{"动态持续拼装" if dynamic else "静态修复"}；{label(e["family"])} |',
            f'| 暂定难度 | {e["level"]}：{LEVELS[e["level"]]}；不是实测成功率 |',
            f'| 为什么这样分 | '+('；'.join(reasons) or '本题没有记录到长流程、临时拆正确件、多次事件这三项负担')+' |',
            f'| 单独看过程长度 | {process}；与上面的结构组合难度不是同一回事 |',
            f'| 图像可见性 | {visibility} |',
            f'| 规模 | 目标中的可操作部分{n}块'+(f'；模块全长{e["moduleParts"]}块' if e.get('moduleParts') else '')+f'；库存含{e["inventoryParts"]}块可操作实物（含备用件） |',
            f'| GT路线 | 装拆共{e["referenceActions"]}次，另提交结束；不限定这条顺序，最短性未验证 |',
            f'| 计划中的动态事件 | {len(e["events"])}次'+('；后台时间表不发给模型' if e['events'] else '')+' |','',
            '**这题要做什么：** '+('从初始状态开始，边拼边看；遇到变化后自行调整，最后拼成右侧完整目标。' if dynamic else '把左侧状态修成右侧指定阶段；不要求继续拼后续完整成品。'),' ',
            '**错误解释（给审题者）：** '+(DESCRIPTIONS['none'] if dynamic and e['family'] in ('control','none') else family_note(e['family'])),'']
        if e.get('contextLocked') or bank=='M':lines+=['图里已有的主体固定不动；上面的目标块数只统计可操作模块，预装主体不算在这个数字里。','']
        if dynamic:
            lines+=['这是没有后台干扰的正常对照：初始还没拼完，需要自己逐件拼到目标。' if not e['events'] else '初始未拼完是正常起点，不是本题的错误；后台干扰是在下面指定的参考过程时刻才发生。实际模型路线不同，触发时刻也可能不同。','']
        if bank=='S':lines+=['本题来自原静态白底板库，是原套装抽取的局部结构；这里新生成了实际状态图，但不代表旧静态全库已完成真人视觉审核。','']
        if e['visibility'] is False or e['visibility'] in ('low-contrast','action-cancellation'):
            lines+=['**单列诊断：** '+('后台变化抵消了刚才的动作，时间图可能看起来没有变化；不能直接叫普通漏检。' if e['visibility']=='action-cancellation' else '已有机器检查标记为低变化／遮挡；不进入普通视觉漏检结论。'),'']
        lines+=['**1）开始答题时的图片：每张左边是当前，右边是唯一目标。**','']
        lines+=image_table(e['initial']['images'],{'current-target'})
        lines+=['**2）完整零件库存：有备用件，不要求用完。**','']
        inventory=[r for r in e['initial']['images'] if r['role']=='inventory']
        for start in range(0,len(inventory),3):lines+=image_table(inventory[start:start+3])
        lines += [f'[查看这题完整首轮输入JSON]({e["initial"]["input"]})。分类、难度、GT和后台事件说明在本审题文档中；不在首轮观察里。','']
        if e['manual']:
            lines+=['**可按需查看的说明书例子：**每步装一块，说明顺序不是强制顺序；整套说明书不会默认全部发送。','',
                image(e['manual'],'按需参考说明第1步'),'']
        if e['candidateExample']:
            preview=e['candidateExample'];lines+=['**按需查看位置的例子：**下图展示GT中某次安装所用零件的候选页／候选预览。它只说明接口怎么选位置，不表示这些候选现在都能装进去。','',
                '请求：`'+json.dumps(preview['request'],ensure_ascii=False,separators=(',',':'))+'`。','']
            lines+=image_table(preview['images'])
        for event in e['events']:
            lines += [f'**3.{event["number"]}）第{event["afterStep"]}次装拆之后，模型真正收到的下一轮输入。**','',
                '当前／目标：','']
            lines+=image_table(event['packet']['images'],{'current-target'})
            lines+=['时间对照：左边是模型上一次操作之前，右边是操作与后台事件之后的真实状态。','']
            lines+=image_table(event['packet']['images'],{'temporal-pair'})
            lines += [f'[这一轮完整输入JSON]({event["packet"]["input"]})。系统没有发消息告诉模型“你遇到了{label(event["family"])}”。','',
                '**仅给审题者看的后台GT：下图左侧时刻不默认提供给模型。**','',
                image(event['truthImage'],f'第{event["number"]}次后台事件的真实前后状态'),' ',
                '后台实际改动：'+'；'.join(('移走' if a['type']=='detach' else '装入')+a['partId']+'（'+a['description']+'）' for a in event['changes'])+'。','']
        first=e['gt'][0]['output'] if e['gt'] else e['finish']
        lines += ['**4）本题一个实际正确输出：**这是GT路线的第一条动作，不是要求一次输出整条路线。','',
            '```json',json.dumps(first,ensure_ascii=False),'```','',
            '**5）完整GT装拆表：**编号与本题图片、输入JSON一致。每行一次动作；表里的“干扰”是后台变化，不计作模型动作。','',
            '| 次数 | 动作 | 零件 | 选哪个位置 | 执行结果／随后变化 |','|---:|---|---|---|---|']
        if not e['gt']:lines+=['| 0 | 不需要装拆 | 当前已达阶段目标 | — | 直接结束 |']
        for a in e['gt']:
            pub=a['publicAction'];lines.append(f'| {a["step"]} | {"装上" if pub["type"]=="attach" else "拆下"} | `{pub["partId"]}`：{a["description"]} | '+(f'`{pub["candidate"]}`' if pub['type']=='attach' else '—')+' | 合法'+('；随后发生后台干扰' if a['eventAfterThisAction'] else '')+' |')
        lines += [f'| 最后 | 提交结束 | — | — | 参考路线通过 |','',
            '结束输出：`'+json.dumps(e['finish'],ensure_ascii=False,separators=(',',':'))+'`。','',
            '**GT关键状态图：**图上数字是上表装拆次数；为控制篇幅只画最多8个状态，完整操作没有省略。','',
            image(e['gtStrip'],'GT路线关键状态，不是模型结果'),' ',
            '**GT最终验收：左边是这条路线实际拼成的结果，右边是本题目标。**','',
            image(e['finalImage'],'GT实际终态与唯一目标'),' ',
            f'[完整GT和逐步状态JSON]({e["gtFile"]})。只验证“存在这条合法路线”，没有证明最短；其他合法拼法按最终结构验收。','',
            '[返回分类索引](#按类别和难度找题)','']
    lines += ['## 怎么用这份文档','',
        '- 你审题：看类别索引，核对每题的初态、唯一目标、零件库存和GT表；再看动态中间输入是否清楚。',
        '- 给真人：可以用它讨论题意；正式盲测要另外用不含错误名和GT的操作页面。',
        '- 给模型：只使用各题`inputs/`中的观察及其图像，按当前接口逐步执行；不能发送本Markdown或`gt/`目录。',
        '- 评分：先看最终是否完成；动态主修复结论还要求相同前半程的正常分支成功、计划事件实际触发、服务正常。未触发和服务错误单列。',
        '- 难度：仍需真实人类／模型成绩验证。本文没有虚构模型成功率、真人回答或错误发生频率。','',
        '## 全题库与来源入口','',
        '- [5,975道任务的统一来源索引](../brickplan-expansion-v7/global-splits.csv)。',
        '- [798条扩展条件逐题清单，含83条旧题的新接口条件](../brickplan-expansion-v7/MODEL-CASE-CATALOG.zh-CN.md)。',
        '- [原静态题库说明](../brickplan-static-plate5/README.zh-CN.md)、[原动态全部物件](../brickplan-dynamic-v6/OBJECTS.zh-CN.md)、[原社区模块清单](../brickplan-community-modules/MODEL-CASE-CATALOG.zh-CN.md)。',
        '- [30个网上来源、18种人类错误／问题和纳入范围](../brickplan-expansion-v7/human-error-research/README.zh-CN.md)。','']
    (OUT/'README.zh-CN.md').write_text('\n'.join(line.rstrip() for line in lines).rstrip()+'\n')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--resume',action='store_true');args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);rows,old_modules,new_models=dataset();examples,groups=select(rows)
    dump(OUT/'selection.json',[{k:v for k,v in r.items() if k!='case'} for r in examples])
    current=None;ctx=None;results={}
    for row in sorted(examples,key=lambda r:(r['bank'],r['model'],r['example'])):
        saved=OUT/'examples'/(row['example']+'.json')
        if args.resume and saved.exists():
            result=read(saved)
            result['title']=row['title']
            gt=read(OUT/result['gtFile']);gt.pop('referenceIsUnique',None)
            gt.update(requiredReferenceOrder=False,referenceIsShortest=None,optimalityCertified=False)
            dump(OUT/result['gtFile'],gt)
            result.setdefault('contextLocked',row['bank']=='M' or row['bank']=='E7' and not row['model'].startswith('v7-long-'))
            if row['bank'] in ('S','D'):
                for p in [result['initial']['input'],*[e['packet']['input'] for e in result['events']]]:
                    data=read(OUT/p);data['system']=S_SYSTEM if row['bank']=='S' else D_SYSTEM;dump(OUT/p,data)
            dump(saved,result)
        else:
            key=row['bank'],row['model']
            if key!=current:ctx=context(row,old_modules);current=key
            result=build_example(row,ctx)
        results[row['example']]=result
        print('EXAMPLE',row['example'],row['bank'],row['mode'],row['family'],row['level'],flush=True)
    ordered=[results[r['example']] for r in examples]
    write_markdown(ordered,groups,rows)
    dump(OUT/'manifest.json',dict(examples=[{k:v for k,v in e.items() if k not in ('gt','initial','events','candidateExample')} for e in ordered],
        completeCellCoverage=len(groups),examplesCount=len(ordered),newModelConfigurationsCovered=len({r['model'] for r in examples if r['bank']=='E7'}),
        selectionPolicy='One per populated bank/mode/category/structural group, plus three diagnostics; no empirical performance selection',
        representedPhysicalTasks=5975,referenceWitnessesPassed=len(ordered),apiModelCalls=0,
        sourceFiles={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [
            Path(__file__),EXT/'global-splits.json',EXT/'difficulty-all.json',
            ROOT/'deliverables/brickplan-static-plate5/cases.jsonl',ROOT/'deliverables/brickplan-dynamic-v6/cases.private.json',
            ROOT/'deliverables/brickplan-community-modules/cases.private.jsonl']}))
    print('DONE',len(ordered),'examples',len(groups),'populated cells',flush=True)


if __name__=='__main__':main()
