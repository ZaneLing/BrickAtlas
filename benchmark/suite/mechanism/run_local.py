"""Run the local Qwen3-0.6B text-only baseline on Mechanism-1."""
from __future__ import annotations

import json
from pathlib import Path
import re
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "mechanism-v1"
MODEL = ROOT / ".runtime/models/qwen3-0.6b"
OUT = RELEASE / "results"
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "local-qwen3-0.6b.json"
PREDICTIONS = OUT / "local-qwen3-0.6b.predictions.json"

SCHEMAS = {
    "prefix-dynamics": {"validPlanId": "string", "invalidPlanFirstFailure": "integer"},
    "insertion-access": {"accessiblePathIds": ["string"]},
    "fault-recovery": {"faultJointId": "string", "actions": ["string"]},
    "inventory-substitution": {"alternativeId": "string"},
    "dynamic-robustness": {"maxSafeImpulse": "number"},
    "functional-kinematics": {"jointId": "string", "reachesTarget": "boolean"},
    "active-inspection": {"queryId": "string"},
    "multiobjective-design": {"paretoIds": ["string"]},
}


def parse_json(text):
    cleaned = text.split("</think>")[-1].strip()
    try:
        return json.loads(cleaned)
    except Exception:
        match = re.search(r"\{.*\}", cleaned, re.S)
        if not match:
            return None
        try:
            return json.loads(match.group(0))
        except Exception:
            return None


def save(rows):
    tmp = RAW.with_suffix(".tmp")
    tmp.write_text(json.dumps(rows, indent=2) + "\n")
    tmp.replace(RAW)
    PREDICTIONS.write_text(json.dumps(
        [{"id": row["id"], "answer": row["answer"]} for row in rows], indent=2
    ) + "\n")


def main():
    tasks = json.loads((RELEASE / "public.json").read_text())
    existing = json.loads(RAW.read_text()) if RAW.exists() else []
    done = {row["id"] for row in existing}
    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.float16 if device == "mps" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(MODEL, local_files_only=True, torch_dtype=dtype).to(device)
    model.eval()
    for index, task in enumerate(tasks):
        if task["id"] in done:
            continue
        public = {
            "id": task["id"], "kind": task["kind"], "capability": task["capability"],
            "question": task["question"], "input": task["input"],
            "responseSchema": SCHEMAS[task["kind"]],
        }
        messages = [
            {"role": "system", "content": "Return exactly one JSON object matching responseSchema. No markdown or explanation."},
            {"role": "user", "content": json.dumps(public)},
        ]
        try:
            prompt = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
            )
        except TypeError:
            prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        start = time.perf_counter()
        with torch.inference_mode():
            output = model.generate(**inputs, max_new_tokens=180, do_sample=False,
                                    pad_token_id=tokenizer.eos_token_id)
        generated = output[0, inputs.input_ids.shape[1]:]
        text = tokenizer.decode(generated, skip_special_tokens=True)
        existing.append({
            "id": task["id"], "model": "Qwen3-0.6B-local-text", "raw": text,
            "answer": parse_json(text), "inputTokens": int(inputs.input_ids.shape[1]),
            "outputTokens": int(generated.shape[0]), "seconds": time.perf_counter() - start,
        })
        save(existing)
        print(json.dumps({"completed": len(existing), "total": len(tasks), "id": task["id"]}), flush=True)


if __name__ == "__main__":
    main()
