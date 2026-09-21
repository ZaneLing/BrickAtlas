#!/usr/bin/env python3
"""Compile a fresh paper archive without reading source files from the checkout."""
import subprocess
import tempfile
import zipfile
from pathlib import Path

from common import ROOT, save, sha


def main():
    import fitz
    paper = ROOT / "benchmark/paper/evidence-v1"
    archive = paper / "paper-source.zip"
    rows = []
    with tempfile.TemporaryDirectory(prefix="brickatlas-paper-extract-") as directory:
        with zipfile.ZipFile(archive) as z:
            z.extractall(directory)
        for name in ["main", "supplement"]:
            result = subprocess.run(
                [str(ROOT / "benchmark/.runtime/tectonic"), "--only-cached", name + ".tex"],
                cwd=directory, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(result.stderr)
            rebuilt = fitz.open(Path(directory) / f"{name}.pdf")
            original = fitz.open(paper / f"{name}.pdf")
            assert len(rebuilt) == len(original)
            assert [p.get_text() for p in rebuilt] == [p.get_text() for p in original]
            rows.append({"document": name, "pages": len(rebuilt), "all_page_text_matches": True})
    report = {"status": "passed", "fresh_extraction_compile": rows,
              "archive_sha256": sha(archive)}
    save(paper / "archive-compile-verification.json", report)
    print(report)


if __name__ == "__main__":
    main()
