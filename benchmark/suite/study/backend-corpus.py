"""Record preprocessing digests for every inference case, then compare backends."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--backend", choices=["torch", "mlx"], required=True)
args = parser.parse_args()
base = ROOT / ".runtime/models/smolvlm-256m"
if args.backend == "torch":
    from transformers import AutoProcessor
    processor = AutoProcessor.from_pretrained(base, local_files_only=True)
else:
    from mlx_vlm.models.idefics3.processing_idefics3 import Idefics3Processor
    from mlx_vlm.utils import prepare_inputs
    processor = Idefics3Processor.from_pretrained(base)
    processor.chat_template = json.loads((base / "chat_template.json").read_text())["chat_template"]
processor.image_processor.do_image_splitting = False
processor.image_processor.size = {"longest_edge": 512}
root = ROOT / "suite/artifacts/study/inputs"
checks = []
for line in (root / "public.jsonl").read_text().splitlines():
    row = json.loads(line)
    messages = [
        {"role": "system", "content": [{"type": "text", "text": row["system"]}]},
        {"role": "user", "content": [{"type": "image"} for _ in row["images"]] +
         [{"type": "text", "text": json.dumps(row["input"], separators=(",", ":"))}]},
    ]
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    images = [Image.open(root / path).convert("RGB") for path in row["images"]]
    if args.backend == "torch":
        batch = processor(text=prompt, images=images or None, return_tensors="pt")
        arrays = {k: value.numpy() for k, value in batch.items()}
    else:
        batch = prepare_inputs(processor, images=images or None, prompts=prompt, image_token_index=49190)
        arrays = {k: np.array(v) for k, v in batch.items() if v is not None}
    checks.append({"caseId": row["caseId"], "inputs": {
        k: {"shape": list(v.shape), "sha256": hashlib.sha256(v.astype(np.float64).tobytes()).hexdigest()}
        for k, v in arrays.items()
    }})
output = ROOT / f".runtime/vlm-training/{args.backend}-corpus.json"
output.write_text(json.dumps(checks, indent=2) + "\n")
other = ROOT / ".runtime/vlm-training/torch-corpus.json"
if args.backend == "mlx" and other.exists():
    expected = json.loads(other.read_text())
    assert len(checks) == len(expected)
    for a, b in zip(expected, checks):
        assert a["caseId"] == b["caseId"]
        for key, value in a["inputs"].items():
            assert value == b["inputs"][key], (a["caseId"], key)
    report = {"cases": len(checks), "allTokenAndPixelDigestsMatch": True,
              "scope": "Preprocessing equality only; kernel precision can change decoding."}
    (ROOT / "suite/artifacts/study/backend-corpus-check.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"backend": args.backend, "cases": len(checks)}), flush=True)
