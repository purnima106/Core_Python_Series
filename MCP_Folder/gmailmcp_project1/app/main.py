from app.prompts.triage import TRIAGE_PROMPT
from fastmcp import FastMCP
from app.services.gmail_service import GmailService

mcp = FastMCP("gmail-mcp-server")

gmail = GmailService()

@mcp.tool()
def list_unread_emails(max_results: int = 5):
    """"Get unread emails from Gmail inbox."""
    emails = gmail.list_unread_emails(max_results)
    return emails   

@mcp.tool()
def send_email(to: str, subject: str, body: str):
    """
    Send an email via Gmail (use carefully)
    """
    return gmail.send_email(to, subject, body)



@mcp.tool()
def label_email(message_id: str, label_ids: list):
    """
    Add labels to an email
    """
    return gmail.label_email(message_id, label_ids)

@mcp.tool()
def draft_reply(to: str, subject: str, body: str):
    """
    Draft an email reply (safe, does not send)
    """
    return gmail.draft_reply(to, subject, body)

@mcp.resource("gmail://inbox")
def inbox_resource():
    """Get current inbox emails."""
    return gmail.list_unread_emails(10)

@mcp.prompt()
def triage_inbox():
    return TRIAGE_PROMPT

if __name__ == "__main__":
    mcp.run()


