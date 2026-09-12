"""Check saved merged checkpoints against the base and portable LoRA matrices."""
import hashlib
import json
from pathlib import Path
import torch
from safetensors import safe_open

ROOT = Path(__file__).resolve().parents[2]
base = ROOT / ".runtime/models/smolvlm-256m/model.safetensors"
reports = []
torch.set_num_threads(4)
with safe_open(base, framework="pt") as original:
    for directory in sorted((ROOT / ".runtime/vlm-training").glob("*-seed*")):
        result = directory / "result.json"
        if not result.exists():
            continue
        manifest = json.loads(result.read_text())
        if manifest["condition"] == "base":
            continue
        adapter_path = directory / "adapter/adapter_model.safetensors"
        merged_path = ROOT / ".runtime/vlm-merged" / directory.name / "model.safetensors"
        assert hashlib.sha256(adapter_path.read_bytes()).hexdigest() == manifest["adapter_sha256"]
        assert hashlib.sha256(merged_path.read_bytes()).hexdigest() == manifest["merged_model_sha256"]
        config = json.loads((directory / "adapter/adapter_config.json").read_text())
        assert not config.get("use_rslora", False) and not config.get("use_dora", False)
        changed, unchanged, max_error = 0, 0, 0.0
        with safe_open(adapter_path, framework="pt") as adapter, safe_open(merged_path, framework="pt") as merged:
            assert set(original.keys()) == set(merged.keys())
            matrices = {key.removeprefix("base_model.model.").removesuffix(".lora_A.weight"): key
                        for key in adapter.keys() if key.endswith(".lora_A.weight")}
            for key in original.keys():
                expected = original.get_tensor(key)
                actual = merged.get_tensor(key)
                name = key.removesuffix(".weight")
                if name in matrices:
                    a = adapter.get_tensor(matrices[name])
                    b = adapter.get_tensor(matrices[name].replace(".lora_A.", ".lora_B."))
                    # MPS in-place addition casts the delta before bfloat16 accumulation.
                    delta = ((b @ a) * (config["lora_alpha"] / config["r"])).to(actual.dtype)
                    expected = expected + delta
                    error = (actual.float() - expected.float()).abs()
                    max_error = max(max_error, float(error.max()))
                    # CPU and MPS products can straddle a bfloat16 rounding boundary.
                    tolerance = (original.get_tensor(key).float().abs() + delta.float().abs()) / 128 + 1e-7
                    assert torch.all(error <= tolerance), (directory.name, key, float(error.max()))
                    assert not torch.equal(actual, original.get_tensor(key)), (directory.name, key, "adapter absent")
                    changed += 1
                else:
                    assert torch.equal(actual, expected), (directory.name, key, "unadapted weight changed")
                    unchanged += 1
            assert changed == len(matrices) and changed > 0
        reports.append({"job": directory.name, "adaptedMatrices": changed, "unchangedTensors": unchanged,
                        "maxAbsoluteCPUMergeDifference": max_error, "passed": True})
output = ROOT / "suite/artifacts/study/merge-verification.json"
output.write_text(json.dumps({"runs": reports,
    "scope": "Independent CPU delta matrix reconstruction with MPS cast-before-add semantics; bfloat16 rounding tolerance, not identical logits across backends."}, indent=2) + "\n")
print(json.dumps(reports), flush=True)
