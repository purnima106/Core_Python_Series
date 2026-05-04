* Folder Structure

smart-gmail-mcp/
│
├── app/
│   ├── __init__.py
│   │
│   ├── main.py              # MCP server entrypoint
│   ├── config.py            # env + settings
│   ├── logger.py            # logging setup
│   │
│   ├── tools/               # MCP tools (core logic exposed to AI)
│   │   ├── __init__.py
│   │   ├── read.py          # list_unread_emails, get_email_body
│   │   ├── write.py         # send_email, draft_reply, label_email
│   │   └── search.py        # search_emails
│   │
│   ├── resources/           # MCP resources
│   │   ├── __init__.py
│   │   └── gmail.py         # inbox + thread resources
│   │
│   ├── services/            # external integrations
│   │   ├── __init__.py
│   │   └── gmail_service.py # Gmail API wrapper
│   │
│   ├── schemas/             # request/response validation
│   │   ├── __init__.py
│   │   └── email.py
│   │
│   └── prompts/             # reusable prompts
│       ├── __init__.py
│       └── triage.py
│
├── tests/                   # basic tests (optional but good)
│
├── .env                     # secrets (not committed)
├── .env.example             # sample env
├── pyproject.toml           # dependencies (uv)
├── README.md
└── claude_desktop_config.json

🧠 Why this structure? (important)
🔧 tools/

👉 AI that actually calls

Example:
list_unread_emails
send_email
🔌 services/

👉 Actual Gmail logic 

API calls
OAuth handling
👉 Tools = interface
👉 Services = implementation

📂 resources/
👉 Live data exposure
inbox
threads

🧾 schemas/
👉 Input validation
wrong data → crash avoid

🧠 prompts/
👉 reusable AI instructions
triage logic

⚙️ main.py
👉 MCP server starts from here

🔥 4. Clean Architecture (easy understanding)
Claude (AI)
   ↓
TOOLS (what AI calls)
   ↓
SERVICES (actual Gmail logic)
   ↓
Gmail API