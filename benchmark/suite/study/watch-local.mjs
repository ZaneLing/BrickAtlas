import { spawn, execFileSync } from 'node:child_process';
import { closeSync, mkdirSync, openSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url)), bench = resolve(here, '../..');
const root = resolve(bench, '.runtime/vlm-training');
mkdirSync(root, { recursive: true });
const python = process.env.TRAIN_PYTHON || resolve(bench, '.runtime/train-env/bin/python');
const active = execFileSync(python, ['-c',
  'import sys; sys.path.insert(0, sys.argv[1]); from pathlib import Path; import importlib; m = importlib.import_module("follow-matrix"); print(m.matrix_running(Path(sys.argv[2])))',
  here, root], { encoding: 'utf8' }).trim() === 'True';
if (!active) throw new Error('No active training matrix; inspect existing jobs before explicit recovery');
const logPath = resolve(bench, '.runtime/matrix-validation.log');
const log = openSync(logPath, 'a'), started = Date.now() / 1000;
const child = spawn(python, ['-u', resolve(here, 'follow-matrix.py')], {
  cwd: resolve(bench, '..'), detached: true, stdio: ['ignore', log, log],
  env: { ...process.env, NODE_BINARY: process.execPath },
});
closeSync(log);
let exited = false;
child.on('exit', () => { exited = true; });
child.on('error', error => { console.error(error.message); exited = true; });
await new Promise(ok => setTimeout(ok, 1000));
if (exited) throw new Error(`Watcher did not start (another watcher may own the lock); inspect ${logPath}`);
writeFileSync(resolve(root, 'watcher.json'), JSON.stringify({ pid: child.pid, startedAt: started }) + '\n');
child.unref();
let previous;
try { previous = JSON.parse(readFileSync(resolve(root, 'validation-status.json'), 'utf8')); } catch {}
console.log(JSON.stringify({ pid: child.pid, log: logPath, previousValidation: previous ?? null,
  note: 'Detached validator started; validation-status.json records success or failure, not process existence.' }, null, 2));
