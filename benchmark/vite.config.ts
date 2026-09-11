import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
export default defineConfig({
  root: resolve(root, 'web'),
  envDir: false,
  plugins: [react()],
  server: {
    fs: {
      strict: true,
      allow: [resolve(root, 'web'), resolve(root, 'shared'), resolve(root, '../node_modules')],
      deny: ['**/.env', '**/.env.*', '**/core/**', '**/.runtime/**', '**/results/**'],
    },
  },
  build: {
    outDir: resolve(root, 'dist'),
    emptyOutDir: true,
    rollupOptions: { input: {
      main: resolve(root, 'web/index.html'),
      render: resolve(root, 'web/render.html'),
    } },
  },
});
