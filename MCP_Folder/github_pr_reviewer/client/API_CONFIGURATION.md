# API Configuration Guide

## Overview

The frontend uses Vite environment variables to configure the backend API URL.
All API calls are centralized in `src/api.js` — **no component may call `fetch` directly**.

---

## Environment Files

| File | When Used | Value |
|------|-----------|-------|
| `.env` | Local Vite dev (`npm run dev`) | `VITE_API_URL=http://localhost:8000` |
| `.env.production` | Docker build (`npm run build`) | `VITE_API_URL=http://backend:8000` |

> **Important:** Vite bakes `VITE_API_URL` into the JS bundle at **build time**.
> The variable must start with `VITE_` and is accessed via `import.meta.env.VITE_API_URL` — **never** `process.env`.

---

## How It Works per Environment

### Local Dev (`npm run dev`)

```
Browser → Vite dev server (port 5173) → fetch("http://localhost:8000/api/review")
                                               ↑
                                  VITE_API_URL from .env
```

The browser talks directly to FastAPI running on port 8000.

### Docker / Nginx (production build)

```
Browser → Nginx (port 80) → /api/* is proxied → FastAPI backend (port 8000)
                 ↑                                      ↑
         serves React SPA                  Docker service name "backend"
                                           (nginx.conf proxy_pass)
```

`VITE_API_URL=http://backend:8000` is baked in at Docker build time. Nginx (via `nginx.conf`) proxies
`/api/*` to the backend container so the browser's request never needs to resolve `backend` itself.

> **Why not call `http://backend:8000` directly from the browser?**
> `backend` is a Docker-internal hostname — only containers on the same Docker network can resolve it.
> The **Nginx proxy in `nginx.conf`** is what bridges the browser to the backend.

---

## File Structure

```
client/
├── .env                  ← Local dev URL (git-ignored)
├── .env.example          ← Template (committed)
├── .env.production       ← Docker build URL (committed)
├── nginx.conf            ← Nginx proxy config (copied into Docker image)
├── Dockerfile            ← Multi-stage build: Node → Nginx
├── vite.config.js        ← No /api proxy needed (uses absolute BASE_URL)
└── src/
    ├── api.js            ← ★ SINGLE source of all API calls
    └── App.jsx           ← Uses apiCall(API.reviewPR, ...) from api.js
```

---

## `src/api.js` — Centralized API Layer

```js
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

console.log("Using API URL:", BASE_URL)   // ← debug log (remove once confirmed)

// Named function (recommended for components)
export const reviewPR = async (data) => {
  return fetch(`${BASE_URL}/api/review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
}

// Endpoint constants
export const API = {
  reviewPR: `${BASE_URL}/api/review`,
}

// Generic helper with error handling
export async function apiCall(url, options = {}) { ... }
```

### Usage in components

```js
// ✅ CORRECT — uses api.js
import { API, apiCall } from './api'
const data = await apiCall(API.reviewPR, { method: 'POST', body: JSON.stringify({...}) })

// ✅ Also correct — named function
import { reviewPR } from './api'
const res = await reviewPR({ pr_url: url })

// ❌ WRONG — never do this in a component
fetch('/api/review', ...)                      // relative URL → hits Nginx, not backend
fetch('http://localhost:8000/api/review', ...) // hardcoded, breaks in Docker
```

---

## Adding New Endpoints

1. **Add to `src/api.js`:**
   ```js
   export const API = {
     reviewPR: `${BASE_URL}/api/review`,
     health:   `${BASE_URL}/api/health`,   // ← new
   }

   export const checkHealth = async () => fetch(`${BASE_URL}/api/health`)
   ```

2. **Use in component:**
   ```js
   import { API, apiCall } from './api'
   const status = await apiCall(API.health)
   ```

---

## Troubleshooting

### `"Unexpected token '<'"` / Nginx returning HTML instead of JSON

**Cause:** `/api/...` request hitting Nginx without a proxy rule → Nginx returns its 404 page (HTML).

**Fix checklist:**
- ✅ `nginx.conf` is copied into the Docker image (`COPY nginx.conf /etc/nginx/conf.d/default.conf`)
- ✅ `nginx.conf` has `location /api/ { proxy_pass http://backend:8000; }`
- ✅ Docker Compose service is named exactly `backend`
- ✅ Frontend is NOT calling a relative `/api/...` URL — it must use `${BASE_URL}/api/...`

### `BASE_URL` is `undefined` in the browser console

**Cause:** `VITE_API_URL` was not set when `npm run build` ran.

**Fix:**
- Confirm `.env.production` exists and contains `VITE_API_URL=http://backend:8000`
- Rebuild the Docker image: `docker build --no-cache -t pr-frontend .`

### CORS errors

The backend FastAPI app needs:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Docker Compose Reference

```yaml
services:
  backend:
    build: .
    ports:
      - "8000:8000"

  frontend:
    build: ./client
    ports:
      - "80:80"
    depends_on:
      - backend
```

> The frontend service name must match whatever is in `nginx.conf`'s `proxy_pass` directive.
> If you rename the backend service, update `nginx.conf` accordingly.
