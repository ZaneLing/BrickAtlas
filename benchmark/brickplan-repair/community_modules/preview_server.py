"""Loopback-only public preview. Never serve private certificates or run logs."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import mimetypes
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[3] / "deliverables/brickplan-community-modules"


class Preview(BaseHTTPRequestHandler):
    def do_GET(self):
        relative = unquote(urlsplit(self.path).path).lstrip("/") or "index.html"
        path = (ROOT / relative).resolve()
        parts = Path(relative).parts
        allowed = (relative in ("index.html", "data.js", "MODEL-CASE-CATALOG.zh-CN.md", "README.zh-CN.md", "INPUT-OUTPUT.zh-CN.md")
                   or (len(parts) == 3 and parts[1] == "images" and parts[2].endswith(".png"))
                   or (len(parts) == 2 and parts[1] == "original.mpd"))
        if not allowed or ROOT.resolve() not in path.parents or not path.is_file():
            self.send_error(404)
            return
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(path.name)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print("Community module preview: http://127.0.0.1:8768", flush=True)
    ThreadingHTTPServer(("127.0.0.1", 8768), Preview).serve_forever()
