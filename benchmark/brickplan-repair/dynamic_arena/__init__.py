"""Local spectator arena for continuous, API-controlled assembly episodes."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'deliverables/brickplan-dynamic-arena'
MODEL = 'google/gemini-2.5-flash'
