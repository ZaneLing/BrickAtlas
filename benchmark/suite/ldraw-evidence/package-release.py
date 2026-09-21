#!/usr/bin/env python3
"""Package a standalone paper source; stage local web assets; seal new files."""
import argparse
import hashlib
import re
import shutil
import zipfile

from common import DATA, ROOT, VERSION, load, save, sha

PAPER = ROOT / "benchmark/paper/evidence-v1"
SITE = ROOT / "public/benchmark/evidence-v1"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seal", action="store_true")
    args = parser.parse_args()
    verified = load(PAPER / "pdf-verification.json")
    assert verified["status"] == "passed"
    for name in ["main", "supplement"]:
        assert sha(PAPER / f"{name}.pdf") == verified["documents"][name]["sha256"]
    files = {p for p in PAPER.iterdir() if p.suffix in {".tex", ".bib", ".bst", ".sty"}}
    files.update(PAPER / n for n in ["README.md", "BUILD.md", "asset-provenance.json"])
    for directory in ["figures", "generated", "figures-v2"]:
        files.update(p for p in (PAPER / directory).iterdir()
                     if p.suffix in {".tex", ".pdf", ".jpg", ".csv", ".json"})
    archive = PAPER / "paper-source.zip"
    hashes = {str(p.relative_to(PAPER)): sha(p) for p in sorted(files)}
    generator = ROOT / "benchmark/suite/ldraw-evidence/publication.py"
    hashes["figure-source.py"] = sha(generator)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        def member(name, content):
            info = zipfile.ZipInfo(str(name), date_time=(2026, 9, 19, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, content)
        for p in sorted(files):
            member(p.relative_to(PAPER), p.read_bytes())
        member("figure-source.py", generator.read_bytes())
        member("SOURCE-SHA256.json", __import__("json").dumps(hashes, indent=2) + "\n")
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for path, expected in hashes.items():
            assert hashlib.sha256(z.read(path)).hexdigest() == expected
    SITE.mkdir(parents=True, exist_ok=True)
    copies = {
        "main.pdf": PAPER / "main.pdf", "supplement.pdf": PAPER / "supplement.pdf",
        "paper-source.zip": archive, "node-prior-audit.json": DATA / "node-prior-audit.json",
        "wrong-image-review.html": DATA / "qa/wrong-image-export-v1/review.html",
        "qa-template.json": DATA / "qa/wrong-image-export-v1/qa-template.json",
    }
    for name, source in copies.items():
        shutil.copyfile(source, SITE / name)
        assert sha(source) == sha(SITE / name)
    html = (ROOT / "evidence-v1.html").read_text()
    for href in re.findall(r'href="([^"]+)"', html):
        assert (ROOT / href.lstrip("/")).exists() or (ROOT / "public" / href.lstrip("/")).exists(), href
    nums = load(PAPER / "generated/numbers.json")
    assert re.findall(r"<td>(\d+)</td>", html) == [str(nums[k]) for k in ["Visual", "Structural", "Controls", "Constant"]]
    compile_path = PAPER / "archive-compile-verification.json"
    compiled = load(compile_path) if compile_path.exists() else {}
    compile_status = ("passed" if compiled.get("status") == "passed"
                      and compiled.get("archive_sha256") == sha(archive) else "pending-fresh-extraction-check")
    save(PAPER / "package-verification.json", {
        "status": "passed", "archive_sha256": sha(archive), "source_files": len(hashes),
        "standalone_compile": compile_status,
        "web_copies": {name: sha(SITE / name) for name in copies},
        "web_links": "all local destinations exist"})
    if args.seal:
        roots = [DATA, PAPER, SITE, ROOT / "benchmark/suite/ldraw-evidence"]
        excluded = {"delivery-manifest.json", "final-validation.json", "v2-before-five-issues.tar.gz"}
        paths = [p for r in roots for p in r.rglob("*") if p.is_file()
                 and p.name not in excluded and "inspection" not in p.parts
                 and "__pycache__" not in p.parts and p.suffix not in {".aux", ".log", ".out", ".blg", ".brf", ".bbl"}]
        paths.append(ROOT / "evidence-v1.html")
        save(DATA / "delivery-manifest.json", {
            "analysis_version": VERSION, "files": [
                {"path": str(p.relative_to(ROOT)), "sha256": sha(p), "bytes": p.stat().st_size}
                for p in sorted(set(paths))],
            "baseline_lock_sha256": sha(DATA / "baseline-lock.json"),
            "original_archive_sha256": load(DATA / "baseline-lock.json")["archive_sha256"],
            "excluded": ["self and final validation receipt", "redundant PDF inspection images", "compiler intermediates", "Python cache"],
            "scope": "New revision files; original archive separately bound by baseline lock."})
    print({"status": "passed", "paper_source_files": len(hashes), "web_assets": len(copies), "sealed": args.seal})


if __name__ == "__main__":
    main()
