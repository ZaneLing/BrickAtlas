"""Versioned command entry point; wire schemas and scoring remain 1.0 compatible."""
import argparse
import json
from pathlib import Path

from runtime import activate, HERE, ROOT


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["serve", "collect", "evaluate", "build", "render"])
    args, rest = parser.parse_known_args()
    activate()
    if args.command == "serve":
        from server import Arena, handler_for
        from http.server import ThreadingHTTPServer
        options = argparse.ArgumentParser()
        options.add_argument("--port", type=int, default=8767)
        options.add_argument("--store", type=Path, default=ROOT / "tem/brickplan-v1.1/sessions")
        options.add_argument("--probe-seed", type=int, default=20260930)
        config = options.parse_args(rest)
        arena = Arena(config.store, config.probe_seed)
        server = ThreadingHTTPServer(("127.0.0.1", config.port), handler_for(arena))
        print(f"BrickPlan 1.1: http://127.0.0.1:{config.port}", flush=True)
        server.serve_forever()
    elif args.command == "build":
        from extension_cases import EXTRA_CASES
        from cases import CASES
        from construct import build_case
        import build
        options = argparse.ArgumentParser()
        options.add_argument("--geometry", action="store_true")
        config = options.parse_args(rest)
        for case in EXTRA_CASES:
            build_case(case, HERE / "data", config.geometry)
        banks = [build.load_bank(c["id"]) for c in CASES]
        build.write_json(HERE / "data/release.json", {
            "schema": "brickplan-release/1.1", "baseRelease": "1.0",
            "structures": len(banks),
            "independentProvenanceGroups": len({b[3]["provenanceGroup"] for b in banks}),
            "episodes": sum(len(b[1]["episodes"]) for b in banks),
            "probeResponses": sum(len(b[1]["choices"]) + len(b[1]["lookahead"])
                                  + sum(len(p["members"]) for p in b[1]["counterfactual"])
                                  for b in banks),
            "cases": [b[3] for b in banks], "modelOrHumanResults": False,
        })
    elif args.command == "render":
        import render_assets
        render_assets.HERE = HERE
        render_assets.main()
    elif args.command == "collect":
        from collect import collect
        from build import write_json
        options = argparse.ArgumentParser()
        options.add_argument("--store", type=Path, required=True)
        options.add_argument("--selection", type=Path)
        options.add_argument("--metadata", type=Path)
        options.add_argument("--output", type=Path, required=True)
        config = options.parse_args(rest)
        metadata = json.loads(config.metadata.read_text()) if config.metadata else {}
        metadata["benchmarkRelease"] = "1.1"
        selection = json.loads(config.selection.read_text()) if config.selection else None
        write_json(config.output, collect(config.store, selection, metadata))
    else:
        from evaluate import evaluate
        from build import write_json
        options = argparse.ArgumentParser()
        options.add_argument("submission", type=Path)
        options.add_argument("--output", type=Path, required=True)
        config = options.parse_args(rest)
        report = evaluate(json.loads(config.submission.read_text()))
        release = json.loads((HERE / "data/release.json").read_text())
        report["benchmarkRelease"] = "1.1"
        report["caseCertificates"] = {c["case"]: c["transitionHash"] for c in release["cases"]}
        write_json(config.output, report)


if __name__ == "__main__":
    main()
