import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0", // Permitir acesso de outras máquinas
    port: 5173,
  },
  define: {
    "process.env": {},
  },
});
