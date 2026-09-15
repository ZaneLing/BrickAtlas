"""Compose deterministic library, task-matrix, and pilot heatmap plates."""
from pathlib import Path
import json
import time

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "hierarchy-v1"
MODELS = json.loads((OUT / "models.json").read_text())
TASKS = json.loads((OUT / "public.json").read_text())
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"


def font(size):
    return ImageFont.truetype(FONT_PATH, size) if Path(FONT_PATH).exists() else ImageFont.load_default()


TITLE = font(25)
BODY = font(18)
SMALL = font(15)
LEVELS = [
    ("D1", "部件级"),
    ("D2", "装配体级"),
    ("D3", "机构级"),
    ("D4", "系统级"),
]
LAYERS = [
    ("atomic", "原子能力"),
    ("metacognitive", "元认知/物理"),
    ("procedural", "可执行操作"),
    ("integrative", "综合复杂题"),
]


def save_pair(canvas, path):
    canvas.save(path)
    epoch = time.gmtime(0)
    canvas.save(path.with_suffix(".pdf"), "PDF", resolution=180,
                creationDate=epoch, modDate=epoch)


def wrapped(draw, xy, text, width, fill, text_font, spacing=4):
    lines, current = [], ""
    for token in text.split():
        candidate = token if not current else current + " " + token
        if draw.textbbox((0, 0), candidate, font=text_font)[2] <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = token
    if current:
        lines.append(current)
    draw.multiline_text(xy, "\n".join(lines), fill=fill, font=text_font, spacing=spacing)


def library_overview():
    cell_w, cell_h, columns = 360, 285, 6
    canvas = Image.new("RGB", (cell_w * columns, cell_h * 4), "#e9eef0")
    draw = ImageDraw.Draw(canvas)
    for row, (level, label) in enumerate(LEVELS):
        selected = [model for model in MODELS if model["difficulty"] == level]
        for col in range(columns):
            left, top = col * cell_w, row * cell_h
            draw.rectangle((left, top, left + cell_w, top + cell_h), fill="#f6f8f9",
                           outline="#c7d2d7", width=2)
            if col >= len(selected):
                continue
            model = selected[col]
            image = Image.open(OUT / f'images/models/{model["id"]}-iso.png').convert("RGB")
            image = ImageOps.contain(image, (cell_w - 24, cell_h - 74))
            canvas.paste(image, (left + (cell_w - image.width) // 2, top + 8))
            draw.text((left + 12, top + cell_h - 59), f"{level} {label} · {model['nameZh']}",
                      fill="#182128", font=BODY)
            draw.text((left + 12, top + cell_h - 31),
                      f"{len(model['parts'])} parts · {len(model['modules'])} modules · {len(model['joints'])} joints",
                      fill="#5a6870", font=SMALL)
    save_pair(canvas, OUT / "LIBRARY_OVERVIEW.png")


def task_matrix():
    margin_x, margin_y = 230, 110
    cell_w, cell_h = 420, 205
    canvas = Image.new("RGB", (margin_x + cell_w * 4, margin_y + cell_h * 4), "#f5f7f8")
    draw = ImageDraw.Draw(canvas)
    colors = ["#e6f1f5", "#fff0ce", "#e5f2e9", "#f2e6ef"]
    capabilities = {
        "atomic": "识别 / 计数 / 位姿 / 连接\n增删改换 / 修复 / 下一步",
        "metacognitive": "支撑 / 可达 / 动力学 / 运动学\n不确定性 / 信息增益 / Pareto",
        "procedural": "装配 / 拆卸 / 编辑验证\n维修 / 库存重规划 / 检查后执行",
        "integrative": "诊断 + 访问 + 资源 + 风险\n长程计划 + 最终验证",
    }
    level_load = {
        "D1": "单接口 · 局部可见 · 1–4 步",
        "D2": "多子装配 · 局部遮挡 · 4–8 步",
        "D3": "多关节 · 隐藏故障 · 6–12 步",
        "D4": "跨工位 · 共享资源 · 12–24 步",
    }
    draw.text((22, 24), "Y：结构难度", fill="#182128", font=TITLE)
    draw.text((margin_x, 24), "X：任务负载与能力组合", fill="#182128", font=TITLE)
    for col, (layer, label) in enumerate(LAYERS):
        draw.text((margin_x + col * cell_w + 14, 68), label, fill="#182128", font=BODY)
    for row, (level, label) in enumerate(LEVELS):
        top = margin_y + row * cell_h
        draw.text((24, top + 55), f"{level} {label}", fill="#182128", font=TITLE)
        count_models = len([model for model in MODELS if model["difficulty"] == level])
        draw.text((24, top + 95), f"{count_models} models", fill="#5a6870", font=BODY)
        for col, (layer, _) in enumerate(LAYERS):
            left = margin_x + col * cell_w
            count = len([task for task in TASKS
                         if task["difficulty"] == level and task["layer"] == layer])
            draw.rectangle((left + 5, top + 5, left + cell_w - 5, top + cell_h - 5),
                           fill=colors[col], outline="#afbdc4", width=2)
            draw.text((left + 18, top + 18), f"{count} questions", fill="#182128", font=TITLE)
            wrapped(draw, (left + 18, top + 62), capabilities[layer], cell_w - 36,
                    "#35434b", BODY, spacing=7)
            draw.text((left + 18, top + cell_h - 37), level_load[level],
                      fill="#596770", font=SMALL)
    save_pair(canvas, OUT / "TASK_ABILITY_MATRIX.png")


def latest_results():
    latest = OUT / "results/latest.json"
    if not latest.exists():
        return []
    meta = json.loads(latest.read_text())
    run = OUT / "results" / meta["path"]
    return json.loads(run.read_text()).get("results", []) if run.exists() else []


def heat_color(value):
    if value is None:
        return "#e6eaec"
    red = int(210 - value * 115)
    green = int(80 + value * 95)
    blue = int(70 + value * 70)
    return f"#{red:02x}{green:02x}{blue:02x}"


def pilot_heatmap():
    results = latest_results()
    models = sorted(set(row["model"] for row in results))
    panels = models + (["combined"] if len(models) > 1 else [])
    if not panels:
        panels = ["pilot pending"]
    panel_w, panel_h = 760, 650
    canvas = Image.new("RGB", (panel_w * len(panels), panel_h), "#f5f7f8")
    draw = ImageDraw.Draw(canvas)
    for panel, model_name in enumerate(panels):
        left = panel * panel_w
        title = model_name.split("/")[-1] if model_name != "combined" else "Combined low-cost pilot"
        draw.text((left + 24, 20), title, fill="#182128", font=TITLE)
        for col, (_, label) in enumerate(LAYERS):
            draw.text((left + 175 + col * 140, 76), label, fill="#334149", font=SMALL)
        for row, (level, label) in enumerate(LEVELS):
            draw.text((left + 24, 145 + row * 115), f"{level} {label}", fill="#182128", font=BODY)
            for col, (layer, _) in enumerate(LAYERS):
                subset = [
                    result for result in results
                    if result["difficulty"] == level and result["layer"] == layer
                    and (model_name == "combined" or result["model"] == model_name)
                ]
                value = None if not subset else sum(item["verdict"]["success"] for item in subset) / len(subset)
                x0, y0 = left + 170 + col * 140, 125 + row * 115
                draw.rectangle((x0, y0, x0 + 124, y0 + 92), fill=heat_color(value),
                               outline="#aab8bf", width=2)
                label_text = "N/A" if value is None else f"{value * 100:.0f}%"
                draw.text((x0 + 35, y0 + 22), label_text, fill="#172027", font=TITLE)
                draw.text((x0 + 40, y0 + 57), f"n={len(subset)}", fill="#42515a", font=SMALL)
        draw.text((left + 24, panel_h - 40), "Exact success; pilot cells are descriptive, not rankings.",
                  fill="#5b6870", font=SMALL)
    save_pair(canvas, OUT / "PILOT_HEATMAP.png")


library_overview()
task_matrix()
pilot_heatmap()
print(json.dumps({
    "models": len(MODELS),
    "tasks": len(TASKS),
    "pilotResults": len(latest_results()),
    "outputs": ["LIBRARY_OVERVIEW", "TASK_ABILITY_MATRIX", "PILOT_HEATMAP"],
}))
