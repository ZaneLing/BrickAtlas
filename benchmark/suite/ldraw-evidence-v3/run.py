#!/usr/bin/env python3
"""Roster-bound one-attempt runner for visual, no-image and graph conditions."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import os
from pathlib import Path

from common import DATA, DATASET, ROOT, VERSION, digest, load, save, sha
from roster import specification, planned
from qa import assets, verify_final
from priors import gate as prior_gate
from graphs import component
from transport import request_bytes, parse_receipt, call


def now():
    return datetime.now(timezone.utc).isoformat()


def codes():
    return {n:sha(Path(__file__).with_name(n)) for n in [
        "common.py","run.py","transport.py","roster.py","qa.py","priors.py","assignment.py","graphs.py","graph_audit.py"]}


def inputs(condition):
    if condition=="graph":
        wires,rows,_=component()
        return wires,{k:{"observation_id":k,"source_id":r["source_id"],"gold":{"value":r["gold"]},
                        "max_value":len(r["surviving_nodes"]),"role":"graph"} for k,r in rows.items()}, {
                        k:digest(v["messages"]) for k,v in wires.items()}
    _,obs,index=assets()
    wires={oid:load(ROOT/w["file"]) for oid,w in index.items()}
    if condition=="no-image":
        wires=deepcopy(wires)
        for wire in wires.values():
            wire["messages"][1]["content"]=[c for c in wire["messages"][1]["content"] if c["type"]!="image_url"]
    return wires,obs,{oid:w["wire_observation_sha256"] for oid,w in index.items()}


def write_bytes(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("xb") as stream:
        stream.write(value)


def run(model_id,condition,qa_path=None,live=False,root=None):
    plan=specification(model_id,condition); entry=plan["model"]
    if live:
        prior_gate()
        qa=verify_final(qa_path,"all") if condition!="graph" else None
        key=os.environ.get("BRICKATLAS_API_KEY")
        assert key, "Provide BRICKATLAS_API_KEY outside the artifacts"
    else:
        qa=None
    wires,_,bindings=inputs(condition)
    assert len(wires)==plan["planned_observations"]
    directory=Path(root) if root else DATA/("model-runs" if live else "wire-audit")
    if live:
        assert directory.resolve()==(DATA/"model-runs").resolve(), "Live runs use the one roster-bound collection root"
    dest=directory/plan["run_id"]
    assert not dest.exists(), "Never overwrite or rerun a planned invocation set"
    adapter=load(ROOT/entry["adapter_file"])
    dest.mkdir(parents=True)
    started=now()
    if qa:
        for row in qa["rows"]:
            for r in row["reviews"]+([row["adjudication"]] if row["adjudication"] else []):
                assert datetime.fromisoformat(r["timestamp"].replace("Z","+00:00"))<=datetime.fromisoformat(started)
    m={"analysis_version":VERSION,"dataset":DATASET,"run_id":plan["run_id"],"model_id":model_id,
       "condition":condition,"mode":"live-inference" if live else "offline-dry-run","status":"running",
       "started":started,"model_roster_sha256":sha(DATA/"model-roster.json"),
       "adapter":adapter,"adapter_hash":entry["adapter_hash"],"code_hashes":codes(),
       "qa":{"file":str(Path(qa_path).resolve()),"sha256":sha(qa_path)} if qa else None,
       "planned_observations":len(wires),"requests":[],"attempts":0,
       "index_sha256":sha(DATA/"observation-index.json") if condition!="graph" else None}
    for oid,wire in wires.items():
        path=dest/"requests"/(oid+".json")
        write_bytes(path,request_bytes(wire,adapter))
        m["requests"].append({"observation_id":oid,"file":str(path.relative_to(dest)),
            "sha256":sha(path),"wire_observation_sha256":bindings[oid]})
    save(dest/"initial-manifest.json",m,immutable=True)
    save(dest/"manifest.json",m)
    if live:
        for req in m["requests"]:
            oid=req["observation_id"]
            intent={"observation_id":oid,"request_sha256":req["sha256"],"started":now(),
                    "attempt":1,"evidence_kind":"pre-call-intent"}
            save(dest/"attempts"/(oid+".json"),intent,immutable=True)
            receipt={**{k:intent[k] for k in ["observation_id","request_sha256","started"]},
                     "evidence_kind":"provider-http-receipt",
                     **call(adapter,(dest/req["file"]).read_bytes(),key),"finished":now()}
            save(dest/"receipts"/(oid+".json"),receipt,immutable=True)
            m["attempts"]+=1;save(dest/"manifest.json",m)
    finish(dest,m,"complete" if live else "dry-run-complete")
    return m


def finish(dest,m,status,closure=None):
    m.update(status=status,finished=now(),closure=closure,
             attempt_hashes={p.stem:sha(p) for p in sorted((dest/"attempts").glob("*.json"))},
             receipt_hashes={p.stem:sha(p) for p in sorted((dest/"receipts").glob("*.json"))})
    m["attempts"]=len(m["attempt_hashes"])
    save(dest/"terminal-manifest.json",m,immutable=True)
    save(dest/"manifest.json",m)


def close_interrupted(directory,reason):
    dest=Path(directory)
    m=load(dest/"manifest.json")
    assert m["mode"]=="live-inference" and m["status"]=="running"
    assert isinstance(reason,str) and reason.strip()
    assert not (dest/"terminal-manifest.json").exists()
    # Preserve the checkpoint before closing; never retry an ambiguous remote call.
    save(dest/"interrupted-checkpoint.json",m,immutable=True)
    ids={r["observation_id"] for r in m["requests"]}
    attempted={p.stem for p in (dest/"attempts").glob("*.json")}
    received={p.stem for p in (dest/"receipts").glob("*.json")}
    assert received<=attempted<=ids
    closure={"reason":reason,"closed_at":now(),"unattempted":sorted(ids-attempted),
             "attempted_without_receipt":sorted(attempted-received),
             "policy":"All scheduled endpoints retained as failures. No fabricated provider receipt or retry."}
    save(dest/"closure.json",closure,immutable=True)
    finish(dest,m,"closed-interrupted",{"file":"closure.json","sha256":sha(dest/"closure.json")})
    verify(dest)


def verify(directory):
    dest=Path(directory).resolve()
    m=load(dest/"manifest.json")
    assert m==load(dest/"terminal-manifest.json"), "Only terminal snapshots are eligible"
    assert m["analysis_version"]==VERSION and m["dataset"]==DATASET
    plan=specification(m["model_id"],m["condition"])
    assert dest.name==m["run_id"]==plan["run_id"]
    assert m["model_roster_sha256"]==sha(DATA/"model-roster.json") and m["code_hashes"]==codes()
    assert m["adapter"]==load(ROOT/plan["model"]["adapter_file"])
    assert m["adapter_hash"]==digest(m["adapter"])==plan["model"]["adapter_hash"]
    initial=load(dest/"initial-manifest.json")
    for key in ["run_id","model_id","condition","started","model_roster_sha256","adapter","adapter_hash",
                "code_hashes","qa","planned_observations","requests","index_sha256","mode"]:
        assert m[key]==initial[key], ("Initial request contract changed",key)
    live=m["mode"]=="live-inference"
    assert m["mode"] in ["live-inference","offline-dry-run"]
    assert m["status"] in (["complete","closed-interrupted"] if live else ["dry-run-complete"])
    wires,obs,bindings=inputs(m["condition"])
    assert m["planned_observations"]==len(wires)==plan["planned_observations"]
    assert [r["observation_id"] for r in m["requests"]]==list(wires)
    assert len({r["observation_id"] for r in m["requests"]})==len(wires)
    qa=None
    if live and m["condition"]!="graph":
        assert m["qa"] and sha(m["qa"]["file"])==m["qa"]["sha256"]
        qa=verify_final(m["qa"]["file"],"all")
        for row in qa["rows"]:
            for r in row["reviews"]+([row["adjudication"]] if row["adjudication"] else []):
                assert datetime.fromisoformat(r["timestamp"].replace("Z","+00:00"))<=datetime.fromisoformat(m["started"])
    else:
        assert m["qa"] is None
    attempted={p.stem:sha(p) for p in (dest/"attempts").glob("*.json")}
    receipts={p.stem:sha(p) for p in (dest/"receipts").glob("*.json")}
    assert attempted==m["attempt_hashes"] and receipts==m["receipt_hashes"]
    assert set(receipts)<=set(attempted)<=set(wires) and len(attempted)==m["attempts"]
    if not live:
        assert not attempted and not receipts and m["closure"] is None
    elif m["status"]=="complete":
        assert set(receipts)==set(attempted)==set(wires) and m["closure"] is None
    else:
        assert m["closure"]=={"file":"closure.json","sha256":sha(dest/"closure.json")}
        closure=load(dest/"closure.json")
        assert closure["unattempted"]==sorted(set(wires)-set(attempted))
        assert closure["attempted_without_receipt"]==sorted(set(attempted)-set(receipts))
        assert closure["reason"].strip()
    rows=[]
    for req in m["requests"]:
        oid=req["observation_id"]; o=obs[oid]
        assert req["file"]==f"requests/{oid}.json"
        assert req["sha256"]==sha(dest/req["file"])
        assert (dest/req["file"]).read_bytes()==request_bytes(wires[oid],m["adapter"])
        assert req["wire_observation_sha256"]==bindings[oid]
        receipt=load(dest/"receipts"/(oid+".json")) if oid in receipts else None
        if oid in attempted:
            intent=load(dest/"attempts"/(oid+".json"))
            assert intent["observation_id"]==oid and intent["request_sha256"]==req["sha256"]
            assert intent["attempt"]==1 and intent["evidence_kind"]=="pre-call-intent"
            assert datetime.fromisoformat(intent["started"])>=datetime.fromisoformat(m["started"])
        if receipt:
            assert live and receipt["evidence_kind"]=="provider-http-receipt"
            assert all(receipt[k]==intent[k] for k in ["observation_id","request_sha256","started"])
            assert datetime.fromisoformat(receipt["finished"])>=datetime.fromisoformat(receipt["started"])
        parsed=parse_receipt(receipt,[p["id"] for p in o.get("payload",{}).get("options",[])],
                             m["adapter"],o.get("max_value"))
        if live and not receipt:
            parsed["failure_reason"]="unattempted-closed" if oid not in attempted else "interrupted-no-receipt"
        rows.append({**{k:o[k] for k in ["observation_id","source_id","gold","role"]},
            **{k:o[k] for k in ["parent_task_id","family","display_name","arm"] if k in o},
            **parsed,"success":int(parsed["answer"]==o["gold"]) if live else None,
            "valid_format":parsed["valid_format"] if live else None,"request_sha256":req["sha256"],
            "wire_observation_sha256":bindings[oid],
            "receipt_file":str(dest/"receipts"/(oid+".json")) if receipt else None,
            "receipt_sha256":receipts.get(oid)})
    return {"analysis_version":VERSION,"mode":m["mode"],"status":m["status"] if live else "not-run",
        "run_id":m["run_id"],"model_id":m["model_id"],"condition":m["condition"],
        "provider":plan["model"]["provider"],"model_revision":m["adapter"]["model_revision"],
        "adapter_hash":m["adapter_hash"],"started":m["started"],"finished":m["finished"],
        "manifest_file":str(dest/"manifest.json"),"manifest_sha256":sha(dest/"manifest.json"),
        "index_sha256":m["index_sha256"],"request_index_sha256":digest(m["requests"]),
        "receipt_set_sha256":digest(receipts),"attempt_set_sha256":digest(attempted),
        "qa":m["qa"],"rows":rows,"closure":m["closure"]}


def main():
    parser=argparse.ArgumentParser(); sub=parser.add_subparsers(dest="command",required=True)
    r=sub.add_parser("run"); r.add_argument("--model",required=True);r.add_argument("--condition",choices=["visual","no-image","graph"],required=True)
    r.add_argument("--qa");r.add_argument("--live",action="store_true");r.add_argument("--root")
    v=sub.add_parser("verify");v.add_argument("directory");v.add_argument("output")
    c=sub.add_parser("close");c.add_argument("directory");c.add_argument("--reason",required=True)
    args=parser.parse_args()
    if args.command=="run":
        m=run(args.model,args.condition,args.qa,args.live,args.root)
        print({k:m[k] for k in ["run_id","status","planned_observations","attempts"]})
    elif args.command=="verify":
        save(args.output,verify(args.directory),immutable=True)
    else:
        close_interrupted(args.directory,args.reason)


if __name__=="__main__":
    main()
