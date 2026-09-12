"""Identical public inputs for every checkpoint; unquantized MLX greedy decoding."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import numpy as np
from mlx_vlm import load, generate
from mlx_vlm.utils import prepare_inputs

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--model", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()
model_path = Path(args.model)
out = Path(args.output)
model, processor = load(str(model_path))
processor.chat_template = json.loads((model_path / "chat_template.json").read_text())["chat_template"]
processor.image_processor.do_image_splitting = False
processor.image_processor.size = {"longest_edge": 512}
source = ROOT / "suite/artifacts/study/inputs"
rows = [json.loads(line) for line in (source / "public.jsonl").read_text().splitlines()]
predictions = []
for row in rows:
    messages = [
        {"role": "system", "content": [{"type": "text", "text": row["system"]}]},
        {"role": "user", "content": [{"type": "image"} for _ in row["images"]] +
         [{"type": "text", "text": json.dumps(row["input"], separators=(",", ":"))}]},
    ]
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    images = [str(source / path) for path in row["images"]]
    prepared = prepare_inputs(processor, images=images or None, prompts=prompt, image_token_index=model.config.image_token_id)
    input_hash = hashlib.sha256(np.array(prepared["input_ids"]).astype(np.int64).tobytes()).hexdigest()
    start = time.perf_counter()
    result = generate(model, processor, prompt, image=images or None, max_tokens=2200, temperature=0.0, verbose=False)
    predictions.append({"caseId": row["caseId"], "raw": result.text, "input_tokens": result.prompt_tokens,
                        "output_tokens": result.generation_tokens, "seconds": time.perf_counter()-start,
                        "images": len(images), "input_token_sha256": input_hash, "backend": "mlx-vlm-0.7.0-unquantized"})
    tmp = out / "predictions.tmp"
    tmp.write_text(json.dumps(predictions, indent=2) + "\n")
    tmp.replace(out / "predictions.json")
    if len(predictions) % 20 == 0:
        print(json.dumps({"predictions": len(predictions), "total": len(rows)}), flush=True)
print(json.dumps({"inference": "complete", "cases": len(predictions)}), flush=True)
