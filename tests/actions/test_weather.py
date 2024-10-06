import pytest
from unittest.mock import Mock, patch
from src.actions.action_weather import WeatherAction
from src.utils.web_utils import WebHelper


@pytest.fixture
def weather_action():
    return WeatherAction()


@pytest.fixture
def mock_web_helper():
    return Mock(spec=WebHelper)


@patch("src.actions.action_weather.requests.get")
def test_action_weather(mock_get, weather_action, mock_web_helper):
    # Mock the API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "Ho Chi Minh City",
        "sys": {"country": "VN"},
        "weather": [{"description": "cloudy"}],
        "main": {"temp": 86, "temp_min": 82, "temp_max": 89},
    }
    mock_get.return_value = mock_response

    # Mock the config values
    weather_action.get_config_value = Mock(side_effect=lambda x: "mock_value")

    # Mock the web_helper.query_ai method
    mock_web_helper.query_ai.return_value = "ho chi minh"

    message = weather_action.execute(
        "room_id", "account_id", "weather in ho chi minh", mock_web_helper
    )

    assert (
        "Current weather of Ho Chi Minh City (VN) is cloudy" in message
    ), "Expected city and weather description in response"
    assert "Temperature" in message, "Expected 'Temperature' to be in response"
    assert "°C" in message, "Expected '°C' to be in response"

    # Verify that the API was called with the correct parameters
    mock_get.assert_called_once_with(
        "mock_value/city/ho chi minh/EN",
        headers={
            "x-rapidapi-host": "open-weather13.p.rapidapi.com",
            "x-rapidapi-key": "mock_value",
        },
    )
