from app.services.gmail_service import GmailService

gmail = GmailService()
emails = gmail.list_unread_emails()

print(emails)