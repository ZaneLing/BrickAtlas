"""Recover a selected official original with validated HTTP byte ranges."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email.parser import BytesParser
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlparse
from source_state import source_state

ROOT = Path(__file__).resolve().parents[3]
STATE = source_state(ROOT)
OUT = Path(os.environ.get("SOURCE_INTAKE_OUTPUT", "/tmp/brickplan-v23-work/source-intake"))
EXPECTED = "3518c3357872225b0425ee6bcd2a0aa8350aca0791d7b83dd056d5baec081f0b"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def response_headers(path):
    blocks = re.split(rb"\r?\n\r?\n", path.read_bytes())
    block = next(block for block in reversed(blocks) if block.startswith(b"HTTP/"))
    status, headers = block.split(b"\n", 1)
    return int(status.split()[1]), BytesParser().parsebytes(headers)


def write_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as stream:
            stream.write(data)
    except FileExistsError:
        assert path.read_bytes() == data, f"Refusing overwrite: {path}"


parser = argparse.ArgumentParser()
parser.add_argument("--kit", required=True)
args = parser.parse_args()
registry_bytes = (STATE / "candidate-registry.frozen.json").read_bytes()
assert sha(registry_bytes) == EXPECTED
registry = json.loads(registry_bytes)
candidate = next(c for c in registry["candidates"] if c["kit"] == args.kit)
detail = json.loads((STATE / "details" / f"{args.kit}.json").read_text())
selected = next((m for m in detail["models"] if m["pageModelLabel"] == "Main Model"),
                sorted(detail["models"], key=lambda m: m["downloadUrl"])[0])
url = selected["downloadUrl"]
parsed = urlparse(url)
assert parsed.scheme == "https" and parsed.netloc == "library.ldraw.org"
assert parsed.path.startswith("/library/omr/")
filename = unquote(parsed.path.rsplit("/", 1)[1])
assert filename.startswith(candidate["setNumber"]) and "/" not in filename
target = ROOT / "assets-source/brickplan-v23/original" / filename
assert not target.exists(), "Existing successful original must not be downloaded again"
work = OUT / "ranges" / candidate["id"]
work.mkdir(parents=True, exist_ok=True)
head_path = work / "head.headers"
subprocess.run(["/usr/bin/curl", "-fLsSI", "--connect-timeout", "10", "--max-time", "30",
                "-D", str(head_path), "-o", os.devnull, url], check=True)
status, headers = response_headers(head_path)
assert status == 200 and headers["Accept-Ranges"] == "bytes"
size, etag = int(headers["Content-Length"]), headers["ETag"]
assert 0 < size < 32 * 1024 * 1024 and etag and not etag.startswith("W/")
chunk_size = 65536


def fetch_chunk(start):
    end = min(start + chunk_size, size) - 1
    body = work / f"{start}-{end}.body"
    meta_path = work / f"{start}-{end}.json"
    if body.exists() and meta_path.exists():
        meta = json.loads(meta_path.read_text())
        assert meta["etag"] == etag and meta["sha256"] == sha(body.read_bytes())
        return start, body, meta
    for attempt, timeout in enumerate((90, 150)):
        partial = work / f"{start}-{end}.attempt-{attempt}.part"
        dump = work / f"{start}-{end}.attempt-{attempt}.headers"
        process = subprocess.run(
            ["/usr/bin/curl", "-fLsS", "--connect-timeout", "10", "--max-time", str(timeout),
             "--speed-time", "30", "--speed-limit", "128", "--range", f"{start}-{end}",
             "-H", f"If-Range: {etag}", "-D", str(dump), "-o", str(partial), url],
            capture_output=True, timeout=timeout + 5)
        if process.returncode:
            print(f"RETRY {start}-{end}: {process.stderr.decode().strip()}", flush=True)
            continue
        code, response = response_headers(dump)
        assert code == 206, f"Server did not honor range: {code}"
        assert response["Content-Range"] == f"bytes {start}-{end}/{size}"
        assert response["ETag"] == etag, "Original changed during transfer"
        data = partial.read_bytes()
        assert len(data) == end - start + 1
        write_new(body, data)
        meta = {"start": start, "end": end, "total": size, "etag": etag, "sha256": sha(data),
                "url": url, "responseHeaders": str(dump), "retrievedAt": datetime.now(timezone.utc).isoformat()}
        write_new(meta_path, (json.dumps(meta, indent=2) + "\n").encode())
        print(f"CHUNK {start}-{end}/{size}", flush=True)
        return start, body, meta
    raise RuntimeError(f"Range transfer failed: {start}-{end}")


with ThreadPoolExecutor(max_workers=4) as pool:
    chunks = sorted(pool.map(fetch_chunk, range(0, size, chunk_size)))
data = b"".join(body.read_bytes() for _, body, _ in chunks)
assert len(data) == size
assert re.search(rb"(?m)^0 FILE " + args.kit.encode() + rb"[ ._-]", data)
assert data.decode("utf-8").encode("utf-8") == data
write_new(target, data)
record = {"candidateRegistrySha256": EXPECTED, "id": candidate["id"], "url": url,
          "path": str(target.relative_to(ROOT)), "bytes": size, "sha256": sha(data), "etag": etag,
          "method": "Exact contiguous byte ranges with strong ETag and Content-Range validation",
          "chunks": [meta for _, _, meta in chunks]}
write_new(work / "download-proof.json", (json.dumps(record, indent=2) + "\n").encode())
print(f"COMPLETE {candidate['id']} bytes={size} sha256={sha(data)}", flush=True)
