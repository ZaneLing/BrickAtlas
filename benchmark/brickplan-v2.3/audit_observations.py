"""Native-resolution initial-input certificate for answer-changing visual pairs."""
import base64
import copy
import io

import numpy as np
from PIL import Image

from bank import DATA, task_bank, write_json
from mission import canonical_hash
from probes import Probe


def semantic(value, pixels=True):
    result = copy.deepcopy(value)
    result.pop("id", None)
    obs = result["observation"]
    for k in ("taskId", "sessionId"):
        obs.pop(k, None)
    if not pixels:
        obs.pop("images", None)
        for frame in obs["inspectionHistory"]:
            frame.pop("images", None)
    return result


def array(image):
    return np.asarray(Image.open(io.BytesIO(base64.b64decode(image["base64"])))).copy()


def main():
    bank = task_bank()
    probes = {p["id"]: p for p in bank["probes"]}
    identity = {"runId": "observation-certificate", "participantId": "software", "condition": "image-id"}
    rows = []
    for pair in bank["pairs"]:
        if pair["kind"] != "visual-geometry":
            continue
        a, b = [Probe(probes[i], "QAUDIT", 0, identity).public(True) for i in pair["members"]]
        views = []
        for value in (a, b):
            obs = value["observation"]
            views.append({"isometric": obs["images"], **{
                f["view"]: f["images"] for f in obs["inspectionHistory"]}})
        differences = {}
        for view in ("isometric", "left", "rear", "right"):
            differences[view] = {}
            for panel in views[0][view]:
                x, y = array(views[0][view][panel]), array(views[1][view][panel])
                differences[view][panel] = (int(np.any(x != y, axis=2).sum()) if x.shape == y.shape else
                                            {"differentDimensions": [list(x.shape), list(y.shape)]})
        reveals = [v for v, panels in differences.items() if any(bool(n) for n in panels.values())]
        row = {"pairId": pair["id"], "members": pair["members"],
               "answers": [probes[i]["firstConflict"] for i in pair["members"]],
               "sameSemanticText": semantic(a, False) == semantic(b, False),
               "differentStaticInput": canonical_hash(semantic(a)) != canonical_hash(semantic(b)),
               "differentPixels": differences, "revealingInitialViews": reveals,
               "activeDefaultAmbiguous": not any(bool(n) for n in differences["isometric"].values()),
               "passed": bool(reveals)}
        rows.append(row)
        write_json(DATA / "observation-certificate.json", {
            "schema": "brickplan-observation-certificate/2.3",
            "bankHash": canonical_hash(bank), "identitySeed": 0,
            "initialViews": ["isometric", "left", "rear", "right"],
            "mainPanelDimensions": [1920, 1440],
            "pairsChecked": len(rows), "complete": False, "pairs": rows})
        print("OBSERVATION", pair["id"], "revealing", reveals, flush=True)
    assert rows and all(r["passed"] and r["differentStaticInput"] for r in rows)
    write_json(DATA / "observation-certificate.json", {
        "schema": "brickplan-observation-certificate/2.3",
        "bankHash": canonical_hash(bank), "identitySeed": 0, "complete": True,
        "initialViews": ["isometric", "left", "rear", "right"],
        "mainPanelDimensions": [1920, 1440], "pairsChecked": len(rows), "pairs": rows,
        "scope": "Pixel distinguishability at the initial checkpoint, not a human/model answerability study. Static mode supplies all four fixed views; active mode starts isometric and charges one acquisition per inspect."})


if __name__ == "__main__":
    main()
