"""Semantic regression checks for mission state, exact costs, metrics and protocol."""
from dataclasses import asdict
import copy
import json
from pathlib import Path
import random

from bank import DATA, ROOT, load_oracle, make_mission, task_bank, task_by_id, write_json
from evaluate import evaluate
from metrics import optimal_corridor, trajectory_metrics
from mission import Action, Mission, State, canonical_hash
from probes import Probe
from session import Session, replay_export


def rejects(call):
    try:
        call()
    except (ValueError, KeyError, TypeError):
        return
    raise AssertionError("Invalid input was accepted")


def send(session, action):
    return session.submit({"requestId": f"request-{session.revision}", "revision": session.revision,
                           "action": action})


def check():
    bank = task_bank()
    identity = {"runId": "semantic-ceiling", "participantId": "software-oracle", "condition": "structured"}
    assignment = {"episodes": [t["id"] for t in bank["episodes"]], "probes": [p["id"] for p in bank["probes"]]}
    submission = {"schema": "brickplan-submission/2.0", "identity": identity, "bankHash": canonical_hash(bank),
                  "assignments": assignment, "seed": 18, "episodes": {}, "probes": {}}
    checks = CounterLike()
    for task in bank["episodes"]:
        oracle, m = load_oracle(task["id"]), make_mission(task)
        session = Session(m, task, seed=18, identity={**identity, "sessionId": task["id"]})
        for action in oracle.witness(session.state):
            response = send(session, session.public_action(action))
            assert response["result"]["code"] == "OK"
            assert m.valid(session.state)
        send(session, {"type": "finish"})
        row = trajectory_metrics(oracle, session)
        assert row["success"] and row["regret"] == 0 and row["conditionalExcessTotal"] == 0
        record = session.export()
        assert replay_export(m, task, record).export() == record
        submission["episodes"][task["id"]] = record
        checks.add("optimal-protocol-replays")
    for probe in bank["probes"]:
        presentation = Probe(probe, probe["id"], 18, identity)
        answer = ({"choice": presentation.order.index(probe["optimalChoices"][0])} if "choices" in probe
                  else {"firstConflict": probe["firstConflict"]})
        presentation.submit({"requestId": "answer", "revision": 0,
                             "action": {"type": "answer", "answer": answer}})
        submission["probes"][probe["id"]] = presentation.export()
        checks.add("oracle-probe-answers")
    report = evaluate(submission)
    assert report["trajectory"]["success"]["value"] == 1
    assert report["probes"]["correct"]["value"] == 1
    assert all(v["joint"]["value"] == 1 for v in report["pairedConsistency"].values())
    write_json(ROOT / "tem/brickplan-v2.2/validation/oracle.submission.json", submission)
    write_json(ROOT / "tem/brickplan-v2.2/validation/oracle.report.json", report)
    # All missing runs remain in the denominator.
    missing = copy.deepcopy(submission)
    missing["episodes"], missing["probes"] = {}, {}
    empty_report = evaluate(missing)
    assert empty_report["trajectory"]["census"]["missing"] == len(bank["episodes"])
    assert empty_report["trajectory"]["success"]["value"] == 0
    assert empty_report["probes"]["correct"]["value"] == 0
    checks.add("missing-assignment-census")
    tampered = copy.deepcopy(submission)
    first_id = bank["episodes"][0]["id"]
    tampered["episodes"][first_id]["events"][0]["after"]["assembly"] ^= 1
    rejects(lambda: evaluate(tampered))
    tampered = copy.deepcopy(submission)
    tampered["episodes"][first_id]["identity"]["participantId"] = "other"
    rejects(lambda: evaluate(tampered))
    checks.add("tamper-and-identity-rejection")
    # Same physical image, different completed jobs: disjoint optimal actions.
    for pair in (p for p in bank["pairs"] if p["kind"] in ("history", "counterfactual-work")):
        a, b = map(task_by_id, pair["members"])
        assert a["start"]["assembly"] == b["start"]["assembly"]
        assert a["goal"] == b["goal"]
        assert not ({tuple(sorted(x.items())) for x in a["initialOptimalActions"]}
                    & {tuple(sorted(x.items())) for x in b["initialOptimalActions"]})
        checks.add("certified-counterfactual-pairs")
    # Check actual horizon recurrence against a separate recursive bounded search.
    probe = next(p for p in bank["probes"] if p["kind"] == "next-action")
    oracle = load_oracle(probe["taskId"])
    tables = oracle.horizon_tables()
    m = oracle.mission
    def bounded(state, depth):
        if state == m.terminal:
            return 0
        if depth == 0:
            return m.lower_bound(state)
        return min(1 + bounded(after, depth - 1) for _, after in m.moves(state))
    s = State(**probe["state"])
    assert bounded(s, 4) == int(tables[4][oracle.encode(s)])
    checks.add("independent-horizon-recurrence")
    # Find a legal error when rework was already mandatory, then undo it.
    task = next(t for t in bank["episodes"] if t["kind"] == "multi-inspection-scheduling"
                and t["profile"] == "kart-deck")
    oracle = load_oracle(task["id"])
    m, start = oracle.mission, State(**task["start"])
    start = next(s for s in m.replay(start, oracle.witness(start))["states"]
                 if oracle.distance(s) > (s.assembly ^ m.goal).bit_count() + len(m.pending(s))
                 and any(1 + oracle.distance(after) > oracle.distance(s) for _, after in m.moves(s)))
    task = {**task, "start": asdict(start)}
    bad = next((a, after) for a, after in m.moves(start)
               if 1 + oracle.distance(after) > oracle.distance(start))
    session = Session(m, task)
    send(session, session.public_action(bad[0]))
    send(session, {"type": "diagnose", "avoidableError": True})
    reverse = Action("attach" if bad[0].type == "detach" else "detach", bad[0].site)
    send(session, session.public_action(reverse))
    row = trajectory_metrics(oracle, session)
    assert row["initialMandatoryRework"]
    assert len(row["errorEvents"]) == 1
    error = row["errorEvents"][0]
    assert error["mandatoryReworkBeforeError"] and error["outcome"] == "restored"
    assert error["diagnosis"] and error["recoveryEfficiency"] == 1
    checks.add("mandatory-rework-error-and-recovery")
    # Repeated errors coexist; an unfinished run is censored, not silently failed.
    def overlapping_fixture():
        for assembly in oracle.graph.states:
            s = State(assembly)
            for a, after in m.moves(s):
                if 1 + oracle.distance(after) <= oracle.distance(s):
                    continue
                for b, final in m.moves(after):
                    if (1 + oracle.distance(final) > oracle.distance(after)
                            and oracle.encode(final) not in optimal_corridor(oracle, s)):
                        return s, [a, b]
        raise AssertionError("No overlapping-error fixture")
    checkpoint, actions = overlapping_fixture()
    session = Session(m, {**task, "start": asdict(checkpoint)})
    for action in actions:
        send(session, session.public_action(action))
    row = trajectory_metrics(oracle, session)
    assert len(row["errorEvents"]) == 2
    assert any(e["outcome"] == "censored" for e in row["errorEvents"])
    checks.add("overlapping-errors-and-censoring")
    # Illegal operations count in regret, including malformed free-action requests.
    session = Session(m, task)
    send(session, {"type": "audit", "partId": "P999"})
    for action in oracle.witness(session.state):
        send(session, session.public_action(action))
    send(session, {"type": "finish"})
    row = trajectory_metrics(oracle, session)
    assert row["regret"] == 1 and row["regretDecomposition"]["invalidAttempts"] == 1
    checks.add("audit-inclusive-regret")
    # Canonical identity, rack overflow, audit eligibility, and idempotency.
    session = Session(m, task)
    request = {"requestId": "one", "revision": 0, "action": {"type": "inspect", "view": "rear"}}
    a = session.submit(request)
    assert session.submit(request) == a and session.views == 1
    rejects(lambda: session.submit({**request, "action": {"type": "finish"}}))
    rejects(lambda: session.submit({**request, "requestId": "stale"}))
    assert len(session.observation()["inspectionHistory"]) == 1
    for i in range(task["maxViews"] - 1):
        send(session, {"type": "inspect", "view": "top"})
    response = send(session, {"type": "inspect", "view": "top"})
    assert response["result"]["code"] == "VIEW_LIMIT" and session.attempts == 1
    site = 0
    response = send(session, {"type": "attach", "partId": session.part_ids[site],
                              "siteId": session.site_ids[(site + 1) % m.domain.n]})
    assert response["result"]["code"] == "REGISTERED_SITE_MISMATCH"
    tight = next(s for s in oracle.graph.states if m.domain.n - s.bit_count() == m.capacity
                 and any(op == "detach" for op, _, _ in m.domain.moves(s)))
    op, site, _ = next(x for x in m.domain.moves(tight) if x[0] == "detach")
    assert m.transition(State(tight), Action(op, site))[1] == "RACK_FULL"
    site = m.jobs[0]
    installed = next(s for s in oracle.graph.states if s & (1 << site))
    assert m.transition(State(installed), Action("audit", site))[1] == "AUDIT_REQUIRES_RACK"
    checks.add("resource-identity-inspection-and-retry-contract")
    # Observations never contain solution tables, graph edges, masks or site flags.
    forbidden = {"oracleFile", "optimalCost", "witness", "initialOptimalActions", "labels",
                 "blockers", "neighbors", "assembly", "done", "relaxationGap", "costs"}
    for track in ("image-id", "structured"):
        observation = Session(m, task, track=track).observation()
        def keys(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    yield key
                    yield from keys(item)
            elif isinstance(value, list):
                for item in value:
                    yield from keys(item)
        assert not forbidden.intersection(keys(observation))
        if track == "image-id":
            assert "sites" not in observation and "fixed" not in observation
        checks.add("observation-isolation")
    write_json(DATA / "semantic-validation.json", {"passed": True, "checks": dict(checks)})
    print(json.dumps(dict(checks), indent=2))


class CounterLike(dict):
    def add(self, key):
        self[key] = self.get(key, 0) + 1


if __name__ == "__main__":
    check()
