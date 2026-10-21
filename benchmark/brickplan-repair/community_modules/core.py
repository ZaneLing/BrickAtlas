"""Instruction-assisted module completion; frozen context is a rigid fixture.

Unknown background collision meshes are NOT removed: original visual AABBs
conservatively block every overlapping endpoint and swept path. Only accepted,
closed-mesh moving pieces can be operated. No whole-kit buildability claim.
"""
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
for path in ("benchmark/brickplan-v1", "benchmark/brickplan-repair",
             "benchmark/brickplan-repair/eval"):
    sys.path.insert(0, str(ROOT / path))
import numpy as np
from assembly import Assembly
from geometry import AXIS_INVERSE, bounds_separate, load_source, sha256, world_bounds
from library import Qualifier
from render import triangles

PROTOCOL = "ldraw-manual-module/2"
OUT = ROOT / "deliverables/brickplan-community-modules"


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def raw_part(row, index):
    raw = AXIS_INVERSE @ np.asarray(row["originalMatrix"]).reshape(4, 4).T
    return dict(sourceIndex=index, sourceInstanceId=row["instanceId"],
                partNumber=row["partNumber"], colorCode=row["colorCode"],
                colorHex=row["colorHex"], name=row["displayName"],
                rawMatrix=raw.tolist(), originalMatrix=row["originalMatrix"])


@lru_cache(maxsize=2048)
def visual_bounds(serialized):
    vertices = triangles(serialized)[0].reshape(-1, 3) * [1, -1, -1]
    return vertices.min(0), vertices.max(0)


def part_bounds(p):
    return visual_bounds(json.dumps(p, sort_keys=True))


class LocalQualifier(Qualifier):
    def connection(self, a, b):
        if bounds_separate(world_bounds(a), world_bounds(b), .05):
            return []
        return super().connection(a, b)


class ModuleAssembly(Assembly):
    def __init__(self, cert):
        super().__init__(cert)
        self.q = LocalQualifier()
        self.unknown = {a: tuple(np.asarray(b) for b in p["bounds"])
                        for a, p in cert["conservativeContext"].items()}
        self.board = np.eye(4)
        self.board[1, 3] = cert["tableY"]
        self.inverse_board = np.linalg.inv(self.board)

    def environment_blockers(self, part):
        bounds = world_bounds(part)
        hits = [a for a, other in self.unknown.items()
                if not bounds_separate(bounds, other)]
        if bounds[1][1] > self.cert["tableY"] + .002:
            hits.append("white-table")
        return hits

    def environment_path_blockers(self, part, direction, length):
        lo, hi = world_bounds(part)
        delta = np.asarray(direction) * length
        swept = (np.minimum(lo, lo + delta), np.maximum(hi, hi + delta))
        hits = [a for a, other in self.unknown.items()
                if not bounds_separate(swept, other)]
        if swept[1][1] > self.cert["tableY"] + .002:
            hits.append("white-table")
        return hits

    def connections(self, state):
        # The already-built context is supplied as a fixture. Its internal
        # assembly history is outside this task. Every NEW connection is checked.
        parts = self.present(state)
        graph = {a: set() for a in parts}
        for a, key in state.items():
            if not key:
                continue
            for b, part in parts.items():
                if a != b and self.q.connection(parts[a], part):
                    graph[a].add(b)
                    graph[b].add(a)
        remaining, groups = set(parts), []
        while remaining:
            todo, found = [min(remaining)], set()
            while todo:
                a = todo.pop()
                if a in found:
                    continue
                found.add(a)
                todo.extend(graph[a] - found)
            groups.append(sorted(found))
            remaining -= found
        return graph, groups

    def anchored(self, state):
        _, groups = self.connections(state)
        return all(set(g) & self.anchor_ids for g in groups)

    def intervention(self, family, state, *, latest=None, placement_order=None):
        """Choose a feasible change from ACTUAL installed geometry, never a GT prefix.

        The incident and its inverse must both be legal. Choices are deterministic
        given the trajectory, and the newest piece is retained. Returned evidence
        is private; neither affected IDs nor recovery actions enter observations.
        """
        order = placement_order or {}
        earlier = sorted((a for a, k in state.items() if k and a.startswith('P') and a != latest),
                         key=lambda a: (order.get(a, 0), a))
        proposals = []
        if family in ('missing', 'wrong-color'):
            for actor in earlier:
                old = state[actor]
                changes = [dict(type='detach', actor=actor)]
                inverse = [dict(type='attach', actor=actor, candidate=old)]
                if family == 'wrong-color':
                    replacement = self.cert['colorReplacements'].get(old)
                    if not replacement or state[replacement['actor']]:
                        continue
                    changes.append(dict(type='attach', **replacement))
                    inverse.insert(0, dict(type='detach', actor=replacement['actor']))
                proposals.append((actor, changes, inverse))
        elif family == 'extra-layer' and not state.get('E'):
            for key, row in self.candidates.items():
                if row['actor'] != 'E':
                    continue
                if any(self.q.connection(row['part'], self.row(state[a])['part']) for a in earlier):
                    proposals.append(('E', [dict(type='attach', actor='E', candidate=key)],
                                      [dict(type='detach', actor='E')]))
        for affected, changes, inverse in proposals:
            trial, checks = dict(state), []
            for change in changes:
                trial, check = self.check(trial, change['actor'], change['type'],
                                          candidate=change.get('candidate'))
                checks.append(check)
                if check['code'] != 'OK':
                    break
            else:
                if not self.anchored(trial):
                    continue
                recovery, recovery_checks = dict(trial), []
                for undo in inverse:
                    recovery, check = self.check(recovery, undo['actor'], undo['type'],
                                                candidate=undo.get('candidate'))
                    recovery_checks.append(check)
                    if check['code'] != 'OK':
                        break
                else:
                    if self.signature(recovery) == self.signature(state):
                        return dict(family=family, affected=affected, changes=changes,
                                    recovery=inverse, before=dict(state), after=trial,
                                    checks=checks, recoveryChecks=recovery_checks)
        return None


def render_certificate(cert):
    visual = deepcopy(cert)
    visual["fixed"].update({a: p["part"] for a, p in cert["conservativeContext"].items()})
    return visual


def source_certificate(spec):
    manifest_path = ROOT / "web/public/models" / spec["model"] / "manifest.json"
    mf = json.loads(manifest_path.read_text())
    provenance = json.loads(manifest_path.with_name("provenance.json").read_text())
    if provenance.get("embeddedPartLockedPathConflicts"):
        raise ValueError("Embedded LDraw part conflicts require source-specific rendering")
    selected = set(spec["indices"])
    fixed, candidates, unknown, all_bounds = {}, {}, {}, []
    for i, row in enumerate(mf["instances"]):
        raw = raw_part(row, i)
        bounds = part_bounds(raw)
        all_bounds.append(bounds)
        try:
            parts, _, _ = load_source(spec["model"], [i])
            part = parts[0]
        except Exception as exc:
            if i in selected:
                raise ValueError(f"Unsupported moving part {spec['model']}:{i}") from exc
            unknown[f"U{i}"] = dict(part=raw, bounds=[v.tolist() for v in bounds],
                                   reason=str(exc)[:240])
            continue
        if i in selected:
            actor = f"P{i}"
            candidates[f"{actor}:goal"] = dict(actor=actor, kind="goal", part=part)
        else:
            fixed[f"F{i}"] = part
    return dict(protocol=PROTOCOL, id=spec["id"], checkpoint=spec.get("checkpoint", 3),
                fixed=fixed, candidates=candidates,
                conservativeContext=unknown, tableY=max(b[1][1] for b in all_bounds) + .1,
                extractionLengthLDU=240, source=dict(
                    modelId=spec["model"], author=spec["author"], url=spec["url"],
                    original=spec["original"], originalSha256=sha256(ROOT / spec["original"]),
                    manifestSha256=sha256(manifest_path), totalInstances=len(mf["instances"]),
                    moduleSourceIndices=spec["indices"], sourceGeometryModified=False,
                    license="Original OMR header: Redistributable under CCAL version 2.0",
                    contextRole="Preassembled rigid fixture; all original instances rendered.",
                    manualOrigin="New one-piece instruction sequence derived from exact source poses; not an official LEGO instruction booklet."))


class Episode:
    """One physical action per turn, immediate observation, hidden intervention.

    Public observation contains no current-pose map, error name, truth labels,
    trigger, or recovery witness. Image production is the adapter's responsibility.
    """
    def __init__(self, cert, case, seed=0):
        import random
        self.cert, self.case = cert, case
        self.runtime = ModuleAssembly(cert)
        self.runtime.goal = dict(case["goal"])
        self.state = dict(case["initial"])
        rng = random.Random(seed)
        actors, keys = list(self.runtime.actors), list(cert["candidates"])
        rng.shuffle(actors)
        rng.shuffle(keys)
        self.actor_alias = {a: f"A{i+1:02}" for i, a in enumerate(actors)}
        self.pose_alias = {k: f"C{i+1:03}" for i, k in enumerate(keys)}
        self.actors = {v: k for k, v in self.actor_alias.items()}
        self.poses = {v: k for k, v in self.pose_alias.items()}
        self.actions, self.inspections, self.event_applied = 0, 0, False
        self.done, self.history, self.feedback = False, [], None
        self.placement_order, self.successful_installs, self.last_event = {}, 0, None
        self.previous = None
        self.manipulation_budget = 4 * len(cert["source"]["moduleSourceIndices"]) + 12

    def observe(self):
        task = ("主体已装好。补完指定模块。说明书只是一种参考拼法，可以采用其他合法顺序；不比较中间状态与说明书。过程中积木可能发生未提示的变化，以每次返回的实际画面为准。"
                if self.case["mode"] == "dynamic" else
                "把当前状态修复成 acceptance-target 目标图。可以采用任何合法修复顺序；参考说明的步数只标识目标图，不规定你的操作顺序。")
        return dict(protocol=PROTOCOL,
                    task=task + "每次只能装或拆一块。完成后 finish。",
                    mode=self.case["mode"],
                    acceptanceStage=self.case["completedInstructionStep"] if self.case["mode"] == "static" else "final",
                    inputs=["fixed-final-target", "initial-context", "numbered-instructions",
                            "inventory", "before-last-action", "current-now"],
                    availableViews=["isometric", "rear", "top"],
                    manualAvailableThroughout=True, contextIsLocked=True,
                    orderPolicy="any-physically-legal-order", intermediateGTMatching=False,
                    actionsUsed=self.actions, inspectionsUsed=self.inspections,
                    manipulationBudget=self.manipulation_budget,
                    done=self.done, feedback=self.feedback,
                    handles=[dict(partId=self.actor_alias[a],
                                  candidates=sorted(self.pose_alias[k] for k, r in self.cert["candidates"].items()
                                                    if r["actor"] == a))
                             for a in sorted(self.actor_alias, key=self.actor_alias.get)],
                    actionSchema=dict(attach=["partId", "candidate"], detach=["partId"],
                                      inspect={"required": ["view"], "optionalOneOf": ["candidate", "partId"]},
                                      finish=[]))

    def step(self, action):
        if self.done:
            raise ValueError("Episode finished")
        if not isinstance(action, dict):
            raise ValueError("One action object is required")
        kind = action.get("type")
        fields = {"attach": {"type", "partId", "candidate"},
                  "detach": {"type", "partId"}, "inspect": {"type", "view"},
                  "finish": {"type"}}
        inspection_fields = ({"type", "view"}, {"type", "view", "candidate"},
                             {"type", "view", "partId"})
        if kind not in fields or (set(action) not in inspection_fields if kind == "inspect"
                                  else set(action) != fields[kind]):
            raise ValueError("Invalid action fields")
        if kind == "inspect":
            if action["view"] not in ("isometric", "rear", "top"):
                raise ValueError("Unknown view")
            if "candidate" in action and action["candidate"] not in self.poses:
                raise ValueError("Unknown candidate")
            if "partId" in action and action["partId"] not in self.actors:
                raise ValueError("Unknown part")
            self.inspections += 1
            self.feedback = dict(code="INSPECT", **{k: v for k, v in action.items() if k != "type"})
            return self.observe()
        if kind == "finish":
            self.done = True
            self.feedback = dict(code="FINISHED")
            return self.observe()
        if self.actions >= self.manipulation_budget:
            raise ValueError("Manipulation budget exhausted")
        actor = self.actors.get(action["partId"])
        if actor is None:
            raise ValueError("Unknown part")
        key = self.poses.get(action.get("candidate")) if kind == "attach" else None
        if kind == "attach" and key is None:
            raise ValueError("Unknown candidate")
        before = dict(self.state)
        after, result = self.runtime.check(self.state, actor, kind, candidate=key)
        self.actions += 1
        self.previous = before
        self.state = after
        self.feedback = dict(code=result["code"])
        if result['code'] == 'OK' and kind == 'attach':
            self.successful_installs += 1
            self.placement_order[actor] = self.successful_installs
        event = self.case.get("event")
        injected = False
        # Occupancy threshold and actual physical feasibility; no target-state or
        # reference-order predicate is involved in deciding whether to intervene.
        if (event and not self.event_applied and result["code"] == "OK"
                and sum(bool(k) for a,k in self.state.items() if a.startswith('P')) >= event['minimumInstalled']):
            incident = self.runtime.intervention(event['family'], self.state,
                latest=actor if kind == 'attach' else None, placement_order=self.placement_order)
            if incident:
                self.state = dict(incident['after'])
                self.last_event = incident
                self.event_applied = injected = True
        self.history.append(dict(action=action, result=result, before=before,
                                 after=dict(self.state), eventApplied=injected,
                                 intervention=self.last_event if injected else None))
        return self.observe()

    def score(self):
        correct = self.runtime.complete(self.state)
        opportunity = not self.case.get("event") or self.event_applied
        return dict(finalGeometryCorrect=correct, finished=self.done,
                    eventApplied=self.event_applied, interventionOpportunity=opportunity,
                    success=self.done and correct,
                    completionSuccess=self.done and correct,
                    repairSuccess=(self.done and correct) if self.case.get('event') and self.event_applied else None,
                    intermediateStateComparedToGT=False,
                    acceptedActionsPhysicallyChecked=True,
                    manipulations=self.actions, inspections=self.inspections,
                    scope="Instruction-assisted module completion; no full-kit or force-simulation claim.")
