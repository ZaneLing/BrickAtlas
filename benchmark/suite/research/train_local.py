"""Local, versioned LoRA pilot. Text/structure tasks only; never calls an API."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import time

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, PeftModel, get_peft_model

ROOT = Path(__file__).resolve().parents[2]
MODEL_ID = "Qwen/Qwen3-0.6B"
REVISION = "c1899de289a04d12100db370d81485cdf75e47ca"
TASKS = {"relations", "generate", "edit", "plan"}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def messages(row):
    # Training and local evaluation use exactly this same public user payload.
    payload = row["input"]
    return [{"role": "system", "content": row["system"]},
            {"role": "user", "content": json.dumps({
                "prompt": payload["prompt"], "input": payload["input"],
                "responseSchema": payload["responseSchema"], "imageTitles": [],
            }, separators=(",", ":"))}]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["base", "single", "multi"], required=True)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--max-length", type=int, default=3072)
    parser.add_argument("--max-new-tokens", type=int, default=1200)
    parser.add_argument("--skip-predict", action="store_true")
    args = parser.parse_args()
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.set_num_threads(6)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.bfloat16 if device == "mps" else torch.float32
    local = ROOT / ".runtime/models/qwen3-0.6b"
    output = ROOT / ".runtime/local-training" / f"{args.condition}-seed{args.seed}"
    if (output / "result.json").exists():
        raise RuntimeError("Completed run exists; refuse to overwrite recorded training")
    output.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(str(local), local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        str(local), local_files_only=True, trust_remote_code=False,
        torch_dtype=dtype, attn_implementation="sdpa").to(device)
    model.config.use_cache = False
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    manifest = {
        "base_model": MODEL_ID, "revision": REVISION, "license": "Apache-2.0",
        "condition": args.condition, "seed": args.seed, "device": device,
        "dtype": str(dtype), "torch": torch.__version__,
        "script_sha256": sha(__file__), "config": vars(args),
        "modalities": "text/structure only; no vision training",
        "model_safetensors_sha256": sha(local / "model.safetensors"),
        "status": "running", "started_at": time.time(),
    }
    save(output / "manifest.json", manifest)
    exports = ROOT / ".runtime/suite-exports"
    train_file = exports / "train.sft.jsonl"
    validation_file = exports / "validation.sft.jsonl"
    inputs_file = exports / "inputs.jsonl"
    manifest["data_hashes"] = {p.name: sha(p) for p in [train_file, validation_file, inputs_file]}

    def load(path, split):
        rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        assert all(r["split"] == split for r in rows)
        return [r for r in rows if not r["needsImages"] and r["kind"] in TASKS]

    training, validation = load(train_file, "train"), load(validation_file, "validation")
    assert not ({r["group"] for r in training} & {r["group"] for r in validation})
    if args.condition == "single":
        training = [r for r in training if r["kind"] == "edit"]
    rng = random.Random(args.seed)
    rng.shuffle(training)

    def encode(row):
        user = json.loads(row["messages"][1]["content"])
        prompt_messages = messages({"system": row["messages"][0]["content"], "input": user})
        prompt = tokenizer.apply_chat_template(prompt_messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        answer = row["messages"][2]["content"] + tokenizer.eos_token
        prefix = tokenizer(prompt, add_special_tokens=False)["input_ids"]
        suffix = tokenizer(answer, add_special_tokens=False)["input_ids"]
        if len(prefix) + len(suffix) > args.max_length:
            return None
        return {"ids": prefix + suffix, "labels": [-100] * len(prefix) + suffix, "kind": row["kind"], "target_tokens": len(suffix)}

    train_rows = [encoded for r in training if (encoded := encode(r)) is not None]
    valid_rows = []
    for kind in sorted(TASKS):
        rows = [r for r in validation if r["kind"] == kind]
        valid_rows.extend([encoded for r in rows[:4] if (encoded := encode(r)) is not None])
    manifest["train_rows"] = len(train_rows)
    manifest["overlength_training_rows_excluded"] = len(training) - len(train_rows)
    manifest["validation_rows"] = len(valid_rows)
    save(output / "manifest.json", manifest)

    def tensors(row):
        return {"input_ids": torch.tensor([row["ids"]], device=device),
                "labels": torch.tensor([row["labels"]], device=device)}

    def evaluate_loss():
        model.eval()
        losses, counts = {}, {}
        with torch.no_grad():
            for row in valid_rows:
                loss = float(model(**tensors(row)).loss.item())
                losses[row["kind"]] = losses.get(row["kind"], 0) + loss * row["target_tokens"]
                counts[row["kind"]] = counts.get(row["kind"], 0) + row["target_tokens"]
        return {kind: losses[kind] / counts[kind] for kind in losses}

    before = evaluate_loss()
    log = []
    if args.condition != "base":
        config = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.0,
                            target_modules=["q_proj", "v_proj"], task_type="CAUSAL_LM")
        model = get_peft_model(model, config)
        model.train()
        optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=2e-4, weight_decay=0.01)
        start = time.perf_counter()
        tokens = 0
        for step in range(args.steps):
            row = train_rows[step % len(train_rows)]
            optimizer.zero_grad(set_to_none=True)
            loss = model(**tensors(row)).loss
            if not torch.isfinite(loss):
                raise RuntimeError("Nonfinite loss; refusing to publish a corrupted checkpoint")
            loss.backward()
            grad = torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
            if not torch.isfinite(grad):
                raise RuntimeError("Nonfinite gradient")
            optimizer.step()
            tokens += len(row["ids"])
            entry = {"step": step + 1, "task": row["kind"], "loss": float(loss.item()),
                     "input_and_output_tokens": len(row["ids"]), "target_tokens": row["target_tokens"],
                     "elapsed_seconds": time.perf_counter() - start}
            log.append(entry)
            if step % 5 == 0 or step + 1 == args.steps:
                with (output / "training.jsonl").open("a") as stream:
                    stream.write(json.dumps(entry) + "\n")
                print(json.dumps(entry), flush=True)
        model.save_pretrained(str(output / "adapter"), safe_serialization=True)
        tokenizer.save_pretrained(str(output / "adapter"))
        manifest["adapter_sha256"] = sha(output / "adapter/adapter_model.safetensors")
        manifest["trained_parameters"] = sum(p.numel() for p in model.parameters() if p.requires_grad)
        manifest["optimization_steps"] = len(log)
        manifest["processed_tokens"] = tokens
        save(output / "training-steps.json", log)
    after = evaluate_loss()
    predictions = []
    if not args.skip_predict:
        model.eval()
        model.config.use_cache = True
        for row in [json.loads(line) for line in inputs_file.read_text().splitlines() if line.strip()]:
            if row["modality"] != "text/structure" or row["input"]["kind"] not in TASKS:
                continue
            prompt = tokenizer.apply_chat_template(messages(row), tokenize=False, add_generation_prompt=True, enable_thinking=False)
            inputs = tokenizer(prompt, return_tensors="pt").to(device)
            start = time.perf_counter()
            with torch.no_grad():
                result = model.generate(**inputs, do_sample=False, max_new_tokens=args.max_new_tokens,
                                        pad_token_id=tokenizer.pad_token_id, eos_token_id=tokenizer.eos_token_id)
            text = tokenizer.decode(result[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True)
            try:
                answer = json.loads(text.strip())
            except ValueError:
                answer = None
            predictions.append({"taskId": row["taskId"], "answer": answer, "raw": text,
                                "new_tokens": result.shape[1] - inputs["input_ids"].shape[1],
                                "seconds": time.perf_counter() - start})
            print(json.dumps({"prediction": row["taskId"], "parsed": answer is not None}), flush=True)
            save(output / "predictions.json", predictions)
    manifest.update({"status": "complete", "completed_at": time.time(),
                     "validation_loss_before": before, "validation_loss_after": after,
                     "predictions": len(predictions),
                     "limitation": "Small local LoRA pilot, one seed per run. Step-matched is not token-matched; text tasks only. Not a trained multimodal foundation model."})
    save(output / "result.json", manifest)
    save(output / "manifest.json", manifest)
    print(json.dumps({"condition": args.condition, "status": "complete", "output": str(output),
                      "before": before, "after": after}), flush=True)


if __name__ == "__main__":
    main()
