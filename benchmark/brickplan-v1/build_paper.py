"""Compile the English release manuscript without touching the existing paper."""
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    output = ROOT / "tem/brickplan-v1/validation"
    output.mkdir(parents=True, exist_ok=True)
    tectonic = shutil.which("tectonic") or str(ROOT / "benchmark/.runtime/tectonic")
    subprocess.run([tectonic, "--keep-logs", "--outdir", str(output), "paper.tex"],
                   cwd=HERE, check=True)
    shutil.copyfile(output / "paper.pdf", HERE / "paper.pdf")


if __name__ == "__main__":
    main()
