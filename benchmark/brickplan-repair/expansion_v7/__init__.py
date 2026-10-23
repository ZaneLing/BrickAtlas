"""Additive, source-linked long assembly and repeated-incident extension."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
for relative in ('benchmark/brickplan-v1', 'benchmark/brickplan-repair/eval',
                 'benchmark/brickplan-repair'):
    path = str(ROOT / relative)
    if path not in sys.path:
        sys.path.insert(0, path)
OUT = ROOT / 'deliverables/brickplan-expansion-v7'
PROTOCOL = 'brickplan-expansion/7'
