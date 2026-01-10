import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const backendHost = env.VITE_BACKEND_HOST || 'localhost'
  const backendPort = env.VITE_BACKEND_PORT || '8000'
  const target = env.VITE_API_URL || `http://${backendHost}:${backendPort}`

  return {
    plugins: [vue()],
    server: 
    {
      port: 5173,
      host: '0.0.0.0',
      proxy: {
        '/api': {
          target,
          changeOrigin: true,
        }
      }
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
  }
})
