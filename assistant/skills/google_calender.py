import os.path
from datetime import datetime, timedelta, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pprint

from assistant.skills.decorator import skill

# If modifying these SCOPES, delete the token.json file
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds = None

    # Load existing credentials from token.json
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials available, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\Asus\Desktop\deskora\credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for next run
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    return creds

@skill
def create_google_calendar_event(summary: str, description: str = "", minutes_from_now: int = 5):
    """
    Add a reminder to the user's Google Calendar.

    Arguments (in this order):
        summary (str): A short title for the reminder.
        description (str, optional): A longer description for the reminder.
        minutes_from_now (int, optional): When the reminder should happen, in minutes from now. Default is 5 minutes.

    Example:
        create_google_calendar_event("Meeting with Bob", "Discuss the project", 15)
    """
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    start_time = datetime.now(timezone.utc) + timedelta(minutes=minutes_from_now)
    end_time = start_time + timedelta(minutes=30)  # Default 30 min duration

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat() ,
            'timeZone': 'UTC',
        },
    }

    pprint.pprint(event) #DEBUG statement for payload sent to api

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"✅ Reminder added to Google Calendar: {event.get('htmlLink')}")
