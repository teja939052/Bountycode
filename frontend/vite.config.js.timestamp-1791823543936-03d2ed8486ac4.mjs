// vite.config.js
import { defineConfig } from "file:///D:/Project-Fremen/frontend/node_modules/vite/dist/node/index.js";
import react from "file:///D:/Project-Fremen/frontend/node_modules/@vitejs/plugin-react/dist/index.js";
import { visualizer } from "file:///D:/Project-Fremen/frontend/node_modules/rollup-plugin-visualizer/dist/plugin/index.js";
var vite_config_default = defineConfig({
  plugins: [
    react(),
    visualizer({
      filename: "bundle-report.html",
      open: false,
      gzipSize: true,
      brotliSize: true
    })
  ],
  resolve: {
    dedupe: ["react", "react-dom"]
  },
  optimizeDeps: {
    include: ["react", "react-dom", "react-router-dom", "zustand", "framer-motion", "lucide-react"]
  },
  server: {
    port: 5173,
    host: true,
    strictPort: true,
    allowedHosts: true,
    warmup: {
      clientFiles: ["./src/App.tsx", "./src/main.tsx", "./src/pages/lazy.ts", "./src/components/Navbar.tsx"]
    },
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        ws: true
      },
      "/ws": {
        target: "ws://127.0.0.1:8000",
        ws: true,
        changeOrigin: true
      }
    }
  },
  build: {
    target: "es2020",
    cssMinify: "esbuild",
    rollupOptions: {
      output: {
        manualChunks: {
          "react-vendor": ["react", "react-dom", "react-router-dom", "zustand"],
          "framer-motion": ["framer-motion"],
          "monaco-editor": ["@monaco-editor/react"]
        }
      }
    },
    assetsInlineLimit: 4096,
    assetsInclude: ["**/*.webp", "**/*.svg"]
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJEOlxcXFxQcm9qZWN0LUZyZW1lblxcXFxmcm9udGVuZFwiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9maWxlbmFtZSA9IFwiRDpcXFxcUHJvamVjdC1GcmVtZW5cXFxcZnJvbnRlbmRcXFxcdml0ZS5jb25maWcuanNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfaW1wb3J0X21ldGFfdXJsID0gXCJmaWxlOi8vL0Q6L1Byb2plY3QtRnJlbWVuL2Zyb250ZW5kL3ZpdGUuY29uZmlnLmpzXCI7aW1wb3J0IHsgZGVmaW5lQ29uZmlnIH0gZnJvbSBcInZpdGVcIjtcbmltcG9ydCByZWFjdCBmcm9tIFwiQHZpdGVqcy9wbHVnaW4tcmVhY3RcIjtcbmltcG9ydCB7IHZpc3VhbGl6ZXIgfSBmcm9tIFwicm9sbHVwLXBsdWdpbi12aXN1YWxpemVyXCI7XG5cbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyh7XG4gIHBsdWdpbnM6IFtcbiAgICByZWFjdCgpLFxuICAgIHZpc3VhbGl6ZXIoe1xuICAgICAgZmlsZW5hbWU6IFwiYnVuZGxlLXJlcG9ydC5odG1sXCIsXG4gICAgICBvcGVuOiBmYWxzZSxcbiAgICAgIGd6aXBTaXplOiB0cnVlLFxuICAgICAgYnJvdGxpU2l6ZTogdHJ1ZSxcbiAgICB9KSxcbiAgXSxcbiAgcmVzb2x2ZToge1xuICAgIGRlZHVwZTogW1wicmVhY3RcIiwgXCJyZWFjdC1kb21cIl0sXG4gIH0sXG4gIG9wdGltaXplRGVwczoge1xuICAgIGluY2x1ZGU6IFtcInJlYWN0XCIsIFwicmVhY3QtZG9tXCIsIFwicmVhY3Qtcm91dGVyLWRvbVwiLCBcInp1c3RhbmRcIiwgXCJmcmFtZXItbW90aW9uXCIsIFwibHVjaWRlLXJlYWN0XCJdLFxuICB9LFxuICBzZXJ2ZXI6IHtcbiAgICBwb3J0OiA1MTczLFxuICAgIGhvc3Q6IHRydWUsXG4gICAgc3RyaWN0UG9ydDogdHJ1ZSxcbiAgICBhbGxvd2VkSG9zdHM6IHRydWUsXG4gICAgd2FybXVwOiB7XG4gICAgICBjbGllbnRGaWxlczogW1wiLi9zcmMvQXBwLnRzeFwiLCBcIi4vc3JjL21haW4udHN4XCIsIFwiLi9zcmMvcGFnZXMvbGF6eS50c1wiLCBcIi4vc3JjL2NvbXBvbmVudHMvTmF2YmFyLnRzeFwiXSxcbiAgICB9LFxuICAgIHByb3h5OiB7XG4gICAgICBcIi9hcGlcIjoge1xuICAgICAgICB0YXJnZXQ6IFwiaHR0cDovLzEyNy4wLjAuMTo4MDAwXCIsXG4gICAgICAgIGNoYW5nZU9yaWdpbjogdHJ1ZSxcbiAgICAgICAgd3M6IHRydWUsXG4gICAgICB9LFxuICAgICAgXCIvd3NcIjoge1xuICAgICAgICB0YXJnZXQ6IFwid3M6Ly8xMjcuMC4wLjE6ODAwMFwiLFxuICAgICAgICB3czogdHJ1ZSxcbiAgICAgICAgY2hhbmdlT3JpZ2luOiB0cnVlLFxuICAgICAgfSxcbiAgICB9LFxuICB9LFxuICBidWlsZDoge1xuICAgIHRhcmdldDogXCJlczIwMjBcIixcbiAgICBjc3NNaW5pZnk6IFwiZXNidWlsZFwiLFxuICAgIHJvbGx1cE9wdGlvbnM6IHtcbiAgICAgIG91dHB1dDoge1xuICAgICAgICBtYW51YWxDaHVua3M6IHtcbiAgICAgICAgICBcInJlYWN0LXZlbmRvclwiOiBbXCJyZWFjdFwiLCBcInJlYWN0LWRvbVwiLCBcInJlYWN0LXJvdXRlci1kb21cIiwgXCJ6dXN0YW5kXCJdLFxuICAgICAgICAgIFwiZnJhbWVyLW1vdGlvblwiOiBbXCJmcmFtZXItbW90aW9uXCJdLFxuICAgICAgICAgIFwibW9uYWNvLWVkaXRvclwiOiBbXCJAbW9uYWNvLWVkaXRvci9yZWFjdFwiXSxcbiAgICAgICAgfSxcbiAgICAgIH0sXG4gICAgfSxcbiAgICBhc3NldHNJbmxpbmVMaW1pdDogNDA5NixcbiAgICBhc3NldHNJbmNsdWRlOiBbXCIqKi8qLndlYnBcIiwgXCIqKi8qLnN2Z1wiXSxcbiAgfSxcbn0pO1xuIl0sCiAgIm1hcHBpbmdzIjogIjtBQUFzUSxTQUFTLG9CQUFvQjtBQUNuUyxPQUFPLFdBQVc7QUFDbEIsU0FBUyxrQkFBa0I7QUFFM0IsSUFBTyxzQkFBUSxhQUFhO0FBQUEsRUFDMUIsU0FBUztBQUFBLElBQ1AsTUFBTTtBQUFBLElBQ04sV0FBVztBQUFBLE1BQ1QsVUFBVTtBQUFBLE1BQ1YsTUFBTTtBQUFBLE1BQ04sVUFBVTtBQUFBLE1BQ1YsWUFBWTtBQUFBLElBQ2QsQ0FBQztBQUFBLEVBQ0g7QUFBQSxFQUNBLFNBQVM7QUFBQSxJQUNQLFFBQVEsQ0FBQyxTQUFTLFdBQVc7QUFBQSxFQUMvQjtBQUFBLEVBQ0EsY0FBYztBQUFBLElBQ1osU0FBUyxDQUFDLFNBQVMsYUFBYSxvQkFBb0IsV0FBVyxpQkFBaUIsY0FBYztBQUFBLEVBQ2hHO0FBQUEsRUFDQSxRQUFRO0FBQUEsSUFDTixNQUFNO0FBQUEsSUFDTixNQUFNO0FBQUEsSUFDTixZQUFZO0FBQUEsSUFDWixjQUFjO0FBQUEsSUFDZCxRQUFRO0FBQUEsTUFDTixhQUFhLENBQUMsaUJBQWlCLGtCQUFrQix1QkFBdUIsNkJBQTZCO0FBQUEsSUFDdkc7QUFBQSxJQUNBLE9BQU87QUFBQSxNQUNMLFFBQVE7QUFBQSxRQUNOLFFBQVE7QUFBQSxRQUNSLGNBQWM7QUFBQSxRQUNkLElBQUk7QUFBQSxNQUNOO0FBQUEsTUFDQSxPQUFPO0FBQUEsUUFDTCxRQUFRO0FBQUEsUUFDUixJQUFJO0FBQUEsUUFDSixjQUFjO0FBQUEsTUFDaEI7QUFBQSxJQUNGO0FBQUEsRUFDRjtBQUFBLEVBQ0EsT0FBTztBQUFBLElBQ0wsUUFBUTtBQUFBLElBQ1IsV0FBVztBQUFBLElBQ1gsZUFBZTtBQUFBLE1BQ2IsUUFBUTtBQUFBLFFBQ04sY0FBYztBQUFBLFVBQ1osZ0JBQWdCLENBQUMsU0FBUyxhQUFhLG9CQUFvQixTQUFTO0FBQUEsVUFDcEUsaUJBQWlCLENBQUMsZUFBZTtBQUFBLFVBQ2pDLGlCQUFpQixDQUFDLHNCQUFzQjtBQUFBLFFBQzFDO0FBQUEsTUFDRjtBQUFBLElBQ0Y7QUFBQSxJQUNBLG1CQUFtQjtBQUFBLElBQ25CLGVBQWUsQ0FBQyxhQUFhLFVBQVU7QUFBQSxFQUN6QztBQUNGLENBQUM7IiwKICAibmFtZXMiOiBbXQp9Cg==
