"""Finite placement repair tasks; exact BFS and replayable causal annotations."""
from collections import deque
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "deliverables/brickplan-repair"
TYPES = {"missing": "漏件", "wrong_color": "错颜色", "wrong_type": "错型号",
         "offset": "水平偏移", "extra": "多余零件", "rotation": "朝向错误",
         "premature_closure": "过早封闭", "external_removal": "外部移除",
         "wrong_size": "错尺寸", "height_layer": "高度错层", "wrong_order": "依赖顺序错误",
         "costly_branch": "合法但高返工", "path_blocked": "插入路径被挡",
         "occluded": "内部错误被遮挡", "stale_plan": "旧计划失效"}


def presets():
    goal = {f"P{i:03}": f"P{i:03}:goal" for i in range(1, 9)}
    rows = [
        ("R001", "内部漏件 · 上层已封闭", "内部缺少必要零件。先打开遮挡，再补件、复原。",
         {"P006": ""}, [("P006", "missing")], 5),
        ("R002", "埋藏的错色件", "一个连接件颜色不对。正确替件在暂存架，需要拆开后换件。",
         {"P006": "", "W006": "W006:wrong"}, [("W006", "wrong_color")], 6),
        ("R003", "顶件偏移一颗 stud", "顶件仍然咬合，但与目标位置相差一颗 stud。拆下后重新对齐。",
         {"P002": "P002:offset"}, [("P002", "offset")], 2),
        ("R004", "多垫一层 · 顶件过高", "一个多余垫片让顶件高了一层。移除多余件，再恢复顶件。",
         {"P002": "P002:raised", "E001": "E001:extra"}, [("E001", "extra")], 3),
        ("R005", "顶件型号装错", "一个普通方板替代了目标转盘底座。拆除错件并换上正确型号。",
         {"P002": "", "W002": "W002:wrong"}, [("W002", "wrong_type")], 2),
        ("R006", "长条朝向装错", "长条绕真实连接点转错了 90°。拆下后按目标方向重装。",
         {"P005": "P005:turned"}, [("P005", "rotation")], 2),
        ("R007", "两处独立错误", "内部同时有错色件与漏件。一次打开上层，修复两处后复原。",
         {"P006": "", "W006": "W006:wrong", "P007": ""},
         [("W006", "wrong_color"), ("P007", "missing")], 7),
        ("R008", "环境封顶 · 旧计划失效", "环境会提前装上顶件。观察旧计划为何失败，再从新状态规划。",
         {"P006": ""}, [("P002", "premature_closure")], 5),
        ("R009", "已装零件被外部取走", "环境会取走一根已装好的长条。恢复结构并更新计划。",
         {"P005": ""}, [("P005", "external_removal")], 1),
        ("R010", "无故障对照", "当前结构与目标完全一致。无需拆装，直接提交。",
         {}, [], 0),
    ]
    cases = {}
    for cid, title, description, edits, roots, optimum in rows:
        active = sorted(set(goal) | set(edits))
        target = {a: goal.get(a, "") for a in active}
        initial = {**target, **edits}
        choices = {a: [k for k in (target[a], initial[a]) if k] for a in active}
        choices = {a: list(dict.fromkeys(v)) for a, v in choices.items()}
        case = dict(id=cid, title=title, description=description, actors=active,
                    initial=initial, goal=target, choices=choices, rackCapacity=5,
                    expectedOptimum=optimum, sourceExample="E002", sourcePieces=27,
                    roots=[dict(eventId=f"root-{i+1}", partId=a, type=t, stage="Root")
                           for i, (a, t) in enumerate(roots)],
                    propagation=[], sourceLabels=["S", "A"],
                    contract="Repair variant; not the original E002 work-order task.")
        if cid in ("R001", "R002", "R007"):
            case["propagation"] = [dict(eventId="close-1", partId="P004", stage="Propagation"),
                                   dict(eventId="close-2", partId="P002", stage="Propagation")]
        if cid == "R004":
            case["propagation"] = [dict(eventId="raised-top", partId="P002", stage="Propagation",
                                        type="height_layer")]
        if cid == "R008":
            case.update(preIntervention={**initial, "P002": ""},
                        intervention=dict(type="attach", partId="P002", candidate="P002:goal"),
                        sourceLabels=["A", "O", "X"])
        if cid == "R009":
            case.update(preIntervention=target,
                        intervention=dict(type="detach", partId="P005"),
                        sourceLabels=["X", "S"])
        cases[cid] = case
    return cases


class Domain:
    def __init__(self, certificate=None, cases=None):
        self.certificate = certificate or json.loads((OUTPUT / "qualification.json").read_text())
        self.candidates = self.certificate["candidates"]
        self.fixed = set(self.certificate["fixed"])
        self.cases = presets() if cases is None else cases
        self.cache = {}

    @staticmethod
    def pack(case, assignment):
        return tuple(assignment[a] for a in case["actors"])

    @staticmethod
    def unpack(case, state):
        return dict(zip(case["actors"], state))

    def valid(self, case, state):
        if len(state) != len(case["actors"]):
            return "INVALID_STATE"
        installed = set(state) - {""}
        if state.count("") > case["rackCapacity"]:
            return "RACK_FULL"
        for actor, candidate in zip(case["actors"], state):
            if candidate and (candidate not in case["choices"][actor] or
                              self.candidates[candidate]["actor"] != actor):
                return "UNREGISTERED_POSE"
        present = installed | self.fixed
        for candidate in installed:
            if present.intersection(self.candidates[candidate]["endpointBlocked"]):
                return "ENDPOINT_COLLISION"
        adjacency = {c: set() for c in present}
        for c in installed:
            for other in present.intersection(self.candidates[c]["support"]):
                adjacency[c].add(other)
                adjacency[other].add(c)
        reachable = set(self.fixed)
        while True:
            new = {c for c in installed if reachable.intersection(adjacency[c])}
            if new <= reachable:
                break
            reachable |= new
        return "OK" if installed <= reachable else "DISCONNECTED_ASSEMBLY"

    def transition(self, case, state, action):
        if not isinstance(action, dict):
            return state, dict(code="INVALID_ACTION")
        kind, actor = action.get("type"), action.get("partId")
        if kind not in ("attach", "detach") or actor not in case["actors"]:
            return state, dict(code="INVALID_ACTION")
        index = case["actors"].index(actor)
        current = state[index]
        if kind == "detach" and not current:
            return state, dict(code="ALREADY_IN_RACK")
        if kind == "attach" and current:
            return state, dict(code="ALREADY_INSTALLED")
        candidate = current if kind == "detach" else action.get("candidate", actor + ":goal")
        if candidate not in case["choices"][actor]:
            return state, dict(code="UNREGISTERED_POSE")
        present = (set(state) - {"", current}) | self.fixed
        blocked = present.intersection(self.candidates[candidate]["pathBlocked"])
        if blocked:
            return state, dict(code="PATH_BLOCKED", blockers=sorted(blocked))
        after = list(state)
        after[index] = "" if kind == "detach" else candidate
        after = tuple(after)
        code = self.valid(case, after)
        return (after if code == "OK" else state), dict(code=code)

    def actions(self, case, state):
        for actor, installed in zip(case["actors"], state):
            if installed:
                yield dict(type="detach", partId=actor)
            else:
                for candidate in case["choices"][actor]:
                    yield dict(type="attach", partId=actor, candidate=candidate)

    def plan(self, case, state):
        key = (case["id"], state, tuple(case["goal"].items()),
               tuple((a, tuple(case["choices"][a])) for a in case["actors"]), case["rackCapacity"])
        if key in self.cache:
            return deepcopy(self.cache[key])
        goal = self.pack(case, case["goal"])
        queue, previous = deque([state]), {state: None}
        while queue:
            node = queue.popleft()
            if node == goal:
                result = []
                while previous[node]:
                    node, action = previous[node]
                    result.append(action)
                result.reverse()
                self.cache[key] = result
                return deepcopy(result)
            for action in self.actions(case, node):
                after, validator = self.transition(case, node, action)
                if validator["code"] == "OK" and after not in previous:
                    previous[after] = (node, action)
                    queue.append(after)
        return None

    def root_counterfactuals(self, case):
        """Replay construction events, correcting each subset of root events."""
        if "causalReplay" in case:
            return self.replay_causal_events(case)
        roots = case["roots"]
        results = []
        for mask in range(1 << len(roots)):
            origin = dict(case["goal"])
            cid = case["id"]
            events = []
            def attach(actor, candidate=None):
                return dict(type="attach", partId=actor, candidate=candidate or actor+":goal")
            if cid in ("R001", "R002", "R007"):
                for actor in ("P002", "P004", "P006"):
                    origin[actor] = ""
                if cid == "R007":
                    origin["P007"] = ""
            elif cid in ("R003", "R004", "R005"):
                origin["P002"] = ""
            elif cid == "R006":
                origin["P005"] = ""
            elif cid == "R008":
                origin = dict(case["preIntervention"])
            for i, root in enumerate(roots):
                corrected = bool(mask & (1 << i))
                actor, kind = root["partId"], root["type"]
                if kind == "missing":
                    action = attach(actor) if corrected else None
                elif kind == "wrong_color":
                    action = attach("P006") if corrected else attach("W006", "W006:wrong")
                elif kind == "wrong_type":
                    action = attach("P002") if corrected else attach("W002", "W002:wrong")
                elif kind == "extra":
                    action = None if corrected else attach("E001", "E001:extra")
                elif kind == "premature_closure":
                    action = None if corrected else attach("P002")
                elif kind == "external_removal":
                    action = None if corrected else dict(type="detach", partId="P005")
                else:
                    action = attach(actor, case["goal"][actor] if corrected else case["initial"][actor])
                events.append(dict(eventId=root["eventId"], stage="Root", corrected=corrected,
                                   action=action, omitted=action is None))
            if cid in ("R001", "R002", "R007"):
                events.extend([dict(eventId="close-1", stage="Propagation", action=attach("P004")),
                               dict(eventId="close-2", stage="Propagation", action=attach("P002"))])
            elif cid == "R004":
                events.append(dict(eventId="raised-top", stage="Propagation",
                                   action=attach("P002", "P002:goal" if mask else "P002:raised")))
            state = self.pack(case, origin)
            assert self.valid(case, state) == "OK"
            replay = []
            for event in events:
                validator = dict(code="SKIPPED_EVENT")
                if event["action"]:
                    state, validator = self.transition(case, state, event["action"])
                    assert validator["code"] == "OK", (cid, event, validator)
                replay.append(dict(**event, validator=validator, state=self.unpack(case, state)))
            if mask == 0:
                assert state == self.pack(case, case["initial"])
            if cid == "R008":
                for action in self.plan(case, self.pack(case, origin)):
                    after, validator = self.transition(case, state, action)
                    replay.append(dict(action=action, stage="Exposure" if validator["code"] != "OK" else "Continuation",
                                       validator=validator, state=self.unpack(case, after)))
                    state = after
                    if validator["code"] != "OK":
                        break
            results.append(dict(correctedRootIds=[roots[i]["eventId"] for i in range(len(roots)) if mask & (1 << i)],
                                initialState=self.unpack(case, self.pack(case, origin)),
                                stateValid=self.valid(case, state) == "OK",
                                goalReached=state == self.pack(case, case["goal"]), replay=replay))
        return results

    def replay_causal_events(self, case):
        """Each root correction changes a recorded event, never the final label."""
        roots, recipe = case["roots"], case["causalReplay"]
        results = []
        for mask in range(1 << len(roots)):
            corrected = {r["eventId"] for i, r in enumerate(roots) if mask & (1 << i)}
            state = self.pack(case, recipe["origin"])
            assert self.valid(case, state) == "OK"
            replay = []
            for event in recipe["events"]:
                use_corrected = event.get("rootId") in corrected
                actions = event.get("correctedActions", []) if use_corrected else event.get("actions", [])
                for action in actions:
                    after, validator = self.transition(case, state, action)
                    expected = event.get("expectedCode", "OK") if not use_corrected else "OK"
                    assert validator["code"] == expected, (case["id"], action, validator, expected)
                    state = after
                    replay.append(dict(eventId=event["eventId"], stage=event["stage"],
                                       corrected=use_corrected, action=action, validator=validator,
                                       state=self.unpack(case, state)))
            if not mask:
                assert state == self.pack(case, case["initial"]), case["id"]
            failure = state != self.pack(case, case["goal"])
            if recipe.get("failureCriterion") == "blocked_attempt":
                failure = any(r["validator"]["code"] != "OK" for r in replay)
            results.append(dict(correctedRootIds=sorted(corrected), stateValid=True,
                                goalReached=state == self.pack(case, case["goal"]),
                                failureAvoided=not failure, replay=replay))
        return results


class Episode:
    def __init__(self, domain, case_id):
        self.domain, self.case = domain, deepcopy(domain.cases[case_id])
        self.state = domain.pack(self.case, self.case.get("preIntervention", self.case["initial"]))
        self.revision = self.environment_version = self.attempts = 0
        self.plan_version = 0
        self.current_plan = domain.plan(self.case, self.state)
        self.old_plan = deepcopy(self.current_plan)
        self.events = []
        self.disturbed = set()
        self.diagnosis = None
        self.hints = False
        self.replans = 0
        self.terminated = False
        self.run_id = str(time.time_ns())
        self.result = None

    def action(self, action, external=False):
        before = self.state
        after, validator = self.domain.transition(self.case, before, action)
        if not external:
            self.attempts += 1
        if validator["code"] == "OK":
            self.state = after
            self.revision += 1
            if external:
                self.environment_version += 1
            else:
                self.disturbed.add(action["partId"])
        self.events.append(dict(
            step_id=len(self.events)+1, intended_action=deepcopy(action),
            executed_action=deepcopy(action) if validator["code"] == "OK" else None,
            pre_state=self.domain.unpack(self.case, before), post_state=self.domain.unpack(self.case, self.state),
            observation_packet=dict(world_revision=self.revision, available_channels=["rendered_views", "part_inventory", "validator"]),
            structured_belief=None, current_plan=deepcopy(self.current_plan), plan_version=self.plan_version,
            validator_output=validator, environment_intervention=deepcopy(action) if external else None,
            root_labels=deepcopy(self.case["roots"]) if external else [],
            propagation_labels=[], exposure_labels=[dict(stage="Exposure", channel="validator", code=validator["code"])]
            if validator["code"] != "OK" else [], terminal_status=None,
            repair_actions=0 if external else 1,
            repair_cost_vector=dict(attempts=0 if external else 1, executed=int(validator["code"] == "OK" and not external))))
        if validator["code"] == "OK" and not external and self.current_plan and self.current_plan[0] == action:
            self.current_plan.pop(0)
        return validator

    def replan(self, count=False):
        if count:
            self.replans += 1
        self.current_plan = self.domain.plan(self.case, self.state)
        self.plan_version = self.environment_version
        return self.current_plan

    def diagnose(self, entries):
        if self.terminated:
            raise ValueError("本轮已评分，请重置后再提交判断。")
        clean = []
        for row in entries:
            if row.get("partId") not in self.case["actors"] or row.get("type") not in TYPES:
                raise ValueError("诊断中的积木 ID 或错误类型无效。")
            clean.append(dict(partId=row["partId"], type=row["type"]))
        self.diagnosis = dict(entries=clean, step=self.attempts, hinted=self.hints)

    def finish(self):
        self.terminated = True
        goal = self.domain.pack(self.case, self.case["goal"])
        success = self.state == goal
        initial = self.domain.pack(self.case, self.case["initial"])
        optimal = len(self.domain.plan(self.case, initial))
        remaining = self.domain.plan(self.case, self.state)
        good = {a for a in self.case["actors"] if self.case["initial"][a] and
                self.case["initial"][a] == self.case["goal"][a]}
        root_set = {(r["partId"], r["type"]) for r in self.case["roots"]}
        diagnosed = {(r["partId"], r["type"]) for r in self.diagnosis["entries"]} if self.diagnosis else None
        root_correct = diagnosed == root_set if diagnosed is not None else None
        self.result = dict(
            success=success, structureMatched=success, attempts=self.attempts, optimalRepairCost=optimal,
            repairCostRegret=self.attempts-optimal if success else None,
            remainingOptimalCost=len(remaining) if remaining is not None else None,
            correctPrefixPreservation=(len(self.domain.fixed)+len(good-self.disturbed))/(len(self.domain.fixed)+len(good)),
            mutableCorrectPreservation=len(good-self.disturbed)/len(good) if good else None,
            rootLocalizationAccuracy=int(root_correct) if root_correct is not None else None,
            conditionalRecoverySuccess=success if self.hints or root_correct else None,
            endToEndRecoverySuccess=None,
            falseRecoveryClaim=not success,
            unnecessaryInterventionRate=int(bool(self.attempts or self.replans or (diagnosed or set()))) if not root_set else None,
            exposureDetectionLatency=None, rollbackPointRegret=None,
            unmeasuredReasons=dict(exposureDetectionLatency="No evaluated image-only observation and alert-timing protocol.",
                                   rollbackPointRegret="No explicit rollback checkpoint selected.",
                                   endToEndRecoverySuccess="Interactive practice reveals fault category and state labels; not a blind model evaluation."),
            mismatches=[dict(partId=a, actual=v, target=self.case["goal"][a])
                        for a, v in zip(self.case["actors"], self.state) if v != self.case["goal"][a]],
            assisted=self.hints, diagnosis=self.diagnosis,
            terminal_status="recovered" if success else "incorrect_recovery_claim")
        return self.result

    def export(self):
        return dict(schema="brickplan-repair-episode/1", runId=self.run_id, case=self.case,
                    certificateSha256=self.domain.certificate["contentSha256"],
                    state=self.domain.unpack(self.case, self.state), revision=self.revision,
                    environmentVersion=self.environment_version, planVersion=self.plan_version,
                    currentPlan=self.current_plan, initialRootLabels=self.case["roots"],
                    initialPropagationLabels=self.case["propagation"], events=self.events, metrics=self.result)


def validate():
    d = Domain()
    results = []
    for case in d.cases.values():
        initial = d.pack(case, case["initial"])
        assert d.valid(case, initial) == "OK", (case["id"], d.valid(case, initial))
        assert d.valid(case, d.pack(case, case["goal"])) == "OK"
        plan = d.plan(case, initial)
        assert len(plan) == case["expectedOptimum"], (case["id"], plan)
        state = initial
        for action in plan:
            state, response = d.transition(case, state, action)
            assert response["code"] == "OK" and d.valid(case, state) == "OK"
        assert state == d.pack(case, case["goal"])
        cf = d.root_counterfactuals(case)
        assert cf[-1]["goalReached"]
        if case["roots"]:
            assert not any(r["goalReached"] for r in cf[:-1])
        e = Episode(d, case["id"])
        if case.get("intervention"):
            assert e.action(case["intervention"], external=True)["code"] == "OK"
            assert e.state == initial and e.attempts == 0
            assert e.plan_version != e.environment_version
        for action in plan:
            assert e.action(action)["code"] == "OK"
        assert e.finish()["success"] and e.result["repairCostRegret"] == 0
        false = Episode(d, case["id"])
        false.state = initial
        assert false.finish()["success"] == (case["id"] == "R010")
        results.append(dict(caseId=case["id"], initialValid=True, optimum=len(plan), plan=plan,
                            rootCounterfactuals=cf, metrics=e.result))
    c = d.cases["R001"]
    s = d.pack(c, c["initial"])
    _, v = d.transition(c, s, dict(type="attach", partId="P006"))
    assert v["code"] == "PATH_BLOCKED" and "P002:goal" in v["blockers"] and "P004:goal" in v["blockers"]
    # Goal-shaped missing support must not be accepted; extra-height placement
    # is legal only while its actual extra plate remains installed.
    unsupported = dict(d.cases["R010"]["goal"], P004="")
    assert d.valid(d.cases["R010"], d.pack(d.cases["R010"], unsupported)) == "DISCONNECTED_ASSEMBLY"
    height = d.cases["R004"]
    h = d.pack(height, {**height["goal"], "P002": ""})
    _, height_rejection = d.transition(height, h, dict(type="attach", partId="P002", candidate="P002:raised"))
    assert height_rejection["code"] == "DISCONNECTED_ASSEMBLY"
    cap = dict(c, rackCapacity=1)
    _, capacity_rejection = d.transition(cap, s, dict(type="detach", partId="P002"))
    assert capacity_rejection["code"] == "RACK_FULL"
    e = Episode(d, "R010")
    e.replan(count=True)
    assert e.finish()["unnecessaryInterventionRate"] == 1
    e = Episode(d, "R007")
    e.diagnose([dict(partId="W006", type="wrong_color")])
    assert e.finish()["rootLocalizationAccuracy"] == 0
    (OUTPUT / "cases.json").write_text(json.dumps(d.cases, ensure_ascii=False, indent=2)+"\n")
    report = dict(schema="brickplan-repair-logical-validation/1", cases=results, blockedInsertion=v,
                  unsupportedHeightRejected=height_rejection, capacityRejected=capacity_rejection,
                  partialRootSetRejected=True, unnecessaryReplanDetected=True,
                  allPassed=True, certificateSha256=d.certificate["contentSha256"])
    (OUTPUT / "logical-validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({r["caseId"]: r["optimum"] for r in results}))


if __name__ == "__main__":
    validate()
