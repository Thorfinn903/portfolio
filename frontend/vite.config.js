import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    chunkSizeWarningLimit: 1600,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules/react/') || id.includes('node_modules/react-dom/') || id.includes('node_modules/react-router-dom/')) {
            return 'vendor'
          }
          if (id.includes('node_modules/framer-motion/')) {
            return 'animations'
          }
          if (id.includes('node_modules/recharts/')) {
            return 'charts'
          }
          if (
            id.includes('node_modules/lucide-react/') ||
            id.includes('node_modules/clsx/') ||
            id.includes('node_modules/tailwind-merge/')
          ) {
            return 'ui'
          }
          return undefined
        },
      },
    },
  },
})
