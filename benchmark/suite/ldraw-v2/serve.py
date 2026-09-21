#!/usr/bin/env python3
"""Serve the built v2 pages plus unchanged repository public assets."""
import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[3]


class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        suffix = unquote(urlsplit(path).path).lstrip("/") or "ldraw-v2.html"
        for root in [ROOT / "dist-ldraw-v2", ROOT / "public"]:
            candidate = (root / suffix).resolve()
            if candidate.is_relative_to(root.resolve()) and candidate.is_file():
                return str(candidate)
        return str(ROOT / "dist-ldraw-v2/.not-found")

    def list_directory(self, path):
        self.send_error(404)

    def log_message(self, format, *args):
        if str(args[1]) != "200":
            super().log_message(format, *args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=5175)
    args = parser.parse_args()
    print(f"http://127.0.0.1:{args.port}/ldraw-v2.html", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
