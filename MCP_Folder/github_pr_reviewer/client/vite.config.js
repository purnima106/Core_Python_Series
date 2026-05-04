import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // NOTE: No /api proxy needed here.
    //
    // All API calls now use the absolute BASE_URL from import.meta.env.VITE_API_URL
    // (defined in .env for local dev, .env.production for Docker builds).
    //
    // .env              → VITE_API_URL=http://localhost:8000   (local Vite dev)
    // .env.production   → VITE_API_URL=http://backend:8000     (Docker / Nginx build)
    //
    // This means the frontend ALWAYS calls the backend directly via BASE_URL,
    // never via a relative /api/... path that would hit the Nginx container itself.
  }
})
