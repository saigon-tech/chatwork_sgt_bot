import requests
from src.config import Config
from celery import shared_task


@shared_task
def send_message_to_room(room_id, message):
    url = f"https://api.chatwork.com/v2/rooms/{room_id}/messages"
    headers = {
        "X-ChatWorkToken": Config.CHATWORK_API_TOKEN
    }
    data = {
        "body": message
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Chatwork: {e}")
        return None
