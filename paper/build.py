#!/usr/bin/env python3
"""Compile the checked-in manuscripts; keep compiler output outside paper/."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=ROOT / "tem/build/paper")
    parser.add_argument("--check-only", action="store_true",
                        help="Compile without replacing the publication PDFs.")
    args = parser.parse_args()
    executable = os.environ.get("TECTONIC") or shutil.which("tectonic")
    if not executable:
        executable = str(ROOT / "benchmark/.runtime/tectonic")
    output = args.outdir.resolve()
    assert output != HERE, "Compiler output belongs outside paper/."
    output.mkdir(parents=True, exist_ok=True)
    for stem in ("main", "supplement"):
        subprocess.run([executable, "--keep-logs", "--keep-intermediates",
                        "--outdir", str(output), f"{stem}.tex"], cwd=HERE, check=True)
    if not args.check_only:
        for stem in ("main", "supplement"):
            shutil.copyfile(output / f"{stem}.pdf", HERE / f"{stem}.pdf")
    print(f"Compiler output: {output}")
    print("Publication PDFs unchanged." if args.check_only else "Publication PDFs updated in paper/.")


if __name__ == "__main__":
    main()
