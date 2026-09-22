"""Frozen legal pixel/text binding rules, optionally composed with exact repair."""
import random
from functools import lru_cache

import numpy as np
from PIL import Image

from common import ASSETS, ROOT, digest
from evaluate import solve

SHAPE_BOXES = [(560, 80, 480, 300), (1070, 80, 480, 300),
               (560, 480, 480, 300), (1070, 480, 480, 300)]
LABEL_BOXES = [(x + 130, y + 307, 220, 50) for x, y, _, _ in SHAPE_BOXES]
REFERENCE_BOX = (20, 260, 480, 300)


def crop(image, box):
    x, y, w, h = box
    return image[y:y+h, x:x+w]


def normalize_glyph(mask):
    ys, xs = np.where(mask)
    if not len(xs):
        return np.zeros((28, 20))
    return np.asarray(Image.fromarray((mask[ys.min():ys.max()+1, xs.min():xs.max()+1] * 255).astype("uint8"))
                      .resize((20, 28), Image.Resampling.NEAREST)) > 0


@lru_cache(maxsize=1)
def font_templates():
    image = np.asarray(Image.open(ASSETS / "font-calibration.png").convert("RGB"))
    return {char: normalize_glyph(np.any(image[:, i*32:(i+1)*32] < 120, axis=2))
            for i, char in enumerate("V0123456789")}


def read_label(image):
    mask = np.any(image < 120, axis=2)
    active = mask.any(axis=0)
    starts = np.flatnonzero(active & ~np.r_[False, active[:-1]])
    ends = np.flatnonzero(active & ~np.r_[active[1:], False]) + 1
    templates = font_templates()
    letters = []
    for start, end in zip(starts, ends):
        glyph = normalize_glyph(mask[:, start:end])
        letters.append(min(templates, key=lambda c: np.mean(glyph != templates[c])))
    return "".join(letters)


def shape_descriptor(image):
    mask = np.any(image < 242, axis=2)
    ys, xs = np.where(mask)
    if not len(xs):
        return np.zeros(8)
    width, height = xs.max()-xs.min()+1, ys.max()-ys.min()+1
    xx, yy = (xs-xs.mean())/480, (ys-ys.mean())/300
    eig = np.linalg.eigvalsh(np.cov(np.stack((xx, yy))))
    return np.array([len(xs)/144000, width/480, height/300,
                     len(xs)/(width*height), eig[0], eig[1],
                     abs((xx**3).mean()), abs((yy**3).mean())])


def appearance_descriptor(image):
    # Public pixels only: foreground RGB histogram plus occupied area.
    mask = np.any(image < 242, axis=2)
    rgb = image[mask]
    hist = np.concatenate([np.histogram(rgb[:, i], bins=8, range=(0, 256))[0]
                           for i in range(3)]).astype(float)
    hist /= max(hist.sum(), 1)
    return np.r_[hist, mask.mean()]


@lru_cache(maxsize=1024)
def image_bindings(image_path):
    image = np.asarray(Image.open(ROOT / image_path).convert("RGB"))
    labels = [read_label(crop(image, b)) for b in LABEL_BOXES]
    result = {"card_first": labels[0]}
    for method, descriptor in (("silhouette", shape_descriptor), ("appearance", appearance_descriptor)):
        ref = descriptor(crop(image, REFERENCE_BOX))
        distances = [float(np.linalg.norm(ref - descriptor(crop(image, b)))) for b in SHAPE_BOXES]
        result[method] = labels[min(range(4), key=lambda i: distances[i])]
    result["ocr_labels"] = labels
    return result


def predict(packet, rule):
    data = packet["input"]
    candidates = data["candidate_ids"]
    if rule in ("card_first", "silhouette", "appearance"):
        binding = image_bindings(packet["images"][0]["path"])[rule]
        if binding not in candidates:
            raise ValueError("pixel_label_read_failure")
    elif rule == "oracle":
        binding = data["bound_terminal"]
    elif rule == "text_first":
        binding = candidates[0]
    elif rule == "min_id":
        binding = min(candidates)
    elif rule == "offset_12":
        target = int(data["fixed_terminals"][0][1:]) + 12
        binding = min(candidates, key=lambda c: (abs(int(c[1:]) - target), c))
    elif rule == "nearest_id":
        binding = min(candidates, key=lambda c: (min(abs(int(c[1:])-int(f[1:]))
                                                   for f in data["fixed_terminals"]), c))
    elif rule == "degree":
        degrees = {c: sum(c in e for e in data["graph"]["edges"]) for c in candidates}
        binding = max(candidates, key=lambda c: (degrees[c], c))
    elif rule in ("min_repair", "max_repair"):
        costs = {c: solve(data, c)["minimum_cost"] for c in candidates}
        binding = (min if rule == "min_repair" else max)(candidates, key=lambda c: (costs[c], c))
    elif rule == "seeded":
        binding = random.Random(digest(packet)).choice(candidates)
    else:
        raise ValueError(f"Unknown rule {rule}")
    return {"bound_terminal": binding} if packet["condition"] == "atomic_binding" else solve(data, binding)


def configurations():
    configs = []
    for rule in ("text_first", "min_id", "offset_12", "nearest_id", "degree", "min_repair", "max_repair", "seeded"):
        configs.append({"id": f"{rule}-repair", "rule": rule, "condition": "no_image"})
    for rule in ("card_first", "silhouette", "appearance"):
        configs.append({"id": f"{rule}-repair", "rule": rule, "condition": "multimodal"})
        configs.append({"id": f"{rule}-atomic", "rule": rule, "condition": "atomic_binding"})
    configs.append({"id": "oracle-repair", "rule": "oracle", "condition": "oracle_binding"})
    assert len(configs) == 15
    return configs
