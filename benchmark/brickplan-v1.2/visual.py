"""Scientific raster observations of locked original LDraw triangles.

Only PNG pixels and opaque IDs leave this module. No scene graph or depth buffer
is served. Orthographic views and exploded site-reference are protocol actions.
"""
import base64
import ctypes
from functools import lru_cache
import hashlib
import io
import json
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
VECTORS = {"isometric": [1.35, 1.05, 1.55], "front": [0, .001, 2],
           "rear": [0, .001, -2], "left": [-2, .001, 0], "right": [2, .001, 0],
           "top": [0, 2, .001], "bottom": [0, -2, .001]}
COLORS = {"0": "#202326", "1": "#0055bf", "4": "#c91a09", "7": "#9ba19d",
          "14": "#f2cd37", "15": "#ffffff", "71": "#a0a5a9", "72": "#6c6e68"}


@lru_cache(maxsize=1)
def library():
    source = HERE / "raster.c"
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:16]
    binary = HERE.parents[1] / "tem/brickplan-v1.2" / f"raster-{digest}.dylib"
    binary.parent.mkdir(parents=True, exist_ok=True)
    if not binary.exists():
        subprocess.run(["cc", "-O3", "-shared", "-fPIC", str(source), "-o", str(binary)], check=True)
    lib = ctypes.CDLL(str(binary))
    ptr = ctypes.c_void_p
    lib.raster.argtypes = [ctypes.c_int, ptr, ptr, ctypes.c_int, ctypes.c_int, ptr, ptr, ptr, ptr]
    lib.raster.restype = None
    return lib


@lru_cache(maxsize=1)
def meshes():
    return json.loads((HERE / "arena/meshes.json").read_text())["meshes"]


@lru_cache(maxsize=8)
def font(size=15):
    for path in ("/System/Library/Fonts/Menlo.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def rgb(color):
    return np.array([int(color[i:i+2], 16) for i in (1, 3, 5)])


@lru_cache(maxsize=8)
def geometry(domain):
    groups = []
    for local, part in enumerate(domain.parts):
        vertices, colors = [], []
        mat = np.asarray(part["rawMatrix"])
        for color, values in meshes()[part["partNumber"]].items():
            v = np.asarray(values).reshape(-1, 3, 3) @ mat[:3, :3].T + mat[:3, 3]
            v *= np.array([1, -1, -1])
            norm = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0])
            norm /= np.maximum(np.linalg.norm(norm, axis=1, keepdims=True), 1e-10)
            # Two-sided original LDraw faces; orientation-independent lighting.
            light = np.abs(norm @ np.array([.4, .8, .45]))
            shade = .55 + .45 * np.clip(light, 0, 1)
            base = rgb(part["colorHex"] if color == "16" else COLORS.get(color, part["colorHex"]))
            vertices.append(v)
            colors.append(np.clip(base[None, :] * shade[:, None], 0, 255))
        groups.append((np.concatenate(vertices), np.concatenate(colors).astype(np.uint8)))
    return groups


def render(domain, locals_, labels, view, size=(760, 580), explode=False, single=False):
    groups = geometry(domain)
    selected = list(locals_)
    bounds = np.concatenate([groups[i][0].reshape(-1, 3) for i in (selected if single else range(len(groups)))])
    center = (bounds.min(0) + bounds.max(0)) / 2
    direction = np.asarray(VECTORS.get(view, VECTORS["isometric"]), dtype=float)
    direction /= np.linalg.norm(direction)
    right = np.cross([0, 1, 0], direction)
    right /= np.linalg.norm(right)
    up = np.cross(direction, right)
    rotation = np.stack([right, -up, direction], axis=1)
    projected = (bounds - center) @ rotation
    unit = size[0] / 760
    scale = min((size[0] - 150 * unit) / max(np.ptp(projected[:, 0]), 1),
                (size[1] - 100 * unit) / max(np.ptp(projected[:, 1]), 1))
    if explode:
        scale *= .66
    vertices, colors, owners = [], [], []
    for i in selected:
        v, c = groups[i]
        shift = (v.reshape(-1, 3).mean(0) - center) * .7 if explode else 0
        p = ((v + shift - center) @ rotation).copy()
        p[:, :, :2] *= scale
        p[:, :, 0] += size[0] / 2
        p[:, :, 1] += size[1] / 2
        vertices.append(p)
        colors.append(c)
        owners.append(np.full(len(v), i, np.int32))
    image = np.full((size[1], size[0], 3), [237, 241, 237], dtype=np.uint8)
    owner = np.full(size[::-1], -1, dtype=np.int32)
    depth = np.full(size[::-1], -np.inf, dtype=np.float32)
    if vertices:
        v = np.ascontiguousarray(np.concatenate(vertices), dtype=np.float32)
        c = np.ascontiguousarray(np.concatenate(colors))
        ids = np.ascontiguousarray(np.concatenate(owners))
        library().raster(len(v), v.ctypes.data, c.ctypes.data, *size,
                         depth.ctypes.data, image.ctypes.data, owner.ctypes.data, ids.ctypes.data)
    result = Image.fromarray(image)
    draw = ImageDraw.Draw(result)
    visible = []
    for i in selected:
        ys, xs = np.where(owner == i)
        if i in labels and len(xs) >= 8:
            visible.append((float(np.mean(ys)), float(np.mean(xs)), labels[i]))
    # Callouts occupy side columns, with lines ending at visible surface pixels.
    for side in (0, 1):
        items = sorted(x for x in visible if (x[1] >= size[0] / 2) == bool(side))
        for j, (y, x, label) in enumerate(items):
            ly = 28 * unit + j * min(31 * unit, (size[1] - 50 * unit) / max(len(items), 1))
            lx = 6 * unit if side == 0 else size[0] - 112 * unit
            draw.line((x, y, lx + 50 * unit, ly + 9 * unit), fill="#526259", width=max(1, round(unit)))
            draw.rounded_rectangle((lx, ly, lx + 106 * unit, ly + 22 * unit),
                                   4 * unit, fill="#faffef", outline="#647669")
            draw.text((lx + 3 * unit, ly + 2 * unit), label, fill="#142c23", font=font(round(12 * unit)))
    return result


def encode(image):
    stream = io.BytesIO()
    image.save(stream, "PNG")
    return {"mime": "image/png", "width": image.width, "height": image.height,
            "base64": base64.b64encode(stream.getvalue()).decode()}


def observation_images(session):
    d, obs = session.domain, {}
    view = session.view
    camera = "isometric" if view == "exploded-reference" else view
    fixed = sorted(d.fixed)
    installed = [i for i in range(d.n) if session.state & (1 << i)]
    required = [i for i in range(d.n) if session.task["goal"] & (1 << i)]
    labels = {d.mutable[i]: f"{session.installed[i]} {session.site_ids[i]}" for i in installed}
    obs["current"] = encode(render(d, fixed + [d.mutable[i] for i in installed], labels, camera))
    obs["target"] = encode(render(d, fixed + [d.mutable[i] for i in required],
                                  {d.mutable[i]: session.site_ids[i] for i in required}, camera))
    obs["siteReference"] = encode(render(d, range(len(d.parts)),
        {d.mutable[i]: session.site_ids[i] for i in range(d.n)}, camera,
        explode=view == "exploded-reference"))
    # Separate reference catalog: all S sites plus inventory P pieces, displayed as pixels.
    available = [p for p in sorted(session.part_types) if p not in session.installed.values()]
    tiles = [(session.site_ids[i], i) for i in range(d.n)]
    tiles += [(p, next(i for i, p0 in session.part_ids.items() if p == p0)) for p in available]
    sheet = Image.new("RGB", (760, ((len(tiles) + 5) // 6) * 110), "#edf1ed")
    draw = ImageDraw.Draw(sheet)
    for j, (label, site) in enumerate(tiles):
        local = d.mutable[site]
        tile = render(d, [local], {}, camera, size=(220, 180), single=True).resize((124, 88))
        x, y = (j % 6) * 126, (j // 6) * 110
        sheet.paste(tile, (x, y + 20))
        draw.text((x + 6, y + 2), label, font=font(14), fill="#142c23")
    obs["catalog"] = encode(sheet)
    return obs
