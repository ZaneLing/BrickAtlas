import type { GeometryChunk } from '../model/types';

self.onmessage = async (event: MessageEvent<{ base: string; chunks: GeometryChunk[] }>) => {
  let downloaded = 0;
  try {
    for (const chunk of event.data.chunks) {
      const ranges = chunk.buckets.flatMap(bucket => Object.values(bucket.attributes));
      if (ranges.some(a => !Number.isSafeInteger(a.offset) || !Number.isSafeInteger(a.count) || a.offset < 0 || a.count < 0))
        throw new Error('Invalid geometry byte range');
      const expectedLength = Math.max(0, ...ranges.map(a => a.offset + a.count * 4));
      if (expectedLength > 512 * 1024 * 1024) throw new Error('Geometry exceeds memory budget');
      const response = await fetch(`${event.data.base}${chunk.url}`);
      if (!response.ok) throw new Error(`${chunk.url}: HTTP ${response.status}`);
      const reader = response.body?.getReader();
      if (!reader) throw new Error('Streaming response unavailable');
      const pieces: Uint8Array[] = [];
      let length = 0;
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        pieces.push(value);
        length += value.byteLength;
        downloaded += value.byteLength;
        if (length > chunk.bytes + 1024) throw new Error(`Unexpected size: ${chunk.url}`);
        self.postMessage({ type: 'progress', downloaded, groupId: chunk.groupId });
      }
      const compressed = new Uint8Array(length);
      let offset = 0;
      for (const piece of pieces) { compressed.set(piece, offset); offset += piece.byteLength; }
      const digest = await crypto.subtle.digest('SHA-256', compressed);
      const hex = [...new Uint8Array(digest)].map(b => b.toString(16).padStart(2, '0')).join('');
      if (hex !== chunk.sha256) throw new Error(`Asset checksum mismatch: ${chunk.url}`);
      const stream = new Blob([compressed]).stream().pipeThrough(new DecompressionStream('gzip'));
      const decoded = stream.getReader();
      // Large original Technic sources exceed 128 MB per material batch.
      // Preallocate the exact manifest range instead of retaining fragments
      // plus a second full copy. Still bound expansion and require exact size.
      const bytes = new Uint8Array(expectedLength);
      let outputLength = 0;
      while (true) {
        const { value, done } = await decoded.read();
        if (done) break;
        if (outputLength + value.byteLength > expectedLength) {
          await decoded.cancel();
          throw new Error('Geometry exceeds declared byte range');
        }
        bytes.set(value, outputLength);
        outputLength += value.byteLength;
      }
      if (outputLength !== expectedLength) throw new Error('Incomplete geometry byte range');
      const buffer = bytes.buffer;
      self.postMessage({ type: 'chunk', groupId: chunk.groupId, buffer }, { transfer: [buffer] });
    }
    self.postMessage({ type: 'complete' });
  } catch (error) {
    self.postMessage({ type: 'error', message: error instanceof Error ? error.message : String(error) });
  }
};
