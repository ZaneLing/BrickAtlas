"""Resolve explicitly recorded relocations without rewriting frozen manifests."""
import json
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tem/repository-layout-20260924/moves.json"


@cache
def relocations():
    data = json.loads(MANIFEST.read_text())
    return sorted(data["moves"] + data["removed_aliases"],
                  key=lambda item: len(item["old"]), reverse=True)


def relocated(relative):
    for row in relocations():
        if relative == row["old"] or relative.startswith(row["old"] + "/"):
            return row["new"] + relative[len(row["old"]):]
    return relative


def historical(relative):
    # The v4 baseline locks these operational files. Updated launchers and
    # builds use canonical paths; their exact old bytes remain archival.
    if relative in {"vite.ldraw-v2.config.ts", "package.json"}:
        return "tem/repository-layout-20260924/original/" + relative
    if relative.startswith("dist-ldraw-v2/"):
        return "tem/repository-layout-20260924/original/" + relative
    return relocated(relative)
