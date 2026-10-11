"""Official OMR metadata snapshots. No geometry parsing or source selection tests."""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone
from source_state import source_state

ROOT = Path(__file__).resolve().parents[3]
HERE = source_state(ROOT)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f"Refusing overwrite: {path}")
    else:
        with path.open("xb") as stream:
            stream.write(data)


def save_json(path, value):
    write_new(path, (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode())


def fetch(url, name):
    target = HERE / "snapshots" / name
    if target.exists():
        return target.read_bytes()
    for attempt in range(4):
        try:
            data = subprocess.check_output(
                ["curl", "--compressed", "-fLsS", "--connect-timeout", "10",
                 "--max-time", "60", url], timeout=65
            )
            break
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            if attempt == 3:
                raise
    if not data:
        raise ValueError(f"Empty response: {url}")
    write_new(target, data)
    save_json(target.with_suffix(".fetch.json"), {
        "url": url, "sha256": digest(data), "bytes": len(data),
        "retrievedAt": datetime.now(timezone.utc).isoformat(),
    })
    return data


class Node:
    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs or []), parent
        self.children = []

    def text(self):
        return " ".join(" ".join(c.text() if isinstance(c, Node) else c
                               for c in self.children).split())

    def all(self, tag):
        for child in self.children:
            if isinstance(child, Node):
                if child.tag == tag:
                    yield child
                yield from child.all(tag)


class Document(HTMLParser):
    def __init__(self, data):
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.current = self.root
        self.feed(data.decode("utf-8"))

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.current)
        self.current.children.append(node)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img",
                       "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.current.children.append(Node(tag, attrs, self.current))

    def handle_endtag(self, tag):
        node = self.current
        while node.parent is not None:
            if node.tag == tag:
                self.current = node.parent
                return
            node = node.parent

    def handle_data(self, data):
        self.current.children.append(data)


def index_page(page):
    url = f"https://library.ldraw.org/omr/sets?page={page}"
    raw = fetch(url, f"index-{page:02d}.html")
    doc = Document(raw).root
    rows = []
    for row in doc.all("tr"):
        cells = list(row.all("td"))
        if len(cells) != 6:
            continue
        texts = [cell.text() for cell in cells]
        if not re.fullmatch(r"\d+-\d+", texts[1]):
            continue
        links = [a.attrs["href"] for a in cells[1].all("a")]
        rows.append(dict(zip(
            ("setNumber", "title", "theme", "year", "modelCount"), texts[1:]
        ), sourceUrl=links[0], indexPage=page, indexSha256=digest(raw)))
    if not rows:
        raise ValueError(f"No rows on {url}")
    save_json(HERE / "index" / f"{page:02d}.json", rows)
    print(f"page={page} rows={len(rows)} first={rows[0]['setNumber']}", flush=True)


def details(row):
    token = row["sourceUrl"].rsplit("/", 1)[1]
    raw = fetch(row["sourceUrl"], f"set-{token}.html")
    doc = Document(raw).root
    models = []
    for anchor in doc.all("a"):
        url = anchor.attrs.get("href", "")
        if not url.startswith("https://library.ldraw.org/library/omr/"):
            continue
        node = anchor.parent
        while node.parent and not all(s in node.text() for s in (
                "Author:", "Missing Parts", "Missing Patterns", "Missing Stickers")):
            node = node.parent
        text = node.text()
        author = re.search(r"Author:\s*(.*?)\s*Missing Parts", text)
        flags = {key: (re.search(key + r"\s*(Yes|No)", text).group(1)
                       if re.search(key + r"\s*(Yes|No)", text) else None)
                 for key in ("Missing Parts", "Missing Patterns", "Missing Stickers")}
        models.append({
            "downloadUrl": url, "pageAuthor": author.group(1) if author else None,
            "pageModelLabel": text.split("Author:")[0].strip(),
            "completeness": flags, "pageModelText": text,
        })
    if not models:
        raise ValueError(f"No downloads: {row['sourceUrl']}")
    return {**row, "pageSha256": digest(raw), "models": models}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("index", "show", "details", "prepare", "freeze"))
    parser.add_argument("--pages", default="1:59")
    parser.add_argument("--range", default="1:100")
    args = parser.parse_args()
    if args.action == "index":
        start, end = map(int, args.pages.split(":"))
        for page in range(start, end + 1):
            index_page(page)
        return
    rows = [row for path in sorted((HERE / "index").glob("*.json"))
            for row in json.loads(path.read_text())]
    if len({r["setNumber"] for r in rows}) != len(rows):
        raise ValueError("Repeated index rows: pagination not reliable")
    if args.action == "show":
        for row in rows:
            if re.search(r"Creator|Town|City|Architecture|Ideas|Advanced", row["theme"]):
                print(row["setNumber"], row["title"], "|", row["theme"],
                      "|", row["sourceUrl"])
        return
    selection = json.loads((HERE / "selection.json").read_text())
    by_set = {r["setNumber"]: r for r in rows}
    if args.action in ("details", "prepare"):
        start, end = map(int, args.range.split(":"))
        selected = [(group, n) for group, numbers in selection["groups"].items()
                    for n in numbers]
        for group, number in selected[start - 1:end]:
            row = by_set[f"{number}-1"]
            save_json(HERE / "details" / f"{number}.json", details(row))
            print(f"details {number} {group}", flush=True)
        if args.action == "prepare":
            subprocess.run([
                str(ROOT / ".tools/node-v22.23.2-darwin-arm64/bin/node"),
                "--import", "tsx", str(Path(__file__).with_name("intake.ts")), f"--range={args.range}"
            ], cwd=ROOT, check=True)
        return
    previous = []
    for path in sorted((ROOT / "web/public/models").glob("*/manifest.json")):
        if path.parent.name.startswith("v23-"):
            continue
        manifest = json.loads(path.read_text())
        matches = re.findall(r"\d{4,7}", path.parent.name)
        previous.append({"modelId": path.parent.name, "kit": matches[0] if matches else None,
                         "sha256": digest(path.read_bytes()),
                         "sourceHash": manifest.get("sourceHash")})
    excluded = {r["kit"] for r in previous}
    candidates = []
    for group, numbers in selection["groups"].items():
        for number in numbers:
            number = str(number)
            if number in excluded:
                raise ValueError(f"Already existing kit: {number}")
            candidates.append({
                **by_set[f"{number}-1"], "id": f"v23-{number}", "kit": number,
                "independenceGroup": number, "intakeStratum": group,
                "sourceSelectionRule": "Main Model if labeled; else lexicographic original URL",
                "sourceHash": None, "geometryQualification": None,
            })
    assert 60 <= len(candidates) <= 100
    assert len({r["kit"] for r in candidates}) == len(candidates)
    registry = {
        "schema": "brickplan-v23-candidates/1.0",
        "frozenAt": datetime.now(timezone.utc).isoformat(),
        "freezeStage": "Kit identities and source plan, before original downloads",
        "provenanceEnrichment": "Separate per-kit details and intake records; registry never rewritten",
        "geometryOrPolicySelectionPerformed": False,
        "selection": selection, "previousModels": previous,
        "candidates": candidates, "count": len(candidates),
        "independenceUnit": "Distinct kit number; alternatives/submodels never counted separately",
        "qualificationStatus": "Not run. All frozen failures remain in denominator.",
    }
    save_json(HERE / "candidate-registry.frozen.json", registry)
    data = (HERE / "candidate-registry.frozen.json").read_bytes()
    write_new(HERE / "candidate-registry.frozen.sha256",
              (digest(data) + "  candidate-registry.frozen.json\n").encode())
    print(f"FROZEN {len(candidates)} kits sha256={digest(data)}", flush=True)


if __name__ == "__main__":
    main()
