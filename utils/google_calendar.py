import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from dateutil import parser

class GoogleCalendar:
    def __init__(self):
        # Hardcode the scope to eliminate .env issues
        self.scope = "https://www.googleapis.com/auth/calendar"
        print(f"[DEBUG] Using scope: {self.scope}")  # Debug line
        self.creds = self._authenticate()

    def _authenticate(self):
        creds = None
        token_path = "token.json"
        
        if os.path.exists(token_path):
            print("[DEBUG] Loading existing token...")
            creds = Credentials.from_authorized_user_file(token_path, [self.scope])
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("[DEBUG] Refreshing expired token...")
                creds.refresh(Request())
            else:
                print("[DEBUG] Starting OAuth flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", 
                    [self.scope]  # Hardcoded scope
                )
                # Use fixed port (matches Google Cloud redirect URI)
                creds = flow.run_local_server(port=8080, open_browser=True)
            
            # Save/update token
            with open(token_path, "w") as token:
                token.write(creds.to_json())
            print("[DEBUG] Token saved!")
        
        return creds

    def create_event(self, title, start_time, end_time=None, description=""):
        service = build("calendar", "v3", credentials=self.creds)
        
        if not end_time:
            end_time = start_time + timedelta(minutes=30)
        
        event = {
            "summary": title,
            "description": description,
            "start": {"dateTime": start_time.isoformat()},
            "end": {"dateTime": end_time.isoformat()},
        }
        
        event = service.events().insert(calendarId="primary", body=event).execute()
        return f"Event created: {event.get('htmlLink')}"

    def parse_time(self, time_str):
        try:
            return parser.parse(time_str)
        except:
            return None