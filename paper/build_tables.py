#!/usr/bin/env python3
"""Build publication assets and genuinely blank, schema-bound experiment tables."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEGACY = ROOT / "tem/papers/legacy-tree/evidence-v4-draft"
BUDGET = ROOT / "benchmark/experiment-plans/model-budget-20260920/config.json"
CONFIG = HERE / "experiments.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def proposed():
    budget = json.loads(BUDGET.read_text())
    models = []
    for item in budget["api_models"] + budget["local_models"]:
        api = "api_id" in item
        visual = item.get("track", "vlm") == "vlm"
        models.append({
            "id": item["id"], "name": item["name"],
            "category": "Proprietary VLM" if api else "Open-weight VLM" if visual else "Open-weight text LM",
            "modality": "Image + text" if visual else "Text only",
            "planned_identifier": item.get("api_id", item.get("repo")),
            "tracks": ["visual", "no-image", "graph"] if visual else ["graph"],
            "status": "proposed-unfrozen",
        })
    vlms = [m for m in models if "visual" in m["tracks"]]
    def rows(items, metrics):
        return [{"id": m["id"], "label": m["name"],
                 "results": {key: None for key in metrics}} for m in items]
    tables = {
        "visual": rows(vlms, ["color_A", "color_New", "color_Both", "type_A", "type_New", "type_Both"]),
        "diagnostics": rows(vlms, ["color_adaptation", "color_retention", "color_valid_both",
                                  "type_adaptation", "type_retention", "type_valid_both"]),
        "controls": rows(vlms, ["color_noimage_Both", "type_noimage_Both", "panel_accuracy",
                               "color_QA_minus_full", "type_QA_minus_full"]),
        "graph": rows(models, ["strong_change_Both", "degree_visible_change_Both",
                              "strong_invariance_Both", "degree_visible_invariance_Both", "valid_observations"]),
        "modes": rows([{"id": "qwen27-mode", "name": "Qwen3.5-27B: thinking on minus off"},
                       {"id": "gemini-pro-mode", "name": "Gemini 3.1 Pro: higher minus lower effort"}],
                      ["color_Both_delta", "type_Both_delta", "graph_strong_Both_delta",
                       "billed_output_tokens", "cost_usd"]),
    }
    return {
        "schema": 1, "status": "experiment-plan-no-model-results",
        "model_snapshot_date": budget["price_checked_date"],
        "model_source": str(BUDGET.relative_to(ROOT)), "model_source_sha256": digest(BUDGET),
        "dataset": "brickatlas-display-v3",
        "study_boundary": "New 15-model proposal; does not replace the sealed v3 three-model roster.",
        "result_policy": "All pending results are null and render as empty cells, never zero or fabricated scores.",
        "aggregation": "Visual families separate; equal-source primary, micro and source intervals companion outputs.",
        "required_before_collection": [
            "Freeze selected IDs, QA lineage, models, provider revisions and precision.",
            "Implement and validate new provider adapters and subset QA gate.",
            "Freeze repeat count, image policy, output/effort budget, failures and inclusion rules.",
        ],
        "models": models, "tables": tables,
    }


def tex(text):
    return text.replace("&", r"\&").replace("_", r"\_")


def table(headers, rows, spec=None):
    spec = spec or "l" + "r" * (len(headers) - 1)
    return "\n".join([
        r"\begin{tabular}{@{}" + spec + r"@{}}", r"\toprule",
        " & ".join(headers) + r"\\", r"\midrule",
        *[" & ".join(row) + r"\\" for row in rows],
        r"\bottomrule", r"\end{tabular}", "",
    ])


def build():
    if not CONFIG.exists():
        CONFIG.write_text(json.dumps(proposed(), indent=2) + "\n")
    config = json.loads(CONFIG.read_text())
    expected = proposed()
    assert config == expected, "Proposal/schema changed: update deliberately before regeneration."
    generated = HERE / "generated"
    generated.mkdir(exist_ok=True)
    inventory = [[tex(m["name"]), tex(m["category"]),
                  "Visual / no-image / graph" if "visual" in m["tracks"] else "Graph"]
                 for m in config["models"]]
    (generated / "models.tex").write_text(table(["Model", "Model class", "Planned inputs"], inventory, "lll"))
    headers = {
        "visual": ["Model", r"\shortstack{Color\\A}", r"\shortstack{Color\\New}", r"\shortstack{Color\\Both}",
                   r"\shortstack{Part-type\\A}", r"\shortstack{Part-type\\New}", r"\shortstack{Part-type\\Both}"],
        "diagnostics": ["Model", r"\shortstack{Color\\Adapt.}", r"\shortstack{Color\\Old}", r"\shortstack{Color\\Valid}",
                        r"\shortstack{Part-type\\Adapt.}", r"\shortstack{Part-type\\Old}", r"\shortstack{Part-type\\Valid}"],
        "controls": ["Model", r"\shortstack{No-image\\Color Both}", r"\shortstack{No-image\\Type Both}",
                     r"\shortstack{Panel\\accuracy}", r"\shortstack{Color\\QA--full}", r"\shortstack{Type\\QA--full}"],
        "graph": ["Model", r"\shortstack{Strong\\change}", r"\shortstack{Degree-visible\\change}",
                  r"\shortstack{Strong\\invariance}", r"\shortstack{Degree-visible\\invariance}",
                  r"\shortstack{Format\\valid}"],
        "modes": ["Configuration contrast", r"$\Delta$ Color", r"$\Delta$ Type", r"$\Delta$ Strong",
                  r"\shortstack{Output\\tokens}", "USD"],
    }
    for key, data in config["tables"].items():
        values = [[tex(row["label"])] + ["" for value in row["results"].values()] for row in data]
        assert all(v is None for row in data for v in row["results"].values())
        (generated / f"{key}.tex").write_text(table(headers[key], values))
    copies = ["cvpr.sty", "ieeenat_fullname.bst", "references.bib",
              "figure-provenance.json", "figures/paired-observations.pdf",
              "figures/given-order-replay.pdf", "figures/position-control.png",
              "generated/sources.tex", "generated/scale.tex", "generated/transitions-color.tex",
              "generated/transitions-type.tex", "generated/shortcuts-type.tex",
              "generated/authors.tex", "generated/overlap.tex", "generated/strong-pairs.tex",
              "generated/graph-main.tex", "generated/graph-invariance.tex", "generated/families.tex"]
    provenance = []
    for relative in copies:
        source, target = LEGACY / relative, HERE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        provenance.append({"source": str(source.relative_to(ROOT)), "target": relative, "sha256": digest(target)})
    (HERE / "asset-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    count = sum(len(row["results"]) for data in config["tables"].values() for row in data)
    print(f"Generated {len(config['models'])} proposed models; {count} empty result cells.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    build()
