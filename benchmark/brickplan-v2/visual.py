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
render, encode = core.render, core.encode


@lru_cache(maxsize=4096)
def piece_tile(domain, local, view):
    return render(domain, [local], {}, view, size=(220, 180), single=True).resize((124, 88))


def catalog(session, sites, view, label):
    sites = sorted(sites, key=lambda i: session.part_ids[i])
    rows = max(1, (len(sites) + 5) // 6)
    image = Image.new("RGB", (760, rows * 120 + 30), "#edf1ed")
    draw = ImageDraw.Draw(image)
    draw.text((8, 7), label, fill="#142c23", font=core.font(13))
    for j, site in enumerate(sites):
        x, y = (j % 6) * 126, (j // 6) * 120 + 30
        image.paste(piece_tile(session.domain, session.domain.mutable[site], view), (x, y + 28))
        draw.text((x + 5, y + 3), f"{session.part_ids[site]} / {session.site_ids[site]}",
                  fill="#142c23", font=core.font(11))
    if not sites:
        draw.text((16, 66), "No pieces in rack", fill="#142c23", font=core.font(16))
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
            (120, 555), "EXPLODED REFERENCE ONLY - not an executable state",
            fill="#142c23", font=core.font(13))
    return {"current": encode(current), "target": encode(target),
            "siteReference": encode(reference),
            "catalog": encode(catalog(session, range(d.n), camera, "REGISTERED PIECE / ORIGINAL SITE")),
            "rack": encode(catalog(session, rack, camera,
                                   f"RACK: {len(rack)} / {m.capacity} HOLDERS OCCUPIED"))}
