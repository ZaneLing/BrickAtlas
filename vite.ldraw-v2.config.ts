import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'node:path';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist-ldraw-v2',
    // Existing source/mesh assets are served from the repository public root.
    // Avoid copying multi-version geometry into a second distribution tree.
    copyPublicDir: false,
    rollupOptions: {
      input: { review: resolve(import.meta.dirname, 'ldraw-v2.html'),
        render: resolve(import.meta.dirname, 'ldraw-v2-render.html') },
      output: { manualChunks: { three: ['three'], react: ['react', 'react-dom'] } },
    },
  },
});
