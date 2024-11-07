import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'url'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', 
    port: 8080,
  },
  preview: {
    host: '0.0.0.0',
    port: 8080
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  css: {
    preprocessorOptions: {
      css: {
        additionalData: `@import "@/assets/styles/main.css";`
      }
    }
  }
})