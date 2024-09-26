import pytest
from unittest.mock import MagicMock
from src.actions.action_weather import WeatherAction
from src.utils.web_utils import WebHelper


def test_weather_action():
    # Arrange
    mock_web_helper = MagicMock(spec=WebHelper)
    weather_action = WeatherAction()

    # Act
    result = weather_action.execute("room_id", "account_id", "What's the weather like?", mock_web_helper)

    # Assert
    assert "The weather in Tokyo is sunny" in result
    assert "25°C" in result
    assert "77°F" in result

# You might want to add more tests here for different scenarios,
# such as different locations or error handling, once the WeatherAction
# is implemented with actual API calls or more complex logic.
