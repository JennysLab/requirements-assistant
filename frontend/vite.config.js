import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Standard-Vite-Konfiguration mit React-Plugin. Das Frontend laeuft aktuell
// ueberwiegend mit Mock-Daten (siehe src/services/generationService.js).
export default defineConfig({
  plugins: [react()],
});
