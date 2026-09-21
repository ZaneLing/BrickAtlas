#!/usr/bin/env python3
"""Package verified v2-only manuscripts and publish local document copies."""
import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / "benchmark/paper"
DATA = ROOT / "benchmark/ldraw-v2"
DOCS = ROOT / "public/benchmark/ldraw-v2/docs"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    verification = json.loads((DATA / "publication-verification.json").read_text())
    assert verification["status"] == "passed"
    for name, record in verification["pdfs"].items():
        assert sha(PAPER / f"{name}.pdf") == record["pdfSha256"]
    files = [PAPER / f for f in ["main-v2.tex", "supplement-v2.tex", "references-v2.bib",
             "cvpr.sty", "ieeenat_fullname.bst", "BUILD-v2.md", "ldraw-v2-experiments.json"]]
    files += sorted((PAPER / "figures-v2").glob("*")) + sorted((PAPER / "tables-v2").glob("*"))
    names = {str(p.relative_to(PAPER)) for p in files}
    for p in files:
        if p.suffix == ".tex":
            for q in re.findall(r"\\(?:input|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}", p.read_text()):
                assert q in names or q + ".tex" in names, (p, q, "missing package dependency")
    target = PAPER / "brickatlas-ldraw-v2-source.zip"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for p in files:
            info = zipfile.ZipInfo(str(p.relative_to(PAPER)), date_time=(2026, 9, 18, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, p.read_bytes())
        for name in ["publication-manifest.json", "publication-verification.json", "reference-verification.json"]:
            info = zipfile.ZipInfo(f"audit/{name}", date_time=(2026, 9, 18, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (DATA / name).read_bytes())
    DOCS.mkdir(exist_ok=True)
    for p in [PAPER / "main-v2.pdf", PAPER / "supplement-v2.pdf", PAPER / "BUILD-v2.md", target]:
        shutil.copyfile(p, DOCS / p.name)
        assert sha(p) == sha(DOCS / p.name)
    for name in ["DELIVERY.md", "PHASE-5-REPORT.md"]:
        if (DATA / name).exists():
            shutil.copyfile(DATA / name, DOCS / name)
    report = {"version": "brickatlas-ldraw-2", "status": "packaged",
              "documents": {str(p.relative_to(ROOT)): sha(p) for p in sorted(DOCS.iterdir()) if p.is_file()},
              "sourceArchiveFiles": len(files) + 3, "compileDependenciesPresent": True,
              "modelResults": None, "humanCertification": "pending"}
    (DATA / "delivery-manifest.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"documents": len(report["documents"]), "archive": str(target),
                      "archiveFiles": report["sourceArchiveFiles"]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    main()
