import { defineConfig } from 'vite';

export default defineConfig({
  base: '/ui/',
  build: { outDir: '../api/static', emptyOutDir: true },
  server: { proxy: { '/v1': 'http://127.0.0.1:8770', '/health': 'http://127.0.0.1:8770' } },
});
