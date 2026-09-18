"""Current English tables, per-source appendix and real-geometry plates."""
from pathlib import Path
from collections import Counter
import json
import hashlib
import math
from PIL import Image, ImageOps, ImageChops

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "benchmark/ldraw-v1"
PAPER = ROOT / "benchmark/paper"
FIG = PAPER / "figures/ldraw"
release = json.loads((DATA / "release.json").read_text())
verification = json.loads((DATA / "verification.json").read_text())
capture = json.loads((DATA / "capture.json").read_text())
catalog = json.loads((DATA / "catalog.json").read_text())
bundles = {m["id"]: json.loads((ROOT / "public/benchmark/ldraw/models" / (m["id"] + ".json")).read_text()) for m in catalog}
assert len(capture["models"]) == len(catalog)
def tex(value):
    return "".join({"&": r"\&", "%": r"\%", "_": r"\_", "#": r"\#", "$": r"\$", "{": r"\{", "}": r"\}", "\\": r"\textbackslash{}"}.get(c, c) for c in str(value))
def picture(file, width=r".48\linewidth"):
    return rf"\includegraphics[width={width}]{{figures/ldraw/print/{Path(file).stem}.jpg}}"
def table(headers, rows, spec):
    return "\\begin{tabular}{" + spec + "}\n\\toprule\n" + " & ".join(headers) + r"\\\midrule" + "\n" + "\n".join(" & ".join(map(tex, row)) + r"\\" for row in rows) + "\n\\bottomrule\n\\end{tabular}\n"

def framed(image, size):
    background = Image.new("RGB", image.size, "#f4f5f8")
    mask = ImageChops.difference(image, background).convert("L").point(lambda v: 255 if v > 10 else 0)
    box = mask.getbbox()
    if box:
        x0, y0, x1, y1 = box
        image = image.crop((max(0, x0-35), max(0, y0-35), min(image.width, x1+35), min(image.height, y1+35)))
    image = ImageOps.contain(image, size, Image.Resampling.LANCZOS)
    frame = Image.new("RGB", size, "#f4f5f8")
    frame.paste(image, ((size[0]-image.width)//2, (size[1]-image.height)//2))
    return frame

# No synthetic imagery: crop/pad and compress original browser pixels for print.
print_dir = FIG / "print"
print_dir.mkdir(exist_ok=True)
derivatives = []
for source in sorted(FIG.glob("*.png")):
    if source.stem == "teaser":
        continue
    target = print_dir / (source.stem + ".jpg")
    image = framed(Image.open(source).convert("RGB"), (1600, 1200))
    image.save(target, quality=94, subsampling=0, optimize=True)
    derivatives.append({"source": source.name, "sourceSha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "file": "print/" + target.name, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
(DATA / "figure-derivatives.json").write_text(json.dumps({
    "method": "Crop empty background, pad to 4:3, resize to 1600x1200, JPEG quality 94; original captures retained.",
    "images": derivatives}, indent=2)+"\n")
teaser_ids = ["omr-42102", "omr-42004", "omr-31088", "31009", "omr-10242", "omr-10269", "omr-21309", "omr-42054"]
teaser = Image.new("RGB", (2400, 1000), "#f4f5f8")
for i, model_id in enumerate(teaser_ids):
    img = Image.open(FIG / f"{model_id}-iso.png").convert("RGB")
    img = framed(img, (600, 500))
    teaser.paste(img, ((i % 4)*600+(600-img.width)//2, (i//4)*500+(500-img.height)//2))
teaser.save(FIG / "teaser.png")
for m in catalog:
    img = Image.open(FIG / f"{m['id']}-iso.png").convert("RGB")
    img.thumbnail((640, 512))
    thumbdir = ROOT / "public/benchmark/ldraw/thumbnails"
    thumbdir.mkdir(exist_ok=True)
    img.save(thumbdir / f"{m['id']}.png")

names = {
    "color": ("Color identification", "Visual", "Original color"),
    "shape-match": ("Part-type correspondence", "Visual", "Original type"),
    "distance": ("Nearest instance", "Source data", "Center distance"),
    "interface": ("Connector record classification", "Graph", "Interface family"),
    "neighbors": ("Direct connector neighbors", "Graph", "Adjacency set"),
    "graph-removal": ("Components after deletion", "Graph", "Induced graph"),
    "coverage": ("Unsupported-instance evidence", "Source data", "Catalog coverage"),
    "evidence-limit": ("Limits of stability evidence", "Source data", "Evidence contract"),
    "source-step": ("Author step lookup", "Source data", "STEP metadata"),
    "source-sequence": ("Author step sequence", "Scene edit", "STEP order"),
    "restore-instance": ("Restore numbered instance", "Scene edit", "Source identity"),
}
family_rows = [[names[k][0], v, names[k][1]] for k, v in release["taskFamilies"].items()]
(PAPER / "ldraw-families.tex").write_text(table(["Family", "$N$", "Input"], family_rows, "lrl"))
rows = []
for d in ["D1", "D2", "D3", "D4"]:
    models = [m for m in catalog if m["difficulty"] == d]
    rows.append([d, len(models), sum(m["parts"] for m in models), sum(m["tasks"] for m in models)])
(PAPER / "ldraw-scale.tex").write_text(table(["Band", "Sources", "Instances", "Tasks"], rows, "lrrr"))
all_tasks = [t for b in bundles.values() for t in b["tasks"]]
choices = [t for t in all_tasks if t["format"] == "single-choice"]
counts = Counter(t["answer"]["choiceId"] for t in choices)
uniform = sum(1/len(t["options"]) for t in choices)/len(choices)
stats = {
    "models": len(catalog), "tasks": len(all_tasks), "parts": release["parts"], "singleChoice": len(choices),
    "choicePositionCounts": dict(counts), "alwaysA": counts["A"]/len(choices), "uniformExpected": uniform,
    "largestInventoryJaccard": max(p["inventoryJaccard"] for p in release["diversityPairs"]),
    "nonMatingIntersectionCandidates": sum(m["intersectionCandidates"] for m in catalog),
    "sourceStepModels": release["sourceStepModels"], "visualQuestions": sum(t["modality"] == "visual" for t in all_tasks),
}
(DATA / "paper-analysis.json").write_text(json.dumps(stats, indent=2)+"\n")
control_rows = [
    ["Reference solutions", len(all_tasks), "100.0"],
    ["Public-precondition solver", verification["publicPreconditionActionsSolved"], "100.0"],
    ["Invalid controls rejected", verification["negativeControls"], "100.0"],
    ["Always A (single choice)", len(choices), f"{stats['alwaysA']*100:.1f}"],
    ["Uniform choice (expected)", len(choices), f"{uniform*100:.1f}"],
]
(PAPER / "ldraw-controls.tex").write_text(table(["Control", "$N$", r"Rate (\%)"], control_rows, "lrr"))
macros = {"LDrawSources": len(catalog), "LDrawTasks": len(all_tasks), "LDrawParts": f"{release['parts']:,}",
          "LDrawIntersections": stats["nonMatingIntersectionCandidates"], "LDrawVisual": stats["visualQuestions"]}
(PAPER / "ldraw-results.tex").write_text("\n".join(r"\newcommand{\%s}{%s}" % (k, v) for k, v in macros.items())+"\n")

# Two landscape-free pages per model: source plate, then full English questions.
appendix = []
for m in catalog:
    b = bundles[m["id"]]
    appendix += [r"\clearpage", r"\section{" + tex(f"{m['setNumber']}: {m['name']}") + "}",
      tex(f"{m['parts']} source instances; {m['tasks']} tasks; {m['difficulty']} scale band.") + "\n",
      r"\begin{center}" + picture(f"{m['id']}-iso.png") + picture(f"{m['id']}-front.png") + r"\\"
        + picture(f"{m['id']}-side.png") + picture(f"{m['id']}-top.png") + r"\end{center}",
      r"\noindent Views: perspective, front, side, top. Original source transforms are preserved.",
      r"\paragraph{Attribution.}" + tex(m["author"] + ". " + m["license"] + ".")
        + r"\par\noindent\url{" + m["sourceUrl"] + "}",
      r"\paragraph{Source lock.}\small\texttt{" + m["sourceHash"][:32] + r"}\\\texttt{" + m["sourceHash"][32:] + r"}\normalsize",
      r"\paragraph{Evidence coverage.}" + tex(f"Connector definitions cover {m['connectorCoverage']*100:.2f}% of instances. "
        f"The audit reports {len(b['audit']['components'])} recognized-graph components and "
        f"{m['intersectionCandidates']} intersection candidates without a recognized mating pair. "
        f"{len(b['audit']['unsupported'])} instances have no connector definition. "
        "These counts do not certify physical defects or gravitational stability."),
      r"\paragraph{Instructions.}" + tex(f"{m['sourceSteps']} expanded author steps." if m["sourceSteps"] else "No author STEP replay or source-order question is provided."),
      r"\clearpage\subsection{Numbered visual input and complete question index}",
      r"\begin{center}" + picture(f"{m['id']}-numbered.png", r".55\linewidth") + r"\end{center}",
      "Only relevant numbers are shown. The website can isolate any instance; public visual tasks provide their own numbered images. "
      "The following prompts are in English. Full operands, options, inputs and reference solutions are in the versioned JSON.",
      r"\begin{enumerate}"]
    for t in b["tasks"]:
        suffix = t["id"].removeprefix("ld1-"+m["id"]+"-")
        answer = t["answer"]
        readable = answer.get("choiceId") or ", ".join(answer.get("choiceIds", answer.get("actionIds", [])))
        appendix.append(r"\item \textbf{" + tex(suffix) + "}. " + tex(t["promptEn"]) + " "
          + r"\textit{Answer:} " + tex(readable) + ".")
    appendix.append(r"\end{enumerate}")
(PAPER / "ldraw-cases.tex").write_text("\n".join(appendix)+"\n")
credits = ["# LDraw-1 retained-source attribution\n", "Original source bytes and scene poses are unchanged. "
           "The benchmark adds numbering, questions and review metadata. Detailed part-library credits ship beside every model.\n"]
for m in catalog:
    credits.append(f"- {m['setNumber']} — {m['name']}. {m['author']}. {m['license']}. {m['sourceUrl']} — SHA256 `{m['sourceHash']}`")
(DATA / "ATTRIBUTION.md").write_text("\n".join(credits)+"\n")
print(json.dumps(stats, indent=2))
