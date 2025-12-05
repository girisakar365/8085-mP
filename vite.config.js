import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const host = process.env.TAURI_DEV_HOST;

// Backend configuration
const BACKEND_HOST = process.env.BACKEND_HOST || "127.0.0.1";
const BACKEND_PORT = process.env.BACKEND_PORT || "8085";
const BACKEND_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`;

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react({
      // Enable automatic JSX runtime (no need to import React)
      jsxRuntime: 'automatic',
    }),
  ],

  // 1. prevent Vite from obscuring rust errors
  clearScreen: false,

  server: {
    // Tauri config
    port: 4916,
    strictPort: true,
    host: '127.185.243.17',
    hmr: host
      ? {
          protocol: "ws",
          host: '127.185.243.17',
          port: 4918,
        }
      : undefined,
    watch: {
      // tell Vite to ignore watching `src-tauri`
      ignored: ["**/src-tauri/**"],
    },
    // Backend API proxy config
    proxy: {
      '/api': {
        target: BACKEND_URL,
        changeOrigin: true,
        secure: false,
        // Handle connection errors gracefully
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.error('Proxy error:', err.message);
          });
        },
      },
      '/health': {
        target: BACKEND_URL,
        changeOrigin: true,
        secure: false,
      },
      '/config': {
        target: BACKEND_URL,
        changeOrigin: true,
        secure: false,
      },
    },
  },
  
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'esbuild',
  },

  // Define environment variables accessible in the app
  define: {
    __BACKEND_URL__: JSON.stringify(BACKEND_URL),
  },
});
