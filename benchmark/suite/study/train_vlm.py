"""V2 image-conditioned LoRA with exact supervised-token budgets and audited inputs."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import random
import time
import gc
import shutil
import subprocess

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText
from peft import LoraConfig, get_peft_model

ROOT = Path(__file__).resolve().parents[2]
MODEL = "HuggingFaceTB/SmolVLM-256M-Instruct"
REVISION = "7e3e67edbbed1bf9888184d9df282b700a323964"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(value, indent=2) + "\n")
    tmp.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["base", "single", "multi", "leave-edit"], required=True)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--tokens-per-step", type=int, default=512)
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()
    out = ROOT / ".runtime/vlm-training" / (args.condition + "-seed" + str(args.seed))
    out.mkdir(parents=True, exist_ok=True)
    lock = (out / "lock").open("w")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    if (out / "result.json").exists():
        raise RuntimeError("Completed run exists; refuse to overwrite")
    if (out / "manifest.json").exists() and not args.probe:
        raise RuntimeError("Incomplete run exists; explicit recovery required")
    rng = random.Random(args.seed)
    torch.manual_seed(args.seed)
    torch.set_num_threads(6)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.bfloat16 if device == "mps" else torch.float32
    base = ROOT / ".runtime/models/smolvlm-256m"
    processor = AutoProcessor.from_pretrained(base, local_files_only=True, trust_remote_code=False)
    processor.image_processor.do_image_splitting = False
    processor.image_processor.size = {"longest_edge": 512}
    model = AutoModelForImageTextToText.from_pretrained(
        base, local_files_only=True, trust_remote_code=False, torch_dtype=dtype, attn_implementation="sdpa").to(device)
    model.config.use_cache = False
    data_dir = ROOT / ".runtime/study-training"
    train = [json.loads(l) for l in (data_dir / "train.jsonl").read_text().splitlines()]
    valid = [json.loads(l) for l in (data_dir / "validation.jsonl").read_text().splitlines()]
    assert not {r["group"] for r in train} & {r["group"] for r in valid}
    if args.condition == "single":
        train = [r for r in train if r["kind"] == "reconstruct"]
    if args.condition == "leave-edit":
        train = [r for r in train if r["kind"] != "edit"]
    rng.shuffle(train)
    tokenizer = processor.tokenizer

    def encode(row, image_root, with_answer):
        images = [Image.open(image_root / path).convert("RGB") for path in row["images"]]
        payload = row["input"]
        messages = [
            {"role": "system", "content": [{"type": "text", "text": row["system"]}]},
            {"role": "user", "content": [{"type": "image"} for _ in images] +
             [{"type": "text", "text": json.dumps(payload, separators=(",", ":"))}]},
        ]
        prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
        answer = json.dumps(row["answer"], separators=(",", ":")) + tokenizer.eos_token if with_answer else ""
        encoded = processor(text=prompt + answer, images=images or None, return_tensors="pt")
        prefix = processor(text=prompt, images=images or None, return_tensors="pt")["input_ids"].shape[1]
        if with_answer:
            labels = encoded["input_ids"].clone()
            labels[:, :prefix] = -100
            encoded["labels"] = labels
        return encoded, prefix

    cache = {}

    def tensors(row):
        if row["caseId"] not in cache:
            encoded, prefix = encode(row, data_dir, True)
            if encoded["input_ids"].shape[1] > 8192:
                raise RuntimeError("Context overflow; no silent truncation")
            cache[row["caseId"]] = encoded
        return {k: v.to(device=device, dtype=dtype if v.dtype.is_floating_point else v.dtype) for k, v in cache[row["caseId"]].items()}

    if args.condition != "base":
        targets = [name for name, _ in model.named_modules()
                   if ".text_model." in name and name.endswith((".q_proj", ".v_proj"))]
        if not targets:
            targets = [name for name, _ in model.named_modules()
                       if "vision_model" not in name and name.endswith((".q_proj", ".v_proj"))]
        model = get_peft_model(model, LoraConfig(r=8, lora_alpha=16, lora_dropout=0.0,
            target_modules=targets, task_type="CAUSAL_LM"))
    if args.probe:
        row = next(r for r in train if r["images"])
        batch = tensors(row)
        loss = model(**batch).loss
        assert torch.isfinite(loss)
        loss.backward()
        print(json.dumps({"probe": True, "loss": float(loss.detach()), "input_tokens": batch["input_ids"].shape[1],
                          "images": len(row["images"]), "pixel_shape": list(batch["pixel_values"].shape),
                          "trainable_parameters": sum(p.numel() for p in model.parameters() if p.requires_grad)}), flush=True)
        return
    manifest = {
        "model": MODEL, "revision": REVISION, "condition": args.condition, "seed": args.seed,
        "device": device, "dtype": str(dtype), "script_sha256": sha(__file__),
        "trainable_parameters": sum(p.numel() for p in model.parameters() if p.requires_grad) if args.condition != "base" else 0,
        "model_sha256": sha(base / "model.safetensors"), "config": vars(args),
        "train_file_sha256": sha(data_dir / "train.jsonl"), "validation_file_sha256": sha(data_dir / "validation.jsonl"),
        "train_rows": len(train), "train_groups": len({r["group"] for r in train}),
        "image_processing": {"image_splitting": False, "longest_edge": 512, "views": "all supplied"},
        "supervision": "Exactly tokens_per_step loss-bearing answer tokens per update, masked deterministic random subsets. Full inputs/answers retained, not truncated.",
        "limitation": "Equal supervised tokens and optimizer steps, not equal image/compute/input-token budgets. Short training pilot.",
        "started_at": time.time(), "status": "running",
    }
    save(out / "manifest.json", manifest)
    validation = []
    for kind in sorted({r["kind"] for r in valid}):
        validation.extend([r for r in valid if r["kind"] == kind][:2])

    def validation_loss():
        model.eval()
        totals, counts = {}, {}
        with torch.no_grad():
            for row in validation:
                batch = tensors(row)
                n = int((batch["labels"][:, 1:] != -100).sum().item())
                loss = float(model(**batch).loss.item())
                totals[row["kind"]] = totals.get(row["kind"], 0) + loss * n
                counts[row["kind"]] = counts.get(row["kind"], 0) + n
        return {k: totals[k] / counts[k] for k in totals}

    before = validation_loss()
    history = []
    if args.condition != "base":
        model.train()
        optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=2e-4, weight_decay=0.01)
        cursor = 0
        for step in range(args.steps):
            optimizer.zero_grad(set_to_none=True)
            remaining, total_loss, samples = args.tokens_per_step, 0.0, []
            while remaining:
                row = train[cursor % len(train)]; cursor += 1
                batch = tensors(row); labels = batch["labels"].clone()
                positions = torch.nonzero(labels[0] != -100).flatten().tolist()
                chosen = rng.sample(positions, min(remaining, len(positions)))
                labels[:] = -100
                labels[0, chosen] = batch["input_ids"][0, chosen]
                batch["labels"] = labels
                loss = model(**batch).loss
                if not torch.isfinite(loss):
                    raise RuntimeError("Nonfinite multimodal loss")
                (loss * len(chosen) / args.tokens_per_step).backward()
                total_loss += float(loss.item()) * len(chosen) / args.tokens_per_step
                remaining -= len(chosen)
                samples.append({"caseId": row["caseId"], "kind": row["kind"], "supervised_tokens": len(chosen),
                                "input_tokens": batch["input_ids"].shape[1], "images": len(row["images"])})
            gradient = torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
            if not torch.isfinite(gradient):
                raise RuntimeError("Nonfinite gradient")
            optimizer.step()
            history.append({"step": step+1, "loss": total_loss, "samples": samples,
                            "supervised_tokens": args.tokens_per_step})
            save(out / "steps.json", history)
            if step % 10 == 0:
                print(json.dumps({"step": step+1, "loss": total_loss}), flush=True)
        model.save_pretrained(out / "adapter", safe_serialization=True)
        manifest["adapter_sha256"] = sha(out / "adapter/adapter_model.safetensors")
    after = validation_loss()
    model.eval(); model.config.use_cache = True
    public_file = ROOT / "suite/artifacts/study/inputs/public.jsonl"
    manifest["test_input_sha256"] = sha(public_file)
    inference_model = base
    if args.condition != "base":
        inference_model = ROOT / ".runtime/vlm-merged" / out.name
        merged = model.merge_and_unload()
        merged.save_pretrained(inference_model, safe_serialization=True)
        for name in ["tokenizer.json", "tokenizer_config.json", "special_tokens_map.json", "added_tokens.json",
                     "merges.txt", "vocab.json", "preprocessor_config.json", "processor_config.json", "chat_template.json", "generation_config.json"]:
            shutil.copyfile(base / name, inference_model / name)
        manifest["merged_model_sha256"] = sha(inference_model / "model.safetensors")
        del merged, optimizer, batch, loss
    del model
    cache.clear(); gc.collect()
    if device == "mps":
        torch.mps.empty_cache()
    inference_script = Path(__file__).with_name("infer_mlx.py")
    manifest["inference_script_sha256"] = sha(inference_script)
    manifest["inference_backend"] = "mlx-vlm-0.7.0-unquantized; not bit-identical to PyTorch kernels"
    manifest["validation_before"] = before
    manifest["validation_after"] = after
    manifest["steps"] = len(history)
    manifest["supervised_tokens"] = len(history)*args.tokens_per_step
    save(out / "manifest.json", manifest)
    subprocess.run([str(ROOT / ".runtime/mlx-env/bin/python"), "-u", str(inference_script),
                    "--model", str(inference_model), "--output", str(out)], check=True)
    predictions = json.loads((out / "predictions.json").read_text())
    manifest.update({"status": "complete", "completed_at": time.time(), "validation_before": before,
                     "validation_after": after, "steps": len(history), "supervised_tokens": len(history)*args.tokens_per_step,
                     "predictions": len(predictions)})
    save(out / "result.json", manifest)
    print(json.dumps({"condition": args.condition, "seed": args.seed, "status": "complete"}), flush=True)


if __name__ == "__main__":
    main()
