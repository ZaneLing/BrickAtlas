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
            "tracks": ["multimodal", "no_image", "oracle_binding", "atomic_binding"] if visual else ["no_image", "oracle_binding"],
            "status": "proposed-unfrozen",
        })
    vlms = [m for m in models if "multimodal" in m["tracks"]]
    def rows(items, metrics):
        return [{"id": m["id"], "label": m["name"],
                 "results": {key: None for key in metrics}} for m in items]
    tables = {
        "repair-primary": rows(vlms, ["repair_exact", "binding_accuracy", "changing_both_correct",
                                      "preserving_both_correct", "structural_both_correct", "factorial_all_correct"]),
        "repair-decomposition": rows(vlms, ["atomic_binding", "no_image_repair", "oracle_binding_repair",
                                            "repair_given_binding", "invalid_rate"]),
        "repair-interface": rows(vlms, ["joint_failure", "joint_eligible_observations",
                                      "joint_eligible_groups", "multimodal_minus_oracle_repair",
                                      "multimodal_minus_atomic_binding"]),
        "repair-text": rows([m for m in models if m not in vlms], ["no_image_repair", "oracle_binding_repair"]),
    }
    return {
        "schema": 3, "status": "experiment-plan-no-model-results",
        "model_snapshot_date": budget["price_checked_date"],
        "model_source": str(BUDGET.relative_to(ROOT)), "model_source_sha256": digest(BUDGET),
        "dataset": "visual-repair-v1",
        "study_boundary": "New 15-model repair proposal; historical atomic protocols and results stay separate.",
        "result_policy": "All pending results are null and render as empty cells, never zero or fabricated scores.",
        "aggregation": "Equal dependence-group means primary; micro, paired group sensitivity and denominators accompany all metrics.",
        "interface_contract": {
            "joint_failure": "P(multimodal exact=0 | atomic binding=1 and oracle exact=1), task aligned.",
            "contingency": "All eight atomic/oracle/multimodal binary counts accompany the estimates.",
            "contrasts": "Same-task multimodal-minus-oracle exact repair and multimodal-minus-atomic binding.",
            "subsets": "Full and construction-qualified reports; common locked eligibility across conditions.",
            "analysis_schema": "visual-repair-interface-v1",
            "table_scope": "interface[].full.heldout; repeat with qualified.heldout in the complete report.",
            "table_fields": {
                "joint_failure": "joint_failure_given_atomic_oracle.group_macro",
                "joint_eligible_observations": "joint_failure_given_atomic_oracle.eligible_n",
                "joint_eligible_groups": "joint_failure_given_atomic_oracle.eligible_groups",
                "multimodal_minus_oracle_repair": "delta_repair.group_macro",
                "multimodal_minus_atomic_binding": "delta_binding.group_macro",
            },
            "empty_denominator": None,
            "interpretation": "Operational observed outcomes, not a causal internal-mechanism claim.",
        },
        "required_before_collection": [
            "Complete native-input qualification and freeze eligible-input lineage.",
            "Pin provider/model revision, precision, adapter and image policy in a separate external run lock.",
            "Bind planned slots, supported generation settings and failure rules to the versioned study manifest.",
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


def build(refresh_proposal=False):
    if refresh_proposal and CONFIG.exists():
        previous = json.loads(CONFIG.read_text())
        assert all(value is None for rows in previous["tables"].values()
                   for row in rows for value in row["results"].values()), "Refuse to overwrite measured results."
    if not CONFIG.exists() or refresh_proposal:
        CONFIG.write_text(json.dumps(proposed(), indent=2) + "\n")
    config = json.loads(CONFIG.read_text())
    expected = proposed()
    assert config == expected, "Proposal/schema changed: update deliberately before regeneration."
    generated = HERE / "generated"
    generated.mkdir(exist_ok=True)
    inventory = [[tex(m["name"]), tex(m["category"]),
                  "All four conditions" if "multimodal" in m["tracks"] else "No-image / oracle"]
                 for m in config["models"]]
    (generated / "repair-models.tex").write_text(table(["Model", "Model class", "Planned inputs"], inventory, "lll"))
    headers = {
        "repair-primary": ["Model", "Exact", "Bind", "V-change", "V-keep", "Fault", "All-six"],
        "repair-decomposition": ["Model", "Atomic", "No-image", "Oracle", r"Repair$|$Bind", "Invalid"],
        "repair-interface": ["Model", r"$J$", r"$n_{AO}$", r"$G_{AO}$", r"$\Delta$Repair", r"$\Delta$Bind"],
        "repair-text": ["Model", "No-image repair", "Oracle repair"],
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
        source = LEGACY / relative
        current = relative in {"cvpr.sty", "ieeenat_fullname.bst", "references.bib"}
        target = (HERE if current else ROOT / "tem/paper/previous-assets") / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        target_relative = relative if current else f"../tem/paper/previous-assets/{relative}"
        provenance.append({"source": str(source.relative_to(ROOT)), "target": target_relative, "sha256": digest(target)})
    (HERE / "asset-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    count = sum(len(row["results"]) for data in config["tables"].values() for row in data)
    print(f"Generated {len(config['models'])} proposed models; {count} empty result cells.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-proposal", action="store_true", help="Deliberately replace only the null-valued planning schema.")
    args = parser.parse_args()
    build(args.refresh_proposal)
