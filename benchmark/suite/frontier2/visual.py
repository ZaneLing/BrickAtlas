"""Render disclosed layers, or solve color-only maintenance using public PNG pixels.

The solve command never reads review-private.json. It is a known-renderer signal
control, not a learned vision baseline or a general pose-reconstruction method.
"""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2] / "diagnostic-v2"
COLORS = {"red": "#bd3028", "blue": "#176cb3", "green": "#368061",
          "yellow": "#e8bc31", "gray": "#95a2ac", "white": "#eef0ef"}
SIZES = {"3005": (1,1,3), "3004": (2,1,3), "3622": (3,1,3), "3010": (4,1,3),
         "3009": (6,1,3), "3008": (8,1,3), "3003": (2,2,3), "3002": (3,2,3),
         "3001": (4,2,3), "2456": (6,2,3), "3007": (8,2,3), "3024": (1,1,1),
         "3023": (2,1,1), "3623": (3,1,1), "3710": (4,1,1), "3666": (6,1,1),
         "3460": (8,1,1), "3022": (2,2,1), "3021": (3,2,1), "3020": (4,2,1),
         "3795": (6,2,1), "3034": (8,2,1), "3031": (4,4,1), "3032": (6,4,1), "3035": (8,4,1)}


def dims(p):
    w, d, h = SIZES[p["partId"]]
    return (d, w, h) if p["turn"] % 2 else (w, d, h)


def layer(parts, y, path):
    im = Image.new("RGB", (1000, 660), "white")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
    draw.text((60, 22), f"Bottom Y = {y}; X right, Z down; 1 stud = 20 pixels", font=font, fill="black")
    for x in range(45):
        draw.line((60+x*20, 100, 60+x*20, 620), fill="#dde3e1")
        if x % 2 == 0:
            draw.text((60+x*20, 76), str(x), font=font, fill="black")
    for z in range(27):
        draw.line((60, 100+z*20, 940, 100+z*20), fill="#dde3e1")
        if z % 2 == 0:
            draw.text((30, 100+z*20), str(z), font=font, fill="black")
    for p in parts:
        if p["y"] != y:
            continue
        w, d, _ = dims(p)
        x0, z0 = 60+p["x"]*20, 100+p["z"]*20
        draw.rectangle((x0+1, z0+1, x0+w*20-1, z0+d*20-1), fill=COLORS[p["color"]], outline="#25352e", width=1)
        for x in range(w):
            for z in range(d):
                cx, cz = x0+x*20+10, z0+z*20+10
                draw.ellipse((cx-5, cz-5, cx+5, cz+5), outline="#617069", width=1)
    im.save(path)


def render():
    rows = json.loads((ROOT / "review-private.json").read_text())
    used = set()
    for row in rows:
        c = row["case"]
        if "referenceAssets" not in c or c["id"] in used:
            continue
        used.add(c["id"])
        for asset in c["referenceAssets"]:
            layer(c["target"]["parts"], asset["bottomY"], ROOT / asset["path"])
        changed = [p for p in c["current"]["parts"] if p["id"] in c["faultIds"]]
        y = changed[0]["y"] if changed else 0
        layer(c["current"]["parts"], y, ROOT / "images" / (c["id"] + "-current.png"))
        layer(c["target"]["parts"], y, ROOT / "images" / (c["id"] + "-target.png"))
    print(json.dumps({"renderedCases": len(used), "pngs": len(list((ROOT / "images").glob("*.png")))}))


def overlap(p, q):
    w, d, _ = dims(p)
    v, e, _ = dims(q)
    return p["x"] < q["x"]+v and q["x"] < p["x"]+w and p["z"] < q["z"]+e and q["z"] < p["z"]+d


def solve():
    rows = json.loads((ROOT / "public.json").read_text())
    predictions = []
    for row in rows:
        if row["kind"] != "maintenance" or row.get("condition") != "layers":
            continue
        data = row["input"]
        images = {a["bottomY"]: Image.open(ROOT / a["path"]).convert("RGB") for a in data["referenceImages"]}
        replacements = []
        projection = data["projection"]
        ox, oz = projection["originPixels"]
        scale = projection["pixelsPerStud"]
        for p in data["current"]["parts"]:
            # Sample a known body interior away from studs and outlines.
            pixel = images[p["y"]].getpixel((int(ox+(p["x"]+.2)*scale), int(oz+(p["z"]+.2)*scale)))
            distances = {}
            for name, color in COLORS.items():
                rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
                distances[name] = sum((a-b)**2 for a, b in zip(pixel, rgb))
            color = min(distances, key=distances.get)
            if color != p["color"]:
                replacements.append({**p, "color": color})
        fault_ids = [p["id"] for p in replacements]
        selected = set(fault_ids)
        parts = data["current"]["parts"]
        for p in sorted(parts, key=lambda p: p["y"]):
            if any(q["id"] in selected and p["y"] >= q["y"]+dims(q)[2] and overlap(p, q) for q in parts):
                selected.add(p["id"])
        order = [p["id"] for p in sorted(parts, key=lambda p: (-p["y"], p["id"])) if p["id"] in selected]
        actions = [{"op": "remove", "id": i} for i in order]
        by_id = {p["id"]: p for p in replacements}
        actions += [{"op": "place", "id": i, **({"part": by_id[i]} if i in by_id else {})} for i in reversed(order)]
        predictions.append({"id": row["id"], "answer": {
            "diagnosis": {"faultIds": fault_ids, "replacements": replacements},
            "access": {"removeIds": order, "order": order}, "repair": {"actions": actions}}})
    (ROOT / "visual-predictions.json").write_text(json.dumps(predictions, indent=2) + "\n")
    print(json.dumps({"predictions": len(predictions), "privateFilesRead": False, "method": "known-renderer-color-signal-control"}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["render", "solve"])
    args = parser.parse_args()
    render() if args.command == "render" else solve()
