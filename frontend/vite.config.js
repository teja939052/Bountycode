import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  resolve: {
    dedupe: ["react", "react-dom"],
  },
  optimizeDeps: {
    include: ["react", "react-dom", "react-router-dom", "zustand"],
  },
  server: {
    port: 5173,
    host: true,
    strictPort: true,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          "framer-motion": ["framer-motion"],
          "gsap": ["gsap"],
          "monaco-editor": ["@monaco-editor/react"],
        },
      },
    },
    assetsInlineLimit: 0,
    assetsInclude: ["**/*.webp", "**/*.svg"],
  },
});
