#!/bin/bash
cd "$(dirname "$0")" || exit 1
task_python="$PWD/benchmark/.runtime/mlx-env/bin/python"
if ! "$task_python" -c 'import urllib.request; urllib.request.urlopen("http://127.0.0.1:8799/objects/models.json", timeout=1)' >/dev/null 2>&1; then
  PYTHONPATH="$PWD/benchmark/brickplan-repair" "$task_python" -m public_preview_server --port 8799 &
  task_server_pid=$!
  trap 'kill "$task_server_pid" 2>/dev/null' EXIT
  for attempt in {1..30}; do
    if "$task_python" -c 'import urllib.request; urllib.request.urlopen("http://127.0.0.1:8799/objects/models.json", timeout=1)' >/dev/null 2>&1; then break; fi
    sleep 0.2
  done
  /usr/bin/open 'http://127.0.0.1:8799/objects/index.html'
  echo '完整物件看图页已打开。关闭这个终端窗口将停止本次预览服务。'
  wait "$task_server_pid"
else
  /usr/bin/open 'http://127.0.0.1:8799/objects/index.html'
fi
