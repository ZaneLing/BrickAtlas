"""Build source-exact, instruction-assisted community module cases."""
from copy import deepcopy
import json
from pathlib import Path
import re
import shutil
import sys
import time

from core import (ROOT, OUT, ModuleAssembly, Episode, dump, render_certificate,
                  source_certificate, sha256, PROTOCOL)
from specs import SPECS
import numpy as np
from library import substitute, transformed
from render import PALETTE
from dynamic_v5.vision import DynamicVisionRenderer
from PIL import Image, ImageFilter

VIEWS = ("isometric", "rear", "top")
ERRORS = {"missing": "少了一块", "wrong-color": "换成了另一种颜色", "extra-layer": "多叠了一块"}


def checked(rt, state, actions):
    states, evidence = [dict(state)], []
    for action in actions:
        state, result = rt.check(state, action["actor"], action["type"],
                                 candidate=action.get("candidate"))
        if result["code"] != "OK" or not rt.anchored(state):
            raise AssertionError((action, result))
        states.append(dict(state))
        evidence.append(result)
    return state, states, evidence


def attach(actor, key=None):
    return dict(type="attach", actor=actor, candidate=key or actor + ":goal")


def detach(actor):
    return dict(type="detach", actor=actor)


def relocated(part, raw):
    p = deepcopy(part)
    raw = np.asarray(raw)
    alias = np.linalg.inv(np.asarray(p['rawMatrix'])) @ np.asarray(p['matrix'])
    p.update(rawMatrix=raw.tolist(), matrix=(raw @ alias).tolist(), direction=(-raw[:3, 1]).tolist())
    return p


def add_variants(cert, normal):
    # All conditions receive the SAME inventory and candidate catalogue.
    # Identical physical pieces can exchange roles; actor identity is not GT.
    actors = [a['actor'] for a in normal]
    originals = {a: cert['candidates'][a + ':goal']['part'] for a in actors}
    cert['colorReplacements'] = {}
    for actor, p in originals.items():
        for other, target in originals.items():
            if other != actor and (p['partNumber'], p['colorHex']) == (target['partNumber'], target['colorHex']):
                cert['candidates'][f'{actor}:exchange:{other}'] = dict(
                    actor=actor, kind='alternative', part=relocated(p, target['rawMatrix']))
        for j, delta in enumerate(([20, 0, 0], [-20, 0, 0])):
            cert['candidates'][f'{actor}:offset{j}'] = dict(
                actor=actor, kind='alternative', part=transformed(p, delta=delta))
    for key, row in list(cert['candidates'].items()):
        actor, p = row['actor'], row['part']
        color = ('14', '#F2CD37') if p['colorCode'] != '14' else ('4', '#C91A09')
        spare, spare_key = 'W_' + actor, 'W_' + key
        cert['candidates'][spare_key] = dict(actor=spare, kind='spare',
            part=substitute(p, p['partNumber'], color))
        cert['colorReplacements'][key] = dict(actor=spare, candidate=spare_key)
    # Connector-derived poses, including rotated studs. Keep several different
    # mounting options so a different legal build order still gets an incident.
    from assembly import Assembly
    prototype = substitute(originals[actors[0]], '3024', ('4', '#C91A09'))
    rotations = [np.eye(3), np.diag([1,-1,-1]),
                 np.array([[1,0,0],[0,0,-1],[0,1,0]]),
                 np.array([[1,0,0],[0,0,1],[0,-1,0]]),
                 np.array([[0,-1,0],[1,0,0],[0,0,1]]),
                 np.array([[0,1,0],[-1,0,0],[0,0,1]])]
    seen = set()
    for parent, part in originals.items():
        local = Assembly(dict(fixed={'anchor': part}, candidates={
            'E:prototype': dict(actor='E', kind='spare', part=prototype)}, extractionLengthLDU=240))
        accepted = 0
        for rotation in rotations:
            for pose in local.snaps({'E': ''}, 'E', rotation):
                raw = pose['rawMatrix']
                token = tuple(np.round(raw, 4).ravel())
                if token in seen:
                    continue
                trial = relocated(prototype, raw)
                if local.q.endpoint(trial, part)['status'] != 'CLEAR' or not local.q.connection(trial, part):
                    continue
                key = f'E:mount:{parent}:{accepted}'
                cert['candidates'][key] = dict(actor='E', kind='spare', part=trial, mount=parent)
                rt = ModuleAssembly(cert)
                state = {a: '' for a in rt.actors}
                state[parent] = parent + ':goal'
                _, result = rt.check(state, 'E', 'attach', candidate=key)
                if result['code'] != 'OK':
                    del cert['candidates'][key]
                    continue
                seen.add(token)
                accepted += 1
                if accepted >= 12:
                    break
            if accepted >= 12:
                break
    if not seen:
        raise AssertionError((cert['id'], 'No qualified extra-layer pose'))


def dynamic_replay(cert, case, normal):
    ep = Episode(cert, case)
    actions = []
    for action in normal:
        ep.step(public_action(ep, action))
        assert ep.feedback['code'] == 'OK', (case['id'], action, ep.feedback)
        actions.append(action)
        if ep.history[-1]['eventApplied']:
            for undo in ep.last_event['recovery']:
                ep.step(public_action(ep, undo))
                assert ep.feedback['code'] == 'OK'
                actions.append(undo)
    ep.step({'type': 'finish'})
    assert ep.score()['success'], (case['id'], ep.score())
    return ep, actions


def case_bank(cert, normal):
    rt = ModuleAssembly(cert)
    initial = {a: '' for a in rt.actors}
    goal, manual_states, manual_evidence = checked(rt, initial, normal)
    # Pick a demonstrated checkpoint where every family is feasible. This
    # number is a minimum installed COUNT, never an exact reference prefix.
    for cp in range(cert['checkpoint'], len(normal)+1):
        prefix = manual_states[cp]
        order = {a['actor']: i for i, a in enumerate(normal[:cp])}
        perturbations = {f: rt.intervention(f, prefix, latest=normal[cp-1]['actor'],
                                            placement_order=order) for f in ERRORS}
        if all(perturbations.values()):
            cert['checkpoint'] = cp
            break
    else:
        raise AssertionError((cert['id'], 'No common feasible checkpoint'))
    cases = []
    def entry(mode, error, current, expected, event, witness):
        cid = cert['id'] + '-' + mode + '-' + error
        repaired, states, checks = checked(rt, current, witness)
        assert rt.signature(repaired) == rt.signature(expected), 'Incorrect recovery witness'
        return dict(id=cid, module=cert['id'], mode=mode, family=error,
                    initial=current, goal=expected, completedInstructionStep=cp if mode == 'static' else 0,
                    event=event, referenceActions=witness, referenceStates=states,
                    referenceChecks=checks)
    cases.append(entry('static', 'control', prefix, prefix, None, []))
    cases.append(entry('dynamic', 'control', initial, goal, None, normal))
    for error, incident in perturbations.items():
        affected = incident['affected']
        incident['affectedInstruction'] = next((i for i, a in enumerate(normal, 1)
                                                if a['actor'] == affected), None)
        if error == 'extra-layer':
            key = incident['changes'][0]['candidate']
            incident['extraParent'] = cert['candidates'][key]['mount']
        cases.append(entry('static', error, incident['after'], prefix, None, incident['recovery']))
        case = dict(id=cert['id']+'-dynamic-'+error, module=cert['id'], mode='dynamic', family=error,
                    initial=initial, goal=goal, completedInstructionStep=0,
                    event=dict(family=error, minimumInstalled=cp, policy='actual-state-feasible'))
        ep, actions = dynamic_replay(cert, case, normal)
        assert ep.event_applied
        case.update(referenceActions=actions, referenceStates=[initial]+[r['after'] for r in ep.history],
                    referenceChecks=[r['result'] for r in ep.history], replayScore=ep.score(),
                    referenceIncident=ep.last_event,
                    eventFrame=next(i for i,r in enumerate(ep.history,1) if r['eventApplied']))
        cases.append(case)
    return cases, manual_states, manual_evidence, perturbations


def order_checks(cert, cases, normal):
    rt = ModuleAssembly(cert)
    initial = {a: '' for a in rt.actors}
    _, reference_states, _ = checked(rt, initial, normal)
    checkpoint = cert['checkpoint']
    candidates = []
    # Prefer crossing the incident threshold with a DIFFERENT physical prefix.
    # Merely swapping the first two actions and rejoining before the incident
    # would not exercise the former exact-prefix-trigger bug.
    for distance in range(1, len(normal)):
        for i in range(len(normal)-distance):
            trial = list(normal)
            trial[i], trial[i+distance] = trial[i+distance], trial[i]
            candidates.append(trial)
    alternative, alternative_states, fallback = None, None, None
    for trial in candidates:
        try:
            _, states, _ = checked(rt, initial, trial)
        except AssertionError:
            continue
        # Select an alternate demonstration that actually exercises all three
        # errors. Other legal routes still count as completion even if no
        # feasible intervention opportunity arises.
        feasible = all(any(rt.intervention(family, states[k], latest=trial[k-1]['actor'],
            placement_order={a['actor']:j for j,a in enumerate(trial[:k])})
            for k in range(checkpoint,len(trial)+1)) for family in ERRORS)
        if not feasible:
            continue
        if fallback is None:
            fallback = (trial, states)
        if rt.signature(states[checkpoint]) != rt.signature(reference_states[checkpoint]):
            alternative, alternative_states = trial, states
            break
    if alternative is None and fallback:
        alternative, alternative_states = fallback
    assert alternative is not None, (cert['id'], 'No alternate route found')
    rows = []
    for case in cases:
        if case['mode'] != 'dynamic':
            continue
        ep, _ = dynamic_replay(cert, case, alternative)
        assert not case['event'] or ep.event_applied, (case['id'], 'Alternate route did not receive incident')
        rows.append(dict(case=case['id'], score=ep.score(),
                         eventCount=sum(r['eventApplied'] for r in ep.history),
                         incidentBeforeDiffersFromReferencePrefix=(
                             rt.signature(ep.last_event['before']) != rt.signature(reference_states[checkpoint])
                             if ep.last_event else None)))
        assert sum(r['eventApplied'] for r in ep.history) == int(bool(case['event']))
    # A failed physical action cannot teleport a brick or count as progress.
    control = next(c for c in cases if c['mode']=='dynamic' and c['family']=='control')
    ep = Episode(cert, control)
    ep.step(public_action(ep, normal[0]))
    before = dict(ep.state)
    ep.step(public_action(ep, normal[0]))
    assert ep.feedback['code']=='ALREADY_INSTALLED' and ep.state==before and ep.successful_installs==1
    replacement=cert['colorReplacements'][normal[0]['candidate']]
    after, feedback=rt.check(before,replacement['actor'],'attach',candidate=replacement['candidate'])
    assert feedback['code']=='ENDPOINT_COLLISION' and after==before
    ep.step({'type':'finish'})
    assert not ep.score()['success'], 'Incomplete shape was accepted'
    floating = np.array(cert['candidates'][normal[1]['candidate']]['part']['rawMatrix'])
    floating[:3,3] += [2000,-2000,2000]
    after, feedback = rt.check(initial, normal[1]['actor'], 'attach', raw=floating)
    assert feedback['code']=='NO_CONNECTION' and after==initial
    # Main completion does not fail merely because no intervention was possible.
    deferred = deepcopy(control)
    deferred['event'] = dict(family='missing', minimumInstalled=len(normal)+1)
    ep, _ = dynamic_replay(cert, deferred, alternative)
    assert ep.score()['success'] and ep.score()['repairSuccess'] is None and not ep.event_applied
    # Interchangeable identical parts must not be judged by their private IDs.
    swaps = []
    for i, a in enumerate(normal):
        for j, b in enumerate(normal[i+1:], i+1):
            ka, kb = a['actor']+':exchange:'+b['actor'], b['actor']+':exchange:'+a['actor']
            if ka in cert['candidates'] and kb in cert['candidates']:
                trial = list(normal)
                trial[i] = attach(b['actor'], kb)
                trial[j] = attach(a['actor'], ka)
                ep, _ = dynamic_replay(cert, control, trial)
                swaps.append(dict(actors=[a['actor'], b['actor']], score=ep.score()))
                break
        if swaps:
            break
    return dict(status='PASS', referenceOrder=[a['actor'] for a in normal],
                alternateOrder=[a['actor'] for a in alternative], alternateReplays=rows,
                interchangeablePieceReplays=swaps, noEventCompletion='PASS',
                differentPhysicalPrefixAtThreshold=(
                    rt.signature(alternative_states[checkpoint]) != rt.signature(reference_states[checkpoint])),
                duplicateAttachRejected=True, floatingAttachRejected=True,
                overlappingAttachRejected=True, incompleteFinishRejected=True)


def public_action(ep, action):
    result = dict(type=action["type"], partId=ep.actor_alias[action["actor"]])
    if action["type"] == "attach":
        result["candidate"] = ep.pose_alias[action["candidate"]]
    return result


def protocol_checks(cert, cases):
    rows = []
    for case in cases:
        ep = Episode(cert, case, seed=97)
        ep.runtime.goal = dict(case["goal"])
        obs = ep.observe()
        forbidden = {"event", "family", "goal", "initial", "referenceActions", "requiredState"}
        assert not forbidden.intersection(obs)
        prior = dict(ep.state)
        ep.step(dict(type="inspect", view="top"))
        assert ep.state == prior and ep.actions == 0 and not ep.event_applied
        for action in case["referenceActions"]:
            ep.step(public_action(ep, action))
            assert ep.feedback["code"] == "OK"
        ep.step(dict(type="finish"))
        assert ep.score()["success"], (case["id"], ep.score())
        rows.append(dict(case=case["id"], replay="PASS", score=ep.score()))
    return rows


def paint_outline(image, mask, actor_id):
    binary = Image.fromarray(np.uint8(mask == actor_id) * 255)
    border = Image.fromarray(np.maximum(
        np.asarray(binary.filter(ImageFilter.MaxFilter(7)), dtype=np.int16)
        - np.asarray(binary, dtype=np.int16), 0).astype("uint8"))
    image = image.copy()
    image.paste((255, 129, 20), (0, 0), border)
    return image


def render_module(spec, cert, normal, states, perturbations, cases, directory):
    rt = ModuleAssembly(cert)
    checkpoint = cert["checkpoint"]
    renderer = DynamicVisionRenderer(render_certificate(cert), runtime=rt)
    # Fixed module framing: same for every state, view and intervention.
    goal_keys = [a["candidate"] for a in normal]
    pts = np.concatenate([renderer.bounds[k] for k in goal_keys])
    lo, hi = pts.min(0) - [20, 28, 20], pts.max(0) + [20, 20, 20]
    renderer.bounds["_module_frame"] = np.array(
        [[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
    frame = ["_module_frame"]
    image_dir = directory / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    images = {}
    state_images = {}
    token = lambda state: json.dumps(state, sort_keys=True)
    def save(name, state, view="isometric", close=True, highlight=None, only=None):
        im, mask = renderer.rgb(state, view, size=(900, 660), supersample=1,
                                frame_keys=frame if close and only is None else None, only=only)
        if highlight:
            im = paint_outline(im, mask, renderer.ids[highlight])
        filename = name + ".png"
        im.save(image_dir / filename, optimize=True)
        images[name] = dict(file=f"{spec['id']}/images/{filename}",
                            sha256=sha256(image_dir / filename), view=view,
                            width=900, height=660)
        if highlight:
            images[name]["instructionVisiblePixels"] = int(np.count_nonzero(mask == renderer.ids[highlight]))
        return im
    save("full-initial", states[0], close=False)
    save("full-final", states[-1], close=False)
    for view in VIEWS:
        save("initial-" + view, states[0], view)
        save("final-" + view, states[-1], view)
        save("checkpoint-" + view, states[checkpoint], view)
    state_images[token(states[0])] = {v: images["initial-" + v]["file"] for v in VIEWS}
    state_images[token(states[checkpoint])] = {v: images["checkpoint-" + v]["file"] for v in VIEWS}
    manual = []
    for step, action in enumerate(normal, 1):
        actor = action["actor"]
        for view in VIEWS:
            save(f"step{step:02}-{view}", states[step], view, highlight=actor)
            save(f"plain{step:02}-{view}", states[step], view)
        state_images[token(states[step])] = {v: images[f"plain{step:02}-{v}"]["file"] for v in VIEWS}
        save(f"part{step:02}", {actor: action["candidate"]}, only=actor)
        p = cert["candidates"][action["candidate"]]["part"]
        visible = {v: images[f"step{step:02}-{v}"]["instructionVisiblePixels"] for v in VIEWS}
        if max(visible.values()) < 128:
            raise AssertionError(("New instruction piece not visible", spec["id"], step, visible))
        manual.append(dict(step=step, sourceIndex=p["sourceIndex"], partNumber=p["partNumber"],
                           color=p["colorHex"], partImage=images[f"part{step:02}"]["file"],
                           visiblePixels=visible,
                           after={v: images[f"step{step:02}-{v}"]["file"] for v in VIEWS}))
    visibility = []
    for family, change in perturbations.items():
        pixel_counts = {}
        for view in VIEWS:
            im = save(f"{family}-{view}", change["after"], view)
            expected = Image.open(image_dir / f"checkpoint-{view}.png")
            diff = np.max(np.abs(np.asarray(im, dtype=np.int16)
                                 - np.asarray(expected, dtype=np.int16)), axis=2)
            pixel_counts[view] = int(np.count_nonzero(diff >= 24))
        visibility.append(dict(family=family, changedPixels=pixel_counts,
                               passed=max(pixel_counts.values()) >= 128,
                               threshold=24, minimumPixels=128,
                               scope="Exterior RGB, fixed module crop, no error highlight; machine pixel visibility only."))
        state_images[token(change["after"])] = {v: images[f"{family}-{v}"]["file"] for v in VIEWS}
    if not all(r["passed"] for r in visibility):
        raise AssertionError(("Invisible intervention", spec["id"], visibility))
    timelines = {}
    for case in cases:
        if case["mode"] != "dynamic":
            continue
        frames = []
        for i, state in enumerate(case["referenceStates"]):
            key = token(state)
            if key not in state_images:
                name = "state-" + __import__("hashlib").sha256(key.encode()).hexdigest()[:16]
                for view in VIEWS:
                    save(name + "-" + view, state, view)
                state_images[key] = {v: images[name + "-" + v]["file"] for v in VIEWS}
            label = "起始状态：主体已搭好，模块还没开始"
            if i:
                action = case["referenceActions"][i-1]
                if action in normal:
                    number = normal.index(action) + 1
                    label = f"装入说明书第 {number} 块后"
                else:
                    label = "拆下多出来或颜色不对的积木后"
                if case["event"] and i == case.get("eventFrame"):
                    label += "（此时后台发生了干扰）"
            frames.append(dict(label=label, images=state_images[key],
                               event=bool(case["event"] and i == case.get("eventFrame"))))
        timelines[case["family"]] = frames
    return images, manual, visibility, timelines


def main():
    started = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    dump(OUT / "audit.json", dict(protocol=PROTOCOL, status="BUILDING"))
    config = (ROOT / "assets-source/ldraw-library/locked/LDConfig.ldr").read_text()
    for code, color in re.findall(r"CODE\s+(\d+)\s+VALUE\s+(#[0-9A-Fa-f]{6})", config):
        PALETTE[code] = color
    public, audit, all_cases = [], [], []
    for spec in SPECS:
        print("Building", spec["id"], flush=True)
        directory = OUT / spec["id"]
        directory.mkdir(parents=True, exist_ok=True)
        cert = source_certificate(spec)
        normal = [attach(f"P{i}") for i in spec["indices"]]
        # Verify initial source order before inventing any perturbation.
        rt = ModuleAssembly(cert)
        checked(rt, {a: "" for a in rt.actors}, normal)
        add_variants(cert, normal)
        cases, states, evidence, changes = case_bank(cert, normal)
        order_evidence = order_checks(cert, cases, normal)
        dump(directory / "order-checks.json", order_evidence)
        replay = protocol_checks(cert, cases)
        imgs, manual, visibility, timelines = render_module(
            spec, cert, normal, states, changes, cases, directory)
        dump(directory / "certificate.private.json", cert)
        dump(directory / "cases.private.json", cases)
        dump(directory / "manual.private.json", dict(actions=normal, states=states, checks=evidence))
        dump(directory / "perturbations.private.json", changes)
        dump(directory / "image-manifest.json", imgs)
        shutil.copyfile(ROOT / spec["original"], directory / "original.mpd")
        dump(directory / "provenance.json", cert["source"])
        public.append(dict(**spec, total=cert["source"]["totalInstances"],
                           remaining=len(normal), fixed=cert["source"]["totalInstances"] - len(normal),
                           conservativeContext=len(cert["conservativeContext"]),
                           manual=manual, images=imgs, staticStage=cert["checkpoint"],
                           orderChecks=order_evidence, perturbations=changes,
                           inventoryCount=len(ModuleAssembly(cert).actors),
                           timelines=timelines,
                           cases=[{k: c[k] for k in ("id", "mode", "family")} for c in cases]))
        audit.append(dict(module=spec["id"], manualSteps=len(normal), manualReplay="PASS",
                          instructionVisibility=[dict(step=r["step"], pixels=r["visiblePixels"]) for r in manual],
                          sourceContextComplete=True, immutableContextCount=cert["source"]["totalInstances"]-len(normal),
                          conservativeContextCount=len(cert["conservativeContext"]),
                          conservativePolicy="Overlapping original AABB rejects endpoint and swept path; never omitted.",
                          deferredModuleIndices=spec["omitted"], visibility=visibility, replays=replay,
                          orderChecks=order_evidence))
        all_cases.extend(cases)
        print("PASS", spec["id"], "steps", len(normal), "cases", len(cases), flush=True)
    dump(OUT / "gallery-data.js.json", public)
    (OUT / "data.js").write_text("window.MODULES=" + json.dumps(public, ensure_ascii=False) + ";\n")
    shutil.copyfile(Path(__file__).with_name("index.html"), OUT / "index.html")
    dump(OUT / "audit.json", dict(protocol=PROTOCOL, status="PASS", modules=len(public),
                                 cases=len(all_cases), apiModelCalls=0, humanValidationCount=0,
                                 seconds=round(time.time()-started, 2), results=audit))
    (OUT / "cases.private.jsonl").write_text(
        "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in all_cases))
    import importlib.util
    doc_spec = importlib.util.spec_from_file_location("module_catalogue", Path(__file__).with_name("catalogue.py"))
    docs = importlib.util.module_from_spec(doc_spec)
    doc_spec.loader.exec_module(docs)
    docs.main()
    dependencies = [Path(__file__), Path(__file__).with_name("catalogue.py"),
                    Path(__file__).with_name("validate.py"), Path(__file__).with_name("core.py"),
                    Path(__file__).with_name("specs.py"), Path(__file__).with_name("index.html"),
                    Path(__file__).with_name("run_episode.py"),
                    Path(__file__).with_name("preview_server.py"),
                    ROOT / "benchmark/brickplan-v1/geometry.py",
                    ROOT / "benchmark/brickplan-repair/assembly.py",
                    ROOT / "benchmark/brickplan-repair/library.py",
                    ROOT / "benchmark/brickplan-repair/eval/vision.py",
                    ROOT / "benchmark/brickplan-repair/eval/render.py",
                    ROOT / "benchmark/brickplan-repair/dynamic_v5/vision.py",
                    ROOT / "assets-source/ldraw-library/locked/LDConfig.ldr"]
    dump(OUT / "source-manifest.json", {
        str(p.relative_to(ROOT)): sha256(p) for p in dependencies})
    print("DONE", len(public), "modules", len(all_cases), "cases", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        dump(OUT / "audit.json", dict(protocol=PROTOCOL, status="FAIL", error=str(exc)))
        raise
