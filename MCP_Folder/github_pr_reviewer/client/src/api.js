/**
 * API Configuration Module
 *
 * Centralized API endpoint management with environment-based configuration.
 * This ensures all API calls use the correct backend URL in ALL environments:
 *
 *   Local Dev (Vite):  VITE_API_URL=http://localhost:8000  (set in .env)
 *   Docker (Nginx):    VITE_API_URL=http://backend:8000    (set in .env.production)
 *   EC2/Remote:        VITE_API_URL=http://<ec2-ip>:8000
 *   Production:        VITE_API_URL=https://api.yourdomain.com
 *
 * IMPORTANT:
 *  - Always use import.meta.env.VITE_API_URL — NEVER process.env
 *  - All fetch/API calls MUST go through this module
 *  - Components must NEVER call fetch("/api/...") directly
 */

// ─── Base URL ────────────────────────────────────────────────────────────────
// Reads from Vite env variables (set in .env / .env.production)
// Falls back to localhost:8000 so local dev still works even without a .env
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Debug log — shows which backend URL is active at runtime
// Remove (or guard with import.meta.env.DEV) once confirmed working
console.log("Using API URL:", BASE_URL)

// ─── Named Endpoint Constants ─────────────────────────────────────────────────
export const API = {
  reviewPR: `${BASE_URL}/api/review`,

  // Add more endpoints here as needed:
  // health: `${BASE_URL}/api/health`,
  // status: `${BASE_URL}/api/status`,
}

// ─── Named API Functions (preferred usage in components) ──────────────────────

/**
 * Submit a GitHub PR URL for AI review.
 * @param {{ pr_url: string }} data
 * @returns {Promise<Response>} Raw fetch Response
 */
export const reviewPR = async (data) => {
  return fetch(`${BASE_URL}/api/review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
}

// ─── Generic API Helper ───────────────────────────────────────────────────────

/**
 * Make an API request with consistent error handling and JSON parsing.
 * @param {string} url      - Full API endpoint URL (use API.* constants above)
 * @param {object} options  - Standard fetch options (method, body, headers…)
 * @returns {Promise<object>} Parsed JSON response
 * @throws {Error} If response is not ok or JSON parsing fails
 */
export async function apiCall(url, options = {}) {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || `HTTP ${response.status}: ${response.statusText}`)
    }

    return data
  } catch (error) {
    console.error(`API Error [${url}]:`, error.message)
    throw error
  }
}
