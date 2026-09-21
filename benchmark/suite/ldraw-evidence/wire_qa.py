"""Blinded QA of exact wire pixels; no score-based exclusion or source-image substitution."""
import argparse
import base64
import hashlib
import html
import json
from pathlib import Path

from common import ROOT, VERSION, digest, load, save
from evidence_adaptation import validate_run, summarize


def observation_id(task_id, condition, request_hash, images):
    return digest({"task": task_id, "condition": condition, "request": request_hash, "images": images})


def template(run):
    observations = []
    for r in run["rows"]:
        if not r["images"]:
            continue
        hashes = [i["wire_sha256"] for i in r["images"]]
        observations.append({
            "observation_id": observation_id(r["task_id"], run["condition"], r["request_sha256"], hashes),
            "task_id": r["task_id"], "source_id": r["source_id"], "condition": run["condition"],
            "request_hash": r["request_sha256"], "image_hashes": hashes,
            "wire_dimensions": [[i["width"], i["height"]] for i in r["images"]],
            "decision": "pending", "reason": "", "reviewer": "", "reviewed_at": None,
            "blinded_to_model_outputs": True, "reviewed_at_native_wire_size": False})
    return {"analysis_version": VERSION, "kind": "independent-exact-wire-visual-QA",
            "run_manifest_hash": run["manifest_sha256"], "observations": observations,
            "policy": "Decidable / insufficient information / invalid item. Do not inspect model outputs. A source render or extra view cannot substitute for actual wire images."}


def validate_feedback(expected, feedback):
    if feedback["analysis_version"] != VERSION or feedback["kind"] != expected["kind"]:
        raise ValueError("QA version/kind mismatch")
    if feedback["run_manifest_hash"] != expected["run_manifest_hash"]:
        raise ValueError("QA run mismatch")
    rows = feedback["observations"]
    if len({r["observation_id"] for r in rows}) != len(rows):
        raise ValueError("Duplicate QA observation")
    by_id = {r["observation_id"]: r for r in rows}
    if set(by_id) != {r["observation_id"] for r in expected["observations"]}:
        raise ValueError("QA denominator changed")
    for ref in expected["observations"]:
        r = by_id[ref["observation_id"]]
        for key in ["task_id", "source_id", "condition", "request_hash", "image_hashes", "wire_dimensions"]:
            if r[key] != ref[key]:
                raise ValueError(f"QA observation mismatch: {key}")
        if r["decision"] not in ["pending", "decidable", "insufficient-information", "invalid-item"]:
            raise ValueError("Unknown QA decision")
        if r["decision"] != "pending":
            if not r["reviewer"].strip() or not r["reviewed_at"] or not r["blinded_to_model_outputs"] or not r["reviewed_at_native_wire_size"]:
                raise ValueError("QA requires reviewer, date, blinding and native-size attestation")
            if r["decision"] != "decidable" and not r["reason"].strip():
                raise ValueError("Non-decidable QA requires an explicit reason")
    return by_id


def qualify_pairs(analysis, feedback_maps):
    qa = {}
    for mapping in feedback_maps:
        if qa.keys() & mapping.keys():
            raise ValueError("Conflicting duplicate QA receipt; adjudicate explicitly")
        qa.update(mapping)
    comparable, reasons = [], []
    for row in analysis["rows"]:
        decisions = []
        for arm in ["A", "B"]:
            key = observation_id(row["parent_task_id"], row[f"condition_{arm}"],
                                 row[f"request_hash_{arm}"], row[f"image_hashes_{arm}"])
            decisions.append(qa.get(key, {}).get("decision", "pending"))
        if decisions == ["decidable", "decidable"]:
            comparable.append(row)
        else:
            reasons.append({"pair_id": row["pair_id"], "decisions_A_B": decisions,
                            "reason": "Both actual observations must be independently decidable"})
    return {"analysis_version": VERSION, "full_pair_denominator": len(analysis["rows"]),
            "full_result_preserved": analysis["summary"], "QA_comparable_pairs": len(comparable),
            "QA_comparable_result": summarize(comparable, analysis["truth_policy"]) if comparable else None,
            "pending_or_access_difference": reasons,
            "interpretation": "Conditional QA subset, never a replacement for the complete denominator."}


def review_html(run, qa):
    manifest = load(ROOT / run["manifest"])
    directory = (ROOT / run["manifest"]).parent
    requests = {r["taskId"]: r for r in manifest["requests"]}
    records = []
    for ref in qa["observations"]:
        path = directory / requests[ref["task_id"]]["file"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != ref["request_hash"]:
            raise ValueError("QA request changed")
        body = load(path)
        content = next(m["content"] for m in body["messages"] if m["role"] == "user")
        payload = json.loads(next(c["text"] for c in content if c["type"] == "text"))
        images = []
        for block in content:
            if block["type"] == "image_url":
                images.append(block["image_url"]["url"])
            elif block["type"] == "image":
                images.append("data:image/png;base64," + block["source"]["data"])
        if [hashlib.sha256(base64.b64decode(i.split(",")[1])).hexdigest() for i in images] != ref["image_hashes"]:
            raise ValueError("QA image bytes mismatch")
        records.append({"task_id": ref["task_id"], "payload": payload, "images": images})
    embedded = json.dumps({"qa": qa, "records": records}, ensure_ascii=True).replace("</", "<\\/")
    return """<!doctype html><html lang="en"><meta charset="utf-8">
<title>BrickAtlas exact-wire observation review</title>
<style>body{font:16px system-ui;margin:24px;color:#183146}button,select,input,textarea{font:inherit;margin:6px;padding:8px}
.pixels{overflow:auto;border:1px solid #bac8d3;max-height:72vh}img{display:block;max-width:none}
pre{white-space:pre-wrap}textarea{width:70%;height:70px}.status{color:#425d72}</style>
<h1>Exact-wire observation review</h1>
<p>Review whether the supplied question is answerable from these exact images and labels.
Images are shown at native wire resolution. Scroll to inspect; do not use extra views or model answers.</p>
<button id="prev">Previous</button><button id="next">Next</button><span id="count"></span>
<button id="export">Export feedback JSON</button>
<span id="exportstatus" role="status"></span>
<details id="exportpreview"><summary>Feedback JSON preview</summary>
<p><a id="download" download="brickatlas-wire-QA.json">Download prepared feedback</a></p>
<textarea id="exportjson" readonly aria-label="Prepared feedback JSON"></textarea></details>
<h2 id="task"></h2><pre id="question"></pre>
<div id="images"></div><p><label>Decision <select id="decision">
<option value="pending">Pending</option><option value="decidable">Decidable</option>
<option value="insufficient-information">Insufficient information</option><option value="invalid-item">Invalid item</option>
</select></label><input id="reviewer" placeholder="Reviewer ID"></p>
<label><input id="native" type="checkbox">I reviewed the native wire images without model outputs.</label>
<p><textarea id="reason" placeholder="Reason (required for insufficient information or invalid items)"></textarea></p>
<p class="status">All items remain in the complete report. Decisions qualify visual comparisons and generate explicit follow-up work.</p>
<script>const data=EMBEDDED;let at=0;const $=id=>document.getElementById(id);
function keep(){const r=data.qa.observations[at];r.decision=$('decision').value;r.reason=$('reason').value;
r.reviewer=$('reviewer').value;r.reviewed_at_native_wire_size=$('native').checked;
r.reviewed_at=r.decision==='pending'?null:new Date().toISOString()}
function show(){const r=data.records[at],q=data.qa.observations[at];$('task').textContent=r.task_id;
$('count').textContent=`${at+1} / ${data.records.length}`;$('question').textContent=JSON.stringify(r.payload,null,2);
$('images').replaceChildren(...r.images.map(src=>{const d=document.createElement('div');d.className='pixels';
const img=document.createElement('img');img.src=src;img.alt='Exact wire observation';d.append(img);return d}));
for(const k of ['decision','reason','reviewer'])$(k).value=q[k];$('native').checked=q.reviewed_at_native_wire_size}
$('prev').onclick=()=>{keep();at=Math.max(0,at-1);show()};$('next').onclick=()=>{keep();at=Math.min(data.records.length-1,at+1);show()};
$('export').onclick=()=>{keep();const text=JSON.stringify(data.qa,null,2),a=$('download');
if(a.href.startsWith('blob:'))URL.revokeObjectURL(a.href);
a.href=URL.createObjectURL(new Blob([text],{type:'application/json'}));
$('exportjson').value=text;$('exportpreview').open=true;
$('exportstatus').textContent=`Prepared ${data.qa.observations.length} observations. Download or copy the JSON below.`;
a.click()};show();</script></html>
""".replace("EMBEDDED", embedded)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--feedback", type=Path)
    args = parser.parse_args()
    run = validate_run(args.run)
    qa = template(run)
    if args.feedback:
        checked = validate_feedback(qa, load(args.feedback))
        print(json.dumps({"observations": len(checked), "reviewed": sum(r["decision"] != "pending" for r in checked.values())}))
    else:
        if args.out.exists():
            parser.error("Use a new output directory")
        args.out.mkdir(parents=True)
        save(args.out / "validated-run.json", run)
        save(args.out / "qa-template.json", qa)
        (args.out / "review.html").write_text(review_html(run, qa))
        print(json.dumps({"observations": len(qa["observations"]), "output": str(args.out)}))


if __name__ == "__main__":
    main()
