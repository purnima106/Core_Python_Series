from fastmcp import FasrMCP
from app.services.gmail_service import GmailService

gmail = GmailService()

def get_inbox():

    return gmail.list_unread_emails(10)