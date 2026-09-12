"""Compare full image/text preprocessing with the independent MLX runner."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from transformers import AutoProcessor

ROOT = Path(__file__).resolve().parents[2]
base = ROOT / ".runtime/models/smolvlm-256m"
processor = AutoProcessor.from_pretrained(base, local_files_only=True)
processor.image_processor.do_image_splitting = False
processor.image_processor.size = {"longest_edge": 512}
inputs = ROOT / "suite/artifacts/study/inputs"
row = next(json.loads(line) for line in (inputs / "public.jsonl").read_text().splitlines()
           if json.loads(line)["input"]["kind"] == "reconstruct")
messages = [
    {"role": "system", "content": [{"type": "text", "text": row["system"]}]},
    {"role": "user", "content": [{"type": "image"} for _ in row["images"]] +
     [{"type": "text", "text": json.dumps(row["input"], separators=(",", ":"))}]},
]
prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
images = [Image.open(inputs / path).convert("RGB") for path in row["images"]]
batch = processor(text=prompt, images=images, return_tensors="pt")
other = np.load(ROOT / ".runtime/vlm-training/mlx-inputs.npz")
checks = {}
for k, value in batch.items():
    a = value.numpy()
    assert k in other, (k, other.files)
    b = other[k]
    if k == "pixel_values" and a.shape != b.shape:
        raise RuntimeError("Image layout differs")
    assert a.shape == b.shape, (k, a.shape, b.shape)
    error = np.max(np.abs(a.astype(float)-b.astype(float)))
    assert error < 1e-5, (k, error)
    checks[k] = {"shape": list(a.shape), "max_absolute_difference": float(error)}
path = ROOT / "suite/artifacts/study/backend-input-check.json"
path.write_text(json.dumps({"caseId": row["caseId"], "checks": checks,
    "scope": "One four-image preprocessing probe; does not guarantee identical floating-point decoding.",
    "apiCalls": 0}, indent=2) + "\n")
print(path.read_text(), flush=True)
