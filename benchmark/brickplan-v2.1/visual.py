"""Scientific observations from locked LDraw triangles, in original source poses.

Pixels are the policy interface. Triangles, depth buffers, masks, blocker edges,
and private evaluator values are never returned by this module.
"""
from functools import lru_cache
import importlib.util
import json
from pathlib import Path

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
    """Rasterize true source triangles at 2x, then antialias to native HD pixels."""
    raster_size = tuple(x * SUPERSAMPLE for x in size)
    image = core.render(domain, locals_, labels, view, size=raster_size,
                        explode=explode, single=single)
    return image.resize(size, Image.Resampling.LANCZOS)


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


def observation_images(session, state, view):
    d, m = session.domain, session.mission
    camera = "isometric" if view == "exploded-reference" else view
    installed = [i for i in range(d.n) if state.assembly & (1 << i)]
    required = [i for i in range(d.n) if m.goal & (1 << i)]
    rack = [i for i in range(d.n) if not state.assembly & (1 << i)]
    current = render(d, sorted(d.fixed) + [d.mutable[i] for i in installed],
                     {d.mutable[i]: f"{session.part_ids[i]} {session.site_ids[i]}" for i in installed}, camera)
    target = render(d, sorted(d.fixed) + [d.mutable[i] for i in required],
                    {d.mutable[i]: session.site_ids[i] for i in required}, camera)
    reference = render(d, range(len(d.parts)), {d.mutable[i]: session.site_ids[i] for i in range(d.n)},
                       camera, explode=view == "exploded-reference")
    if view == "exploded-reference":
        ImageDraw.Draw(reference).text(
            (220, 1380), "EXPLODED REFERENCE ONLY - not an executable state",
            fill="#142c23", font=core.font(28))
    return {"current": encode(current), "target": encode(target),
            "siteReference": encode(reference),
            "catalog": encode(catalog(session, range(d.n), camera, "REGISTERED PIECE / ORIGINAL SITE")),
            "rack": encode(catalog(session, rack, camera,
                                   f"RACK: {len(rack)} / {m.capacity} HOLDERS OCCUPIED"))}
