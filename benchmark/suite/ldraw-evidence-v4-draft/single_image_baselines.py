#!/usr/bin/env python3
"""Deterministic Color baseline; stdin is ONE model-visible wire, stdout a prediction.

No project imports, paths, evaluator metadata, source records or paired inputs.
The CLI can be invoked in an empty cwd. Scoring is a separate evaluator.
"""
import base64
import io
import json
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

CONTRACT = {
    "name": "single-image-connected-color-v1",
    "access": "single-model-visible-PNG-and-text",
    "allowed_inputs": ["one PNG", "system text", "question", "identity contract", "options"],
    "color_prototypes": {"Red": [255, 0, 0], "Blue": [0, 0, 255],
                         "Yellow": [255, 255, 0], "Black": [0, 0, 0]},
    "white_min_channel": 0.90,
    "black_max_channel": 0.30,
    "chromatic_min_saturation": 0.35,
    "max_hue_distance_degrees": 60,
    "min_component_pixels": 64,
    "min_component_fraction": 0.0005,
    "winner_fraction": 0.55,
    "connectivity": 4,
    "tie_policy": "abstain",
    "failure_policy": "abstain on invalid input, no retained color region, or mixed colors",
    "scope": "Appearance sanity only; does not locate or read a target label.",
}


def decode_wire(wire):
    if set(wire) != {"messages"} or len(wire["messages"]) != 2:
        raise ValueError("one independent system/user wire required")
    system, user = wire["messages"]
    if set(system) != {"role", "content"} or system["role"] != "system" or not isinstance(system["content"], str):
        raise ValueError("invalid system message")
    if set(user) != {"role", "content"} or user["role"] != "user" or len(user["content"]) != 2:
        raise ValueError("one text and one PNG required")
    text, image = user["content"]
    if set(text) != {"type", "text"} or text["type"] != "text":
        raise ValueError("invalid text content")
    if set(image) != {"type", "image_url"} or image["type"] != "image_url":
        raise ValueError("invalid image content")
    if set(image["image_url"]) != {"url", "detail"} or image["image_url"]["detail"] != "high":
        raise ValueError("native high-detail PNG required")
    payload = json.loads(text["text"])
    if set(payload) != {"identity_contract", "question", "format", "options"}:
        raise ValueError("unexpected non-visible or missing payload field")
    if payload["format"] != "single-choice" or not all(isinstance(payload[k], str) for k in ["question", "identity_contract"]):
        raise ValueError("invalid question")
    options = payload["options"]
    if len(options) != 4 or any(set(o) != {"id", "label"} for o in options):
        raise ValueError("exactly four public options required")
    if len({o["id"] for o in options}) != 4 or {o["label"] for o in options} != set(CONTRACT["color_prototypes"]):
        raise ValueError("unsupported or duplicate options")
    prefix = "data:image/png;base64,"
    url = image["image_url"]["url"]
    if not url.startswith(prefix):
        raise ValueError("inline PNG only; file and network access forbidden")
    pixels = base64.b64decode(url[len(prefix):], validate=True)
    with Image.open(io.BytesIO(pixels)) as img:
        if img.format != "PNG":
            raise ValueError("PNG required")
        rgb = np.asarray(img.convert("RGB"), dtype=np.float64) / 255
    return rgb, options


def predict(wire):
    try:
        rgb, options = decode_wire(wire)
    except (KeyError, ValueError, TypeError, IndexError, OSError) as error:
        return {"choiceId": None, "status": "abstained", "reason": "invalid-input",
                "detail": str(error)}
    high, low = rgb.max(axis=2), rgb.min(axis=2)
    delta = high - low
    saturation = np.divide(delta, high, out=np.zeros_like(high), where=high > 0)
    white = low >= CONTRACT["white_min_channel"]
    black = (~white) & (high <= CONTRACT["black_max_channel"])
    chromatic = (~white) & (~black) & (saturation >= CONTRACT["chromatic_min_saturation"])
    hue = np.zeros_like(high)
    r, g, b = (rgb[:, :, i] for i in range(3))
    for channel, expression in [
        (0, np.divide(g-b, delta, out=np.zeros_like(high), where=delta > 0) % 6),
        (1, np.divide(b-r, delta, out=np.zeros_like(high), where=delta > 0) + 2),
        (2, np.divide(r-g, delta, out=np.zeros_like(high), where=delta > 0) + 4),
    ]:
        chosen = (rgb.argmax(axis=2) == channel) & (delta > 0)
        hue[chosen] = expression[chosen] * 60
    names, centers = ["Red", "Blue", "Yellow"], np.array([0, 240, 60])
    distances = np.abs((hue[:, :, None] - centers + 180) % 360 - 180)
    nearest = distances.argmin(axis=2)
    masks = {"Black": black}
    masks.update({name: chromatic & (nearest == i) & (distances[:, :, i] <= CONTRACT["max_hue_distance_degrees"])
                  for i, name in enumerate(names)})
    min_area = max(CONTRACT["min_component_pixels"],
                   int(np.ceil(high.size * CONTRACT["min_component_fraction"])))
    support = {}
    for name, mask in masks.items():
        labels, count = ndimage.label(mask)
        areas = np.bincount(labels.ravel(), minlength=count+1)[1:]
        support[name] = int(areas[areas >= min_area].sum())
    total = sum(support.values())
    ranked = sorted(support, key=lambda name: (-support[name], name))
    detail = {"support_pixels": support, "min_component_pixels": min_area}
    if not total:
        return {"choiceId": None, "status": "abstained", "reason": "no-color-region", **detail}
    if support[ranked[0]] == support[ranked[1]] or support[ranked[0]] / total < CONTRACT["winner_fraction"]:
        return {"choiceId": None, "status": "abstained", "reason": "mixed-colors", **detail}
    return {"choiceId": next(o["id"] for o in options if o["label"] == ranked[0]),
            "status": "predicted", "reason": None, "semantic_prediction": ranked[0], **detail}


if __name__ == "__main__":
    print(json.dumps(predict(json.load(sys.stdin)), sort_keys=True, allow_nan=False))
