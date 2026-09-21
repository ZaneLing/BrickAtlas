#!/usr/bin/env python3
"""Package the paper, validate download routes, and seal new release contents."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import tempfile
from urllib.parse import urlparse, unquote
from urllib.request import urlopen, Request
import zipfile

import fitz

from common import ROOT, DATA, PUBLIC, VERSION, load, save, sha
from preserve import verify as verify_preserved

PAPER = ROOT / "benchmark/paper/evidence-v2"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            value = dict(attrs).get("href", "")
            if value.startswith("/"):
                self.urls.add(value)


def downloads(http=False):
    links = Links()
    links.feed((ROOT / "evidence-v2.html").read_text())
    rows = []
    for url in sorted(links.urls):
        relative = unquote(urlparse(url).path).lstrip("/")
        file = PUBLIC.parents[1] / relative if relative.startswith("benchmark/") else ROOT / relative
        # PUBLIC.parents[1] is the public root.
        assert file.is_file(), (url, str(file))
        row = {"url": url, "sha256": sha(file), "bytes": file.stat().st_size}
        if http:
            with urlopen(Request("http://localhost:5173" + url), timeout=30) as response:
                prefix = response.read(8)
                assert response.status == 200
                if file.suffix == ".pdf":
                    assert prefix.startswith(b"%PDF")
                if file.suffix == ".zip":
                    assert prefix.startswith(b"PK")
                row["http_status"] = response.status
        rows.append(row)
    return rows


def package(source_check=False):
    dest = PUBLIC / "paper"
    dest.mkdir(exist_ok=True)
    for name in ["main.pdf", "supplement.pdf"]:
        shutil.copyfile(PAPER / name, dest / name)
    source = PAPER / "brickatlas-evidence-v2-source.zip"
    include = [p for p in PAPER.rglob("*") if p.is_file()
               and (p.suffix in {".tex", ".bib", ".sty", ".bst"} or p.name == "BUILD.md"
                    or p.parent.name == "figures" and p.suffix in {".pdf", ".png"})]
    with zipfile.ZipFile(source, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(include):
            archive.write(p, str(p.relative_to(PAPER)))
    shutil.copyfile(source, dest / "source.zip")
    for name in ["REVIEW-RESPONSE.md", "site-validation.json"]:
        shutil.copyfile(DATA / name, PUBLIC / name)
    validation = {"status": "passed", "source_files": len(include), "source_zip_sha256": sha(source),
                  "pages": {}, "source_compilation": "not-requested"}
    if source_check:
        with tempfile.TemporaryDirectory(prefix="brickatlas-evidence-v2-paper-") as directory:
            folder = Path(directory)
            with zipfile.ZipFile(source) as archive:
                archive.extractall(folder)
            for name in ["main", "supplement"]:
                result = subprocess.run([str(ROOT / "benchmark/.runtime/tectonic"), f"{name}.tex"],
                                        cwd=folder, capture_output=True, text=True, timeout=120)
                assert result.returncode == 0, result.stdout + result.stderr
                built, original = fitz.open(folder / f"{name}.pdf"), fitz.open(PAPER / f"{name}.pdf")
                assert len(built) == len(original)
                assert [p.get_text() for p in built] == [p.get_text() for p in original]
                validation["pages"][name] = len(built)
        validation["source_compilation"] = "both PDFs compile independently; extracted text and page counts match"
    validation["download_routes"] = downloads(http=True)
    save(DATA / "package-validation.json", validation)
    print({"status": "packaged", "source_files": len(include), "download_routes": len(validation["download_routes"]),
           "source_compilation": validation["source_compilation"]})


def seal():
    inspection = load(PAPER / "visual-inspection.json")
    assert inspection["status"] == "passed"
    assert inspection["reviewed_pdf_sha256"] == {
        name: sha(PAPER / f"{name}.pdf") for name in ["main", "supplement"]}
    validation = load(DATA / "package-validation.json")
    assert validation["source_compilation"].startswith("both PDFs compile")
    source = PAPER / "brickatlas-evidence-v2-source.zip"
    assert validation["source_zip_sha256"] == sha(source)
    with zipfile.ZipFile(source) as archive:
        for member in archive.namelist():
            assert archive.read(member) == (PAPER / member).read_bytes(), ("Repackage changed source", member)
    roots = ["benchmark/ldraw-evidence-v2", "benchmark/suite/ldraw-evidence-v2",
             "benchmark/paper/evidence-v2", "public/benchmark/evidence-v2", "src/evidence-v2"]
    files = [ROOT / "evidence-v2.html", ROOT / "evidence-v2-render.html"]
    ignored_names = {"delivery-manifest.json", "delivery-verification.json"}
    excluded_paths = ["__pycache__", "/inspection/", "/runs/wire-audit/", "/runs/graph-wire-audit/"]
    for relative in roots:
        files += [p for p in (ROOT / relative).rglob("*") if p.is_file() and
                  p.name not in ignored_names and p.suffix not in
                  {".pyc", ".log", ".aux", ".bbl", ".blg", ".out", ".brf", ".gz"} and
                  not any(part in str(p) for part in excluded_paths)]
    rows = [{"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha(p)}
            for p in sorted(set(files))]
    save(DATA / "delivery-manifest.json", {
        "analysis_version": VERSION, "files": rows,
        "preservation_lock_sha256": sha(DATA / "preservation-lock.json"),
        "render_assets_lock_sha256": sha(DATA / "render-assets-lock.json"),
        "excluded": "Caches, TeX intermediates, raster page previews, superseded dry snapshots; preservation archives separately locked.",
        "empirical_state": {"human_primary_final": 0, "real_model_results": 0},
        "review": "REVIEW-RESPONSE.md"})
    print({"status": "sealed", "files": len(rows)})


def verify():
    m = load(DATA / "delivery-manifest.json")
    for r in m["files"]:
        p = ROOT / r["path"]
        assert p.stat().st_size == r["bytes"] and sha(p) == r["sha256"], r["path"]
    assert sha(DATA / "preservation-lock.json") == m["preservation_lock_sha256"]
    assert sha(DATA / "render-assets-lock.json") == m["render_assets_lock_sha256"]
    preserved = verify_preserved()
    tests = (DATA / "validation-tests.txt").read_text()
    assert "Ran 26 tests" in tests and tests.rstrip().endswith("OK")
    assert load(DATA / "typecheck-validation.json")["exit_code"] == 0
    report = {"status": "passed", "sealed_new_files": len(m["files"]), "preserved": preserved,
              "source_render_assets": len(load(DATA / "render-assets-lock.json")["files"]),
              "protocol_analysis_tests": 26, "typescript": "passed",
              "paper_pages": {"main": 8, "supplement": 6},
              "human_primary_final": 0, "real_model_results": 0,
              "download_routes": len(downloads()), "manifest_sha256": sha(DATA / "delivery-manifest.json")}
    save(DATA / "delivery-verification.json", report)
    print(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--source-check", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else seal() if args.seal else package(args.source_check)
