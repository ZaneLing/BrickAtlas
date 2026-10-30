"""Local review: GT checking, blind operation and physical judgment are separate."""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs
from pathlib import Path
from copy import deepcopy
import argparse,json,re,threading,time,os,tempfile
from reliability import OUT
from reliability.run import Offline
from bench_design.session import Session,internal_action,digest
from dynamic_arena.tool_arena import ToolArena
from dynamic_arena import OUT as ARENA
from expansion_v7.build import read

def write(path,value):
 """A completed answer replaces the previous file atomically."""
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=path.parent,delete=False) as f:
  temporary=Path(f.name);json.dump(value,f,ensure_ascii=False);f.flush();os.fsync(f.fileno())
 temporary.replace(path)

CHOICES={'gt':['correct','problem','unclear'],'blind':['independent','unclear','unfinished'],
         'physics':['possible','impossible','unclear']}

class Server(ThreadingHTTPServer):
 def __init__(self,address,data=None):
  self.catalog=read(OUT/'review/tasks.private.json');self.tasks={r['code']:r for r in self.catalog['tasks']}
  self.probes={p['code']:p for p in read(OUT/'review/geometry.private.json')['probes']}
  self.data=Path(data or OUT/'review/responses');self.lock=threading.RLock();self.sessions={};self.assets={};self.downloads={}
  super().__init__(address,Handler)
 def folder(self,person,role,code):
  if person not in ('A','B','C') or role not in CHOICES or code not in (self.probes if role=='physics' else self.tasks):raise ValueError('Invalid review identity')
  return self.data/self.catalog['version'][:16]/person/role/code
 def task(self,role,code):return self.tasks[self.probes[code]['reviewCode']] if role=='physics' else self.tasks[code]
 def arena(self,person,role,code):
  folder=self.folder(person,role,code);key=(person,role,code)
  if key not in self.sessions:
   task=self.task(role,code);s=Session.open(task['id'],folder/'execution','human:'+person);s.autosave=False
   a=ToolArena(s,Offline(),s.cap);a.spectator_frame=lambda *args,**kw:None
   saved=folder/'tools.private.json'
   if saved.exists():
    for call in read(saved)['calls']:a.step(call['modelOutputRaw'])
   self.sessions[key]=a
  return self.sessions[key]
 def asset(self,a,image,role,**kw):
  item=a.image(image,role,**kw);self.assets[item['sha256']]=ARENA/item['url'].lstrip('/')
  return item
 def exposed(self,person,code):
  base=self.data/self.catalog['version'][:16]/person
  if (base/'gt'/code/'viewed.json').exists():return True
  return any((base/'physics'/p['code']/'viewed.json').exists() for p in self.probes.values() if p['reviewCode']==code)
 def public(self,person,role,code,view='isometric'):
  if view not in ('isometric','rear','top'):raise ValueError('Unknown view')
  folder=self.folder(person,role,code);task=self.task(role,code)
  if role=='blind' and self.exposed(person,code):raise ValueError('这位审查者已经看过答案或拆装提示。请换未看过的人做盲操作；已有答案不会删除。')
  a=self.arena(person,role,code);saved=folder/'answer.json'
  result=dict(code=code,role=role,person=person,title=task['title'],answer=read(saved) if saved.exists() else None,
      choices=CHOICES[role],images=[],version=self.catalog['version'],responseFormat='click-only')
  if role=='blind':
   request=a.request();result.update(observation=request[2],images=request[3],finished=a.session.done)
   for im in result['images']:self.assets[im['sha256']]=ARENA/im['url'].lstrip('/')
  else:
   write(folder/'viewed.json',dict(viewedAt=time.time(),caseId=task['id']))
   if role=='gt':
    reference=deepcopy(a.session.ep.case.get('referenceActions',[]));state=deepcopy(a.session.initial)
    result['images']=[self.asset(a,a.render(state,view),'当前'),self.asset(a,a.render(a.session.goal,view),'唯一目标')]
    # Replay on a separate session so looking at GT never contaminates a blind run.
    s=Session.open(task['id'],folder/'reference','scripted:gt-display');s.autosave=False
    for i,action in enumerate(reference):
     s.submit(internal_action(s.ep,action))
     label=f'{i+1} '+('拆下' if action['type']=='detach' else '安装')+' '+getattr(s.ep,'actor_alias',{}).get(action['actor'],action['actor'])
     result['images'].append(self.asset(a,a.render(s.ep.state,view),label))
    result['referenceNotice']='参考步骤是一条合法路线，不要求唯一顺序，也不承诺最短。'
   else:
    p=self.probes[code];moving=p['action']['actor'];result['action']='拆下' if p['action']['type']=='detach' else '安装'
    result['partId']=a.sensors.aliases[moving]
    for view in ('isometric','rear','top'):
     for name,state in [('之前',p['state']),('假设之后',p['proposed'])]:result['images'].append(self.asset(a,a.render(state,view),view+' '+name))
    key=p['state'][moving] if p['action']['type']=='detach' else p['action']['candidate']
    im=a.sensors.renderer.rgb({moving:key},only=moving,frame_keys=[key],fixtures=False,size=(400,300),supersample=1)[0]
    result['images'].append(self.asset(a,im,'只判断移动这一块'))
    result['referenceNotice']='只判断单块的直线拆装。允许夹具托住；不判断重力、摩擦或卡扣力。此处不显示引擎结论。'
    from bench_design.review_server import Server as LegacyReview
    result['geometryDownload']=LegacyReview.physics_package(self,p)
  return result
 def submit(self,body):
  person,role,code=(body[k] for k in ('person','role','code'));folder=self.folder(person,role,code)
  if body.get('version')!=self.catalog['version']:raise ValueError('题目版本已变化，请刷新页面')
  if body.get('choice') not in CHOICES[role]:raise ValueError('请选择一个判断')
  if role=='blind' and self.exposed(person,code):raise ValueError('看过答案，不能记为盲操作')
  a=self.arena(person,role,code);value=dict(person=person,role=role,code=code,choice=body['choice'],version=self.catalog['version'],submittedAt=time.time())
  if role=='blind':value.update(actualCompleted=bool(a.session.result()['stateMetrics']['success']),actions=len(a.calls),modelInputProtocol=a.public_request()['protocol'])
  if role=='physics':
   method=body.get('method','images')
   if method not in ('images','third-party-software','physical-parts'):raise ValueError('Invalid method')
   value['method']=method
  if (folder/'answer.json').exists():write(folder/'history'/f'{time.time_ns()}.json',read(folder/'answer.json'))
  write(folder/'answer.json',value);return value
 def summary(self):
  answers=[read(p) for p in (self.data/self.catalog['version'][:16]).glob('*/*/*/answer.json')]
  return dict(version=self.catalog['version'],roles={r:[x for x in answers if x['role']==r] for r in CHOICES},
      humanValidatedWholeDataset=False,sampleOnly=True,
      blindCompleted=sum(x['role']=='blind' and x.get('actualCompleted') and x['choice']=='independent' for x in answers))

class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def send(self,value,status=200,kind='application/json'):
  data=value if isinstance(value,bytes) else json.dumps(value,ensure_ascii=False).encode()
  self.send_response(status);self.send_header('Content-Type',kind+'; charset=utf-8');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
 def do_GET(self):
  try:
   parsed=urlparse(self.path);q={k:v[0] for k,v in parse_qs(parsed.query).items()}
   with self.server.lock:
    if parsed.path=='/':return self.send(Path(__file__).with_name('review.html').read_bytes(),kind='text/html')
    if parsed.path=='/api/tasks':
     role=q.get('role','gt');rows=self.server.probes.values() if role=='physics' else self.server.tasks.values()
     return self.send([dict(code=r['code'],title=self.server.task(role,r['code'])['title']) for r in rows])
    if parsed.path=='/api/open':return self.send(self.server.public(q['person'],q['role'],q['code'],q.get('view','isometric')))
    if parsed.path=='/api/summary':return self.send(self.server.summary())
    if re.fullmatch(r'/assets/[a-f0-9]{64}\.png',parsed.path):
     key=Path(parsed.path).stem
     return self.send(self.server.assets[key].read_bytes(),kind='image/png')
    if re.fullmatch(r'/downloads/[a-f0-9]{64}\.zip',parsed.path):return self.send(self.server.downloads[Path(parsed.path).stem].read_bytes(),kind='application/zip')
    self.send(dict(error='not found'),404)
  except (ValueError,KeyError) as exc:self.send(dict(error=str(exc)),400)
 def do_POST(self):
  try:
   length=int(self.headers.get('Content-Length',0))
   if not 0<length<16384:raise ValueError('Invalid request size')
   body=json.loads(self.rfile.read(length));path=urlparse(self.path).path
   with self.server.lock:
    if path=='/api/submit':return self.send(self.server.submit(body))
    if path=='/api/action':
     if body.get('role')!='blind':raise ValueError('Only blind operation uses tools')
     person,code=body['person'],body['code']
     if self.server.exposed(person,code):raise ValueError('Already exposed to an answer')
     a=self.server.arena(person,'blind',code);a.step(json.dumps(body['action']))
     write(self.server.folder(person,'blind',code)/'tools.private.json',dict(calls=a.calls))
     return self.send(self.server.public(person,'blind',code))
    self.send(dict(error='not found'),404)
  except (ValueError,KeyError) as exc:self.send(dict(error=str(exc)),400)

def main():
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8820);p.add_argument('--data',type=Path);args=p.parse_args()
 server=Server(('127.0.0.1',args.port),args.data);print(f'http://127.0.0.1:{args.port}/?person=A&role=gt',flush=True);server.serve_forever()

if __name__=='__main__':main()
