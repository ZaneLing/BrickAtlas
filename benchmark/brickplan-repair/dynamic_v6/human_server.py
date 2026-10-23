"""Local A/B/C interactive review. All actions are clicks; every case resumes independently."""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from collections import Counter
import json,re,sys,threading,hashlib,argparse
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'eval')]
from dynamic_v6.episode import BANK,DynamicEpisode,load_case
from dynamic_v6.interface import renderer_for,packet
from dynamic_v5.build import write
from expansion_v7.scope import allowed
OUT=BANK/'human-review'
PAGE=HERE/'human.html'

def review_tasks():
    cases=[c for c in json.loads((BANK/'cases.private.json').read_text())['cases'] if allowed(c)]
    previous=OUT/'answer-key.private.json'
    if previous.exists():
        accepted={c['id'] for c in cases}
        # Preserve existing human task identities and their saved answers.
        return {code:cid for code,cid in json.loads(previous.read_text()).items() if cid in accepted}
    selected=[];coverage=Counter()
    audit=json.loads((BANK/'audit.json').read_text())
    visible={r['caseId'] for r in audit['rows'] if r['primaryMachineCandidate']}
    # Three tasks per complete object: normal, earlier disturbance, late disturbance.
    for mid in sorted({c['modelId'] for c in cases if c['track']=='complete-object'}):
        rows=[c for c in cases if c['modelId']==mid]
        selected.append(next(c for c in rows if c['kind']=='none'))
        events=[c for c in rows if c['kind']!='none']
        for stage in ('early','late'):
            options=[c for c in events if c['stage']==stage]
            if options:
                # Prefer ordinary visible cases, balance categories, never use subject answers.
                options=[c for c in options if c['id'] in visible] or options
                chosen=min(options,key=lambda c:(coverage[c['kind']],hashlib.sha256(('human-v6:'+c['id']).encode()).hexdigest()))
                selected.append(chosen);coverage[chosen['kind']]+=1
    selected.sort(key=lambda c:hashlib.sha256(('blind-task-order-v6:'+c['id']).encode()).hexdigest())
    return {f'H{i+1:03}':c['id'] for i,c in enumerate(selected)}

class Server(ThreadingHTTPServer):
    def __init__(self,address):
        OUT.mkdir(parents=True,exist_ok=True);self.tasks=review_tasks();self.sessions={};self.lock=threading.RLock()
        write(OUT/'answer-key.private.json',self.tasks)
        super().__init__(address,Handler)

class Handler(BaseHTTPRequestHandler):
    def send(self,data,kind='application/json',status=200):
        if isinstance(data,dict):data=json.dumps(data,ensure_ascii=False).encode()
        elif isinstance(data,str):data=data.encode()
        self.send_response(status);self.send_header('Content-Type',kind+'; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
    def do_GET(self):
        u=urlparse(self.path)
        if u.path in ('/','/A','/B','/C'):return self.send(PAGE.read_text(),'text/html')
        if u.path in ('/gallery','/gallery.html'):return self.send((BANK/'gallery.html').read_text(),'text/html')
        if u.path in ('/README.zh-CN.md','/FIX-REPORT.zh-CN.md','/INPUT-OUTPUT.zh-CN.md','/EVALUATION.zh-CN.md','/OBJECTS.zh-CN.md'):
            return self.send((BANK/u.path[1:]).read_text(),'text/plain')
        model=re.fullmatch(r'/models/([a-z0-9-]+)/target\.png',u.path)
        if model and (BANK/'models'/model.group(1)/'target.png').is_file():
            return self.send((BANK/'models'/model.group(1)/'target.png').read_bytes(),'image/png')
        if u.path=='/health':return self.send(dict(ok=True,version=6,tasks=len(self.server.tasks)))
        if u.path=='/api/tasks':
            reviewer=parse_qs(u.query).get('reviewer',['A'])[0]
            if reviewer not in 'ABC' or len(reviewer)!=1:return self.send(dict(message='无效审查者'),status=400)
            tasks=[]
            for code in self.server.tasks:
                p=OUT/'runs'/f'{reviewer}-{code}.json';saved=json.loads(p.read_text()) if p.exists() else {}
                tasks.append(dict(code=code,finished=saved.get('episode',{}).get('score',{}).get('finished',False),steps=len(saved.get('episode',{}).get('records',[]))))
            return self.send(dict(tasks=tasks))
        m=re.fullmatch(r'/images/([0-9a-f]{64}\.png)',u.path)
        if m and (OUT/'images'/m.group(1)).is_file():return self.send((OUT/'images'/m.group(1)).read_bytes(),'image/png')
        self.send(dict(message='地址无效'),status=404)
    def body(self):
        size=int(self.headers.get('Content-Length','0'))
        if not 0<size<12000:raise ValueError('请求大小无效')
        data=json.loads(self.rfile.read(size))
        if not isinstance(data,dict):raise ValueError('请求无效')
        return data
    def load(self,reviewer,code,restart=False):
        if reviewer not in ('A','B','C') or code not in self.server.tasks:raise ValueError('题号无效')
        key=reviewer+'-'+code;path=OUT/'runs'/(key+'.json')
        if key in self.server.sessions and not restart:return self.server.sessions[key]
        cert,case=load_case(self.server.tasks[code]);ep=DynamicEpisode(cert,case)
        extra=None;request_ids=[];attempt=1
        if path.exists():
            saved=json.loads(path.read_text());attempt=saved.get('attempt',1)
            if restart:
                archive=OUT/'runs'/'archive';archive.mkdir(parents=True,exist_ok=True)
                write(archive/f'{key}-attempt-{attempt:03}.json',saved);attempt+=1
            else:
                if saved['sourceSha256']!=cert['contentSha256'] or saved['episode']['caseId']!=case['id']:raise ValueError('题库版本已变化，请开启新回合')
                for r in saved['episode']['records']:ep.step(r.get('submittedAction',r['action']))
                ep.judgments=saved['episode'].get('changeJudgments',[]);extra=saved.get('extra');request_ids=saved.get('requestIds',[])
        s=dict(key=key,code=code,reviewer=reviewer,episode=ep,renderer=renderer_for(ep),extra=extra,requestIds=request_ids,attempt=attempt,path=path)
        self.server.sessions[key]=s;return s
    def save(self,s):
        write(s['path'],dict(reviewer=s['reviewer'],code=s['code'],attempt=s['attempt'],sourceSha256=s['episode'].input_certificate['contentSha256'],extra=s['extra'],requestIds=s['requestIds'],episode=s['episode'].export()))
    def view(self,s,feedback=None):
        ep=s['episode'];obs,imgs=packet(ep,s['renderer'],OUT,s['extra'])
        return dict(code=s['code'],reviewer=s['reviewer'],revision=len(ep.records),budget=ep.decision_budget,images=imgs,handles=obs['actionHandles'],feedback=feedback,
                    lastAction=ep.history[-1] if ep.history else None,finished=ep.finished,success=ep.success,budgetExhausted=ep.budget_exhausted,
                    inspectedPart=s['extra'].get('partId') if s['extra'] else None)
    def do_POST(self):
        try:
            data=self.body();reviewer=data.get('reviewer');code=data.get('code')
            with self.server.lock:
                if self.path=='/api/open':
                    s=self.load(reviewer,code,restart=data.get('restart') is True);self.save(s);return self.send(self.view(s))
                if self.path!='/api/step':raise ValueError('地址无效')
                s=self.load(reviewer,code);ep=s['episode'];request_id=data.get('requestId')
                if not isinstance(request_id,str) or not 1<=len(request_id)<=100:raise ValueError('缺少请求编号')
                if request_id in s['requestIds']:return self.send(self.view(s))
                if data.get('revision')!=len(ep.records):return self.send({**self.view(s), 'message':'已同步最新状态；该操作没有重复执行'},status=409)
                if ep.finished:raise ValueError('这道题已提交，可换题或重新开始')
                fb=ep.submit(dict(action=data.get('action'),unexpectedChange=data.get('unexpectedChange')))
                action=data.get('action') or {};s['extra']=({'partId':fb['partId']} if 'partId' in fb else action) if action.get('type')=='inspect' and fb['code']=='OBSERVED' else None
                s['requestIds'].append(request_id);self.save(s);return self.send(self.view(s,fb))
        except (ValueError,KeyError,TypeError,json.JSONDecodeError) as e:return self.send(dict(message=str(e)),status=400)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8767);a=p.parse_args()
    server=Server(('127.0.0.1',a.port));print(f'http://127.0.0.1:{a.port}/A  /B  /C',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
