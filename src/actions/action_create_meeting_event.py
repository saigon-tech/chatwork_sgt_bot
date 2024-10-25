import json
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.actions.action_decorator import Action, ActionRegistry
from src.config import Config
from src.utils.logger import logger
from src.utils.web_utils import WebHelper

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.readonly",
]

@ActionRegistry.register("create_meeting_event", "Create an event in google calendar.")
class CreateMeetingEventAction(Action):
    def execute(self, room_id: str, account_id: str, message: str, web_helper: WebHelper) -> str:
        try:
            event = self._get_data_from_message(message, web_helper)
            self._create_calendar_event(event)
            return "Event registration successful!"
        except Exception as e:
            error_message = f"An error occurred while trying to create event: {str(e)}"
            logger.error(error_message, exc_info=True)
            return "Cannot create google calendar event."

    def _get_data_from_message(self, message, web_helper):
        event = web_helper.query_ai(
            prompt=(
                "Get an json object of google calendar event from the text include eventName, eventDescription, startDatetime, endDatetime: "
                f"{message}"
                f"If not found property, set it null."
               ),
            system_message=(
                "You are a helpful assistant that return google calendar event objects from text."
                "Do not provide additional information or explanation beyond the request."
            ),
            max_tokens=300,
        )
        print(event)
        return event

    def _create_calendar_event(self, event):
        eventObj = json.loads(event)
        service = self._get_calendar_service()
        event = {
            'summary': eventObj['eventName'],
            'description': eventObj['eventDescription'] or "",
            'start': {
                'dateTime': eventObj['startDatetime'],
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
            'end': {
                'dateTime': eventObj['endDatetime'] or eventObj['startDatetime'],
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
        }
        eventResult = service.events().insert(calendarId=self.get_config_value("MEETING_CALENDAR_ID"), body=event).execute()

    def _get_calendar_service(self):
        credentials = Credentials.from_service_account_info({
            "type": "service_account",
            "project_id": self.get_config_value("PROJECT_ID"),
            "private_key_id": self.get_config_value("PRIVATE_KEY_ID"),
            "private_key": self.get_config_value("PRIVATE_KEY"),
            "client_email": self.get_config_value("CLIENT_EMAIL"),
            "client_id": self.get_config_value("CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": self.get_config_value("CLIENT_X509_CERT_URL"),
            "universe_domain": "googleapis.com",
        })

        return build('calendar', 'v3', credentials=credentials)
