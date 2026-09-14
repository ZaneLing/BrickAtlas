"""Compose the authored Frontier audit plates and reproducible paper tables."""
import hashlib
import json
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "frontier-cases"
PAPER = ROOT / "paper"
manifest = json.loads((DATA / "manifest.json").read_text())
cases = json.loads((DATA / "cases.json").read_text())
baselines = json.loads((DATA / "baselines.json").read_text())
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
font = ImageFont.truetype(font_path, 25)
small = ImageFont.truetype(font_path, 19)
plate = Image.new("RGB", (1800, 1080), "white")
draw = ImageDraw.Draw(plate)
for i, m in enumerate(manifest["models"]):
    x, y = (i % 3) * 600, (i // 3) * 540
    image = Image.open(DATA / (m["id"] + "-iso.png")).convert("RGB").resize((600, 450))
    plate.paste(image, (x, y))
    draw.text((x + 22, y + 450), m["name"], font=font, fill="#202827")
    s = m["stats"]
    draw.text((x + 22, y + 486), f'{s["parts"]} parts | {s["layers"]} levels | depth {s["depth"]}', font=small, fill="#166b79")
plate.save(DATA / "ALL_MODELS.png")
plate.save(PAPER / "figures/frontier-models.pdf", "PDF", resolution=160)
figdir = PAPER / "figures/frontier"
figdir.mkdir(exist_ok=True)
md = ["# Frontier 逐模型案例报告", "", "六个原创大结构；每个8类任务，共48对已评分正反例。不是模型预测。",
      "图片是审核上下文，正式输入以每题 public.json 为准；字段题看JSON，不能根据图是否相同判答案。",
      "", "![全部新模型](ALL_MODELS.png)", ""]
tex = [r"\clearpage", r"\onecolumn", r"\section{Frontier Model and Case Atlas}",
       r"All 48 pairs are constructed evaluator controls, not model predictions. Field-answer images are context only.",
       r"Only the exported public JSON is allowed evidence; the plates do not define an image-only track."]
model_table = []
for m in manifest["models"]:
    s, mid = m["stats"], m["id"]
    model_table.append(f'{m["name"]} & {s["parts"]} & {s["layers"]} & {s["depth"]} & {s["extent"]["x"]}$\\times${s["extent"]["z"]} \\\\')
    md += [f'## {m["name"]}', "", f'{s["parts"]} 件，{s["layers"]} 个底高层，依赖深度 {s["depth"]}。',
           f'[交互目录]({mid}.html) · [完整结构]({mid}.json)', "", f'![模型]({mid}-iso.png)', ""]
    for start in [0, 4]:
        tex += [r"\clearpage", r"\subsection{" + m["name"] + (" (continued)" if start else "") + "}",
                f'{s["parts"]} parts; {s["layers"]} bottom-Y levels; dependency depth {s["depth"]}.']
        subset = [c for c in cases if c["modelId"] == mid][start:start+4]
        for c in subset:
            stem = c["stem"]
            for suffix in ["good", "bad"]:
                image = Image.open(DATA / f"{stem}-{suffix}.png").convert("RGB")
                image.resize((500, 375)).save(figdir / f"{stem}-{suffix}.jpg", quality=90)
            tex += [r"\subsubsection*{" + c["kind"].replace("-", " ") + r"}",
                    r"\noindent\includegraphics[width=.24\textwidth]{figures/frontier/" + stem + "-good.jpg}" +
                    r"\includegraphics[width=.24\textwidth]{figures/frontier/" + stem + r"-bad.jpg}\hfill" +
                    r"\begin{minipage}[b]{.48\textwidth}\small Positive success: 1. Negative success: 0.\\Rejection: \texttt{" +
                    ", ".join(c["bad"]["issues"]).replace("_", r"\_") + r"}.\\",
                    "Positive metrics: " + ", ".join(f'{k}={v}' for k, v in c["good"]["metrics"].items()) + r".\end{minipage}\par"]
            if c["kind"] == "inspection-policy":
                tex += [r"\noindent\small Positive policy queries q0, q1, q2 and identifies all eight worlds at worst cost 6; the negative guesses h0 without querying. Full branch tree is in the corresponding review JSON.\par\normalsize"]
            elif c["kind"] in ["ambiguity-set", "minimal-intervention"]:
                tex += [r"\noindent\small\texttt{" + ("Positive: " + json.dumps(c["positive"])).replace("_", r"\_").replace("{", r"\{").replace("}", r"\}") + r"}\par\normalsize"]
            md += [f'### {c["label"]}', "", "| 正确参考 | 构造错误 |", "|---|---|",
                   f'| ![]({stem}-good.png) | ![]({stem}-bad.png) |', "",
                   f'正例=1；反例=0；失败原因：`{", ".join(c["bad"]["issues"])}`。',
                   f'[公开题面]({stem}-public.json) · [完整答案及评分]({stem}-review.json)', "",
                   "```json", json.dumps({"positiveMetrics": c["good"]["metrics"], "negative": c["negative"]}, ensure_ascii=False, indent=2),
                   "```", ""]
(DATA / "REPORT.zh-CN.md").write_text("\n".join(md).rstrip() + "\n")
(PAPER / "tables/frontier-cases.tex").write_text("\n".join(tex) + "\n")
(PAPER / "tables/frontier-models.tex").write_text("\n".join(model_table) + "\n")
summary = []
for kind in dict.fromkeys(c["kind"] for c in cases):
    rows = [r for r in baselines if r["kind"] == kind]
    summary.append(f'{kind.replace("-", " ")} & {sum(r["solver"]["success"] for r in rows)}/6 & {sum(r["shortcut"]["success"] for r in rows)}/6 \\\\')
(PAPER / "tables/frontier-baselines.tex").write_text("\n".join(summary) + "\n")
evidence = {"version": manifest["version"], "models": 6, "cases": 48, "placedParts": manifest["placedParts"],
            "modelInferences": 0, "generatorSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "manifestSha256": hashlib.sha256((DATA / "manifest.json").read_bytes()).hexdigest(),
            "outputs": {}}
for p in [DATA / "REPORT.zh-CN.md", DATA / "ALL_MODELS.png", PAPER / "figures/frontier-models.pdf",
          PAPER / "tables/frontier-cases.tex", PAPER / "tables/frontier-models.tex", PAPER / "tables/frontier-baselines.tex"]:
    evidence["outputs"][str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
(PAPER / "frontier-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
print(json.dumps({k: v for k, v in evidence.items() if k != "outputs"}))
