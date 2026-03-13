import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api/v1/auth': {
        target: 'http://teleflow-auth-service:8001',
        changeOrigin: true,
      },
      '/api/v1/content': {
        target: 'http://teleflow-content-service:8002',
        changeOrigin: true,
      },
      '/api/v1/publishing': {
        target: 'http://teleflow-publishing-service:8004',
        changeOrigin: true,
      },
      '/api/v1/funnels': {
        target: 'http://teleflow-funnel-service:8005',
        changeOrigin: true,
      },
      '/api/v1/bot': {
        target: 'http://teleflow-bot-gateway:8006',
        changeOrigin: true,
      },
      '/api/v1/userbot': {
        target: 'http://teleflow-userbot-service:8007',
        changeOrigin: true,
      },
      '/api/v1/promotion': {
        target: 'http://teleflow-promotion-service:8008',
        changeOrigin: true,
      },
      '/api/v1/ai': {
        target: 'http://teleflow-ai-service:8009',
        changeOrigin: true,
      },
      '/api/v1/analytics': {
        target: 'http://teleflow-analytics-service:8010',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          charts: ['recharts'],
          forms: ['react-hook-form', '@hookform/resolvers', 'zod'],
        },
      },
    },
  },
})
