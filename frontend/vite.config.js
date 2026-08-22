import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { visualizer } from "rollup-plugin-visualizer";

export default defineConfig({
  plugins: [
    react(),
    visualizer({
      filename: "bundle-report.html",
      open: false,
      gzipSize: true,
      brotliSize: true,
    }),
  ],
  resolve: {
    dedupe: ["react", "react-dom"],
  },
  optimizeDeps: {
    include: ["react", "react-dom", "react-router-dom", "zustand", "framer-motion", "lucide-react"],
  },
  server: {
    port: 5173,
    host: true,
    strictPort: true,
    allowedHosts: true,
    warmup: {
      clientFiles: ["./src/App.tsx", "./src/main.tsx", "./src/pages/lazy.ts", "./src/components/Navbar.tsx"],
    },
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        ws: true,
      },
      "/ws": {
        target: "ws://127.0.0.1:8000",
        ws: true,
        changeOrigin: true,
      },
    },
  },
  build: {
    target: "es2020",
    cssMinify: "esbuild",
    rollupOptions: {
      output: {
        manualChunks: {
          "react-vendor": ["react", "react-dom", "react-router-dom", "zustand"],
          "framer-motion": ["framer-motion"],
          "monaco-editor": ["@monaco-editor/react"],
        },
      },
    },
    assetsInlineLimit: 4096,
    assetsInclude: ["**/*.webp", "**/*.svg"],
  },
});
