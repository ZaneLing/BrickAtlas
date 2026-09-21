#!/usr/bin/env python3
"""Independently verify stimuli and freeze exact, native-resolution model observations."""
import base64
from collections import Counter
import io
import json
import numpy as np
from PIL import Image, ImageFilter

from common import DATA, PUBLIC, ROOT, DATASET, VERSION, digest, frozen, load, original_tasks, save, sha
from priors import gate


def main():
    prior_audit = gate()
    m, rendered = load(DATA / "visual-manifest.json"), load(DATA / "renders.json")
    rows = {r["observation_id"]: r for r in rendered["images"]}
    obs = {o["observation_id"]: o for o in m["observations"]}
    assert len(rows) == len(obs) == 347 and set(rows) == set(obs)
    tasks = original_tasks()
    bundles = {sid: frozen(f"public/benchmark/ldraw-v2/models/{sid}.json")
               for sid in {o["source_id"] for o in obs.values()}}
    verified, wire_index, public = [], [], []
    for o in obs.values():
        r, spec = rows[o["observation_id"]], o["render_spec"]
        assert sha(ROOT / r["file"]) == r["sha256"]
        pixels = (ROOT / r["file"]).read_bytes()
        assert Image.open(io.BytesIO(pixels)).size == (1280, 800)
        assert "original color" not in o["payload"]["question"].lower()
        if spec["kind"] == "appearance-color":
            assert spec["render_operands"] == [spec["target_id"]]
            answer = next(p["id"] for p in o["payload"]["options"]
                          if p["label"] == spec["body_color"]["name"])
            assert r["metadata"]["color_settings"]["body"] == spec["body_color"]
        else:
            parts = {p["id"]: p for p in bundles[o["source_id"]]["parts"]}
            t = tasks[o["parent_task_id"]]
            candidates = spec.get("candidate_ids") or [
                next(k for k, v in spec["labels"].items() if v == option["label"])
                for option in o["payload"]["options"]]
            matches = [index for index, c in enumerate(candidates)
                       if parts[c]["partNumber"] == parts[spec["target_id"]]["partNumber"]]
            assert len(matches) == 1, (t["id"], "not unique source type", matches)
            answer = o["payload"]["options"][matches[0]]["id"]
            if spec["kind"] == "preserved-render":
                assert r["sha256"] == spec["source_sha256"] == sha(ROOT / spec["source_file"])
            if spec["kind"] == "candidate-labels":
                assert r["metadata"]["labels"] == spec["labels"]
                assert r["metadata"]["reference_positions"] == spec["reference_positions"]
                assert r["metadata"]["camera"] == spec["camera"]
                for name in ["base","mask"]:
                    assert sha(ROOT / r[name+"_file"]) == r[name+"_sha256"]
        assert o["gold"] == {"choiceId": answer}, "Independent gold verification failed"
        # This exact messages array is the complete model-visible observation. Provider
        # envelope fields are separately hashed per run and cannot alter these messages.
        messages = [
            {"role": "system", "content": m["system_prompt"]},
            {"role": "user", "content": [
                {"type": "text", "text": json.dumps(o["payload"], ensure_ascii=True, separators=(",", ":"))},
                {"type": "image_url", "image_url": {
                    "url": "data:image/png;base64," + base64.b64encode(pixels).decode(), "detail": "high"}}]}]
        wire = {"messages": messages}
        path = DATA / "observations" / (o["observation_id"] + ".json")
        save(path, wire, immutable=True)
        if not o["observation_id"].startswith("obs3-"):
            old_index = frozen("benchmark/ldraw-evidence-v2/observation-index.json")
            prior = next(r for r in old_index["observations"] if r["observation_id"]==o["observation_id"])
            assert sha(path)==prior["wire_observation_sha256"], "Unaffected component wire changed"
        wire_index.append({"observation_id": o["observation_id"], "file": str(path.relative_to(ROOT)),
                           "wire_observation_sha256": sha(path), "messages_hash": digest(messages),
                           "image_sha256": sha(ROOT / r["file"]), "width": 1280, "height": 800,
                           "role": o["role"], "family": o["family"]})
        public.append({"observation_id": o["observation_id"], "payload": o["payload"],
                       "image": "/" + r["file"].removeprefix("public/"),
                       "wire_observation_sha256": sha(path)})
    for p in m["pairs"]:
        a, b = obs[p["a"]], obs[p["b"]]
        assert a["payload"] == b["payload"] and a["gold"] != b["gold"]
        assert a["canonical_target"] == b["canonical_target"] and a["source_truth"] == b["source_truth"]
        detail = {"pair_id": p["pair_id"], "family": p["family"], "gold_verified": True}
        if p["family"] == "color":
            ra, rb = rows[p["a"]], rows[p["b"]]
            sa = {k: v for k, v in a["render_spec"].items() if k != "body_color"}
            sb = {k: v for k, v in b["render_spec"].items() if k != "body_color"}
            assert sa == sb
            for key in ["cameras", "projections", "render_operands"]:
                assert ra["metadata"][key] == rb["metadata"][key], key
            assert ra["mask_sha256"] == rb["mask_sha256"] == sha(ROOT / ra["mask_file"])
            assert sha(ROOT / rb["mask_file"]) == ra["mask_sha256"]
            pa = np.array(Image.open(ROOT / ra["file"]).convert("RGB"))
            pb = np.array(Image.open(ROOT / rb["file"]).convert("RGB"))
            changed = np.any(pa != pb, axis=2)
            mask = Image.open(ROOT / ra["mask_file"]).convert("L").point(lambda v: 255 if v < 255 else 0)
            # One-pixel dilation includes multisample antialiasing at the body boundary.
            allowed = np.array(mask.filter(ImageFilter.MaxFilter(3))) > 0
            outside = int(np.count_nonzero(changed & ~allowed))
            assert outside == 0, (p["pair_id"], "nonbody pixels changed", outside)
            assert int(changed.sum()) > 100
            detail.update(changed_pixels=int(changed.sum()), nonbody_changed_pixels=outside,
                          silhouette_identical=True, camera_identical=True, label_projections_identical=True)
        else:
            ra,rb = rows[p["a"]],rows[p["b"]]
            assert ra["base_sha256"]==rb["base_sha256"], "Underlying Part-type rendering changed"
            assert ra["mask_sha256"]==rb["mask_sha256"]
            assert a["render_spec"]["reference_positions"]==b["render_spec"]["reference_positions"]
            pa,pb = [np.asarray(Image.open(ROOT/r["file"]).convert("RGB")) for r in [ra,rb]]
            changed=np.any(pa!=pb,axis=2)
            allowed=np.asarray(Image.open(ROOT/ra["mask_file"]).convert("L"))<255
            outside=int((changed&~allowed).sum())
            assert outside==0 and changed.sum()>0
            detail.update(changed_pixels=int(changed.sum()),nonlabel_changed_pixels=outside,
                          underlying_pixels_identical=True,reference_positions_identical=True)
        verified.append(detail)
    save(DATA / "stimulus-validation.json", {"analysis_version": VERSION, "status": "passed",
         "observations": len(obs), "pairs": len(verified), "gold_counts": dict(Counter(
             o["gold_semantics"] for o in obs.values() if o["family"] == "color")),
         "answer_prior_audit_sha256":sha(DATA/"answer-prior-audit.json"),
         "answer_prior_audit":prior_audit,
         "records": verified, "human_answerability": "not-established-by-machine-validation"}, immutable=True)
    save(DATA / "prior-gate-validation.json", {"status":"passed",
         "audit_sha256":sha(DATA/"answer-prior-audit.json"),
         "assignment_contract_sha256":sha(DATA/"assignment-contract.json"),
         "part_type_marginals":prior_audit["families"]["shape-match"]["gold_marginals"],
         "part_type_transition_matrix":prior_audit["families"]["shape-match"]["transition_matrix"],
         "enforcement":"Independently reconstructed before wire seal; also required before live runs."},immutable=True)
    save(DATA / "observation-index.json", {"dataset": DATASET, "analysis_version": VERSION,
         "identity_contract_sha256": sha(DATA / "identity-contract.json"),
         "manifest_sha256": sha(DATA / "visual-manifest.json"),
         "renders_sha256": sha(DATA / "renders.json"), "system_prompt": m["system_prompt"],
         "binding": "Exact model-visible messages and PNG bytes; provider envelopes separately receipt-bound.",
         "observations": wire_index}, immutable=True)
    save(PUBLIC / "stimuli.json", {"dataset": DATASET, "role": "model-input-no-gold",
         "observations": public}, immutable=True)
    print({"status": "passed", "observations": len(obs), "primary": 280,
           "color_pixel_invariance": sum(r["family"] == "color" for r in verified)})


if __name__ == "__main__":
    main()
