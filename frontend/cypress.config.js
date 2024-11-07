import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:8080',
    supportFile: 'tests/e2e/support/index.js'
  },
  component: {
    devServer: {
      framework: 'vue',
      bundler: 'vite'
    }
  }
})