import { defineConfig } from "vite";

export default defineConfig({
  build: {
    lib: {
      entry: {
        quill: "./src/editors/quill/index.js",
      },
      name: "wagtail_forum",
      formats: ["iife"],
      fileName: () => "js/quill.js",
    },
    outDir: "../wagtail_forum/static/wagtail_forum",
    rollupOptions: {
      output: {
        assetFileNames: () => {
          return `[ext]/[name].[ext]`;
        },
      },
    },
  },
});
