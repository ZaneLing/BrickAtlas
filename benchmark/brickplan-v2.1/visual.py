"""Scientific observations from locked LDraw triangles, in original source poses.

Pixels are the policy interface. Triangles, depth buffers, masks, blocker edges,
and private evaluator values are never returned by this module.
"""
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "brickplan_source_raster", HERE.parent / "brickplan-v1.2/visual.py")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


@lru_cache(maxsize=1)
def meshes():
    return json.loads((HERE / "arena/meshes.json").read_text())["meshes"]


# Keep the immutable triangle raster and lighting, extending the source atlas.
core.meshes = meshes
encode = core.encode
MAIN_SIZE = (1920, 1440)
SUPERSAMPLE = 2


def render(domain, locals_, labels, view, size=MAIN_SIZE, explode=False, single=False):
    """Preserve the native raster exactly without scanning every fixed piece."""
    native_size = size
    size = tuple(x * SUPERSAMPLE for x in size)
    groups = core.geometry(domain)
    selected = list(locals_)
    bounds = np.concatenate([groups[i][0].reshape(-1, 3)
                             for i in (selected if single else range(len(groups)))])
    center = (bounds.min(0) + bounds.max(0)) / 2
    direction = np.asarray(core.VECTORS.get(view, core.VECTORS["isometric"]), dtype=float)
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
        core.library().raster(len(v), v.ctypes.data, c.ctypes.data, *size,
                              depth.ctypes.data, image.ctypes.data, owner.ctypes.data, ids.ctypes.data)
    result = Image.fromarray(image)
    draw = ImageDraw.Draw(result)
    visible = []
    # The old renderer scanned the entire 11MP ownership buffer once per part,
    # including hundreds of unlabelled fixed parts and every unlabelled tile.
    # Aggregate only labelled surface pixels in one pass, retaining exact means.
    if labels:
        wanted = np.zeros(len(groups) + 1, dtype=bool)
        for i in selected:
            wanted[i + 1] = i in labels
        ys, xs = np.nonzero(wanted[owner + 1])
        owned = owner[ys, xs]
        counts = np.bincount(owned, minlength=len(groups))
        sum_x = np.bincount(owned, weights=xs, minlength=len(groups))
        sum_y = np.bincount(owned, weights=ys, minlength=len(groups))
        for i in selected:
            if i in labels and counts[i] >= 8:
                visible.append((float(sum_y[i] / counts[i]), float(sum_x[i] / counts[i]), labels[i]))
    for side in (0, 1):
        items = sorted(x for x in visible if (x[1] >= size[0] / 2) == bool(side))
        for j, (y, x, label) in enumerate(items):
            ly = 28 * unit + j * min(31 * unit, (size[1] - 50 * unit) / max(len(items), 1))
            lx = 6 * unit if side == 0 else size[0] - 112 * unit
            draw.line((x, y, lx + 50 * unit, ly + 9 * unit), fill="#526259", width=max(1, round(unit)))
            draw.rounded_rectangle((lx, ly, lx + 106 * unit, ly + 22 * unit),
                                   4 * unit, fill="#faffef", outline="#647669")
            draw.text((lx + 3 * unit, ly + 2 * unit), label, fill="#142c23", font=core.font(round(12 * unit)))
    return result.resize(native_size, Image.Resampling.LANCZOS)


@lru_cache(maxsize=128)
def encoded_render(domain, locals_, labels, view, explode=False):
    # Cache compact PNGs, not full supersampled RGB/depth buffers.
    return encode(render(domain, locals_, dict(labels), view, explode=explode))


@lru_cache(maxsize=256)
def piece_tile(domain, local, view):
    return render(domain, [local], {}, view, size=(480, 360), single=True)


def catalog(session, sites, view, label):
    sites = sorted(sites, key=lambda i: session.part_ids[i])
    rows = max(1, (len(sites) + 3) // 4)
    image = Image.new("RGB", (1920, rows * 410 + 58), "#edf1ed")
    draw = ImageDraw.Draw(image)
    draw.text((20, 14), label, fill="#142c23", font=core.font(26))
    for j, site in enumerate(sites):
        x, y = (j % 4) * 480, (j // 4) * 410 + 58
        image.paste(piece_tile(session.domain, session.domain.mutable[site], view), (x, y + 44))
        draw.text((x + 16, y + 8), f"{session.part_ids[site]} / {session.site_ids[site]}",
                  fill="#142c23", font=core.font(26))
        draw.line((x + 8, y + 408, x + 472, y + 408), fill="#cbd8cf", width=2)
    if not sites:
        draw.text((32, 190), "No pieces in rack", fill="#142c23", font=core.font(32))
    return image


@lru_cache(maxsize=128)
def encoded_catalog(domain, sites, part_ids, site_ids, view, label):
    session = SimpleNamespace(domain=domain, part_ids=dict(part_ids), site_ids=dict(site_ids))
    return encode(catalog(session, sites, view, label))


def observation_images(session, state, view):
    d, m = session.domain, session.mission
    camera = "isometric" if view == "exploded-reference" else view
    installed = [i for i in range(d.n) if state.assembly & (1 << i)]
    required = [i for i in range(d.n) if m.goal & (1 << i)]
    rack = [i for i in range(d.n) if not state.assembly & (1 << i)]
    current = encoded_render(d, tuple(sorted(d.fixed) + [d.mutable[i] for i in installed]),
                             tuple((d.mutable[i], f"{session.part_ids[i]} {session.site_ids[i]}") for i in installed), camera)
    target = encoded_render(d, tuple(sorted(d.fixed) + [d.mutable[i] for i in required]),
                            tuple((d.mutable[i], session.site_ids[i]) for i in required), camera)
    reference_labels = tuple((d.mutable[i], session.site_ids[i]) for i in range(d.n))
    if view == "exploded-reference":
        reference = render(d, range(len(d.parts)), dict(reference_labels), camera, explode=True)
        ImageDraw.Draw(reference).text(
            (220, 1380), "EXPLODED REFERENCE ONLY - not an executable state",
            fill="#142c23", font=core.font(28))
        reference = encode(reference)
    else:
        reference = encoded_render(d, tuple(range(len(d.parts))), reference_labels, camera)
    part_ids, site_ids = tuple(session.part_ids.items()), tuple(session.site_ids.items())
    return {"current": current, "target": target, "siteReference": reference,
            "catalog": encoded_catalog(d, tuple(range(d.n)), part_ids, site_ids, camera, "REGISTERED PIECE / ORIGINAL SITE"),
            "rack": encoded_catalog(d, tuple(rack), part_ids, site_ids, camera,
                                    f"RACK: {len(rack)} / {m.capacity} HOLDERS OCCUPIED")}
