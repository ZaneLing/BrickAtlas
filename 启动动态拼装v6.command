#!/bin/bash
set -e
cd "$(dirname "$0")"
if /usr/bin/curl -fsS http://127.0.0.1:8767/health 2>/dev/null | /usr/bin/grep -q '"version": 6'; then
    open http://127.0.0.1:8767/A
    exit 0
fi
export PYTHONPATH=benchmark/brickplan-repair:benchmark/brickplan-repair/eval:benchmark/brickplan-v1
echo '动态拼装 v6：打开 http://127.0.0.1:8767/A，B、C 分别使用对应字母。'
echo '请保留这个窗口；按 Ctrl+C 可以停止服务。'
benchmark/.runtime/mlx-env/bin/python -u benchmark/brickplan-repair/dynamic_v6/human_server.py --port 8767 &
brickplan_server_pid=$!
trap 'kill "$brickplan_server_pid" 2>/dev/null || true' EXIT INT TERM
for brickplan_attempt in {1..30}; do
    if /usr/bin/curl -fsS http://127.0.0.1:8767/health >/dev/null 2>&1; then
        open http://127.0.0.1:8767/A
        break
    fi
    sleep 0.2
done
wait "$brickplan_server_pid"
