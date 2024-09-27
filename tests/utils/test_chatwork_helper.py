import pytest
from unittest.mock import patch, MagicMock
import requests
from src.utils.chatwork_api import send_message_to_room
from src.config import Config


@pytest.fixture
def mock_config():
    with patch('src.utils.chatwork_api.Config') as mock:
        mock.CHATWORK_API_TOKEN = 'fake_token'
        yield mock


def test_send_message_to_room_success(mock_config):
    with patch('src.utils.chatwork_api.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message_id": "1234"}
        mock_post.return_value = mock_response

        result = send_message_to_room("room_id", "Test message")
        assert result == {"message_id": "1234"}

        mock_post.assert_called_once_with(
            "https://api.chatwork.com/v2/rooms/room_id/messages",
            headers={"X-ChatWorkToken": "fake_token"},
            data={"body": "Test message"}
        )


def test_send_message_to_room_error(mock_config, caplog):
    with patch('src.utils.chatwork_api.requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.RequestException("API error")

        result = send_message_to_room("room_id", "Test message")

        assert result is None
        assert "Error sending message to Chatwork: API error" in caplog.text
