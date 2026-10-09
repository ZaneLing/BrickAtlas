"""Prepare labelled oracle UI controls through the public session API."""
from build import HERE, load_bank, write_json
from cases import CASES
from client import Client
from session import Session


def main():
    client = Client()
    catalog = client.tasks()
    fixtures = []
    for config, mode in ((CASES[0], "full"), (CASES[1], "repair")):
        domain, tasks, _, _ = load_bank(config["id"])
        task = next(t for t in tasks["episodes"] if t["mode"] == mode)
        # Match the same frozen public task assignment as the server, then verify its observation.
        from server import Arena
        import tempfile
        with tempfile.TemporaryDirectory() as store:
            assignment = Arena(store)
            public_id = next(k for k, (_, t) in assignment.tasks.items() if t["id"] == task["id"])
        result = client.start(public_id, 31)
        mirror = Session(domain, task, 31)
        assert mirror.observation() == result["observation"]
        actions = [{"type": "diagnose", "needsRework": mode == "repair"}]
        for a in task["completionWitness"]:
            action = mirror.public_action(a)
            actions.append(action)
            mirror.submit({"requestId": str(mirror.revision), "revision": mirror.revision, "action": action})
        actions.append({"type": "finish"})
        fixtures.append({"label": f"software-oracle-{task['id']}", "mode": mode,
                         "sessionId": result["sessionId"], "actions": actions,
                         "optimalActions": task["optimalActions"],
                         "minimumDetaches": task["minimumDetaches"]})
    write_json(HERE.parents[1] / "tem/brickplan-v1/validation/ui-fixtures.json", fixtures)
    print("Prepared two software-oracle UI fixtures; these are not model or human trials.")


if __name__ == "__main__":
    main()
