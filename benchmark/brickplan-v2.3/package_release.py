"""Export practice questions and package the evaluator, not source construction."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

from bank import HERE, ROOT, task_bank, write_json
from catalogue import catalogue, preview
from mission import canonical_hash
from scenes import model_scene, preview_scene
from server import Arena, run_config

OUT = HERE / "release"
ZIP = "brickplan-v2.3-release.zip"
EXPORT_FILES = ("questions.jsonl", "catalogue.json", "samples.json", "samples.jsonl", "case-scene.json")
EXPORT_RUNTIME = ("package_release.py", "bank.py", "catalogue.py", "probes.py", "session.py",
                  "scenes.py", "visual.py", "mission.py", "server.py", "arena/meshes.json",
                  "cases/local-vlm.json", "cases/local-vlm.authoritative.json", "cases/task.v2.1.json")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def jsonl(path, rows):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text("".join(json.dumps(r, ensure_ascii=False, allow_nan=False) + "\n" for r in rows))
    temporary.replace(path)


def export_questions(arena):
    cat = catalogue(arena)
    taxonomy = {x["id"]: x for x in cat["taxonomy"]}
    rows = []
    for item in cat["questions"]:
        public = preview(arena, item["id"])
        family = taxonomy[item["category"]]
        rows.append({
            **item, "identitySeed": arena.seed, "question": public["question"],
            "given": family["given"]["en"], "answerFormat": family["answer"]["en"],
            "scoring": family["score"]["en"],
            "metadataScope": "Practice catalogue only. Policies receive publicInputJSON, not cohort/provenance metadata.",
            "publicInputJSON": json.dumps(public, ensure_ascii=False, sort_keys=True),
            "stimulusRecipe": json.dumps({"publicId": item["id"], "seed": arena.seed, "track": arena.track,
                                         "endpoint": f"/api/preview/{item['id']}"}),
        })
    jsonl(OUT / "questions.jsonl", rows)
    write_json(OUT / "catalogue.json", cat)
    print(f"Exported {len(rows)} public question records.", flush=True)
    return cat


def questions():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="brickplan-questions-") as store:
        export_questions(Arena(store, run_config(), render_images=False))


def sample_question(cat, family):
    candidates = (r for r in cat["questions"] if r["category"] == family)
    if family == "geometry":
        candidates = (r for r in candidates if r["evaluationCohort"] == "primary-matched")
    item = next(candidates, None)
    if item is None:
        raise ValueError(f"No exportable sample for {family}; geometry requires primary-matched")
    return item


def export():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="brickplan-export-") as store:
        arena = Arena(store, run_config(), render_images=False)
        cat = export_questions(arena)
        folder = OUT / "samples"
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(exist_ok=True)
        arena.render_images = True
        samples = []
        for family in cat["taxonomy"]:
            item = sample_question(cat, family["id"])
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
        paths = [OUT / name for name in EXPORT_FILES]
        paths += files(folder)
        write_json(OUT / "export-manifest.json", {
            "bankHash": canonical_hash(task_bank()),
            "runtimeFiles": {name: sha(HERE / name) for name in EXPORT_RUNTIME},
            "files": {str(p.relative_to(OUT)): sha(p) for p in paths}})
    print(f"Exported {len(cat['questions'])} full public question records and {len(samples)} HD examples.", flush=True)


def files(root):
    return sorted(p for p in root.rglob("*") if p.is_file()
                  and "__pycache__" not in p.parts and "node_modules" not in p.parts and not p.name.startswith(".")
                  and p.suffix not in (".pyc", ".aux", ".log", ".out", ".bbl", ".blg", ".brf", ".synctex"))


def check_export():
    manifest = json.loads((OUT / "export-manifest.json").read_text())
    assert manifest["bankHash"] == canonical_hash(task_bank()), "Run export for the current bank"
    assert manifest["runtimeFiles"] == {name: sha(HERE / name) for name in EXPORT_RUNTIME}, "Re-export changed runtime inputs"
    paths = [OUT / name for name in EXPORT_FILES] + files(OUT / "samples")
    assert {str(p.relative_to(OUT)) for p in paths} == set(manifest["files"]), "Unexpected public export files"
    for name, digest in manifest["files"].items():
        assert sha(OUT / name) == digest, f"Stale public export: {name}"
    cat = json.loads((OUT / "catalogue.json").read_text())
    assert cat["release"] == "2.3" and cat["bankHash"] == manifest["bankHash"]
    return cat


def prepare_site(folder):
    """Prepare the real static UI without needing final manuscript artifacts."""
    check_export()
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)
    for name in ("questions.jsonl", "catalogue.json", "samples.json", "samples.jsonl"):
        shutil.copyfile(OUT / name, folder / name)
    shutil.copytree(OUT / "samples", folder / "samples")
    shutil.copytree(HERE / "cases", folder / "cases")
    shutil.copyfile(OUT / "case-scene.json", folder / "cases/scene.json")
    assert sha(folder / "cases/local-vlm.json") == sha(HERE / "cases/local-vlm.json")
    app = HERE / "arena/app"
    shutil.copytree(app / "assets", folder / "assets")
    index = (app / "index.html").read_text().replace(
        "<head>", '<head><meta name="brickplan-mode" content="static" />')
    (folder / "index.html").write_text(index)


def build():
    if not (HERE / "data/release.json").exists():
        raise ValueError("Freeze the core release before building its portable archive")
    cat = check_export()
    expected_outputs = {*EXPORT_FILES, "export-manifest.json", "samples", ZIP, "manifest.json",
                        "static-site", "huggingface-dataset", "huggingface-space"}
    assert not {p.name for p in OUT.iterdir() if not p.name.startswith(".")} - expected_outputs, "Unexpected stale release outputs"
    core = json.loads((HERE / "data/release.json").read_text())
    assert core["claims"]["bankHash"] == canonical_hash(task_bank()), "Core release belongs to another bank"
    for name, digest in core["files"].items():
        assert sha(HERE / name) == digest, f"Core release changed since freeze: {name}"
    for name, digest in core["dependencies"].items():
        assert sha(ROOT / name) == digest, f"Release dependency changed since freeze: {name}"
    archive_files = {}
    prefix = "brickplan-v2.3/"
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
            # The editable sources already ship in the Overleaf ZIP, and
            # the PDFs already ship at their canonical benchmark paths.
            if folder.name == "brickplan-paper" and (
                    p.relative_to(folder).parts[0] == "overleaf"
                    or p.name in ("brickplan-main.pdf", "brickplan-supplement.pdf")):
                continue
            archive_files[prefix + str(p.relative_to(ROOT))] = p
    for name in ("questions.jsonl", "catalogue.json", "samples.json", "samples.jsonl", "case-scene.json", "export-manifest.json"):
        archive_files[prefix + "benchmark/brickplan-v2.3/release/" + name] = OUT / name
    for p in files(OUT / "samples"):
        archive_files[prefix + "benchmark/brickplan-v2.3/release/" + str(p.relative_to(OUT))] = p
    bundle_readme = (
            "# BrickPlan 2.3 evaluator/runtime bundle\n\n"
            "This archive runs the frozen evaluator and original-geometry practice UI. "
            "It is not a complete source-construction checkout.\n\n"
            "Install benchmark/brickplan-v2.3/requirements.txt, then run "
            "`python benchmark/brickplan-v2.3/server.py serve --port 8783`.\n\n"
            "Read paper.pdf and supplement.pdf under benchmark/brickplan-v2.3. "
            "The complete editable manuscript is in "
            "deliverables/brickplan-paper/brickplan-cvpr-overleaf.zip.\n\n"
            "Rebuilding candidate admissions or fully rerunning source-provenance audits "
            "requires the matching git source checkout, including assets-source/brickplan-v23, "
            "the locked LDraw library, web/public/models/v23-* manifests/provenance, "
            "construction geometry dependencies and the archived data/source-intake records. "
            "Raw source assets are not promised by this runtime bundle.\n\n"
            "questions.jsonl contains practice-only catalogue/provenance metadata. "
            "Policy inputs are the publicInputJSON records or authoritative observation API; "
            "do not expose cohort, source, stable ID or scoring metadata to evaluated policies.\n")
    inventory = {name[len(prefix):]: sha(p) for name, p in archive_files.items()}
    inventory["BUNDLE-README.md"] = hashlib.sha256(bundle_readme.encode()).hexdigest()
    with zipfile.ZipFile(OUT / ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, p in archive_files.items():
            archive.write(p, name)
        archive.writestr(prefix + "BUNDLE-MANIFEST.json", json.dumps(inventory, indent=2) + "\n")
        archive.writestr(prefix + "BUNDLE-README.md", bundle_readme)
    # Static site and Dataset contain the same public images and metadata.
    for destination in ("static-site", "huggingface-dataset"):
        folder = OUT / destination
        prepare_site(folder)
        for name in ("paper.pdf", "supplement.pdf", "ASSET-LICENSES.json", "VALIDITY.md"):
            shutil.copyfile(HERE / name, folder / name)
        shutil.copyfile(OUT / ZIP, folder / ZIP)
        shutil.copyfile(ROOT / "deliverables/brickplan-paper/brickplan-cvpr-overleaf.zip",
                        folder / "brickplan-cvpr-overleaf.zip")
    site = OUT / "static-site"
    shutil.copyfile(HERE / "DATASET-CARD.md", OUT / "huggingface-dataset/README.md")
    space = OUT / "huggingface-space"
    if space.exists():
        shutil.rmtree(space)
    space.mkdir(exist_ok=True)
    for name in ("Dockerfile", "README.md"):
        source = HERE / "publishing" / ("SPACE.md" if name == "README.md" else name)
        text = source.read_text().replace("2.1", cat["release"])
        if name == "README.md":
            text = text.replace("145 interactive episodes, 739 diagnostic questions and 11 source groups.",
                                f"{cat['counts']['episodes']} interactive episodes, "
                                f"{cat['counts']['probes']} diagnostic questions and "
                                f"{cat['counts']['sources']} source groups.")
            text = text.replace("an actual four-call SmolVLM integration case.",
                                "a historical BrickPlan 2.1 SmolVLM integration case, not a new 2.3 measurement.")
        (space / name).write_text(text)
    shutil.copyfile(OUT / ZIP, space / ZIP)
    write_json(OUT / "manifest.json", {
        "schema": "brickplan-download/2.3", "coreManifestSha256": sha(HERE / "data/release.json"),
        "bankHash": canonical_hash(task_bank()),
        "questions": len(cat["questions"]), "sampleFamilies": len(cat["taxonomy"]),
        "externalHosting": "Prepared, not uploaded",
        "files": {str(p.relative_to(OUT)): sha(p) for p in files(OUT) if p.name != "manifest.json"},
    })
    shutil.copyfile(OUT / "manifest.json", site / "manifest.json")
    check()


def check():
    manifest = json.loads((OUT / "manifest.json").read_text())
    cat = check_export()
    assert manifest["bankHash"] == canonical_hash(task_bank())
    assert manifest["coreManifestSha256"] == sha(HERE / "data/release.json")
    actual = {str(p.relative_to(OUT)): sha(p) for p in files(OUT) if p.name != "manifest.json"}
    assert actual == manifest["files"], "Download artifact hashes differ"
    rows = [json.loads(line) for line in (OUT / "questions.jsonl").read_text().splitlines()]
    assert len(rows) == len(task_bank()["episodes"]) + len(task_bank()["probes"]) == manifest["questions"]
    assert len({row["stableId"] for row in rows}) == len(rows)
    assert len(json.loads((OUT / "samples.json").read_text())) == len(cat["taxonomy"]) == manifest["sampleFamilies"]
    with zipfile.ZipFile(OUT / ZIP) as archive:
        assert archive.testzip() is None
        prefix = "brickplan-v2.3/"
        inventory = json.loads(archive.read(prefix + "BUNDLE-MANIFEST.json"))
        for name in ("quality.py", "scenes.py", "session.py", "probes.py", "server.py"):
            assert f"benchmark/brickplan-v2.3/{name}" in inventory
        for name, digest in inventory.items():
            assert hashlib.sha256(archive.read(prefix + name)).hexdigest() == digest
    for destination in ("static-site", "huggingface-dataset"):
        assert sha(OUT / destination / "cases/local-vlm.json") == sha(HERE / "cases/local-vlm.json")
    print(f"Verified {len(rows)} questions, {len(actual)} download files, {len(inventory)} bundled files; "
          f"archive {(OUT / ZIP).stat().st_size / 1e6:.1f} MB.", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("questions", "export", "build", "check"))
    args = parser.parse_args()
    {"questions": questions, "export": export, "build": build, "check": check}[args.command]()
