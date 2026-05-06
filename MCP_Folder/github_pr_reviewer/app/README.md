# GitHub PR Reviewer - Backend 🚀

The backend for the GitHub PR Reviewer is a FastAPI application that serves as the orchestration layer between the frontend, the Groq LLM, and the GitHub API.

## 🛠️ Tech Stack
- **FastAPI**: Modern, fast web framework for building APIs.
- **Groq SDK**: Interface for interacting with Llama 3 models on Groq's high-speed infrastructure.
- **FastMCP**: Implementation of the Model Context Protocol for tool management.
- **httpx**: Async HTTP client for calling GitHub's API.
- **Pydantic**: Data validation and settings management.

## ⚙️ Setup & Installation

### Local Development
1. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key
   GITHUB_TOKEN=your_github_personal_access_token
   ```
4. **Run the server**:
   ```bash
   python -m app.main
   ```
   The API will be available at `http://localhost:8000`.

## 🧬 Architecture Details

### Agentic Loop (`app/mcp/tools/analyze.py`)
The core logic resides in an agentic loop. Instead of a single prompt, the system:
1. Sends the PR URL and available tools to the LLM.
2. The LLM decides which tools to call (e.g., `get_pr_diff`).
3. The backend executes the tool and sends the result back to the LLM.
4. This continues until the LLM provides the final structured JSON review.

### MCP Tools
Tools are defined using `FastMCP`. Currently implemented:
- `get_pr_diff(pr_url)`: Fetches the raw diff from GitHub using the `GitHubService`.

## 📡 API Endpoints

### `POST /api/review`
Submits a PR for analysis.
- **Request Body**:
  ```json
  {
    "pr_url": "https://github.com/owner/repo/pull/123"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "review": {
      "summary": "...",
      "risk": "low",
      "issues": [],
      "suggestions": []
    }
  }
  ```

---
