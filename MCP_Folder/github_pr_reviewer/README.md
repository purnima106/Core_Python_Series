User → Frontend
      ↓
FastAPI (/review)
      ↓
Call Claude API + provide MCP tools
      ↓
Claude:
   - reads prompt
   - decides to call tools
      ↓
MCP tools run:
   - get_pr_metadata
   - get_pr_diff
      ↓
Claude processes results
      ↓
Returns structured review
      ↓
FastAPI → Frontend