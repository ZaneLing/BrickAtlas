"""Local read-only arena viewer. It cannot trigger model spending or actions."""
import argparse
import gzip
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import threading
from urllib.parse import urlparse, parse_qs
from dynamic_arena import OUT

PREVIEW_LOCK = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/api/preview': return self.send_error(404)
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0 < length <= 4096: return self.send_error(400)
            payload=json.loads(self.rfile.read(length))
            if set(payload) != {'caseId','normal'} or type(payload['normal']) is not bool: return self.send_error(400)
            from dynamic_arena.run import preview
            with PREVIEW_LOCK: runid=preview(payload['caseId'],payload['normal'])
            self.send(json.dumps(dict(runId=runid)).encode(),'application/json')
        except (KeyError,ValueError,StopIteration,TypeError): self.send_error(400,'Unknown dynamic task')

    def do_GET(self):
        parsed = urlparse(self.path)
        try:
            if parsed.path in ('/', '/arena'):
                return self.send(Path(__file__).with_name('arena.html').read_bytes(), 'text/html; charset=utf-8')
            if parsed.path == '/library':
                return self.send(Path(__file__).with_name('library.html').read_bytes(), 'text/html; charset=utf-8')
            if parsed.path in ('/api/catalogue','/api/sources'):
                name='catalogue.json' if parsed.path=='/api/catalogue' else 'source-library.json'
                return self.send((OUT/name).read_bytes(),'application/json')
            if parsed.path.startswith('/source-thumbnail/'):
                number=parsed.path.removeprefix('/source-thumbnail/')
                if not re.fullmatch(r'\d+-\d+',number): return self.send_error(400)
                from dynamic_arena import ROOT
                rows=json.loads((OUT/'source-library.json').read_text())['models']
                row=next((r for r in rows if r['setNumber']==number),None)
                if not row or not row.get('thumbnail'): return self.send_error(404)
                return self.send((ROOT/row['thumbnail']).read_bytes(),'image/jpeg')
            if parsed.path == '/api/state':
                runid = parse_qs(parsed.query).get('run', [None])[0]
                if not runid:
                    runid = json.loads((OUT / 'latest.json').read_text())['runId']
                if not re.fullmatch(r'[a-zA-Z0-9_-]+', runid):
                    return self.send_error(400)
                return self.send((OUT / 'runs' / runid / 'spectator.json').read_bytes(), 'application/json')
            if parsed.path in ('/api/log', '/api/raw-request', '/api/raw-response'):
                query = parse_qs(parsed.query)
                runid = query.get('run', [''])[0]
                if not re.fullmatch(r'[a-zA-Z0-9_-]+', runid):
                    return self.send_error(400)
                directory = OUT / 'runs' / runid
                if parsed.path == '/api/log':
                    return self.send((directory / 'log.json').read_bytes(), 'application/json')
                number = query.get('call', [''])[0]
                if not number.isdecimal() or not 1 <= int(number) <= 10000:
                    return self.send_error(400)
                ledger_name = ('unified-ledger.private.json' if runid.startswith('arena-') else 'normal-pilot-ledger.private.json' if
                    runid.startswith(('normal-', 'incident-')) else 'api-ledger.private.json')
                ledger = json.loads((OUT / ledger_name).read_text())
                charges = [c for c in ledger['charges'] if c['run'] == runid]
                if int(number) > len(charges):
                    return self.send_error(404)
                if parsed.path == '/api/raw-response':
                    if charges[int(number)-1]['status'] != 'settled':
                        return self.send_error(404, 'Provider returned no recorded response')
                    return self.send((directory / 'api' / (charges[int(number)-1]['id'] + '.private.json')).read_bytes(),
                                     'application/json')
                data = gzip.decompress((directory / 'api' / (charges[int(number)-1]['id'] + '.request.json.gz')).read_bytes())
                return self.send(data, 'application/json')
            if parsed.path == '/api/runs':
                runs = []
                for p in sorted((OUT / 'runs').glob('*/spectator.json'), reverse=True):
                    r = json.loads(p.read_text())
                    if r['runId'].startswith('preview-'): continue
                    runs.append({k: r.get(k) for k in ('runId', 'model', 'phase', 'startedAt','title','condition','evidenceType','caseId')})
                return self.send(json.dumps(runs).encode(), 'application/json')
            if re.fullmatch(r'/assets/[0-9a-f]{64}\.png', parsed.path):
                return self.send((OUT / parsed.path[1:]).read_bytes(), 'image/png')
            if parsed.path == '/health':
                return self.send(b'{"ok":true,"readOnly":true}', 'application/json')
            self.send_error(404)
        except FileNotFoundError:
            self.send_error(404, 'Arena has not been prepared')

    def send(self, data, mime):
        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8810)
    args = parser.parse_args()
    print(f'Dynamic arena: http://127.0.0.1:{args.port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()


if __name__ == '__main__':
    main()
