import os
from loguru import logger
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import base64
from email.mime.text import MIMEText

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


class GmailService:
    def __init__(self):
        self.creds = self.authenticate()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def authenticate(self):
        creds = None
        token_path = os.getenv("TOKEN_PATH", "token.json")
        credentials_path = os.getenv("GOOGLE_CREDENTIALS", "credentials.json")

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                logger.info("Running OAuth Flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return creds

    def list_unread_emails(self, max_results=5):
        results = (
            self.service.users()
            .messages()
            .list(userId="me", labelIds=["UNREAD"], maxResults=max_results)
            .execute()
        )

        messages = results.get("messages", [])
        return messages

    def send_email(self, to: str, subject: str, body: str):
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        send_message = (
            self.service.users()
            .messages()
            .send(userId="me", body={"raw": raw_message})
            .execute()
        )

        return {"status": "sent", "id": send_message["id"]}

    def label_email(self, message_id: str, label_ids: list):
        self.service.users().messages().modify(
            userId="me",
            id=message_id,
            body={"addLabelIds": label_ids}
        ).execute()

        return {"status": "labeled"}

    def draft_reply(self, to: str, subject: str, body: str):
        return {
            "to": to,
            "subject": subject,
            "body": body,
            "status": "draft"
        }