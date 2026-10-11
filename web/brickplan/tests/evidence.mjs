import { readFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
export const benchmark = path.join(root, 'benchmark/brickplan-v2.3');
export const out = path.resolve(process.env.BRICKPLAN_TEST_OUTPUT || '/tmp/brickplan-v23-work/frontend');
if (out === root || out.startsWith(root + path.sep)) {
  throw new Error('Intermediate frontend evidence must be outside the workspace');
}
const sha = bytes => createHash('sha256').update(bytes).digest('hex');

export async function downloadedJSON(page, button) {
  const [download] = await Promise.all([page.waitForEvent('download'), button.click()]);
  const chunks = [];
  for await (const chunk of await download.createReadStream()) chunks.push(chunk);
  return JSON.parse(Buffer.concat(chunks).toString('utf8'));
}

export async function evidence() {
  const frontendFiles = {};
  async function visit(folder) {
    for (const entry of await readdir(folder, { withFileTypes: true })) {
      if (entry.name.startsWith('.') || ['node_modules', '__pycache__'].includes(entry.name)) continue;
      const file = path.join(folder, entry.name);
      if (entry.isDirectory()) await visit(file);
      else frontendFiles[path.relative(root, file)] = sha(await readFile(file));
    }
  }
  await visit(path.join(root, 'web/brickplan'));
  await visit(path.join(benchmark, 'arena/app'));
  for (const name of ['catalogue.py', 'package_release.py', 'scenes.py', 'server.py',
    'test_workbench.mjs', 'test_workbench_integration.mjs']) {
    const file = path.join(benchmark, name);
    frontendFiles[path.relative(root, file)] = sha(await readFile(file));
  }
  const certificate = JSON.parse(await readFile(path.join(benchmark, 'data/certificate.json')));
  return {
    bankHash: certificate.tasksHash,
    bankFileSha256: sha(await readFile(path.join(benchmark, 'data/tasks.private.json'))),
    frontendFiles,
  };
}
