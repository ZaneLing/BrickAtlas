"""Run archived independent reviewer rules on this release, without runtime imports."""
import hashlib
import json
from pathlib import Path
import types

HERE = Path(__file__).resolve().parent


def main():
    source = HERE / "data/independent-audit/reviewer_rules.py"
    implementation = json.loads((source.parent / "implementation.json").read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest() == implementation["sha256"]
    before = implementation["adaptation"]["before"]
    after = implementation["adaptation"]["after"]
    text = source.read_text()
    assert text.count(before) == 1
    adapted = text.replace(before, after)
    assert hashlib.sha256(adapted.encode()).hexdigest() == implementation["executedSourceSha256"]
    module = types.ModuleType("independent_review_rules")
    module.__file__ = str(source)
    exec(compile(adapted, str(source), "exec"), module.__dict__)
    output = HERE.parents[1] / "tem/brickplan-v2.2/independent-audit"
    output.mkdir(parents=True, exist_ok=True)
    module.OUT, module.RELEASE, module.DATA = output, HERE, HERE / "data"
    module.main()
    print(f"Independent recheck outputs: {output}")


if __name__ == "__main__":
    main()
