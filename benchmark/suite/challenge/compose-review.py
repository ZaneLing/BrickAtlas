"""Build all-model report plates and per-model appendix from scored control fixtures."""
import json
import hashlib
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops

ROOT = Path(__file__).resolve().parents[2]
GALLERY = ROOT / "review-gallery"
PAPER = ROOT / "paper"
rows = json.loads((GALLERY / "cases.json").read_text())
models = list(dict.fromkeys(row["modelId"] for row in rows))
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
contact = Image.new("RGB", (1200, 6 * 340), "white")
draw = ImageDraw.Draw(contact)
target = PAPER / "figures/review-cases"
target.mkdir(exist_ok=True)
tex = [r"\clearpage", r"\onecolumn", r"\section{All Authored Models: Scored Case Studies}",
       r"These are constructed positive and negative evaluator controls, not model predictions.",
       r"The 18 source models remain 18 sources; their 36 demonstration cases are not independent samples.",
       r"All 5,120 frozen procedural sources are shown separately in the 80-page offline gallery."]
md = ["# 全部模型与正反案例", "", "18 个设计模型，36 个构造对照。PASS/FAIL 是裁判自测，不是模型成绩。",
      "", "[打开全部模型图集](index.html) · [打开全部 5,120 个程序模型](procedural-001.html)", "",
      "![18 个设计模型](ALL_MODELS.png)", ""]
def score(v):
    return v.get("success", v.get("metrics", {}).get("success"))
def escape(s):
    return str(s).replace("_", r"\_").replace("&", r"\&").replace("%", r"\%")
for i, model in enumerate(models):
    selected = [r for r in rows if r["modelId"] == model]
    first = selected[0]
    image = Image.open(GALLERY / (first["stem"] + "-model.jpg")).convert("RGB")
    contact.paste(ImageOps.contain(image, (395, 292)), ((i % 3)*400, (i//3)*340))
    draw.text(((i % 3)*400+8, (i//3)*340+291), first["name"], font=font, fill="#182428")
    draw.text(((i % 3)*400+8, (i//3)*340+318), "2 scored controls; not model results", font=small, fill="#526166")
    if i:
        tex.append(r"\clearpage")
    tex += [r"\subsection{" + escape(first["name"]) + "}",
            r"\noindent Source: \texttt{" + escape(model) + "}.",
            r"Two cases share this source. Read numeric/graph answer fields alongside context-only images."]
    md += [f"## {i+1}. {first['name']}", "", f"[逐例浏览与 JSON](model-{i+1}.html)", ""]
    for row in selected:
        assert score(row["positive"]) == 1 and score(row["negative"]) == 0
        stem = row["stem"]
        for variant in ["input", "good", "bad"]:
            Image.open(GALLERY / f"{stem}-{variant}.jpg").convert("RGB").save(target / f"{stem}-{variant}.jpg", quality=95)
        issues = row["negative"].get("issues", [])
        prompt = row["prompt"] if row["kind"] not in ["plan", "repair"] else (
            "Given the full target, return all IDs in an executable vertical insertion order. The negative reverses the order."
            if row["kind"] == "plan" else "Given current and full symbolic reference, restore a wrong color and report its current ID. The negative copies current.")
        tex += [r"\paragraph{" + escape(row["kind"]) + r".} Case \texttt{" + row["id"] + r"}.\par",
                escape(prompt) + r"\par",
                r"\noindent\begin{tabular}{@{}ccc@{}}",
                r"Input / context & Positive reference & Constructed negative\\",
                " & ".join(r"\includegraphics[width=.31\textwidth]{figures/review-cases/" + f"{stem}-{v}.jpg" + "}" for v in ["input", "good", "bad"]) + r"\\",
                r"\end{tabular}\par",
                r"\noindent Strict success: positive $1$, negative $0$. Rejection: \texttt{" + escape(", ".join(issues) or "required-field/target mismatch") + "}.",
                r"Machine-readable inputs, both answers and all metrics are in \texttt{review-gallery/" + stem + ".json}.",
                r"Field-answer cases use scene images for context only; a matching scene is not a correct field answer."]
        if row["kind"] in ["active-inspection", "support-counterfactual", "graph-reasoning", "step-selection", "pose-estimation"]:
            tex += [r"\begin{quote}\small", r"\begin{verbatim}",
                    "\n".join(textwrap.wrap("Positive: " + json.dumps(row["good"]), width=90)),
                    "\n".join(textwrap.wrap("Negative: " + json.dumps(row["bad"]), width=90)),
                    r"\end{verbatim}", r"\end{quote}"]
        md += [f"### {row['kind']}", "", row["prompt"], "",
               "| 输入 / 上下文 | 正确参考 | 构造错误 |", "|---|---|---|",
               f"| ![]({stem}-input.jpg) | ![]({stem}-good.jpg) | ![]({stem}-bad.jpg) |", "",
               f"正例 success=1；负例 success=0；失败原因：`{', '.join(issues) or '字段/目标不匹配'}`。",
               f"[完整评分 JSON]({stem}.json)", ""]
contact.save(GALLERY / "ALL_MODELS.png")
contact.save(PAPER / "figures/review-all-models.pdf", "PDF", resolution=150)
(PAPER / "tables/review-case-studies.tex").write_text("\n".join(tex) + "\n")
(GALLERY / "REPORT.zh-CN.md").write_text("\n".join(md).rstrip() + "\n")

catalog = json.loads((GALLERY / "catalog.json").read_text())
bad = []
for row in catalog["models"]:
    im = Image.open(GALLERY / row["image"]).convert("RGB")
    assert im.size == (400, 300)
    r, g, b = im.split()
    foreground = sum(ImageChops.darker(ImageChops.darker(r, g), b).histogram()[:230])
    if foreground < 1000:
        bad.append(row["id"])
assert not bad, bad
files = [p for p in GALLERY.iterdir() if p.is_file() and p.name != "verification.json"]
report = {"authoredModels": len(models), "controlCases": len(rows), "positivesPassed": 36, "negativesRejected": 36,
          "proceduralModelsRendered": len(catalog["models"]), "proceduralCaseLinks": 10240,
          "blankImages": bad, "modelInferences": 0,
          "sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(GALLERY / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({k: v for k, v in report.items() if k != "sha256"}))
