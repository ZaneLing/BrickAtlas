"""Prepare read-only base references, HTML branding, or labelled UI fixtures."""
import argparse
import json
from runtime import HERE, BASE, OUT, activate


def assets():
    for relative, target in (
        ("data/roadster-body", BASE / "data/roadster-body"),
        ("data/kart-deck", BASE / "data/kart-deck"),
        ("arena/app.js", BASE / "arena/app.js"),
        ("arena/style.css", BASE / "arena/style.css"),
    ):
        import os
        path = HERE / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.is_symlink():
            if path.resolve() != target.resolve():
                raise ValueError(f"Unexpected dependency: {path}")
        elif path.exists():
            raise ValueError(f"Refusing to replace {path}")
        else:
            path.symlink_to(os.path.relpath(target, path.parent), target_is_directory=target.is_dir())
    release_path = HERE / "data/release.json"
    if release_path.exists():
        release = json.loads(release_path.read_text())
        text = (BASE / "arena/index.html").read_text()
        text = text.replace("<span>1.0</span>", "<span>1.1</span>")
        text = text.replace("BrickPlan 1.0 · 2 structures · 8 episodes · 26 probe responses",
                            f"BrickPlan 1.1 · {release['structures']} structures · "
                            f"{release['episodes']} episodes · {release['probeResponses']} probe responses")
        (HERE / "arena/index.html").write_text(text)


def fixtures(url):
    activate()
    from build import load_bank, write_json
    from cases import CASES
    from client import Client
    from session import Session
    from server import Arena
    import tempfile
    client = Client(url)
    prepared = []
    with tempfile.TemporaryDirectory() as store:
        assignment = Arena(store)
    for config in CASES:
        domain, tasks, _, _ = load_bank(config["id"])
        for mode in ("full", "repair"):
            task = next(t for t in tasks["episodes"] if t["mode"] == mode)
            public_id = next(k for k, (_, t) in assignment.tasks.items() if t["id"] == task["id"])
            result = client.start(public_id, 31)
            mirror = Session(domain, task, 31)
            assert mirror.observation() == result["observation"]
            actions = [{"type": "diagnose", "needsRework": mode == "repair"}]
            for action in task["completionWitness"]:
                public = mirror.public_action(action)
                actions.append(public)
                mirror.submit({"requestId": str(mirror.revision), "revision": mirror.revision,
                               "action": public})
            actions.append({"type": "finish"})
            prepared.append({
                "label": f"software-oracle-{task['id']}", "case": config["id"], "mode": mode,
                "sessionId": result["sessionId"], "actions": actions,
                "optimalActions": task["optimalActions"], "minimumDetaches": task["minimumDetaches"],
            })
    write_json(OUT / "ui-fixtures.json", {"url": url, "fixtures": prepared})
    print(f"Prepared {len(prepared)} labelled software UI fixtures.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["assets", "fixtures"])
    parser.add_argument("--url", default="http://127.0.0.1:8767")
    args = parser.parse_args()
    assets() if args.command == "assets" else fixtures(args.url)
