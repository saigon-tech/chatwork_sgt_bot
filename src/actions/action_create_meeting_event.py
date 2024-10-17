from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.actions.action_decorator import Action, ActionRegistry
from src.config import Config
from src.utils.web_utils import WebHelper

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.readonly",
]

@ActionRegistry.register("create_meeting_event", "Create an event in google calendar.")
class CreateMeetingEventAction(Action):
    def execute(self, room_id: str, account_id: str, message: str, web_helper: WebHelper) -> str:
        try:
            event = _get_data_from_message(self, message)
            _create_calendar_event(self, event)
            return "Success."
        except Exception as e:
            error_message = f"An error occurred while trying to create event: {str(e)}"
            logger.error(error_message, exc_info=True)
            return "Cannot create google calendar event."

    def _get_data_from_message(self, message):
        event = web_helper.query_ai(
            prompt=(
                "Get an object of google calendar event from the text include eventName, eventDescription, startDatetime, endDatetime: "
                f"{message}"
                f"If not found property, set it null."
               ),
            system_message=(
                "You are a helpful assistant that return google calendar event objects from text."
                "Do not provide additional information or explanation beyond the request."
            ),
            max_tokens=300,
        )
        return event

    def _create_calendar_event(self, event):
        service = _get_calendar_service()
        event = {
            'summary': event.eventName,
            'description': event.eventDescription or "",
            'start': {
                'dateTime': event.startDatetime,
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
            'end': {
                'dateTime': event.endDatetime or event.startDatetime,
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
        }
        API_URL = self.get_config_value("API_URL")
        eventResult = service.events().insert(calendarId=Config.MEETING_CALENDAR_ID, body=event).execute()

    def _get_calendar_service():
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        service = build("calendar", "v3", credentials=creds)
        return service
