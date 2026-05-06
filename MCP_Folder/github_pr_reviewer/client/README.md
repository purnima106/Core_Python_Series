# GitHub PR Reviewer - Frontend 🎨

A modern, responsive React interface for submitting GitHub Pull Requests for AI analysis and viewing the results.

## 🛠️ Tech Stack
- **React 19**: Using the latest features for UI components.
- **Vite**: Ultra-fast build tool and development server.
- **Vanilla CSS**: Custom-styled components with a premium aesthetic.
- **Environment Based Config**: Centralized API management.

## ⚙️ Setup & Installation

### Local Development
1. **Install dependencies**:
   ```bash
   npm install
   ```
2. **Configure Environment Variables**:
   Create a `.env` file in the `client` directory:
   ```env
   VITE_API_URL=http://localhost:8000
   ```
3. **Run the development server**:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`.

## 📦 Build & Production
To build the application for production:
```bash
npm run build
```
The output will be in the `dist/` directory. In the Docker setup, these files are served by **Nginx**.

## 🧩 Key Components

### `App.jsx`
The main entry point that handles form submission, loading states, and rendering the review results. It utilizes a structured display for the AI's JSON response, categorizing feedback into Summary, Risk, Issues, and Suggestions.

### `api.js`
A centralized module for all API interactions. It ensures that the correct backend URL is used regardless of the environment (Local, Docker, or Production).

## 🌍 Environment Variables
- `VITE_API_URL`: The base URL of the FastAPI backend.
  - Development: `http://localhost:8000`
  - Production (Docker): `http://backend:8000` (internal network)

---

