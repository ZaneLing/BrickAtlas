"""Practice-only, bilingual question descriptions; no answer labels in previews."""
import copy
from collections import Counter

from bank import make_mission, task_bank, task_by_id
from probes import Probe, probe_by_id
from mission import canonical_hash
from session import Session


def bi(zh, en):
    return {"zh": zh, "en": en}


TAXONOMY = [
    {"id": "assembly", "number": "01", "name": bi("装配与重构", "Assembly & reconfiguration"),
     "question": bi("如何从当前结构到达目标结构？", "How do you transform the current assembly into the target?"),
     "given": bi("当前图、目标图、零件与位置 ID、暂存架容量。", "Current and target images, piece/site IDs and rack capacity."),
     "answer": bi("逐步提交安装、拆卸操作，最后结束。", "Submit attach/detach operations, then finish."),
     "score": bi("是否完成；实际操作数减最优操作数。", "Completion and excess operations over the exact optimum.")},
    {"id": "resource", "number": "02", "name": bi("有限资源调度", "Finite-resource scheduling"),
     "question": bi("暂存架快满了，先拆哪块、先装哪块？", "Which piece should move first when rack space is limited?"),
     "given": bi("当前与目标结构、暂存架占用、检修工单。", "Assemblies, occupied rack holders and inspection orders."),
     "answer": bi("提交操作序列，同时满足容量和工单约束。", "Execute a sequence satisfying capacity and work orders."),
     "score": bi("完成率、额外代价、非法操作与死路。", "Completion, excess cost, rejected actions and dead ends.")},
    {"id": "inspection", "number": "03", "name": bi("检修与历史状态", "Inspection & persistent state"),
     "question": bi("外形一样，检修进度不同，下一步会改变吗？", "Can identical assemblies require different actions after inspection?"),
     "given": bi("结构图片、尚未完成的离架检修工单及完成记录。", "Assembly images and the persistent off-assembly inspection ledger."),
     "answer": bi("拆卸指定零件，在暂存架检修，再按目标复装。", "Detach designated pieces, audit them on the rack, then restore the target."),
     "score": bi("结构与全部工单同时完成；重复操作计入代价。", "Both target and all orders must be complete; repeated operations count.")},
    {"id": "next-action", "number": "04", "name": bi("下一步决策", "Next-action judgment"),
     "question": bi("哪些当前合法动作能让总完成代价最小？", "Which currently legal action minimizes total completion cost?"),
     "given": bi("冻结的状态、目标、资源、工单与候选动作。", "A frozen checkpoint, goal, resources, ledger and candidate actions."),
     "answer": bi("从候选动作中选择一个。", "Select one candidate action."),
     "score": bi("选中任意最优候选即正确；报告条件额外代价。", "Any optimal candidate is correct; conditional excess is also reported.")},
    {"id": "continuation", "number": "05", "name": bi("未来序列检查", "Future-sequence checking"),
     "question": bi("这串操作执行下去，第一次冲突发生在哪一步？", "Where does this proposed sequence first become illegal?"),
     "given": bi("当前状态与一段完整的候选操作序列。", "A checkpoint and a complete proposed action sequence."),
     "answer": bi("第一个非法操作的序号（从 1 开始），或“全部合法”。", "The first illegal index (1-based), or “all legal”."),
     "score": bi("精确匹配；同前缀、同首尾的配对题联合统计。", "Exact match; paired questions share prefixes and endpoint actions.")},
    {"id": "geometry", "number": "06", "name": bi("视觉几何与外观对照", "Visual geometry & appearance"),
     "question": bi("支撑结构改变会影响后续操作吗？只改颜色呢？", "Does changing support context alter the sequence? What about color alone?"),
     "given": bi("独立认证的原始几何上下文，或原色/灰度图片。", "Independently certified original geometry contexts, or color/grayscale images."),
     "answer": bi("判断序列第一次冲突的位置，或全部合法。", "Locate the first conflict, or indicate all legal."),
     "score": bi("几何对照要求答案改变；外观对照要求答案不变。", "Answer-changing geometry pairs and answer-invariant appearance pairs.")},
    {"id": "repair", "number": "07", "name": bi("延迟错误恢复", "Delayed error recovery"),
     "question": bi("犯错后又走了几步，怎样最省操作地回到正确路径？", "After an error and more actions, how do you return to an optimal path?"),
     "given": bi("错误前检查点、后续执行历史、当前状态与候选动作。", "Pre-error checkpoint, executed history, current state and candidates."),
     "answer": bi("选择最短恢复路径上的下一步。", "Choose the next action on a shortest repair path."),
     "score": bi("回到错误前任意最优路径的非终点状态；只到终点不算恢复。", "Rejoin a nonterminal state on any pre-error optimal path; the goal is excluded.")}
]


def category(task):
    if task["kind"] in ("unlimited-rack-control", "unlimited-rework-control", "visual-geometry-context"):
        return "assembly"
    if task["kind"] == "finite-rack-reconfiguration":
        return "resource"
    return "inspection"


def catalogue(arena):
    if arena.study:
        raise ValueError("Practice catalogue is unavailable in controlled study")
    bank = task_bank()
    tasks = {t["id"]: t for t in bank["episodes"]}
    probes = {p["id"]: p for p in bank["probes"]}
    profiles = {p["id"]: p for p in bank["profiles"]}
    visual_pairs = [p for p in bank["pairs"] if p["kind"] == "visual-geometry"]
    cohorts = {member: p["evaluationCohort"] for p in visual_pairs for member in p["members"]}
    rows = []
    for key, internal in arena.tasks.items():
        task = tasks[internal]
        rows.append(row(key, task, category(task), "episode", internal, task["kind"], profiles[task["profile"]]))
    for key, internal in arena.probe_ids.items():
        probe = probes[internal]
        kind = probe["kind"]
        cat = {"delayed-repair": "repair", "appearance-continuation": "geometry",
               "geometry-continuation": "geometry"}.get(kind, kind)
        task = tasks[probe["taskId"]]
        rows.append(row(key, task, cat, "probe", internal, kind, profiles[task["profile"]],
                        cohorts.get(internal, "")))
    counts = Counter(r["category"] for r in rows)
    cohort_rows = []
    for cohort, label, notice in (
        ("primary-matched", bi("主评测：匹配几何对照", "Primary matched geometry"),
         bi("零件数量、精确零件型号与颜色清单匹配的几何对照。只统计本组，不与历史回归题合并。",
            "Count-, part-number- and color-inventory-matched geometry pairs. Report separately from historical regressions.")),
        ("historical-unmatched-regression", bi("历史回归：非匹配对照", "Historical unmatched regression"),
         bi("保留的历史几何回归题，未满足主评测的完整清单匹配要求，不属于主评测。",
            "Preserved historical geometry regressions without the primary inventory-matching guarantee; not primary evaluation.")),
    ):
        selected = [r for r in rows if r["evaluationCohort"] == cohort]
        visible = {r["stableId"] for r in selected}
        cohort_rows.append({"id": cohort, "label": label, "notice": notice, "probes": len(selected),
                            "pairs": sum(p["evaluationCohort"] == cohort and set(p["members"]) <= visible
                                         for p in visual_pairs),
                            "sources": len({r["source"] for r in selected}),
                            "heldoutSources": len({r["source"] for r in selected if r["split"] == "heldout-source"})})
    visible = {r["stableId"] for r in rows}
    return {"release": "2.3", "bankHash": canonical_hash(bank), "questions": rows,
            "scope": "Practice-only catalogue metadata; never a policy observation or study input.",
            "cohorts": cohort_rows,
            "taxonomy": [{**c, "count": counts[c["id"]]} for c in TAXONOMY],
            "counts": {"episodes": len(arena.tasks), "probes": len(arena.probe_ids),
                       "sources": len({r["source"] for r in rows}),
                       "pairs": sum(set(p["members"]) <= visible for p in bank["pairs"])},
            "lengthNotice": bi("D1–D4 仅表示最优操作长度区间，不代表必需的思维深度。",
                               "D1–D4 describe optimal-operation-length bins, not necessary reasoning depth.")}


def row(key, task, cat, form, stable_id, kind, profile, cohort=""):
    return {"id": key, "stableId": stable_id, "category": cat, "form": form,
            "kind": kind, "source": task["sourceGroup"], "profile": task["profile"],
            "split": task["split"], "tier": task["tier"],
            "evaluationCohort": cohort,
            "provenance": {"introducedVersion": profile.get("introducedVersion", "pre-2.3"),
                           "sampling": profile["sampling"]},
            "lengthBin": {"D1": "1–8", "D2": "9–16", "D3": "17–24", "D4": "25+"}[task["tier"]]}


def preview(arena, key):
    if key in arena.probe_ids:
        value = Probe(probe_by_id(arena.probe_ids[key]), key, arena.seed, arena.identity).public(arena.render_images)
    else:
        task = task_by_id(arena.tasks[key])
        s = Session(make_mission(task), task, arena.seed, arena.track, render_images=arena.render_images,
                    identity={**arena.identity, "sessionId": "preview"})
        obs = s.observation()
        obs["taskId"] = key
        value = {"id": key, "kind": "episode", "observation": obs,
                 "question": "Match the target assembly and complete every off-assembly inspection within the action budget. Submit finish when done."}
    return value


def answer_review(arena, key):
    probe = arena.probe(key)
    if probe.answer is None:
        raise ValueError("Submit an answer before opening practice review")
    p = probe.probe
    if "choices" in p:
        correct = [probe.order.index(i) for i in p["optimalChoices"]]
        return {"correctChoices": sorted(correct), "scoringRole": p["scoringRole"],
                "correct": probe.answer["choice"] in p["optimalChoices"],
                "labels": [copy.deepcopy(p["labels"][i]) | {"action": probe.session.public_action(p["choices"][i])}
                           for i in probe.order]}
    return {"firstConflict": p["firstConflict"], "correct": probe.answer["firstConflict"] == p["firstConflict"]}
