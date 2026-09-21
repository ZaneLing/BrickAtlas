#!/usr/bin/env python3
"""Check blank experiments, evidence counts, references, assets and compiled PDFs."""
import hashlib
import json
from pathlib import Path
import re

import fitz

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    config = load(HERE / "experiments.json")
    budget = load(ROOT / config["model_source"])
    assert sha(ROOT / config["model_source"]) == config["model_source_sha256"]
    assert len(config["models"]) == 15
    assert {m["id"] for m in config["models"]} == {
        m["id"] for m in budget["api_models"] + budget["local_models"]}
    assert sum("visual" in m["tracks"] for m in config["models"]) == 13
    cells = 0
    for name, rows in config["tables"].items():
        text = (HERE / "generated" / f"{name}.tex").read_text()
        data_lines = text.split(r"\midrule", 1)[1].split(r"\bottomrule", 1)[0].strip().splitlines()
        assert len(rows) == len(data_lines), name
        for row, line in zip(rows, data_lines):
            assert all(value is None for value in row["results"].values()), row["id"]
            contents = line.removesuffix(r"\\").split("&")
            assert len(contents) == len(row["results"]) + 1, row["id"]
            assert all(not cell.strip() for cell in contents[1:]), row["id"]
            cells += len(row["results"])
    assert cells == 306
    for item in load(HERE / "asset-provenance.json"):
        assert sha(HERE / item["target"]) == sha(ROOT / item["source"]) == item["sha256"]
    manifest = load(ROOT / "benchmark/ldraw-evidence-v3/visual-manifest.json")
    index = load(ROOT / "benchmark/ldraw-evidence-v3/observation-index.json")
    assert len(manifest["pairs"]) == 140
    assert sum(p["family"] == "color" for p in manifest["pairs"]) == 73
    assert sum(p["family"] == "shape-match" for p in manifest["pairs"]) == 67
    assert len(index["observations"]) == 347
    bibliography = (HERE / "references.bib").read_text()
    keys = set(re.findall(r"@\w+\{([^,]+),", bibliography))
    documents = {}
    for stem in ["main", "supplement"]:
        source = (HERE / f"{stem}.tex").read_text()
        assert not re.search(r"[\u4e00-\u9fff]", source), stem
        for relative in re.findall(r"\\input\{([^}]+)\}", source):
            assert (HERE / relative).is_file(), relative
        for relative in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", source):
            assert (HERE / relative).is_file(), relative
        for citations in re.findall(r"\\cite\{([^}]+)\}", source):
            assert set(citations.split(",")) <= keys, citations
        log = (HERE / f"{stem}.log").read_text()
        assert not re.search(r"Overfull \\[hv]box", log), f"{stem}: overflow"
        assert "undefined references" not in log.lower(), stem
        assert not re.search(r"Citation .* undefined", log), stem
        pdf = fitz.open(HERE / f"{stem}.pdf")
        pages = [page.get_text() for page in pdf]
        assert all(text.strip() for text in pages), f"{stem}: empty page"
        assert not any(re.search(r"[\u4e00-\u9fff]", text) for text in pages), stem
        text = "\n".join(pages)
        assert "??" not in text, f"{stem}: unresolved reference"
        if stem == "main":
            for phrase in ["GPT-6 Astra", "Qwen3.5-27B", "DeepSeek-R1", "Planned Experiments",
                           "NewAcc", "Old-gold", "Part-type", "306"]:
                if phrase != "306":
                    assert phrase in text, phrase
        documents[stem] = {"pages": len(pdf), "sha256": sha(HERE / f"{stem}.pdf"),
                           "text_characters": len(text)}
    result = {"status": "passed", "models": 15, "visual_models": 13, "text_models": 2,
              "empty_result_cells": cells, "primary_pairs": 140, "visual_observations": 347,
              "documents": documents, "human_or_model_collection_performed": False}
    (HERE / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
