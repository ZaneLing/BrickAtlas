#!/usr/bin/env python3
"""Snapshot and verify every planned roster request without provider calls."""
from common import DATA, VERSION, load, save, sha
from roster import planned
from run import run, verify


def main():
    rows=[]
    for plan in planned().values():
        dest=DATA/"wire-audit"/plan["run_id"]
        if not dest.exists():
            run(plan["model"]["model_id"],plan["condition"])
        checked=verify(dest)
        assert checked["mode"]=="offline-dry-run" and checked["status"]=="not-run"
        rows.append({"run_id":plan["run_id"],"condition":plan["condition"],
            "requests":len(checked["rows"]),"manifest_sha256":checked["manifest_sha256"],
            "request_index_sha256":checked["request_index_sha256"],"provider_calls":0})
    save(DATA/"wire-audit-validation.json",{"analysis_version":VERSION,"status":"passed",
        "model_roster_sha256":sha(DATA/"model-roster.json"),"runs":rows,
        "planned_runs":9,"request_count":sum(r["requests"] for r in rows),"provider_calls":0,
        "empirical_registration":"prohibited: all are offline dry runs"},immutable=True)
    print({"status":"passed","runs":len(rows),"requests":sum(r["requests"] for r in rows),"provider_calls":0})


if __name__=="__main__":
    main()
