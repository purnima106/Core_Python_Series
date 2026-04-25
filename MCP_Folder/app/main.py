from fastmcp import FastMCP
from app.services.gmail_service import GmailService

mcp = FastMCP("gmail-mcp-server")

gmail = GmailService()

@mcp.tool()
def list_unread_emails(max_results: int = 5):
    """"Get unread emails from Gmail inbox."""
    emails = gmail.list_unread_emails(max_results)
    return emails   

if __name__ == "__main__":
    mcp.run()

