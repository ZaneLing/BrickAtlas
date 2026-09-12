"""Download the pinned public base model for the existing local training recipe."""
from pathlib import Path
from huggingface_hub import snapshot_download

ROOT = Path(__file__).resolve().parents[2]
snapshot_download(
    repo_id="Qwen/Qwen3-0.6B",
    revision="c1899de289a04d12100db370d81485cdf75e47ca",
    local_dir=str(ROOT / ".runtime/models/qwen3-0.6b"),
    allow_patterns=["*.json", "*.safetensors", "*.txt", "*.jinja", "LICENSE", "README.md"],
)
