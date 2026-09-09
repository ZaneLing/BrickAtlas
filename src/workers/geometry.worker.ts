import type { GeometryChunk } from '../model/types';

self.onmessage = async (event: MessageEvent<{ base: string; chunks: GeometryChunk[] }>) => {
  let downloaded = 0;
  try {
    for (const chunk of event.data.chunks) {
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
      const output: Uint8Array[] = [];
      let outputLength = 0;
      while (true) {
        const { value, done } = await decoded.read();
        if (done) break;
        outputLength += value.byteLength;
        if (outputLength > 128 * 1024 * 1024) {
          await decoded.cancel();
          throw new Error('Geometry exceeds memory budget');
        }
        output.push(value);
      }
      const bytes = new Uint8Array(outputLength);
      let position = 0;
      for (const piece of output) { bytes.set(piece, position); position += piece.byteLength; }
      const buffer = bytes.buffer;
      self.postMessage({ type: 'chunk', groupId: chunk.groupId, buffer }, { transfer: [buffer] });
    }
    self.postMessage({ type: 'complete' });
  } catch (error) {
    self.postMessage({ type: 'error', message: error instanceof Error ? error.message : String(error) });
  }
};
