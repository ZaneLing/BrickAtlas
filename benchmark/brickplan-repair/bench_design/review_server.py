"""Local click-only independent review; persistent per person, role, and task."""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs
from pathlib import Path
from collections import OrderedDict,Counter
from copy import deepcopy
import argparse,base64,hashlib,io,json,secrets,threading,time,zipfile
import re
import numpy as np
from PIL import Image,ImageDraw
from bench_design.challenges import QUALITY
from bench_design.session import Session,INPUT_VERSION,digest
from bench_design.run_episode import load
from expansion_v7.build import read,write
from render import FONT

HERE=Path(__file__).resolve().parent
PEOPLE=('A','B','C')
BLIND_OPTIONS={
    'goal':('yes','no','unsure'),
    'view':('clear','clear_after_views','unclear'),
    'operation':('clear','positions_confusing','feedback_confusing','unusable'),
    'change':('yes','no','unsure'),
    'effort':('independent','helped','unfinished')}
PHYSICS_OPTIONS={'verdict':('possible','impossible','uncertain'),
    'reason':('clear_path','blocked_path','overlap','connection_uncertain','needs_fixture','unclear_image'),
    'method':('images','third_party_software','physical_parts')}


def atomic(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.pending')
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    temporary.replace(path)


class Server(ThreadingHTTPServer):
    daemon_threads=True
    def __init__(self,address,data=None):
        self.tasks=read(QUALITY/'review-tasks.private.json')
        self.maps={role:{r['code']:r for r in self.tasks[role]} for role in ['blind','physics']}
        self.probes={p['code']:p for p in read(QUALITY/'physics-probes.private.json.gz')['probes']}
        self.data=Path(data or QUALITY/'submissions').resolve();self.data.mkdir(parents=True,exist_ok=True)
        self.assets={};self.downloads={};self.sessions=OrderedDict();self.lock=threading.RLock()
        keyfile=self.data/'manager-key.private.json'
        if not keyfile.exists():atomic(keyfile,dict(key=secrets.token_urlsafe(24)))
        self.manager=read(keyfile)['key']
        super().__init__(address,Handler)

    def identity(self,person,role,code):
        if person not in PEOPLE or role not in self.maps or code not in self.maps[role]:raise ValueError('审查者或题号无效')
        return self.data/person/role/code

    def state(self,person,role,code):
        folder=self.identity(person,role,code);p=folder/'review.json'
        if p.exists():
            value=read(p)
            if value['taskVersion']!=self.tasks['taskVersion'] or value['inputVersion']!=INPUT_VERSION:
                raise ValueError('题目版本已变，请开启新审核轮次，不能覆盖旧答案')
            return value
        return dict(reviewer=person,role=role,code=code,taskVersion=self.tasks['taskVersion'],
                    inputVersion=INPUT_VERSION,ratings={},submitted=False,requestIds=[],answerRevision=0,
                    createdAt=time.time(),notImportedFromOtherReviewer=True)

    def save_state(self,value):
        folder=self.identity(value['reviewer'],value['role'],value['code'])
        atomic(folder/'review.json',value)

    def session(self,person,code):
        folder=self.identity(person,'blind',code);key=(person,code)
        if key in self.sessions:
            self.sessions.move_to_end(key);return self.sessions[key]
        session=Session.open(self.maps['blind'][code]['caseId'],folder/'execution',actor='human:'+person)
        record=folder/'execution/record.private.json.gz'
        if record.exists():
            saved=read(record);session.autosave=False
            if saved['caseId']!=session.row['key'] or saved['inputVersion']!=INPUT_VERSION:
                raise ValueError('历史操作与本题不匹配')
            for r in saved['records']:
                session._pending_observation=r.get('observation')
                session.submit(r['action'],r.get('parseError',False),r.get('requestEvidence'),r.get('clientRequestId'))
            if session.ep.state!=saved['final'] or digest(session.records)!=digest(saved['records']):
                raise ValueError('历史操作回放不一致，已保留原记录，请联系组织者')
            session.run_id=saved['runId'];session.autosave=True
            pending=folder/'execution/pending-observation.private.json'
            if pending.exists():
                current=read(pending)
                if current.get('decision')==len(session.records)+1:session._pending_observation=current
        self.sessions[key]=session
        while len(self.sessions)>4:self.sessions.popitem(last=False)
        return session

    def register_image(self,asset):
        path=Path(asset['file']).resolve();sha=asset.get('sha256') or hashlib.sha256(path.read_bytes()).hexdigest()
        self.assets[sha]=path
        return {**asset,'file':'/assets/'+sha+'.png','sha256':sha}

    def observe(self,person,role,code):
        value=self.state(person,role,code)
        if role=='blind':
            session=self.session(person,code);obs=session.observe()
            obs['images']=[self.register_image(x) for x in obs['images']]
            # No native score, event ledger, reference actions, or private labels.
            return dict(code=code,role=role,reviewer=person,revision=len(session.records),
                observation=obs,ratings=value['ratings'],submitted=value['submitted'],answerRevision=value['answerRevision'])
        probe=self.probes[code]
        blind_code=probe.get('sameAsBlindCase')
        if blind_code and not self.state(person,'blind',blind_code)['submitted']:
            return dict(code=code,role=role,reviewer=person,locked=True,requiredBlindTask=blind_code,
                        message='先独立完成对应盲做题，再看这道拆装检查，避免提前获得操作提示。')
        assets=self.physics_images(probe)
        return dict(code=code,role=role,reviewer=person,revision=0,
            actionDescription=('拆下' if probe['action']['type']=='detach' else '装上')+'图中单独展示的这一块',
            externalScenePackage=self.physics_package(probe),
            images=assets,ratings=value['ratings'],submitted=value['submitted'],answerRevision=value['answerRevision'],
            rules=['只判断图示单块动作是否存在直线取放通路，不要求照某一条参考路线。',
                   '夹具允许托住分离子结构；重力、摩擦、卡扣力度不在此项判断范围。',
                   '不确定就选“无法判断”；图像判断与实物、第三方软件复核分别记录。'])

    def physics_package(self,probe):
        """Actual before/proposed source geometry for independent software review.

        Supplied only after the blind-operation gate. No target, engine verdict,
        event label, reference repair, or correct candidate is exported.
        """
        cache=self.data/'public-probe-assets'/probe['code'];cache.mkdir(parents=True,exist_ok=True)
        path=cache/'external-scenes.zip'
        if not path.exists():
            row,ep,_,_=load(probe['caseId'],cache)
            rt=ep.runtime;actor=probe['action']['actor']
            def ldraw(parts):
                lines=['0 Independent review geometry; no legality verdict or target']
                for aid,p in sorted(parts.items()):
                    raw=p.get('rawMatrix');matrix=np.asarray(raw if raw is not None else p['matrix'])
                    number=p.get('partNumber',p.get('canonical')) if raw is not None else p['canonical']
                    number=str(number);number=number if number.lower().endswith('.dat') else number+'.dat'
                    lines.append('0 '+('MOVING_PART' if aid==actor else 'CONTEXT'))
                    values=[*matrix[:3,3],*matrix[:3,:3].flat]
                    lines.append('1 '+str(p.get('colorCode',16))+' '+' '.join(f'{v:.9g}' for v in values)+' '+number)
                return '\n'.join(lines)+'\n'
            def scene(state):
                return {**{a:r['part'] for a,r in rt.cert.get('conservativeContext',{}).items()},**rt.present(state)}
            key=probe['state'][actor] if probe['action']['type']=='detach' else probe['action']['candidate']
            environment={k:rt.cert[k] for k in ['environmentMode','tableY','baseplate','boundary'] if k in rt.cert}
            environment['coordinateSystem']='LDraw coordinates, LDU; the supplied fixture/table/board rules still apply.'
            temporary=path.with_suffix('.pending.zip')
            with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED) as z:
                z.writestr('before.ldr',ldraw(scene(probe['state'])))
                z.writestr('proposed.ldr',ldraw(scene(probe['proposed'])))
                z.writestr('moving-part.ldr',ldraw({actor:rt.row(key)['part']}))
                z.writestr('environment.json',json.dumps(environment,ensure_ascii=False,indent=2))
                z.writestr('README.txt','独立拆装检查：before.ldr是动作前，proposed.ldr是假设动作后，moving-part.ldr是唯一移动件。\n用带LDraw零件库的独立软件打开；若软件缺零件或场景不完整，请选无法判断。\n背景中的未确定碰撞件也完整导出，不能把它们删掉后宣称原题可行。\n桌面／底板规则另见environment.json；虚拟平面不一定是LDraw实体。\n只比较指定单件的直线取放，不模拟重力、摩擦、卡扣力度。没有提供目标答案或合法性结论。\n')
            temporary.replace(path)
        token=hashlib.sha256(path.read_bytes()).hexdigest();self.downloads[token]=path
        return dict(file='/downloads/'+token+'.zip',sha256=token,format='LDraw source parts, before/proposed only',notTarget=True)

    def physics_images(self,probe):
        cache=self.data/'public-probe-assets'/probe['code'];index=cache/'images.json'
        if index.exists():
            stored=read(index)
            if isinstance(stored,dict) and stored.get('renderVersion')==2:
                return [self.register_image(x) for x in stored['assets']]
        cache.mkdir(parents=True,exist_ok=True)
        row,ep,packet,renderer=load(probe['caseId'],cache)
        renderer=packet.renderer if packet else renderer
        frame=['_module_frame'] if '_module_frame' in renderer.bounds else None
        assets=[];actor=probe['action']['actor'];key=probe['state'][actor] if probe['action']['type']=='detach' else probe['action']['candidate']
        def save(image,role,**meta):
            stream=io.BytesIO();image.save(stream,format='PNG');data=stream.getvalue();sha=hashlib.sha256(data).hexdigest();path=cache/(sha+'.png');path.write_bytes(data)
            assets.append(dict(file=str(path),sha256=sha,role=role,width=image.width,height=image.height,**meta))
        for view in ['isometric','rear','top']:
            image=Image.new('RGB',(1600,636),'white');draw=ImageDraw.Draw(image)
            for x,state,title in [(0,probe['state'],'BEFORE'),(800,probe['proposed'],'PROPOSED RESULT - NOT A LEGALITY VERDICT')]:
                im,mask=renderer.rgb(state,view,size=(800,600),frame_keys=frame,supersample=1)
                from PIL import ImageFilter
                selected=Image.fromarray(np.uint8(mask==renderer.ids[actor])*255)
                outer=np.asarray(selected.filter(ImageFilter.MaxFilter(7))).astype(int)
                border=Image.fromarray(np.uint8(np.maximum(0,outer-np.asarray(selected).astype(int))))
                im.paste((0,151,164),(0,0),border)
                image.paste(im,(x,36));draw.text((x+10,8),title,font=FONT,fill='#17283a')
            save(image,'physical-before-proposed',view=view)
        im,_=renderer.rgb({actor:key},'isometric',only=actor,size=(400,300),supersample=1)
        save(im,'moving-piece')
        # Show the first portion of the declared test ray without publishing its verdict.
        verdict=probe['engineResult'];direction=verdict.get('path')
        if direction:
            distance=min(20.,verdict['pathLengthLDU']);original=renderer.geometry[key]
            image=Image.new('RGB',(1600,340),'white');draw=ImageDraw.Draw(image)
            try:
                fractions=[0.,.25,.5,1.] if probe['action']['type']=='detach' else [1.,.5,.25,0.]
                for i,fraction in enumerate(fractions):
                    temporary='__review_motion__'
                    shift=np.asarray(direction)*distance*fraction*np.array([1,-1,-1])
                    renderer.geometry[temporary]=(original[0]+shift,original[1])
                    im,_=renderer.rgb({**probe['state'],actor:temporary},'isometric',size=(400,300),frame_keys=frame,supersample=1)
                    image.paste(im,(i*400,36));draw.text((i*400+8,8),f'PROPOSED TRANSLATION {distance*fraction:.1f} LDU',font=FONT,fill='#17283a')
                save(image,'proposed-path-prefix',shownLengthLDU=distance)
            finally:renderer.geometry.pop('__review_motion__',None)
        atomic(index,dict(renderVersion=2,assets=assets))
        return [self.register_image(x) for x in assets]

    def summary(self):
        out=[];physics=[]
        for role in ['blind','physics']:
            for code,task in self.maps[role].items():
                entries=[self.state(person,role,code) for person in PEOPLE]
                submitted=[r for r in entries if r['submitted']]
                votes=[r for r in submitted if r['ratings'].get('independent') is True and
                       (role!='blind' or r['ratings'].get('effort')!='helped')]
                if role=='blind':
                    success=[]
                    for v in votes:
                        record=self.identity(v['reviewer'],role,code)/'execution/record.private.json.gz'
                        success.append(read(record)['normalizedResult']['success'])
                    concerns=[v['reviewer'] for v in submitted if v['ratings']['goal']!='yes' or
                        v['ratings']['view']=='unclear' or v['ratings']['operation']!='clear' or
                        v['ratings']['effort']!='independent']
                    status='需要检查题面／操作' if concerns else '有非独立反馈，待独立检查' if submitted and not votes else '待真人检查' if not votes else '盲做未全部成功，需要复查' if not all(success) else '盲做初步通过' if len(votes)>=3 else '还需独立参与者'
                    out.append(dict(code=code,caseId=task['caseId'],independentSubmissions=len(votes),
                        totalSubmissions=len(submitted),nonIndependentSubmissions=len(submitted)-len(votes),
                        successfulOperations=sum(x is True for x in success),concerns=concerns,status=status,
                        reportedChangeVotes=dict(Counter(v['ratings']['change'] for v in votes)),
                        verdictScope='仅对应本题和当前输入版本，不外推整个物件或全题库'))
                else:
                    probe=self.probes[code];expected=probe['engineResult']['code']=='OK'
                    disputes=[v['reviewer'] for v in votes if v['ratings']['verdict']=='uncertain' or
                        (v['ratings']['verdict']=='possible')!=expected]
                    backend=probe['independentResult']['status']
                    backend_issue=backend in ('needs-review','accepted-action-has-independent-collision')
                    status='独立几何发现待查项，暂停纳入' if backend_issue else '待真人拆装检查' if not votes else '拆装判断存在分歧，暂停纳入' if disputes else '图像与独立几何初查通过' if len(votes)>=3 else '还需独立参与者'
                    documented=[v['reviewer'] for v in votes if v['ratings'].get('method')!='images' and v.get('evidence')]
                    physics.append(dict(code=code,caseId=task['caseId'],independentSubmissions=len(votes),
                        totalSubmissions=len(submitted),nonIndependentSubmissions=len(submitted)-len(votes),
                        independentBackend=backend,disputes=disputes,status=status,documentedExternalChecks=documented,
                        realAssemblyQualified=False))
        admission=[]
        for row in out:
            related=[p for p in physics if p['caseId']==row['caseId']]
            unresolved=[p['code'] for p in related if p['independentBackend'] in
                ('needs-review','accepted-action-has-independent-collision') or p['disputes']]
            status=('拆装存在待查项，暂停纳入' if unresolved else
                '盲做尚未通过' if row['status']!='盲做初步通过' else
                '盲做通过，尚无本题独立拆装抽查' if not related else
                '还需真人独立判断拆装' if any(p['status']!='图像与独立几何初查通过' for p in related) else
                '本题图像与几何初查通过；不代表实物验证')
            admission.append(dict(code=row['code'],caseId=row['caseId'],status=status,
                relatedPhysics=[p['code'] for p in related],unresolvedPhysics=unresolved,
                realAssemblyQualified=False))
        result=dict(inputVersion=INPUT_VERSION,taskVersion=self.tasks['taskVersion'],
            blind=out,physics=physics,submittedBlind=sum(x['independentSubmissions'] for x in out),
            admission=admission,
            receivedBlindResponses=sum(x['totalSubmissions'] for x in out),
            receivedPhysicsResponses=sum(x['totalSubmissions'] for x in physics),
            submittedPhysics=sum(x['independentSubmissions'] for x in physics),
            blindStatusCounts=dict(Counter(x['status'] for x in out)),physicsStatusCounts=dict(Counter(x['status'] for x in physics)),
            wholeDatasetHumanQualified=False,causalHumanModelComparison=False,
            policy='每人每题按一次独立提交计数；分歧保留；未检查题不自动通过；图像一致不能代替实物验证。')
        atomic(self.data/'qualification-summary.json',result)
        return result


class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def send(self,value,status=200,kind='application/json'):
        if kind=='application/json':value=json.dumps(value,ensure_ascii=False).encode()
        elif isinstance(value,str):value=value.encode()
        self.send_response(status);self.send_header('Content-Type',kind+'; charset=utf-8');self.send_header('Content-Length',str(len(value)))
        self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(value)
    def do_GET(self):
        u=urlparse(self.path);q=parse_qs(u.query)
        try:
            if u.path in ('/','/A','/B','/C'):
                return self.send((HERE/'human_review.html').read_text(),kind='text/html')
            if u.path=='/health':return self.send(dict(ok=True,inputVersion=INPUT_VERSION,tasks={k:len(v) for k,v in self.server.maps.items()}))
            if u.path=='/api/tasks':
                person=q.get('reviewer',['A'])[0];role=q.get('role',['blind'])[0]
                if person not in PEOPLE or role not in self.server.maps:raise ValueError('审查者无效')
                tasks=[]
                for code,item in self.server.maps[role].items():
                    saved=self.server.state(person,role,code)
                    tasks.append(dict(code=code,mode=item.get('mode'),priority=item.get('priority',False),submitted=saved['submitted']))
                if role=='blind':
                    priority=[x for x in tasks if x['priority']];others=[x for x in tasks if not x['priority']]
                    shift=PEOPLE.index(person);tasks=priority[shift:]+priority[:shift]+others
                return self.send(dict(tasks=tasks,reviewer=person,role=role,inputVersion=INPUT_VERSION))
            if u.path=='/api/summary':
                if q.get('key',[''])[0]!=self.server.manager:return self.send(dict(message='仅组织者可以查看汇总'),403)
                with self.server.lock:return self.send(self.server.summary())
            match=re.fullmatch(r'/assets/([0-9a-f]{64})\.png',u.path)
            if match and match.group(1) in self.server.assets:
                p=self.server.assets[match.group(1)];return self.send(p.read_bytes(),kind='image/png')
            match=re.fullmatch(r'/downloads/([0-9a-f]{64})\.zip',u.path)
            if match and match.group(1) in self.server.downloads:
                return self.send(self.server.downloads[match.group(1)].read_bytes(),kind='application/zip')
            return self.send(dict(message='地址不存在'),404)
        except (ValueError,KeyError) as exc:return self.send(dict(message=str(exc)),400)
    def do_POST(self):
        try:
            origin=self.headers.get('Origin')
            if origin and origin not in (f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'):
                raise ValueError('只接受本机页面提交')
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<10_000_000:raise ValueError('请求大小无效')
            data=json.loads(self.rfile.read(length))
            if not isinstance(data,dict):raise ValueError('请求格式无效')
            person,role,code=(data.get(k) for k in ('reviewer','role','code'))
            self.server.identity(person,role,code)
            with self.server.lock:
                saved=self.server.state(person,role,code)
                if self.path=='/api/open':return self.send(self.server.observe(person,role,code))
                if self.path=='/api/action':
                    if role!='blind' or saved['submitted']:raise ValueError('本题已提交或不是操作题')
                    request=data.get('requestId')
                    if not isinstance(request,str) or not 1<=len(request)<=100:raise ValueError('请求编号无效')
                    session=self.server.session(person,code)
                    if request in saved['requestIds'] or any(r.get('clientRequestId')==request for r in session.records):return self.send(self.server.observe(person,role,code))
                    if data.get('revision')!=len(session.records):return self.send({**self.server.observe(person,role,code),'message':'已恢复本题最新状态；操作没有重复执行。'},409)
                    feedback=session.submit(data.get('action'),client_request_id=request)
                    saved['requestIds'].append(request);saved['updatedAt']=time.time();self.server.save_state(saved)
                    return self.send({**self.server.observe(person,role,code),'lastFeedback':feedback})
                if self.path in ('/api/ratings','/api/submit'):
                    if saved['submitted']:return self.send(self.server.observe(person,role,code))
                    choices=BLIND_OPTIONS if role=='blind' else PHYSICS_OPTIONS
                    supplied=data.get('ratings',{})
                    if not isinstance(supplied,dict) or set(supplied)-set(choices)-{'independent','locatedParts'}:raise ValueError('选择字段无效')
                    for key,value in supplied.items():
                        if key in choices and value not in choices[key]:raise ValueError('选项无效')
                    if 'independent' in supplied and type(supplied['independent']) is not bool:raise ValueError('请确认独立完成')
                    if 'locatedParts' in supplied:
                        if role!='blind' or not isinstance(supplied['locatedParts'],list) or len(supplied['locatedParts'])>200:raise ValueError('定位选择无效')
                        ep=self.server.session(person,code).ep
                        allowed=set(getattr(ep,'actor_alias',getattr(ep,'alias',{})).values())
                        if not set(supplied['locatedParts'])<=allowed:raise ValueError('零件编号无效')
                    # Each request carries a monotonic client answer revision. An old
                    # autosave cannot overwrite a newer answer or another task.
                    rev=data.get('answerRevision')
                    if type(rev) is not int or rev<saved['answerRevision']:
                        return self.send(self.server.observe(person,role,code))
                    saved['ratings'].update(supplied);saved['answerRevision']=rev
                    if self.path=='/api/submit':
                        if any(k not in saved['ratings'] for k in choices):
                            raise ValueError('请完成本题的选择；不需要填写文字。')
                        saved['ratings'].setdefault('independent',False)
                        if role=='blind' and not self.server.session(person,code).done:
                            raise ValueError('请先结束本题操作；未拼完也可以按“结束并提交当前状态”。')
                        if role=='physics':
                            probe=self.server.probes[code];required=probe.get('sameAsBlindCase')
                            if required and not self.server.state(person,'blind',required)['submitted']:
                                raise ValueError('请先完成对应盲做题，避免提前看到操作提示。')
                        saved['submitted']=True;saved['submittedAt']=time.time()
                    self.server.save_state(saved)
                    if self.path=='/api/submit':self.server.summary()
                    return self.send(self.server.observe(person,role,code))
                if self.path=='/api/evidence':
                    if role!='physics' or saved['submitted']:raise ValueError('只能在拆装检查提交前添加证据')
                    raw=base64.b64decode(data.get('imageBase64',''),validate=True)
                    if len(raw)>5_000_000:raise ValueError('图片请小于5MB')
                    im=Image.open(io.BytesIO(raw));im.verify()
                    if im.format not in ('PNG','JPEG'):raise ValueError('只接受PNG或JPEG')
                    sha=hashlib.sha256(raw).hexdigest();p=self.server.identity(person,role,code)/('evidence-'+sha+('.png' if im.format=='PNG' else '.jpg'))
                    p.write_bytes(raw);saved['evidence']=dict(sha256=sha,file=p.name);self.server.save_state(saved)
                    return self.send(dict(saved=True,sha256=sha))
                raise ValueError('接口不存在')
        except (ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
            return self.send(dict(message=str(exc)),400)
        except Exception as exc:
            # A harness error is visible and is never converted into a human failure.
            return self.send(dict(message='页面处理遇到问题，答案已保留，请重试。',category='harness_error',detail=type(exc).__name__),500)


def main():
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8808);p.add_argument('--data-dir',type=Path);a=p.parse_args()
    server=Server(('127.0.0.1',a.port),a.data_dir)
    print(f'参与者：http://127.0.0.1:{a.port}/A  /B  /C',flush=True)
    print(f'组织者：http://127.0.0.1:{a.port}/?manager={server.manager}',flush=True)
    try:server.serve_forever()
    finally:server.server_close()


if __name__=='__main__':main()
