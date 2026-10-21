"""Small local/LAN server for three blinded human reviewers.

Only tokenized review pages, image assets, a completion dashboard, and the
submission endpoint are exposed. Private case answers are never served.
"""
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import html
import json
import os
import re
import secrets
import threading

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BANK=ROOT/'deliverables/brickplan-dynamic-v5'
OUT=BANK/'human-temporal-review'
CONFIG=ROOT/'benchmark/.runtime/temporal-human-review-server.json'
REVIEWERS=('reviewer-A','reviewer-B','reviewer-C')
FIELDS=('code','changed')


def atomic_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.'+secrets.token_hex(6)+'.tmp')
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    temporary.replace(path)


def tokens(path=CONFIG):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        data=json.loads(path.read_text())
    else:
        data={name:secrets.token_urlsafe(24) for name in (*REVIEWERS,'admin')}
        flags=os.O_CREAT|os.O_EXCL|os.O_WRONLY
        try:
            descriptor=os.open(path,flags,0o600)
        except FileExistsError:
            data=json.loads(path.read_text())
        else:
            with os.fdopen(descriptor,'w') as stream:
                json.dump(data,stream,indent=2)
                stream.write('\n')
    assert set(data)==set((*REVIEWERS,'admin'))
    assert len(set(data.values()))==4
    return data


class ReviewServer(ThreadingHTTPServer):
    def __init__(self,address,root=OUT,answer_key=BANK/'human-temporal-answer-key.private.json',secret_path=CONFIG):
        self.root=Path(root)
        self.answer_key=Path(answer_key)
        self.codes={r['code'] for r in json.loads(self.answer_key.read_text())['rows']}
        self.tokens=tokens(Path(secret_path))
        self.reviewer_by_token={self.tokens[name]:name for name in REVIEWERS}
        self.write_lock=threading.Lock()
        super().__init__(address,ReviewHandler)


class ReviewHandler(BaseHTTPRequestHandler):
    server: ReviewServer

    def send_bytes(self,data,content_type,status=200,cache='no-store'):
        self.send_response(status)
        self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control',cache)
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('X-Frame-Options','DENY')
        self.end_headers()
        self.wfile.write(data)

    def send_json(self,obj,status=200):
        self.send_bytes(json.dumps(obj,ensure_ascii=False).encode('utf-8'),
                        'application/json; charset=utf-8',status)

    def do_GET(self):
        path=unquote(urlsplit(self.path).path)
        if path=='/health':
            self.send_json({'ok':True,'service':'brickplan-temporal-human-review'})
            return
        if path.startswith('/r/'):
            token=path.removeprefix('/r/')
            reviewer=self.server.reviewer_by_token.get(token)
            if reviewer:
                file=self.server.root/f'{reviewer}.html'
                self.send_bytes(file.read_bytes(),'text/html; charset=utf-8')
                return
        match=re.fullmatch(r'/images/([0-9a-f]{64}\.png)',path)
        if match:
            file=self.server.root/'images'/match.group(1)
            if file.is_file():
                self.send_bytes(file.read_bytes(),'image/png',cache='public, max-age=86400')
                return
        if path.startswith('/status/') and path.removeprefix('/status/')==self.server.tokens['admin']:
            rows=[]
            for reviewer in REVIEWERS:
                file=self.server.root/'submissions'/f'{reviewer}.json'
                if file.exists():
                    data=json.loads(file.read_text())
                    state=f'已提交 · {len(data["answers"])} 题 · 第 {data["revision"]} 次 · {html.escape(data["submittedAt"])}'
                else:
                    state='尚未提交'
                rows.append(f'<li>{reviewer}: {state}</li>')
            body='<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="15">' \
                 '<title>盲审提交状态</title><h1>三位真人的提交状态</h1><ul>'+''.join(rows)+'</ul>' \
                 '<p>本页每 15 秒更新；只显示是否提交，不显示回答或答案。</p>'
            self.send_bytes(body.encode('utf-8'),'text/html; charset=utf-8')
            return
        self.send_error(404,'Not found')

    def do_POST(self):
        path=unquote(urlsplit(self.path).path)
        if not path.startswith('/api/submit/'):
            self.send_json({'ok':False,'message':'地址无效'},404)
            return
        reviewer=self.server.reviewer_by_token.get(path.removeprefix('/api/submit/'))
        if reviewer is None:
            self.send_json({'ok':False,'message':'提交链接无效'},403)
            return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 1<=size<=100_000:
                raise ValueError('提交内容大小不正确')
            payload=json.loads(self.rfile.read(size))
            if not isinstance(payload,dict) or payload.get('reviewer')!=reviewer:
                raise ValueError('审查者编号与链接不一致')
            answers=payload.get('answers')
            if not isinstance(answers,list) or len(answers)!=len(self.server.codes):
                raise ValueError('请先完成全部题目')
            codes=[];clean=[]
            for answer in answers:
                if not isinstance(answer,dict) or set(answer)!=set(FIELDS):
                    raise ValueError('答案格式不正确')
                code=answer['code'];codes.append(code)
                if not isinstance(code,str) or code not in self.server.codes:
                    raise ValueError('题目编号无效')
                if answer['changed'] not in ('yes','no','unsure'):
                    raise ValueError(f'{code} 尚未选择有／没有／看不清')
                clean.append({'code':code,'changed':answer['changed']})
            if set(codes)!=self.server.codes or len(set(codes))!=len(codes):
                raise ValueError('题目有重复或遗漏')
            with self.server.write_lock:
                directory=self.server.root/'submissions'
                latest=directory/f'{reviewer}.json'
                revision=json.loads(latest.read_text())['revision']+1 if latest.exists() else 1
                record=dict(schema='brickplan-temporal-human-submission/2',reviewer=reviewer,
                            submittedAt=datetime.now(timezone.utc).isoformat(),revision=revision,
                            answers=clean)
                atomic_json(directory/f'{reviewer}-revision-{revision:03}.json',record)
                atomic_json(latest,record)
            self.send_json({'ok':True,'revision':revision,'message':'提交成功'})
        except (ValueError,TypeError,KeyError,json.JSONDecodeError) as exc:
            self.send_json({'ok':False,'message':str(exc)},400)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',default='0.0.0.0')
    parser.add_argument('--port',type=int,default=8765)
    parser.add_argument('--link-host',default='127.0.0.1',help='Host name/IP printed in review links')
    args=parser.parse_args()
    server=ReviewServer((args.host,args.port))
    base=f'http://{args.link_host}:{server.server_port}'
    print('A:',base+'/r/'+server.tokens['reviewer-A'],flush=True)
    print('B:',base+'/r/'+server.tokens['reviewer-B'],flush=True)
    print('C:',base+'/r/'+server.tokens['reviewer-C'],flush=True)
    print('Status:',base+'/status/'+server.tokens['admin'],flush=True)
    print('Submissions:',server.root/'submissions',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__=='__main__':main()
