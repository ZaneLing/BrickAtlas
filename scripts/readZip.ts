import { fromBuffer, type Entry, type ZipFile } from 'yauzl';
import type { Readable } from 'node:stream';

// No extraction API: callers receive bytes and explicitly choose their output paths.
export async function readZip(buffer: Buffer) {
  const zip = await new Promise<ZipFile>((resolve, reject) => {
    fromBuffer(buffer, { lazyEntries: true, autoClose: false }, (error, file) => error ? reject(error) : resolve(file!));
  });
  const entries = await new Promise<Entry[]>((resolve, reject) => {
    const result: Entry[] = [];
    zip.on('error', reject);
    zip.on('entry', (entry: Entry) => { result.push(entry); zip.readEntry(); });
    zip.on('end', () => resolve(result));
    zip.readEntry();
  });
  return entries.map(entry => ({
    entryName: entry.fileName,
    async getData() {
      if (entry.uncompressedSize > 16 * 1024 * 1024) throw new Error('Library entry exceeds 16 MB');
      const stream = await new Promise<Readable>((resolve, reject) => {
        zip.openReadStream(entry, (error, data) => error ? reject(error) : resolve(data!));
      });
      const chunks: Buffer[] = [];
      let size = 0;
      for await (const chunk of stream) {
        size += chunk.length;
        if (size > 16 * 1024 * 1024) { stream.destroy(); throw new Error('Library entry exceeds 16 MB'); }
        chunks.push(chunk);
      }
      return Buffer.concat(chunks);
    },
  }));
}
