import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import Components from 'unplugin-vue-components/vite';
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers';
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [
        AntDesignVueResolver({
          importStyle: false, // css in js
        }),],
    }),
  ],
  css: {
    preprocessorOptions: {
      less: {
      }
    }
  },

  build: {
    rollupOptions: {

      // external: ['axios'],
    },
  },

  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    }
  }
})
