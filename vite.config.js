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
    port: 1420,
    strictPort: true,
    host: host || false,
    hmr: host
      ? {
          protocol: "ws",
          host,
          port: 1421,
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
        target: 'http://127.0.0.1:3221',
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
