"""Generate original LDraw observation meshes with locked-source provenance."""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "brickplan_locked_mesh_export", HERE.parent / "brickplan-v1/render_assets.py")
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)
# The immutable flattener retains its locked library path; only outputs change.
exporter.HERE = HERE


if __name__ == "__main__":
    exporter.main()
