import { spawn } from 'node:child_process';
import { openSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import net from 'node:net';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const port = 5173;
const url = `http://127.0.0.1:${port}`;

function available(port) {
  return new Promise(resolve => {
    const server = net.createServer();
    server.once('error', () => resolve(false));
    server.listen(port, '127.0.0.1', () => server.close(() => resolve(true)));
  });
}

async function brickAtlasIsRunning() {
  const abort = new AbortController();
  const timer = setTimeout(() => abort.abort(), 1500);
  try {
    const response = await fetch(url, { signal: abort.signal });
    const html = await response.text();
    return response.ok && html.includes('<title>Brick Atlas');
  } catch {
    return false;
  } finally {
    clearTimeout(timer);
  }
}

if (!await available(port)) {
  if (await brickAtlasIsRunning()) {
    console.log(`Brick Atlas is already running: ${url}`);
    process.exit(0);
  }
  console.error(`Port ${port} is occupied by another application. Brick Atlas always uses ${url}.`);
  process.exit(1);
}

mkdirSync(resolve(root, '.tools'), { recursive: true });
const log = openSync(resolve(root, '.tools/dev-server.log'), 'a');
const child = spawn(process.execPath, ['node_modules/vite/bin/vite.js', '--host', '127.0.0.1', '--port', String(port), '--strictPort'], {
  cwd: root, detached: true, stdio: ['ignore', log, log],
});
child.unref();
writeFileSync(resolve(root, '.tools/dev-server.pid'), `${child.pid}\n`);
console.log(`Brick Atlas: ${url}\nPID: ${child.pid}\nLog: ${root}/.tools/dev-server.log`);
