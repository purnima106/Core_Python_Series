# ── Stage 1: Build React app ────────────────────────────────────────────────
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files first (better layer caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the source code
# .env.production is included here — Vite reads it automatically during build
# and bakes VITE_API_URL into the JS bundle
COPY . .

# Build for production (Vite picks up .env.production automatically)
RUN npm run build

# ── Stage 2: Serve with Nginx ───────────────────────────────────────────────
FROM nginx:alpine

# Replace default Nginx config with our custom one.
# Our nginx.conf:
#   - Proxies /api/* → http://backend:8000  (FastAPI container)
#   - Serves index.html for all other routes (React SPA routing)
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
