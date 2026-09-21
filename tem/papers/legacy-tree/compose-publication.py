"""English publication plates from actual, hash-bound 3D canvas captures."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps
import hashlib
import json
import time
import math

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = ROOT / "benchmark/hierarchy-v3-expanded"
catalog = {m["id"]: m for m in json.loads((DATA / "catalog.json").read_text())}
capture = json.loads((HERE / "publication-capture.json").read_text())
sources, outputs, labels = {}, {}, []
BG = "#edf1f4"

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def font(size):
    return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size)

def text(draw, xy, value, size=24, fill="#193248"):
    assert value.isascii(), value
    labels.append(value)
    draw.text(xy, value, font=font(size), fill=fill)

def load(p):
    sources[str(p.relative_to(ROOT))] = sha(p)
    return Image.open(p).convert("RGB")

def bounds(image):
    diff = ImageChops.difference(image, Image.new("RGB", image.size, BG)).convert("L")
    box = diff.point(lambda p: 255 if p > 22 else 0).getbbox()
    if box is None:
        return (0, 0, image.width, image.height)
    return (max(0, box[0]-20), max(0, box[1]-20), min(image.width, box[2]+20), min(image.height, box[3]+20))

def save(im, name):
    for ext in ["png", "pdf"]:
        p = HERE / "figures" / f"publication-{name}.{ext}"
        if ext == "pdf":
            im.save(p, resolution=220, creationDate=time.gmtime(0), modDate=time.gmtime(0))
        else:
            im.save(p)
        outputs[str(p.relative_to(ROOT))] = sha(p)

selected = [
    "camera-gimbal", "folding-gripper", "exp-d1-arm-2",
    "scissor-service-lift", "articulated-loader", "exp-d2-wings-2",
    "segmented-petal-observatory", "rotary-excavator", "wildfire-tiltrotor",
    "automated-cargo-terminal", "orbital-telescope-yard", "exp-d4-gantry-2",
]
w, h = 650, 420
im = Image.new("RGB", (w*3, h*4), "white")
d = ImageDraw.Draw(im)
for i, model_id in enumerate(selected):
    m = catalog[model_id]
    x, y = i % 3*w, i//3*h
    raw = load(DATA / "images" / f"{model_id}-iso.png")
    tile = ImageOps.contain(raw.crop(bounds(raw)), (w-18, h-70))
    d.rounded_rectangle((x+6, y+6, x+w-6, y+h-6), 18, fill=BG)
    im.paste(tile, (x+(w-tile.width)//2, y+10+(h-80-tile.height)//2))
    name = m["name"].replace("\u2013", "-").replace("\u2014", "-")
    text(d, (x+22,y+h-58), f'{m["difficulty"]}  |  {name}', 22 if len(name) < 39 else 18)
    text(d, (x+22,y+h-29), f'{m["parts"]} parts / {m["modules"]} modules', 19, "#586e80")
save(im, "teaser")

def strip(family, steps, headings, name):
    records = [next(r for r in capture["frames"] if r["family"] == family and r["step"] == step and r["accepted"]) for step in steps]
    # Identical crop/scale across a sequence preserves disappearance and size.
    box = bounds(load(ROOT / records[0]["file"]))
    w, h = 480, 490
    columns = min(4, len(steps))
    im = Image.new("RGB", (w*columns, h*math.ceil(len(steps)/columns)), "white")
    d = ImageDraw.Draw(im)
    for i, (record, heading) in enumerate(zip(records, headings)):
        x, y = i % columns*w, i//columns*h
        d.rounded_rectangle((x+5, y+5, x+w-5, y+h-5), 16, fill=BG)
        raw = load(ROOT / record["file"]).crop(box)
        tile = ImageOps.contain(raw, (w-20, h-115))
        im.paste(tile, (x+(w-tile.width)//2, y+50+(h-120-tile.height)//2))
        text(d, (x+20,y+18), f'{record["step"]:02d}  {heading}', 28)
        text(d, (x+20,y+h-58), f'{len(record["activeModules"])} modules present', 26)
        text(d, (x+20,y+h-28), f'Accepted cost: {record["cost"]}', 24, "#586e80")
    save(im, name)

strip("disassembly", [0,1,2,3,4,5,6], ["Initial","Remove tool","Remove wrist","Remove elbow","Remove shoulder","Remove mount","Remove base"], "disassembly")
strip("service-repair", [0,1,2,3,4,5,6,7], ["Initial","Support","Open","Remove","Replace","Verify","Close","Release"], "repair")
strip("disassembly", [0,1,3,5], ["Initial","Remove tool","After elbow","Base remains"], "steps")

im = Image.new("RGB", (1600,500), "white")
d = ImageDraw.Draw(im)
for i, family in enumerate(["disassembly", "service-repair"]):
    r = next(r for r in capture["frames"] if r["family"] == family and not r["accepted"])
    raw = load(ROOT / r["file"])
    tile = ImageOps.contain(raw.crop(bounds(raw)), (390,440))
    im.paste(tile, (i*800+10, (500-tile.height)//2))
    x = i*800+420
    text(d, (x,90), "REJECTED AT STEP 1", 25, "#a03435")
    text(d, (x,150), "Remove base first" if i == 0 else "Remove before support", 23)
    text(d, (x,210), "Child still present" if i == 0 else "Precondition missing", 23)
    text(d, (x,260), "State unchanged", 23)
    text(d, (x,310), "Accepted cost: 0", 23)
save(im, "invalid")
sources[str(Path(__file__).relative_to(ROOT))] = sha(Path(__file__))
sources[str((HERE / "publication-capture.json").relative_to(ROOT))] = sha(HERE / "publication-capture.json")
(HERE / "publication-figures.json").write_text(json.dumps({
    "labels": labels, "englishLabelsOnly": True,
    "sourceType": "Original 3D canvas images; no UI screenshots or synthetic concept art",
    "sources": sources, "outputs": outputs,
}, indent=2) + "\n")
print(json.dumps({"plates": len(outputs)//2, "asciiLabels": len(labels)}))
