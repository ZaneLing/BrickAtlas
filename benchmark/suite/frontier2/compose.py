"""Build the diagnostic release gallery, paper figure and artifact manifest."""
import hashlib
import html
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

BENCH = Path(__file__).resolve().parents[2]
DATA = BENCH / "diagnostic-v2"
PAPER = BENCH / "paper"
audit = json.loads((DATA / "audit.json").read_text())
public = json.loads((DATA / "public.json").read_text())
private = json.loads((DATA / "review-private.json").read_text())
scores = json.loads((DATA / "visual-scores.json").read_text())
plt.rcParams.update({"font.size": 10, "pdf.fonttype": 42})
fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), constrained_layout=True)
axes[0].bar(["Legacy set", "Best set", "Best tree"], [audit["oldSetSuccess"], audit["bestFixedSetSuccess"], audit["bestFixedPolicySuccess"]],
            color=["#bc3434", "#2b8a70", "#317bab"])
axes[0].set_ylim(0, 18)
axes[0].set_ylabel("Successes / 18 observation cases")
axes[0].set_title("A. Fixed-answer transfer")
pairs = audit["matchedContextPairs"]
for group in dict.fromkeys(p["sourceGroup"] for p in pairs):
    ps = [p for p in pairs if p["sourceGroup"] == group]
    axes[1].plot([p["faultCount"] for p in ps], [p["optimalActions"] for p in ps], marker="o", label=group)
axes[1].set_xlabel("Fault count (correlated with selected depth)")
axes[1].set_ylabel("Optimal maintenance actions")
axes[1].set_title("B. Measured design factors")
axes[2].scatter([p["localParts"] for p in pairs], [p["fullParts"] for p in pairs], color="#317bab")
axes[2].set_xlabel("Local context parts")
axes[2].set_ylabel("Full context parts")
axes[2].set_title("C. Same answer, different context")
fig.savefig(PAPER / "figures/diagnostic-v2.pdf")
fig.savefig(DATA / "DIAGNOSTICS.png", dpi=160)
plt.close(fig)
css = """*{box-sizing:border-box}body{margin:0;font:15px/1.55 system-ui,sans-serif;color:#25332d}
main{max-width:1180px;margin:auto;padding:24px}h1{font-size:28px}h2{font-size:22px}h3{font-size:17px}
a{color:#146881}header{border-bottom:2px solid #287c66}article{border-bottom:1px solid #ccd4d2;padding:20px 0}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}img{width:100%;height:auto}
pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f4f3;padding:12px;max-height:280px;overflow:auto}
p{overflow-wrap:anywhere}figure{margin:0}figcaption{font-size:13px}@media(max-width:650px){main{padding:14px}.grid{grid-template-columns:1fr}h1{font-size:24px}}"""
def page(title, body):
    return f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{css}</style><main>{body}</main></html>'

model_ids = list(dict.fromkeys(r["sourceGroup"] for r in public))
links = []
tex = [r"\clearpage", r"\onecolumn", r"\section{Diagnostic-2 Matched Visual Examples}",
       r"These examples disclose all bottom-Y layers. They are not ordinary exterior-only observations.",
       r"Each row pairs a current layer with its correct reference at identical grid calibration; other layers remain in the exported input."]
md = ["# Diagnostic-2 案例导航", "", "六个源模型，138条条件；不等于138个独立对象。", "",
      "维护目标、访问证书和维修动作可联合或独立作答。图像是实际模型输入的底高分层视图，不是只用于展示的背景。", ""]
for group in model_ids:
    model_rows = [r for r in private if r["case"].get("sourceGroup") == group]
    maintenance = [r for r in model_rows if r["id"].endswith("-full-layers") and "maintenance" in r["id"]]
    body = f'<header><a href="index.html">返回目录</a><h1>{group}</h1><p><a href="../frontier-cases/{group}.html">完整三维模型</a></p></header>'
    body += f'<img src="../frontier-cases/{group}-iso.png" alt="{group}">'
    tex += [r"\clearpage", r"\subsection{" + group.replace("-", " ") + "}"]
    md += [f"## {group}", "", f"[打开图文案例]({group}.html)", ""]
    for row in maintenance:
        c = row["case"]
        body += f'<article><h2>维护层级 {c["tier"]}</h2><p>{html.escape(json.dumps(c["factors"]))}</p><div class="grid">'
        for suffix, label in [("current", "当前状态"), ("target", "正确参考层")]:
            path = f'images/{c["id"]}-{suffix}.png'
            body += f'<figure><img loading="lazy" src="{path}" alt="{label}"><figcaption>{label}</figcaption></figure>'
        body += '</div><details><summary>Ground truth 与维修证书</summary><pre>' + html.escape(json.dumps(c["oracle"], indent=2)) + '</pre></details></article>'
        if c["tier"] == 2:
            body += '<article><h2>已执行的三维维修检查点</h2><div class="grid">'
            for step in ["before", "opened", "repaired"]:
                body += f'<figure><img loading="lazy" src="images/{c["id"]}-{step}.png"><figcaption>{step}</figcaption></figure>'
            body += '</div></article>'
        image = Image.new("RGB", (1000, 330), "white")
        for col, suffix in enumerate(["current", "target"]):
            im = Image.open(DATA / f'images/{c["id"]}-{suffix}.png').convert("RGB").resize((500, 330))
            image.paste(im, (col*500, 0))
        path = f'figures/diagnostic-{group}-{c["tier"]}.jpg'
        image.save(PAPER / path, quality=92)
        tex += [r"\subsubsection*{Maintenance tier " + str(c["tier"]) + "}",
                r"\noindent\includegraphics[width=.95\textwidth]{" + path + r"}\par",
                f'Left: current. Right: reference. Faults: {c["factors"]["faultCount"]}; minimum actions: {c["factors"]["optimalActions"]}.',
                r"The local/full counterpart has exactly the same answer. All stages use the same reference disclosure."]
    pose = next(r for r in private if r["id"] == f'f2-{group}-pose-patch-layers')
    pid = pose["case"]["id"]
    body += f'<article><h2>平移、朝向与颜色混合修复</h2><div class="grid"><img loading="lazy" src="images/{pid}-current.png"><img loading="lazy" src="images/{pid}-target.png"></div><details><summary>修复补丁</summary><pre>{html.escape(json.dumps(pose["oracle"],indent=2))}</pre></details></article>'
    body += '<h2>公开任务合同</h2>'
    for row in public:
        if row["sourceGroup"] != group:
            continue
        body += f'<details><summary>{html.escape(row["id"])}</summary><pre>{html.escape(json.dumps(row,indent=2))}</pre></details>'
    (DATA / (group + ".html")).write_text(page(group, body))
    links.append(f'<article><a href="{group}.html"><h2>{group}</h2><img src="../frontier-cases/{group}-iso.png"></a></article>')
body = '<header><h1>BrickAtlas Diagnostic-2</h1><p>共享对象的诊断、观测与可执行维修</p><p><a href="../DIAGNOSTIC_UPGRADE.zh-CN.md">升级报告</a> · <a href="public.json">公开题面</a> · <a href="stage-public.json">独立阶段题面</a> · <a href="audit.json">捷径审计</a></p></header>'
body += '<div class="grid">' + "".join(links) + '</div>'
(DATA / "index.html").write_text(page("BrickAtlas Diagnostic-2", body))
(DATA / "REPORT.zh-CN.md").write_text("\n".join(md).rstrip() + "\n")
(PAPER / "tables/diagnostic-v2-cases.tex").write_text("\n".join(tex) + "\n")
manifest = {"version": audit["version"], "recordCount": len(public), "sourceGroups": 6,
            "visualControlSuccess": scores["strata"]["maintenance:layers"]["success"],
            "visualControlDenominator": 36, "modelInferences": 0, "files": {}}
for p in DATA.rglob("*"):
    if p.is_file() and p.name != "verification.json":
        manifest["files"][str(p.relative_to(DATA))] = hashlib.sha256(p.read_bytes()).hexdigest()
(DATA / "verification.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({k: v for k, v in manifest.items() if k != "files"}))
