"""Audit prompt/answer boundaries and reference output lengths without running a model."""
import gzip
import json
from pathlib import Path
from PIL import Image
from transformers import AutoProcessor

ROOT = Path(__file__).resolve().parents[2]
base = ROOT / ".runtime/models/smolvlm-256m"
processor = AutoProcessor.from_pretrained(base, local_files_only=True)
processor.image_processor.do_image_splitting = False
processor.image_processor.size = {"longest_edge": 512}
study = ROOT / "suite/artifacts/study"
rows = []
for split in ["train", "validation"]:
    directory = study / "training-data"
    for line in gzip.decompress((directory / f"{split}.jsonl.gz").read_bytes()).decode().splitlines():
        row = json.loads(line)
        images = [Image.open(directory / path).convert("RGB") for path in row["images"]]
        messages = [
            {"role": "system", "content": [{"type": "text", "text": row["system"]}]},
            {"role": "user", "content": [{"type": "image"} for _ in images] +
             [{"type": "text", "text": json.dumps(row["input"], separators=(",", ":"))}]},
        ]
        prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
        answer = json.dumps(row["answer"], separators=(",", ":")) + processor.tokenizer.eos_token
        prefix = processor(text=prompt, images=images or None, return_tensors="pt")["input_ids"][0]
        full = processor(text=prompt + answer, images=images or None, return_tensors="pt")["input_ids"][0]
        assert full[:len(prefix)].equal(prefix), row["caseId"]
        assert len(full) <= 8192 and len(prefix) > 0 and len(full) > len(prefix)
        assert full[-1].item() == processor.tokenizer.eos_token_id
        rows.append({"caseId": row["caseId"], "split": split, "kind": row["kind"],
                     "promptTokens": len(prefix), "answerTokens": len(full) - len(prefix),
                     "fullTokens": len(full), "referenceExceedsOutputCap": len(full) - len(prefix) > 2200})
result = {"rows": rows, "cases": len(rows), "prefixTokensUnchanged": True, "promptLabelsMasked": True,
          "maximumFullTokens": max(r["fullTokens"] for r in rows),
          "referenceExceedsOutputCap": sum(r["referenceExceedsOutputCap"] for r in rows),
          "scope": "Train/validation oracle serialization lengths, not a lower bound for all correct equivalent answers. No inference performed."}
(study / "training-token-audit.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "rows"}), flush=True)
