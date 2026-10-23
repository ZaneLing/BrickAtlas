"""Serve two explicitly public output folders on loopback; never private cases."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
import argparse

OUT = Path(__file__).resolve().parents[2] / 'deliverables/brickplan-public-preview'
OBJECTS = OUT.parent / 'brickplan-recognizable-models/public'


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(OUT), **kwargs)

    def public_path(self):
        name = unquote(urlparse(self.path).path).lstrip('/')
        if name == 'objects' or name.startswith('objects/'):
            root=OBJECTS
            relative=name.removeprefix('objects').lstrip('/') or 'index.html'
        else:
            root=OUT
            relative=name or 'index.html'
        path=(root / relative).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            return None
        if path.suffix not in ('.html', '.css', '.js', '.json', '.jsonl', '.png', '.jpg', '.webp', '.md'):
            return None
        return path

    def translate_path(self, path):
        # The default handler must use the exact same authorized resolved file.
        return str(self.public_path() or OUT / '__unavailable__')

    def permitted(self):
        if self.public_path() is None:
            self.send_error(404)
            return False
        return True

    def do_GET(self):
        if urlparse(self.path).path == '/objects':
            self.send_response(301)
            self.send_header('Location', '/objects/')
            self.end_headers()
            return
        if self.permitted(): super().do_GET()

    def do_HEAD(self):
        if self.permitted(): super().do_HEAD()

    def list_directory(self, path):
        self.send_error(404)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8799)
    args = parser.parse_args()
    print(f'http://127.0.0.1:{args.port}/', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()


if __name__ == '__main__': main()
