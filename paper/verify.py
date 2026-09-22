#!/usr/bin/env python3
"""Verify current task version, empty empirical cells, figure lineage and CVPR length."""
import hashlib
import json
from pathlib import Path
import re

import fitz
from build_tables import proposed

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "benchmark/visual-repair-v1"


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_records(value):
    if isinstance(value, dict):
        if "sha256" in value and ("file" in value or "path" in value):
            path = ROOT / value.get("file", value.get("path"))
            assert sha(path) == value["sha256"], path
        for child in value.values():
            check_records(child)
    elif isinstance(value, list):
        for child in value:
            check_records(child)


def main():
    config = load(HERE / "experiments.json")
    assert config == proposed() and config["dataset"] == "visual-repair-v1"
    assert len(config["models"]) == 15
    expected_blank_cells = 13 * 6 + 13 * 5 + 13 * 5 + 2 * 2
    actual_blank_cells = 0
    for name, rows in config["tables"].items():
        text = (HERE / "generated" / f"{name}.tex").read_text()
        lines = text.splitlines()
        for row in rows:
            assert all(v is None for v in row["results"].values())
            rendered = next(line for line in lines if line.startswith(row["label"]))
            columns = rendered.removesuffix(r"\\").split("&")
            assert len(columns) == len(row["results"]) + 1 and all(not c.strip() for c in columns[1:])
            actual_blank_cells += len(row["results"])
    assert actual_blank_cells == expected_blank_cells
    for asset in load(HERE / "asset-provenance.json"):
        assert sha(HERE / asset["target"]) == asset["sha256"]
        assert sha(ROOT / asset["source"]) == asset["sha256"]
    provenance = load(HERE / "repair-figure-provenance.json")
    assert provenance["version"] == "visual-repair-v1" and provenance["model_or_human_results"] is None
    check_records(provenance)
    assert {f["figure"] for f in provenance["figures"]} == {"repair-task", "repair-factorial", "source-atlas"}
    public = {t["id"]: t for t in load(DATA / "public.json")["tasks"]}
    gold = {t["id"]: t["answer"] for t in load(DATA / "gold.json")["tasks"]}
    assert public[provenance["example"]]["split"] == "dev"
    def canonical(answer):
        return {**answer, "solutions": sorted([
            {"restored": sorted(s["restored"]), "component_sizes": sorted(s["component_sizes"], reverse=True)}
            for s in answer["solutions"]], key=lambda s: s["restored"])}
    assert provenance["gt"] == canonical(gold[provenance["example"]])
    assert provenance["native_packet"]["input"] == public[provenance["example"]]["input"]
    for figure in provenance["figures"]:
        assert figure["model_responses"] is None
        pdf = fitz.open(HERE / "figures" / f"{figure['figure']}.pdf")
        assert len(pdf) == 1
        assert not re.search(r"[\u4e00-\u9fff]", pdf[0].get_text())
        if "tasks" in figure:
            for task in figure["tasks"]:
                assert public[task["id"]] == task
                assert figure["answers"][task["id"]] == canonical(gold[task["id"]])
    audit = load(DATA / "dependency-audit.json")
    summary = load(DATA / "summary.json")
    assert audit["status"] == "passed"
    assert audit["independent_semantic_answers"] == len(public) == summary["observation_count"]
    # Each native image pair is reused across the two structural conditions.
    assert audit["image_pairs_checked"] * 2 == summary["visual_changing_pairs"] + summary["visual_preserving_pairs"]
    check_records(audit["inputs"])
    baseline = load(DATA / "baseline-report.json")
    assert baseline["kind"] == "algorithmic-not-model-or-human"
    assert baseline["model_results"] is None and baseline["human_results"] is None
    assert baseline["analysis_schema"] == config["interface_contract"]["analysis_schema"]
    assert baseline["analysis_sets"]["full"]["task_count"] == len(public)
    for interface in baseline["interface"]:
        for subset in ("full", "qualified"):
            for split in ("dev", "heldout", "all"):
                stats = interface[subset][split]
                assert set(stats["contingency"]) == {f"{i:03b}" for i in range(8)}
                assert sum(stats["contingency"].values()) == stats["planned_count"]
                for path in config["interface_contract"]["table_fields"].values():
                    value = stats
                    for key in path.split("."):
                        value = value[key]
                joint = stats["joint_failure_given_atomic_oracle"]
                assert joint["failure_n"] == stats["contingency"]["110"]
                assert joint["eligible_n"] == sum(stats["contingency"][k] for k in ("110", "111"))
                if not joint["eligible_n"]:
                    assert joint["micro"] is None and joint["group_macro"] is None
    documents = {}
    bibkeys = set(re.findall(r"@\w+\{([^,]+),", (HERE / "references.bib").read_text()))
    for stem in ["main", "supplement"]:
        source = (HERE / f"{stem}.tex").read_text()
        assert not re.search(r"[\u4e00-\u9fff]", source)
        cited = {key for group in re.findall(r"\\cite\{([^}]+)\}", source) for key in group.split(",")}
        assert cited <= bibkeys
        for graphics in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", source):
            assert (HERE / graphics).exists(), graphics
        for included in re.findall(r"\\input\{([^}]+)\}", source):
            assert (HERE / included).exists(), included
        log = (HERE / f"{stem}.log").read_text()
        assert not re.search(r"Overfull \\[hv]box", log), f"{stem}: overfull box"
        assert "There were undefined" not in log and "Rerun to get cross-references right" not in log
        doc = fitz.open(HERE / f"{stem}.pdf")
        texts = [page.get_text() for page in doc]
        text = "\n".join(texts)
        assert not re.search(r"[\u4e00-\u9fff]", text)
        content_pages = len(doc)
        if stem == "main":
            reference_page = next(i for i, value in enumerate(texts) if "\nReferences\n" in value)
            content_pages = reference_page
            assert content_pages <= 8, f"CVPR content length {content_pages} exceeds 8 pages"
            assert "color-question-gt" not in source and "complex-repair" not in source
            for phrase in ["GPT-6 Astra", "Qwen3.5-27B", "DeepSeek-R1",
                           "minimum", "Factorial", "Oracle", "V-change", "All-six"]:
                assert phrase in text, phrase
            assert len(doc[0].get_images()) + sum(len(p.get_images()) for p in doc) > 0
        documents[stem] = {"pages": len(doc), "content_pages": content_pages,
                           "sha256": sha(HERE / f"{stem}.pdf"), "text_characters": len(text),
                           "figure_count": len(re.findall(r"\\includegraphics", source))}
    result = {"status": "passed", "version": "visual-repair-v1", "model_count": 15,
              "vlm_count": 13, "text_only_count": 2, "empty_result_cells": actual_blank_cells,
              "documents": documents, "primary_constructions": summary["construction_count"],
              "primary_observations": len(public), "image_pairs_verified": audit["image_pairs_checked"],
              "human_or_model_collection_performed": False}
    (HERE / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
