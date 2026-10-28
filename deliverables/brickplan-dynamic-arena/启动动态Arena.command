#!/bin/bash
set -e
task_root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$task_root"
if ! curl -fsS http://127.0.0.1:8810/health >/dev/null 2>&1; then
  nohup env PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m dynamic_arena.server >> deliverables/brickplan-dynamic-arena/server.log 2>&1 < /dev/null &
  for attempt in {1..30}; do
    if curl -fsS http://127.0.0.1:8810/health >/dev/null 2>&1; then break; fi
    sleep 0.2
  done
fi
open http://127.0.0.1:8810/library
