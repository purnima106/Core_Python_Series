from fastmcp import FasrMCP
from app.services.gmail_service import GmailService

Gmail = GmailService()

def get_inbox():

    return Gmail.list_unread_emails(10)