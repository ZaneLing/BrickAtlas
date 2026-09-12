"""Download only the pinned public SmolVLM checkpoint, not gated assets."""
import hashlib
import json
from pathlib import Path
from huggingface_hub import snapshot_download

ROOT = Path(__file__).resolve().parents[2]
MODEL = "HuggingFaceTB/SmolVLM-256M-Instruct"
REVISION = "7e3e67edbbed1bf9888184d9df282b700a323964"
destination = ROOT / ".runtime/models/smolvlm-256m"
snapshot_download(repo_id=MODEL, revision=REVISION, local_dir=destination,
                  allow_patterns=["*.json", "*.txt", "*.safetensors", "*.jinja", "README.md", "LICENSE"])
files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in destination.iterdir() if p.is_file()}
(destination / "brickatlas-download.json").write_text(json.dumps({
    "model": MODEL, "revision": REVISION, "license": "Apache-2.0 per upstream model card",
    "gated": False, "files": files,
}, indent=2) + "\n")
print(json.dumps({"model": MODEL, "revision": REVISION, "files": len(files)}), flush=True)
