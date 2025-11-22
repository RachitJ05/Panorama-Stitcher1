import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/stitch': 'http://localhost:5000',
      '/download': 'http://localhost:5000'
    }
  }
})
