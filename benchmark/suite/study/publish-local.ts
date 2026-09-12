import assert from 'node:assert/strict';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, renameSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

export function publishLocal(dir: string, files: Record<string, unknown>) {
  const verify = () => {
    for (const [name, value] of Object.entries(files)) {
      const raw = readFileSync(resolve(dir, name));
      assert.deepEqual(Buffer.isBuffer(value) ? raw : JSON.parse(raw.toString('utf8')), value,
        `Published local evidence changed: ${name}`);
    }
  };
  if (existsSync(dir)) { verify(); return; }
  // Stage outside the discoverable local/ tree; readers only see a complete job.
  mkdirSync(dirname(dir), { recursive: true });
  const staging = mkdtempSync(resolve(dirname(dirname(dir)), '.local-import-'));
  try {
    for (const [name, value] of Object.entries(files)) {
      const path = resolve(staging, name); mkdirSync(dirname(path), { recursive: true });
      writeFileSync(path, Buffer.isBuffer(value) ? value : JSON.stringify(value, null, 2) + '\n');
    }
    try { renameSync(staging, dir); }
    catch (error) {
      if (!existsSync(dir)) throw error;
      verify();
    }
  } finally { rmSync(staging, { recursive: true, force: true }); }
}
