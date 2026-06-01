# LinkedIn Autoposter System 🤖✍️

An automated LinkedIn content generation and staging system. This application uses Groq's high-performance **Llama 3.3 70B** model (via the official `groq` SDK) to draft high-quality technical posts on DevOps, Platform Engineering, Observability, and cloud topics, staging them in a local SQLite database for approval or posting.

## 🚀 Features

- **Automated Generation**: Automatically drafts high-quality professional posts based on a curated topics catalog.
- **SQLite Database Staging**: Saves generated drafts in a structured SQLite database using SQLAlchemy ORM.
- **High-Performance LLM**: Uses Groq's `llama-3.3-70b-versatile` model for lightning-fast, high-quality generation.
- **Environment Isolation**: Supports virtual environments and secures API keys using `.env` configurations.

---

## 🛠️ Tech Stack

- **Core Language**: Python 3
- **ORM & Database**: SQLAlchemy (SQLite)
- **AI Integration**: `groq` (using `llama-3.3-70b-versatile`)
- **Environment Management**: `python-dotenv`

---

## 📂 Project Structure

```
├── main.py            # CLI / Orchestrator entrypoint
├── generator.py       # Groq API client & copywriter 
├── database.py        # SQLAlchemy database models & session setup
├── topics.py          # Catalog of DevOps & SRE topics
├── .env               # Environment secret keys (ignored by git)
├── .gitignore         # Prevents tracking virtual envs & secrets
├── requirements.txt   # Declared Python dependencies
└── posts.db           # Local SQLite database (auto-generated)
```

---

## 🔧 Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.10+ installed globally.

### 2. Configure Virtual Environment
If you don't have a virtual environment set up, run:
```bash
python -m venv .venv
```

Activate the environment:
* **Windows (PowerShell)**:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
* **macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a file named `.env` in the root directory (or update the existing one):
```env
# Groq API Key from Groq Console (https://console.groq.com/)
GROQ_API_KEY=your_actual_groq_api_key_here
```

---

## 📝 Database Schema

The database `posts.db` contains a single `posts` table managed by `database.py`:

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer (PK)` | Auto-incrementing post ID |
| `topic` | `String` | Selected post category |
| `post_text` | `Text` | The actual copy drafted by Llama |
| `status` | `String` | Status of the post (e.g. `'generated'`, `'posted'`) |

---

## 🏃 Running the Application

To run the generator and stage a new post draft:
```bash
python main.py
```

The script will automatically:
1. Select a random topic from `topics.py`.
2. Connect to the Groq Cloud API.
3. Draft a tailored LinkedIn post.
4. Save the record into `posts.db`.
5. Print the selected topic and generated copy to the console.
