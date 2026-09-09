import { spawn } from 'node:child_process';
import { openSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import net from 'node:net';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
let port = 5173;
function available(port) {
  return new Promise(resolve => {
    const server = net.createServer();
    server.once('error', () => resolve(false));
    server.listen(port, '127.0.0.1', () => server.close(() => resolve(true)));
  });
}
while (!await available(port)) port++;
mkdirSync(resolve(root, '.tools'), { recursive: true });
const log = openSync(resolve(root, '.tools/dev-server.log'), 'a');
const child = spawn(process.execPath, ['node_modules/vite/bin/vite.js', '--host', '127.0.0.1', '--port', String(port), '--strictPort'], {
  cwd: root, detached: true, stdio: ['ignore', log, log],
});
child.unref();
console.log(`Brick Atlas: http://127.0.0.1:${port}\nPID: ${child.pid}\nLog: ${root}/.tools/dev-server.log`);
