import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // যেকোনো IP থেকে অ্যাক্সেসযোগ্য
    port: 5173,
    cors: true,
    strictPort: true,
    allowedHosts: [
      '.ngrok-free.app', // ✅ ngrok এর জন্য allow
      'localhost',
      '127.0.0.1'
    ],
  }
})

