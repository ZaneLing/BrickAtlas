#!/bin/bash
set -e
task_root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$task_root"
export PYTHONPATH="$task_root/benchmark/brickplan-repair"
exec "$task_root/benchmark/.runtime/mlx-env/bin/python" -m bench_design.launch_review
