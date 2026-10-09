import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: '../../benchmark/brickplan-v2.1/arena/app',
    emptyOutDir: true,
    rollupOptions: { output: { manualChunks: { three: ['three', 'three/addons/controls/OrbitControls.js'] } } },
  },
  server: {
    port: 5174,
    proxy: Object.fromEntries(['/api', '/media', '/download', '/paper.pdf', '/supplement.pdf']
      .map(path => [path, 'http://127.0.0.1:8769'])),
  },
});
