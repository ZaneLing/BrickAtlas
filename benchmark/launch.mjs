import { spawn } from 'node:child_process';
import { closeSync, existsSync, mkdirSync, openSync, readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const infoPath = resolve(root, '.runtime/server.json');
if (existsSync(infoPath)) {
  try {
    const info = JSON.parse(readFileSync(infoPath, 'utf8'));
    const response = await fetch(`${info.url}/api/status`, { signal: AbortSignal.timeout(1500) });
    if (response.ok && (await response.json()).title === 'Brick Atlas Benchmark') {
      console.log(`Benchmark already running: ${info.url}`);
      process.exit(0);
    }
  } catch { /* A stale server record does not imply a running process. */ }
}
mkdirSync(resolve(root, '.runtime'), { recursive: true });
const log = openSync(resolve(root, '.runtime/server.log'), 'a');
const child = spawn(process.execPath, [resolve(root, '../node_modules/tsx/dist/cli.mjs'), resolve(root, 'server.ts')], {
  cwd: root, detached: true, stdio: ['ignore', log, log],
});
child.unref();
closeSync(log);
for (let i = 0; i < 30; i++) {
  await new Promise(resolve => setTimeout(resolve, 500));
  if (!existsSync(infoPath)) continue;
  try {
    const info = JSON.parse(readFileSync(infoPath, 'utf8'));
    const response = await fetch(`${info.url}/api/status`, { signal: AbortSignal.timeout(1000) });
    if (response.ok && (await response.json()).title === 'Brick Atlas Benchmark') {
      console.log(`Benchmark: ${info.url}\nPID: ${info.pid}\nLog: ${root}/.runtime/server.log`);
      process.exit(0);
    }
  } catch { /* Wait for the independent server to become ready. */ }
}
console.error(`Server did not become ready. Inspect ${root}/.runtime/server.log`);
process.exitCode = 1;
