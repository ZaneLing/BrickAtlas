"""Reconcile the frozen plan with cached official HTML and original MPD headers."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlparse
from source_state import source_state

ROOT = Path(__file__).resolve().parents[3]
STATE = source_state(ROOT)
OUT = Path(os.environ.get("SOURCE_INTAKE_OUTPUT", "/tmp/brickplan-v23-work/source-intake"))
OUT.mkdir(parents=True, exist_ok=True)
EXPECTED = "3518c3357872225b0425ee6bcd2a0aa8350aca0791d7b83dd056d5baec081f0b"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text())


def author_key(text):
    text = re.sub(r"\s*\[.*\]\s*$", "", text)
    return "".join(c for c in unicodedata.normalize("NFKD", text)
                   if not unicodedata.combining(c)).strip().lower()


spec = importlib.util.spec_from_file_location("intake_discover", Path(__file__).with_name("discover.py"))
discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discovery)
registry = load(STATE / "candidate-registry.frozen.json")
assert sha((STATE / "candidate-registry.frozen.json").read_bytes()) == EXPECTED
records = []
for candidate in registry["candidates"]:
    record = {"id": candidate["id"], "kit": candidate["kit"],
              "setNumber": candidate["setNumber"], "title": candidate["title"],
              "sourceUrl": candidate["sourceUrl"], "issues": []}
    try:
        index_path = STATE / "snapshots" / f'index-{candidate["indexPage"]:02d}.html'
        index_bytes = index_path.read_bytes()
        assert sha(index_bytes) == candidate["indexSha256"], "Index snapshot hash"
        index_doc = discovery.Document(index_bytes).root
        matching = []
        for row in index_doc.all("tr"):
            cells = list(row.all("td"))
            if len(cells) == 6 and cells[1].text() == candidate["setNumber"]:
                matching.append(cells)
        assert len(matching) == 1, "Unique official index identity"
        cells = matching[0]
        for key, cell in zip(("setNumber", "title", "theme", "year", "modelCount"), cells[1:]):
            assert str(candidate[key]) == cell.text(), f"Index field mismatch: {key}"
        assert candidate["sourceUrl"] in [a.attrs.get("href") for a in cells[1].all("a")]
        saved = load(STATE / "details" / f'{candidate["kit"]}.json')
        token = candidate["sourceUrl"].rsplit("/", 1)[1]
        page_path = STATE / "snapshots" / f"set-{token}.html"
        page_bytes = page_path.read_bytes()
        assert sha(page_bytes) == saved["pageSha256"], "Detail snapshot hash"
        page_text = discovery.Document(page_bytes).root.text()
        assert candidate["setNumber"] in page_text and candidate["title"] in page_text
        reparsed = discovery.details(candidate)
        assert reparsed["models"] == saved["models"], "Saved model metadata differs from official HTML"
        chosen = next((m for m in saved["models"] if m["pageModelLabel"] == "Main Model"),
                      sorted(saved["models"], key=lambda m: m["downloadUrl"])[0])
        parsed_url = urlparse(chosen["downloadUrl"])
        assert parsed_url.scheme == "https" and parsed_url.netloc == "library.ldraw.org"
        assert parsed_url.path.startswith("/library/omr/")
        filename = unquote(parsed_url.path.rsplit("/", 1)[1])
        assert filename.startswith(candidate["setNumber"]), "Download filename identity"
        assert chosen["pageAuthor"], "Missing official page author"
        snapshot_records = []
        for snapshot in (index_path, page_path):
            fetch = load(snapshot.with_suffix(".fetch.json"))
            assert fetch["sha256"] == sha(snapshot.read_bytes())
            expected_url = (candidate["sourceUrl"] if snapshot == page_path else
                            f'https://library.ldraw.org/omr/sets?page={candidate["indexPage"]}')
            assert fetch["url"] == expected_url, "Snapshot fetch URL"
            snapshot_records.append({**fetch, "path": str(snapshot.relative_to(ROOT))})
        record.update(downloadUrl=chosen["downloadUrl"], pageAuthor=chosen["pageAuthor"],
                      selectedModelLabel=chosen["pageModelLabel"],
                      selectionRuleVerified=True, completeness=chosen["completeness"],
                      snapshotEvidence=snapshot_records, catalogIdentityStatus="pass")
        original_path = ROOT / "assets-source/brickplan-v23/original" / filename
        result = load(STATE / "results" / f'{candidate["id"]}.json')
        record["intakeStatus"] = result["status"]
        record["intakeError"] = result.get("error")
        if not original_path.exists():
            assert result["status"] == "intake-failed"
            record.update(status="original-unavailable", originalIdentityStatus="not-run")
        else:
            original = original_path.read_bytes()
            assert sha(original) == result["sourceHash"]
            text = original.decode("utf-8")
            assert text.encode("utf-8") == original
            sections = list(re.finditer(r"(?im)^0 FILE (.+)\r?$", text))
            root_name = sections[0][1].strip().replace("\\", "/").lower() if sections else filename.lower()
            root_text = text[sections[0].end():sections[1].start()
                             if len(sections) > 1 else len(text)] if sections else text
            root_identity_matches = bool(re.match(rf'^{candidate["kit"]}[ ._-]', root_name))
            author = re.search(r"(?im)^0 Author:\s*(.+)$", root_text)[1].strip()
            license_text = re.search(r"(?im)^0 !LICENSE\s+(.+)$", root_text)[1].strip()
            assert re.search(r"CC BY (2\.0|4\.0)|CCAL version 2\.0|CC0", license_text)
            history = re.findall(r"(?im)^0 !HISTORY.*$", root_text)
            attribution = ("exact-match" if author == chosen["pageAuthor"] else
                           "normalized-display-name" if author_key(author) == author_key(chosen["pageAuthor"]) else
                           "original-author-and-history-contributor" if any(chosen["pageAuthor"] in h for h in history)
                           else "unresolved")
            assert attribution != "unresolved", "Unexplained page/header author mismatch"
            record.update(status="pass", originalIdentityStatus="pass",
                          originalPath=str(original_path.relative_to(ROOT)), originalSha256=sha(original),
                          originalBytes=len(original), rootFile=root_name, sourceAuthor=author,
                          sourceLicense=license_text, authorAttribution=attribution, sourceHistory=history,
                          embeddedDefinitionCount=len(sections), rootNameMatchesKit=root_identity_matches)
            if not root_identity_matches:
                record.update(status="catalog-verified-root-name-conflict", originalIdentityStatus="conflict")
                record["issues"].append(
                    f"Official set/download identify {candidate['setNumber']}, but original root is {root_name}; no correction made.")
                record["embeddedSectionNames"] = [section[1].strip() for section in sections]
            if result["status"] == "intake-failed":
                record["status"] = "root-identity-verified-intake-excluded"
                record["issues"].append(result["error"])
            else:
                manifest_bytes = (ROOT / result["manifestFile"]).read_bytes()
                assert sha(manifest_bytes) == result["manifestSha256"]
                manifest = json.loads(manifest_bytes)
                expected_model = {
                    "id": candidate["id"], "setNumber": candidate["setNumber"],
                    "title": candidate["title"], "theme": candidate["theme"],
                    "year": int(candidate["year"]), "author": author, "license": license_text,
                    "sourceUrl": candidate["sourceUrl"], "downloadUrl": chosen["downloadUrl"],
                }
                for key, value in expected_model.items():
                    assert manifest["model"][key] == value, f"Manifest metadata mismatch: {key}"
                provenance_path = ROOT / "web/public/models" / candidate["id"] / "provenance.json"
                provenance_bytes = provenance_path.read_bytes()
                assert sha(provenance_bytes) == result["provenanceSha256"]
                provenance = json.loads(provenance_bytes)
                assert provenance["model"] == manifest["model"]
                assert provenance["page"]["url"] == candidate["sourceUrl"]
                assert provenance["page"]["sha256"] == saved["pageSha256"]
                assert provenance["page"]["author"] == chosen["pageAuthor"]
                assert provenance["model"]["author"] == author
                record.update(manifestMetadataStatus="pass", manifestSha256=sha(manifest_bytes),
                              manifestMetadataFieldsChecked=list(expected_model),
                              provenanceSha256=sha(provenance_bytes))
    except Exception as exc:
        record["status"] = "failed"
        record["issues"].append(str(exc))
    records.append(record)

report = {
    "schema": "brickplan-source-identity-verification/1.0",
    "candidateRegistrySha256": EXPECTED,
    "method": "Reparse hash-verified official index/detail HTML, fetch URL records and original UTF-8 MPD headers.",
    "evidenceScope": "Official OMR publication identity, not LEGO endorsement or verified real-person identity.",
    "crossValidation": "Compares catalog index, detail page and MPD within one publisher; conflicts are explicit, not three independent publishers.",
    "freshness": "Uses preserved retrieval timestamps; successful originals were not downloaded again.",
    "records": records,
}
(OUT / "identity-verification.json").write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n")
print(json.dumps({status: sum(r["status"] == status for r in records)
                  for status in sorted({r["status"] for r in records})}, indent=2))
assert not any(r["status"] == "failed" for r in records)
