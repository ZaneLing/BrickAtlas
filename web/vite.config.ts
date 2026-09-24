import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { resolve } from 'node:path';

export default defineConfig({
  root: import.meta.dirname,
  envDir: resolve(import.meta.dirname, '..'),
  cacheDir: resolve(import.meta.dirname, '../tem/build/vite-cache'),
  // Keep HTML proxy cache keys aligned with the shared benchmark mount.
  resolve: { preserveSymlinks: true },
  plugins: [react()],
  server: {
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
    fs: { allow: [resolve(import.meta.dirname, '..')] },
  },
  preview: {
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
  },
  build: {
    outDir: resolve(import.meta.dirname, '../tem/build/web'),
    emptyOutDir: true,
    rollupOptions: {
      output: { manualChunks: { three: ['three'], react: ['react', 'react-dom'] } },
    },
  },
  test: {
    root: resolve(import.meta.dirname, '..'),
    include: ['web/tests/unit/**/*.test.ts'],
  },
});
