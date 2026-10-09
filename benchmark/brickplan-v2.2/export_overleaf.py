"""Create an independent, upload-ready CVPR paper folder without benchmark data."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "deliverables/brickplan-paper"
SOURCE = OUT / "overleaf"
ARCHIVE = OUT / "brickplan-cvpr-overleaf.zip"

GUIDE = """# BrickPlan CVPR manuscript — Overleaf source

1. In Overleaf, choose **New Project → Upload Project** and select
   `brickplan-cvpr-overleaf.zip`.
2. Set the main document to **main.tex** and the compiler to **XeLaTeX**.
3. Recompile. The main manuscript includes its references.
4. To build the separate supplement, set the main document to
   **supplement.tex** and recompile.

All local TeX inputs, bibliography/style files and actual figure files are
included. No Python runtime, dataset, server, external image download or
local filesystem path is required.

The public draft uses the unmodified official CVPR author-kit in
page-numbered preprint mode. For anonymous review, define `\\reviewcopy`
before the document begins in main.tex, and update the actual conference
year and paper ID. The pinned upstream kit labels itself 2026; this is
not a claim that a later year's official kit has been verified.
Replace the draft author line before camera-ready submission.

Main document: main.tex
Supplement: supplement.tex (includes appendix.tex)
References: references.bib, ieeenat_fullname.bst
Template: cvpr.sty
Generated evidence tables: the included *.tex inputs
Figures: figures/
Asset attribution and upstream provenance: included JSON/README files

This is a snapshot of the benchmark manuscript. Edit these source files
freely in Overleaf. To regenerate a fresh upload package from the repository,
run `python benchmark/brickplan-v2.2/export_overleaf.py --check`.
The repository's exporter refreshes its own deliverables folder only;
it does not modify an existing Overleaf project.
"""


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect():
    found = set()

    def visit(name):
        if name in found:
            return
        path = HERE / name
        if not path.is_file():
            raise FileNotFoundError(f"Manuscript dependency not found: {name}")
        found.add(name)
        if path.suffix != ".tex":
            return
        text = path.read_text()
        for dep in re.findall(r"\\(?:input|include)\{([^}]+)\}", text):
            visit(dep if Path(dep).suffix else dep + ".tex")
        for dep in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text):
            visit(dep)
        for dep in re.findall(r"\\bibliography\{([^}]+)\}", text):
            for stem in dep.split(","):
                visit(stem + ".bib")
        for dep in re.findall(r"\\bibliographystyle\{([^}]+)\}", text):
            visit(dep + ".bst")

    for name in ("paper.tex", "supplement.tex", "cvpr.sty", "CVPR-README.md",
                 "cvpr-template-provenance.json", "ASSET-LICENSES.json"):
        visit(name)
    return sorted(found)


def export(check=False):
    SOURCE.mkdir(parents=True, exist_ok=True)
    expected = set()
    for name in collect():
        destination = "main.tex" if name == "paper.tex" else name
        target = SOURCE / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(HERE / name, target)
        expected.add(destination)
    (SOURCE / "README.md").write_text(GUIDE)
    expected.add("README.md")
    # Only remove old generated files inside this dedicated export folder.
    for path in SOURCE.rglob("*"):
        if path.is_file() and str(path.relative_to(SOURCE)) not in expected | {"SOURCE-MANIFEST.json"}:
            path.unlink()
    inventory = {name: sha(SOURCE / name) for name in sorted(expected)}
    (SOURCE / "SOURCE-MANIFEST.json").write_text(json.dumps(inventory, indent=2) + "\n")
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(SOURCE.rglob("*")):
            if path.is_file():
                entry = zipfile.ZipInfo(str(path.relative_to(SOURCE)), (2026, 10, 9, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(entry, path.read_bytes())
    for name, target in (("paper.pdf", "brickplan-main.pdf"), ("supplement.pdf", "brickplan-supplement.pdf")):
        shutil.copyfile(HERE / name, OUT / target)
    (OUT / "README.md").write_text(
        "# BrickPlan 论文独立交付包\n\n"
        "- 上传 Overleaf：`brickplan-cvpr-overleaf.zip`，无需上传整个 benchmark。\n"
        "- 主文件选 `main.tex`，编译器选 **XeLaTeX**。\n"
        "- 附录单独编译：将主文件切换为 `supplement.tex`。\n"
        "- `overleaf/` 是可直接编辑的完整源码；同目录 PDF 可直接预览。\n"
        "- 论文源文件、图、参考文献和 CVPR 模板均已包含。\n")
    results = {}
    if check:
        import fitz
        with tempfile.TemporaryDirectory(prefix="brickplan-overleaf-") as folder:
            with zipfile.ZipFile(ARCHIVE) as archive:
                archive.extractall(folder)
            for name in ("main", "supplement"):
                process = subprocess.run(
                    [str(ROOT / "benchmark/.runtime/tectonic"), "-k", f"{name}.tex"],
                    cwd=folder, capture_output=True, text=True, check=True)
                pdf = fitz.open(Path(folder) / f"{name}.pdf")
                original = fitz.open(HERE / ("paper.pdf" if name == "main" else "supplement.pdf"))
                text = "\n".join(page.get_text() for page in pdf)
                assert len(pdf) == len(original)
                assert "??" not in text
                assert text == "\n".join(page.get_text() for page in original)
                results[name] = {"pages": len(pdf), "independentCompilePassed": True,
                                 "textMatchesPublishedPDF": True}
    manifest = {"schema": "brickplan-overleaf/1.0",
                "archive": ARCHIVE.name, "archiveSha256": sha(ARCHIVE),
                "sourceFiles": len(inventory), "checks": results,
                "files": {str(p.relative_to(OUT)): sha(p)
                          for p in sorted(OUT.rglob("*")) if p.is_file() and p.name != "manifest.json"}}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"folder": str(OUT), "zip": str(ARCHIVE),
                      "sizeMB": round(ARCHIVE.stat().st_size / 1e6, 2),
                      "sourceFiles": len(inventory), "checks": results}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    export(parser.parse_args().check)
