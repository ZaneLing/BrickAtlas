"""Export public questions and build a portable evaluator + hosting packages."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

from bank import HERE, ROOT, task_bank, write_json
from catalogue import catalogue, preview
from scenes import model_scene, preview_scene
from server import Arena, run_config

OUT = HERE / "release"
ZIP = "brickplan-v2.1-release.zip"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def jsonl(path, rows):
    path.write_text("".join(json.dumps(r, ensure_ascii=False, allow_nan=False) + "\n" for r in rows))


def export():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="brickplan-export-") as store:
        arena = Arena(store, run_config(), render_images=False)
        cat = catalogue(arena)
        taxonomy = {x["id"]: x for x in cat["taxonomy"]}
        rows = []
        for item in cat["questions"]:
            public = preview(arena, item["id"])
            family = taxonomy[item["category"]]
            rows.append({
                **item, "identitySeed": 0, "question": public["question"],
                "given": family["given"]["en"], "answerFormat": family["answer"]["en"],
                "scoring": family["score"]["en"],
                "publicInputJSON": json.dumps(public, ensure_ascii=False, sort_keys=True),
                "stimulusRecipe": json.dumps({"publicId": item["id"], "seed": 0, "track": "image-id",
                                             "endpoint": f"/api/preview/{item['id']}"}),
            })
        jsonl(OUT / "questions.jsonl", rows)
        write_json(OUT / "catalogue.json", cat)
        folder = OUT / "samples"
        folder.mkdir(exist_ok=True)
        arena.render_images = True
        samples = []
        for family in cat["taxonomy"]:
            candidates = [r for r in cat["questions"] if r["category"] == family["id"]]
            if family["id"] == "geometry":
                candidates = [r for r in candidates if r["kind"] == "geometry-continuation"]
            item = candidates[0]
            public = arena.media(preview(arena, item["id"]))

            def relocate(value):
                if isinstance(value, dict):
                    if value.get("mime") == "image/png" and "url" in value:
                        name = value["url"].split("/")[-1]
                        (folder / "media").mkdir(exist_ok=True)
                        shutil.copyfile(arena.media_file(value["url"]), folder / "media" / name)
                        return {**value, "url": "samples/media/" + name}
                    return {k: relocate(v) for k, v in value.items()}
                if isinstance(value, list):
                    return [relocate(v) for v in value]
                return value

            public = relocate(public)
            write_json(folder / f"{item['id']}.json", public)
            write_json(folder / f"{item['id']}.scene.json", preview_scene(arena, item["id"]))
            samples.append({**item, "preview": f"samples/{item['id']}.json",
                            "scene": f"samples/{item['id']}.scene.json",
                            "currentImage": public["observation"]["images"]["current"]["url"],
                            "targetImage": public["observation"]["images"]["target"]["url"]})
        write_json(OUT / "samples.json", samples)
        jsonl(OUT / "samples.jsonl", samples)
        write_json(OUT / "case-scene.json", model_scene(arena, "case-local"))
    print(f"Exported {len(rows)} full public question records and {len(samples)} HD examples.", flush=True)


def files(root):
    return sorted(p for p in root.rglob("*") if p.is_file()
                  and "__pycache__" not in p.parts and "node_modules" not in p.parts and not p.name.startswith(".")
                  and p.suffix not in (".pyc", ".aux", ".log", ".out", ".bbl", ".blg", ".brf", ".synctex"))


def build():
    if not (HERE / "data/release.json").exists():
        raise ValueError("Freeze the core release before building its portable archive")
    archive_files = {}
    prefix = "brickplan-v2.1/"
    for p in files(HERE):
        if OUT in p.parents:
            continue
        archive_files[prefix + str(p.relative_to(ROOT))] = p
    dependencies = [
        "benchmark/brickplan-v1.2/engine.py", "benchmark/brickplan-v1.2/visual.py",
        "benchmark/brickplan-v1.2/raster.c", "LICENSE",
    ]
    for name in dependencies:
        archive_files[prefix + name] = ROOT / name
    for folder in (ROOT / "web/brickplan", ROOT / "deliverables/brickplan-paper"):
        for p in files(folder):
            archive_files[prefix + str(p.relative_to(ROOT))] = p
    for name in ("questions.jsonl", "catalogue.json", "samples.json", "samples.jsonl"):
        archive_files[prefix + "benchmark/brickplan-v2.1/release/" + name] = OUT / name
    for p in files(OUT / "samples"):
        archive_files[prefix + "benchmark/brickplan-v2.1/release/" + str(p.relative_to(OUT))] = p
    inventory = {name[len(prefix):]: sha(p) for name, p in archive_files.items()}
    with zipfile.ZipFile(OUT / ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, p in archive_files.items():
            archive.write(p, name)
        archive.writestr(prefix + "BUNDLE-MANIFEST.json", json.dumps(inventory, indent=2) + "\n")
    # Static site and Dataset contain the same public images and metadata.
    for destination in ("static-site", "huggingface-dataset"):
        folder = OUT / destination
        folder.mkdir(exist_ok=True)
        for name in ("questions.jsonl", "catalogue.json", "samples.json", "samples.jsonl"):
            shutil.copyfile(OUT / name, folder / name)
        shutil.copytree(OUT / "samples", folder / "samples", dirs_exist_ok=True)
        shutil.copytree(HERE / "cases", folder / "cases", dirs_exist_ok=True)
        shutil.copyfile(OUT / "case-scene.json", folder / "cases/scene.json")
        case = json.loads((folder / "cases/local-vlm.json").read_text())
        # Archived model media use runtime absolute routes; static hosting uses
        # document-relative URLs so deployment also works under repository paths.
        def static_media(value):
            if isinstance(value, dict):
                return {k: ("cases" + v if k == "url" and isinstance(v, str) and v.startswith("/media/")
                            else static_media(v)) for k, v in value.items()}
            if isinstance(value, list):
                return [static_media(v) for v in value]
            return value
        write_json(folder / "cases/local-vlm.json", static_media(case))
        for name in ("paper.pdf", "supplement.pdf", "ASSET-LICENSES.json", "VALIDITY.md"):
            shutil.copyfile(HERE / name, folder / name)
        shutil.copyfile(OUT / ZIP, folder / ZIP)
        shutil.copyfile(ROOT / "deliverables/brickplan-paper/brickplan-cvpr-overleaf.zip",
                        folder / "brickplan-cvpr-overleaf.zip")
    app = HERE / "arena/app"
    site = OUT / "static-site"
    if (site / "assets").exists():
        shutil.rmtree(site / "assets")
    shutil.copytree(app / "assets", site / "assets")
    index = (app / "index.html").read_text().replace(
        "<head>", '<head><meta name="brickplan-mode" content="static" />')
    (site / "index.html").write_text(index)
    shutil.copyfile(HERE / "DATASET-CARD.md", OUT / "huggingface-dataset/README.md")
    space = OUT / "huggingface-space"
    space.mkdir(exist_ok=True)
    for name in ("Dockerfile", "README.md"):
        shutil.copyfile(HERE / "publishing" / ("SPACE.md" if name == "README.md" else name), space / name)
    shutil.copyfile(OUT / ZIP, space / ZIP)
    write_json(OUT / "manifest.json", {
        "schema": "brickplan-download/2.1", "coreManifestSha256": sha(HERE / "data/release.json"),
        "questions": 884, "sampleFamilies": 7,
        "externalHosting": "Prepared, not uploaded",
        "files": {str(p.relative_to(OUT)): sha(p) for p in files(OUT) if p.name != "manifest.json"},
    })
    shutil.copyfile(OUT / "manifest.json", site / "manifest.json")
    check()


def check():
    manifest = json.loads((OUT / "manifest.json").read_text())
    assert manifest["coreManifestSha256"] == sha(HERE / "data/release.json")
    actual = {str(p.relative_to(OUT)): sha(p) for p in files(OUT) if p.name != "manifest.json"}
    assert actual == manifest["files"], "Download artifact hashes differ"
    rows = [json.loads(line) for line in (OUT / "questions.jsonl").read_text().splitlines()]
    assert len(rows) == len(task_bank()["episodes"]) + len(task_bank()["probes"]) == manifest["questions"]
    assert len({row["stableId"] for row in rows}) == len(rows)
    assert len(json.loads((OUT / "samples.json").read_text())) == 7
    with zipfile.ZipFile(OUT / ZIP) as archive:
        assert archive.testzip() is None
        prefix = "brickplan-v2.1/"
        inventory = json.loads(archive.read(prefix + "BUNDLE-MANIFEST.json"))
        for name, digest in inventory.items():
            assert hashlib.sha256(archive.read(prefix + name)).hexdigest() == digest
    print(f"Verified {len(rows)} questions, {len(actual)} download files, {len(inventory)} bundled files; "
          f"archive {(OUT / ZIP).stat().st_size / 1e6:.1f} MB.", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("export", "build", "check"))
    args = parser.parse_args()
    {"export": export, "build": build, "check": check}[args.command]()
