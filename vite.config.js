import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const host = process.env.TAURI_DEV_HOST;

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
    //tauri config
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
    // backend api config
    proxy: {
      // Proxy API requests to the backend server
      '/api': {
        target: 'http://127.185.243.18:8085',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    outDir: 'dist',
  },
}
);
