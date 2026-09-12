"""Measure private test oracle serialization lengths, never model them as inputs."""
import json
from pathlib import Path
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
tokenizer = AutoTokenizer.from_pretrained(ROOT / ".runtime/models/smolvlm-256m", local_files_only=True)
witnesses = json.loads((ROOT / ".runtime/study-test-token-witness.json").read_text())
rows = []
for row in witnesses:
    answer = json.dumps(row["answer"], separators=(",", ":")) + tokenizer.eos_token
    tokens = len(tokenizer(answer, add_special_tokens=False)["input_ids"])
    rows.append({"caseId": row["caseId"], "kind": row["kind"], "oracleTokens": tokens,
                 "exceedsOutputCap": tokens > 2200})
result = {"cases": len(rows), "maximumOracleTokens": max(r["oracleTokens"] for r in rows),
          "exceedsOutputCap": sum(r["exceedsOutputCap"] for r in rows), "rows": rows,
          "scope": "SmolVLM compact oracle serialization only; no test answer passed to inference. Other tokenizers and equivalent answers can have different lengths."}
(ROOT / "suite/artifacts/study/test-token-audit.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "rows"}))
