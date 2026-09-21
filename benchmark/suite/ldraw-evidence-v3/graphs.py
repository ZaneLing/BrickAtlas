"""Verify the preserved graph component without regenerating its corpus."""
import json
from common import frozen, digest
from graph_audit import inspect

INPUTS="benchmark/ldraw-evidence-v1/matched-graphs-v1/inputs.json"
PRIOR="benchmark/ldraw-evidence-v1/matched-graphs-v1/manifest.json"
AUDIT="benchmark/ldraw-evidence-v2/graph-audit.json"
SYSTEM=("Answer using only the supplied hypothetical undirected graph. Return exactly one JSON object "
        "with the integer field value. Do not add prose, markdown, other fields, or use tools.")


def component():
    prior,audit,public=frozen(PRIOR),frozen(AUDIT),frozen(INPUTS)
    rebuilt=[inspect(o["id"],o["source_id"],o["parent_task_id"],o["input"],o["gold"]["value"])
             for o in prior["observations"]]
    assert digest(rebuilt)==digest(audit["observations"])
    byid={o["id"]:o for o in rebuilt}
    assert len(public["observations"])==219 and len(audit["pairs"])==146
    wires={}
    for o in public["observations"]:
        src=next(r for r in prior["observations"] if r["id"]==o["id"])
        assert o["payload"]==src["input"]
        wires[o["id"]]={"messages":[{"role":"system","content":SYSTEM},
            {"role":"user","content":[{"type":"text","text":json.dumps(o["payload"],ensure_ascii=True,separators=(",",":"))}]}]}
    return wires,byid,audit
