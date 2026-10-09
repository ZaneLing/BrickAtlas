"""Verify a portable archive after extraction, without predecessor checkouts."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    manifest = json.loads((ROOT / "BUNDLE-MANIFEST.json").read_text())
    for relative, expected in manifest.items():
        path = ROOT / relative
        assert path.is_file(), f"Missing bundled file: {relative}"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, f"Changed file: {relative}"
    from bank import task_bank, load_oracle
    from mission import State
    from server import Arena, run_config, portable_archive
    from catalogue import catalogue, preview
    from scenes import preview_scene, model_scene
    import tempfile
    bank = task_bank()
    task = bank["episodes"][0]
    assert load_oracle(task["id"]).distance(State(**task["start"])) == task["optimalCost"]
    with tempfile.TemporaryDirectory(prefix="brickplan-bundle-") as store:
        arena = Arena(store, run_config(), render_images=True)
        cat = catalogue(arena)
        public = preview(arena, cat["questions"][0]["id"])
        assert public["observation"]["images"]["current"]["width"] == 1920
        assert arena.model_manager().get("case-local")["recorded"]
        assert preview_scene(arena, cat["questions"][0]["id"])["frames"]
        assert model_scene(arena, "case-local")["frames"]
    app = ROOT / "benchmark/brickplan-v2.1/arena/app"
    assert (app / "index.html").is_file() and list((app / "assets").glob("*.js"))
    assert json.loads((ROOT / "web/brickplan/package.json").read_text())["dependencies"]["react"] == "19.1.1"
    import zipfile
    with zipfile.ZipFile(ROOT / "deliverables/brickplan-paper/brickplan-cvpr-overleaf.zip") as archive:
        assert archive.testzip() is None
        assert {"main.tex", "supplement.tex", "cvpr.sty"} <= set(archive.namelist())
    with zipfile.ZipFile(portable_archive()) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(manifest) + 1
    print(f"Verified {len(manifest)} files, {len(cat['questions'])} questions, native rendering, "
          "an exact oracle, original 3D scenes, React assets, independent Overleaf sources, "
          "the recorded model case and the regenerated download.")


if __name__ == "__main__":
    main()
