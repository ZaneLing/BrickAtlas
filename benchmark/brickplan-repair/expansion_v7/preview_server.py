"""Local read-only design gallery. Private certificates and runs are blocked."""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import unquote,urlparse
import argparse
from expansion_v7 import OUT


class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(OUT),**kwargs)
    def allowed(self):
        path=unquote(urlparse(self.path).path).lstrip('/') or 'index.html'
        target=(OUT/path).resolve()
        allowed=(path in ('index.html','gallery-data.js','README.zh-CN.md','MODEL-CASE-CATALOG.zh-CN.md',
                         'global-splits.csv','difficulty-all.json','evaluation-sets.json','cases.csv','HUMAN-ERROR-SCOPE.zh-CN.md',
                         'human-error-scope.json','inventory-audit/audit.json')
                 or path.startswith(('assets/','inventory-audit/assets/')) and path.endswith('.png')
                 or path=='human-error-research/README.zh-CN.md')
        if not target.is_relative_to(OUT.resolve()) or not allowed or not target.is_file():
            self.send_error(404);return False
        return True
    def do_GET(self):
        if not self.allowed():return
        super().do_GET()
    def do_HEAD(self):
        if not self.allowed():return
        super().do_HEAD()
    def list_directory(self,path):self.send_error(404)


def main():
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8797);args=p.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print(f'http://127.0.0.1:{args.port}/',flush=True);server.serve_forever()


if __name__=='__main__':main()
