#!/usr/bin/env python3
"""Draft manuscript inputs from sealed evidence; no old generator is executed."""
import argparse
from pathlib import Path
import re
import shutil

from baseline import ROOT, WORK, PAPER, BASE, VERSION, checked, load, save, sha


def compiled_keys(bbl):
    """Read BibTeX-emitted bibitem keys after the TeX/BibTeX compilation."""
    return re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}", bbl)


def generate():
    inputs = load(PAPER / "inputs/source-inputs.json")
    for row in inputs:
        assert sha(ROOT / row["file"]) == row["sha256"]
    base = PAPER / "base-references.bib"
    additions = PAPER / "additions.bib"
    output = PAPER / "references.bib"
    text = base.read_text() + "\n" + additions.read_text()
    # One-way composition; never use references.bib as its own input.
    output.write_text(text)
    first = output.read_bytes()
    output.write_text(base.read_text() + "\n" + additions.read_text())
    assert output.read_bytes() == first
    replay = PAPER / "inputs/given-order-replay.pdf"
    shutil.copyfile(replay, PAPER / "figures/given-order-replay.pdf")
    old = checked(ROOT / "benchmark/paper/evidence-v3/publication-provenance.json")
    for path, digest in old["inputs"].items():
        assert sha(ROOT / path) == digest
    for path in (ROOT / "benchmark/paper/evidence-v3/generated").glob("*.tex"):
        assert sha(PAPER / "generated" / path.name) == sha(path)
    prior_keys = compiled_keys((ROOT / "benchmark/paper/evidence-v3/main.bbl").read_text())
    assert len(prior_keys) == 13 and len(set(prior_keys)) == 13
    measurement_inputs = {}
    if (WORK / "work/phase-2-machine-validation.json").exists():
        audit = load(WORK / "work/phase-2-machine-validation.json")
        assert audit["machine_status"] == "passed"
        for name, expected in audit["outputs"].items():
            assert sha(WORK / name) == expected
            measurement_inputs[str((WORK / name).relative_to(ROOT))] = expected
        for name, expected in audit["code_hashes"].items():
            assert sha(Path(__file__).with_name(name)) == expected
        color = load(WORK / "single-image-color-baseline.json")
        macros = {
            "EvColorBaselineCorrect": str(color["endpoint_correct"]),
            "EvColorBaselineAbstentions": str(color["abstentions"]),
            "EvColorBaselineBothHits": str(sum(r["Both"] for r in color["per_pair"])),
            "EvColorBaselineBothMicro": f'{100*color["metrics"]["Both"]["micro"]:.2f}',
            "EvColorBaselineBothSource": f'{100*color["metrics"]["Both"]["source_macro"]:.2f}',
        }
        (PAPER / "generated/measurement-audit.tex").write_text(
            "% Generated from the complete legal single-image baseline audit.\n" +
            "".join(f"\\newcommand{{\\{key}}}{{{value}}}\n" for key, value in macros.items()))
        measurement_inputs[str((WORK / "work/single-image-baseline-lock.json").relative_to(ROOT))] = sha(
            WORK / "work/single-image-baseline-lock.json")
    save(PAPER / "publication-provenance.json", {
        "analysis_version": VERSION, "stimulus_dataset": "brickatlas-display-v3",
        "evidence_kind": "draft-manuscript-over-sealed-baseline",
        "inputs": {**old["inputs"], **measurement_inputs, **{str(p.relative_to(ROOT)): sha(p) for p in [
            base, additions, replay, WORK / "work/literature/visualflip-v1.html"]}},
        "generated_tables": "Retained v3 tables plus derived Phase-2 algorithm audit macros; no learned-model values inserted.",
        "bibliography": {"prior_compiled_keys": prior_keys,
                         "added_keys": ["zhu2026visualflip"],
                         "expected_cited_keys": sorted(prior_keys + ["zhu2026visualflip"]),
                         "composition": "base-references.bib + newline + additions.bib",
                         "idempotence_checked": True},
        "real_model_results": 0, "genuine_human_reviews": 0
    })
    provenance = load(PAPER / "figure-provenance.json")
    for row in provenance:
        if row["figure"] == "given-order-replay":
            row["file"] = str(replay.relative_to(ROOT))
            row["source_origin"] = "benchmark/paper/evidence-v1/figures/given-order-replay.pdf"
            row["sha256"] = sha(replay)
    save(PAPER / "figure-provenance.json", provenance)
    save(WORK / "work/phase-1-generation.json", {
        "status": "passed", "reference_sha256": sha(output), "idempotent": True,
        "expected_citations": 14, "old_release_writes": 0,
        "remaining_reproduction_scope": "Full offline-wire and asset recovery still require Phase 7 validation."
    })
    print({"status": "generated", "draft": VERSION, "expected_citations": 14, "idempotent_bibliography": True})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.parse_args()
    generate()
