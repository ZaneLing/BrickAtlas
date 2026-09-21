#!/usr/bin/env python3
"""Extract only cited v2 references; verify original URLs without editing v1."""
import argparse
import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / "benchmark/paper"


def main():
    text = (PAPER / "main-v2.tex").read_text()
    keys = sorted({k for group in re.findall(r"\\cite\{([^}]+)\}", text) for k in group.split(",")})
    source = (PAPER / "references.bib").read_text()
    entries = {}
    starts = list(re.finditer(r"(?m)^@\w+\{([^,]+),", source))
    for i, match in enumerate(starts):
        entries[match.group(1)] = source[match.start():starts[i+1].start() if i+1 < len(starts) else len(source)].strip()
    (PAPER / "references-v2.bib").write_text("\n\n".join(entries[k] for k in keys) + "\n")
    checks = []
    for key in keys:
        urls = re.findall(r"https://[^}\s]+", entries[key])
        assert urls, key
        for url in urls:
            row = {"key": key, "url": url, "accessedAt": datetime.now(timezone.utc).isoformat()}
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "BrickAtlas publication reference verifier"})
                with urllib.request.urlopen(request, timeout=25) as response:
                    body = response.read()
                    challenge = "/challenge" in response.url
                    row.update(status=response.status, finalUrl=response.url, bytes=len(body),
                               contentSha256=hashlib.sha256(body).hexdigest(),
                               reachable=response.status == 200 and not challenge,
                               challengeDetected=challenge)
            except Exception as e:
                row.update(reachable=False, error=str(e))
            print(key, row.get("status", row.get("error")), flush=True)
            checks.append(row)
    # A separate read-only retrieval can verify content when urllib is challenged.
    notes_path = ROOT / "benchmark/ldraw-v2/reference-tool-evidence.json"
    notes = json.loads(notes_path.read_text()) if notes_path.exists() else {}
    for row in checks:
        note = notes.get(row["key"])
        if note and note["url"] == row["url"]:
            row["alternateContentVerification"] = note
        row["contentVerified"] = row["reachable"] or bool(note and note["url"] == row["url"])
    report = {"scope": "Only references actually cited by main-v2.tex; v1 bibliography preserved",
              "urlChecks": checks, "allReachable": all(r["reachable"] for r in checks),
              "allContentVerified": all(r["contentVerified"] for r in checks),
              "capabilityBoundary": "Abstract-level topics only for LEGO-Puzzles and PhyBlock; detailed capabilities remain to verify."}
    (ROOT / "benchmark/ldraw-v2/reference-verification.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    main()
