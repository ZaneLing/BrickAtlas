"""Local, image-first human run of the same six-piece visual car control."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import re
import secrets
import sys
import threading

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
sys.path.insert(0,str(HERE.parent/'eval'))
from dynamic_v5.episode import DynamicEpisode, load_case
from dynamic_v5.vision import DynamicVisionRenderer
from vision import images

ROOT=HERE.parents[2]
OUT=ROOT/'deliverables/brickplan-dynamic-v5/human-car-build'
CASE='obj-city-car--t3--control'
MAX_STEPS=40

PAGE='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>小汽车 · 从零拼装</title>
<style>body{font:16px/1.5 -apple-system,BlinkMacSystemFont,sans-serif;max-width:1500px;margin:auto;padding:18px;background:#f3f6f8;color:#182736}h1{margin:0 0 8px}.hint{background:#e4f0f5;padding:12px;border-radius:8px}.grid{display:grid;grid-template-columns:2fr 1fr;gap:12px}.panel,.controls{background:white;border:1px solid #c8d2da;border-radius:8px;padding:12px;margin:12px 0}.panel img{width:100%;border:1px solid #d4dade}.panel b{display:block;margin-bottom:5px}.controls{position:sticky;top:0;z-index:2}.parts{display:flex;gap:12px;align-items:start;flex-wrap:wrap}.parts .panel:first-child{flex:0 0 320px}.parts .panel:last-child{flex:1 1 850px}.parts #inventory{width:320px;max-width:100%}.catalog{width:100%;max-width:100%;height:auto;cursor:crosshair;border:2px solid #3d8c9b}button,select{font-size:16px;padding:8px;margin:4px;cursor:pointer}.primary{background:#176384;color:white;border:0;border-radius:5px}#message{font-weight:700}.failed{color:#a32b1d}.ok{color:#176132}@media(max-width:850px){.grid{grid-template-columns:1fr}}</style>
<h1>小汽车：从空底板拼到目标</h1>
<p class="hint">这是给模型的同一道<b>无干扰小汽车题</b>。每次只装一块、拆一块或查看一块。看当前图、目标图和零件卡片；零件卡片里也有用不上的备选件。先选零件，点“看它能放哪里”，再点候选图片里的位置即可尝试安装。蓝色轮廓只标出你选的零件，<b>不表示那个位置正确或现在能装</b>。装好后点“我拼好了”。最多 40 次操作。</p>
<div class="controls"><span id="counter">准备开始</span><span id="message"></span><br><select id="part" aria-label="选择零件"></select><button onclick="inspect()">看它能放哪里</button><button onclick="detach()">拆下所选零件</button><button class="primary" onclick="finish()">我拼好了</button><button onclick="start()">重新开始</button></div>
<div class="grid"><div class="panel"><b>左：上一步之前　→　右：现在 · 斜视</b><img id="pairIso" alt="动作前和当前斜视"></div><div class="panel"><b>最终目标 · 斜视</b><img id="targetIso" alt="目标斜视"></div><div class="panel"><b>左：上一步之前　→　右：现在 · 俯视</b><img id="pairTop" alt="动作前和当前俯视"></div><div class="panel"><b>最终目标 · 俯视</b><img id="targetTop" alt="目标俯视"></div></div>
<div class="parts"><div class="panel"><b>零件卡片</b><img id="inventory" alt="零件卡片"></div><div class="panel"><b>所选零件的候选位置：点图片中的一张卡片尝试安装</b><div id="catalogHelp">先点“看它能放哪里”。</div><img id="catalog" class="catalog" hidden alt="候选安装位置"></div></div>
<script>
let session='',steps=0,catalogPart='',catalogPage=1;
function img(records,role,view){return records.find(r=>r.role===role && (!view || r.view===view))?.file || ''}
function show(data){
 session=data.session;steps=data.steps;
 document.getElementById('counter').textContent='已操作 '+steps+' / 40 次';
 const records=data.images;
 for(const [id,role,view] of [['pairIso','temporal-pair','isometric'],['pairTop','temporal-pair','top'],['targetIso','target','isometric'],['targetTop','target','top'],['inventory','inventory',null]]){
   document.getElementById(id).src='/'+img(records,role,view);
 }
 const catalog=records.find(r=>r.role==='candidate-catalog');
 const el=document.getElementById('catalog');
 if(catalog){el.hidden=false;el.src='/'+catalog.file;catalogPart=data.inspectedPart;catalogPage=catalog.page;document.getElementById('catalogHelp').textContent='当前查看 '+catalogPart+'；点击图片中的一张候选卡片尝试安装。';}
 else{el.hidden=true;el.removeAttribute('src');catalogPart='';document.getElementById('catalogHelp').textContent='先点“看它能放哪里”。';}
 if(data.feedback){const msg=document.getElementById('message');msg.textContent=' · '+data.feedback.code+(data.feedback.blockers?.length?'（挡住：'+data.feedback.blockers.join('、')+'）':'');msg.className=['OK','OBSERVED','SUCCESS'].includes(data.feedback.code)?'ok':'failed';}
 if(data.finished){document.querySelectorAll('.controls button:not(:last-child),#part').forEach(e=>e.disabled=true);document.getElementById('message').textContent=data.success?' · 拼装成功！':' · 尚未拼好；请点“重新开始”再试。';}
 else document.querySelectorAll('.controls button,#part').forEach(e=>e.disabled=false);
}
async function start(){
 const r=await fetch('/api/start',{method:'POST'}),d=await r.json();
 if(!r.ok){alert(d.message||'开始失败');return}
 const select=document.getElementById('part');select.innerHTML='';
 for(const h of d.handles){const o=document.createElement('option');o.value=h.id;o.textContent=h.id;select.append(o)}
 document.getElementById('message').textContent='';show(d);
}
async function step(action){
 if(!session)return;
 const r=await fetch('/api/step/'+session,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action})}),d=await r.json();
 if(!r.ok){alert(d.message||'操作失败');return}show(d);
}
function inspect(){step({type:'inspect',partId:document.getElementById('part').value})}
function detach(){step({type:'detach',partId:document.getElementById('part').value})}
function finish(){step({type:'finish'})}
document.getElementById('catalog').addEventListener('click',e=>{
 if(!catalogPart)return;
 const box=e.currentTarget.getBoundingClientRect();
 const x=Math.min(.999999,Math.max(0,(e.clientX-box.left)/box.width)),y=Math.min(.999999,Math.max(0,(e.clientY-box.top)/box.height));
 step({type:'attach',partId:catalogPart,catalogPage,catalogPoint:[x,y]});
});
start();
</script></html>'''

class Server(ThreadingHTTPServer):
    def __init__(self,address):
        OUT.mkdir(parents=True,exist_ok=True)
        self.sessions={}
        self.lock=threading.Lock()
        super().__init__(address,Handler)

class Handler(BaseHTTPRequestHandler):
    server:Server
    def send(self,data,kind='application/json',status=200):
        if isinstance(data,dict):data=json.dumps(data,ensure_ascii=False).encode()
        elif isinstance(data,str):data=data.encode()
        self.send_response(status);self.send_header('Content-Type',kind+'; charset=utf-8')
        self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store')
        self.end_headers();self.wfile.write(data)
    def do_GET(self):
        if self.path=='/':return self.send(PAGE,'text/html')
        if self.path=='/health':return self.send({'ok':True})
        m=re.fullmatch(r'/images/([0-9a-f]{64}\.png)',self.path)
        if m:
            path=OUT/'images'/m.group(1)
            if path.is_file():return self.send(path.read_bytes(),'image/png')
        self.send({'message':'地址无效'},status=404)
    def body(self):
        size=int(self.headers.get('Content-Length','0'))
        if not 0<size<5000:raise ValueError('请求大小无效')
        return json.loads(self.rfile.read(size))
    def view(self,s,feedback=None):
        ep=s['episode'];renderer=s['renderer']
        records=images(ep,renderer,OUT,extra=s['extra'],views=('isometric','top'),
                       previous_state=s['previous'],paired_layout=True)
        result=dict(session=s['id'],steps=len(ep.records),images=records,
                    feedback=feedback,finished=ep.finished,success=ep.success)
        if s['extra'] and 'partId' in s['extra']:result['inspectedPart']=s['extra']['partId']
        return result
    def do_POST(self):
        try:
            if self.path=='/api/start':
                cert,case=load_case(CASE);ep=DynamicEpisode(cert,case,seed=41)
                renderer=DynamicVisionRenderer(ep.cert,ep.runtime);renderer.catalog_in_context=True
                ep.vision_renderer=renderer
                sid=secrets.token_urlsafe(18)
                s=dict(id=sid,episode=ep,renderer=renderer,previous=None,extra=None)
                with self.server.lock:self.server.sessions[sid]=s
                return self.send({**self.view(s),'handles':ep.observe()['actionHandles']})
            m=re.fullmatch(r'/api/step/([A-Za-z0-9_-]+)',self.path)
            if not m:raise ValueError('地址无效')
            data=self.body();action=data.get('action')
            if not isinstance(action,dict):raise ValueError('动作无效')
            with self.server.lock:
                s=self.server.sessions.get(m.group(1))
                if not s:raise ValueError('回合不存在，请重新开始')
                ep=s['episode']
                if ep.finished or len(ep.records)>=MAX_STEPS:raise ValueError('本回合已结束，请重新开始')
                s['previous']=ep.assignments();feedback=ep.step(action)
                s['extra']=({'partId':feedback['partId']} if 'partId' in feedback else action) if action.get('type')=='inspect' and feedback['code']=='OBSERVED' else None
                result=self.view(s,feedback)
                path=OUT/'runs'/f"{s['id']}.json";path.parent.mkdir(exist_ok=True)
                path.write_text(json.dumps(ep.export(),ensure_ascii=False,indent=2)+'\n')
            return self.send(result)
        except (ValueError,KeyError,TypeError,json.JSONDecodeError) as error:
            return self.send({'message':str(error)},status=400)

if __name__=='__main__':
    server=Server(('127.0.0.1',8766))
    print('Human car build: http://127.0.0.1:8766',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
