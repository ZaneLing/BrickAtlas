#!/usr/bin/env python3
"""Exercise paired estimators on separate synthetic fixtures, never model results."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parents[2]
with tempfile.TemporaryDirectory(prefix="ldraw-v2-statistics-") as tmp:
    tmp = Path(tmp)
    for cond in ["a", "b"]:
        rows = []
        for source, n in [("small", 1), ("large", 3)]:
            for i in range(n):
                rows.append({"id": f"{source}-{i}", "modelId": source, "family": "fixture",
                             "verdict": {"success": int(cond == "a" and source == "small")}})
        (tmp / f"{cond}.json").write_text(json.dumps({
            "version": "brickatlas-ldraw-2", "missing": 0, "rows": rows}))
    command = [sys.executable, str(here / "paired-analysis.py"), "--a", str(tmp / "a.json"),
               "--b", str(tmp / "b.json"), "--out", str(tmp / "paired.json")]
    subprocess.run(command, check=True)
    first = (tmp / "paired.json").read_bytes()
    subprocess.run(command, check=True)
    assert (tmp / "paired.json").read_bytes() == first
    result = json.loads(first)["byFamily"]["fixture"]
    assert result["deltaMacro"] == .5 and result["deltaMicro"] == .25
    assert result["correctToWrong"] == 1 and result["wrongToCorrect"] == 0
    assert result["macroCI95"] == [0, 1]
    assert "equivalence not established" in result["interpretation"]
report = {"status": "passed", "purpose": "Synthetic implementation fixture only; not benchmark evidence",
          "checks": ["source macro vs micro weighting", "source-block CI", "paired transitions",
                     "fixed-seed reproducibility", "no-equivalence wording"]}
(root / "benchmark/ldraw-v2/statistics-verification.json").write_text(json.dumps(report, indent=2) + "\n")
print("Paired-statistics implementation fixtures passed.")
