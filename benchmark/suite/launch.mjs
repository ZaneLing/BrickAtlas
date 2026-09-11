import { spawn } from 'node:child_process';
import { closeSync, existsSync, mkdirSync, openSync, readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = dirname(fileURLToPath(import.meta.url)), bench = resolve(root, '..');
const infoFile = resolve(bench, '.runtime/suite-server.json');
async function running() {
  try {
    if (!existsSync(infoFile)) return null;
    const info = JSON.parse(readFileSync(infoFile, 'utf8'));
    const response = await fetch(info.url + '/api/status', { signal: AbortSignal.timeout(1000) });
    return response.ok && (await response.json()).title === 'BrickAtlas Multitask' ? info : null;
  } catch { return null; }
}
const current = await running();
if (current) { console.log(current.url); process.exit(0); }
mkdirSync(resolve(bench, '.runtime'), { recursive: true });
const log = openSync(resolve(bench, '.runtime/suite-server.log'), 'a');
const child = spawn(process.execPath, [resolve(bench, '../node_modules/tsx/dist/cli.mjs'), resolve(root, 'server.ts')], {
  cwd: bench, detached: true, stdio: ['ignore', log, log],
});
child.unref(); closeSync(log);
for (let i = 0; i < 30; i++) {
  await new Promise(ok => setTimeout(ok, 500));
  const info = await running();
  if (info) { console.log(`BrickAtlas Multitask: ${info.url}\nPID: ${info.pid}`); process.exit(0); }
}
throw new Error('Server startup failed: inspect .runtime/suite-server.log');
