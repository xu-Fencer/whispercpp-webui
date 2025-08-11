import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',  // 后端接口地址（根据实际情况修改）
      '/ws': 'ws://localhost:8000',    // WebSocket 代理
    },
  },
  build: {
    outDir: 'dist',  // 输出目录
  },
});
