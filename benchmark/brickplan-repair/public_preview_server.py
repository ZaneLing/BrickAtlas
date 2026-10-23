"""Serve only the portable public-preview folder on loopback."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
import argparse

OUT = Path(__file__).resolve().parents[2] / 'deliverables/brickplan-public-preview'


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(OUT), **kwargs)

    def permitted(self):
        name = unquote(urlparse(self.path).path).lstrip('/') or 'index.html'
        path = (OUT / name).resolve()
        if not path.is_relative_to(OUT.resolve()) or not path.is_file():
            self.send_error(404)
            return False
        if path.suffix not in ('.html', '.css', '.js', '.json', '.jsonl', '.png', '.jpg', '.webp', '.md'):
            self.send_error(404)
            return False
        return True

    def do_GET(self):
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
