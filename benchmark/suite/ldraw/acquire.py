"""Acquire unchanged OMR candidates; selection follows dependency/geometry audit."""
from pathlib import Path
import subprocess
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "benchmark/ldraw-v1/sources"
OUT.mkdir(parents=True, exist_ok=True)
# Different official sets, not generated variations or alternative builds.
NUMBERS = [
    "42004", "42007", "42020", "42025", "42042", "42043", "42054", "42055",
    "42061", "42064", "42065", "42066", "42074", "42075", "42078", "42081",
    "42082", "42102", "42105", "42110", "9391", "9396", "8043", "8110",
    "31019", "31031", "31044", "31058", "31062", "31088", "31090", "31094",
    "31097", "31098", "31109", "31112", "31120", "31121", "21303", "21309",
    "21318", "10231", "10242", "10252", "10258", "10265", "10266", "10269",
]
records = []
for number in NUMBERS:
    url = f"https://library.ldraw.org/library/omr/{number}-1.mpd"
    path = OUT / f"{number}-1.mpd"
    if not path.exists():
        partial = path.with_suffix(".partial")
        run = subprocess.run(["curl", "-fLs", "--max-time", "18", url, "-o", str(partial)])
        if run.returncode == 0:
            partial.rename(path)
        else:
            partial.unlink(missing_ok=True)
    if path.exists():
        raw = path.read_bytes()
        content = raw.decode("utf-8-sig", errors="replace")
        if not re.search(r"^1\s", content, re.M) or "<html" in content.lower():
            path.unlink()
            continue
        first = re.split(r"^0 FILE ", content, flags=re.M)[1] if "0 FILE " in content else content
        author = re.search(r"^0 Author:\s*(.+)$", first, re.M)
        license = re.search(r"^0 !LICENSE\s*(.+)$", first, re.M)
        title = next((line[2:] for line in first.splitlines()[1:] if line.startswith("0 ") and not re.match(r"0 (Name:|Author:|!)", line)), number)
        records.append({"id": number, "url": url, "sha256": hashlib.sha256(raw).hexdigest(),
                        "author": author[1].strip() if author else None,
                        "license": license[1].strip() if license else None, "title": title})
        print(f"{number}: {title} ({len(raw)} bytes)", flush=True)
    else:
        print(f"{number}: unavailable", flush=True)
    (OUT.parent / "acquired.json").write_text(json.dumps(records, indent=2) + "\n")
