"""Finite text-only interface calibration. Never trains or reads probe answers."""
import fcntl
import hashlib
import json
from pathlib import Path
import time

from mlx_vlm import load, generate
import mlx.core as mx

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "suite/artifacts/study/interface-probes"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(value, indent=2) + "\n")
    tmp.replace(path)


def main():
    inputs = OUT / "inputs.json"
    protocol = json.loads(inputs.read_text())
    with (ROOT / ".runtime/interface-probes.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for checkpoint in protocol["checkpoints"]:
            path = OUT / (checkpoint + ".json")
            base = ROOT / ".runtime/models/smolvlm-256m" if checkpoint.startswith("base") else ROOT / ".runtime/vlm-merged" / checkpoint
            evidence = {"checkpoint": checkpoint, "inputsSha256": sha(inputs),
                        "modelSha256": sha(base / "model.safetensors"), "scriptSha256": sha(Path(__file__)),
                        "backend": "mlx-vlm-0.7.0-unquantized"}
            if path.exists():
                previous = json.loads(path.read_text())
                assert all(previous[k] == v for k, v in evidence.items()), "Existing probe evidence differs"
                assert previous["status"] == "complete", "Incomplete probe: preserve evidence and recover explicitly"
                assert len(previous["predictions"]) == len(protocol["cases"])
                print(json.dumps({"checkpoint": checkpoint, "status": "already-complete"}), flush=True)
                continue
            model, processor = load(str(base))
            processor.chat_template = json.loads((base / "chat_template.json").read_text())["chat_template"]
            evidence.update({"status": "running", "predictions": [], "startedAt": time.time()})
            save(path, evidence)
            for row in protocol["cases"]:
                messages = [{"role": "system", "content": [{"type": "text", "text": row["system"]}]},
                            {"role": "user", "content": [{"type": "text", "text": row["user"]}]}]
                prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
                start = time.perf_counter()
                result = generate(model, processor, prompt, image=None, max_tokens=protocol["maxTokens"],
                                  temperature=protocol["temperature"], verbose=False)
                evidence["predictions"].append({"id": row["id"], "raw": result.text,
                    "inputTokens": result.prompt_tokens, "outputTokens": result.generation_tokens,
                    "seconds": time.perf_counter() - start})
                save(path, evidence)
                print(json.dumps({"checkpoint": checkpoint, "completed": len(evidence["predictions"])}), flush=True)
            evidence.update({"status": "complete", "completedAt": time.time()})
            save(path, evidence)
            del model, processor
            mx.clear_cache()


if __name__ == "__main__":
    main()
