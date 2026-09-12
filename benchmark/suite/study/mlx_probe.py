"""Read-only backend probe; never included as a scored benchmark result."""
import json
from pathlib import Path
import time
import numpy as np
from mlx_vlm import load, generate
from mlx_vlm.utils import prepare_inputs

ROOT = Path(__file__).resolve().parents[2]
base = ROOT / ".runtime/models/smolvlm-256m"
model, processor = load(str(base))
processor.chat_template = json.loads((base / "chat_template.json").read_text())["chat_template"]
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
images = [str(inputs / path) for path in row["images"]]
batch = prepare_inputs(processor, images=images, prompts=prompt, image_token_index=model.config.image_token_id)
np.savez(ROOT / ".runtime/vlm-training/mlx-inputs.npz", **{k: np.array(v) for k, v in batch.items() if v is not None})
start = time.perf_counter()
result = generate(model, processor, prompt, image=images, max_tokens=100, temperature=0.0, verbose=False)
out = ROOT / ".runtime/vlm-training/mlx-probe.json"
out.write_text(json.dumps({
    "caseId": row["caseId"], "seconds": time.perf_counter()-start,
    "text": result.text, "prompt_tokens": result.prompt_tokens, "generation_tokens": result.generation_tokens,
    "input_ids": np.array(batch["input_ids"]).tolist(),
    "note": "Backend speed/input-equivalence probe only, not a benchmark result.",
}, indent=2) + "\n")
print(out.read_text()[:1000], flush=True)
