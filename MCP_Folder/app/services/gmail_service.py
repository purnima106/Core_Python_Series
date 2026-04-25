import os
from loguru import logger
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from dotenv import load_dotenv

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